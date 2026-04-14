import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, a as addAttribute } from './server_DjVGnHP9.mjs';
import { r as renderScript } from './script_CjXWaIL1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$LiberCollapsus = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$LiberCollapsus;
  const base = "/GENERATIVE-COLLAPSE-DYNAMICS/";
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "Deep Reading — Liber Collapsus", "description": "Interactive deep reading of Liber Universalis de Collapsus Mathematica with live verification" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="max-w-4xl mx-auto"> <!-- ═══ Hero ═══ --> <div class="text-center py-16 md:py-24 relative"> <p class="text-xs uppercase tracking-[0.3em] text-kernel-500 mb-4">Deep Reading</p> <h1 class="text-3xl md:text-5xl font-bold text-kernel-100 mb-3 leading-[1.1] tracking-tight font-serif italic">
Liber Universalis<br>de Collapsus Mathematica
</h1> <p class="text-sm text-kernel-500 mb-2">Clement Paulus · 11 October 2025</p> <p class="text-xs text-kernel-600 max-w-lg mx-auto mb-8">
An interactive reading of the foundational Latin treatise. Each section pairs the original text
        with English translation, contextual commentary, and live verification tools.
</p> <div class="inline-flex gap-3"> <a href="#prooemium" class="bg-amber-500 hover:bg-amber-400 text-kernel-950 px-5 py-2.5 rounded-lg text-sm font-semibold transition shadow-lg shadow-amber-500/20">
Begin Reading &darr;
</a> <a${addAttribute(`${base}calculator/`, "href")} class="bg-kernel-800/80 hover:bg-kernel-700 border border-kernel-700/50 text-kernel-200 px-5 py-2.5 rounded-lg text-sm font-medium transition">
Open Calculator &rarr;
</a> </div> </div> <!-- ═══ Table of Contents ═══ --> <nav class="mb-16 bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-6"> <p class="text-xs tracking-[0.2em] uppercase text-kernel-600 mb-4">Capita</p> <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm"> <a href="#prooemium" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">—</span> <span>Prooemium <span class="text-kernel-600 text-xs ml-1">Prologue</span></span> </a> <a href="#caput-1" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">I</span> <span>De Axiomate Paradoxali <span class="text-kernel-600 text-xs ml-1">The Paradoxical Axiom</span></span> </a> <a href="#caput-2" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">II</span> <span>De Invariantibus <span class="text-kernel-600 text-xs ml-1">The Invariants &amp; Universal Kernel</span></span> </a> <a href="#caput-3" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">III</span> <span>De Memoria Viva <span class="text-kernel-600 text-xs ml-1">Living Memory &amp; Perpetual Audit</span></span> </a> <a href="#caput-4" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">IV</span> <span>De Paradoxo <span class="text-kernel-600 text-xs ml-1">Paradox, Rupture &amp; Repair</span></span> </a> <a href="#caput-5" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">V</span> <span>De Regiminibus <span class="text-kernel-600 text-xs ml-1">Regimes &amp; Thresholds</span></span> </a> <a href="#caput-6" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">VI</span> <span>De Ethica Operativa <span class="text-kernel-600 text-xs ml-1">Operative Ethics</span></span> </a> <a href="#caput-7" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">VII</span> <span>Exempla <span class="text-kernel-600 text-xs ml-1">Universal Applications</span></span> </a> <a href="#caput-8" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">VIII</span> <span>De Innovatione <span class="text-kernel-600 text-xs ml-1">Continuous Innovation</span></span> </a> <a href="#conclusio" class="toc-link flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-kernel-800/60 transition text-kernel-300 hover:text-kernel-100 no-underline"> <span class="text-xs font-mono text-kernel-600 w-6 text-right">—</span> <span>Conclusio <span class="text-kernel-600 text-xs ml-1">Conclusion</span></span> </a> </div> </nav> <!-- ════════════════════════════════════════════════ --> <!--  PROOEMIUM                                      --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="prooemium"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Prooemium</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <!-- Latin original --> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Nihil stabile est nisi quod per casum iteratur atque regeneratur in formam propriam redintegratam.
          Omne quod in veritate participat, per dissolutionem, auditum universalem, memoriam viventem,
          reparationem atque recursionem transit. Non in immobilitate perpetua, sed in motu, lapsu, ac
          reditu substantia vera et ipsa veritas revelantur. Haec est radix et fundamentum collapsus
          mathematicae: non ad abstractionem otiosam, sed ad operationem viventem, auditum universalem,
          et regenerationem apertam omnia referuntur.
</blockquote> <!-- Translation --> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
Nothing is stable unless it is iterated through collapse and regenerated into its own restored form.
            Everything that participates in truth passes through dissolution, universal hearing, living memory,
            repair, and recursion. Not in perpetual immobility, but in motion, fall, and return are true substance
            and truth itself revealed. This is the root and foundation of collapse mathematics: everything refers not
            to idle abstraction, but to living operation, universal hearing, and open regeneration.
</p> </div> <!-- Commentary --> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed">
The prologue establishes the central thesis immediately: stability is not a static property but an
            emergent feature of dynamic return. The five key operations are named in sequence — <em>dissolution</em>
(collapse), <em>hearing</em> (audit), <em>living memory</em> (ledger), <em>repair</em> (return),
            and <em>recursion</em> (iteration). These correspond directly to the five stops of the Spine:
            Contract → Canon → Closures → Integrity Ledger → Stance. The prologue also insists on
<em>operationem viventem</em> — living operation — distinguishing GCD from static mathematical
            frameworks. The mathematics must <em>do</em> something; it is not ornamental.
</p> </div> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT I                                        --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-1"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput I · The Paradoxical Axiom</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
In ipso fundamento, paradoxum ponimus: collapsus generativus est; solum quod per casum transiit
          et iterum redit, reale est. Hac lege universali, non tantum materia, sed etiam ratio, memoria,
          historia comprehenduntur. Ordo ex ruina oritur, structura ex resolutione, identitas ex oblivione
          et restitutione.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
At the very foundation, we place a paradox: collapse is generative; only what has passed through
            fall and returns again is real. Under this universal law, not only matter but also reason, memory,
            and history are comprehended. Order arises from ruin, structure from dissolution, identity from
            oblivion and restoration.
</p> </div> <!-- Interactive: Axiom-0 verification --> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed mb-4">
This is <strong class="text-kernel-200">Axiom-0</strong> — the single axiom from which the entire system derives.
            The Latin captures something the English misses: <em>casum</em> means simultaneously "fall," "case" (to examine),
            and "occasion" (for generation). The triple meaning is not accidental — collapse is all three at once.
</p> <p class="text-kernel-400 text-sm leading-relaxed">
The final sentence — <em>ordo ex ruina</em> — is not metaphorical. When we compute the kernel on a trace
            vector that has undergone collapse (channels near 0), the regime classification "Collapse" is where
<strong class="text-kernel-200">63.1%</strong> of the Fisher manifold lives. Stability (12.5%) is the rare exception.
            The axiom tells us this is not a failure state — it is the generative condition.
</p> </div> <!-- Live tool link --> <div class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl"> <span class="text-amber-400 text-lg">⊕</span> <div class="flex-1"> <p class="text-sm text-kernel-200 font-medium">Try it: Compute the kernel on a collapsed trace</p> <p class="text-xs text-kernel-500">Set channels near 0 and watch how the regime classifies — stability is structurally rare</p> </div> <a${addAttribute(`${base}calculator/`, "href")} class="text-xs text-amber-400 hover:text-amber-300 transition font-medium whitespace-nowrap">
Open Calculator &rarr;
</a> </div> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT II                                       --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-2"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput II · The Invariants &amp; Universal Kernel</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Quicumque numerus, ordo, aut notio ad rem pertinere vult, probationem collapsus subire debet.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
Whatever number, order, or concept wishes to pertain to reality must undergo the test of collapse.
</p> </div> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed">
This is the <strong class="text-kernel-200">universality claim</strong>: the kernel is not domain-specific.
            Any measurable system can be embedded as a trace vector. The "test of collapse" is computation through the
            kernel function K: [0,1]<sup>n</sup> × Δ<sup>n</sup> → (F, ω, S, C, κ, IC).
</p> </div> <!-- The Trace Vector --> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-3">The Trace Vector</p> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed mb-4 text-sm">
Sit tractus delimitatus Ψ(t) = (c₁(t), c₂(t), …, cₙ(t)), cᵢ(t) ∈ [0,1], wᵢ ≥ 0, Σwᵢ = 1.
</blockquote> <p class="text-kernel-400 text-sm leading-relaxed">
Every system is encoded as a bounded trace vector — n channels, each in [0,1], with simplex weights.
            The boundedness [0,1] is not a limitation — it is the <em>embedding</em>. Raw measurements are normalized
            into this domain by the Tier-0 protocol. The weights w form a probability simplex (they sum to 1),
            ensuring the kernel outputs are scale-invariant.
</p> </div> <!-- Guard Band --> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-3">The Guard Band (ε)</p> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed mb-4 text-sm">
Munus praecipuum guard-bandi ε est fines custodire, ne singularitas logarithmica oriatur.
            Hic ε non arbitrium est, sed trans suturam congelatum.
</blockquote> <p class="text-kernel-400 text-sm leading-relaxed mb-3">
"The chief function of the guard band ε is to guard the boundaries, lest a logarithmic singularity
            arise. This ε is not arbitrary, but frozen across the seam."
</p> <p class="text-kernel-400 text-sm leading-relaxed">
The clamped coordinate c<sub>i,ε</sub> = min(1−ε, max(ε, cᵢ)) prevents ln(0) in the κ computation.
            The frozen value <span class="font-mono text-amber-400">ε = 10⁻⁸</span> is not chosen by convention
            — it is the unique value where the pole at ω = 1 does not affect measurements to machine precision.
</p> </div> <!-- The Six Invariants — interactive cards --> <div> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-4">The Six Invariants</p> <div class="space-y-4" id="invariant-sections"> <!-- Populated by script --> </div> </div> <!-- Live verification panel --> <div class="bg-gradient-to-b from-amber-500/5 to-transparent border border-amber-500/20 rounded-xl p-5" id="verify-panel"> <div class="flex items-center gap-2 mb-4"> <span class="text-amber-400">⚡</span> <p class="text-xs text-amber-400 uppercase tracking-wider font-bold">Live Verification</p> </div> <p class="text-kernel-400 text-xs mb-4">
Enter a trace vector and verify the three identities from Caput II in real time.
</p> <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"> <div> <label class="text-xs text-kernel-500 block mb-1">Channels (comma-separated, 0–1)</label> <input type="text" id="verify-channels" value="0.95, 0.80, 0.60, 0.30" class="w-full bg-kernel-950 border border-kernel-700 rounded-lg px-3 py-2 text-sm text-kernel-200 font-mono focus:border-amber-500 focus:outline-none transition"> </div> <div> <label class="text-xs text-kernel-500 block mb-1">Weights (equal if empty)</label> <input type="text" id="verify-weights" value="" class="w-full bg-kernel-950 border border-kernel-700 rounded-lg px-3 py-2 text-sm text-kernel-200 font-mono focus:border-amber-500 focus:outline-none transition"> </div> </div> <button id="verify-btn" class="bg-amber-500 hover:bg-amber-400 text-kernel-950 px-5 py-2 rounded-lg text-sm font-semibold transition mb-4">
Compute &amp; Verify
</button> <!-- Results --> <div id="verify-results" class="hidden space-y-3"> <div class="grid grid-cols-3 md:grid-cols-6 gap-2" id="invariant-outputs"></div> <div class="space-y-2 mt-4" id="identity-checks"></div> </div> </div> <!-- Tool links for Caput II --> <div class="grid grid-cols-1 md:grid-cols-2 gap-3"> <a${addAttribute(`${base}calculator/`, "href")} class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl hover:border-kernel-600 transition no-underline group"> <span class="text-amber-400 text-lg">⊕</span> <div> <p class="text-sm text-kernel-200 font-medium group-hover:text-amber-400 transition">Structure Explorer</p> <p class="text-xs text-kernel-500">Full kernel computation with 9 analysis modes</p> </div> </a> <a${addAttribute(`${base}identities/`, "href")} class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl hover:border-kernel-600 transition no-underline group"> <span class="text-cyan-400 text-lg">≡</span> <div> <p class="text-sm text-kernel-200 font-medium group-hover:text-cyan-400 transition">44 Structural Identities</p> <p class="text-xs text-kernel-500">All provable properties of the kernel function</p> </div> </a> </div> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT III                                      --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-3"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput III · Living Memory &amp; Perpetual Audit</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Memoria non est simplex recordatio, sed structura perpetua regiminis, auditus vivus et operativus.
          In archivis memoriae non tantum res gestae, sed etiam silentia, defectus, omissiones, hiatus
          diligenter conservari debent. Nihil in memoria perit; omnia prompta ad recursionem, reparationem
          et innovationem manent. Auditus est radix veritatis; memoria viva est thesaurus realitatis.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
Memory is not simple recollection, but a perpetual structure of governance, living and operative hearing.
            In the archives of memory, not only deeds but also silences, defects, omissions, and gaps must be
            diligently preserved. Nothing perishes in memory; everything remains ready for recursion, repair,
            and innovation. Hearing is the root of truth; living memory is the treasury of reality.
</p> </div> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed mb-3">
This chapter formalizes the <strong class="text-kernel-200">Integrity Ledger</strong> — the fourth stop of the Spine.
            The key insight is that the ledger preserves <em>everything</em>, including failures and gaps (silentia, defectus, omissiones).
            This maps directly to the append-only data model: <em>Historia numquam rescribitur; sutura tantum additur.</em> </p> <p class="text-kernel-400 text-sm leading-relaxed">
The word <em>auditus</em> (hearing) is not metaphorical. Validation <em>is</em> listening. The ledger hears
            every claim, every debit, every credit. That hearing is the audit. The Latin makes this identity visible:
            auditus = audit = hearing. One word, one operation.
</p> </div> <a${addAttribute(`${base}ledger/`, "href")} class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl hover:border-kernel-600 transition no-underline group"> <span class="text-green-400 text-lg">⧖</span> <div> <p class="text-sm text-kernel-200 font-medium group-hover:text-green-400 transition">Integrity Ledger</p> <p class="text-xs text-kernel-500">See the living audit trail — append-only, hash-chained, never rewritten</p> </div> </a> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT IV                                       --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-4"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput IV · Paradox, Rupture &amp; Repair</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Paradoxum colendum est, non solvitur. In lapsu incipit regeneratio; in defectu, occasio
          reparationis; in silentio, vocatio ad auditum emergit. Ruptura est fons constantiae.
          Per defectum integritas roboratur; omnis lapsus novum iter ad claritatem et praesentiam parit.
          Qui collapsum intueri et iterare audet, novam vitam et ordinem reperiet.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
The paradox is to be cultivated, not solved. In the fall, regeneration begins; in the defect, the occasion
            for repair; in the silence, the call to hearing emerges. Rupture is the source of constancy.
            Through defect, integrity is strengthened; every fall gives birth to a new path toward clarity and
            presence. Whoever dares to observe collapse and iterate will find new life and order.
</p> </div> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed mb-3"> <em>"Ruptura est fons constantiae"</em> — rupture is the source of constancy. This is not rhetoric;
            it is structural. The regime classification shows that <strong class="text-kernel-200">63.1%</strong>
of the Fisher manifold is in the Collapse regime. The system <em>lives</em> in collapse. Return
            from collapse to stability — the axiom's core operation — is what creates constancy.
</p> <p class="text-kernel-400 text-sm leading-relaxed"> <em>"Paradoxum colendum est, non solvitur."</em> The paradox is cultivated, not resolved. This governs
            how the system handles contradictions: they are not bugs to fix but structural signals to audit. The
            third verdict — <strong class="text-kernel-200">NON_EVALUABLE</strong> — exists precisely for this.
            When a paradox appears, the system does not force a binary answer. It declares the third state.
</p> </div> <!-- Interactive: Geometric Slaughter demo --> <div class="bg-gradient-to-b from-red-500/5 to-transparent border border-red-500/20 rounded-xl p-5"> <div class="flex items-center gap-2 mb-3"> <span class="text-red-400">◎</span> <p class="text-xs text-red-400/80 uppercase tracking-wider font-bold">Live Demo: Ruptura est fons constantiae</p> </div> <p class="text-kernel-400 text-xs mb-4">
Watch one dead channel destroy IC while F stays healthy — this is "geometric slaughter."
            The rupture <em>is</em> the source of constancy because it reveals what the arithmetic mean F cannot see.
</p> <div class="grid grid-cols-2 gap-3 mb-3"> <div> <label class="text-xs text-kernel-500 block mb-1">Number of channels</label> <input type="range" id="slaughter-n" min="2" max="12" value="8" class="w-full accent-red-400"> <span class="text-xs text-kernel-500 font-mono" id="slaughter-n-label">8 channels</span> </div> <div> <label class="text-xs text-kernel-500 block mb-1">Dead channel value</label> <input type="range" id="slaughter-dead" min="0" max="100" value="1" class="w-full accent-red-400"> <span class="text-xs text-kernel-500 font-mono" id="slaughter-dead-label">0.01</span> </div> </div> <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center" id="slaughter-results"> <div class="bg-kernel-950/80 rounded-lg p-3"> <div class="text-xs text-kernel-500">F</div> <div class="text-lg font-bold font-mono text-kernel-200" id="sl-F">—</div> </div> <div class="bg-kernel-950/80 rounded-lg p-3"> <div class="text-xs text-kernel-500">IC</div> <div class="text-lg font-bold font-mono text-kernel-200" id="sl-IC">—</div> </div> <div class="bg-kernel-950/80 rounded-lg p-3"> <div class="text-xs text-kernel-500">Δ = F − IC</div> <div class="text-lg font-bold font-mono text-amber-400" id="sl-gap">—</div> </div> <div class="bg-kernel-950/80 rounded-lg p-3"> <div class="text-xs text-kernel-500">IC/F</div> <div class="text-lg font-bold font-mono text-red-400" id="sl-ratio">—</div> </div> </div> <p class="text-[10px] text-kernel-600 mt-2 italic">
All other channels are 1.0 (perfect). One channel near 0 kills IC because IC is a geometric mean — it cannot
            hide a dead channel the way the arithmetic mean F can.
</p> </div> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT V                                        --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-5"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput V · Regimes &amp; Thresholds</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Regimina collapsus sunt tria, per quattuor portas coniunctivas determinata.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
The regimes of collapse are three, determined by four conjunctive gates.
</p> </div> <!-- The three regimes with exact thresholds --> <div class="grid grid-cols-1 md:grid-cols-3 gap-3"> <div class="bg-kernel-900/50 border-l-4 border-green-500 rounded-r-xl p-4"> <div class="flex items-center justify-between mb-2"> <span class="text-green-400 font-bold">Stabile</span> <span class="text-xs text-green-400/60 font-mono">12.5%</span> </div> <div class="text-xs text-kernel-400 font-mono space-y-0.5"> <div>ω &lt; 0.038</div> <div>F &gt; 0.90</div> <div>S &lt; 0.15</div> <div>C &lt; 0.14</div> </div> <p class="text-[10px] text-kernel-600 mt-2">All four gates must be satisfied (conjunctive)</p> </div> <div class="bg-kernel-900/50 border-l-4 border-yellow-500 rounded-r-xl p-4"> <div class="flex items-center justify-between mb-2"> <span class="text-yellow-400 font-bold">Observandum</span> <span class="text-xs text-yellow-400/60 font-mono">24.4%</span> </div> <div class="text-xs text-kernel-400 font-mono">
Neither Stable nor Collapse
</div> <p class="text-[10px] text-kernel-600 mt-2">Intermediate — at least one Stable gate fails</p> </div> <div class="bg-kernel-900/50 border-l-4 border-red-500 rounded-r-xl p-4"> <div class="flex items-center justify-between mb-2"> <span class="text-red-400 font-bold">Collapsus</span> <span class="text-xs text-red-400/60 font-mono">63.1%</span> </div> <div class="text-xs text-kernel-400 font-mono">
ω ≥ 0.30
</div> <p class="text-[10px] text-kernel-600 mt-2">The dominant regime — collapse is the norm</p> </div> </div> <!-- The Fisher partition bar --> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-4"> <p class="text-xs text-kernel-500 mb-2 uppercase tracking-wider">Fisher Space Partition</p> <div class="h-8 rounded-full overflow-hidden flex"> <div class="bg-green-600 flex items-center justify-center text-xs text-white font-bold" style="width:12.5%">12.5%</div> <div class="bg-yellow-600 flex items-center justify-center text-xs text-white font-bold" style="width:24.4%">24.4%</div> <div class="bg-red-600 flex items-center justify-center text-xs text-white font-bold" style="width:63.1%">63.1%</div> </div> </div> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Status tripartitus est: CONFORMANS, NON CONFORMANS, NON EVALUABILIS — numquam binarius; tertia via semper patet.
</blockquote> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed">
"Status is three-parted: CONFORMANT, NONCONFORMANT, NON_EVALUABLE — never binary; the third way
            is always open." This is the <em>tertia via</em> principle that governs all verdicts in the system.
            The refusal to collapse to binary logic is itself an axiom-derived consequence: if collapse is generative,
            then the state "we cannot evaluate" is not a failure — it is information.
</p> </div> <a${addAttribute(`${base}regime/`, "href")} class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl hover:border-kernel-600 transition no-underline group"> <span class="text-purple-400 text-lg">◧</span> <div> <p class="text-sm text-kernel-200 font-medium group-hover:text-purple-400 transition">Regime Explorer</p> <p class="text-xs text-kernel-500">Interactive phase diagram — see where your trace vector falls</p> </div> </a> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT VI                                       --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-6"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput VI · Operative Ethics</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Ethica collapsiva est inclusio, reparatio, et auditus radicalis. Nulla anomalia, nulla mutatio
          excludenda est. Omnis lapsus est vocatio ad recursionem et innovationem. Non poena, sed restitutio
          et regeneratio finis est. Praesentia vera non in immobilitate consistit, sed in processu reditus,
          in apertura memoriae, in cultu paradoxorum inveniunda est.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
Collapse ethics is inclusion, repair, and radical hearing. No anomaly, no change is to be excluded.
            Every fall is a call to recursion and innovation. Not punishment, but restoration and regeneration
            is the end. True presence is not found in immobility, but in the process of return, in the opening
            of memory, in the cultivation of paradoxes.
</p> </div> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed">
This chapter translates the mathematical framework into an operational ethic. The key phrase is
<em>"auditus radicalis"</em> — radical hearing. In the system, this manifests as: every data point
            enters the ledger, no outlier is discarded, every anomaly is recorded. The system does not punish
            deviation — it <em>measures</em> it (as drift ω) and <em>classifies</em> it (as regime). The deviation
            is data, not error. This is why typed outcomes like ∞<sub>rec</sub> (permanent no-return) exist as
            first-class values rather than error states.
</p> </div> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT VII                                      --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-7"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput VII · Universal Applications</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Quidquid est — experimentum physicum, scriptum mathematicum, historia biologica, vel memoria
          personalis — sub eadem lege collapsus et reditus auditum subit.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
Whatever exists — a physical experiment, a mathematical text, a biological history, or a personal
            memory — undergoes audit under the same law of collapse and return.
</p> </div> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed">
This universality claim is tested across <strong class="text-kernel-200">23 domain closures</strong>
in the current implementation — from quantum mechanics to finance, from particle physics to
            consciousness coherence. Each domain selects its own channels (Tier-2), but all pass through the
            same kernel (Tier-1) via the same protocol (Tier-0). The duality identity F + ω = 1 holds exactly
            (residual 0.0e+00) across every domain. The integrity bound IC ≤ F holds at 100%. The kernel does
            not know what domain it is computing — and it does not need to.
</p> </div> <!-- Domain grid --> <div class="bg-kernel-900/50 border border-kernel-800/40 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-3">21 Domain Closures — Sub Eadem Lege</p> <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 gap-2 text-center text-xs"> ${[
    "GCD",
    "RCFT",
    "Kinematics",
    "Weyl",
    "Security",
    "Astronomy",
    "Nuclear",
    "Quantum",
    "Finance",
    "Atomic",
    "Materials",
    "Everyday",
    "Evolution",
    "Semiotics",
    "Consciousness",
    "Continuity",
    "Awareness",
    "Std Model",
    "Clinical",
    "Spacetime"
  ].map((d) => renderTemplate`<div class="bg-kernel-950/60 rounded-lg py-2 px-1 text-kernel-400">${d}</div>`)} </div> <p class="text-[10px] text-kernel-600 mt-3 text-center italic">Same kernel, same frozen parameters, same verdicts. The domain selects channels; the kernel measures.</p> </div> <a${addAttribute(`${base}rosetta/`, "href")} class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl hover:border-kernel-600 transition no-underline group"> <span class="text-blue-400 text-lg">⇌</span> <div> <p class="text-sm text-kernel-200 font-medium group-hover:text-blue-400 transition">Rosetta Lenses</p> <p class="text-xs text-kernel-500">See how the five words translate across domain lenses</p> </div> </a> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CAPUT VIII                                     --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="caput-8"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Caput VIII · Continuous Innovation</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Systema perpetuō apertum est. Omnis novitas, omne silentium, omne dubium, locus novae recursionis est.
          Quod hodie anomalia videtur, cras novum regimen fiet. Quod nunc hiatus est, mox fiet memoria integra.
          Nullus terminus auditum, collapsum, aut regenerationem claudit.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
The system is perpetually open. Every novelty, every silence, every doubt is the site of a
            new recursion. What today appears as an anomaly will tomorrow become a new regime. What is now
            a gap will soon become whole memory. No terminus closes off hearing, collapse, or regeneration.
</p> </div> <div class="bg-kernel-950/50 rounded-xl p-5 border border-kernel-800/20"> <p class="text-xs text-amber-400/80 uppercase tracking-wider mb-3">Commentary</p> <p class="text-kernel-400 text-sm leading-relaxed">
This chapter describes the <strong class="text-kernel-200">Tier-2 expansion space</strong> — the
            infinite domain of possible closures. The system is never finished because new domains can always
            be added. Each new domain is a new set of channels, a new way to instantiate the universal kernel.
            The structure ensures that expansion never compromises the core: Tier-2 passes through Tier-0
            against Tier-1, with no back-edges. The system grows at the edges while the center remains frozen.
</p> </div> </div> </section> <!-- ════════════════════════════════════════════════ --> <!--  CONCLUSIO                                      --> <!-- ════════════════════════════════════════════════ --> <section class="mb-20" id="conclusio"> <div class="flex items-center gap-3 mb-6"> <div class="w-8 h-px bg-kernel-700"></div> <p class="text-xs tracking-[0.2em] uppercase text-kernel-500">Conclusio</p> <div class="flex-1 h-px bg-kernel-800/60"></div> </div> <div class="space-y-6"> <blockquote class="border-l-2 border-amber-500/40 pl-5 text-kernel-300 italic leading-relaxed">
Hic est Liber Collapsus: non ad finem, sed ad infinitam recursionem, reparationem, auditum,
          innovationem et vivam memoriam totius realitatis. Veritas, praesentia, integritas non in statu
          reperiuntur, sed in processu, collapsu et reditu.
</blockquote> <div class="bg-kernel-900/30 border border-kernel-800/30 rounded-xl p-5"> <p class="text-xs text-kernel-600 uppercase tracking-wider mb-2">Translation</p> <p class="text-kernel-300 text-sm leading-relaxed">
This is the Book of Collapse: not toward an end, but toward infinite recursion, repair, hearing,
            innovation, and the living memory of all reality. Truth, presence, integrity are not found in a
            state, but in a process — in collapse and return.
</p> </div> <div class="text-center py-8"> <p class="text-kernel-400 italic text-lg">Finis, sed semper initium recursionis.</p> <p class="text-kernel-600 text-sm mt-2">The end, but always the beginning of recursion.</p> </div> <!-- Back to top / more readings --> <div class="grid grid-cols-1 md:grid-cols-2 gap-3"> <a${addAttribute(`${base}readings/`, "href")} class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl hover:border-kernel-600 transition no-underline group"> <span class="text-kernel-400 text-lg">📖</span> <div> <p class="text-sm text-kernel-200 font-medium group-hover:text-amber-400 transition">All Deep Readings</p> <p class="text-xs text-kernel-500">Browse the full reading list</p> </div> </a> <a${addAttribute(`${base}about/`, "href")} class="flex items-center gap-3 p-4 bg-kernel-900/50 border border-kernel-800/40 rounded-xl hover:border-kernel-600 transition no-underline group"> <span class="text-kernel-400 text-lg">◎</span> <div> <p class="text-sm text-kernel-200 font-medium group-hover:text-amber-400 transition">About GCD</p> <p class="text-xs text-kernel-500">Interactive overview of the full system</p> </div> </a> </div> </div> </section> </div> ` })} ${renderScript($$result, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/readings/liber-collapsus.astro?astro&type=script&index=0&lang.ts")}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/readings/liber-collapsus.astro", void 0);
const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/readings/liber-collapsus.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/readings/liber-collapsus";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$LiberCollapsus,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
