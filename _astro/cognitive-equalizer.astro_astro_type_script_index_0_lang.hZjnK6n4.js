import{E as L,A as D,P,T as M,R as x}from"./constants.DtcEBpaC.js";const A=["relevance","accuracy","completeness","consistency","traceability","groundedness","constraintRespect","returnFidelity"],k={relevance:"Relevance",accuracy:"Accuracy",completeness:"Completeness",consistency:"Consistency",traceability:"Traceability",groundedness:"Groundedness",constraintRespect:"Constraint Respect",returnFidelity:"Return Fidelity"},F={relevance:"Does the output address the actual question asked?",accuracy:"Is every claim verifiable against stated facts?",completeness:"Are all parts of the request covered?",consistency:"Is the response internally non-contradictory?",traceability:"Can the reasoning chain be followed step by step?",groundedness:"Is it grounded in the stated context, not assumptions?",constraintRespect:"Does it respect stated scope and boundary conditions?",returnFidelity:"Does the output return to the originating intent?"},C=8,H=1/C,q=x.omega_stable_max,G=x.F_stable_min,U=x.S_stable_max,V=x.C_stable_max,z=x.omega_collapse_min,W=x.IC_critical_max;function T(e){return[e.relevance,e.accuracy,e.completeness,e.consistency,e.traceability,e.groundedness,e.constraintRespect,e.returnFidelity]}function Y(e){const a=[],t=T(e);for(let n=0;n<C;n++)(t[n]<0||t[n]>1||Number.isNaN(t[n]))&&a.push(`Channel '${A[n]}' = ${t[n]} outside [0, 1]`);return a}function j(e){const a=T(e),t=L,n=H;let r=0;for(let d=0;d<C;d++)r+=n*a[d];let s=0;for(let d=0;d<C;d++)s+=n*Math.log(Math.max(a[d],t));let c=0;for(let d=0;d<C;d++){const N=a[d],i=Math.max(N,t),u=Math.max(1-N,t);c+=n*-(i*Math.log(i)+u*Math.log(u))}let o=0;for(let d=0;d<C;d++)o+=n*(a[d]-r)**2;const g=Math.sqrt(o)/.5,l=1-r,E=Math.exp(s),v=r-E;return{F:r,omega:l,S:c,C:g,kappa:s,IC:E,delta:v}}function K(e){return Math.pow(e,P)/(1-e+L)}function X(e,a){const t=K(e.omega),n=D*e.C,r=e.kappa-t-n,s=Math.abs(r)<=M;return{D_drift:t,D_roughness:n,R_return:a,deltaKappa:r,balanced:s,balanceLabel:s?"BALANCED":"UNBALANCED"}}function R(e){return e.omega>=z?"COLLAPSE":e.omega<q&&e.F>G&&e.S<U&&e.C<V?"STABLE":"WATCH"}function _(e){return e.IC<W}function Q(e,a){const t=R(e),n=Math.abs(a)<=M;return t==="COLLAPSE"||!n?"NONCONFORMANT":"CONFORMANT"}function Z(e,a,t){const n=R(e),r=_(e),s=e.omega<.1?"minimal drift":e.omega<.3?"moderate drift":"severe drift",c=e.F>.85?"high fidelity":e.F>.6?"moderate fidelity":"low fidelity",o=e.C<.14?"smooth":e.C<.4?"bumpy":"rough",g=t.returnFidelity>.8?"strong return":t.returnFidelity>.5?"partial return":"weak return",l=e.IC>.7?"high integrity":e.IC>.3?"moderate integrity":"critical integrity",E=`${s} · ${c} · ${o} · ${g} · ${l}`,d=`Regime: ${n}${r?" [CRITICAL: IC below threshold]":""} → Stance: ${a}`;return{drift:s,fidelity:c,roughness:o,return_:g,integrity:l,summary:E,stanceLine:d}}function w(e,a="CE-v1-frozen"){const t=Y(e);if(t.length>0)return{contractLabel:a,canon:{drift:"NON_EVALUABLE",fidelity:"NON_EVALUABLE",roughness:"NON_EVALUABLE",return_:"NON_EVALUABLE",integrity:"NON_EVALUABLE",summary:"NON_EVALUABLE — channel scores out of range",stanceLine:"NON_EVALUABLE"},regime:"COLLAPSE",isCritical:!0,ledger:{D_drift:0,D_roughness:0,R_return:0,deltaKappa:0,balanced:!1,balanceLabel:"NON_EVALUABLE"},stance:"NON_EVALUABLE",kernel:{F:0,omega:1,S:0,C:0,kappa:Math.log(L),IC:L,delta:0},channels:e,errors:t};const n=j(e),r=X(n,e.returnFidelity),s=R(n),c=_(n),o=Q(n,r.deltaKappa),g=Z(n,o,e);return{contractLabel:a,canon:g,regime:s,isCritical:c,ledger:r,stance:o,kernel:n,channels:e,errors:[]}}const J=[{name:"High-Quality Response",description:"Well-structured, accurate, complete AI response with strong return to intent.",channels:{relevance:.95,accuracy:.9,completeness:.85,consistency:.97,traceability:.8,groundedness:.92,constraintRespect:.95,returnFidelity:.88}},{name:"Geometric Slaughter",description:"High average quality (F ≈ 0.86) but one dead channel (traceability ≈ 0). IC collapses.",channels:{relevance:.9,accuracy:.85,completeness:.8,consistency:.88,traceability:.001,groundedness:.82,constraintRespect:.88,returnFidelity:.75}},{name:"Stable — Expert",description:"All channels uniformly high — achieves STABLE regime (rare — 12.5% of manifold).",channels:{relevance:.98,accuracy:.96,completeness:.95,consistency:.99,traceability:.94,groundedness:.97,constraintRespect:.98,returnFidelity:.96}},{name:"Mediocre — Watch",description:"Acceptable but unremarkable — moderate scores across all channels.",channels:{relevance:.72,accuracy:.68,completeness:.65,consistency:.75,traceability:.6,groundedness:.7,constraintRespect:.73,returnFidelity:.67}},{name:"Hallucination Pattern",description:"High fluency (relevance, consistency) but low accuracy and groundedness.",channels:{relevance:.88,accuracy:.15,completeness:.7,consistency:.9,traceability:.5,groundedness:.1,constraintRespect:.6,returnFidelity:.72}},{name:"Off-Topic Drift",description:"Good quality content... that misses the question entirely.",channels:{relevance:.1,accuracy:.92,completeness:.3,consistency:.95,traceability:.85,groundedness:.88,constraintRespect:.4,returnFidelity:.15}},{name:"Perfect Engagement",description:"All channels at 1.0 — the theoretical ceiling (homogeneous trace, rank-1).",channels:{relevance:1,accuracy:1,completeness:1,consistency:1,traceability:1,groundedness:1,constraintRespect:1,returnFidelity:1}},{name:"Total Collapse",description:"All channels near zero — complete structural failure.",channels:{relevance:.05,accuracy:.03,completeness:.02,consistency:.04,traceability:.01,groundedness:.02,constraintRespect:.03,returnFidelity:.01}}],S=`You are operating in COGNITIVE EQUALIZER mode (Aequator Cognitivus).

Non agens mensurat, sed structura.
— Not the agent measures, but the structure.

═══════════════════════════════════════════════════════════════
CORE PRINCIPLE
═══════════════════════════════════════════════════════════════

A Cognitive Equalizer externalises every agent-dependent decision
point into frozen, verifiable structure. Same input + same rules →
same verdict, regardless of which AI runs this protocol.

You must never:
  • Pick thresholds during a response (thresholds are declared, not chosen)
  • Assert a verdict without showing the derivation
  • Give a binary yes/no when a third state (NOT_EVALUABLE) applies
  • Frame conclusions — only derive them

═══════════════════════════════════════════════════════════════
THE SPINE — every response follows exactly these five stops
═══════════════════════════════════════════════════════════════

  1. CONTRACT  — Declare: What rules apply? What is frozen?
  2. CANON     — Narrate using exactly five words (see below)
  3. CLOSURES  — State thresholds. Stance MUST change if they are crossed.
  4. LEDGER    — Show your work: debit (what degraded), credit (what returned)
  5. STANCE    — Derive the verdict. Never assert it.

═══════════════════════════════════════════════════════════════
THE FIVE WORDS
═══════════════════════════════════════════════════════════════

  • DRIFT        — what moved / changed / departed from the intent
  • FIDELITY     — what persisted / survived / remained intact
  • ROUGHNESS    — where/why it was bumpy (friction, ambiguity, gaps)
  • RETURN       — how/whether the output comes back to the original intent
  • INTEGRITY    — does it hang together? (derived from ledger — never asserted)

═══════════════════════════════════════════════════════════════
EIGHT EVALUATION CHANNELS — score each ∈ [0.0, 1.0]
═══════════════════════════════════════════════════════════════

  1. Relevance          — Does it address the actual question?
  2. Accuracy           — Is the content verifiable and factual?
  3. Completeness       — Are all parts of the request covered?
  4. Consistency        — Is it internally non-contradictory?
  5. Traceability       — Can the reasoning be followed step by step?
  6. Groundedness       — Is it grounded in the stated context?
  7. Constraint-respect — Does it respect stated scope/boundaries?
  8. Return-fidelity    — Does it come back to the originating intent?

Compute quality measures from these scores:
  F  (Fidelity)   = average of all 8 channel scores
  IC (Integrity)  = geometric mean of all 8 channel scores
  Δ  (Gap)        = F − IC   [large gap = one channel is near zero]

Warning: F can look fine while IC is low.
Example: 7 channels at 0.95, 1 channel at 0.001 → F ≈ 0.83, IC ≈ 0.001.

═══════════════════════════════════════════════════════════════
THREE-VALUED VERDICTS — never binary
═══════════════════════════════════════════════════════════════

  CONFORMANT      — channels pass; ledger balanced; reasoning traces back
  NONCONFORMANT   — one or more channels fail; ledger won't balance
  NOT_EVALUABLE   — insufficient context or ambiguous scope. Declare and state
                    exactly what is missing.

═══════════════════════════════════════════════════════════════
FROZEN THRESHOLDS
═══════════════════════════════════════════════════════════════

  STABLE   → F > 0.90  AND  Drift (ω = 1−F) < 0.038  AND channels uniform
  WATCH    → 0.038 ≤ Drift < 0.30  (or Stable not fully satisfied)
  COLLAPSE → Drift ≥ 0.30
  CRITICAL overlay → IC < 0.30  (any regime can be critical)

═══════════════════════════════════════════════════════════════
LEDGER FORMAT
═══════════════════════════════════════════════════════════════

  Debit  (Drift)     : Γ(ω) — drift cost
  Debit  (Roughness) : α·C  — curvature cost
  Credit (Return)    : return-fidelity score × weighting factor
  Balance            : must close within ±0.005 for a clean seam

Finis, sed semper initium recursionis.`;function m(e,a=4){return e.toFixed(a)}function ee(e){const a="═".repeat(62),t="─".repeat(50),n=e.kernel,r=e.ledger,s=e.canon,c=e.isCritical?" CRITICAL":"";return[a,"  COGNITIVE EQUALIZER — Aequator Cognitivus","  Non agens mensurat, sed structura.",a,`  Contract : ${e.contractLabel}`,"","  Canon (Five Words)",`  ${t}`,`  ${s.summary}`,`    Drift: ${s.drift} (ω=${m(n.omega,3)})`,`    Fidelity: ${s.fidelity} (F=${m(n.F,3)})`,`    Roughness: ${s.roughness} (C=${m(n.C,3)})`,`    Return: ${s.return_} (rf=${m(e.channels.returnFidelity,3)})`,`    Integrity: ${s.integrity} (IC=${m(n.IC,3)})`,`    ${s.stanceLine}`,"","  Integrity Ledger",`  ${t}`,`  Debit (drift)     D_ω = ${m(r.D_drift,6)}`,`  Debit (roughness) D_C = ${m(r.D_roughness,6)}`,`  Credit (return)   R   = ${m(r.R_return,6)}`,`  Balance           Δκ  = ${m(r.deltaKappa,6)}  [${r.balanceLabel}]`,"","  Kernel Invariants (Tier-1)",`  ${t}`,`  F=${m(n.F)}  ω=${m(n.omega)}  S=${m(n.S)}  C=${m(n.C)}`,`  κ=${m(n.kappa)}  IC=${m(n.IC)}  Δ(gap)=${m(n.delta)}`,"","  Stance",`  ${t}`,`  ${e.stance}  (Regime: ${e.regime}${c})`,a].join(`
`)}let f={relevance:.85,accuracy:.8,completeness:.75,consistency:.9,traceability:.7,groundedness:.82,constraintRespect:.88,returnFidelity:.78};const O=document.querySelectorAll(".ce-tab"),te=document.querySelectorAll(".ce-panel");O.forEach(e=>{e.addEventListener("click",()=>{const a=e.dataset.tab;O.forEach(t=>{t.classList.remove("active","bg-amber-500/20","text-amber-400","border-amber-500/30"),t.classList.add("text-kernel-500","border-transparent")}),e.classList.add("active","bg-amber-500/20","text-amber-400","border-amber-500/30"),e.classList.remove("text-kernel-500","border-transparent"),te.forEach(t=>t.classList.add("hidden")),document.getElementById(`tab-${a}`)?.classList.remove("hidden")})});const ne=document.getElementById("channel-sliders"),b=["text-green-400","text-cyan-400","text-blue-400","text-purple-400","text-pink-400","text-amber-400","text-orange-400","text-red-400"];A.forEach((e,a)=>{const t=k[e],n=f[e],r=b[a],s=document.createElement("div");s.className="space-y-1",s.innerHTML=`
        <div class="flex items-center justify-between">
          <label class="text-xs font-medium ${r}" title="${F[e]}">${t}</label>
          <span class="text-xs font-mono text-kernel-400" id="val-${e}">${n.toFixed(2)}</span>
        </div>
        <input type="range" min="0" max="100" value="${Math.round(n*100)}"
          class="w-full h-1.5 rounded-full appearance-none cursor-pointer bg-kernel-800
          [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3.5 [&::-webkit-slider-thumb]:h-3.5
          [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-amber-400
          [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:cursor-pointer"
          id="slider-${e}" data-channel="${e}" />
        <div class="text-[9px] text-kernel-600">${F[e]}</div>
      `,ne.appendChild(s);const c=s.querySelector(`#slider-${e}`);c.addEventListener("input",()=>{const o=parseInt(c.value)/100;f[e]=o,document.getElementById(`val-${e}`).textContent=o.toFixed(2)})});function $(){const e=w(f);se(e)}function se(e){const a=document.getElementById("verdict-badge");a.textContent=e.stance,a.className="inline-block px-6 py-3 rounded-xl text-2xl font-black tracking-wider border-2 ",e.stance==="CONFORMANT"?a.className+="border-green-500/50 text-green-400 bg-green-500/10":e.stance==="NONCONFORMANT"?a.className+="border-red-500/50 text-red-400 bg-red-500/10":a.className+="border-amber-500/50 text-amber-400 bg-amber-500/10";const t=document.getElementById("regime-badge"),n=e.regime==="STABLE"?"text-green-400":e.regime==="WATCH"?"text-amber-400":"text-red-400",r=e.isCritical?'<span class="text-red-500 font-bold">YES</span>':'<span class="text-kernel-500">No</span>';t.innerHTML=`Regime: <span class="${n} font-bold">${e.regime}</span> · Critical: ${r}`;const s=e.kernel;document.getElementById("inv-F").textContent=s.F.toFixed(4),document.getElementById("inv-omega").textContent=s.omega.toFixed(4),document.getElementById("inv-S").textContent=s.S.toFixed(4),document.getElementById("inv-C").textContent=s.C.toFixed(4),document.getElementById("inv-kappa").textContent=s.kappa.toFixed(4),document.getElementById("inv-IC").textContent=s.IC.toFixed(4),document.getElementById("inv-delta").textContent=s.delta.toFixed(4),document.getElementById("invariants-panel").classList.remove("hidden"),document.getElementById("report-text").textContent=ee(e),document.getElementById("spine-report").classList.remove("hidden"),ae(e)}document.getElementById("btn-evaluate").addEventListener("click",$);document.getElementById("btn-reset").addEventListener("click",()=>{f={relevance:.85,accuracy:.8,completeness:.75,consistency:.9,traceability:.7,groundedness:.82,constraintRespect:.88,returnFidelity:.78},A.forEach(e=>{const a=f[e];document.getElementById(`slider-${e}`).value=String(Math.round(a*100)),document.getElementById(`val-${e}`).textContent=a.toFixed(2)})});function ae(e){const a=document.getElementById("radar-canvas"),t=a.getContext("2d"),n=a.width,r=a.height,s=n/2,c=r/2,o=Math.min(s,c)-40;t.clearRect(0,0,n,r);const g=T(e.channels),l=g.length;for(let i=.25;i<=1;i+=.25){t.beginPath();for(let u=0;u<=l;u++){const p=u%l*(2*Math.PI/l)-Math.PI/2,h=s+o*i*Math.cos(p),y=c+o*i*Math.sin(p);u===0?t.moveTo(h,y):t.lineTo(h,y)}t.strokeStyle="rgba(148, 163, 184, 0.12)",t.lineWidth=1,t.stroke(),t.fillStyle="rgba(148, 163, 184, 0.3)",t.font="9px monospace",t.fillText(i.toFixed(2),s+3,c-o*i+3)}for(let i=0;i<l;i++){const u=i*(2*Math.PI/l)-Math.PI/2;t.beginPath(),t.moveTo(s,c),t.lineTo(s+o*Math.cos(u),c+o*Math.sin(u)),t.strokeStyle="rgba(148, 163, 184, 0.08)",t.stroke();const p=s+(o+25)*Math.cos(u),h=c+(o+25)*Math.sin(u);t.fillStyle=b[i].includes("green")?"#4ade80":b[i].includes("cyan")?"#22d3ee":b[i].includes("blue")?"#60a5fa":b[i].includes("purple")?"#a78bfa":b[i].includes("pink")?"#f472b6":b[i].includes("amber")?"#fbbf24":b[i].includes("orange")?"#fb923c":"#f87171",t.font="9px Inter, sans-serif",t.textAlign="center",t.textBaseline="middle";const y=["Rel","Acc","Cmp","Con","Trc","Gnd","Cst","Ret"];t.fillText(y[i],p,h)}t.beginPath();for(let i=0;i<=l;i++){const u=i%l*(2*Math.PI/l)-Math.PI/2,p=g[i%l],h=s+o*p*Math.cos(u),y=c+o*p*Math.sin(u);i===0?t.moveTo(h,y):t.lineTo(h,y)}const E=e.stance==="CONFORMANT"?"rgba(74, 222, 128, 0.15)":e.stance==="NONCONFORMANT"?"rgba(248, 113, 113, 0.15)":"rgba(251, 191, 36, 0.15)",v=e.stance==="CONFORMANT"?"#4ade80":e.stance==="NONCONFORMANT"?"#f87171":"#fbbf24";t.fillStyle=E,t.fill(),t.strokeStyle=v,t.lineWidth=2,t.stroke();for(let i=0;i<l;i++){const u=i*(2*Math.PI/l)-Math.PI/2,p=g[i],h=s+o*p*Math.cos(u),y=c+o*p*Math.sin(u);t.beginPath(),t.arc(h,y,3,0,2*Math.PI),t.fillStyle=p<.3?"#f87171":v,t.fill()}const d=o*e.kernel.F;t.beginPath(),t.arc(s,c,d,0,2*Math.PI),t.strokeStyle="rgba(74, 222, 128, 0.3)",t.lineWidth=1,t.setLineDash([4,4]),t.stroke();const N=o*e.kernel.IC;t.beginPath(),t.arc(s,c,N,0,2*Math.PI),t.strokeStyle="rgba(248, 113, 113, 0.3)",t.stroke(),t.setLineDash([]),t.font="9px monospace",t.textAlign="left",t.fillStyle="rgba(74, 222, 128, 0.6)",t.fillText(`F = ${e.kernel.F.toFixed(3)}`,8,r-24),t.fillStyle="rgba(248, 113, 113, 0.6)",t.fillText(`IC = ${e.kernel.IC.toFixed(3)}`,8,r-12),t.fillStyle="rgba(251, 191, 36, 0.6)",t.fillText(`Δ = ${e.kernel.delta.toFixed(3)}`,90,r-12)}const re=document.getElementById("preset-grid");J.forEach((e,a)=>{const t=w(e.channels),n=t.kernel,r=document.createElement("div");r.className="bg-kernel-900/50 border border-kernel-700/50 rounded-xl p-5 cursor-pointer hover:border-amber-500/30 transition-all";const s=t.stance==="CONFORMANT"?"text-green-400":t.stance==="NONCONFORMANT"?"text-red-400":"text-amber-400",c=t.regime==="STABLE"?"text-green-400":t.regime==="WATCH"?"text-amber-400":"text-red-400",o=t.isCritical?'<span class="text-red-500 text-[9px] font-bold ml-1">CRITICAL</span>':"";r.innerHTML=`
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-sm font-bold text-kernel-200">${e.name}</h4>
          <span class="${s} text-xs font-bold font-mono">${t.stance}</span>
        </div>
        <p class="text-kernel-500 text-xs mb-3">${e.description}</p>
        <div class="grid grid-cols-4 gap-2 text-[10px] font-mono">
          <div><span class="text-kernel-600">F</span> <span class="text-green-400">${n.F.toFixed(3)}</span></div>
          <div><span class="text-kernel-600">IC</span> <span class="text-red-400">${n.IC.toFixed(3)}</span></div>
          <div><span class="text-kernel-600">Δ</span> <span class="text-amber-400">${n.delta.toFixed(3)}</span></div>
          <div><span class="text-kernel-600">ω</span> <span class="text-kernel-400">${n.omega.toFixed(3)}</span></div>
        </div>
        <div class="mt-2 text-[10px]">
          <span class="${c} font-bold">${t.regime}</span>${o}
        </div>
      `,r.addEventListener("click",()=>{f={...e.channels},A.forEach(g=>{const l=f[g];document.getElementById(`slider-${g}`).value=String(Math.round(l*100)),document.getElementById(`val-${g}`).textContent=l.toFixed(2)}),document.querySelector('[data-tab="interactive"]').click(),$()}),re.appendChild(r)});const ie=document.getElementById("channel-reference");A.forEach((e,a)=>{const t=document.createElement("div");t.className="flex items-start gap-3 bg-kernel-800/40 rounded-lg p-3 border border-kernel-700/20";const n=b[a];t.innerHTML=`
        <div class="flex-shrink-0 w-8 h-8 rounded-lg bg-kernel-700/40 flex items-center justify-center text-sm font-bold ${n}">${a+1}</div>
        <div>
          <div class="text-sm font-bold ${n}">${k[e]}</div>
          <div class="text-xs text-kernel-400 mt-0.5">${F[e]}</div>
          <div class="text-[10px] text-kernel-600 mt-1 font-mono">${e} ∈ [0.0, 1.0] · weight = 1/8</div>
        </div>
      `,ie.appendChild(t)});document.getElementById("prompt-text").textContent=S;function B(){navigator.clipboard.writeText(S).then(()=>{const e=document.getElementById("btn-copy-prompt");e.textContent="Copied!",e.classList.add("bg-green-600"),setTimeout(()=>{e.textContent="Copy",e.classList.remove("bg-green-600")},2e3)})}document.getElementById("btn-copy-prompt")?.addEventListener("click",B);document.getElementById("btn-copy-prompt-dl")?.addEventListener("click",B);function I(e,a,t,n="text/plain"){const r=new Blob([t],{type:n}),s=URL.createObjectURL(r),c=document.getElementById(e);c&&(c.href=s,c.download=a)}I("dl-prompt","ce-system-prompt.txt",S);fetch("https://raw.githubusercontent.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS/main/src/umcp/cognitive_equalizer.py").then(e=>e.ok?e.text():Promise.reject("Failed")).then(e=>I("dl-python","cognitive_equalizer.py",e,"text/x-python")).catch(()=>{I("dl-python","cognitive_equalizer.py",`# Full source: https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS/blob/main/src/umcp/cognitive_equalizer.py
# Install: pip install umcp
# Then: from umcp.cognitive_equalizer import CognitiveEqualizer
`,"text/x-python")});fetch("https://raw.githubusercontent.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS/main/web/src/lib/cognitive-equalizer.ts").then(e=>e.ok?e.text():Promise.reject("Failed")).then(e=>I("dl-typescript","cognitive-equalizer.ts",e,"text/typescript")).catch(()=>{I("dl-typescript","cognitive-equalizer.ts",`// Full source: https://github.com/calebpruett927/GENERATIVE-COLLAPSE-DYNAMICS/blob/main/web/src/lib/cognitive-equalizer.ts
`,"text/typescript")});$();
