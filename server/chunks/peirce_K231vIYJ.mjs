import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Peirce = createComponent(($$result, $$props, $$slots) => {
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Peirce Correspondence — GCD" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-5xl mx-auto"> <div class="mb-6"> <nav class="text-xs text-kernel-500 mb-3"> <a${addAttribute(`${base}rosetta/`, "href")} class="hover:text-kernel-300 transition">Rosetta</a> <span class="mx-1">›</span> <span class="text-kernel-400">Peirce Correspondence</span> </nav> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Peirce Correspondence</h1> <p class="text-kernel-400 max-w-3xl">
Charles Sanders Peirce's triadic semiotics (Object → Sign → Interpretant) maps
        structurally onto the GCD kernel pipeline. But GCD completes what Peirce left
        open: the <strong class="text-kernel-200">seam</strong> provides a stopping condition
        for unlimited semiosis. The return axiom determines when interpretation terminates.
</p> </div> <!-- Main correspondence table --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Structural Mapping</h2> <div class="overflow-x-auto" id="peirce-table-container"></div> </div> <!-- The missing piece --> <div class="bg-gradient-to-r from-kernel-900 via-amber-950/20 to-kernel-900 border border-amber-700/50 rounded-lg p-6 mb-6"> <h2 class="text-lg font-bold text-amber-300 mb-3">The Missing Piece</h2> <div class="grid grid-cols-1 md:grid-cols-2 gap-6"> <div> <h3 class="text-sm font-bold text-kernel-300 mb-2">Peirce's Problem</h3> <p class="text-sm text-kernel-400">
Peirce recognized that signs generate interpretants which become signs for further
            interpretants — an unbounded chain he called <em class="text-kernel-300">unlimited semiosis</em>.
            He never solved the termination problem: when does interpretation stop?
            Without a stopping condition, meaning remains indefinitely deferred.
</p> </div> <div> <h3 class="text-sm font-bold text-kernel-300 mb-2">Axiom-0's Completion</h3> <p class="text-sm text-kernel-400"> <em class="text-kernel-300">"Only what returns is real."</em>
The seam (τ_R, tol_seam) provides the missing termination condition.
            When the seam budget reconciles (|residual| ≤ 0.005), interpretation has
<em class="text-kernel-200">returned</em> — the sign chain closes. When it doesn't
            (τ_R = ∞_rec), interpretation remains a <em class="text-kernel-300">gestus</em>:
            an emission without receipt.
</p> </div> </div> <div class="mt-4 p-3 bg-kernel-800/50 rounded text-xs text-kernel-500 text-center"> <em>Semeiosis terminatur cum sutura clauditur.</em> — Semiosis terminates when the seam closes.
</div> </div> <!-- Semiotic kernel findings --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4 mb-6"> <h2 class="text-lg font-bold text-kernel-200 mb-3">Semiotic Kernel — Key Findings</h2> <p class="text-xs text-kernel-500 mb-4">
The 8-channel semiotic kernel profiles 30 sign systems. Each maps to:
        referential precision, syntactic complexity, ground stability, interpretant depth,
        compositional productivity, modality richness, temporal stability, context sensitivity.
</p> <div class="grid grid-cols-1 md:grid-cols-3 gap-3" id="semiotic-findings"></div> </div> <!-- Triadic diagram --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-6"> <h2 class="text-lg font-bold text-kernel-200 mb-4">Triadic Structure</h2> <div class="flex justify-center"> <div class="relative w-80 h-64"> <!-- Triangle vertices --> <div class="absolute top-0 left-1/2 -translate-x-1/2 text-center"> <div class="bg-cyan-900/50 border border-cyan-700 rounded-lg px-4 py-2"> <div class="text-cyan-300 font-bold text-sm">Object</div> <div class="text-kernel-500 text-xs">x(t) — raw data</div> </div> </div> <div class="absolute bottom-0 left-0 text-center"> <div class="bg-amber-900/50 border border-amber-700 rounded-lg px-4 py-2"> <div class="text-amber-300 font-bold text-sm">Sign</div> <div class="text-kernel-500 text-xs">Ψ(t) — trace</div> </div> </div> <div class="absolute bottom-0 right-0 text-center"> <div class="bg-purple-900/50 border border-purple-700 rounded-lg px-4 py-2"> <div class="text-purple-300 font-bold text-sm">Interpretant</div> <div class="text-kernel-500 text-xs">(F,ω,S,C,κ,IC)</div> </div> </div> <!-- Center: the seam --> <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"> <div class="bg-green-900/60 border-2 border-green-500 rounded-full px-3 py-2 text-center"> <div class="text-green-300 font-bold text-xs">Seam</div> <div class="text-kernel-500 text-[10px]">τ_R, tol</div> </div> </div> <!-- Connecting lines (SVG) --> <svg class="absolute inset-0 w-full h-full" viewBox="0 0 320 256" fill="none"> <line x1="160" y1="40" x2="60" y2="200" stroke="#475569" stroke-width="1" stroke-dasharray="4"></line> <line x1="160" y1="40" x2="260" y2="200" stroke="#475569" stroke-width="1" stroke-dasharray="4"></line> <line x1="60" y1="200" x2="260" y2="200" stroke="#475569" stroke-width="1" stroke-dasharray="4"></line> </svg> </div> </div> <p class="text-center text-xs text-kernel-500 mt-4">
Peirce's triad mediates Object → Sign → Interpretant.
        GCD adds the <span class="text-green-400">seam</span> at center — the return constraint that closes the cycle.
</p> </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/peirce.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/peirce.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/rosetta/peirce.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/rosetta/peirce";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Peirce,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
