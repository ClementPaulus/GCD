export type CorpusObjectKind =
  | "contract"
  | "closure"
  | "casepack"
  | "theorem"
  | "lemma"
  | "identity"
  | "entity"
  | "paper"
  | "run"
  | "weld";

export type OperatorMode =
  | "explain"
  | "locate"
  | "derive"
  | "validate"
  | "casepack"
  | "weld"
  | "invoke";

export interface CorpusRef {
  kind: CorpusObjectKind;
  id: string;
  title?: string;
}

export interface ContractBinding {
  contractId: string;
  version?: string;
  source: "repo" | "user" | "generated";
  frozen: boolean;
}

export interface ClosureBinding {
  closureId: string;
  role: "primary" | "supporting" | "diagnostic";
  active: boolean;
}

export interface CanonState {
  summary: string;
  fiveWordView: {
    drift?: string;
    fidelity?: string;
    roughness?: string;
    return?: string;
    integrity?: string;
  };
}

export interface LedgerState {
  runId?: string;
  receiptId?: string;
  residual?: number;
  deltaKappa?: number;
  regime?: string;
  passesTolerance?: boolean;
}

export interface StanceState {
  verdict: "CONFORMANT" | "NONCONFORMANT" | "NON_EVALUABLE";
  regime?: "STABLE" | "WATCH" | "COLLAPSE";
  critical?: boolean;
  rationale: string[];
}

export interface SpineState {
  contract?: ContractBinding;
  canon?: CanonState;
  closures: ClosureBinding[];
  ledger?: LedgerState;
  stance?: StanceState;
}

export interface SessionMemory {
  recentObjects: CorpusRef[];
  pinnedObjects: CorpusRef[];
  recentQueries: string[];
}

export interface OperatorSession {
  sessionId: string;
  mode: OperatorMode;
  activeContractId?: string;
  activeClosureIds: string[];
  activeCasepackId?: string | null;
  workingSet: CorpusRef[];
  currentRunId?: string;
  currentWeldId?: string;
  memory: SessionMemory;
  createdAt: string;
  updatedAt: string;
}

export interface CEAudit {
  relevance: number;
  accuracy: number;
  completeness: number;
  consistency: number;
  traceability: number;
  groundedness: number;
  constraintRespect: number;
  returnFidelity: number;
}

export interface OperatorAnswer {
  messageId: string;
  plainText: string;
  structured: SpineState;
  usedObjects: CorpusRef[];
  ceAudit?: CEAudit;
  availableActions?: PreparedAction[];
}

export interface PreparedAction {
  actionId: string;
  actionType: string;
  allowed: boolean;
  reason?: string;
}

export interface CreateSessionRequest {
  mode: OperatorMode;
  activeContractId?: string;
  activeClosureIds?: string[];
  activeCasepackId?: string | null;
}

export interface CreateSessionResponse extends OperatorSession {}

export interface SessionEnvelope {
  session: OperatorSession;
  spineState: SpineState;
}

export interface CorpusSearchRequest {
  query: string;
  kinds?: CorpusObjectKind[];
  limit?: number;
}

export interface CorpusSearchResult {
  kind: CorpusObjectKind;
  id: string;
  title: string;
  summary?: string;
  relations?: CorpusRef[];
}

export interface CorpusSearchResponse {
  results: CorpusSearchResult[];
}

export interface CorpusObjectResponse {
  object: {
    kind: CorpusObjectKind;
    id: string;
    title: string;
    body: unknown;
    metadata?: Record<string, unknown>;
    relations?: CorpusRef[];
  };
}

export interface ChatRequest {
  sessionId: string;
  message: string;
  mode: OperatorMode;
  workingSet?: CorpusRef[];
}

export interface ChatResponse {
  messageId: string;
  answer: OperatorAnswer;
  usedObjects: CorpusRef[];
  ceAudit?: CEAudit;
}

export interface BindContractRequest {
  sessionId: string;
  contractId: string;
}

export interface BindContractResponse {
  sessionId: string;
  activeContractId: string;
  spineState: SpineState;
}

export type RunStatus = "queued" | "running" | "completed" | "failed";

export interface RunArtifact {
  name: string;
  url?: string;
}

export interface RunRecord {
  runId: string;
  status: RunStatus;
  casepackId: string;
  contractId: string;
  invariants?: Record<string, number> | null;
  stance?: {
    verdict?: string;
    regime?: string;
    critical?: boolean;
    rationale?: string[];
  } | null;
  artifacts?: RunArtifact[] | null;
  error?: string | null;
}

export interface StartCasepackRunRequest {
  sessionId: string;
  contractId?: string;
  overrideInputs?: Record<string, unknown> | null;
}

export interface StartCasepackRunResponse {
  runId: string;
  status: RunStatus;
}
// Operator types for corpus objects and actions
export type CorpusObjectType = 'contract' | 'closure' | 'casepack' | 'theorem' | 'entity' | 'paper';

export interface CorpusObject {
  id: string;
  type: CorpusObjectType;
  label: string;
  description?: string;
}

export type OperatorAction = 'declare' | 'log' | 'weld' | 'invoke';
