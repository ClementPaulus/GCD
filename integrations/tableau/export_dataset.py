#!/usr/bin/env python3
"""Build a source-faithful Tableau dataset bundle from the GCD/UMCP repository.

The exporter is intentionally read-only with respect to the source repository. It does
not recompute Tier-1 values, derive stance, promote diagnostics, or reinterpret legacy
run-local semantics as current canon. It serializes the distinctions already present in
run artifacts and casepacks into Tableau-friendly CSV relations plus a manifest.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPORT_ID = "SR.TABLEAU.DATASET.v0.1"


@dataclass(frozen=True)
class SourceRun:
    run_dir: Path
    source_scope: str

    @property
    def manifest_path(self) -> Path:
        return self.run_dir / "manifest.json"

    @property
    def frozen_path(self) -> Path:
        return self.run_dir / "config" / "frozen.json"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    return value if isinstance(value, dict) else {"value": value}


def _stringify(value: Any) -> tuple[str, str]:
    if value is None:
        return "", "null"
    if isinstance(value, bool):
        return "true" if value else "false", "boolean"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not math.isfinite(value):
            return str(value), "number_nonfinite"
        return repr(value), "number"
    if isinstance(value, str):
        return value, "string"
    return json.dumps(value, sort_keys=True, separators=(",", ":")), "json"


def _flatten(value: Any, prefix: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(value, Mapping):
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            yield from _flatten(value[key], child)
        return
    if isinstance(value, list):
        # Lists are preserved as one JSON value. Expanding them by position would create
        # artificial row identity and can erase the fact that the source supplied one list.
        yield prefix, value
        return
    yield prefix, value


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
            count += 1
    return count


def _repo_commit(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "UNAVAILABLE"


def _iter_runs(root: Path, include_archive: bool) -> Iterator[SourceRun]:
    current = root / "runs"
    if current.exists():
        for run_dir in sorted(path for path in current.iterdir() if path.is_dir()):
            yield SourceRun(run_dir=run_dir, source_scope="current")
    if include_archive:
        archived = root / "archive" / "runs"
        if archived.exists():
            for run_dir in sorted(path for path in archived.iterdir() if path.is_dir()):
                yield SourceRun(run_dir=run_dir, source_scope="archive")


def _run_key(source_scope: str, run_id: str) -> str:
    return f"{source_scope}:{run_id}"


def _number_or_blank(raw: str) -> str:
    if raw is None:
        return ""
    value = raw.strip()
    if not value:
        return ""
    try:
        number = float(value)
    except ValueError:
        return ""
    if not math.isfinite(number):
        return ""
    return repr(number)


def _token_class(raw: str) -> str:
    value = (raw or "").strip()
    if value in {"INF_REC", "UNIDENTIFIABLE", "OOR"}:
        return value
    if _number_or_blank(value):
        return "NUMERIC"
    if not value:
        return "MISSING"
    return "SOURCE_TOKEN"


def _build_run_rows(root: Path, include_archive: bool) -> tuple[list[dict[str, Any]], list[SourceRun]]:
    rows: list[dict[str, Any]] = []
    runs = list(_iter_runs(root, include_archive))
    for source in runs:
        manifest = _load_json(source.manifest_path)
        frozen = _load_json(source.frozen_path)
        run_id = str(manifest.get("run_id") or frozen.get("run_id") or source.run_dir.name)
        casepack_id = str(manifest.get("casepack_id") or frozen.get("casepack_id") or "")
        contract_id = str(manifest.get("contract") or frozen.get("contract") or "")
        adapter = manifest.get("adapter") or frozen.get("adapter") or {}
        adapter_name = adapter.get("name", "") if isinstance(adapter, dict) else ""
        row = {
            "run_key": _run_key(source.source_scope, run_id),
            "run_id": run_id,
            "source_scope": source.source_scope,
            "casepack_id": casepack_id,
            "created_utc": manifest.get("created_utc", frozen.get("created_utc", "")),
            "contract_id": contract_id,
            "timezone": manifest.get("timezone", frozen.get("timezone", "")),
            "git_commit_declared": manifest.get("git_commit", frozen.get("git_commit", "")),
            "package_version_declared": manifest.get("package_version", frozen.get("package_version", "")),
            "pipeline": manifest.get("pipeline", frozen.get("pipeline", "")),
            "adapter_name": adapter_name,
            "semantic_status": "SOURCE_DECLARED_UNASSESSED",
            "authority_status": "NO_PROMOTION_BY_EXPORT",
            "evidence_origin": "DERIVED_RESTATEMENT",
            "manifest_path": str(source.manifest_path.relative_to(root)) if source.manifest_path.exists() else "",
            "frozen_path": str(source.frozen_path.relative_to(root)) if source.frozen_path.exists() else "",
            "has_kernel": (source.run_dir / "kernel" / "kernel.csv").exists(),
            "has_kernel_gate": (source.run_dir / "kernel" / "kernel_gate.csv").exists(),
            "has_return": (source.run_dir / "tables" / "tauR_series.csv").exists(),
            "has_seam": (source.run_dir / "seams" / "seam_ledger.csv").exists(),
            "has_receipt": (source.run_dir / "receipts" / "weld_receipt.json").exists(),
            "has_censor_log": (source.run_dir / "logs" / "censor.csv").exists(),
            "has_oor_log": (source.run_dir / "logs" / "oor.csv").exists(),
            "has_trace": (source.run_dir / "derived" / "psi.csv").exists(),
        }
        rows.append(row)
    return rows, runs


def _contract_rows(root: Path, runs: Iterable[SourceRun]) -> Iterator[dict[str, Any]]:
    for source in runs:
        manifest = _load_json(source.manifest_path)
        frozen = _load_json(source.frozen_path)
        run_id = str(manifest.get("run_id") or frozen.get("run_id") or source.run_dir.name)
        run_key = _run_key(source.source_scope, run_id)
        for source_name, source_path, payload in [
            ("manifest", source.manifest_path, manifest),
            ("frozen_contract", source.frozen_path, frozen),
        ]:
            if not payload:
                continue
            for field_path, value in _flatten(payload):
                value_text, value_type = _stringify(value)
                yield {
                    "run_key": run_key,
                    "run_id": run_id,
                    "source_scope": source.source_scope,
                    "source_kind": source_name,
                    "field_path": field_path,
                    "value": value_text,
                    "value_type": value_type,
                    "source_path": str(source_path.relative_to(root)),
                }


def _kernel_rows(root: Path, runs: Iterable[SourceRun]) -> Iterator[dict[str, Any]]:
    core = ["t", "omega", "F", "S", "C", "tau_R", "IC", "kappa", "kappa_cum"]
    for source in runs:
        manifest = _load_json(source.manifest_path)
        run_id = str(manifest.get("run_id") or source.run_dir.name)
        run_key = _run_key(source.source_scope, run_id)
        gate_path = source.run_dir / "kernel" / "kernel_gate.csv"
        kernel_path = source.run_dir / "kernel" / "kernel.csv"
        selected = gate_path if gate_path.exists() else kernel_path
        for index, row in enumerate(_read_csv(selected)):
            payload = {key: value for key, value in row.items() if key not in core}
            tau_raw = row.get("tau_R", "")
            yield {
                "run_key": run_key,
                "run_id": run_id,
                "source_scope": source.source_scope,
                "row_index": index,
                "t": row.get("t", ""),
                "omega": row.get("omega", ""),
                "F": row.get("F", ""),
                "S": row.get("S", ""),
                "C": row.get("C", ""),
                "tau_R_raw": tau_raw,
                "tau_R_numeric": _number_or_blank(tau_raw),
                "tau_R_token_class": _token_class(tau_raw),
                "IC": row.get("IC", ""),
                "kappa": row.get("kappa", ""),
                "kappa_cum": row.get("kappa_cum", ""),
                "source_regime": row.get("regime_gate", row.get("regime", "")),
                "source_payload_json": json.dumps(payload, sort_keys=True, separators=(",", ":")),
                "source_path": str(selected.relative_to(root)),
                "semantic_status": "SOURCE_DECLARED_UNASSESSED",
            }


def _return_rows(root: Path, runs: Iterable[SourceRun]) -> Iterator[dict[str, Any]]:
    for source in runs:
        manifest = _load_json(source.manifest_path)
        run_id = str(manifest.get("run_id") or source.run_dir.name)
        run_key = _run_key(source.source_scope, run_id)
        path = source.run_dir / "tables" / "tauR_series.csv"
        for index, row in enumerate(_read_csv(path)):
            tau_raw = row.get("tau_R", "")
            yield {
                "run_key": run_key,
                "run_id": run_id,
                "source_scope": source.source_scope,
                "row_index": index,
                "t": row.get("t", ""),
                "tau_R_raw": tau_raw,
                "tau_R_numeric": _number_or_blank(tau_raw),
                "tau_R_token_class": _token_class(tau_raw),
                "source_path": str(path.relative_to(root)),
                "semantic_status": "SOURCE_DECLARED_UNASSESSED",
            }


def _trace_rows(root: Path, runs: Iterable[SourceRun]) -> Iterator[dict[str, Any]]:
    for source in runs:
        manifest = _load_json(source.manifest_path)
        run_id = str(manifest.get("run_id") or source.run_dir.name)
        run_key = _run_key(source.source_scope, run_id)
        path = source.run_dir / "derived" / "psi.csv"
        for row_index, row in enumerate(_read_csv(path)):
            t_value = row.get("t", "")
            for field_name, raw in row.items():
                if field_name == "t":
                    continue
                yield {
                    "run_key": run_key,
                    "run_id": run_id,
                    "source_scope": source.source_scope,
                    "row_index": row_index,
                    "t": t_value,
                    "field_name": field_name,
                    "value_raw": raw,
                    "value_numeric": _number_or_blank(raw),
                    "source_path": str(path.relative_to(root)),
                }


def _missingness_rows(root: Path, runs: Iterable[SourceRun]) -> Iterator[dict[str, Any]]:
    for source in runs:
        manifest = _load_json(source.manifest_path)
        run_id = str(manifest.get("run_id") or source.run_dir.name)
        run_key = _run_key(source.source_scope, run_id)
        for kind, filename, flag_name in [
            ("CENSOR", "censor.csv", "censored"),
            ("OOR", "oor.csv", "oor"),
        ]:
            path = source.run_dir / "logs" / filename
            for row_index, row in enumerate(_read_csv(path)):
                yield {
                    "run_key": run_key,
                    "run_id": run_id,
                    "source_scope": source.source_scope,
                    "row_index": row_index,
                    "t": row.get("t", ""),
                    "channel": row.get("channel", ""),
                    "missingness_kind": kind,
                    "flag_raw": row.get(flag_name, ""),
                    "rate_raw": row.get("rate", ""),
                    "source_path": str(path.relative_to(root)),
                }


def _seam_rows(root: Path, runs: Iterable[SourceRun]) -> Iterator[dict[str, Any]]:
    for source in runs:
        manifest = _load_json(source.manifest_path)
        run_id = str(manifest.get("run_id") or source.run_dir.name)
        run_key = _run_key(source.source_scope, run_id)
        path = source.run_dir / "seams" / "seam_ledger.csv"
        for row_index, row in enumerate(_read_csv(path)):
            seam_id = row.get("seam_id", str(row_index))
            yield {
                "run_key": run_key,
                "run_id": run_id,
                "source_scope": source.source_scope,
                "row_index": row_index,
                "seam_id": seam_id,
                "source_type": row.get("type", ""),
                "t_raw": row.get("t", row.get("t_s", "")),
                "payload_json": json.dumps(row, sort_keys=True, separators=(",", ":")),
                "source_path": str(path.relative_to(root)),
                "weld_status": "NOT_DERIVED_BY_EXPORT",
            }


def _receipt_rows(root: Path, runs: Iterable[SourceRun]) -> Iterator[dict[str, Any]]:
    for source in runs:
        manifest = _load_json(source.manifest_path)
        run_id = str(manifest.get("run_id") or source.run_dir.name)
        run_key = _run_key(source.source_scope, run_id)
        path = source.run_dir / "receipts" / "weld_receipt.json"
        payload = _load_json(path)
        for field_path, value in _flatten(payload):
            value_text, value_type = _stringify(value)
            yield {
                "run_key": run_key,
                "run_id": run_id,
                "source_scope": source.source_scope,
                "field_path": field_path,
                "value": value_text,
                "value_type": value_type,
                "source_path": str(path.relative_to(root)) if path.exists() else "",
                "authority_status": "SOURCE_RECEIPT_ONLY",
            }


def _casepack_rows(root: Path) -> tuple[list[dict[str, Any]], list[Path]]:
    rows: list[dict[str, Any]] = []
    manifests: list[Path] = []
    casepacks_dir = root / "casepacks"
    if not casepacks_dir.exists():
        return rows, manifests
    for casepack_dir in sorted(path for path in casepacks_dir.iterdir() if path.is_dir()):
        manifest_path = casepack_dir / "manifest.json"
        if not manifest_path.exists():
            continue
        manifest = _load_json(manifest_path)
        manifests.append(manifest_path)
        cp = manifest.get("casepack", {}) if isinstance(manifest.get("casepack"), dict) else {}
        refs = manifest.get("refs", {}) if isinstance(manifest.get("refs"), dict) else {}
        contract = refs.get("contract", {}) if isinstance(refs.get("contract"), dict) else {}
        closures = refs.get("closures_registry", {}) if isinstance(refs.get("closures_registry"), dict) else {}
        casepack_id = str(cp.get("id") or casepack_dir.name)
        expected_path = casepack_dir / "expected" / "invariants.json"
        rows.append(
            {
                "casepack_id": casepack_id,
                "version": cp.get("version", ""),
                "title": cp.get("title", ""),
                "description": cp.get("description", ""),
                "created_utc": cp.get("created_utc", ""),
                "timezone": cp.get("timezone", ""),
                "contract_id": contract.get("id", ""),
                "closure_registry_id": closures.get("id", ""),
                "manifest_path": str(manifest_path.relative_to(root)),
                "expected_invariants_path": str(expected_path.relative_to(root)) if expected_path.exists() else "",
                "semantic_status": "SOURCE_DECLARED_UNASSESSED",
                "authority_status": "NO_PROMOTION_BY_EXPORT",
            }
        )
    return rows, manifests


def _casepack_invariant_rows(root: Path, manifests: Iterable[Path]) -> Iterator[dict[str, Any]]:
    for manifest_path in manifests:
        manifest = _load_json(manifest_path)
        cp = manifest.get("casepack", {}) if isinstance(manifest.get("casepack"), dict) else {}
        casepack_id = str(cp.get("id") or manifest_path.parent.name)
        path = manifest_path.parent / "expected" / "invariants.json"
        payload = _load_json(path)
        rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
        for row_index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            regime = row.get("regime", {}) if isinstance(row.get("regime"), dict) else {}
            tau_raw = str(row.get("tau_R", ""))
            yield {
                "casepack_id": casepack_id,
                "row_index": row_index,
                "t": row.get("t", ""),
                "omega": row.get("omega", ""),
                "F": row.get("F", ""),
                "S": row.get("S", ""),
                "C": row.get("C", ""),
                "tau_R_raw": tau_raw,
                "tau_R_numeric": _number_or_blank(tau_raw),
                "tau_R_token_class": _token_class(tau_raw),
                "kappa": row.get("kappa", ""),
                "IC": row.get("IC", ""),
                "source_regime": regime.get("label", row.get("regime", "")),
                "source_critical_overlay": regime.get("critical_overlay", ""),
                "source_payload_json": json.dumps(row, sort_keys=True, separators=(",", ":")),
                "source_path": str(path.relative_to(root)),
                "semantic_status": "SOURCE_DECLARED_UNASSESSED",
            }


def export_dataset(root: Path, output_dir: Path, include_archive: bool = True) -> dict[str, Any]:
    root = root.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    run_rows, runs = _build_run_rows(root, include_archive)
    casepack_rows, casepack_manifests = _casepack_rows(root)

    counts: dict[str, int] = {}
    counts["runs"] = _write_csv(
        output_dir / "runs.csv",
        [
            "run_key",
            "run_id",
            "source_scope",
            "casepack_id",
            "created_utc",
            "contract_id",
            "timezone",
            "git_commit_declared",
            "package_version_declared",
            "pipeline",
            "adapter_name",
            "semantic_status",
            "authority_status",
            "evidence_origin",
            "manifest_path",
            "frozen_path",
            "has_kernel",
            "has_kernel_gate",
            "has_return",
            "has_seam",
            "has_receipt",
            "has_censor_log",
            "has_oor_log",
            "has_trace",
        ],
        run_rows,
    )
    counts["contract_fields"] = _write_csv(
        output_dir / "contract_fields.csv",
        ["run_key", "run_id", "source_scope", "source_kind", "field_path", "value", "value_type", "source_path"],
        _contract_rows(root, runs),
    )
    counts["kernel_observations"] = _write_csv(
        output_dir / "kernel_observations.csv",
        [
            "run_key",
            "run_id",
            "source_scope",
            "row_index",
            "t",
            "omega",
            "F",
            "S",
            "C",
            "tau_R_raw",
            "tau_R_numeric",
            "tau_R_token_class",
            "IC",
            "kappa",
            "kappa_cum",
            "source_regime",
            "source_payload_json",
            "source_path",
            "semantic_status",
        ],
        _kernel_rows(root, runs),
    )
    counts["return_observations"] = _write_csv(
        output_dir / "return_observations.csv",
        [
            "run_key",
            "run_id",
            "source_scope",
            "row_index",
            "t",
            "tau_R_raw",
            "tau_R_numeric",
            "tau_R_token_class",
            "source_path",
            "semantic_status",
        ],
        _return_rows(root, runs),
    )
    counts["trace_fields"] = _write_csv(
        output_dir / "trace_fields.csv",
        ["run_key", "run_id", "source_scope", "row_index", "t", "field_name", "value_raw", "value_numeric", "source_path"],
        _trace_rows(root, runs),
    )
    counts["missingness_events"] = _write_csv(
        output_dir / "missingness_events.csv",
        [
            "run_key",
            "run_id",
            "source_scope",
            "row_index",
            "t",
            "channel",
            "missingness_kind",
            "flag_raw",
            "rate_raw",
            "source_path",
        ],
        _missingness_rows(root, runs),
    )
    counts["seam_events"] = _write_csv(
        output_dir / "seam_events.csv",
        [
            "run_key",
            "run_id",
            "source_scope",
            "row_index",
            "seam_id",
            "source_type",
            "t_raw",
            "payload_json",
            "source_path",
            "weld_status",
        ],
        _seam_rows(root, runs),
    )
    counts["receipt_fields"] = _write_csv(
        output_dir / "receipt_fields.csv",
        [
            "run_key",
            "run_id",
            "source_scope",
            "field_path",
            "value",
            "value_type",
            "source_path",
            "authority_status",
        ],
        _receipt_rows(root, runs),
    )
    counts["casepacks"] = _write_csv(
        output_dir / "casepacks.csv",
        [
            "casepack_id",
            "version",
            "title",
            "description",
            "created_utc",
            "timezone",
            "contract_id",
            "closure_registry_id",
            "manifest_path",
            "expected_invariants_path",
            "semantic_status",
            "authority_status",
        ],
        casepack_rows,
    )
    counts["casepack_expected_invariants"] = _write_csv(
        output_dir / "casepack_expected_invariants.csv",
        [
            "casepack_id",
            "row_index",
            "t",
            "omega",
            "F",
            "S",
            "C",
            "tau_R_raw",
            "tau_R_numeric",
            "tau_R_token_class",
            "kappa",
            "IC",
            "source_regime",
            "source_critical_overlay",
            "source_payload_json",
            "source_path",
            "semantic_status",
        ],
        _casepack_invariant_rows(root, casepack_manifests),
    )

    relationships = [
        {"left_table": "runs", "left_key": "run_key", "right_table": name, "right_key": "run_key", "cardinality": "1:M"}
        for name in [
            "contract_fields",
            "kernel_observations",
            "return_observations",
            "trace_fields",
            "missingness_events",
            "seam_events",
            "receipt_fields",
        ]
    ]
    relationships.append(
        {
            "left_table": "casepacks",
            "left_key": "casepack_id",
            "right_table": "casepack_expected_invariants",
            "right_key": "casepack_id",
            "cardinality": "1:M",
        }
    )
    counts["relationships"] = _write_csv(
        output_dir / "relationships.csv",
        ["left_table", "left_key", "right_table", "right_key", "cardinality"],
        relationships,
    )

    manifest = {
        "dataset_id": EXPORT_ID,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "repository_commit": _repo_commit(root),
        "source_root": str(root),
        "include_archive": include_archive,
        "evidence_origin": "DERIVED_RESTATEMENT",
        "semantic_boundary": (
            "Source rows are preserved under their declared local semantics. The export does not assert current "
            "Tier-1/Tier-0 compatibility, does not reconcile historical conventions, and does not promote repository "
            "presence into authority."
        ),
        "return_boundary": (
            "tau_R tokens are preserved verbatim. INF_REC, UNIDENTIFIABLE, OOR, numeric values, missing values, "
            "and other source tokens remain distinguishable."
        ),
        "missingness_boundary": "Missing values and missingness logs are not imputed as zero.",
        "stance_boundary": "The exporter derives no final stance and no weld verdict.",
        "table_counts": counts,
        "tables": sorted([path.name for path in output_dir.glob("*.csv")]),
    }
    with (output_dir / "dataset_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return manifest


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="GCD repository root")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for the Tableau CSV bundle")
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Exclude archive/runs. Default is to retain archived runs with source_scope=archive.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest = export_dataset(args.repo_root, args.output_dir, include_archive=not args.no_archive)
    print(json.dumps({"dataset_id": manifest["dataset_id"], "table_counts": manifest["table_counts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
