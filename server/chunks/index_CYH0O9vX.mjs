import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute, d as renderSlot } from './server_DjVGnHP9.mjs';
import { g as getCollection, r as renderEntry } from './_astro_content_DlhPuBG1.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$DomainLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$DomainLayout;
  const { frontmatter } = Astro2.props;
  const {
    title = "Domain",
    description = "",
    domain = "",
    regime = "UNKNOWN",
    primaryColor = "#0f172a",
    accentColor = "#f59e0b",
    icon = "atom",
    lens = "Ontology"
  } = frontmatter || {};
  const regimeColors = {
    STABLE: "bg-stable/20 text-stable border-stable/40",
    WATCH: "bg-watch/20 text-watch border-watch/40",
    COLLAPSE: "bg-collapse/20 text-collapse border-collapse/40",
    UNKNOWN: "bg-kernel-700/20 text-kernel-400 border-kernel-600/40"
  };
  const regimeBarColors = {
    STABLE: "bg-green-500",
    WATCH: "bg-amber-500",
    COLLAPSE: "bg-red-500",
    UNKNOWN: "bg-kernel-600"
  };
  const lensDescriptions = {
    Epistemology: "Drift = change in belief · Fidelity = retained warrant · Roughness = inference friction · Return = justified re-entry",
    Ontology: "Drift = state transition · Fidelity = conserved properties · Roughness = heterogeneity · Return = restored coherence",
    Phenomenology: "Drift = perceived shift · Fidelity = stable features · Roughness = distress/effort · Return = coping that holds",
    History: "Drift = periodization · Fidelity = what endures · Roughness = rupture · Return = restitution",
    Policy: "Drift = regime shift · Fidelity = mandate persistence · Roughness = friction/cost · Return = reinstatement",
    Semiotics: "Drift = sign departure · Fidelity = convention survived · Roughness = meaning loss · Return = interpretant closure"
  };
  const lensColors = {
    Epistemology: "text-amber-400 border-amber-700/50 bg-amber-900/20",
    Ontology: "text-blue-400 border-blue-700/50 bg-blue-900/20",
    Phenomenology: "text-purple-400 border-purple-700/50 bg-purple-900/20",
    History: "text-rose-400 border-rose-700/50 bg-rose-900/20",
    Policy: "text-emerald-400 border-emerald-700/50 bg-emerald-900/20",
    Semiotics: "text-cyan-400 border-cyan-700/50 bg-cyan-900/20"
  };
  const domainRelations = {
    gcd: ["rcft", "kinematics", "continuity_theory"],
    rcft: ["gcd", "quantum_mechanics", "standard_model"],
    kinematics: ["gcd", "everyday_physics", "spacetime_memory"],
    weyl: ["spacetime_memory", "astronomy", "standard_model"],
    standard_model: ["nuclear_physics", "quantum_mechanics", "atomic_physics"],
    nuclear_physics: ["standard_model", "atomic_physics", "materials_science"],
    quantum_mechanics: ["standard_model", "atomic_physics", "rcft"],
    atomic_physics: ["nuclear_physics", "materials_science", "quantum_mechanics"],
    materials_science: ["atomic_physics", "everyday_physics", "nuclear_physics"],
    everyday_physics: ["materials_science", "kinematics", "finance"],
    finance: ["security", "continuity_theory", "everyday_physics"],
    security: ["finance", "continuity_theory", "gcd"],
    astronomy: ["weyl", "spacetime_memory", "nuclear_physics"],
    evolution: ["awareness_cognition", "consciousness_coherence", "clinical_neuroscience"],
    consciousness_coherence: ["clinical_neuroscience", "awareness_cognition", "dynamic_semiotics"],
    awareness_cognition: ["consciousness_coherence", "evolution", "clinical_neuroscience"],
    clinical_neuroscience: ["consciousness_coherence", "awareness_cognition", "evolution"],
    dynamic_semiotics: ["consciousness_coherence", "continuity_theory", "gcd"],
    continuity_theory: ["gcd", "dynamic_semiotics", "finance"],
    spacetime_memory: ["weyl", "astronomy", "kinematics"]
  };
  const domainDisplayNames = {
    gcd: "GCD",
    rcft: "RCFT",
    kinematics: "Kinematics",
    weyl: "WEYL",
    standard_model: "Standard Model",
    nuclear_physics: "Nuclear Physics",
    quantum_mechanics: "Quantum Mechanics",
    atomic_physics: "Atomic Physics",
    materials_science: "Materials Science",
    everyday_physics: "Everyday Physics",
    finance: "Finance",
    security: "Security",
    astronomy: "Astronomy",
    evolution: "Evolution",
    consciousness_coherence: "Consciousness",
    awareness_cognition: "Awareness",
    clinical_neuroscience: "Clinical Neuro",
    dynamic_semiotics: "Semiotics",
    continuity_theory: "Continuity",
    spacetime_memory: "Spacetime Memory"
  };
  const related = domainRelations[domain] || [];
  const regimeBadge = regimeColors[regime] || regimeColors["UNKNOWN"];
  const regimeBar = regimeBarColors[regime] || regimeBarColors["UNKNOWN"];
  const lensColor = lensColors[lens] || "text-kernel-400 border-kernel-700 bg-kernel-900/20";
  const lensDesc = lensDescriptions[lens] || "";
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": title, "description": description, "primaryColor": primaryColor, "accentColor": accentColor }, { "default": ($$result2) => renderTemplate`  ${maybeRenderHead()}<div${addAttribute(`h-1 ${regimeBar} rounded-full mb-6 opacity-60`, "class")}></div>  <div class="mb-8"> <div class="flex items-center gap-3 mb-3"> <h1 class="text-3xl font-bold tracking-tight">${title}</h1> <span${addAttribute(`text-xs font-mono px-2.5 py-1 rounded border ${regimeBadge}`, "class")}> ${regime} </span> </div> ${description && renderTemplate`<p class="text-kernel-400 text-lg mb-3">${description}</p>`} <!-- Lens badge with Rosetta hint --> <div${addAttribute(`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs ${lensColor}`, "class")}> <span class="font-bold">Rosetta Lens: ${lens}</span> ${lensDesc && renderTemplate`<span class="hidden md:inline text-[10px] opacity-70">— ${lensDesc}</span>`} </div> <!-- Sub-page navigation — enhanced with icons and counts --> <nav class="flex flex-wrap gap-2 mt-5 pt-4 border-t border-kernel-800 text-sm"> <a${addAttribute(`${base}${domain}/`, "href")} class="px-3 py-1.5 rounded-lg bg-kernel-700 text-kernel-100 border border-kernel-600 font-medium transition-colors">
Overview
</a> <a${addAttribute(`${base}${domain}/contract`, "href")} class="px-3 py-1.5 rounded-lg bg-kernel-800 text-kernel-300 hover:bg-kernel-700 hover:text-kernel-100 transition-colors border border-kernel-700/50">
📜 Contract
</a> <a${addAttribute(`${base}${domain}/theorems`, "href")} class="px-3 py-1.5 rounded-lg bg-kernel-800 text-kernel-300 hover:bg-kernel-700 hover:text-kernel-100 transition-colors border border-kernel-700/50">
📐 Theorems
</a> <a${addAttribute(`${base}${domain}/entities`, "href")} class="px-3 py-1.5 rounded-lg bg-kernel-800 text-kernel-300 hover:bg-kernel-700 hover:text-kernel-100 transition-colors border border-kernel-700/50">
🔬 Entities
</a> <a${addAttribute(`${base}identities/`, "href")} class="px-3 py-1.5 rounded-lg bg-kernel-800/50 text-kernel-400 hover:bg-kernel-700 hover:text-kernel-100 transition-colors border border-kernel-700/30">
≡ Identities
</a> <a${addAttribute(`${base}calculator/`, "href")} class="px-3 py-1.5 rounded-lg bg-kernel-800/50 text-kernel-400 hover:bg-kernel-700 hover:text-kernel-100 transition-colors border border-kernel-700/30">
⊕ Calculator
</a> </nav> </div>  <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8"> <!-- Kernel state panel (3 cols) --> <div class="lg:col-span-3 bg-kernel-900 border border-kernel-700 rounded-lg p-5"> <div class="flex items-center justify-between mb-4"> <h2 class="text-sm font-bold text-kernel-300">Live Kernel State</h2> <button id="recompute-btn" class="text-xs px-3 py-1 rounded bg-kernel-800 text-kernel-400 hover:text-amber-400 hover:bg-kernel-700 transition border border-kernel-700">
Recompute ↻
</button> </div> <!-- Kernel gauges --> <div class="grid grid-cols-3 md:grid-cols-6 gap-3 mb-4" id="kernel-gauges"> <!-- Filled by script --> </div> <!-- Identity checks --> <div class="grid grid-cols-1 md:grid-cols-3 gap-2" id="identity-checks"> <!-- Filled by script --> </div> </div> <!-- Related domains sidebar (1 col) --> <div class="lg:col-span-1"> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4 mb-4"> <h3 class="text-xs font-bold text-kernel-400 mb-3">Related Domains</h3> <div class="space-y-2"> ${related.map((r) => renderTemplate`<a${addAttribute(`${base}${r}/`, "href")} class="flex items-center gap-2 px-2.5 py-2 rounded bg-kernel-800/60 text-kernel-300 hover:bg-kernel-700 hover:text-kernel-100 transition text-xs no-underline group border border-kernel-700/30 hover:border-kernel-600"> <span class="text-kernel-600 group-hover:text-amber-500 transition">→</span> <span>${domainDisplayNames[r] || r}</span> </a>`)} </div> </div> <!-- Quick links --> <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-4"> <h3 class="text-xs font-bold text-kernel-400 mb-3">Spine Stops</h3> <div class="space-y-1 text-xs"> <div class="flex items-center gap-2 text-kernel-500"> <span class="w-2 h-2 rounded-full bg-blue-500"></span> <span>Contract — freeze before evidence</span> </div> <div class="flex items-center gap-2 text-kernel-500"> <span class="w-2 h-2 rounded-full bg-green-500"></span> <span>Canon — narrate with 5 words</span> </div> <div class="flex items-center gap-2 text-kernel-500"> <span class="w-2 h-2 rounded-full bg-amber-500"></span> <span>Closures — publish thresholds</span> </div> <div class="flex items-center gap-2 text-kernel-500"> <span class="w-2 h-2 rounded-full bg-purple-500"></span> <span>Ledger — debit/credit reconcile</span> </div> <div class="flex items-center gap-2 text-kernel-500"> <span class="w-2 h-2 rounded-full bg-red-500"></span> <span>Stance — derived verdict</span> </div> </div> </div> </div> </div>  <article class="prose prose-invert prose-sm max-w-none
    prose-headings:font-bold prose-headings:tracking-tight
    prose-h2:text-xl prose-h2:mt-10 prose-h2:mb-4 prose-h2:border-b prose-h2:border-kernel-800 prose-h2:pb-2
    prose-h3:text-lg
    prose-table:text-sm
    prose-th:text-left prose-th:text-kernel-400 prose-th:font-normal prose-th:border-b prose-th:border-kernel-700 prose-th:py-2
    prose-td:py-2 prose-td:border-b prose-td:border-kernel-800
    prose-code:text-kernel-300 prose-code:bg-kernel-800 prose-code:px-1 prose-code:rounded
    prose-strong:text-kernel-100
    prose-blockquote:border-kernel-700 prose-blockquote:text-kernel-400
    prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline
    prose-li:marker:text-kernel-600"> ${renderSlot($$result2, $$slots["default"])} </article>  <div class="mt-12 pt-6 border-t border-kernel-800 flex justify-between items-center"> <a${addAttribute(`${base}`, "href")} class="text-sm text-kernel-500 hover:text-kernel-300 transition">← Domain Network</a> <div class="flex gap-2"> ${related.slice(0, 2).map((r) => renderTemplate`<a${addAttribute(`${base}${r}/`, "href")} class="text-xs text-kernel-500 hover:text-kernel-300 transition"> ${domainDisplayNames[r] || r} →
</a>`)} </div> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/DomainLayout.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/DomainLayout.astro", void 0);

async function getStaticPaths() {
  const domains = await getCollection("domains");
  return domains.map((entry) => {
    const slug = entry.id.replace(/\/index$/, "").replace(/^index$/, "");
    return {
      params: { domain: slug || entry.data.domain },
      props: { entry }
    };
  });
}
const $$Index = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$Index;
  const { entry } = Astro2.props;
  const { Content } = await renderEntry(entry);
  return renderTemplate`${renderComponent($$result, "DomainLayout", $$DomainLayout, { "frontmatter": entry.data }, { "default": async ($$result2) => renderTemplate` ${renderComponent($$result2, "Content", Content, {})} ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/[domain]/index.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/[domain]/index.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/[domain]";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
