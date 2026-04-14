import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Spine = createComponent(($$result, $$props, $$slots) => {
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Discourse Spine — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-5xl mx-auto"> <div class="mb-6"> <nav class="text-xs text-kernel-500 mb-3"> <a${addAttribute(`${base}rosetta/`, "href")} class="hover:text-kernel-300 transition">Rosetta</a> <span class="mx-1">›</span> <span class="text-kernel-400">Discourse Spine</span> </nav> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Spina Grammatica</h1> <p class="text-kernel-400 max-w-3xl">
Every claim passes through exactly five stops. This is both a validation pipeline
        and a grammatical structure for how claims are told, checked, and connected.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Spina non negotiabilis est. — The spine is non-negotiable.
</p> </div> <!-- Spine visualization --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6" id="spine-visual"></div> <!-- Detailed stop cards --> <div class="space-y-4 mb-6" id="spine-cards"></div> <!-- Governance mechanisms --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-3">Governance as Punctuation</h2> <p class="text-xs text-kernel-500 mb-4">
Two mechanisms punctuate the spine without being the spine itself.
</p> <div class="grid grid-cols-1 md:grid-cols-2 gap-4"> <div class="bg-kernel-800 rounded-lg p-4 border border-kernel-700"> <h3 class="text-kernel-200 font-bold text-sm mb-2">Manifest <span class="text-kernel-600 text-xs italic">(Manifestum)</span></h3> <p class="text-sm text-kernel-400 mb-2">
Provenance — binds artifacts to time, tools, checksums.
            Every claim carries its receipt.
</p> <div class="text-xs text-kernel-500"> <strong class="text-kernel-400">Contains:</strong> SHA-256 checksums, timestamps,
            tool versions, data sources, contract reference. The manifest proves the claim
            was produced by the declared process.
</div> </div> <div class="bg-kernel-800 rounded-lg p-4 border border-kernel-700"> <h3 class="text-kernel-200 font-bold text-sm mb-2">Weld <span class="text-kernel-600 text-xs italic">(Sutura)</span></h3> <p class="text-sm text-kernel-400 mb-2">
Continuity across change — the only legitimate way to change policy.
</p> <div class="text-xs text-kernel-500"> <strong class="text-kernel-400">Protocol:</strong> Names an anchor, runs pre/post tests,
            enforces κ-continuity (residual ≤ tol). History is <em class="text-kernel-400">append-only
            and welded, never rewritten</em>.
</div> <div class="text-xs text-kernel-600 italic mt-2">
Historia numquam rescribitur; sutura tantum additur.
</div> </div> </div> </div> <!-- How to use the spine --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4"> <h2 class="text-lg font-bold text-kernel-200 mb-3">Using the Spine in Practice</h2> <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm"> <div> <h3 class="text-kernel-300 font-bold text-xs mb-2">For Validation</h3> <ol class="list-decimal list-inside space-y-1 text-kernel-400 text-xs"> <li><strong class="text-kernel-300">Freeze</strong> — declare contract, sources, normalization before computing</li> <li><strong class="text-kernel-300">Compute</strong> — run kernel on embedded trace vector</li> <li><strong class="text-kernel-300">Publish</strong> — thresholds and their order; no mid-episode edits</li> <li><strong class="text-kernel-300">Reconcile</strong> — debit/credit budget Δκ = R·τ_R − (D_ω + D_C)</li> <li><strong class="text-kernel-300">Read</strong> — derive regime from gates, emit three-valued verdict</li> </ol> </div> <div> <h3 class="text-kernel-300 font-bold text-xs mb-2">For Discourse</h3> <ol class="list-decimal list-inside space-y-1 text-kernel-400 text-xs"> <li><strong class="text-kernel-300">Contract</strong> — state what rules constrain your claim</li> <li><strong class="text-kernel-300">Canon</strong> — narrate using Drift, Fidelity, Roughness, Return, Integrity</li> <li><strong class="text-kernel-300">Closures</strong> — name your thresholds; if they change, say so</li> <li><strong class="text-kernel-300">Ledger</strong> — show the receipt: what was debited, credited, residual?</li> <li><strong class="text-kernel-300">Stance</strong> — state the derived verdict — never assert, always derive</li> </ol> </div> </div> <div class="mt-4 p-3 bg-kernel-800/50 rounded text-xs text-kernel-500 text-center"> <em>Omnia per spinam transeunt.</em> — Everything passes through the spine.
</div> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/spine.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/spine.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/spine.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/rosetta/spine";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Spine,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
