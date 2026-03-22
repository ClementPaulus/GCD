import{b as y,g as v,d as k}from"./kernel.D906R9kQ.js";import{T as $,b as R,O as m,A as C}from"./constants.DoHs_Qwz.js";const s={omega:document.getElementById("omega"),curvature:document.getElementById("curvature"),R:document.getElementById("R"),tauR:document.getElementById("tauR"),infRec:document.getElementById("inf-rec"),kappaLedger:document.getElementById("kappa-ledger")},w={stable:{omega:.02,C:.08,R:.8,tauR:3,inf:!1,kappa:0},watch:{omega:.15,C:.2,R:.5,tauR:8,inf:!1,kappa:0},collapse:{omega:.55,C:.45,R:.3,tauR:20,inf:!1,kappa:0},pole:{omega:.97,C:.6,R:.1,tauR:50,inf:!1,kappa:0},gesture:{omega:.4,C:.3,R:0,tauR:1,inf:!0,kappa:0}};function E(a){const e=w[a];e&&(s.omega.value=`${e.omega}`,s.curvature.value=`${e.C}`,s.R.value=`${e.R}`,s.tauR.value=`${e.tauR}`,s.infRec.checked=e.inf,s.kappaLedger.value=`${e.kappa}`,h())}document.querySelectorAll("[data-preset]").forEach(a=>{a.addEventListener("click",()=>{E(a.dataset.preset)})});function h(){const a=parseFloat(s.omega.value),e=parseFloat(s.curvature.value),t=parseFloat(s.R.value),l=s.infRec.checked?1/0:parseInt(s.tauR.value),n=parseFloat(s.kappaLedger.value);document.getElementById("omega-label").textContent=a.toFixed(3),document.getElementById("curvature-label").textContent=e.toFixed(2),document.getElementById("R-label").textContent=t.toFixed(2),document.getElementById("tauR-label").textContent=s.infRec.checked?"∞_rec":`${l}`,document.getElementById("kappa-label").textContent=n.toFixed(2);const o=y(a,e,t,l,n),d=o.gamma,x=o.D_omega,c=o.D_C,p=s.infRec.checked?0:t*l,b=[{l:"Γ(ω)",v:d>1e3?d.toExponential(2):d.toFixed(4),c:"text-red-400"},{l:"D_C = α·C",v:c.toFixed(4),c:"text-amber-400"},{l:"Credit R·τ_R",v:s.infRec.checked?"0 (∞_rec)":p.toFixed(4),c:p>0?"text-green-400":"text-kernel-500"},{l:"Δκ (budget)",v:o.deltaKappa>1e3?o.deltaKappa.toExponential(2):o.deltaKappa.toFixed(4),c:o.pass?"text-green-400":"text-red-400"}];document.getElementById("budget-results").innerHTML=b.map(f=>`
      <div class="bg-kernel-900 border border-kernel-700 rounded-lg p-3 text-center">
        <div class="text-xs text-kernel-500">${f.l}</div>
        <div class="font-mono text-lg ${f.c}">${f.v}</div>
      </div>
    `).join("");const u=x+c,r=Math.max(u,p,.01);document.getElementById("budget-bars").innerHTML=`
      <div class="space-y-2">
        <div>
          <div class="flex justify-between text-xs text-kernel-500 mb-1">
            <span>Debits: D_ω + D_C = ${u.toFixed(4)}</span>
            <span class="text-red-400">Cost</span>
          </div>
          <div class="h-6 bg-kernel-800 rounded overflow-hidden flex">
            <div class="h-full bg-red-600" style="width: ${Math.min(100,x/r*100)}%;"
                 title="Γ(ω) = ${x.toFixed(4)}"></div>
            <div class="h-full bg-amber-600" style="width: ${Math.min(100,c/r*100)}%;"
                 title="D_C = ${c.toFixed(4)}"></div>
          </div>
          <div class="flex text-[10px] text-kernel-600 mt-0.5 gap-3">
            <span class="flex items-center gap-1"><span class="w-2 h-2 bg-red-600 rounded-sm inline-block"></span> Γ(ω)</span>
            <span class="flex items-center gap-1"><span class="w-2 h-2 bg-amber-600 rounded-sm inline-block"></span> D_C</span>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-xs text-kernel-500 mb-1">
            <span>Credit: R·τ_R = ${s.infRec.checked?"0":p.toFixed(4)}</span>
            <span class="text-green-400">Return</span>
          </div>
          <div class="h-6 bg-kernel-800 rounded overflow-hidden">
            <div class="h-full bg-green-600" style="width: ${s.infRec.checked?0:Math.min(100,p/r*100)}%;"></div>
          </div>
        </div>
      </div>`;const i=o.pass,g=Math.abs(o.residual);document.getElementById("verdict-line").innerHTML=`
      <span class="px-3 py-1 rounded text-sm font-bold ${i?"bg-green-900/60 text-green-400 border border-green-700":"bg-red-900/60 text-red-400 border border-red-700"}">
        ${i?"SEAM PASS":"SEAM FAIL"}
      </span>
      <span class="text-xs text-kernel-500">|residual| = ${g>1e3?g.toExponential(2):g.toFixed(6)} ${i?"≤":">"} tol = ${$}</span>
      ${s.infRec.checked?'<span class="text-xs text-kernel-600 italic ml-2">(Gesture — τ_R = ∞_rec, no credit)</span>':""}`,_(a)}function _(a){const e=document.getElementById("gamma-chart"),t=200,l=10;let n=`<svg viewBox="0 0 ${t} 100" preserveAspectRatio="none" class="w-full h-full">`;for(let r=1;r<=l;r+=1){const i=100-r/l*100;n+=`<line x1="0" y1="${i}" x2="${t}" y2="${i}" stroke="#334155" stroke-width="0.3" />`}let o="M";for(let r=0;r<=t;r++){const i=r/t,g=v(i),f=100-Math.min(g/l,1)*100;o+=`${r},${f} `}n+=`<path d="${o}" fill="none" stroke="#ef4444" stroke-width="1.5" />`;const d=a*t,x=100-Math.min(v(a)/l,1)*100;n+=`<circle cx="${d}" cy="${x}" r="3" fill="#f59e0b" stroke="#fff" stroke-width="0.5" />`,n+=`<line x1="${d}" y1="0" x2="${d}" y2="100" stroke="#f59e0b" stroke-width="0.5" stroke-dasharray="2,2" />`;const c=m*t,p=100-Math.min(v(m)/l,1)*100;n+=`<line x1="${c}" y1="0" x2="${c}" y2="100" stroke="#a855f7" stroke-width="0.5" stroke-dasharray="3,3" />`,n+=`<circle cx="${c}" cy="${p}" r="2" fill="#a855f7" />`;const b=.038*t,u=.3*t;n+=`<line x1="${b}" y1="0" x2="${b}" y2="100" stroke="#22c55e" stroke-width="0.3" stroke-dasharray="4,4" />`,n+=`<line x1="${u}" y1="0" x2="${u}" y2="100" stroke="#ef4444" stroke-width="0.3" stroke-dasharray="4,4" />`,n+="</svg>",e.innerHTML=`
      <div class="absolute left-0 top-0 bottom-0 w-6 text-[9px] text-kernel-600 flex flex-col justify-between pr-1">
        <span>${l}</span>
        <span>${l/2}</span>
        <span>0</span>
      </div>
      <div class="ml-6 h-full">${n}</div>
      <div class="absolute text-[9px] text-amber-400 font-mono" style="left: ${d/t*95+5}%; top: 4px;">
        Γ(${a.toFixed(3)}) = ${v(a).toFixed(4)}
      </div>
      <div class="absolute text-[9px] text-purple-400 font-mono" style="left: ${m*95+5}%; bottom: 4px;">
        ω_trap = ${m}
      </div>`}function F(){const a=[{name:"Γ(ω) — Drift Cost",formula:"Γ(ω) = ω^p / (1 − ω + ε)",desc:`Monotone increasing with a pole at ω = 1. The frozen exponent p = ${R} makes ω_trap = ${m} the Cardano root of x³ + x − 1 = 0. Beyond ω_trap, return cost exceeds capacity.`,color:"border-red-700/50",samples:[0,.038,.15,.3,.5,m,.8,.95].map(e=>({w:e,g:v(e)}))},{name:"D_C — Curvature Cost",formula:`D_C = α · C (α = ${C})`,desc:"Linear cost in curvature. Measures coupling to uncontrolled degrees of freedom. At C = 0 (homogeneous), no curvature cost. At C = 1 (max heterogeneity), full penalty.",color:"border-amber-700/50",samples:[0,.1,.2,.3,.5,.7,.9,1].map(e=>({w:e,g:k(e)}))},{name:"R·τ_R — Return Credit",formula:"Credit = R · τ_R (0 if τ_R = ∞_rec)",desc:"Only what returns earns credit. R measures credibility of re-entry; τ_R measures delay. Infinite delay (∞_rec) yields zero credit — the gesture gets nothing.",color:"border-green-700/50",samples:[{w:"R=0.1, τ=3",g:.3},{w:"R=0.5, τ=5",g:2.5},{w:"R=1.0, τ=10",g:10},{w:"R=0.3, τ=∞",g:0}]}];document.getElementById("cost-anatomy").innerHTML=a.map(e=>`
      <div class="bg-kernel-800 border ${e.color} rounded-lg p-4">
        <h3 class="text-sm font-bold text-kernel-200 mb-1">${e.name}</h3>
        <div class="text-xs font-mono text-kernel-400 mb-2">${e.formula}</div>
        <p class="text-xs text-kernel-500 mb-3">${e.desc}</p>
        <table class="w-full text-xs">
          <thead><tr class="text-kernel-500"><th class="text-left">Input</th><th class="text-right">Value</th></tr></thead>
          <tbody>
            ${e.samples.map(t=>`
              <tr class="border-t border-kernel-700/50">
                <td class="text-kernel-400 py-0.5">${typeof t.w=="number"?t.w.toFixed(3):t.w}</td>
                <td class="text-right font-mono text-kernel-300">${t.g>1e3?t.g.toExponential(2):t.g.toFixed(4)}</td>
              </tr>`).join("")}
          </tbody>
        </table>
      </div>
    `).join("")}Object.values(s).forEach(a=>{a.type!=="checkbox"?a.addEventListener("input",h):a.addEventListener("change",h)});F();h();
