import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, c as Fragment, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { $ as $$OperatorShell } from './OperatorShell_B4gj5AHW.mjs';
import { g as getOperatorSession, c as createOperatorSession } from './operator-api_DTUbUlB7.mjs';

const $$Index = createComponent(async ($$result, $$props, $$slots) => {
  let session = null;
  let spine = null;
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
  }
  return renderTemplate`${renderComponent($$result, "OperatorShell", $$OperatorShell, { "title": "CAI · Collapse-Aware Intelligence", "sessionId": session?.sessionId ?? "" }, { "default": async ($$result2) => renderTemplate`  ${maybeRenderHead()}<section> <h2>Workspace Overview</h2> <ul> <li><strong>Session created:</strong> ${session?.createdAt ?? "—"}</li> <li><strong>Active contract:</strong> ${session?.activeContractId ?? "—"}</li> <li><strong>Active casepack:</strong> ${session?.activeCasepackId ?? "—"}</li> <li><strong>Closures:</strong> ${session?.activeClosureIds?.length ?? 0}</li> </ul> <details> <summary>Spine State</summary> <pre>${JSON.stringify(spine, null, 2)}</pre> </details> </section> `, "left": async ($$result2) => renderTemplate`${renderComponent($$result2, "Fragment", Fragment, { "slot": "left" }, { "default": async ($$result3) => renderTemplate` <section class="operator-sidebar-card"> <h2>Session</h2> <p><strong>Session ID:</strong> ${session?.sessionId ?? "—"}</p> <p><strong>Active Contract:</strong> ${session?.activeContractId ?? "—"}</p> <p><strong>Mode:</strong> ${session?.mode ?? "—"}</p> </section> ` })}` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/operator/index.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/operator/index.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/operator";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
	__proto__: null,
	default: $$Index,
	file: $$file,
	url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
