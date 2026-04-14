import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$SeamBudget = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Seam Budget Explorer — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <div class="mb-6"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Seam Budget Explorer</h1> <p class="text-kernel-400 max-w-3xl">
The seam budget Δκ = R·τ_R − (D_ω + D_C) must reconcile to |residual| ≤ tol_seam.
        Explore the cost functions, credit mechanisms, and the pole structure that governs
        the boundary between return and permanent detention.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Si τ_R = ∞_rec, nulla fides datur. — If return time is infinite, no credit is given.
</p> </div> <!-- Budget controls --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Budget Parameters</h2> <div class="grid grid-cols-2 md:grid-cols-5 gap-4"> <div> <label class="text-xs text-kernel-400 block mb-1">ω (Drift)</label> <input id="omega" type="range" min="0" max="0.99" step="0.001" value="0.15" class="w-full accent-red-500"> <div class="text-xs font-mono text-kernel-500 text-center" id="omega-label">0.150</div> </div> <div> <label class="text-xs text-kernel-400 block mb-1">C (Curvature)</label> <input id="curvature" type="range" min="0" max="1" step="0.01" value="0.10" class="w-full accent-amber-500"> <div class="text-xs font-mono text-kernel-500 text-center" id="curvature-label">0.10</div> </div> <div> <label class="text-xs text-kernel-400 block mb-1">R (Return credit)</label> <input id="R" type="range" min="0" max="2" step="0.01" value="0.50" class="w-full accent-green-500"> <div class="text-xs font-mono text-kernel-500 text-center" id="R-label">0.50</div> </div> <div> <label class="text-xs text-kernel-400 block mb-1">τ_R (Return time)</label> <input id="tauR" type="range" min="1" max="50" step="1" value="5" class="w-full accent-blue-500"> <div class="text-xs font-mono text-kernel-500 text-center" id="tauR-label">5</div> <label class="text-[10px] text-kernel-600 block mt-1"> <input type="checkbox" id="inf-rec" class="mr-1"> ∞_rec (no return)
</label> </div> <div> <label class="text-xs text-kernel-400 block mb-1">κ_ledger</label> <input id="kappa-ledger" type="range" min="-2" max="2" step="0.01" value="0" class="w-full accent-purple-500"> <div class="text-xs font-mono text-kernel-500 text-center" id="kappa-label">0.00</div> </div> </div> <!-- Preset buttons --> <div class="flex flex-wrap gap-2 mt-4"> <button data-preset="stable" class="px-3 py-1 text-xs bg-green-900/50 text-green-400 rounded border border-green-800 hover:bg-green-800/50">Stable return</button> <button data-preset="watch" class="px-3 py-1 text-xs bg-amber-900/50 text-amber-400 rounded border border-amber-800 hover:bg-amber-800/50">Watch regime</button> <button data-preset="collapse" class="px-3 py-1 text-xs bg-red-900/50 text-red-400 rounded border border-red-800 hover:bg-red-800/50">Deep collapse</button> <button data-preset="pole" class="px-3 py-1 text-xs bg-purple-900/50 text-purple-400 rounded border border-purple-800 hover:bg-purple-800/50">Near pole (ω→1)</button> <button data-preset="gesture" class="px-3 py-1 text-xs bg-kernel-800 text-kernel-400 rounded border border-kernel-600 hover:bg-kernel-700">Gesture (∞_rec)</button> </div> </div> <!-- Budget results --> <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6" id="budget-results"></div> <!-- Budget visualization --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Budget Breakdown</h2> <div id="budget-bars"></div> <div class="mt-4 flex items-center gap-2" id="verdict-line"></div> </div> <!-- Γ(ω) curve --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Drift Cost Curve Γ(ω)</h2> <p class="text-xs text-kernel-500 mb-4">
Γ(ω) = ω³ / (1 − ω + ε). Monotone increasing with a pole at ω = 1.
        The frozen exponent p = 3 yields ω_trap = 0.6823 (Cardano root of x³ + x − 1 = 0).
</p> <div class="relative"> <canvas id="gamma-canvas" class="cursor-crosshair" style="max-width: 720px; height: 280px; width: 100%;"></canvas> <div id="gamma-tooltip" class="hidden absolute text-xs font-mono bg-kernel-800/95 border border-kernel-600 text-kernel-200 px-2 py-1 rounded shadow-lg pointer-events-none z-10 whitespace-nowrap"></div> </div> </div> <!-- Cost decomposition across ω sweep --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Cost Anatomy</h2> <p class="text-xs text-kernel-500 mb-4">
Three cost functions govern the seam. The budget Δκ is their net balance.
</p> <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="cost-anatomy"></div> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/seam-budget.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/seam-budget.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/seam-budget.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/seam-budget";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$SeamBudget,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
