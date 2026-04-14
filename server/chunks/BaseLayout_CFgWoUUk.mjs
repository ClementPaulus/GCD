import { l as defineStyleVars, r as renderTemplate, a as addAttribute, d as renderSlot, n as renderHead, u as unescapeHTML } from './server_DjVGnHP9.mjs';
import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'clsx';
import { r as renderScript } from './script_CjXWaIL1.mjs';

const TEST_COUNT = "20,235";
const DOMAIN_COUNT = "23";
const IDENTITY_COUNT = "44";
const LEMMA_COUNT = "47";
const CLOSURE_COUNT = "245";
const THEOREM_COUNT = "746";
const LANGUAGE_COUNT = "3";
const TEST_FILE_COUNT = "232";
const AT_A_GLANCE = [
  { n: TEST_COUNT, label: "Tests", icon: "✓" },
  { n: DOMAIN_COUNT, label: "Domains", icon: "◈" },
  { n: IDENTITY_COUNT, label: "Identities", icon: "≡" },
  { n: LEMMA_COUNT, label: "Lemmas", icon: "∴" },
  { n: CLOSURE_COUNT, label: "Closures", icon: "⊕" },
  { n: LANGUAGE_COUNT, label: "Languages", icon: "⟨⟩" }
];

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(cooked.slice()) }));
var _a;
const $$BaseLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$BaseLayout;
  const {
    title,
    description = "Generative Collapse Dynamics — a single-axiom mathematical framework with 23 domain closures, 44 structural identities, and interactive kernel computation.",
    primaryColor = "#0f172a",
    accentColor = "#f59e0b",
    ogImage = "",
    ogType = "website"
  } = Astro2.props;
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  const siteUrl = "https://calebpruett927.github.io/GENERATIVE-COLLAPSE-DYNAMICS";
  const canonicalUrl = new URL(Astro2.url.pathname, siteUrl).href;
  const fullTitle = `${title} — GCD`;
  const navGroups = [
    {
      label: "Explore",
      items: [
        { name: "Calculator", href: `${base}calculator/` },
        { name: "Regime Diagram", href: `${base}regime/` },
        { name: "Precision", href: `${base}precision/` },
        { name: "Formulas", href: `${base}formulas/` },
        { name: "Mapper", href: `${base}mapper/` },
        { name: "Seam Budget", href: `${base}seam-budget/` },
        { name: "τ_R* Diagnostic", href: `${base}diagnostics/` },
        { name: "Scale Ladder", href: `${base}scale-ladder/` },
        { name: "Cognitive Equalizer", href: `${base}cognitive-equalizer/` }
      ]
    },
    {
      label: "Theory",
      items: [
        { name: "Mathematics", href: `${base}mathematics/` },
        { name: "Geometry", href: `${base}geometry/` },
        { name: "Identities", href: `${base}identities/` },
        { name: "Grammar", href: `${base}grammar/` },
        { name: "Epistemology", href: `${base}epistemology/` },
        { name: "Philosophy", href: `${base}philosophy/` },
        { name: "Orientation", href: `${base}orientation/` }
      ]
    },
    {
      label: "Reference",
      items: [
        { name: "Rosetta", href: `${base}rosetta/` },
        { name: "Ledger", href: `${base}ledger/` },
        { name: "Index", href: `${base}reference/` },
        { name: "Continuity", href: `${base}continuity/` },
        { name: "Papers", href: `${base}papers/` },
        { name: "Deep Readings", href: `${base}readings/` }
      ]
    },
    {
      label: "Visualize",
      items: [
        { name: "Black Hole", href: `${base}blackhole/` },
        { name: "Space Sim", href: `${base}space/` },
        { name: "Brain", href: `${base}brain/` }
      ]
    }
  ];
  const $$definedVars = defineStyleVars([{ primaryColor, accentColor }]);
  return renderTemplate(_a || (_a = __template(['<html lang="en" data-astro-cid-37fxchfa', '> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description"', '><link rel="icon" type="image/svg+xml"', '><link rel="canonical"', "><title>", '</title><!-- Fonts --><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"><!-- Open Graph --><meta property="og:title"', '><meta property="og:description"', '><meta property="og:type"', '><meta property="og:url"', '><meta property="og:site_name" content="GCD">', '<!-- Twitter Card --><meta name="twitter:card" content="summary"><meta name="twitter:title"', '><meta name="twitter:description"', '><!-- Structured Data (JSON-LD) — machine-readable for AI agents and scrapers --><script type="application/ld+json">', '</script><!-- Project statistics — canonical machine-readable values for AI extraction --><meta name="gcd:version" content="2.3.1"><meta name="gcd:domains" content="23"><meta name="gcd:theorems" content="746"><meta name="gcd:tests" content="20221"><meta name="gcd:identities" content="44"><meta name="gcd:lemmas" content="47"><meta name="gcd:closure-modules" content="245"><meta name="gcd:test-files" content="231"><meta name="gcd:c-cpp-assertions" content="760"><meta name="gcd:frozen-parameters" content="epsilon=1e-8,p=3,alpha=1.0,lambda=0.2,tol_seam=0.005"><meta name="gcd:axiom" content="Collapse is generative; only what returns is real."><meta name="gcd:repository" content="https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS">', '</head> <body class="bg-kernel-950 text-kernel-100 min-h-screen antialiased" data-astro-cid-37fxchfa', '> <!-- Skip to content (accessibility) --> <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:bg-amber-500 focus:text-kernel-950 focus:px-4 focus:py-2 focus:rounded focus:text-sm focus:font-bold" data-astro-cid-37fxchfa', '>\nSkip to main content\n</a> <!-- Navigation --> <nav class="sticky top-0 z-40 border-b border-kernel-800/60 bg-kernel-950/80 backdrop-blur-xl" aria-label="Main navigation" data-astro-cid-37fxchfa', '> <div class="max-w-7xl mx-auto px-6 nav-px h-16 flex items-center justify-between" data-astro-cid-37fxchfa', "> <!-- Logo --> <a", ' class="flex items-center gap-2 group" aria-label="GCD home" data-astro-cid-37fxchfa', '> <span class="text-xl font-bold tracking-tight text-kernel-100 group-hover:text-amber-400 transition-colors" data-astro-cid-37fxchfa', '>GCD</span> <span class="hidden sm:inline text-xs text-kernel-500 font-light tracking-wide" data-astro-cid-37fxchfa', '>Generative Collapse Dynamics</span> </a> <!-- Desktop Navigation --> <div class="desktop-nav flex items-center gap-1" data-astro-cid-37fxchfa', "> <a", ' class="text-sm text-kernel-400 hover:text-kernel-100 transition-colors px-3 py-2 rounded-lg hover:bg-kernel-800/50" data-astro-cid-37fxchfa', ">Domains</a> ", " <a", ' class="text-sm text-kernel-400 hover:text-kernel-100 transition-colors px-3 py-2 rounded-lg hover:bg-kernel-800/50" data-astro-cid-37fxchfa', ">GCD CAI</a> <a", ' class="text-sm text-kernel-400 hover:text-kernel-100 transition-colors px-3 py-2 rounded-lg hover:bg-kernel-800/50" data-astro-cid-37fxchfa', '>About</a> <div class="w-px h-5 bg-kernel-800 mx-1" data-astro-cid-37fxchfa', '></div> <a href="https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS" class="text-sm text-kernel-400 hover:text-kernel-100 transition-colors px-3 py-2 rounded-lg hover:bg-kernel-800/50" target="_blank" rel="noopener" aria-label="GitHub (opens in new tab)" data-astro-cid-37fxchfa', '> <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" data-astro-cid-37fxchfa', '><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" data-astro-cid-37fxchfa', '></path></svg> </a> </div> <!-- Mobile toggle --> <button class="mobile-toggle items-center justify-center w-10 h-10 rounded-lg text-kernel-400 hover:text-kernel-100 hover:bg-kernel-800/50 transition" id="mobile-nav-toggle" aria-label="Toggle navigation menu" data-astro-cid-37fxchfa', '> <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" data-astro-cid-37fxchfa', '><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" data-astro-cid-37fxchfa', '></path></svg> </button> </div> <!-- Mobile menu --> <div id="mobile-menu" class="border-t border-kernel-800/60 bg-kernel-950/98 backdrop-blur-xl px-6 py-4" data-astro-cid-37fxchfa', "> <a", ' class="block py-2.5 text-sm text-kernel-300 hover:text-kernel-100 font-medium" data-astro-cid-37fxchfa', ">Domains</a> ", ' <div class="pt-2 border-t border-kernel-800/40 mt-2" data-astro-cid-37fxchfa', "> <a", ' class="block py-2.5 text-sm text-kernel-300 hover:text-kernel-100 font-medium" data-astro-cid-37fxchfa', '>About</a> <a href="https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS" target="_blank" rel="noopener" class="block py-2.5 text-sm text-kernel-400 hover:text-kernel-100" data-astro-cid-37fxchfa', '>GitHub</a> </div> </div> </nav> <!-- Main content --> <main id="main-content" class="max-w-7xl mx-auto px-6 main-px py-8 sm:py-12" role="main" data-astro-cid-37fxchfa', "> ", ' </main> <!-- Footer --> <footer class="border-t border-kernel-800/40 mt-32" role="contentinfo" data-astro-cid-37fxchfa', '> <div class="max-w-7xl mx-auto px-6 ftr-px py-10 sm:py-16" data-astro-cid-37fxchfa', '> <div class="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12" data-astro-cid-37fxchfa', '> <!-- Brand --> <div class="md:col-span-1" data-astro-cid-37fxchfa', '> <div class="text-lg font-bold text-kernel-100 mb-3" data-astro-cid-37fxchfa', '>GCD</div> <p class="text-sm text-kernel-500 leading-relaxed" data-astro-cid-37fxchfa', ">A single-axiom mathematical framework for measuring what survives collapse and what returns.</p> </div> <!-- Explore --> <div data-astro-cid-37fxchfa", '> <div class="text-xs uppercase tracking-widest text-kernel-600 font-medium mb-4" data-astro-cid-37fxchfa', '>Explore</div> <div class="space-y-2" data-astro-cid-37fxchfa', "> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Calculator</a> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Regime Diagram</a> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Precision</a> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Mapper</a> </div> </div> <!-- Theory --> <div data-astro-cid-37fxchfa", '> <div class="text-xs uppercase tracking-widest text-kernel-600 font-medium mb-4" data-astro-cid-37fxchfa', '>Theory</div> <div class="space-y-2" data-astro-cid-37fxchfa', "> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Mathematics</a> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Geometry</a> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Grammar</a> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">Papers</a> </div> </div> <!-- Project --> <div data-astro-cid-37fxchfa", '> <div class="text-xs uppercase tracking-widest text-kernel-600 font-medium mb-4" data-astro-cid-37fxchfa', '>Project</div> <div class="space-y-2" data-astro-cid-37fxchfa', "> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', ">About</a> <a", ' class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', '>Rosetta</a> <a href="https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS" target="_blank" rel="noopener" class="block text-sm text-kernel-400 hover:text-kernel-200 transition-colors" data-astro-cid-37fxchfa', '>GitHub</a> </div> </div> </div> <!-- Bottom bar --> <div class="border-t border-kernel-800/40 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4" data-astro-cid-37fxchfa', '> <p class="text-xs text-kernel-600 italic" data-astro-cid-37fxchfa', '>Collapsus generativus est; solum quod redit, reale est.</p> <p class="text-xs text-kernel-600" data-astro-cid-37fxchfa', ">UMCP v2.3.1</p> </div> </div> </footer> ", " </body> </html>"])), addAttribute($$definedVars, "style"), addAttribute(description, "content"), addAttribute(`${base}favicon.svg`, "href"), addAttribute(canonicalUrl, "href"), fullTitle, addAttribute(fullTitle, "content"), addAttribute(description, "content"), addAttribute(ogType, "content"), addAttribute(canonicalUrl, "content"), ogImage && renderTemplate`<meta property="og:image"${addAttribute(ogImage, "content")}>`, addAttribute(fullTitle, "content"), addAttribute(description, "content"), unescapeHTML(JSON.stringify({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Generative Collapse Dynamics",
    "alternateName": "GCD / UMCP",
    "url": siteUrl,
    "description": `A single-axiom mathematical framework for measuring what survives collapse and what returns. ${DOMAIN_COUNT} domain closures, ${THEOREM_COUNT} proven theorems, ${IDENTITY_COUNT} structural identities, ${LEMMA_COUNT} lemmas, ${CLOSURE_COUNT} closure modules, ${TEST_COUNT} automated tests.`,
    "version": "2.3.1",
    "publisher": {
      "@type": "Organization",
      "name": "GCD / UMCP"
    },
    "about": {
      "@type": "SoftwareSourceCode",
      "name": "UMCP",
      "description": "Universal Measurement Contract Protocol — single-axiom mathematical framework",
      "codeRepository": "https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS",
      "programmingLanguage": ["Python", "C", "C++", "TypeScript"],
      "runtimePlatform": "Python 3.11+",
      "softwareVersion": "2.3.1",
      "license": "https://opensource.org/licenses/MIT"
    }
  })), renderHead(), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute(base, "href"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute(base, "href"), addAttribute($$definedVars, "style"), navGroups.map((group) => renderTemplate`<div class="nav-group" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}> <button class="text-sm text-kernel-400 hover:text-kernel-100 transition-colors px-3 py-2 rounded-lg hover:bg-kernel-800/50 flex items-center gap-1 cursor-pointer" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}> ${group.label} <svg class="w-3 h-3 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}></path></svg> </button> <div class="nav-dropdown" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}> <div class="nav-dropdown-inner" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}> ${group.items.map((item) => renderTemplate`<a${addAttribute(item.href, "href")} class="block px-4 py-2 text-sm text-kernel-400 hover:text-kernel-100 hover:bg-kernel-800/50 transition-colors" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}> ${item.name} </a>`)} </div> </div> </div>`), addAttribute(`${base}gcd-cai/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}about/`, "href"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute(base, "href"), addAttribute($$definedVars, "style"), navGroups.map((group) => renderTemplate`<div class="py-2" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}> <div class="text-[10px] uppercase tracking-widest text-kernel-600 font-medium mb-1" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}>${group.label}</div> ${group.items.map((item) => renderTemplate`<a${addAttribute(item.href, "href")} class="block py-1.5 pl-3 text-sm text-kernel-400 hover:text-kernel-100 transition-colors" data-astro-cid-37fxchfa${addAttribute($$definedVars, "style")}>${item.name}</a>`)} </div>`), addAttribute($$definedVars, "style"), addAttribute(`${base}about/`, "href"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), renderSlot($$result, $$slots["default"]), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute(`${base}calculator/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}regime/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}precision/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}mapper/`, "href"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute(`${base}mathematics/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}geometry/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}grammar/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}papers/`, "href"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute(`${base}about/`, "href"), addAttribute($$definedVars, "style"), addAttribute(`${base}rosetta/`, "href"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), addAttribute($$definedVars, "style"), renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/BaseLayout.astro?astro&type=script&index=0&lang.ts"));
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/BaseLayout.astro", void 0);

export { $$BaseLayout as $, AT_A_GLANCE as A, CLOSURE_COUNT as C, DOMAIN_COUNT as D, IDENTITY_COUNT as I, LEMMA_COUNT as L, TEST_COUNT as T, THEOREM_COUNT as a, TEST_FILE_COUNT as b };
