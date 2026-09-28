# Structura Reditus Tableau datasource export

This directory provides a source-faithful export layer between the GCD/UMCP repository and Tableau.
It is an integration surface, not a new kernel, closure, validator, return rule, seam rule, or stance engine.

## Burden

Produce a reproducible Tableau-ready dataset without collapsing distinctions that matter to the active
Structura Reditus / UMCP readback. The exporter preserves run identity, source scope, contract fields,
source-declared kernel rows, typed return tokens, trace fields, missingness logs, seam records, receipts,
and casepack metadata as separate relations.

The export is **derived restatement**. It creates no new evidence and no authority promotion.

## Why the datasource is relational

A single flat table would merge grains that answer different questions. Kernel observations, return
records, trace channels, seam records, receipts, and casepack expectations do not have the same row
identity. The bundle therefore keeps them separate and publishes explicit relationships instead of
silently duplicating or averaging values.

The central key is `run_key = <source_scope>:<run_id>`. `source_scope` distinguishes active `runs/`
from `archive/runs/`, so archival retention does not masquerade as current execution.

## Tables

| Table | Grain | Primary use |
| --- | --- | --- |
| `runs.csv` | one row per source run | run identity, contract/version pointers, availability flags |
| `contract_fields.csv` | one flattened source field | contract/manifest inspection without schema loss |
| `kernel_observations.csv` | one source kernel row | source-declared F, omega, S, C, tau_R, kappa, IC and diagnostic fields |
| `return_observations.csv` | one source return row | tau_R token preservation and return timeline |
| `trace_fields.csv` | one trace field per time row | heterogeneous trace/channel readback |
| `missingness_events.csv` | one censor/OOR record | missingness before failure |
| `seam_events.csv` | one source seam row | seam provenance; payload retained losslessly as JSON |
| `receipt_fields.csv` | one receipt field | source receipt inspection without granting weld |
| `casepacks.csv` | one casepack manifest | casepack identity and declared contract/closure references |
| `casepack_expected_invariants.csv` | one expected invariant row | source-declared expected outputs, kept distinct from executed runs |
| `relationships.csv` | one relationship declaration | Tableau logical-model guidance |

`dataset_manifest.json` records export identity, source commit when available, table counts, and the
semantic/evidence boundaries of the export.

## Non-negotiable boundaries

1. **No canonicalization by column name.** Historical or run-local files may use the reserved symbols
   under an earlier contract. Their values are exported as source-declared values and marked
   `SOURCE_DECLARED_UNASSESSED`; the export does not claim compatibility with the current kernel.
2. **No return coercion.** `INF_REC`, `UNIDENTIFIABLE`, `OOR`, finite numeric values, missing values,
   and other source tokens remain distinct. A numeric helper is supplied only when the source token is
   actually finite numeric text.
3. **No zero imputation.** Missingness is not converted to zero.
4. **No regime-to-stance promotion.** Source regime fields remain diagnostics. The exporter derives no
   `CONFORMANT`, `NONCONFORMANT`, or `NON_EVALUABLE` stance.
5. **No seam-to-weld promotion.** Seam and receipt artifacts are carried as source evidence. The exporter
   does not independently grant continuity or weld.
6. **Archive is lineage, not current authority.** Archived runs are retained by default but are tagged
   `source_scope=archive`.

## Build

```bash
python integrations/tableau/export_dataset.py \
  --repo-root . \
  --output-dir artifacts/tableau
```

To build only from current `runs/` and omit archival lineage:

```bash
python integrations/tableau/export_dataset.py \
  --repo-root . \
  --output-dir artifacts/tableau-current \
  --no-archive
```

The command is read-only with respect to source artifacts. Delete the output directory and rerun to
rebuild from the repository state.

## Tableau logical model

Use `runs.csv` as the run hub. Relate all run-grain child tables to `runs.csv` on `run_key` as declared
in `relationships.csv`. Use `casepacks.csv` as the casepack hub for expected-invariant records.

Do not physically join all child tables into one rowset before aggregation. Doing so can multiply rows
across independent grains and create values that were never present in the source.

## Intended dashboard order

A Structura Reditus control surface can then read, without changing the underlying burden:

```text
Object / source / contract
        -> trace and source-declared kernel
        -> typed return
        -> seam / receipt evidence
        -> missingness and open boundaries
        -> separately authorized stance, if a governing evaluator supplies one
```

This export stops before that last authorization boundary.
