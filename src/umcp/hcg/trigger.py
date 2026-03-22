"""
Validation Trigger — Bridges the validation pipeline to the webhook orchestrator.

When ``umcp validate`` produces a CONFORMANT verdict, the trigger fires the
webhook orchestrator to rebuild the affected domain's static site.  This is
the "autonomous rebuild" mechanism in the HCG architecture.

The trigger can operate in three modes:
    1. **Post-validation hook**: Called programmatically after validation
    2. **Ledger watcher**: Polls or tails the ledger for new CONFORMANT rows
    3. **CLI one-shot**: Manual fire for testing / admin use

Integration points:
    - ``api_umcp.py`` calls ``fire_on_conformant()`` after a validation endpoint
    - ``cli.py`` calls ``fire_on_conformant()`` after ``umcp validate``
    - GitHub Actions uses ``repository_dispatch`` event type ``hcg-rebuild-*``

Usage:
    from umcp.hcg.trigger import ValidationTrigger

    trigger = ValidationTrigger.from_env()
    trigger.fire_on_conformant("finance", kernel_snapshot={...})
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from umcp.hcg.webhook import WebhookOrchestrator, WebhookResult

logger = logging.getLogger(__name__)


@dataclass
class TriggerEvent:
    """Record of a single trigger firing."""

    timestamp: str
    domain: str
    verdict: str  # CONFORMANT | NONCONFORMANT | NON_EVALUABLE
    fired: bool  # whether webhooks were actually dispatched
    results: list[WebhookResult] = field(default_factory=list)
    kernel_snapshot: dict[str, Any] = field(default_factory=dict)


class ValidationTrigger:
    """Bridges validation verdicts to HCG webhook rebuilds.

    Holds a ``WebhookOrchestrator`` and fires it when a CONFORMANT verdict
    arrives.  Non-CONFORMANT verdicts are logged but do not trigger rebuilds
    (you don't publish broken state).
    """

    def __init__(
        self,
        orchestrator: WebhookOrchestrator | None = None,
        *,
        enabled: bool = True,
        dry_run: bool = False,
    ) -> None:
        self._orchestrator = orchestrator or WebhookOrchestrator()
        self._enabled = enabled
        self._dry_run = dry_run
        self._history: list[TriggerEvent] = []

    @classmethod
    def from_env(cls) -> ValidationTrigger:
        """Create a trigger with targets auto-discovered from env vars.

        Reads HCG_WEBHOOK_<NAME>_URL etc. and HCG_TRIGGER_ENABLED.
        See ``WebhookOrchestrator.add_target_from_env()`` for env format.
        """
        import os

        orch = WebhookOrchestrator()
        orch.add_target_from_env()

        enabled = os.environ.get("HCG_TRIGGER_ENABLED", "true").lower() in (
            "true",
            "1",
            "yes",
        )
        dry_run = os.environ.get("HCG_TRIGGER_DRY_RUN", "false").lower() in (
            "true",
            "1",
            "yes",
        )

        return cls(orch, enabled=enabled, dry_run=dry_run)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @property
    def history(self) -> list[TriggerEvent]:
        """Return firing history (read-only copy)."""
        return list(self._history)

    def fire_on_conformant(
        self,
        domain: str,
        kernel_snapshot: dict[str, Any] | None = None,
        *,
        verdict: str = "CONFORMANT",
    ) -> TriggerEvent:
        """Fire webhooks if verdict is CONFORMANT.

        Parameters
        ----------
        domain : str
            The domain that was validated (e.g. "finance").
        kernel_snapshot : dict, optional
            Kernel invariants (F, ω, S, C, κ, IC, regime, Δ) to include
            in the webhook payload.
        verdict : str
            The validation verdict. Only CONFORMANT triggers a rebuild.

        Returns
        -------
        TriggerEvent
            Record of what happened.
        """
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        event = TriggerEvent(
            timestamp=ts,
            domain=domain,
            verdict=verdict,
            fired=False,
            kernel_snapshot=kernel_snapshot or {},
        )

        if verdict != "CONFORMANT":
            logger.info(
                "Trigger skip: domain=%s verdict=%s (only CONFORMANT fires)",
                domain,
                verdict,
            )
            self._history.append(event)
            return event

        if not self._enabled:
            logger.info("Trigger disabled: domain=%s would have fired", domain)
            self._history.append(event)
            return event

        # Build payload with kernel data + domain metadata
        payload: dict[str, Any] = {
            "verdict": verdict,
            "kernel": kernel_snapshot or {},
        }

        results = self._orchestrator.fire(
            domain,
            payload=payload,
            dry_run=self._dry_run,
        )

        event.fired = len(results) > 0
        event.results = results
        self._history.append(event)

        success_count = sum(1 for r in results if r.success)
        logger.info(
            "Trigger fired: domain=%s verdict=%s targets=%d success=%d",
            domain,
            verdict,
            len(results),
            success_count,
        )

        return event

    def fire_from_ledger_row(
        self,
        row: dict[str, Any],
        domain: str | None = None,
    ) -> TriggerEvent:
        """Fire from a parsed ledger row dict.

        Extracts verdict and kernel snapshot from the row and delegates
        to ``fire_on_conformant()``.
        """
        verdict = row.get("run_status", "NON_EVALUABLE")
        snapshot = {
            "F": row.get("F"),
            "omega": row.get("omega"),
            "S": row.get("S"),
            "C": row.get("C"),
            "kappa": row.get("kappa"),
            "IC": row.get("IC"),
        }
        # Filter None values
        snapshot = {k: v for k, v in snapshot.items() if v is not None}

        # Domain detection: if not specified, try to infer from row metadata
        if domain is None:
            domain = row.get("domain", "unknown")

        return self.fire_on_conformant(
            domain=domain or "unknown",
            kernel_snapshot=snapshot,
            verdict=verdict,
        )


class LedgerWatcher:
    """Watches the ledger file for new CONFORMANT entries and fires triggers.

    This is a lightweight polling watcher — not a daemon.  Call ``check()``
    periodically or use ``watch()`` for a blocking loop.
    """

    def __init__(
        self,
        trigger: ValidationTrigger,
        ledger_path: Path | str | None = None,
    ) -> None:
        self._trigger = trigger
        if ledger_path is None:
            from umcp.hcg.extractor import _repo_root

            ledger_path = _repo_root() / "ledger" / "return_log.csv"
        self._ledger_path = Path(ledger_path)
        self._last_line_count = 0
        self._initialized = False

    def _count_lines(self) -> int:
        """Count lines in ledger file."""
        if not self._ledger_path.exists():
            return 0
        with open(self._ledger_path, encoding="utf-8") as f:
            return sum(1 for _ in f)

    def _read_new_rows(self) -> list[dict[str, Any]]:
        """Read rows added since last check."""
        import csv

        if not self._ledger_path.exists():
            return []

        rows: list[dict[str, Any]] = []
        with open(self._ledger_path, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            if header is None:
                return []

            for i, line in enumerate(reader, start=1):
                if i <= self._last_line_count - 1:  # -1 for header
                    continue
                if len(line) < 8:
                    continue
                rows.append(
                    {
                        "timestamp": line[0],
                        "run_status": line[1],
                        "F": float(line[2]) if line[2] else None,
                        "omega": float(line[3]) if line[3] else None,
                        "kappa": float(line[4]) if line[4] else None,
                        "IC": float(line[5]) if line[5] else None,
                        "C": float(line[6]) if line[6] else None,
                        "S": float(line[7]) if line[7] else None,
                    }
                )

        return rows

    def check(self, domain: str = "unknown") -> list[TriggerEvent]:
        """Check for new ledger entries and fire triggers.

        Returns list of trigger events for new CONFORMANT rows.
        """
        current_lines = self._count_lines()

        if not self._initialized:
            # First call: set baseline without firing
            self._last_line_count = current_lines
            self._initialized = True
            logger.info(
                "LedgerWatcher initialized: %d existing rows",
                current_lines - 1,  # -1 for header
            )
            return []

        if current_lines <= self._last_line_count:
            return []

        new_rows = self._read_new_rows()
        self._last_line_count = current_lines

        events: list[TriggerEvent] = []
        for row in new_rows:
            event = self._trigger.fire_from_ledger_row(row, domain=domain)
            events.append(event)

        return events

    def watch(
        self,
        domain: str = "unknown",
        interval_seconds: float = 5.0,
        max_iterations: int = 0,
    ) -> None:
        """Blocking poll loop — check ledger every *interval_seconds*.

        Parameters
        ----------
        domain : str
            Domain to attribute new rows to.
        interval_seconds : float
            Seconds between checks.
        max_iterations : int
            Stop after this many iterations. 0 = infinite.
        """
        logger.info(
            "LedgerWatcher starting: path=%s interval=%.1fs",
            self._ledger_path,
            interval_seconds,
        )
        iteration = 0
        while True:
            events = self.check(domain=domain)
            for ev in events:
                if ev.fired:
                    logger.info(
                        "Fired %d webhooks for %s (%s)",
                        len(ev.results),
                        ev.domain,
                        ev.verdict,
                    )

            iteration += 1
            if max_iterations and iteration >= max_iterations:
                break

            time.sleep(interval_seconds)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """CLI for the validation trigger."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="hcg-trigger",
        description="HCG Validation Trigger — Fire webhooks on CONFORMANT events",
    )
    sub = parser.add_subparsers(dest="command")

    # fire: one-shot trigger
    fire_cmd = sub.add_parser("fire", help="Fire a manual trigger")
    fire_cmd.add_argument("domain", help="Domain to trigger rebuild for")
    fire_cmd.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually send requests",
    )

    # watch: polling loop
    watch_cmd = sub.add_parser("watch", help="Watch ledger for new entries")
    watch_cmd.add_argument(
        "--domain",
        "-d",
        default="unknown",
        help="Domain to attribute new rows to",
    )
    watch_cmd.add_argument(
        "--interval",
        "-i",
        type=float,
        default=5.0,
        help="Seconds between checks (default: 5)",
    )

    # status: show current targets
    sub.add_parser("status", help="Show registered webhook targets")

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if getattr(args, "verbose", False) else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    trigger = ValidationTrigger.from_env()

    if args.command == "fire":
        event = trigger.fire_on_conformant(
            domain=args.domain,
            verdict="CONFORMANT",
        )
        if event.fired:
            for r in event.results:
                status = "OK" if r.success else f"FAIL ({r.error})"
                print(f"  {r.target_name}: {status} ({r.elapsed_ms:.0f}ms)")
        else:
            print("No webhook targets matched or trigger disabled.")
        return 0

    if args.command == "watch":
        watcher = LedgerWatcher(trigger)
        watcher.watch(
            domain=args.domain,
            interval_seconds=args.interval,
        )
        return 0

    if args.command == "status":
        orch_targets = trigger._orchestrator.targets
        if not orch_targets:
            print("No webhook targets configured.")
            print("Set HCG_WEBHOOK_<NAME>_URL environment variables.")
        else:
            print(f"{len(orch_targets)} webhook target(s):")
            for t in orch_targets:
                domains = ", ".join(t.domains) if t.domains else "all"
                enabled = "enabled" if t.enabled else "disabled"
                print(f"  {t.name:20s} {t.kind:10s} {domains:30s} {enabled}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
