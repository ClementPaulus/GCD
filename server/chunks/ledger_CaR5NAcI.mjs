import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { m as maybeRenderHead, r as renderTemplate, b as renderComponent, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';
import 'clsx';

const $$LedgerViewer = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$LedgerViewer;
  return renderTemplate`${maybeRenderHead()}<div id="ledger-viewer" class="space-y-4"> <!-- Quick compute --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4"> <h3 class="text-sm font-bold text-kernel-300 mb-3">Quick Domain Selector</h3> <p class="text-kernel-500 text-xs mb-2">
Click a domain to see its kernel invariants. Click any row in the table below
      to expand full channel analysis, identity verification, and budget reconciliation.
</p> <div class="flex flex-wrap gap-2 mb-3" id="domain-presets"></div> <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2 mt-2" id="domain-invariants"></div> </div> <!-- Domain table with expandable rows --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4"> <h3 class="text-sm font-bold text-kernel-300 mb-3">All 21 Domains — Click Row to Expand</h3> <div class="overflow-x-auto"> <table class="w-full text-xs font-mono" id="domain-table"> <thead> <tr class="text-kernel-500 border-b border-kernel-700"> <th class="text-left p-1.5"></th> <th class="text-left p-1.5">Domain</th> <th class="text-right p-1.5">F</th> <th class="text-right p-1.5">ω</th> <th class="text-right p-1.5">IC</th> <th class="text-right p-1.5">Δ</th> <th class="text-right p-1.5">S</th> <th class="text-right p-1.5">C</th> <th class="text-center p-1.5">Regime</th> <th class="text-center p-1.5">IC/F</th> </tr> </thead> <tbody id="domain-tbody"></tbody> </table> </div> <p class="text-xs text-kernel-600 mt-2 italic">
Click any row to expand: trace channels, identity verification, and seam budget analysis.
</p> </div> <!-- Regime distribution --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4"> <h3 class="text-sm font-bold text-kernel-300 mb-3">Cross-Domain Regime Distribution</h3> <div id="domain-regime-bars"></div> </div> <!-- Domain ranking --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4"> <h3 class="text-sm font-bold text-kernel-300 mb-3">Domain Rankings</h3> <div id="domain-rankings" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div> </div> </div> ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/components/LedgerViewer.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/components/LedgerViewer.astro", void 0);

const $$Ledger = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$Ledger;
  const sections = ["purpose", "domains", "viewer", "budget", "identities", "comparison", "spine"];
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Integrity Ledger — GCD", "description": "Domain overview, kernel metrics, budget reconciliation, identity verification, and cross-domain integrity ledger for all 21 closure domains." }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <!-- ═══════════ HERO ═══════════ --> <div class="mb-8"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Integrity Ledger</h1> <p class="text-kernel-400 text-lg italic">Auditus praecedit responsum — hearing precedes response.</p> <p class="text-kernel-500 text-sm mt-2 max-w-3xl">
The ledger is the fourth stop on the spine: it debits Drift and Roughness,
        credits Return, and derives the verdict. This page shows the kernel metrics
        for all 21 closure domains — where each domain stands, how they compare,
        and where the heterogeneity gap reveals structural insight.
</p> </div> <!-- ═══════════ NAV ═══════════ --> <nav class="mb-8 flex flex-wrap gap-2"> ${sections.map((s) => renderTemplate`<a${addAttribute(`#${s}`, "href")} class="px-3 py-1.5 rounded-full text-xs font-medium
          bg-kernel-800/60 text-kernel-400 hover:text-kernel-200 hover:bg-kernel-700/60
          border border-kernel-700/40 transition no-underline"> ${s === "viewer" ? "Domain Ledger" : s === "budget" ? "Budget Simulator" : s === "identities" ? "Identity Check" : s === "comparison" ? "Cross-Domain" : s.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())} </a>`)} </nav> <!-- ═══════════ §1: PURPOSE ═══════════ --> <section id="purpose" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">What the Ledger Does</h2> <div class="grid grid-cols-1 md:grid-cols-3 gap-4"> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <h3 class="text-sm font-bold text-red-400 mb-2">Debit Side</h3> <ul class="text-xs text-kernel-400 space-y-2"> <li class="flex items-start gap-2"> <span class="text-red-400 shrink-0 font-mono">D<sub>ω</sub></span> <span><strong class="text-kernel-300">Drift cost</strong> — Γ(ω) = ω<sup>3</sup>/(1 − ω + ε). How far the system departed from fidelity.</span> </li> <li class="flex items-start gap-2"> <span class="text-red-400 shrink-0 font-mono">D<sub>C</sub></span> <span><strong class="text-kernel-300">Curvature cost</strong> — α · C where α = 1.0. Friction from coupling to uncontrolled degrees of freedom.</span> </li> </ul> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <h3 class="text-sm font-bold text-emerald-400 mb-2">Credit Side</h3> <ul class="text-xs text-kernel-400 space-y-2"> <li class="flex items-start gap-2"> <span class="text-emerald-400 shrink-0 font-mono">R·τ<sub>R</sub></span> <span><strong class="text-kernel-300">Return credit</strong> — Credible re-entry, typed and timestamped. Exactly zero if τ<sub>R</sub> = ∞<sub>rec</sub>.</span> </li> </ul> <div class="mt-3 text-xs text-kernel-500 bg-kernel-800/50 rounded p-2 font-mono">
Δκ = R·τ<sub>R</sub> − (D<sub>ω</sub> + D<sub>C</sub>)
</div> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <h3 class="text-sm font-bold text-amber-400 mb-2">Reconciliation</h3> <ul class="text-xs text-kernel-400 space-y-2"> <li class="flex items-start gap-2"> <span class="text-amber-400 shrink-0">▸</span> <span>If |Δκ| ≤ tol<sub>seam</sub> (0.005): the seam <strong class="text-emerald-400">closes</strong> → SUTURA</span> </li> <li class="flex items-start gap-2"> <span class="text-amber-400 shrink-0">▸</span> <span>If |Δκ| > tol<sub>seam</sub>: the claim is a <strong class="text-red-400">gesture</strong> → GESTUS</span> </li> <li class="flex items-start gap-2"> <span class="text-amber-400 shrink-0">▸</span> <span>History is <strong class="text-kernel-200">append-only</strong> and welded, never rewritten</span> </li> </ul> </div> </div> <div class="mt-4 bg-kernel-900/50 border border-kernel-800 rounded-lg p-4"> <h3 class="text-sm font-bold text-kernel-300 mb-2">Three-Valued Verdict</h3> <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs text-center"> <div class="bg-green-900/20 border border-green-700/30 rounded p-2"> <div class="text-green-400 font-bold">CONFORMANT</div> <div class="text-kernel-500 mt-1">Budget closes, all gates pass, identities hold</div> </div> <div class="bg-red-900/20 border border-red-700/30 rounded p-2"> <div class="text-red-400 font-bold">NONCONFORMANT</div> <div class="text-kernel-500 mt-1">Budget fails, identity violated, or gate crossed</div> </div> <div class="bg-yellow-900/20 border border-yellow-700/30 rounded p-2"> <div class="text-yellow-400 font-bold">NON_EVALUABLE</div> <div class="text-kernel-500 mt-1">Insufficient data — the third state, always available</div> </div> </div> <p class="text-xs text-kernel-600 italic text-center mt-2">
Numquam binarius; tertia via semper patet. — Never boolean; the third way is always open.
</p> </div> </section> <!-- ═══════════ §2: THE 21 DOMAINS ═══════════ --> <section id="domains" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">The 21 Closure Domains</h2> <p class="text-sm text-kernel-400 mb-4">
Each domain selects which real-world quantities become trace vector channels.
        The kernel function is the same everywhere — Tier-2 closures choose the <em>input</em>;
        Tier-1 computes the <em>output</em>. The ledger records both.
</p> <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-2"> ${[
    { id: "gcd", label: "GCD", cat: "Core" },
    { id: "rcft", label: "RCFT", cat: "Core" },
    { id: "kinematics", label: "Kinematics", cat: "Physics" },
    { id: "weyl", label: "Weyl", cat: "Physics" },
    { id: "astronomy", label: "Astronomy", cat: "Physics" },
    { id: "nuclear_physics", label: "Nuclear", cat: "Physics" },
    { id: "quantum_mechanics", label: "Quantum", cat: "Physics" },
    { id: "atomic_physics", label: "Atomic", cat: "Physics" },
    { id: "everyday_physics", label: "Everyday", cat: "Physics" },
    { id: "standard_model", label: "Std Model", cat: "Physics" },
    { id: "spacetime_memory", label: "Spacetime", cat: "Physics" },
    { id: "materials_science", label: "Materials", cat: "Material" },
    { id: "finance", label: "Finance", cat: "Social" },
    { id: "security", label: "Security", cat: "Social" },
    { id: "evolution", label: "Evolution", cat: "Bio" },
    { id: "consciousness_coherence", label: "Consciousness", cat: "Neuro" },
    { id: "awareness_cognition", label: "Awareness", cat: "Neuro" },
    { id: "clinical_neuroscience", label: "Clinical", cat: "Neuro" },
    { id: "dynamic_semiotics", label: "Semiotics", cat: "Language" },
    { id: "continuity_theory", label: "Continuity", cat: "Theory" },
    { id: "immunology", label: "Immunology", cat: "Bio" }
  ].map((d) => {
    const catColors = {
      Core: "border-amber-700/40",
      Physics: "border-blue-700/40",
      Material: "border-cyan-700/40",
      Social: "border-emerald-700/40",
      Bio: "border-green-700/40",
      Neuro: "border-purple-700/40",
      Language: "border-orange-700/40",
      Theory: "border-kernel-600/40"
    };
    const colorClass = catColors[d.cat] || "border-kernel-700/30";
    return renderTemplate`<div${addAttribute(`bg-kernel-800/50 border ${colorClass} rounded px-2 py-1.5 text-xs text-kernel-400`, "class")}> <span class="font-mono">${d.label}</span> <span class="text-kernel-600 ml-1 text-[10px]">${d.cat}</span> </div>`;
  })} </div> </section> <!-- ═══════════ §3: INTERACTIVE VIEWER ═══════════ --> <section id="viewer" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Domain Ledger</h2> ${renderComponent($$result2, "LedgerViewer", $$LedgerViewer, {})} </section> <!-- ═══════════ §4: BUDGET SIMULATOR ═══════════ --> <section id="budget" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Budget Reconciliation Simulator</h2> <p class="text-sm text-kernel-400 mb-4">
Simulate the seam budget for any custom scenario. Adjust drift cost, curvature cost,
        return magnitude, and return time to see whether the seam closes.
</p> <div class="grid grid-cols-1 md:grid-cols-2 gap-4"> <!-- Budget inputs --> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5 space-y-4"> <div class="text-sm font-bold text-kernel-300 mb-2">Budget Parameters</div> <div> <label class="text-xs text-kernel-500 block mb-1">ω (Drift) — drives D<sub>ω</sub> = Γ(ω) = ω³/(1 − ω + ε)</label> <input id="sim-omega" type="range" min="0" max="0.99" step="0.01" value="0.15" class="w-full accent-red-400"> <div class="flex justify-between text-xs mt-1"> <span id="sim-omega-val" class="text-red-400 font-mono">0.15</span> <span id="sim-dw-val" class="text-kernel-500 font-mono">D<sub>ω</sub> = 0.0040</span> </div> </div> <div> <label class="text-xs text-kernel-500 block mb-1">C (Curvature) — drives D<sub>C</sub> = α · C</label> <input id="sim-curv" type="range" min="0" max="1" step="0.01" value="0.10" class="w-full accent-orange-400"> <div class="flex justify-between text-xs mt-1"> <span id="sim-curv-val" class="text-orange-400 font-mono">0.10</span> <span id="sim-dc-val" class="text-kernel-500 font-mono">D<sub>C</sub> = 0.1000</span> </div> </div> <div> <label class="text-xs text-kernel-500 block mb-1">R (Return magnitude)</label> <input id="sim-r" type="range" min="0" max="1" step="0.01" value="0.30" class="w-full accent-blue-400"> <span id="sim-r-val" class="text-xs text-blue-400 font-mono">0.30</span> </div> <div> <label class="text-xs text-kernel-500 block mb-1">τ<sub>R</sub> (Return time factor)</label> <div class="flex gap-2 items-center"> <input id="sim-tau" type="range" min="0.1" max="5" step="0.1" value="1.0" class="flex-1 accent-emerald-400"> <label class="flex items-center gap-1 text-xs text-kernel-500"> <input type="checkbox" id="sim-inf" class="accent-red-400">
∞<sub>rec</sub> </label> </div> <span id="sim-tau-val" class="text-xs text-emerald-400 font-mono">1.0</span> </div> </div> <!-- Budget result --> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <div class="text-sm font-bold text-kernel-300 mb-3">Reconciliation Result</div> <div id="sim-result" class="space-y-3"> <!-- filled by script --> </div> </div> </div> </section> <!-- ═══════════ §5: IDENTITY VERIFICATION ═══════════ --> <section id="identities" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Identity Verification</h2> <p class="text-sm text-kernel-400 mb-4">
Enter a trace vector to verify all three algebraic identities in real-time.
        These identities must hold for <em>any</em> valid trace — they are provable from Axiom-0.
</p> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <div class="mb-4"> <label class="text-xs text-kernel-500 block mb-1">Trace vector (comma-separated values in [0, 1])</label> <input id="id-trace" type="text" value="0.95, 0.80, 0.60, 0.90, 0.75, 0.85" class="w-full bg-kernel-950 border border-kernel-700 rounded px-3 py-2 text-sm text-kernel-200 font-mono"> <p class="text-xs text-kernel-600 mt-1">Equal weights applied automatically. Edit to test any configuration.</p> </div> <div id="id-results" class="space-y-3"> <!-- filled by script --> </div> </div> </section> <!-- ═══════════ §6: CROSS-DOMAIN COMPARISON ═══════════ --> <section id="comparison" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Cross-Domain Comparison</h2> <p class="text-sm text-kernel-400 mb-4">
Select two domains to compare their kernel metrics side by side. The heterogeneity gap (Δ = F − IC)
        reveals where each domain's channels diverge — and what it costs multiplicative coherence.
</p> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <div class="grid grid-cols-2 gap-4 mb-4"> <div> <label class="text-xs text-kernel-500 block mb-1">Domain A</label> <select id="cmp-a" class="w-full bg-kernel-950 border border-kernel-700 rounded px-3 py-2 text-sm text-kernel-200"></select> </div> <div> <label class="text-xs text-kernel-500 block mb-1">Domain B</label> <select id="cmp-b" class="w-full bg-kernel-950 border border-kernel-700 rounded px-3 py-2 text-sm text-kernel-200"></select> </div> </div> <div id="cmp-result" class="space-y-3"> <!-- filled by script --> </div> </div> </section> <!-- ═══════════ §7: THE SPINE ═══════════ --> <section id="spine" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">The Ledger in the Spine</h2> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <div class="flex flex-wrap justify-center gap-2 text-xs font-mono mb-4"> <span class="px-3 py-1.5 bg-kernel-800 border border-kernel-700 rounded text-kernel-400">Contract</span> <span class="text-kernel-600">&rarr;</span> <span class="px-3 py-1.5 bg-kernel-800 border border-kernel-700 rounded text-kernel-400">Canon</span> <span class="text-kernel-600">&rarr;</span> <span class="px-3 py-1.5 bg-kernel-800 border border-kernel-700 rounded text-kernel-400">Closures</span> <span class="text-kernel-600">&rarr;</span> <span class="px-3 py-1.5 bg-amber-900/40 border border-amber-700/50 rounded text-amber-400 font-bold">Integrity Ledger</span> <span class="text-kernel-600">&rarr;</span> <span class="px-3 py-1.5 bg-kernel-800 border border-kernel-700 rounded text-kernel-400">Stance</span> </div> <p class="text-xs text-kernel-400 text-center max-w-xl mx-auto">
The Integrity Ledger is the <strong class="text-kernel-300">fourth stop</strong> on the
          spine. Everything before it produces data (Contract freezes, Canon narrates, Closures gate).
          The Ledger <em>reconciles</em> — it is the proof that the sentence is well-formed.
          The Stance that follows is read from the reconciled ledger, never asserted independently.
</p> <p class="text-xs text-kernel-600 italic text-center mt-3">
Continuitas non narratur: mensuratur. — Continuity is not narrated: it is measured.
</p> </div> </section> <!-- ═══════════ AGGREGATE STATS ═══════════ --> <section class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Aggregate Statistics</h2> <div id="agg-stats" class="grid grid-cols-2 md:grid-cols-4 gap-3"> <!-- filled by script --> </div> </section> <!-- Footer --> <div class="text-center text-kernel-600 text-xs italic pb-8">
Historia numquam rescribitur; sutura tantum additur. — History is never rewritten; only a weld is added.
</div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/ledger.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/ledger.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/ledger.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/ledger";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Ledger,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
