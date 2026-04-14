import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { r as renderTemplate } from './server_DjVGnHP9.mjs';
import 'clsx';

const $$Invoke = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`// Operator invocation panel
import InvocationGatePanel from "../../components/InvocationGatePanel.astro"
<InvocationGatePanel />`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/operator/invoke.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/operator/invoke.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/operator/invoke";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
	__proto__: null,
	default: $$Invoke,
	file: $$file,
	url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
