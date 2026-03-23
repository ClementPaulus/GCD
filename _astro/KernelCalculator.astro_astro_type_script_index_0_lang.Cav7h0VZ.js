import{P as A,c as N,a as W,v as D,b as _}from"./kernel.Cz7tUtLI.js";import{g as j,K as q}from"./constants.BqDZhys3.js";let g=8,h=[.95,.92,.97,.93,.96,.94,.91,.98],v=Array(8).fill(.125);function K(){O(),M(),V()}function O(){const t=document.getElementById("preset-buttons");t.innerHTML="";for(const[l,a]of Object.entries(A)){const n=document.createElement("button");n.className="text-xs px-3 py-1.5 bg-kernel-800 text-kernel-300 rounded hover:bg-kernel-700 hover:text-kernel-100 transition",n.textContent=a.name,n.addEventListener("click",()=>{h=[...a.c],v=[...a.w],g=h.length,M(),R()}),t.appendChild(n)}}function M(){const t=document.getElementById("channel-inputs"),l=document.getElementById("weight-inputs");t.innerHTML="",l.innerHTML="";for(let a=0;a<g;a++){const n=document.createElement("div");n.className="flex items-center gap-2",n.innerHTML=`
        <span class="text-xs text-kernel-500 w-8">c${a+1}</span>
        <input type="range" min="0" max="1" step="0.001" value="${h[a]??.5}"
          class="flex-1 h-1.5 accent-amber-500" data-ch="${a}" />
        <input type="number" min="0" max="1" step="0.01" value="${(h[a]??.5).toFixed(3)}"
          class="w-20 px-2 py-1 bg-kernel-800 border border-kernel-600 rounded text-kernel-200 text-xs text-right" data-ch-num="${a}" />
      `,t.appendChild(n);const o=document.createElement("div");o.className="flex items-center gap-2",o.innerHTML=`
        <span class="text-xs text-kernel-500 w-8">w${a+1}</span>
        <input type="range" min="0" max="1" step="0.001" value="${v[a]??1/g}"
          class="flex-1 h-1.5 accent-blue-400" data-w="${a}" />
        <input type="number" min="0" max="1" step="0.01" value="${(v[a]??1/g).toFixed(4)}"
          class="w-20 px-2 py-1 bg-kernel-800 border border-kernel-600 rounded text-kernel-200 text-xs text-right" data-w-num="${a}" />
      `,l.appendChild(o)}P()}function V(){document.getElementById("channel-inputs").addEventListener("input",t=>{const l=t.target,a=l.dataset.ch??l.dataset.chNum;if(a!==void 0){h[parseInt(a)]=parseFloat(l.value);const n=l.closest("div"),o=n.querySelector(`[data-ch="${a}"]`),c=n.querySelector(`[data-ch-num="${a}"]`);o&&l!==o&&(o.value=l.value),c&&l!==c&&(c.value=parseFloat(l.value).toFixed(3))}}),document.getElementById("weight-inputs").addEventListener("input",t=>{const l=t.target,a=l.dataset.w??l.dataset.wNum;if(a!==void 0){v[parseInt(a)]=parseFloat(l.value);const n=l.closest("div"),o=n.querySelector(`[data-w="${a}"]`),c=n.querySelector(`[data-w-num="${a}"]`);o&&l!==o&&(o.value=l.value),c&&l!==c&&(c.value=parseFloat(l.value).toFixed(4)),P()}}),document.getElementById("btn-add-ch").addEventListener("click",()=>{g++,h.push(.5),v.push(0),M()}),document.getElementById("btn-rm-ch").addEventListener("click",()=>{g>2&&(g--,h.pop(),v.pop(),M())}),document.getElementById("btn-uniform").addEventListener("click",()=>{v=Array(g).fill(1/g),M()}),document.getElementById("btn-compute").addEventListener("click",R)}function P(){const t=v.reduce((a,n)=>a+n,0),l=document.getElementById("weight-sum");l.textContent=`Σw = ${t.toFixed(4)}`,l.className=Math.abs(t-1)<.01?"text-xs text-green-400 mt-2":"text-xs text-red-400 mt-2"}function R(){const t=N(h,v),{regime:l,isCritical:a}=W(t),n=D(t);document.getElementById("results-panel").classList.remove("hidden");const o=document.getElementById("regime-badge"),c=j[a?"CRITICAL":l];o.style.backgroundColor=c.bg,o.style.color=c.text,o.style.borderColor=c.border,o.className="text-center py-3 rounded-lg font-bold text-lg border-2",o.textContent=a?`${l} + CRITICAL`:l;const u=document.getElementById("invariants-grid"),m=q,E=[{key:"F",value:t.F,sym:m.F},{key:"omega",value:t.omega,sym:m.omega},{key:"S",value:t.S,sym:m.S},{key:"C",value:t.C,sym:m.C},{key:"kappa",value:t.kappa,sym:m.kappa},{key:"IC",value:t.IC,sym:m.IC}];G(t,l,a),u.innerHTML=E.map(r=>`
      <div class="bg-kernel-800 rounded-lg p-3 border border-kernel-700">
        <div class="text-xs text-kernel-500">${r.sym.name} (${r.sym.symbol})</div>
        <div class="text-lg font-mono font-bold text-kernel-100">${r.value.toFixed(6)}</div>
        <div class="text-xs text-kernel-600 mt-1">${r.sym.latin}</div>
      </div>
    `).join(""),u.innerHTML+=`
      <div class="bg-kernel-800 rounded-lg p-3 border border-kernel-700 col-span-2 md:col-span-3">
        <div class="flex justify-between items-center">
          <span class="text-xs text-kernel-500">Heterogeneity Gap (Δ = F − IC)</span>
          <span class="text-lg font-mono font-bold ${t.delta>.1?"text-amber-400":"text-kernel-100"}">${t.delta.toFixed(6)}</span>
        </div>
        <div class="w-full bg-kernel-900 rounded-full h-2 mt-2">
          <div class="h-2 rounded-full transition-all ${t.delta>.3?"bg-red-500":t.delta>.1?"bg-amber-500":"bg-green-500"}"
            style="width: ${Math.min(t.delta*100,100)}%"></div>
        </div>
      </div>
    `;const e=document.getElementById("identity-checks");e.innerHTML=n.map(r=>`
      <div class="flex items-center justify-between text-sm">
        <span class="text-kernel-300">
          <span class="${r.pass?"text-green-400":"text-red-400"}">${r.pass?"✓":"✗"}</span>
          ${r.name}: ${r.formula}
        </span>
        <span class="font-mono text-xs ${r.pass?"text-green-400":"text-red-400"}">
          |residual| = ${r.residual.toExponential(2)}
        </span>
      </div>
    `).join(""),F(t),document.getElementById("seam-R").addEventListener("input",()=>F(t)),document.getElementById("seam-tauR").addEventListener("input",()=>F(t))}function F(t){const l=parseFloat(document.getElementById("seam-R").value),a=parseFloat(document.getElementById("seam-tauR").value),n=_(t.omega,t.C,l,a),o=document.getElementById("seam-results");o.innerHTML=`
      <div class="grid grid-cols-2 gap-2 text-xs">
        <div class="bg-kernel-800 rounded p-2">
          <span class="text-kernel-500">Γ(ω)</span>
          <span class="float-right font-mono text-kernel-200">${n.gamma.toFixed(6)}</span>
        </div>
        <div class="bg-kernel-800 rounded p-2">
          <span class="text-kernel-500">D_ω (drift debit)</span>
          <span class="float-right font-mono text-kernel-200">${n.D_omega.toFixed(6)}</span>
        </div>
        <div class="bg-kernel-800 rounded p-2">
          <span class="text-kernel-500">D_C (curvature debit)</span>
          <span class="float-right font-mono text-kernel-200">${n.D_C.toFixed(6)}</span>
        </div>
        <div class="bg-kernel-800 rounded p-2">
          <span class="text-kernel-500">Δκ (budget)</span>
          <span class="float-right font-mono text-kernel-200">${n.deltaKappa.toFixed(6)}</span>
        </div>
      </div>
      <div class="mt-2 p-2 rounded text-center font-bold text-sm ${n.pass?"bg-green-900/50 text-green-400 border border-green-700":"bg-red-900/50 text-red-400 border border-red-700"}">
        Seam ${n.pass?"PASS":"FAIL"} — |s| = ${Math.abs(n.residual).toFixed(6)} ${n.pass?"≤":">"} tol=${.005}
      </div>
    `}function G(t,l,a){const n=document.getElementById("radar-canvas"),o=document.getElementById("radar-tooltip"),c=n.parentElement,u=Math.min(c.clientWidth,420),m=u,E=window.devicePixelRatio||1;n.width=Math.round(u*E),n.height=Math.round(m*E),n.style.width=u+"px",n.style.height=m+"px";const e=n.getContext("2d");e.scale(E,E),e.fillStyle="#06060c",e.fillRect(0,0,u,m);const r=u/2,I=m/2,y=Math.min(u,m)/2-40,k=[{label:"F",value:t.F,max:1},{label:"ω",value:t.omega,max:1},{label:"S",value:t.S,max:Math.log(2)+.01},{label:"C",value:t.C,max:1},{label:"κ",value:Math.abs(t.kappa),max:Math.max(Math.abs(t.kappa),5)},{label:"IC",value:t.IC,max:1}],p=k.length;function L(s){return Math.PI*2*s/p-Math.PI/2}for(let s=1;s<=5;s++){const i=s/5*y;e.beginPath();for(let d=0;d<=p;d++){const b=L(d%p),f=r+i*Math.cos(b),C=I+i*Math.sin(b);d===0?e.moveTo(f,C):e.lineTo(f,C)}e.closePath(),e.strokeStyle=s===5?"rgba(255,255,255,0.15)":"rgba(255,255,255,0.06)",e.lineWidth=s===5?.8:.5,e.stroke()}for(let s=0;s<p;s++){const i=L(s);e.beginPath(),e.moveTo(r,I),e.lineTo(r+y*Math.cos(i),I+y*Math.sin(i)),e.strokeStyle="rgba(255,255,255,0.08)",e.lineWidth=.5,e.stroke()}e.font="12px ui-sans-serif, system-ui, sans-serif",e.textAlign="center",e.textBaseline="middle";for(let s=0;s<p;s++){const i=L(s),d=r+(y+22)*Math.cos(i),b=I+(y+22)*Math.sin(i);e.fillStyle="rgba(255,255,255,0.7)",e.fillText(k[s].label,d,b),e.font="9px ui-monospace, monospace",e.fillStyle="rgba(255,255,255,0.4)";const f=k[s].label==="κ"?t.kappa.toFixed(3):k[s].value.toFixed(3);e.fillText(f,d,b+14),e.font="12px ui-sans-serif, system-ui, sans-serif"}const $=[];for(let s=0;s<p;s++){const i=Math.min(k[s].value/k[s].max,1),d=L(s);$.push([r+i*y*Math.cos(d),I+i*y*Math.sin(d)])}const S=a?"rgba(168,85,247,":l==="STABLE"?"rgba(34,197,94,":l==="WATCH"?"rgba(245,158,11,":"rgba(239,68,68,";e.beginPath();for(let s=0;s<=p;s++){const[i,d]=$[s%p];s===0?e.moveTo(i,d):e.lineTo(i,d)}e.closePath(),e.fillStyle=S+"0.12)",e.fill(),e.shadowColor=S+"0.5)",e.shadowBlur=8,e.strokeStyle=S+"0.8)",e.lineWidth=2,e.stroke(),e.shadowBlur=0;for(let s=0;s<p;s++){const[i,d]=$[s];e.beginPath(),e.arc(i,d,4,0,Math.PI*2),e.fillStyle=S+"0.9)",e.fill(),e.strokeStyle="#fff",e.lineWidth=.5,e.stroke()}e.beginPath(),e.arc(r,I,2,0,Math.PI*2),e.fillStyle="rgba(255,255,255,0.25)",e.fill();const H=s=>{const i=n.getBoundingClientRect(),d=s.clientX-i.left,b=s.clientY-i.top;let f=-1,C=20;for(let x=0;x<p;x++){const w=d-$[x][0],B=b-$[x][1],T=Math.sqrt(w*w+B*B);T<C&&(C=T,f=x)}if(f>=0){const x=k[f],w=x.label==="κ"?t.kappa.toFixed(6):x.value.toFixed(6);o.innerHTML=`${x.label} = ${w}`,o.style.left=d+12+"px",o.style.top=b-10+"px",o.classList.remove("hidden")}else o.classList.add("hidden")};n.onmousemove=H,n.onmouseleave=()=>o.classList.add("hidden")}K();
