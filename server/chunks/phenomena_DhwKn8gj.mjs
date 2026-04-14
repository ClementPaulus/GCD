import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Phenomena = createComponent(($$result, $$props, $$slots) => {
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Collapse Phenomena — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-5xl mx-auto"> <div class="mb-6"> <nav class="text-xs text-kernel-500 mb-3"> <a${addAttribute(`${base}rosetta/`, "href")} class="hover:text-kernel-300 transition">Rosetta</a> <span class="mx-1">›</span> <span class="text-kernel-400">Collapse Phenomena</span> </nav> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Collapse Phenomena</h1> <p class="text-kernel-400 max-w-3xl">
16 Latin terms naming the structural phenomena discovered across 146 experiments
        and 21 closure domains. These are not metaphors — each names a measurable pattern
        in the kernel invariants, verifiable through computation.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Ruptura est fons constantiae. — Rupture is the source of constancy.
</p> </div> <!-- Category overview --> <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6"> <div class="bg-red-900/20 border border-red-700/50 rounded-lg p-4 text-center"> <div class="text-red-400 font-bold text-sm">Channel Collapse</div> <div class="text-kernel-500 text-xs mt-1">5 phenomena</div> <div class="text-kernel-600 text-xs mt-1">What happens when channels die</div> </div> <div class="bg-amber-900/20 border border-amber-700/50 rounded-lg p-4 text-center"> <div class="text-amber-400 font-bold text-sm">Seam</div> <div class="text-kernel-500 text-xs mt-1">4 phenomena</div> <div class="text-kernel-600 text-xs mt-1">The collapse-return boundary</div> </div> <div class="bg-blue-900/20 border border-blue-700/50 rounded-lg p-4 text-center"> <div class="text-blue-400 font-bold text-sm">Structural States</div> <div class="text-kernel-500 text-xs mt-1">4 phenomena</div> <div class="text-kernel-600 text-xs mt-1">Phases of the collapse landscape</div> </div> <div class="bg-green-900/20 border border-green-700/50 rounded-lg p-4 text-center"> <div class="text-green-400 font-bold text-sm">Scale Ladder</div> <div class="text-kernel-500 text-xs mt-1">3 phenomena</div> <div class="text-kernel-600 text-xs mt-1">Cross-scale coherence dynamics</div> </div> </div> <!-- Phenomena sections --> <div class="space-y-8" id="phenomena-categories"></div> <!-- Key findings --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mt-8"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Structural Insights</h2> <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm"> <div class="bg-kernel-800 rounded-lg p-4 border border-kernel-700"> <h3 class="text-red-400 font-bold text-xs mb-2">Geometric Slaughter Is Universal</h3> <p class="text-kernel-400 text-xs">
Every domain exhibits geometric slaughter when a single channel approaches ε.
            In particle physics: quark color → 0 at confinement. In finance: subprime → 0 in 2008.
            In consciousness: sleep stages → variable channel death. The mechanism is always the same:
            one near-zero channel in the geometric mean (IC) drags the product toward zero while the
            arithmetic mean (F) remains healthy. This is the integrity bound IC ≤ F in action.
</p> </div> <div class="bg-kernel-800 rounded-lg p-4 border border-kernel-700"> <h3 class="text-green-400 font-bold text-xs mb-2">Scale Inversion Heals Damage</h3> <p class="text-kernel-400 text-xs">
After geometric slaughter at one scale, new degrees of freedom at the next scale
            can restore IC. Quarks (IC/F ≈ 0.80) → hadrons (IC/F ≈ 0.03) → atoms (IC/F ≈ 0.96).
            The scale ladder is not monotonic — it oscillates between slaughter and recovery.
            Each recovery introduces new channels that re-cohere what the previous boundary destroyed.
<em class="text-kernel-300">Ruina fecunda</em> — fruitful ruin.
</p> </div> <div class="bg-kernel-800 rounded-lg p-4 border border-kernel-700"> <h3 class="text-amber-400 font-bold text-xs mb-2">The First Weld Requires Homogeneity</h3> <p class="text-kernel-400 text-xs">
Near the generative threshold (c ≈ 0.318), the first seam closes only when all channels
            are equal. Heterogeneity at this boundary prevents the budget from reconciling because
            even small channel variance creates enough gap (Δ = F − IC) to exceed the residual tolerance.
<em class="text-kernel-300">Excitatio homogenea</em> — the homogeneous lift.
</p> </div> <div class="bg-kernel-800 rounded-lg p-4 border border-kernel-700"> <h3 class="text-blue-400 font-bold text-xs mb-2">∞_rec Is a First-Class Verdict</h3> <p class="text-kernel-400 text-xs">
Permanent detention (τ_R = ∞_rec) is not an error — it is a legitimate outcome.
            A gestus sine receptu (gesture without receipt) is an epistemic emission that cannot
            close a seam. It may carry insight but it cannot carry credit. The system distinguishes
            between "not yet returned" and "cannot return" — both are meaningful, both are measured.
</p> </div> </div> </div> <!-- Interactive demo --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mt-6"> <h2 class="text-lg font-bold text-kernel-200 mb-3">Live Demonstration: Geometric Slaughter</h2> <p class="text-xs text-kernel-500 mb-4">
Drag the slider to kill one channel. Watch IC collapse while F stays healthy.
        This is Trucidatio Geometrica — the defining phenomenon of GCD.
</p> <div class="grid grid-cols-1 md:grid-cols-2 gap-6"> <div> <label class="text-xs text-kernel-400 block mb-2">
Dead channel value: <span id="dead-val" class="font-mono text-amber-400">0.500</span> </label> <input id="dead-slider" type="range" min="0.001" max="1" step="0.001" value="0.5" class="w-full h-2 accent-red-500"> <div class="text-xs text-kernel-600 mt-1">Other 7 channels fixed at 0.95</div> </div> <div id="slaughter-results" class="grid grid-cols-2 gap-2"> <!-- Filled by script --> </div> </div> <div class="mt-4"> <div class="text-xs text-kernel-400 mb-1">IC/F Ratio</div> <div class="h-6 bg-kernel-800 rounded overflow-hidden"> <div id="icf-bar" class="h-full bg-green-500 transition-all duration-200 rounded" style="width: 80%"></div> </div> <div class="flex justify-between text-[10px] text-kernel-600 mt-0.5"> <span>0</span> <span id="icf-label" class="text-kernel-400 font-mono">0.800</span> <span>1</span> </div> </div> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/phenomena.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/phenomena.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/phenomena.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/rosetta/phenomena";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Phenomena,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
