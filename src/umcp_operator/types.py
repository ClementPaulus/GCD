from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

CorpusObjectKind = Literal[
    "contract", "closure", "casepack", "theorem", "lemma", "identity", "entity", "paper", "run", "weld"
]
OperatorMode = Literal["explain", "locate", "derive", "validate", "casepack", "weld", "invoke"]
RunStatus = Literal["queued", "running", "completed", "failed"]
Verdict = Literal["CONFORMANT", "NONCONFORMANT", "NON_EVALUABLE"]


class CorpusRef(BaseModel):
    kind: CorpusObjectKind
    id: str
    title: str | None = None


class ContractBinding(BaseModel):
    contractId: str
    version: str | None = None
    source: Literal["repo", "user", "generated"] = "repo"
    frozen: bool = True


class ClosureBinding(BaseModel):
    closureId: str
    role: Literal["primary", "supporting", "diagnostic"] = "primary"
    active: bool = True


class CanonFiveWordView(BaseModel):
    drift: str | None = None
    fidelity: str | None = None
    roughness: str | None = None
    return_: str | None = Field(default=None, alias="return")
    integrity: str | None = None
    model_config = {"populate_by_name": True}


class CanonState(BaseModel):
    summary: str
    fiveWordView: CanonFiveWordView


class LedgerState(BaseModel):
    runId: str | None = None
    receiptId: str | None = None
    residual: float | None = None
    deltaKappa: float | None = None
    regime: str | None = None
    passesTolerance: bool | None = None


class StanceState(BaseModel):
    verdict: Verdict
    regime: Literal["STABLE", "WATCH", "COLLAPSE"] | None = None
    critical: bool | None = None
    rationale: list[str] = Field(default_factory=list)


class SpineState(BaseModel):
    contract: ContractBinding | None = None
    canon: CanonState | None = None
    closures: list[ClosureBinding] = Field(default_factory=list)
    ledger: LedgerState | None = None
    stance: StanceState | None = None


class SessionMemory(BaseModel):
    recentObjects: list[CorpusRef] = Field(default_factory=list)
    pinnedObjects: list[CorpusRef] = Field(default_factory=list)
    recentQueries: list[str] = Field(default_factory=list)


class OperatorSession(BaseModel):
    sessionId: str
    mode: OperatorMode
    activeContractId: str | None = None
    activeClosureIds: list[str] = Field(default_factory=list)
    activeCasepackId: str | None = None
    workingSet: list[CorpusRef] = Field(default_factory=list)
    currentRunId: str | None = None
    currentWeldId: str | None = None
    memory: SessionMemory = Field(default_factory=SessionMemory)
    createdAt: str
    updatedAt: str


class CEAudit(BaseModel):
    relevance: float
    accuracy: float
    completeness: float
    consistency: float
    traceability: float
    groundedness: float
    constraintRespect: float
    returnFidelity: float


class OperatorAnswer(BaseModel):
    messageId: str
    plainText: str
    structured: SpineState
    usedObjects: list[CorpusRef] = Field(default_factory=list)
    ceAudit: CEAudit | None = None


class CreateSessionRequest(BaseModel):
    mode: OperatorMode = "explain"
    activeContractId: str | None = None
    activeClosureIds: list[str] = Field(default_factory=list)
    activeCasepackId: str | None = None


class SessionEnvelope(BaseModel):
    session: OperatorSession
    spineState: SpineState


class CorpusSearchRequest(BaseModel):
    query: str
    kinds: list[CorpusObjectKind] = Field(default_factory=list)
    limit: int = 10


class CorpusSearchResult(BaseModel):
    kind: CorpusObjectKind
    id: str
    title: str
    summary: str | None = None
    relations: list[CorpusRef] = Field(default_factory=list)


class CorpusSearchResponse(BaseModel):
    results: list[CorpusSearchResult]


class CorpusObject(BaseModel):
    kind: CorpusObjectKind
    id: str
    title: str
    body: dict[str, Any] | list[Any] | str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    relations: list[CorpusRef] = Field(default_factory=list)


class CorpusObjectResponse(BaseModel):
    object: CorpusObject


class ChatRequest(BaseModel):
    sessionId: str
    message: str
    mode: OperatorMode = "explain"
    workingSet: list[CorpusRef] = Field(default_factory=list)


class ChatResponse(BaseModel):
    messageId: str
    answer: OperatorAnswer
    usedObjects: list[CorpusRef] = Field(default_factory=list)
    ceAudit: CEAudit | None = None


class BindContractRequest(BaseModel):
    sessionId: str
    contractId: str


class BindContractResponse(BaseModel):
    sessionId: str
    activeContractId: str
    spineState: SpineState


class RunArtifact(BaseModel):
    name: str
    url: str | None = None


class RunRecord(BaseModel):
    runId: str
    status: RunStatus
    casepackId: str
    contractId: str
    invariants: dict[str, float] | None = None
    stance: dict[str, Any] | None = None
    artifacts: list[RunArtifact] = Field(default_factory=list)
    error: str | None = None


class StartCasepackRunRequest(BaseModel):
    sessionId: str
    contractId: str | None = None
    overrideInputs: dict[str, Any] | None = None


class StartCasepackRunResponse(BaseModel):
    runId: str
    status: RunStatus
