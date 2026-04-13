from __future__ import annotations

import csv
import uuid
from pathlib import Path
from typing import Any

import numpy as np

from .corpus_resolver import CORPUS_RESOLVER
from .run_store import RUN_STORE
from .session_store import SESSION_STORE
from .types import RunArtifact, RunRecord, StartCasepackRunRequest, StartCasepackRunResponse


class CasepackService:
    def start_run(self, casepack_id: str, payload: StartCasepackRunRequest) -> StartCasepackRunResponse:
        session = SESSION_STORE.get(payload.sessionId)
        if session is None:
            raise KeyError(f"Unknown session: {payload.sessionId}")

        obj = CORPUS_RESOLVER.get_object("casepack", casepack_id).object
        casepack_path = self._resolve_casepack_path(obj)

        contract_id = payload.contractId or session.activeContractId or "UMA.INTSTACK.v1"
        run_id = f"run_{uuid.uuid4().hex[:12]}"

        run = RunRecord(
            runId=run_id,
            status="queued",
            casepackId=casepack_id,
            contractId=contract_id,
        )
        RUN_STORE.create(run)

        completed = self._execute_casepack(run, casepack_path)
        RUN_STORE.save(completed)

        session.currentRunId = completed.runId
        session.activeCasepackId = casepack_id
        SESSION_STORE.save(session)

        return StartCasepackRunResponse(runId=completed.runId, status=completed.status)

    def get_run(self, run_id: str) -> RunRecord:
        run = RUN_STORE.get(run_id)
        if run is None:
            raise KeyError(f"Unknown run: {run_id}")
        return run

    def _resolve_casepack_path(self, obj: Any) -> Path:
        """
        Resolve a casepack object from corpus metadata to an on-disk path.
        Current corpus registry uses body.path = 'casepacks/<name>'.
        """
        body = obj.body if hasattr(obj, "body") else {}
        if not isinstance(body, dict):
            raise KeyError(f"Casepack object has no usable path metadata: {obj.id}")

        raw_path = body.get("path")
        if not isinstance(raw_path, str):
            raise KeyError(f"Casepack object missing body.path: {obj.id}")

        path = Path(raw_path)
        if path.exists():
            return path.resolve()

        # Fallback: try relative to repo root
        repo_root = self._find_repo_root(Path.cwd())
        if repo_root is not None:
            candidate = (repo_root / raw_path).resolve()
            if candidate.exists():
                return candidate

        raise KeyError(f"Casepack path does not exist: {raw_path}")

    def _find_repo_root(self, start: Path) -> Path | None:
        cur = start.resolve()
        if cur.is_file():
            cur = cur.parent
        for p in [cur, *cur.parents]:
            if (p / "pyproject.toml").exists():
                return p
        return None

    def _execute_casepack(self, run: RunRecord, casepack_path: Path) -> RunRecord:
        """
        Authoritative hello_world adapter:
        - validate via the real UMCP Python API
        - hydrate invariants via the documented MeasurementEngine path

        Generalization path:
        - for non-hello_world casepacks, first use validate(...) for authoritative verdict
        - then either:
          (a) parse expected/invariants.json if present, or
          (b) parse contracts/embedding.yaml + weights.yaml and feed raw data into MeasurementEngine
        """
        try:
            # 1) Authoritative verdict path
            from umcp import validate

            validation_result = validate(str(casepack_path))
            verdict = getattr(validation_result, "status", None) or getattr(validation_result, "run_status", None)
            verdict = str(verdict or "NON_EVALUABLE")
        except Exception as exc:
            run.status = "failed"
            run.error = f"Validation adapter failed: {exc}"
            run.stance = {
                "verdict": "NON_EVALUABLE",
                "regime": None,
                "critical": False,
                "rationale": [run.error],
            }
            return run

        if run.casepackId == "hello_world":
            try:
                engine_payload = self._run_hello_world_measurement_engine(casepack_path)

                row = engine_payload["row"]
                raw = engine_payload["raw"]

                F = float(row.F)
                omega = float(row.omega)
                S = float(row.S)
                C = float(row.C)
                kappa = float(row.kappa)
                IC = float(row.IC)
                regime = str(getattr(row, "regime", "")) or None

                run.status = "completed" if verdict != "NONCONFORMANT" else "failed"
                run.invariants = {
                    "F": F,
                    "omega": omega,
                    "S": S,
                    "C": C,
                    "kappa": kappa,
                    "IC": IC,
                }
                run.stance = {
                    "verdict": verdict,
                    "regime": regime,
                    "critical": IC < 0.30,
                    "rationale": [
                        "Verdict derived from the authoritative UMCP validate(...) path.",
                        "Invariants hydrated via MeasurementEngine.from_array(...) using LINEAR_SCALE over [0,10].",
                        f"Loaded raw trace shape: {tuple(raw.shape)}.",
                    ],
                }
                run.artifacts = [
                    RunArtifact(name="manifest.json"),
                    RunArtifact(name="raw_measurements.csv"),
                    RunArtifact(name="expected/invariants.json"),
                    RunArtifact(name="expected/psi.csv"),
                    RunArtifact(name="expected/ss1m_receipt.json"),
                ]
                return run

            except Exception as exc:
                run.status = "failed"
                run.error = f"MeasurementEngine hydration failed: {exc}"
                run.stance = {
                    "verdict": "NON_EVALUABLE",
                    "regime": None,
                    "critical": False,
                    "rationale": [
                        "Validation succeeded or was attempted, but invariant hydration failed.",
                        run.error,
                    ],
                }
                return run

        # Generalized fallback for non-hello_world casepacks:
        # authoritative verdict first, invariant hydration later.
        run.status = "completed" if verdict != "NONCONFORMANT" else "failed"
        run.invariants = None
        run.stance = {
            "verdict": verdict,
            "regime": None,
            "critical": False,
            "rationale": [
                "Authoritative verdict derived from validate(casepack_path).",
                "Invariant hydration for non-hello_world casepacks is the next generalization step.",
            ],
        }
        run.artifacts = [RunArtifact(name="manifest.json")]
        return run

    def _run_hello_world_measurement_engine(self, casepack_path: Path) -> dict[str, Any]:
        """
        Exact worked-example path documented in The First Pass:
        raw = [[9.9, 9.9, 9.9]]
        embedding = LINEAR_SCALE over input_range (0,10)
        weights = [1/3, 1/3, 1/3]
        """
        from umcp.measurement_engine import (
            EmbeddingConfig,
            EmbeddingSpec,
            EmbeddingStrategy,
            MeasurementEngine,
        )

        raw_path = casepack_path / "raw_measurements.csv"
        if not raw_path.exists():
            raise FileNotFoundError(f"Missing raw measurements: {raw_path}")

        rows: list[list[float]] = []
        import contextlib

        with raw_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header

            for row in reader:
                numeric = []
                for cell in row:
                    cell = cell.strip()
                    if not cell:
                        continue
                    with contextlib.suppress(ValueError):
                        numeric.append(float(cell))
                if numeric:
                    rows.append(numeric)

        if not rows:
            raise ValueError("No numeric raw measurements found in hello_world casepack.")

        raw = np.array(rows, dtype=float)
        n_channels = raw.shape[1]

        spec = EmbeddingSpec(
            strategy=EmbeddingStrategy.LINEAR_SCALE,
            input_range=(0, 10),
        )
        embedding = EmbeddingConfig(specs=[spec] * n_channels)
        weights = [1.0 / n_channels] * n_channels

        engine = MeasurementEngine()
        result = engine.from_array(raw, weights=weights, embedding=embedding)
        row = result.invariants[0]

        return {
            "raw": raw,
            "result": result,
            "row": row,
        }


CASEPACK_SERVICE = CasepackService()
