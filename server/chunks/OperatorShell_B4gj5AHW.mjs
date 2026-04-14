import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { m as maybeRenderHead, r as renderTemplate, d as renderSlot } from './server_DjVGnHP9.mjs';
import 'clsx';

const $$OperatorShell = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$OperatorShell;
  const { title = "CAI · Collapse-Aware Intelligence", sessionId = "" } = Astro2.props;
  return renderTemplate`${maybeRenderHead()}<div class="operator-shell__container"> <header class="operator-shell__header"> <h1>${title}</h1> ${sessionId && renderTemplate`<span class="operator-shell__session-id">Session: ${sessionId}</span>`} </header> <nav class="operator-shell__nav"> <ul> <li><a href="/cai">CAI Home</a></li> <li><a href="/operator">Operator Workspace</a></li> <li><a href="/operator/chat">Chat</a></li> <li><a href="/operator/contracts">Contracts</a></li> <li><a href="/operator/casepacks">Casepacks</a></li> </ul> </nav> <div class="operator-shell__layout"> <aside class="operator-shell__left"> ${renderSlot($$result, $$slots["left"])} </aside> <main class="operator-shell__main"> ${renderSlot($$result, $$slots["default"])} </main> <aside class="operator-shell__right"> ${renderSlot($$result, $$slots["right"])} </aside> </div> </div>`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/components/OperatorShell.astro", void 0);

export { $$OperatorShell as $ };
