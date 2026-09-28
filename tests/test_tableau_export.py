from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_tableau_export_preserves_return_and_missingness_distinctions(tmp_path: Path) -> None:
    repo = tmp_path / "fixture"
    run = repo / "runs" / "R1"

    _write(
        run / "manifest.json",
        json.dumps(
            {
                "run_id": "R1",
                "casepack_id": "CP1",
                "contract": "C1",
                "tier1_identities": {"note": "source-local"},
            }
        ),
    )
    _write(run / "config" / "frozen.json", '{"run_id":"R1","missingness_policy":"preserve"}\n')
    _write(
        run / "kernel" / "kernel.csv",
        "t,omega,F,S,C,tau_R,IC,kappa,kappa_cum\n"
        "0,0.1,0.9,0.2,0.1,INF_REC,0.8,-0.2,-0.2\n"
        "1,0.2,0.8,0.3,0.2,2,0.7,-0.3,-0.5\n",
    )
    _write(run / "tables" / "tauR_series.csv", "t,tau_R\n0,INF_REC\n1,2\n")
    _write(run / "derived" / "psi.csv", "t,a,b\n0,0.1,\n1,0.2,0.4\n")
    _write(run / "logs" / "censor.csv", "t,channel,censored,rate\n0,a,1,\n")
    _write(run / "logs" / "oor.csv", "t,channel,oor,rate\n0,b,1,\n")
    _write(run / "seams" / "seam_ledger.csv", "seam_id,type,t_s,residual\nS1,test,1,0.001\n")
    _write(run / "receipts" / "weld_receipt.json", '{"seam_id":"S1","result":"SOURCE_ONLY"}\n')

    casepack = repo / "casepacks" / "CP1"
    _write(
        casepack / "manifest.json",
        '{"casepack":{"id":"CP1","version":"1.0","title":"Fixture"},'
        '"refs":{"contract":{"id":"C1"},"closures_registry":{"id":"CL1"}}}\n',
    )
    _write(
        casepack / "expected" / "invariants.json",
        '{"rows":[{"t":0,"omega":0.1,"F":0.9,"S":0.2,"C":0.1,'
        '"tau_R":"INF_REC","kappa":-0.2,"IC":0.8,'
        '"regime":{"label":"Watch","critical_overlay":false}}]}\n',
    )

    project_root = Path(__file__).resolve().parents[1]
    script = project_root / "integrations" / "tableau" / "export_dataset.py"
    output = tmp_path / "out"
    subprocess.run(
        [sys.executable, str(script), "--repo-root", str(repo), "--output-dir", str(output)],
        check=True,
        cwd=project_root,
    )

    returns = _read_csv(output / "return_observations.csv")
    assert returns[0]["tau_R_raw"] == "INF_REC"
    assert returns[0]["tau_R_numeric"] == ""
    assert returns[0]["tau_R_token_class"] == "INF_REC"
    assert returns[1]["tau_R_numeric"] == "2.0"
    assert returns[1]["tau_R_token_class"] == "NUMERIC"

    trace = _read_csv(output / "trace_fields.csv")
    missing_b = next(row for row in trace if row["row_index"] == "0" and row["field_name"] == "b")
    assert missing_b["value_raw"] == ""
    assert missing_b["value_numeric"] == ""

    missingness = _read_csv(output / "missingness_events.csv")
    assert {row["missingness_kind"] for row in missingness} == {"CENSOR", "OOR"}

    runs = _read_csv(output / "runs.csv")
    assert runs[0]["semantic_status"] == "SOURCE_DECLARED_UNASSESSED"
    assert runs[0]["authority_status"] == "NO_PROMOTION_BY_EXPORT"
    assert runs[0]["evidence_origin"] == "DERIVED_RESTATEMENT"

    seams = _read_csv(output / "seam_events.csv")
    assert seams[0]["weld_status"] == "NOT_DERIVED_BY_EXPORT"

    casepack_rows = _read_csv(output / "casepack_expected_invariants.csv")
    assert casepack_rows[0]["source_regime"] == "Watch"
    assert casepack_rows[0]["tau_R_token_class"] == "INF_REC"

    manifest = json.loads((output / "dataset_manifest.json").read_text(encoding="utf-8"))
    assert manifest["evidence_origin"] == "DERIVED_RESTATEMENT"
    assert manifest["table_counts"]["runs"] == 1
    assert manifest["table_counts"]["casepacks"] == 1
