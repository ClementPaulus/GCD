import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Reference = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$Reference;
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Cross-Reference Index — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <div class="mb-8"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Cross-Reference Index</h1> <p class="text-kernel-400 max-w-3xl">
Unified lookup across all GCD formal objects — kernel symbols, frozen parameters,
        identities, regime gates, lenses, and domains. Every reference resolves to one definition.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Omnia per spinam transeunt. — Everything passes through the spine.
</p> </div> <!-- Quick search --> <div class="mb-6"> <input type="text" id="ref-search" placeholder="Search symbols, parameters, identities, domains..." class="w-full bg-kernel-900 border border-kernel-700 rounded-lg px-4 py-3 text-kernel-200 placeholder-kernel-600 focus:outline-none focus:border-amber-600 text-sm"> </div> <!-- Tab navigation --> <div class="flex flex-wrap gap-2 mb-6"> <button data-tab="symbols" class="ref-tab-btn bg-kernel-700 text-kernel-200 px-4 py-2 rounded-lg text-sm transition">
Kernel Symbols (6)
</button> <button data-tab="frozen" class="ref-tab-btn bg-kernel-800 text-kernel-400 px-4 py-2 rounded-lg text-sm transition hover:bg-kernel-700">
Frozen Parameters (7)
</button> <button data-tab="regime" class="ref-tab-btn bg-kernel-800 text-kernel-400 px-4 py-2 rounded-lg text-sm transition hover:bg-kernel-700">
Regime Gates
</button> <button data-tab="lenses" class="ref-tab-btn bg-kernel-800 text-kernel-400 px-4 py-2 rounded-lg text-sm transition hover:bg-kernel-700">
Rosetta Lenses (6)
</button> <button data-tab="spine" class="ref-tab-btn bg-kernel-800 text-kernel-400 px-4 py-2 rounded-lg text-sm transition hover:bg-kernel-700">
The Spine
</button> <button data-tab="terminology" class="ref-tab-btn bg-kernel-800 text-kernel-400 px-4 py-2 rounded-lg text-sm transition hover:bg-kernel-700">
Terminology
</button> </div> <!-- Tab content --> <div id="ref-content"> <!-- Filled by script --> </div> <!-- Cross-link map: Domains × Identities --> <div class="mt-12"> <h2 class="text-xl font-bold text-kernel-200 mb-4">Domain × Identity Matrix</h2> <p class="text-xs text-kernel-500 mb-4">
Which identities are most relevant to each domain. Click a cell to navigate.
</p> <div class="overflow-x-auto"> <table class="text-[10px] w-full" id="cross-matrix"> <!-- Filled by script --> </table> </div> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/reference.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/reference.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/reference.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/reference";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Reference,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
