// Minimal Node.js API route for Operator Session (Astro SSR or Express-compatible)

async function get(req, res) {
  // Simulate fetching a session (in-memory or from DB)
  const sessionId = req.query.sessionId || 'demo-session';
  res.json({
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
        summary: "This is a Node.js session.",
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
        rationale: ["Node.js demo: all is well."]
      }
    }
  });
}

async function post(req, res) {
  // Simulate creating a session
  const sessionId = Math.random().toString(36).slice(2, 10);
  res.json({
    sessionId,
    mode: req.body.mode || "explain",
    activeContractId: "UMA.INTSTACK.v1",
    activeClosureIds: ["gcd"],
    activeCasepackId: null,
    workingSet: [],
    currentRunId: null,
    currentWeldId: null,
    memory: { recentObjects: [], pinnedObjects: [], recentQueries: [] },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  });
}

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  get,
  post
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
