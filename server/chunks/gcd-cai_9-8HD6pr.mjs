import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, c as Fragment, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { $ as $$OperatorShell } from './OperatorShell_B4gj5AHW.mjs';
import { $ as $$OperatorChatPanel, a as $$CEAuditCard } from './CEAuditCard_C-3safBI.mjs';
import { $ as $$CorpusResolverPanel } from './CorpusResolverPanel_DkWs4U3g.mjs';

function randomId() {
  return Math.random().toString(36).slice(2, 10);
}
async function createOperatorSession(payload) {
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
    createdAt: (/* @__PURE__ */ new Date()).toISOString(),
    updatedAt: (/* @__PURE__ */ new Date()).toISOString()
  };
}
async function getOperatorSession(sessionId) {
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
      createdAt: (/* @__PURE__ */ new Date()).toISOString(),
      updatedAt: (/* @__PURE__ */ new Date()).toISOString()
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

const $$GcdCai = createComponent(async ($$result, $$props, $$slots) => {
  let session = null;
  let spine = null;
  let ceAudit = null;
  if (typeof window !== "undefined") {
    const storedSessionId = window.localStorage.getItem("operatorSessionId");
    if (storedSessionId) {
      try {
        const envelope = await getOperatorSession(storedSessionId);
        session = envelope.session;
        spine = envelope.spineState;
      } catch (e) {
      }
    }
    if (!session) {
      const created = await createOperatorSession({ mode: "explain" });
      session = created;
      window.localStorage.setItem("operatorSessionId", session.sessionId);
      const envelope = await getOperatorSession(session.sessionId);
      spine = envelope.spineState;
    }
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent("operator:session-ready", { detail: { sessionId: session?.sessionId } }));
    }, 0);
    window.addEventListener("operator:ce-audit", (event) => {
      ceAudit = event.detail;
    });
    window.addEventListener("operator:spine-update", (event) => {
      spine = event.detail;
    });
  }
  return renderTemplate`${session ? renderTemplate`${renderComponent($$result, "OperatorShell", $$OperatorShell, { "title": "GCD CAI · Collapse-Aware Intelligence", "sessionId": session.sessionId }, { "default": async ($$result2) => renderTemplate`${maybeRenderHead()}<section>${renderComponent($$result2, "OperatorChatPanel", $$OperatorChatPanel, { "session": session, "initialSpine": spine })}<section class="operator-chat-spine-state"><h3>Spine State</h3><pre id="spine-state-json">${JSON.stringify(spine, null, 2)}</pre></section><section class="operator-ce-audit-panel">${renderComponent($$result2, "CEAuditCard", $$CEAuditCard, { "audit": ceAudit })}</section></section>`, "left": async ($$result2) => renderTemplate`${renderComponent($$result2, "Fragment", Fragment, { "slot": "left" }, { "default": async ($$result3) => renderTemplate`<section class="operator-sidebar-card"><h2>Session</h2><p><strong>Session ID:</strong>${session.sessionId}</p><p><strong>Active Contract:</strong>${session.activeContractId ?? "—"}</p><p><strong>Mode:</strong>${session.mode ?? "—"}</p></section>${renderComponent($$result3, "CorpusResolverPanel", $$CorpusResolverPanel, {})}` })}` })}` : renderTemplate`<div class="operator-chat-loading"><h2>Loading Operator Session…</h2><p>This page requires JavaScript and a valid session. Please wait…</p></div>`}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/gcd-cai.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/gcd-cai.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/gcd-cai";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$GcdCai,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
