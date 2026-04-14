import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$Orientation = createComponent(($$result, $$props, $$slots) => {
  const sections = [
    {
      num: 1,
      title: "Duality",
      proves: "F + ω = 1 exactly (0.0e+00 residual across 10K traces)",
      key: "max_residual = 0.0",
      detail: "The duality identity holds with zero residual — not approximately, EXACTLY. This is not unitarity borrowed from quantum mechanics; it is a structural identity of collapse derived from Axiom-0."
    },
    {
      num: 2,
      title: "Integrity Bound",
      proves: "IC ≤ F — and WHY (geometric vs arithmetic mean)",
      key: "Δ = F − IC = 0.445",
      detail: "IC ≤ F is the solvability condition: for n=2 channels, c₁,₂ = F ± √(F²−IC²) requires IC ≤ F for real solutions. It has composition laws that classical AM-GM lacks entirely."
    },
    {
      num: 3,
      title: "Geometric Slaughter",
      proves: "One dead channel kills IC while F stays healthy",
      key: "IC/F: 1.00 → 0.11",
      detail: "Seven perfect channels at c=1.0 and one at ε give F = 0.875 but IC = 0.100. The geometric mean is merciless: one near-zero channel destroys multiplicative coherence."
    },
    {
      num: 4,
      title: "First Weld",
      proves: "c ≈ 0.318 is where Γ first drops below 1.0",
      key: "Γ(0.682) = 0.998",
      detail: "The drift cost function Γ(ω) = ωᵖ/(1−ω+ε) with p=3 has its critical threshold at ω ≈ 0.682 (i.e., c ≈ 0.318). This is the Cardano root of x³+x−1=0 — the unique integer p that produces this algebraic structure."
    },
    {
      num: 5,
      title: "Confinement Cliff",
      proves: "IC drops 98% at quark→hadron boundary",
      key: "IC/F: 0.94 → 0.01",
      detail: "Individual quarks have IC/F ≈ 0.94, but hadrons (protons, neutrons) have IC/F < 0.04. The dead color channel (color→0 in confinement) triggers geometric slaughter at the phase boundary."
    },
    {
      num: 6,
      title: "Scale Inversion",
      proves: "Atoms restore IC with new degrees of freedom",
      key: "IC/F: 0.01 → 0.96",
      detail: "Nickel (Z=28) has IC/F = 0.9573. Atoms don't inherit the hadron IC collapse — they introduce new channels (electronegativity, ionization energy, etc.) that restore multiplicative coherence."
    },
    {
      num: 7,
      title: "Full Spine",
      proves: "Contract → Kernel → Budget → Verdict on real data",
      key: "Watch: CONFORMANT",
      detail: "The complete five-stop spine runs on real data: define a contract, compute the kernel, evaluate the budget, derive a verdict. The Watch regime is CONFORMANT — 87.5% of the manifold is NOT stable."
    },
    {
      num: 8,
      title: "Equator Convergence",
      proves: "S + κ = 0 at c = 1/2 (four-way convergence)",
      key: "f(1/2) = 0.0",
      detail: "At the equator (c = 1/2), entropy S and log-integrity κ cancel exactly. This is a quintuple fixed point: S + κ = 0, the maximum of S, the inflection of IC, and the Fisher midpoint."
    },
    {
      num: 9,
      title: "Super-Exponential",
      proves: "IC convergence faster than exponential",
      key: "gap shrinks 28.5×",
      detail: "As channels converge toward c = 1, the heterogeneity gap Δ = F − IC shrinks super-exponentially — 28.5× per step. IC's geometric nature means that convergence accelerates rather than plateaus."
    },
    {
      num: 10,
      title: "Seam Composition",
      proves: "Associative algebra with identity (monoid)",
      key: "|error| = 5.55e-17",
      detail: "Seam composition is associative to machine precision. The seam algebra forms a monoid — it has an identity element and associativity. This means validation chains compose without order dependence."
    }
  ];
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Orientation — GCD Kernel", "description": "Re-derive the 10 structural insights of GCD through computation." }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-5xl mx-auto"> <div class="mb-10"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Orientation</h1> <p class="text-kernel-400 mb-1">
Re-derive the 10 structural insights of GCD through computation.
</p> <p class="text-kernel-500 text-sm italic">
Intellectus non legitur; computatur. — Understanding is not read; it is computed.
</p> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4 mb-8"> <h3 class="text-sm font-bold text-kernel-300 mb-2">Run Locally</h3> <pre class="text-xs text-kernel-400 font-mono bg-kernel-950 rounded p-3 overflow-x-auto">python scripts/orientation.py          # Full orientation — 10 sections, ~10 seconds
python scripts/orientation.py -s 3     # Single section (e.g., §3: geometric slaughter)
python scripts/orientation_checkpoint.py --verify  # Verify understanding (must PASS)</pre> </div> <div class="space-y-6"> ${sections.map((s) => renderTemplate`<div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl overflow-hidden"> <div class="flex items-start gap-4 p-5"> <div class="flex-shrink-0 w-10 h-10 rounded-full bg-kernel-800 flex items-center justify-center
                        text-amber-400 font-bold text-lg"> ${s.num} </div> <div class="flex-1"> <h3 class="text-lg font-bold text-kernel-100 mb-1">§${s.num}: ${s.title}</h3> <p class="text-sm text-kernel-300 mb-3">${s.proves}</p> <div class="bg-kernel-950 border border-kernel-700 rounded px-3 py-2 mb-3"> <span class="text-xs text-kernel-500">Key number: </span> <span class="text-sm font-mono text-amber-400">${s.key}</span> </div> <p class="text-sm text-kernel-400">${s.detail}</p> </div> </div> </div>`)} </div> <!-- Orientation Receipts Summary --> <div class="mt-10 bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-6"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Computational Ground Truth</h2> <p class="text-sm text-kernel-400 mb-4">
These numbers are compressed derivation chains. They constrain what can be said about the system.
</p> <div class="overflow-x-auto"> <table class="w-full text-sm"> <thead class="text-kernel-500 text-xs"> <tr> <th class="text-left p-2">Receipt</th> <th class="text-left p-2">Value</th> <th class="text-left p-2">Proves</th> </tr> </thead> <tbody class="text-kernel-300"> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">max|F + ω − 1|</td> <td class="p-2 font-mono text-amber-400">0.0e+00</td> <td class="p-2">Duality is exact</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">Δ for (0.95, 0.001)</td> <td class="p-2 font-mono text-amber-400">0.4447</td> <td class="p-2">Dead channel → massive gap</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">IC/F (1 dead channel, 8ch)</td> <td class="p-2 font-mono text-amber-400">0.1143</td> <td class="p-2">Geometric slaughter</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">Γ(0.682)</td> <td class="p-2 font-mono text-amber-400">0.9975</td> <td class="p-2">First weld threshold</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">Neutron IC/F</td> <td class="p-2 font-mono text-amber-400">0.0089</td> <td class="p-2">Confinement cliff</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">Nickel IC/F</td> <td class="p-2 font-mono text-amber-400">0.9573</td> <td class="p-2">Scale inversion → restored coherence</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">S + κ at c=1/2</td> <td class="p-2 font-mono text-amber-400">0.0</td> <td class="p-2">Equator convergence</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">Stable regime</td> <td class="p-2 font-mono text-amber-400">12.5%</td> <td class="p-2">Stability is rare</td> </tr> <tr class="border-t border-kernel-800"> <td class="p-2 font-mono text-xs">Seam associativity</td> <td class="p-2 font-mono text-amber-400">5.55e-17</td> <td class="p-2">Exact monoid</td> </tr> </tbody> </table> </div> </div> <div class="mt-8 text-center text-kernel-600 text-xs italic">
Numeri sunt intellectus. — The numbers are the understanding.
</div> </div> ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/orientation.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/orientation.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/orientation";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Orientation,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
