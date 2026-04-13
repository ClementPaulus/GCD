from __future__ import annotations

from collections.abc import MutableMapping

from .types import RunRecord


class InMemoryRunStore:
    def __init__(self) -> None:
        self._runs: MutableMapping[str, RunRecord] = {}

    def create(self, run: RunRecord) -> RunRecord:
        self._runs[run.runId] = run
        return run

    def get(self, run_id: str) -> RunRecord | None:
        return self._runs.get(run_id)

    def save(self, run: RunRecord) -> RunRecord:
        self._runs[run.runId] = run
        return run


RUN_STORE = InMemoryRunStore()
