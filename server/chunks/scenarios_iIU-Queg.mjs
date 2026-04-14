import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Scenarios = createComponent(($$result, $$props, $$slots) => {
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Domain Scenarios — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <div class="mb-6"> <nav class="text-xs text-kernel-500 mb-3"> <a${addAttribute(`${base}rosetta/`, "href")} class="hover:text-kernel-300 transition">Rosetta</a> <span class="mx-1">›</span> <span class="text-kernel-400">Domain Scenarios</span> </nav> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Domain Scenarios</h1> <p class="text-kernel-400 max-w-3xl">
Five cross-domain scenarios computed through the kernel and read through every Rosetta lens.
        The numbers are identical — only the dialect changes. This is the Cognitive Equalizer in action.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Significatio stabilis manet dum dialectus mutatur. — Meaning stays stable while dialect changes.
</p> </div> <!-- Scenario selector --> <div class="flex flex-wrap gap-2 mb-4" id="scenario-nav"></div> <!-- Scenario detail --> <div id="scenario-detail" class="space-y-6"></div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/scenarios.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/scenarios.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/scenarios.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/rosetta/scenarios";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Scenarios,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
