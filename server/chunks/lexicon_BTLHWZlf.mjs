import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Lexicon = createComponent(($$result, $$props, $$slots) => {
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Lexicon Latinum — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-5xl mx-auto"> <div class="mb-6"> <nav class="text-xs text-kernel-500 mb-3"> <a${addAttribute(`${base}rosetta/`, "href")} class="hover:text-kernel-300 transition">Rosetta</a> <span class="mx-1">›</span> <span class="text-kernel-400">Lexicon Latinum</span> </nav> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Lexicon Latinum</h1> <p class="text-kernel-400 max-w-3xl">
These Latin terms are the <strong class="text-kernel-200">canonical names</strong> of GCD structures.
        Each word carries its operational meaning in its morphology — use them as orientation
        priors when the English is ambiguous. The morphology IS the constraint.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Continuitas non narratur: mensuratur. — Continuity is not narrated: it is measured.
</p> </div> <!-- Foundational Terms --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4 mb-6" id="lexicon-section"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Foundational Terms</h2> <div class="overflow-x-auto"> <table class="w-full text-sm" id="lexicon-table"> <thead> <tr class="border-b border-kernel-600 text-kernel-400"> <th class="text-left p-2 font-medium">Latin</th> <th class="text-left p-2 font-medium text-kernel-500">Symbol</th> <th class="text-left p-2 font-medium">Literal</th> <th class="text-left p-2 font-medium">Operational Seed</th> </tr> </thead> <tbody id="lexicon-body"></tbody> </table> </div> </div> <!-- Collapse Phenomena --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-2">Collapse Phenomena Lexicon</h2> <p class="text-xs text-kernel-500 mb-4">
16 Latin terms naming the specific phenomena discovered across 146 experiments.
        Grouped by where in the collapse-return cycle they occur.
</p> <div class="space-y-6" id="phenomena-sections"></div> </div> <!-- Pronunciation Guide --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4"> <h2 class="text-lg font-bold text-kernel-200 mb-3">Nota de Pronunciatione</h2> <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-kernel-400"> <div> <h3 class="text-kernel-300 font-bold text-xs mb-2">Classical Latin Pronunciation</h3> <ul class="space-y-1 text-xs"> <li><strong class="text-kernel-300">c</strong> — always hard: <em>casus</em> = "KAH-soos"</li> <li><strong class="text-kernel-300">ae</strong> — as English "eye": <em>clausurae</em> = "klow-SOO-rye"</li> <li><strong class="text-kernel-300">v</strong> — pronounced as "w": <em>via</em> = "WEE-ah"</li> <li><strong class="text-kernel-300">-itas</strong> — fourth syllable stress: <em>fidelitas</em> = "fi-DEH-li-tahs"</li> <li><strong class="text-kernel-300">-tio</strong> — "TEE-oh": <em>derivatio</em> = "deh-ri-WAH-tee-oh"</li> </ul> </div> <div> <h3 class="text-kernel-300 font-bold text-xs mb-2">Why Latin?</h3> <p class="text-xs text-kernel-500">
Latin carries morphological constraints that English lacks. When you say
<em class="text-kernel-400">derivatio</em> (de- + rivus: diverting the stream), the word's
            structure constrains its meaning more tightly than "drift" does.
            The Latin formulation of Axiom-0 — <em class="text-kernel-300">Collapsus generativus est;
            solum quod redit, reale est</em> — carries the axiom's morphological, syntactic,
            and etymological layers simultaneously. This is not ornament. It is precision.
</p> </div> </div> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/lexicon.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/lexicon.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/lexicon.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/rosetta/lexicon";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Lexicon,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
