import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { m as maybeRenderHead, r as renderTemplate, b as renderComponent, a as addAttribute } from './server_DjVGnHP9.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';
import 'clsx';
import { r as renderScript } from './script_CjXWaIL1.mjs';

const $$DiachronicTimeline = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$DiachronicTimeline;
  return renderTemplate`${maybeRenderHead()}<div id="diachronic-timeline" class="space-y-8"> <!-- ═══ Header ═══ --> <div class="bg-kernel-900 border border-kernel-700 rounded-xl p-6"> <div class="flex items-start justify-between flex-wrap gap-4"> <div> <h2 class="text-xl font-bold text-kernel-100 mb-1">Diachronic Timeline</h2> <p class="text-kernel-400 text-sm max-w-xl">
Append-only history of collapse-return cycles. Every row is permanent —
          corrections cross a <strong class="text-kernel-200">Weld</strong>, never an overwrite.
</p> <p class="text-xs italic text-kernel-600 mt-2">
Historia numquam rescribitur; sutura tantum additur.
</p> </div> <div class="flex items-center gap-3 text-xs"> <div class="text-center px-3 py-2 bg-kernel-800 rounded-lg"> <div class="text-lg font-bold text-amber-400" id="tl-total-entries">10,023</div> <div class="text-kernel-500">Ledger Rows</div> </div> <div class="text-center px-3 py-2 bg-kernel-800 rounded-lg"> <div class="text-lg font-bold text-blue-400" id="tl-total-welds">29</div> <div class="text-kernel-500">Versions</div> </div> <div class="text-center px-3 py-2 bg-kernel-800 rounded-lg"> <div class="text-lg font-bold text-green-400" id="tl-elapsed-days">68</div> <div class="text-kernel-500">Days</div> </div> </div> </div> </div> <!-- ═══ Layer toggles ═══ --> <div class="flex flex-wrap gap-2"> <button data-layer="ledger" class="tl-layer-btn active px-3 py-1.5 bg-amber-900/40 border border-amber-700 text-amber-400 rounded-lg text-xs font-medium transition hover:border-amber-500">
◉ Ledger Stream
</button> <button data-layer="welds" class="tl-layer-btn active px-3 py-1.5 bg-blue-900/40 border border-blue-700 text-blue-400 rounded-lg text-xs font-medium transition hover:border-blue-500">
⊕ Weld Events
</button> <button data-layer="versions" class="tl-layer-btn active px-3 py-1.5 bg-purple-900/40 border border-purple-700 text-purple-400 rounded-lg text-xs font-medium transition hover:border-purple-500">
◈ Version Milestones
</button> <button data-layer="freezes" class="tl-layer-btn active px-3 py-1.5 bg-cyan-900/40 border border-cyan-700 text-cyan-400 rounded-lg text-xs font-medium transition hover:border-cyan-500">
❄ Freeze Points
</button> <button data-layer="epistemic" class="tl-layer-btn active px-3 py-1.5 bg-green-900/40 border border-green-700 text-green-400 rounded-lg text-xs font-medium transition hover:border-green-500">
⊙ Epistemic Verdicts
</button> </div> <!-- ═══ Main Canvas ═══ --> <div class="bg-kernel-900 border border-kernel-700 rounded-xl p-4 relative"> <div class="flex items-center justify-between mb-3"> <h3 class="text-sm font-bold text-kernel-300">Integrity Over Time</h3> <div class="flex gap-2 text-xs"> <button id="tl-zoom-in" class="px-2 py-1 bg-kernel-800 text-kernel-400 rounded hover:bg-kernel-700 transition">+</button> <button id="tl-zoom-out" class="px-2 py-1 bg-kernel-800 text-kernel-400 rounded hover:bg-kernel-700 transition">−</button> <button id="tl-zoom-fit" class="px-2 py-1 bg-kernel-800 text-kernel-400 rounded hover:bg-kernel-700 transition">Fit</button> </div> </div> <div class="relative"> <canvas id="tl-canvas" class="w-full rounded" style="height: 320px; cursor: crosshair;"></canvas> <div id="tl-tooltip" class="hidden absolute pointer-events-none text-xs bg-kernel-950/95 border border-kernel-600 rounded-lg px-3 py-2 text-kernel-200 font-mono shadow-xl z-20 max-w-xs"></div> </div> <!-- Legend --> <div class="flex flex-wrap gap-4 mt-3 text-[10px] text-kernel-500"> <div class="flex items-center gap-1"><span class="w-3 h-0.5 bg-amber-400 inline-block rounded"></span> F (Fidelity)</div> <div class="flex items-center gap-1"><span class="w-3 h-0.5 bg-green-400 inline-block rounded"></span> IC (Integrity)</div> <div class="flex items-center gap-1"><span class="w-3 h-0.5 bg-red-400 inline-block rounded"></span> ω (Drift)</div> <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-blue-500 inline-block rounded-full"></span> Weld</div> <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 border border-purple-400 inline-block rounded-sm"></span> Version</div> <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 border border-cyan-400 inline-block rounded-full"></span> Freeze</div> </div> </div> <!-- ═══ Version Lineage (Append-Only Timeline) ═══ --> <div class="bg-kernel-900 border border-kernel-700 rounded-xl p-5"> <h3 class="text-sm font-bold text-kernel-300 uppercase tracking-wider mb-4">
Append-Only Version Lineage
</h3> <p class="text-xs text-kernel-500 mb-4">
Each version is a structural snapshot — never rewritten.
      Click any milestone to see what was welded.
</p> <div id="tl-version-timeline" class="relative"> <!-- Populated by script --> </div> </div> <!-- ═══ Weld Registry ═══ --> <div class="bg-kernel-900 border border-kernel-700 rounded-xl p-5"> <h3 class="text-sm font-bold text-kernel-300 uppercase tracking-wider mb-4">
Weld Registry
</h3> <p class="text-xs text-kernel-500 mb-4">
Verified seam closures with IC before and after. A weld that passes (|Δκ| ≤ tol_seam) proves
      continuity across the change.
</p> <div id="tl-weld-registry" class="space-y-3"> <!-- Populated by script --> </div> </div> <!-- ═══ Epistemic Classification ═══ --> <div class="bg-kernel-900 border border-kernel-700 rounded-xl p-5"> <h3 class="text-sm font-bold text-kernel-300 uppercase tracking-wider mb-4">
Epistemic Trichotomy
</h3> <p class="text-xs text-kernel-500 mb-4">
Every emission is classified: <strong class="text-green-400">Return</strong> (seam closed),
<strong class="text-kernel-400">Gesture</strong> (emission exists but seam didn't close),
      or <strong class="text-red-400">Dissolution</strong> (ω ≥ 0.30).
</p> <div class="grid grid-cols-1 md:grid-cols-3 gap-3" id="tl-epistemic-cards"> <!-- Populated by script --> </div> </div> <!-- ═══ Freeze Archive ═══ --> <div class="bg-kernel-900 border border-kernel-700 rounded-xl p-5"> <h3 class="text-sm font-bold text-kernel-300 uppercase tracking-wider mb-4">
Freeze Points — Trans Suturam Congelatum
</h3> <p class="text-xs text-kernel-500 mb-4">
Frozen contract snapshots with SHA-256 hashes.
      Same rules on both sides of every collapse-return boundary.
</p> <div id="tl-freeze-archive" class="space-y-3"> <!-- Populated by script --> </div> </div> <!-- ═══ Continuity Principle ═══ --> <div class="bg-kernel-900/50 border border-kernel-800 rounded-xl p-5 text-center"> <p class="text-kernel-500 text-sm italic">
"History is never rewritten; only a weld is added."
</p> <p class="text-kernel-600 text-xs mt-1">
Historia numquam rescribitur; sutura tantum additur.
</p> <div class="flex justify-center gap-6 mt-4 text-xs text-kernel-400"> <div><span class="text-amber-400 font-bold">10,023</span> ledger rows</div> <div><span class="text-blue-400 font-bold">29</span> versions</div> <div><span class="text-green-400 font-bold">100%</span> CONFORMANT</div> <div><span class="text-cyan-400 font-bold">0</span> rewrites</div> </div> </div> </div> ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/components/DiachronicTimeline.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/components/DiachronicTimeline.astro", void 0);

const $$Continuity = createComponent(($$result, $$props, $$slots) => {
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  const sections = ["principle", "timeline", "lineage", "welds", "epistemic", "freezes"];
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Diachronic Continuity — GCD", "description": "Append-only history of collapse-return cycles. Weld lineage, freeze points, epistemic verdicts, and the full integrity ledger timeline." }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-6xl mx-auto"> <!-- ═══════════ HERO ═══════════ --> <div class="mb-8"> <h1 class="text-3xl font-bold text-kernel-100 mb-2">Diachronic Continuity</h1> <p class="text-kernel-400 text-lg italic">Historia numquam rescribitur; sutura tantum additur.</p> <p class="text-kernel-500 text-sm mt-2 max-w-3xl">
History is never rewritten; only a weld is added. This page visualizes the
        append-only audit trail — every version, weld, freeze, and epistemic verdict
        that constitutes the project's return domain D<sub>θ</sub>.
</p> </div> <!-- ═══════════ NAV ═══════════ --> <nav class="mb-8 flex flex-wrap gap-2"> ${sections.map((s) => renderTemplate`<a${addAttribute(`#${s}`, "href")} class="px-3 py-1.5 rounded-full text-xs font-medium
          bg-kernel-800/60 text-kernel-400 hover:text-kernel-200 hover:bg-kernel-700/60
          border border-kernel-700/40 transition no-underline"> ${s === "principle" ? "Continuity Principle" : s === "timeline" ? "Integrity Timeline" : s === "lineage" ? "Version Lineage" : s === "welds" ? "Weld Registry" : s === "epistemic" ? "Epistemic Trichotomy" : s === "freezes" ? "Freeze Points" : s.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())} </a>`)} </nav> <!-- ═══════════ §1: CONTINUITY PRINCIPLE ═══════════ --> <section id="principle" class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">The Continuity Constraint</h2> <div class="grid grid-cols-1 md:grid-cols-2 gap-4"> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <h3 class="text-sm font-bold text-amber-400 mb-3">Append-Only Ledger</h3> <p class="text-xs text-kernel-400 leading-relaxed mb-3">
Every validation run, weld event, and freeze point is <strong class="text-kernel-200">permanent</strong>.
            Prior exchanges, ledger rows, and validation results are never edited in place.
            They form the return domain D<sub>θ</sub> that gives the present its context.
</p> <div class="flex items-center gap-3 text-xs text-kernel-500"> <span class="text-amber-400 font-mono font-bold">10,023</span> ledger rows
<span class="text-kernel-700">·</span> <span class="text-purple-400 font-mono font-bold">29</span> versions
<span class="text-kernel-700">·</span> <span class="text-green-400 font-mono font-bold">0</span> rewrites
</div> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <h3 class="text-sm font-bold text-blue-400 mb-3">Corrections Cross a Weld</h3> <p class="text-xs text-kernel-400 leading-relaxed mb-3">
If a prior claim, threshold, or policy must change, the change is a named
<strong class="text-kernel-200">Weld</strong> at a shared anchor — not an overwrite.
            The Weld runs pre/post tests, enforces κ-continuity (residual ≤ tol), and records
            what changed and why.
</p> <p class="text-xs text-kernel-400 leading-relaxed">
Errata are <strong class="text-kernel-200">first-class</strong>: not failures, but
            Errata Welds that preserve the full audit trail.
</p> </div> </div> <!-- The Five Stops of Continuity --> <div class="mt-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <h3 class="text-sm font-bold text-kernel-300 mb-3">The Spine Governs History</h3> <div class="flex items-center gap-2 text-xs font-mono text-kernel-500 overflow-x-auto pb-2"> <div class="bg-kernel-800 rounded px-3 py-2 text-center min-w-[100px]"> <div class="text-cyan-400 font-bold">CONTRACT</div> <div class="text-[10px] text-kernel-600">freeze before evidence</div> </div> <span class="text-kernel-700">→</span> <div class="bg-kernel-800 rounded px-3 py-2 text-center min-w-[100px]"> <div class="text-amber-400 font-bold">CANON</div> <div class="text-[10px] text-kernel-600">narrate with 5 words</div> </div> <span class="text-kernel-700">→</span> <div class="bg-kernel-800 rounded px-3 py-2 text-center min-w-[100px]"> <div class="text-purple-400 font-bold">CLOSURES</div> <div class="text-[10px] text-kernel-600">publish thresholds</div> </div> <span class="text-kernel-700">→</span> <div class="bg-kernel-800 rounded px-3 py-2 text-center min-w-[100px]"> <div class="text-green-400 font-bold">LEDGER</div> <div class="text-[10px] text-kernel-600">debit / credit</div> </div> <span class="text-kernel-700">→</span> <div class="bg-kernel-800 rounded px-3 py-2 text-center min-w-[100px]"> <div class="text-red-400 font-bold">STANCE</div> <div class="text-[10px] text-kernel-600">derive verdict</div> </div> </div> <p class="text-[10px] text-kernel-600 mt-2 italic">
Each stop is a permanent entry in the audit trail. History passes through all five.
</p> </div> <!-- Governance mechanisms --> <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4"> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <h3 class="text-sm font-bold text-cyan-400 mb-2">Manifest <span class="text-kernel-600 font-normal">manifestum</span></h3> <p class="text-xs text-kernel-400 leading-relaxed">
Provenance — binds artifacts to time, tools, checksums.
            Every claim carries its receipt. SHA-256 hashes anchor
            each freeze point immutably.
</p> </div> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <h3 class="text-sm font-bold text-blue-400 mb-2">Weld <span class="text-kernel-600 font-normal">sutura</span></h3> <p class="text-xs text-kernel-400 leading-relaxed">
Continuity across change — the <em>only</em> legitimate way to change policy.
            Names an anchor, runs pre/post tests, enforces κ-continuity.
            History is append-only and welded, never rewritten.
</p> </div> </div> </section> <!-- ═══════════ §2: TIMELINE (Interactive Canvas) ═══════════ --> <section id="timeline" class="mb-10"> ${renderComponent($$result2, "DiachronicTimeline", $$DiachronicTimeline, {})} </section> <!-- ═══════════ CROSS-LINKS ═══════════ --> <section class="mb-10"> <h2 class="text-xl font-bold text-kernel-100 mb-4">Related Pages</h2> <div class="grid grid-cols-2 md:grid-cols-4 gap-3"> ${[
    { name: "Ledger", href: `${base}ledger/`, desc: "Domain integrity audit", icon: "◉" },
    { name: "Episteme", href: `${base}epistemology/`, desc: "Epistemic weld theory", icon: "⊙" },
    { name: "Grammar", href: `${base}grammar/`, desc: "The five-stop spine", icon: "⌘" },
    { name: "Seam Budget", href: `${base}seam-budget/`, desc: "Γ(ω), D_C, Δκ", icon: "△" }
  ].map((link) => renderTemplate`<a${addAttribute(link.href, "href")} class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4 hover:border-kernel-600 hover:bg-kernel-900/80 transition group no-underline"> <div class="text-xl mb-1">${link.icon}</div> <div class="text-sm font-bold text-kernel-100 group-hover:text-amber-400 transition">${link.name}</div> <div class="text-xs text-kernel-500">${link.desc}</div> </a>`)} </div> </section> <!-- ═══════════ FOOTER ═══════════ --> <div class="text-center text-kernel-600 text-xs pb-8"> <p>UMCP v2.3.1 · MIT License</p> <p class="mt-1 italic">Continuitas non narratur: mensuratur.</p> </div> </div> ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/continuity.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/continuity.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/continuity";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Continuity,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
