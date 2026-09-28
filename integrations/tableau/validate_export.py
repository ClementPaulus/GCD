#!/usr/bin/env python3
"""Validate a Structura Reditus Tableau export bundle without changing source data."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

REQUIRED_TABLES = {
    "runs.csv",
    "contract_fields.csv",
    "kernel_observations.csv",
    "return_observations.csv",
    "trace_fields.csv",
    "missingness_events.csv",
    "seam_events.csv",
    "receipt_fields.csv",
    "casepacks.csv",
    "casepack_expected_invariants.csv",
    "relationships.csv",
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _is_finite_number(value: str) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def validate_export(bundle: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = bundle / "dataset_manifest.json"
    if not manifest_path.exists():
        return ["dataset_manifest.json is missing"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("evidence_origin") != "DERIVED_RESTATEMENT":
        errors.append("manifest evidence_origin must remain DERIVED_RESTATEMENT")
    if manifest.get("stance_boundary") != "The exporter derives no final stance and no weld verdict.":
        errors.append("manifest stance boundary changed or is missing")

    missing_tables = sorted(REQUIRED_TABLES - {path.name for path in bundle.glob("*.csv")})
    if missing_tables:
        errors.append(f"missing required tables: {', '.join(missing_tables)}")
        return errors

    runs = _read_csv(bundle / "runs.csv")
    run_keys = [row["run_key"] for row in runs]
    if len(run_keys) != len(set(run_keys)):
        errors.append("runs.csv contains duplicate run_key values")
    for row in runs:
        if row.get("authority_status") != "NO_PROMOTION_BY_EXPORT":
            errors.append(f"{row.get('run_key')}: authority_status changed")
        if row.get("semantic_status") != "SOURCE_DECLARED_UNASSESSED":
            errors.append(f"{row.get('run_key')}: semantic_status changed")

    for table_name in ["kernel_observations.csv", "return_observations.csv", "casepack_expected_invariants.csv"]:
        for index, row in enumerate(_read_csv(bundle / table_name), start=2):
            raw = row.get("tau_R_raw", "")
            numeric = row.get("tau_R_numeric", "")
            token_class = row.get("tau_R_token_class", "")
            if raw in {"INF_REC", "UNIDENTIFIABLE", "OOR"}:
                if numeric:
                    errors.append(f"{table_name}:{index}: typed return token was coerced to numeric")
                if token_class != raw:
                    errors.append(f"{table_name}:{index}: typed return token class was not preserved")
            elif numeric and not _is_finite_number(numeric):
                errors.append(f"{table_name}:{index}: numeric helper is not finite")

    trace_rows = _read_csv(bundle / "trace_fields.csv")
    for index, row in enumerate(trace_rows, start=2):
        if row.get("value_raw", "") == "" and row.get("value_numeric", "") != "":
            errors.append(f"trace_fields.csv:{index}: missing source value was imputed")

    seam_rows = _read_csv(bundle / "seam_events.csv")
    for index, row in enumerate(seam_rows, start=2):
        if row.get("weld_status") != "NOT_DERIVED_BY_EXPORT":
            errors.append(f"seam_events.csv:{index}: exporter asserted a weld")

    relationship_rows = _read_csv(bundle / "relationships.csv")
    declared_tables = {row["right_table"] for row in relationship_rows}
    expected_children = {
        "contract_fields",
        "kernel_observations",
        "return_observations",
        "trace_fields",
        "missingness_events",
        "seam_events",
        "receipt_fields",
        "casepack_expected_invariants",
    }
    if declared_tables != expected_children:
        errors.append("relationships.csv does not declare the expected logical-model children")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Directory produced by export_dataset.py")
    args = parser.parse_args()

    errors = validate_export(args.bundle)
    if errors:
        print("NONCONFORMANT export bundle")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CONFORMANT export bundle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
