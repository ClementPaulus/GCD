const API_BASE = "/api/v1";
async function request(path, init) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...init?.headers ?? {}
    },
    ...init
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API ${response.status}: ${text}`);
  }
  return await response.json();
}
async function createOperatorSession(payload) {
  return request("/operator/session", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
async function getOperatorSession(sessionId) {
  return request(`/operator/session/${sessionId}`, {
    method: "GET"
  });
}

export { createOperatorSession as c, getOperatorSession as g };
