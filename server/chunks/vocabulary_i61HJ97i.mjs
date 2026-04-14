import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Vocabulary = createComponent(($$result, $$props, $$slots) => {
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Vocabulary & Identities — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-5xl mx-auto"> <div class="mb-6"> <nav class="text-xs text-kernel-500 mb-3"> <a${addAttribute(`${base}rosetta/`, "href")} class="hover:text-kernel-300 transition">Rosetta</a> <span class="mx-1">›</span> <span class="text-kernel-400">Vocabulary & Identities</span> </nav> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Vocabulary & Identities</h1> <p class="text-kernel-400 max-w-3xl">
The complete reference for GCD's formal vocabulary. Six symbols, five words,
        three algebraic identities, five frozen parameters, and three regime gates.
        Everything derives from a single axiom. Everything is verifiable by computation.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Algebra est cautio, non porta. — The algebra is a warranty, not a gate.
</p> </div> <!-- Section nav --> <div class="flex flex-wrap gap-2 mb-6"> <button data-tab="symbols" class="tab-btn px-3 py-1.5 rounded text-xs font-medium bg-kernel-700 text-kernel-200">Kernel Symbols</button> <button data-tab="words" class="tab-btn px-3 py-1.5 rounded text-xs font-medium bg-kernel-800 text-kernel-400">Five Words</button> <button data-tab="identities" class="tab-btn px-3 py-1.5 rounded text-xs font-medium bg-kernel-800 text-kernel-400">Algebraic Identities</button> <button data-tab="frozen" class="tab-btn px-3 py-1.5 rounded text-xs font-medium bg-kernel-800 text-kernel-400">Frozen Parameters</button> <button data-tab="regimes" class="tab-btn px-3 py-1.5 rounded text-xs font-medium bg-kernel-800 text-kernel-400">Regime Gates</button> <button data-tab="verify" class="tab-btn px-3 py-1.5 rounded text-xs font-medium bg-kernel-800 text-kernel-400">Live Verifier</button> </div> <!-- Tab content --> <div id="tab-symbols" class="tab-content"></div> <div id="tab-words" class="tab-content hidden"></div> <div id="tab-identities" class="tab-content hidden"></div> <div id="tab-frozen" class="tab-content hidden"></div> <div id="tab-regimes" class="tab-content hidden"></div> <div id="tab-verify" class="tab-content hidden"></div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/vocabulary.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/vocabulary.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/vocabulary.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/rosetta/vocabulary";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Vocabulary,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
