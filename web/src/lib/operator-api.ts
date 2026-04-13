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
} from "./operator-types";

const API_BASE = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API ${response.status}: ${text}`);
  }

  return (await response.json()) as T;
}

export async function createOperatorSession(
  payload: CreateSessionRequest,
): Promise<CreateSessionResponse> {
  return request<CreateSessionResponse>("/operator/session", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getOperatorSession(sessionId: string): Promise<SessionEnvelope> {
  return request<SessionEnvelope>(`/operator/session/${sessionId}`, {
    method: "GET",
  });
}

export async function searchCorpus(
  payload: CorpusSearchRequest,
): Promise<CorpusSearchResponse> {
  return request<CorpusSearchResponse>("/corpus/search", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getCorpusObject(
  kind: string,
  id: string,
): Promise<CorpusObjectResponse> {
  return request<CorpusObjectResponse>(`/corpus/object/${kind}/${id}`, {
    method: "GET",
  });
}

export async function chatOperator(payload: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>("/operator/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function bindContract(
  payload: BindContractRequest,
): Promise<BindContractResponse> {
  return request<BindContractResponse>("/operator/bind-contract", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function startCasepackRun(
  casepackId: string,
  payload: StartCasepackRunRequest,
): Promise<StartCasepackRunResponse> {
  return request<StartCasepackRunResponse>(`/operator/casepacks/${casepackId}/run`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getRun(runId: string): Promise<RunRecord> {
  return request<RunRecord>(`/runs/${runId}`, {
    method: "GET",
  });
}
// Operator API bridge to UMCP backend services
export async function validateCasepack(casepackId: string) {
  // TODO: Call UMCP REST API for validation
}

export async function runKernel(inputs: any) {
  // TODO: Call UMCP REST API for kernel computation
}
