import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { g as getCollection, r as renderEntry } from './_astro_content_DlhPuBG1.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout, I as IDENTITY_COUNT, L as LEMMA_COUNT, T as TEST_COUNT } from './BaseLayout_CFgWoUUk.mjs';

const $$IndexLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$IndexLayout;
  const { frontmatter } = Astro2.props;
  const { title = "Generative Collapse Dynamics", description = "A single-axiom mathematical framework that measures what survives collapse and what returns — across 23 scientific domains." } = frontmatter || {};
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  const toolCategories = [
    {
      name: "Compute",
      tools: [
        { name: "Calculator", href: `${base}calculator/`, desc: "Kernel invariants from any trace vector" },
        { name: "Formulas", href: `${base}formulas/`, desc: "Build & sweep mathematical expressions" },
        { name: "Mapper", href: `${base}mapper/`, desc: "Map kernel signatures to real physics" }
      ]
    },
    {
      name: "Visualize",
      tools: [
        { name: "Regime", href: `${base}regime/`, desc: "Phase diagram: Stable / Watch / Collapse" },
        { name: "τ_R*", href: `${base}diagnostics/`, desc: "Thermodynamic return diagnostic" },
        { name: "Seam Budget", href: `${base}seam-budget/`, desc: "Explore Γ(ω), D_C, and Δκ budget" }
      ]
    },
    {
      name: "Verify",
      tools: [
        { name: "Precision", href: `${base}precision/`, desc: "15-decimal identity verification sweep" },
        { name: "Identities", href: `${base}identities/`, desc: "44 structural identities with proofs" },
        { name: "Scale Ladder", href: `${base}scale-ladder/`, desc: "Cross-scale IC/F coherence" }
      ]
    },
    {
      name: "Reference",
      tools: [
        { name: "Mathematics", href: `${base}mathematics/`, desc: "Full algebra, calculus, convergence" },
        { name: "Geometry", href: `${base}geometry/`, desc: "Flat manifold, Fisher metric, proofs" },
        { name: "Rosetta", href: `${base}rosetta/`, desc: "Cross-domain 6-lens translation" },
        { name: "Ledger", href: `${base}ledger/`, desc: "Domain overview with kernel metrics" },
        { name: "Index", href: `${base}reference/`, desc: "Searchable cross-reference" }
      ]
    }
  ];
  const corpus = [
    { title: "Grammar of Return", desc: "Five words, one spine — how every claim is told, checked, and connected.", href: `${base}grammar/`, latin: "Quinque Verba" },
    { title: "Episteme of Return", desc: "Observation cost, cognitive equalizer, reproducibility.", href: `${base}epistemology/`, latin: "Episteme Reditus" },
    { title: "Philosophy of Collapse", desc: "Philosophical parallels computed through the kernel.", href: `${base}philosophy/`, latin: "Philosophia Collapsus" },
    { title: "Mathematics", desc: "Full algebra, calculus, convergence, seam calculus, rank theory.", href: `${base}mathematics/`, latin: "Mathematica Collapsus" },
    { title: "Geometry", desc: "The flat Bernoulli manifold, Fisher metric, composition algebra.", href: `${base}geometry/`, latin: "Geometria Manifoldum" },
    { title: "Orientation", desc: "Ten computational re-derivations. Understanding is computed.", href: `${base}orientation/`, latin: "Intellectus Computatur" }
  ];
  const domainCatalog = [
    { slug: "gcd", name: "Generative Collapse Dynamics", lens: "Epistemology", modules: 11, category: "Core", desc: "The axiom, the kernel, the spine.", channels: 6, theorems: 37 },
    { slug: "rcft", name: "Recursive Collapse Field Theory", lens: "Epistemology", modules: 13, category: "Core", desc: "Recursive field-theoretic structure of collapse.", channels: 8, theorems: 30 },
    { slug: "kinematics", name: "Kinematics", lens: "Ontology", modules: 11, category: "Physics", desc: "Motion, phase space, and trajectory analysis.", channels: 8, theorems: 34 },
    { slug: "weyl", name: "WEYL Cosmology", lens: "Ontology", modules: 7, category: "Physics", desc: "Modified gravity and cosmological structure.", channels: 8, theorems: 10 },
    { slug: "standard_model", name: "Standard Model", lens: "Ontology", modules: 14, category: "Physics", desc: "31 particles → 8-channel trace. 30 proven theorems.", channels: 8, theorems: 30 },
    { slug: "nuclear_physics", name: "Nuclear Physics", lens: "Ontology", modules: 14, category: "Physics", desc: "Binding energy, decay, QGP, confinement.", channels: 8, theorems: 51 },
    { slug: "quantum_mechanics", name: "Quantum Mechanics", lens: "Phenomenology", modules: 21, category: "Physics", desc: "Wavefunction, entanglement, QDM, FQHE.", channels: 8, theorems: 99 },
    { slug: "atomic_physics", name: "Atomic Physics", lens: "Ontology", modules: 12, category: "Physics", desc: "118 elements — full periodic kernel.", channels: 8, theorems: 26 },
    { slug: "materials_science", name: "Materials Science", lens: "Ontology", modules: 23, category: "Physics", desc: "118 elements × 18 fields.", channels: 8, theorems: 52 },
    { slug: "everyday_physics", name: "Everyday Physics", lens: "Phenomenology", modules: 8, category: "Physics", desc: "Thermo, optics, E&M, waves, fluids.", channels: 8, theorems: 29 },
    { slug: "finance", name: "Finance", lens: "Policy", modules: 5, category: "Applied", desc: "Portfolio continuity and market coherence.", channels: 8, theorems: 22 },
    { slug: "security", name: "Security & Audit", lens: "Policy", modules: 18, category: "Applied", desc: "Input validation, audit, integrity.", channels: 8, theorems: 22 },
    { slug: "astronomy", name: "Astronomy", lens: "Ontology", modules: 12, category: "Science", desc: "Stellar classification, HR diagram, ages.", channels: 8, theorems: 42 },
    { slug: "evolution", name: "Evolution & Neuroscience", lens: "History", modules: 9, category: "Biology", desc: "40 organisms, 10-channel brain kernel.", channels: 10, theorems: 22 },
    { slug: "consciousness_coherence", name: "Consciousness Coherence", lens: "Phenomenology", modules: 5, category: "Cognition", desc: "20 systems, 28 theorems, altered states.", channels: 8, theorems: 28 },
    { slug: "awareness_cognition", name: "Awareness & Cognition", lens: "Phenomenology", modules: 4, category: "Cognition", desc: "5+5 channel awareness-aptitude kernel.", channels: 10, theorems: 22 },
    { slug: "clinical_neuroscience", name: "Clinical Neuroscience", lens: "Phenomenology", modules: 8, category: "Cognition", desc: "10-channel cortical kernel, neurotransmitters.", channels: 10, theorems: 53 },
    { slug: "dynamic_semiotics", name: "Dynamic Semiotics", lens: "Semiotics", modules: 8, category: "Humanities", desc: "30 sign systems, 8-channel semiotic kernel.", channels: 8, theorems: 40 },
    { slug: "continuity_theory", name: "Continuity Theory", lens: "History", modules: 5, category: "Humanities", desc: "Continuity law, topological persistence.", channels: 8, theorems: 29 },
    { slug: "spacetime_memory", name: "Spacetime Memory", lens: "Ontology", modules: 8, category: "Physics", desc: "40 entities, gravitational memory.", channels: 8, theorems: 46 },
    { slug: "immunology", name: "Immunology", lens: "Phenomenology", modules: 6, category: "Biology", desc: "Immune cell kernel, cytokine networks, vaccine response.", channels: 8, theorems: 36 },
    { slug: "ecology", name: "Ecology", lens: "History", modules: 3, category: "Biology", desc: "12 ecological states, trophic cascades.", channels: 5, theorems: 2 },
    { slug: "information_theory", name: "Information Theory", lens: "Epistemology", modules: 3, category: "Applied", desc: "10 complexity classes, computability kernel.", channels: 5, theorems: 2 }
  ];
  const categories = ["Core", "Physics", "Science", "Biology", "Cognition", "Applied", "Humanities"];
  const categoryColors = {
    Core: "text-amber-400 border-amber-600/30",
    Physics: "text-blue-400 border-blue-600/30",
    Science: "text-cyan-400 border-cyan-600/30",
    Biology: "text-green-400 border-green-600/30",
    Cognition: "text-purple-400 border-purple-600/30",
    Applied: "text-emerald-400 border-emerald-600/30",
    Humanities: "text-rose-400 border-rose-600/30"
  };
  const toolCatColors = {
    Compute: "text-amber-400",
    Visualize: "text-blue-400",
    Verify: "text-green-400",
    Reference: "text-purple-400"
  };
  const lensColors = {
    Epistemology: "text-amber-400",
    Ontology: "text-blue-400",
    Phenomenology: "text-purple-400",
    History: "text-rose-400",
    Policy: "text-emerald-400",
    Semiotics: "text-cyan-400"
  };
  const totalTheorems = 746;
  const totalModules = domainCatalog.reduce((s, d) => s + d.modules, 0);
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": title, "description": description }, { "default": ($$result2) => renderTemplate`  ${maybeRenderHead()}<section class="text-center py-24 md:py-32 relative" id="hero"> <div class="absolute inset-0 -z-10 overflow-hidden"> <canvas id="hero-canvas" class="w-full h-full opacity-25"></canvas> </div> <p class="text-xs tracking-[0.3em] uppercase text-kernel-500 mb-6">Single-Axiom Mathematical Framework</p> <h1 class="text-5xl md:text-7xl font-bold tracking-tight mb-8 leading-[1.1]">
Generative Collapse<br> <span class="text-amber-400">Dynamics</span> </h1> <blockquote class="text-lg md:text-xl text-kernel-300 italic mb-2 max-w-2xl mx-auto font-light">
"Collapse is generative; only what returns is real."
</blockquote> <p class="text-xs text-kernel-600 font-mono italic mb-12">
Collapsus generativus est; solum quod redit, reale est.
</p> <p class="text-kernel-400 max-w-2xl mx-auto mb-12 leading-relaxed text-sm md:text-base">
A mathematical framework built from a single axiom — measuring what survives collapse
      and what returns, verified across
<strong class="text-kernel-200">${domainCatalog.length} domains</strong>,
<strong class="text-kernel-200">${totalTheorems}+ theorems</strong>, and
<strong class="text-kernel-200">44 structural identities</strong>.
</p> <div class="flex flex-wrap gap-3 justify-center"> <a${addAttribute(`${base}calculator/`, "href")} class="px-8 py-3 bg-amber-500 hover:bg-amber-400 text-kernel-950 font-semibold rounded-lg transition text-sm shadow-lg shadow-amber-500/20">
Open Calculator
</a> <a${addAttribute(`${base}mathematics/`, "href")} class="px-8 py-3 bg-kernel-800/80 hover:bg-kernel-700 text-kernel-200 font-medium rounded-lg border border-kernel-700/50 transition text-sm">
Read the Mathematics
</a> <a${addAttribute(`${base}about/`, "href")} class="px-8 py-3 text-kernel-400 hover:text-kernel-200 font-medium rounded-lg transition text-sm">
What is GCD?
</a> </div> </section>  <section class="py-20 border-t border-kernel-800/40 relative"> <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-px bg-gradient-to-r from-transparent via-amber-500/60 to-transparent"></div> <div class="text-center mb-12"> <p class="text-xs tracking-[0.2em] uppercase text-kernel-600 mb-3">The Kernel Function</p> <h2 class="text-3xl font-bold text-kernel-100">K: [0,1]<sup>n</sup> &times; &Delta;<sup>n</sup> &rarr; (F, &omega;, S, C, &kappa;, IC)</h2> <p class="text-sm text-kernel-500 mt-4 max-w-xl mx-auto">
Four equations, six outputs, three effective degrees of freedom — the complete measurement of collapse and return.
</p> </div> <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8"> <div class="text-center py-6 rounded-xl bg-kernel-900/50 hover:bg-kernel-900/80 transition group"> <div class="text-3xl font-bold text-amber-400 font-mono mb-2 group-hover:scale-110 transition-transform">F</div> <div class="text-sm text-kernel-300">Fidelity</div> <div class="text-[10px] text-kernel-600 font-mono mt-1">&Sigma; w<sub>i</sub>c<sub>i</sub></div> </div> <div class="text-center py-6 rounded-xl bg-kernel-900/50 hover:bg-kernel-900/80 transition group"> <div class="text-3xl font-bold text-red-400 font-mono mb-2 group-hover:scale-110 transition-transform">&omega;</div> <div class="text-sm text-kernel-300">Drift</div> <div class="text-[10px] text-kernel-600 font-mono mt-1">1 &minus; F</div> </div> <div class="text-center py-6 rounded-xl bg-kernel-900/50 hover:bg-kernel-900/80 transition group"> <div class="text-3xl font-bold text-blue-400 font-mono mb-2 group-hover:scale-110 transition-transform">S</div> <div class="text-sm text-kernel-300">Entropy</div> <div class="text-[10px] text-kernel-600 font-mono mt-1">Bernoulli field</div> </div> <div class="text-center py-6 rounded-xl bg-kernel-900/50 hover:bg-kernel-900/80 transition group"> <div class="text-3xl font-bold text-green-400 font-mono mb-2 group-hover:scale-110 transition-transform">C</div> <div class="text-sm text-kernel-300">Curvature</div> <div class="text-[10px] text-kernel-600 font-mono mt-1">&sigma;(c<sub>i</sub>)/0.5</div> </div> <div class="text-center py-6 rounded-xl bg-kernel-900/50 hover:bg-kernel-900/80 transition group"> <div class="text-3xl font-bold text-purple-400 font-mono mb-2 group-hover:scale-110 transition-transform">&kappa;</div> <div class="text-sm text-kernel-300">Log-integrity</div> <div class="text-[10px] text-kernel-600 font-mono mt-1">&Sigma; w<sub>i</sub> ln c<sub>i</sub></div> </div> <div class="text-center py-6 rounded-xl bg-kernel-900/50 hover:bg-kernel-900/80 transition group"> <div class="text-3xl font-bold text-cyan-400 font-mono mb-2 group-hover:scale-110 transition-transform">IC</div> <div class="text-sm text-kernel-300">Integrity</div> <div class="text-[10px] text-kernel-600 font-mono mt-1">exp(&kappa;)</div> </div> </div> <div class="flex flex-wrap gap-6 justify-center text-xs"> <a${addAttribute(`${base}mathematics/`, "href")} class="text-kernel-500 hover:text-amber-400 transition">Full algebra &rarr;</a> <a${addAttribute(`${base}geometry/`, "href")} class="text-kernel-500 hover:text-blue-400 transition">Geometric structure &rarr;</a> <a${addAttribute(`${base}calculator/`, "href")} class="text-kernel-500 hover:text-green-400 transition">Compute live &rarr;</a> </div> </section>  <section class="py-20 border-t border-kernel-800/40 relative"> <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-px bg-gradient-to-r from-transparent via-blue-500/60 to-transparent"></div> <div class="text-center mb-12"> <p class="text-xs tracking-[0.2em] uppercase text-kernel-600 mb-3">Every claim follows the same path</p> <h2 class="text-3xl font-bold text-kernel-100">The Spine</h2> </div> <div class="flex flex-wrap items-center justify-center gap-2 md:gap-3 text-sm font-mono mb-10"> <div class="px-5 py-3 text-amber-400 rounded-xl bg-amber-500/10 border border-amber-500/20">Contract</div> <span class="text-kernel-700 text-lg">&rarr;</span> <div class="px-5 py-3 text-blue-400 rounded-xl bg-blue-500/10 border border-blue-500/20">Canon</div> <span class="text-kernel-700 text-lg">&rarr;</span> <div class="px-5 py-3 text-green-400 rounded-xl bg-green-500/10 border border-green-500/20">Closures</div> <span class="text-kernel-700 text-lg">&rarr;</span> <div class="px-5 py-3 text-purple-400 rounded-xl bg-purple-500/10 border border-purple-500/20">Ledger</div> <span class="text-kernel-700 text-lg">&rarr;</span> <div class="px-5 py-3 text-cyan-400 rounded-xl bg-cyan-500/10 border border-cyan-500/20">Stance</div> </div> <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto"> <div class="pl-4 border-l-2 border-amber-500/30"> <div class="text-[10px] uppercase tracking-widest text-amber-400/70 mb-1">Tier-1 &middot; Immutable</div> <h3 class="text-base font-semibold text-kernel-200 mb-2">The Kernel</h3> <p class="text-xs text-kernel-500 leading-relaxed">The mathematical function plus 3 algebraic identities, 44 structural identities, 47 lemmas, and 5 frozen constants.</p> </div> <div class="pl-4 border-l-2 border-blue-500/30"> <div class="text-[10px] uppercase tracking-widest text-blue-400/70 mb-1">Tier-0 &middot; Protocol</div> <h3 class="text-base font-semibold text-kernel-200 mb-2">The Implementation</h3> <p class="text-xs text-kernel-500 leading-relaxed">Python + C99 + C++ implementations. Three-valued verdicts. Frozen parameters from the seam. The code is Tier-0; what it computes is Tier-1.</p> </div> <div class="pl-4 border-l-2 border-green-500/30"> <div class="text-[10px] uppercase tracking-widest text-green-400/70 mb-1">Tier-2 &middot; Expansion</div> <h3 class="text-base font-semibold text-kernel-200 mb-2">Domain Closures</h3> <p class="text-xs text-kernel-500 leading-relaxed">${domainCatalog.length} domains select which real-world quantities become channels. ${totalTheorems}+ theorems, ${totalModules} modules. Same kernel, different questions.</p> </div> </div> </section>  <section class="py-20 border-t border-kernel-800/40 relative"> <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-px bg-gradient-to-r from-transparent via-green-500/60 to-transparent"></div> <div class="text-center mb-12"> <p class="text-xs tracking-[0.2em] uppercase text-kernel-600 mb-3">Client-side &middot; No server required</p> <h2 class="text-3xl font-bold text-kernel-100">Interactive Tools</h2> </div> <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-5xl mx-auto"> ${toolCategories.flatMap((cat) => {
    const textColor = toolCatColors[cat.name] || "text-kernel-400";
    return cat.tools.map((t) => renderTemplate`<a${addAttribute(t.href, "href")} class="flex items-center gap-4 px-5 py-4 rounded-xl bg-kernel-900/40 hover:bg-kernel-900/80 border border-kernel-800/40 hover:border-kernel-700/60 transition group no-underline"> <div> <div class="flex items-center gap-2"> <span class="text-sm font-medium text-kernel-200 group-hover:text-amber-400 transition">${t.name}</span> <span${addAttribute(`text-[9px] uppercase tracking-widest ${textColor} opacity-60`, "class")}>${cat.name}</span> </div> <div class="text-xs text-kernel-500">${t.desc}</div> </div> </a>`);
  })} </div> </section>  <section class="py-20 border-t border-kernel-800/40 relative" id="domains"> <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-px bg-gradient-to-r from-transparent via-purple-500/60 to-transparent"></div> <div class="text-center mb-8"> <p class="text-xs tracking-[0.2em] uppercase text-kernel-600 mb-3">From quarks to consciousness</p> <h2 class="text-3xl font-bold text-kernel-100">${domainCatalog.length} Domain Closures</h2> <p class="text-sm text-kernel-500 mt-3 max-w-lg mx-auto">Each domain selects which real-world quantities become channels. The kernel stays the same — only the question changes.</p> </div> <!-- Category filter --> <div class="flex flex-wrap gap-2 justify-center mb-8"> <button class="domain-cat-btn text-xs px-4 py-2 rounded-full bg-kernel-800 text-kernel-200 hover:bg-kernel-700 transition cursor-pointer" data-cat="all">
All
</button> ${categories.map((cat) => renderTemplate`<button${addAttribute(`domain-cat-btn text-xs px-4 py-2 rounded-full bg-kernel-900/60 hover:bg-kernel-800 transition cursor-pointer ${categoryColors[cat]?.split(" ")[0] || "text-kernel-400"}`, "class")}${addAttribute(cat, "data-cat")}> ${cat} </button>`)} </div> <!-- Domain grid --> <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3" id="domain-grid"> ${domainCatalog.map((d) => renderTemplate`<a${addAttribute(`${base}${d.slug}/`, "href")}${addAttribute(`domain-card rounded-xl px-5 py-4 border bg-kernel-900/30 hover:bg-kernel-900/60 transition group no-underline block ${categoryColors[d.category]?.split(" ").slice(1).join(" ") || "border-kernel-800/40"}`, "class")}${addAttribute(d.category, "data-category")}${addAttribute(d.lens, "data-lens")}> <div class="flex items-center gap-2 mb-1"> <span${addAttribute(`inline-block w-1.5 h-1.5 rounded-full ${categoryColors[d.category]?.split(" ")[0]?.replace("text-", "bg-") || "bg-kernel-500"}`, "class")}></span> <span class="text-sm font-medium text-kernel-200 group-hover:text-amber-400 transition">${d.name}</span> </div> <p class="text-xs text-kernel-500 mb-3">${d.desc}</p> <div class="flex items-center gap-2 text-[10px] text-kernel-600"> <span>${d.modules} modules</span> <span class="text-kernel-800">&middot;</span> <span>${d.theorems} theorems</span> <span class="text-kernel-800">&middot;</span> <span${addAttribute(`${lensColors[d.lens] || "text-kernel-500"}`, "class")}>${d.lens}</span> </div> </a>`)} </div> </section>  <section class="py-20 border-t border-kernel-800/40 relative"> <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-px bg-gradient-to-r from-transparent via-cyan-500/60 to-transparent"></div> <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-8 text-center max-w-5xl mx-auto"> <div> <div class="text-3xl font-bold text-amber-400">1</div> <div class="text-[11px] text-kernel-500 mt-1">Axiom</div> </div> <div> <div class="text-3xl font-bold text-kernel-300">6</div> <div class="text-[11px] text-kernel-500 mt-1">Invariants</div> </div> <div> <div class="text-3xl font-bold text-kernel-300">3</div> <div class="text-[11px] text-kernel-500 mt-1">DOF</div> </div> <div> <div class="text-3xl font-bold text-kernel-300">${domainCatalog.length}</div> <div class="text-[11px] text-kernel-500 mt-1">Domains</div> </div> <div> <div class="text-3xl font-bold text-kernel-300">${IDENTITY_COUNT}</div> <div class="text-[11px] text-kernel-500 mt-1">Identities</div> </div> <div> <div class="text-3xl font-bold text-kernel-300">${LEMMA_COUNT}</div> <div class="text-[11px] text-kernel-500 mt-1">Lemmas</div> </div> <div> <div class="text-3xl font-bold text-kernel-300">${totalModules}</div> <div class="text-[11px] text-kernel-500 mt-1">Modules</div> </div> <div> <div class="text-3xl font-bold text-amber-400">${TEST_COUNT}</div> <div class="text-[11px] text-kernel-500 mt-1">Tests</div> </div> </div> </section>  <section class="py-20 border-t border-kernel-800/40 relative"> <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-px bg-gradient-to-r from-transparent via-amber-500/40 to-transparent"></div> <div class="grid grid-cols-1 lg:grid-cols-2 gap-16"> <!-- Corpus --> <div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-600 mb-6">Deep Reading</p> <div class="space-y-3"> ${corpus.map((c) => renderTemplate`<a${addAttribute(c.href, "href")} class="flex items-center justify-between px-5 py-3 rounded-xl hover:bg-kernel-900/60 transition group no-underline block"> <div> <div class="text-sm font-medium text-kernel-200 group-hover:text-amber-400 transition">${c.title}</div> <div class="text-xs text-kernel-500">${c.desc}</div> </div> <span class="text-[10px] text-kernel-700 italic font-mono shrink-0 ml-4">${c.latin}</span> </a>`)} </div> </div> <!-- Papers --> <div> <div class="flex items-center justify-between mb-6"> <p class="text-xs tracking-[0.2em] uppercase text-kernel-600">Published Papers</p> <a${addAttribute(`${base}papers/`, "href")} class="text-xs text-kernel-600 hover:text-amber-400 transition">View all &rarr;</a> </div> <div class="space-y-3"> <a${addAttribute(`${base}papers/`, "href")} class="block px-5 py-3 rounded-xl hover:bg-kernel-900/60 transition group no-underline"> <div class="text-sm font-medium text-kernel-200 group-hover:text-amber-400 transition">Standard Model Kernel</div> <div class="text-xs text-kernel-500">31 particles, 10 theorems, 74/74 subtests</div> </a> <a${addAttribute(`${base}papers/`, "href")} class="block px-5 py-3 rounded-xl hover:bg-kernel-900/60 transition group no-underline"> <div class="text-sm font-medium text-kernel-200 group-hover:text-amber-400 transition">RCFT Second Edition</div> <div class="text-xs text-kernel-500">Recursive collapse field theory foundations</div> </a> <a${addAttribute(`${base}papers/`, "href")} class="block px-5 py-3 rounded-xl hover:bg-kernel-900/60 transition group no-underline"> <div class="text-sm font-medium text-kernel-200 group-hover:text-amber-400 transition">Cross-Scale Matter</div> <div class="text-xs text-kernel-500">Quarks to bulk via five phase boundaries</div> </a> <a${addAttribute(`${base}papers/`, "href")} class="block px-5 py-3 rounded-xl hover:bg-kernel-900/60 transition group no-underline"> <div class="text-sm font-medium text-kernel-200 group-hover:text-amber-400 transition">Consciousness Coherence</div> <div class="text-xs text-kernel-500">Seven theorems in the GCD kernel</div> </a> </div> </div> </div> </section> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/IndexLayout.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/IndexLayout.astro", void 0);

const $$Index = createComponent(async ($$result, $$props, $$slots) => {
  const indexEntries = await getCollection("networkIndex");
  const entry = indexEntries[0];
  const { Content } = await renderEntry(entry);
  return renderTemplate`${renderComponent($$result, "IndexLayout", $$IndexLayout, { "frontmatter": entry.data }, { "default": async ($$result2) => renderTemplate` ${renderComponent($$result2, "Content", Content, {})} ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/index.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/index.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
