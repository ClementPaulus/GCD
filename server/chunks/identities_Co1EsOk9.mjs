import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Identities = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Identity Network — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <div class="mb-6"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Identity Network</h1> <p class="text-kernel-400 max-w-3xl">
44 structural identities derived from Axiom-0. Identities are classified as
<span class="text-green-400 font-medium">Exact</span> (algebraic, machine-precision),
<span class="text-blue-400 font-medium">Sampled</span> (numerically verified by Monte Carlo),
        or <span class="text-kernel-300 font-medium">Narrative</span> (analytical proof in prose).
        Click any identity for its full bounds, proof sketch, and cross-links.
</p> <p class="text-kernel-500 italic text-sm mt-2">
Numeri sunt intellectus. — The numbers are the understanding.
</p> </div> <!-- Series filter + search --> <div class="flex flex-col md:flex-row gap-3 mb-6"> <div class="grid grid-cols-2 md:grid-cols-5 gap-2 flex-1"> <button data-series="all" class="series-btn bg-kernel-700 text-kernel-200 px-3 py-3 rounded-lg text-center transition"> <div class="text-2xl font-bold">44</div> <div class="text-xs">All</div> </button> <button data-series="E" class="series-btn bg-kernel-800 text-kernel-400 px-3 py-3 rounded-lg text-center hover:bg-kernel-700 transition"> <div class="text-2xl font-bold text-blue-400">8</div> <div class="text-xs">E — Equator</div> </button> <button data-series="B" class="series-btn bg-kernel-800 text-kernel-400 px-3 py-3 rounded-lg text-center hover:bg-kernel-700 transition"> <div class="text-2xl font-bold text-green-400">12</div> <div class="text-xs">B — Bound</div> </button> <button data-series="D" class="series-btn bg-kernel-800 text-kernel-400 px-3 py-3 rounded-lg text-center hover:bg-kernel-700 transition"> <div class="text-2xl font-bold text-amber-400">8</div> <div class="text-xs">D — Duality</div> </button> <button data-series="cluster" class="series-btn bg-kernel-800 text-kernel-400 px-3 py-3 rounded-lg text-center hover:bg-kernel-700 transition"> <div class="text-2xl font-bold text-cyan-400">6</div> <div class="text-xs">Clusters</div> </button> </div> <div class="flex items-end"> <input id="identity-search" type="text" placeholder="Search identities..." class="bg-kernel-800 border border-kernel-700 rounded-lg px-4 py-2 text-sm text-kernel-200 placeholder:text-kernel-600 focus:outline-none focus:border-amber-600 w-full md:w-56"> </div> </div> <!-- Jump-to cluster links --> <div class="flex flex-wrap gap-2 mb-4" id="cluster-jump-links"> <span class="text-xs text-kernel-500 py-1">Jump to cluster:</span> </div> <!-- Identity list (expandable cards) --> <div id="identity-list" class="space-y-2 mb-8"></div> <!-- Connection clusters --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">6 Connection Clusters</h2> <p class="text-xs text-kernel-500 mb-4">
The 44 identities form a connected network. Click a cluster to filter, or click
        a member identity to jump to its expanded card.
</p> <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="clusters"></div> </div> <!-- Kernel symbols reference --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Kernel Symbol Reference</h2> <p class="text-xs text-kernel-500 mb-4">
These six Tier-1 invariants appear throughout the identities. Each is computed by
        the kernel function K&thinsp;: [0,1]ⁿ &times; &Delta;ⁿ &rarr; (F, &omega;, S, C, &kappa;, IC).
</p> <div class="grid grid-cols-2 md:grid-cols-3 gap-3" id="symbol-ref"></div> </div> <!-- Live verification --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6"> <h2 class="text-lg font-bold text-kernel-200 mb-3">Live Verification</h2> <p class="text-xs text-kernel-500 mb-4">
Verify the core algebraic identities (E1, E2, E3, B1) by sweeping 1000 random
        channel configurations. Only Exact and Sampled identities participate in this sweep.
        Narrative identities are not machine-verified here.
</p> <div class="flex gap-3 items-center"> <button id="run-sweep" class="bg-amber-700 hover:bg-amber-600 text-white px-4 py-2 rounded text-sm transition">
Run 1000-Point Sweep
</button> <span id="sweep-status" class="text-xs text-kernel-500"></span> </div> <div id="sweep-results" class="mt-4"></div> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/identities.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/identities.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/identities.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/identities";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Identities,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
