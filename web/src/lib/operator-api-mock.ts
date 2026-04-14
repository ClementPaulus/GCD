// Mocked Operator API for static GitHub Pages demo
import type {
  BindContractRequest,
  BindContractResponse,
  ChatRequest,
  ChatResponse,
  CorpusObjectResponse,
  CorpusSearchRequest,
  CorpusSearchResponse,
  CreateSessionRequest,
  CreateSessionResponse,
  SessionEnvelope,
  StartCasepackRunRequest,
  StartCasepackRunResponse,
  RunRecord,
  OperatorSession,
  SpineState,
  CEAudit
} from "./operator-types";

function randomId() {
  return Math.random().toString(36).slice(2, 10);
}

export async function createOperatorSession(payload: CreateSessionRequest): Promise<CreateSessionResponse> {
  const sessionId = randomId();
  return {
    sessionId,
    mode: payload.mode || "explain",
    activeContractId: "UMA.INTSTACK.v1",
    activeClosureIds: ["gcd"],
    activeCasepackId: null,
    workingSet: [],
    currentRunId: null,
    currentWeldId: null,
    memory: { recentObjects: [], pinnedObjects: [], recentQueries: [] },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

export async function getOperatorSession(sessionId: string): Promise<SessionEnvelope> {
  return {
    session: {
      sessionId,
      mode: "explain",
      activeContractId: "UMA.INTSTACK.v1",
      activeClosureIds: ["gcd"],
      activeCasepackId: null,
      workingSet: [],
      currentRunId: null,
      currentWeldId: null,
      memory: { recentObjects: [], pinnedObjects: [], recentQueries: [] },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
    spineState: {
      contract: {
        contractId: "UMA.INTSTACK.v1",
        version: "1.0.0",
        source: "repo",
        frozen: true
      },
      canon: {
        summary: "This is a static demo session.",
        fiveWordView: {
          drift: "None",
          fidelity: "Full",
          roughness: "Zero",
          return: "Immediate",
          integrity: "Max"
        }
      },
      closures: [],
      ledger: {
        runId: null,
        receiptId: null,
        residual: 0,
        deltaKappa: 0,
        regime: "STABLE",
        passesTolerance: true
      },
      stance: {
        verdict: "CONFORMANT",
        regime: "STABLE",
        rationale: ["Static demo: all is well."]
      }
    }
  };
}

export async function chatOperator(payload: ChatRequest): Promise<ChatResponse> {
  return {
    messageId: randomId(),
    plainText: `Static demo: You said "${payload.message}". (No backend, just a mock reply.)`,
    structured: {
      contract: {
        contractId: "UMA.INTSTACK.v1",
        version: "1.0.0",
        source: "repo",
        frozen: true
      },
      canon: {
        summary: "Static demo response.",
        fiveWordView: {
          drift: "None",
          fidelity: "Full",
          roughness: "Zero",
          return: "Immediate",
          integrity: "Max"
        }
      },
      closures: [],
      ledger: {
        runId: null,
        receiptId: null,
        residual: 0,
        deltaKappa: 0,
        regime: "STABLE",
        passesTolerance: true
      },
      stance: {
        verdict: "CONFORMANT",
        regime: "STABLE",
        rationale: ["Static demo: all is well."]
      }
    },
    usedObjects: [],
    ceAudit: {
      relevance: 1,
      accuracy: 1,
      completeness: 1,
      consistency: 1,
      traceability: 1,
      groundedness: 1,
      constraintRespect: 1,
      returnFidelity: 1
    }
  };
}

// Other API functions can be stubbed as needed for the demo
