import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$ScaleLadder = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Scale Ladder — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <div class="mb-6"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Scale Ladder</h1> <p class="text-kernel-400 max-w-3xl">
How coherence propagates across physical scales. Fidelity descends, integrity
        slaughters at phase boundaries, then new degrees of freedom restore what was lost.
        The ladder oscillates between destruction and recovery.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Ruina fecunda — fruitful ruin. Inversio scalarum — scale inversion.
</p> </div> <!-- Scale ladder visual --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">The Ladder</h2> <div class="relative"> <canvas id="ladder-canvas" class="cursor-crosshair" style="max-width: 720px; height: 360px; width: 100%;"></canvas> <div id="ladder-tooltip" class="hidden absolute text-xs font-mono bg-kernel-800/95 border border-kernel-600 text-kernel-200 px-2 py-1 rounded shadow-lg pointer-events-none z-10 whitespace-nowrap"></div> </div> <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 mt-4" id="ladder-stats"></div> </div> <!-- Phase boundary analysis --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Phase Boundary Analysis</h2> <p class="text-xs text-kernel-500 mb-4">
Each phase boundary is a seam where channels die and new ones emerge. The kernel
        measures the exact IC/F drop at each transition. Click a boundary to see the computation.
</p> <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="boundaries"></div> </div> <!-- Slaughter explorer --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Geometric Slaughter Explorer</h2> <p class="text-xs text-kernel-500 mb-4">
Kill 1, 2, or 3 channels and watch IC collapse while F stays healthy. This is the
        mechanism behind every phase boundary on the scale ladder.
</p> <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4"> <div> <label class="text-xs text-kernel-400 block mb-1">Total channels</label> <input id="n-channels" type="range" min="3" max="12" value="8" class="w-full accent-amber-500"> <div class="text-xs text-kernel-500 text-center"><span id="n-label">8</span> channels</div> </div> <div> <label class="text-xs text-kernel-400 block mb-1">Dead channels</label> <input id="n-dead" type="range" min="0" max="4" value="1" class="w-full accent-red-500"> <div class="text-xs text-kernel-500 text-center"><span id="dead-label">1</span> dead (at ε)</div> </div> <div> <label class="text-xs text-kernel-400 block mb-1">Healthy channel value</label> <input id="healthy-val" type="range" min="0.5" max="1" step="0.01" value="0.95" class="w-full accent-green-500"> <div class="text-xs text-kernel-500 text-center"><span id="healthy-label">0.95</span></div> </div> </div> <div id="slaughter-results" class="grid grid-cols-2 md:grid-cols-4 gap-3"></div> <div class="mt-3"> <canvas id="slaughter-canvas" style="max-width: 720px; height: 120px; width: 100%;"></canvas> </div> </div> <!-- Domain examples --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Scale Ladder Across Domains</h2> <p class="text-xs text-kernel-500 mb-4">
The scale ladder pattern repeats across all 21 closure domains — not just physics.
        Wherever channels die at a boundary, IC drops; wherever new DOF emerge, IC recovers.
</p> <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="domain-examples"></div> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/scale-ladder.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/scale-ladder.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/scale-ladder.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/scale-ladder";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$ScaleLadder,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
