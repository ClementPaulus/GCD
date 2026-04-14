import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { m as maybeRenderHead, r as renderTemplate, b as renderComponent, a as addAttribute } from './server_DjVGnHP9.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';
import 'clsx';
import { r as renderScript } from './script_CjXWaIL1.mjs';

const $$PhysicalMapper = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$PhysicalMapper;
  return renderTemplate`${maybeRenderHead()}<div id="physical-mapper" class="space-y-4" data-astro-cid-qmyfqgs7> <!-- Tab navigation --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-2" data-astro-cid-qmyfqgs7> <div class="flex flex-wrap gap-1" role="tablist" data-astro-cid-qmyfqgs7> <button class="pm-tab px-3 py-1.5 rounded text-sm transition" data-tab="identify" role="tab" aria-selected="true" data-astro-cid-qmyfqgs7>
🔍 Identify
</button> <button class="pm-tab px-3 py-1.5 rounded text-sm transition" data-tab="interpret" role="tab" aria-selected="false" data-astro-cid-qmyfqgs7>
📖 Interpret
</button> <button class="pm-tab px-3 py-1.5 rounded text-sm transition" data-tab="predict" role="tab" aria-selected="false" data-astro-cid-qmyfqgs7>
🧪 Predict Unknown
</button> <button class="pm-tab px-3 py-1.5 rounded text-sm transition" data-tab="atlas" role="tab" aria-selected="false" data-astro-cid-qmyfqgs7>
🗺️ Entity Atlas
</button> </div> </div> <!-- ═══════════ TAB 1: Identify ═══════════ --> <div id="pm-identify" class="pm-panel space-y-4" data-astro-cid-qmyfqgs7> <div class="bg-kernel-900/50 border border-kernel-700 rounded-lg p-4" data-astro-cid-qmyfqgs7> <h3 class="text-lg font-semibold text-kernel-100 mb-3" data-astro-cid-qmyfqgs7>Signature Identification</h3> <p class="text-sm text-kernel-400 mb-4" data-astro-cid-qmyfqgs7>
Enter kernel invariant values or a trace vector to find the closest known physical entities.
</p> <!-- Input mode toggle --> <div class="flex gap-2 mb-4" data-astro-cid-qmyfqgs7> <button id="pm-mode-kernel" class="pm-mode-btn px-3 py-1 rounded text-sm bg-kernel-600 text-kernel-100" data-astro-cid-qmyfqgs7>
Kernel Values (F, ω, IC…)
</button> <button id="pm-mode-trace" class="pm-mode-btn px-3 py-1 rounded text-sm bg-kernel-800 text-kernel-400" data-astro-cid-qmyfqgs7>
Trace Vector (8 channels)
</button> <button id="pm-mode-preset" class="pm-mode-btn px-3 py-1 rounded text-sm bg-kernel-800 text-kernel-400" data-astro-cid-qmyfqgs7>
Reference Entity
</button> </div> <!-- Kernel input --> <div id="pm-kernel-input" class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4" data-astro-cid-qmyfqgs7> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>F (Fidelity)</label> <input type="number" id="pm-F" value="0.750" step="0.01" min="0" max="1" class="w-full bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100" data-astro-cid-qmyfqgs7> </div> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>ω (Drift)</label> <input type="number" id="pm-omega" value="0.250" step="0.01" min="0" max="1" class="w-full bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100" disabled data-astro-cid-qmyfqgs7> </div> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>IC (Integrity)</label> <input type="number" id="pm-IC" value="0.500" step="0.01" min="0" max="1" class="w-full bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100" data-astro-cid-qmyfqgs7> </div> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>Δ (Gap = F − IC)</label> <input type="number" id="pm-delta" value="0.250" step="0.01" class="w-full bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100" disabled data-astro-cid-qmyfqgs7> </div> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>S (Entropy)</label> <input type="number" id="pm-S" value="0.550" step="0.01" min="0" max="2" class="w-full bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100" data-astro-cid-qmyfqgs7> </div> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>C (Curvature)</label> <input type="number" id="pm-C" value="0.150" step="0.01" min="0" max="1" class="w-full bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100" data-astro-cid-qmyfqgs7> </div> </div> <!-- Trace input (hidden by default) --> <div id="pm-trace-input" class="hidden mb-4" data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500 mb-1 block" data-astro-cid-qmyfqgs7>8-Channel Trace Vector (comma-separated)</label> <div class="flex gap-2" data-astro-cid-qmyfqgs7> <input type="text" id="pm-trace-values" value="0.77, 0.82, 0.71, 0.88, 0.78, 0.76, 0.79, 0.65" class="flex-1 bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100 font-mono" data-astro-cid-qmyfqgs7> <button id="pm-compute-trace" class="px-3 py-1 bg-kernel-600 hover:bg-kernel-500 rounded text-sm text-kernel-100 transition" data-astro-cid-qmyfqgs7>
Compute
</button> </div> <p class="text-xs text-kernel-500 mt-1" data-astro-cid-qmyfqgs7>Each value in [0, 1]. Equal weights assumed.</p> </div> <!-- Preset selector (hidden by default) --> <div id="pm-preset-input" class="hidden mb-4" data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500 mb-1 block" data-astro-cid-qmyfqgs7>Select a Reference Entity</label> <select id="pm-entity-select" class="w-full bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-sm text-kernel-100" data-astro-cid-qmyfqgs7></select> </div> <!-- Scale filter --> <div class="flex gap-2 items-center mb-4" data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>Scale filter:</label> <select id="pm-scale-filter" class="bg-kernel-800 border border-kernel-600 rounded px-2 py-1 text-xs text-kernel-100" data-astro-cid-qmyfqgs7> <option value="all" data-astro-cid-qmyfqgs7>All scales</option> <option value="subatomic" data-astro-cid-qmyfqgs7>Subatomic</option> <option value="hadronic" data-astro-cid-qmyfqgs7>Hadronic</option> <option value="nuclear" data-astro-cid-qmyfqgs7>Nuclear</option> <option value="atomic" data-astro-cid-qmyfqgs7>Atomic</option> <option value="molecular" data-astro-cid-qmyfqgs7>Molecular</option> <option value="bulk" data-astro-cid-qmyfqgs7>Bulk Material</option> <option value="astronomical" data-astro-cid-qmyfqgs7>Astronomical</option> <option value="abstract" data-astro-cid-qmyfqgs7>Abstract / Emergent</option> </select> <button id="pm-identify-btn" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 rounded text-sm font-medium text-white transition" data-astro-cid-qmyfqgs7>
Identify ↵
</button> </div> </div> <!-- Results --> <div id="pm-identify-results" class="space-y-3" data-astro-cid-qmyfqgs7></div> </div> <!-- ═══════════ TAB 2: Interpret ═══════════ --> <div id="pm-interpret" class="pm-panel hidden space-y-4" data-astro-cid-qmyfqgs7> <div class="bg-kernel-900/50 border border-kernel-700 rounded-lg p-4" data-astro-cid-qmyfqgs7> <h3 class="text-lg font-semibold text-kernel-100 mb-3" data-astro-cid-qmyfqgs7>Physical Interpretation</h3> <p class="text-sm text-kernel-400 mb-4" data-astro-cid-qmyfqgs7>
Click a kernel invariant to see its physical meaning across different scales.
        Each number has a physical consequence.
</p> <!-- Invariant quick-buttons --> <div class="flex flex-wrap gap-2 mb-4" data-astro-cid-qmyfqgs7> <button class="pm-inv-btn px-3 py-1.5 rounded text-sm bg-kernel-700 hover:bg-kernel-600 text-kernel-100 transition" data-inv="F" data-astro-cid-qmyfqgs7>
F — Fidelity
</button> <button class="pm-inv-btn px-3 py-1.5 rounded text-sm bg-kernel-700 hover:bg-kernel-600 text-kernel-100 transition" data-inv="omega" data-astro-cid-qmyfqgs7>
ω — Drift
</button> <button class="pm-inv-btn px-3 py-1.5 rounded text-sm bg-kernel-700 hover:bg-kernel-600 text-kernel-100 transition" data-inv="IC" data-astro-cid-qmyfqgs7>
IC — Integrity
</button> <button class="pm-inv-btn px-3 py-1.5 rounded text-sm bg-kernel-700 hover:bg-kernel-600 text-kernel-100 transition" data-inv="delta" data-astro-cid-qmyfqgs7>
Δ — Heterogeneity Gap
</button> <button class="pm-inv-btn px-3 py-1.5 rounded text-sm bg-kernel-700 hover:bg-kernel-600 text-kernel-100 transition" data-inv="S" data-astro-cid-qmyfqgs7>
S — Entropy
</button> <button class="pm-inv-btn px-3 py-1.5 rounded text-sm bg-kernel-700 hover:bg-kernel-600 text-kernel-100 transition" data-inv="C" data-astro-cid-qmyfqgs7>
C — Curvature
</button> </div> </div> <!-- Interpretation panel --> <div id="pm-interpret-result" class="space-y-3" data-astro-cid-qmyfqgs7></div> </div> <!-- ═══════════ TAB 3: Predict Unknown ═══════════ --> <div id="pm-predict" class="pm-panel hidden space-y-4" data-astro-cid-qmyfqgs7> <div class="bg-kernel-900/50 border border-kernel-700 rounded-lg p-4" data-astro-cid-qmyfqgs7> <h3 class="text-lg font-semibold text-kernel-100 mb-3" data-astro-cid-qmyfqgs7>Predict Unknown Composition</h3> <p class="text-sm text-kernel-400 mb-4" data-astro-cid-qmyfqgs7>
Input a trace vector from an unknown or hypothetical system. The mapper will predict
        its physical scale, structure, composition, and stability based on kernel similarity
        to known entities. Novel signatures (high distance from all references) may indicate
        unknown matter compositions.
</p> <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4" id="pm-predict-channels" data-astro-cid-qmyfqgs7> <!-- 8 channel sliders generated by JS --> </div> <div class="flex gap-2 items-center" data-astro-cid-qmyfqgs7> <button id="pm-predict-random" class="px-3 py-1 bg-kernel-700 hover:bg-kernel-600 rounded text-sm text-kernel-400 transition" data-astro-cid-qmyfqgs7>
Random Trace
</button> <button id="pm-predict-novel" class="px-3 py-1 bg-kernel-700 hover:bg-kernel-600 rounded text-sm text-kernel-400 transition" data-astro-cid-qmyfqgs7>
Novel Region
</button> <button id="pm-predict-btn" class="px-4 py-1.5 bg-amber-600 hover:bg-amber-500 rounded text-sm font-medium text-white transition" data-astro-cid-qmyfqgs7>
Predict Properties ↵
</button> </div> </div> <!-- Prediction results --> <div id="pm-predict-results" class="space-y-3" data-astro-cid-qmyfqgs7></div> </div> <!-- ═══════════ TAB 4: Entity Atlas ═══════════ --> <div id="pm-atlas" class="pm-panel hidden space-y-4" data-astro-cid-qmyfqgs7> <div class="bg-kernel-900/50 border border-kernel-700 rounded-lg p-4" data-astro-cid-qmyfqgs7> <h3 class="text-lg font-semibold text-kernel-100 mb-3" data-astro-cid-qmyfqgs7>Entity Atlas</h3> <p class="text-sm text-kernel-400 mb-2" data-astro-cid-qmyfqgs7>
All reference entities plotted in kernel space. Hover for details. Click to load into Identify tab.
</p> <!-- Axis selectors --> <div class="flex gap-4 items-center mb-2" data-astro-cid-qmyfqgs7> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>X axis:</label> <select id="pm-atlas-x" class="bg-kernel-800 border border-kernel-600 rounded px-1 py-0.5 text-xs text-kernel-100" data-astro-cid-qmyfqgs7> <option value="F" selected data-astro-cid-qmyfqgs7>F (Fidelity)</option> <option value="omega" data-astro-cid-qmyfqgs7>ω (Drift)</option> <option value="IC" data-astro-cid-qmyfqgs7>IC (Integrity)</option> <option value="delta" data-astro-cid-qmyfqgs7>Δ (Gap)</option> <option value="S" data-astro-cid-qmyfqgs7>S (Entropy)</option> <option value="C" data-astro-cid-qmyfqgs7>C (Curvature)</option> </select> </div> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>Y axis:</label> <select id="pm-atlas-y" class="bg-kernel-800 border border-kernel-600 rounded px-1 py-0.5 text-xs text-kernel-100" data-astro-cid-qmyfqgs7> <option value="F" data-astro-cid-qmyfqgs7>F (Fidelity)</option> <option value="omega" data-astro-cid-qmyfqgs7>ω (Drift)</option> <option value="IC" selected data-astro-cid-qmyfqgs7>IC (Integrity)</option> <option value="delta" data-astro-cid-qmyfqgs7>Δ (Gap)</option> <option value="S" data-astro-cid-qmyfqgs7>S (Entropy)</option> <option value="C" data-astro-cid-qmyfqgs7>C (Curvature)</option> </select> </div> <div data-astro-cid-qmyfqgs7> <label class="text-xs text-kernel-500" data-astro-cid-qmyfqgs7>Color by:</label> <select id="pm-atlas-color" class="bg-kernel-800 border border-kernel-600 rounded px-1 py-0.5 text-xs text-kernel-100" data-astro-cid-qmyfqgs7> <option value="scale" selected data-astro-cid-qmyfqgs7>Scale</option> <option value="regime" data-astro-cid-qmyfqgs7>Regime</option> </select> </div> </div> </div> <!-- Atlas canvas --> <div class="bg-kernel-900/50 border border-kernel-700 rounded-lg p-4" data-astro-cid-qmyfqgs7> <canvas id="pm-atlas-canvas" width="800" height="500" class="w-full rounded border border-kernel-700" style="max-height: 500px;" data-astro-cid-qmyfqgs7></canvas> <div id="pm-atlas-tooltip" class="hidden absolute bg-kernel-800 border border-kernel-600 rounded px-3 py-2 text-xs text-kernel-200 shadow-lg z-10 max-w-sm pointer-events-none" data-astro-cid-qmyfqgs7></div> </div> <!-- Entity list --> <div id="pm-atlas-list" class="space-y-2" data-astro-cid-qmyfqgs7></div> </div> </div>  ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/components/PhysicalMapper.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/components/PhysicalMapper.astro", void 0);

const $$Mapper = createComponent(($$result, $$props, $$slots) => {
  const sections = ["about", "mapper", "scales", "methodology"];
  const scales = [
    { name: "Subatomic", color: "text-red-400", border: "border-red-800/40", bg: "bg-red-900/20", entities: "Quarks, leptons, bosons, hadrons", channels: "mass_log, spin, charge, color, weak_isospin, lepton_num, baryon_num, generation" },
    { name: "Nuclear", color: "text-orange-400", border: "border-orange-800/40", bg: "bg-orange-900/20", entities: "Nuclei, isotopes, decay chains, QGP", channels: "BE/A, magic_proximity, neutron_excess, shell_filling" },
    { name: "Atomic", color: "text-amber-400", border: "border-amber-800/40", bg: "bg-amber-900/20", entities: "118 elements, electron configs", channels: "ionization_energy, electronegativity, density, melting_pt, boiling_pt, atomic_radius" },
    { name: "Material", color: "text-green-400", border: "border-green-800/40", bg: "bg-green-900/20", entities: "Crystals, alloys, polymers", channels: "18-field element database incl. bulk properties" },
    { name: "Biological", color: "text-cyan-400", border: "border-cyan-800/40", bg: "bg-cyan-900/20", entities: "Organisms, neural systems, brain regions", channels: "10-channel brain kernel, neural correlates" },
    { name: "Cosmological", color: "text-blue-400", border: "border-blue-800/40", bg: "bg-blue-900/20", entities: "Stars, galaxies, spacetime structures", channels: "Stellar classification, HR diagram, gravitational memory" }
  ];
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Physical Signature Mapper — GCD", "description": "Map kernel invariants to real-world physical entities across all scales." }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <!-- ═══════════ HERO ═══════════ --> <div class="mb-8"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Physical Signature Mapper</h1> <p class="text-kernel-400 text-lg italic">Quid supersit post collapsum? — What survives collapse?</p> <p class="text-kernel-500 text-sm mt-2 max-w-3xl">
Every physical entity has a kernel signature &mdash; the six invariants (F, &omega;, S, C, &kappa;, IC)
        computed from its measurable properties mapped to a trace vector. This tool identifies
        known matter by its signature, interprets what each invariant means physically, predicts
        properties of unknown compositions, and lets you explore reference entities across every scale.
</p> </div> <!-- ═══════════ NAV ═══════════ --> <nav class="mb-8 flex flex-wrap gap-2"> ${sections.map((s) => renderTemplate`<a${addAttribute(`#${s}`, "href")} class="px-3 py-1.5 rounded-full text-xs font-medium
          bg-kernel-800/60 text-kernel-400 hover:text-kernel-200 hover:bg-kernel-700/60
          border border-kernel-700/40 transition no-underline"> ${s.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())} </a>`)} </nav> <!-- ═══════════ §1: ABOUT ═══════════ --> <section id="about" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">How Physical Mapping Works</h2> <div class="grid grid-cols-1 md:grid-cols-2 gap-4"> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <h3 class="text-sm font-bold text-kernel-200 mb-2">Trace Construction (Tier-2)</h3> <p class="text-xs text-kernel-400">
Each domain closure selects which <strong>measurable properties</strong> become channels c&#7522;
            in the trace vector. A quark has 8 channels (mass, spin, charge, color, &hellip;).
            An atom has 12 (nuclear + electronic + bulk). Channel selection IS the Tier-2 contribution.
</p> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <h3 class="text-sm font-bold text-kernel-200 mb-2">Kernel Computation (Tier-1)</h3> <p class="text-xs text-kernel-400">
The kernel K: [0,1]&#8319; &times; &Delta;&#8319; &rarr; (F, &omega;, S, C, &kappa;, IC)
            is domain-independent. The same function that analyzes quarks also analyzes
            neurons, poems, and financial portfolios. Only the channels differ.
</p> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <h3 class="text-sm font-bold text-kernel-200 mb-2">Signature Matching</h3> <p class="text-xs text-kernel-400">
Given a kernel signature, the mapper searches reference entities across scales
            to find matches. A signature with IC/F &lt; 0.04 and high &Delta; suggests
            confinement (geometric slaughter from a dead channel). A signature with IC/F &gt; 0.95
            suggests coherent structure.
</p> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <h3 class="text-sm font-bold text-kernel-200 mb-2">Cross-Scale Universality</h3> <p class="text-xs text-kernel-400">
The same kernel detects confinement in quarks (IC drops 98% at the hadron boundary),
            shell closure in atoms (magic numbers), and phase transitions in materials &mdash;
            all as instances of geometric slaughter at structural boundaries.
</p> </div> </div> </section> <!-- ═══════════ §2: MAPPER ═══════════ --> <section id="mapper" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Interactive Mapper</h2> ${renderComponent($$result2, "PhysicalMapper", $$PhysicalMapper, {})} </section> <!-- ═══════════ §3: SCALES ═══════════ --> <section id="scales" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Scale Coverage</h2> <p class="text-sm text-kernel-400 mb-4">
The mapper spans 6 scales &mdash; from quarks to cosmological structures.
        Each scale has its own channel vocabulary (Tier-2) but shares the same kernel (Tier-1).
</p> <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3"> ${scales.map((s) => renderTemplate`<div${addAttribute(`${s.bg} border ${s.border} rounded-lg p-4`, "class")}> <h3${addAttribute(`text-sm font-bold ${s.color} mb-2`, "class")}>${s.name}</h3> <p class="text-xs text-kernel-400 mb-2">${s.entities}</p> <p class="text-[10px] text-kernel-600 font-mono">${s.channels}</p> </div>`)} </div> </section> <!-- ═══════════ §4: METHODOLOGY ═══════════ --> <section id="methodology" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Methodology</h2> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-kernel-400"> <div> <h3 class="text-sm font-bold text-kernel-200 mb-2">Embedding</h3> <p>
Raw physical data &rarr; normalized trace vector c &isin; [0,1]&#8319; via pre_clip
              policy (frozen). Min-max normalization with domain bounds [0, 1]. Guard band
              &epsilon; = 10&#8315;&#8312; prevents logarithmic poles.
</p> </div> <div> <h3 class="text-sm font-bold text-kernel-200 mb-2">Regime Detection</h3> <p>
Four-gate criterion: Stable requires &omega; &lt; 0.038 AND F &gt; 0.90 AND S &lt; 0.15
              AND C &lt; 0.14 (conjunctive). Watch is intermediate. Collapse: &omega; &ge; 0.30.
              Critical: IC &lt; 0.30 (severity overlay).
</p> </div> <div> <h3 class="text-sm font-bold text-kernel-200 mb-2">Key Diagnostic</h3> <p>
The heterogeneity gap &Delta; = F &minus; IC is the central diagnostic.
              Small &Delta; means all channels contribute equally. Large &Delta; means
              one or more channels are near dead &mdash; the signature of confinement,
              phase boundaries, and structural transitions.
</p> </div> </div> </div> </section> <!-- Footer --> <div class="text-center text-kernel-600 text-xs italic pb-8">
Non agens mensurat, sed structura. — Not the agent measures, but the structure.
</div> </div> ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/mapper.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/mapper.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/mapper";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Mapper,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
