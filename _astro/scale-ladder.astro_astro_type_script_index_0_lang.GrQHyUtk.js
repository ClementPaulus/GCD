import{c as u,a as p}from"./kernel.D906R9kQ.js";import{E as m}from"./constants.DoHs_Qwz.js";const y=[{name:"Quarks",subtitle:"Fundamental fermions",channels:[.63,.5,.33,1,.5,0,.33,.33],channelNames:["mass_log","spin","charge","color","isospin","lepton","baryon","generation"],color:"blue"},{name:"Hadrons",subtitle:"Composite (confinement)",channels:[.55,.5,.5,m,.5,0,1,.33],channelNames:["mass_log","spin","charge","color_confined","isospin","lepton","baryon","generation"],color:"red"},{name:"Nuclei",subtitle:"Nuclear binding",channels:[.6,.5,.45,m,.4,0,1,.5],channelNames:["mass_log","spin","charge","color_confined","isospin","lepton","baryon","shell"],color:"amber"},{name:"Atoms",subtitle:"Electronic restoration",channels:[.65,.5,.8,.75,.7,.8,.85,.9],channelNames:["mass","spin","ionization","electronegativity","radius","affinity","melting_pt","density"],color:"green"},{name:"Molecules",subtitle:"Chemical bonding",channels:[.7,.6,.85,.8,.75,.65,.78,.82],channelNames:["bond_energy","symmetry","polarity","reactivity","stability","flexibility","dipole","orbital_overlap"],color:"cyan"}],i=y.map(e=>{const t=e.channels.map(()=>1/e.channels.length),n=u(e.channels,t),l=p(n);return{...e,result:n,regime:l,icf:n.F>0?n.IC/n.F:0}}),k=document.getElementById("ladder-visual");k.innerHTML=`
    <div class="flex items-end gap-1 justify-center mb-4" style="height: 200px;">
      ${i.map((e,t)=>{const n=Math.max(5,e.icf*100),l=e.icf>.7?"bg-green-500":e.icf>.3?"bg-amber-500":"bg-red-500";return`
          <div class="flex flex-col items-center flex-1 max-w-[120px]">
            <div class="text-xs font-mono text-kernel-400 mb-1">${e.icf.toFixed(3)}</div>
            <div class="w-full ${l} rounded-t transition-all" style="height: ${n*2}px;"></div>
            <div class="text-xs text-kernel-300 font-bold mt-2">${e.name}</div>
            <div class="text-[10px] text-kernel-500">${e.subtitle}</div>
          </div>
          ${t<i.length-1?`
            <div class="flex flex-col items-center mx-1 self-center">
              <div class="text-xs text-kernel-600">→</div>
              <div class="text-[10px] text-kernel-600 mt-1">${i[t+1].icf>e.icf?"↑ restore":"↓ slaughter"}</div>
            </div>
          `:""}`}).join("")}
    </div>
    <div class="grid grid-cols-5 gap-2 mt-4">
      ${i.map(e=>{const t=e.regime.regime==="STABLE"?"text-green-400":e.regime.regime==="WATCH"?"text-amber-400":"text-red-400";return`
          <div class="bg-kernel-800 rounded p-2 text-center text-xs">
            <div class="text-kernel-500">F</div>
            <div class="font-mono text-kernel-300">${e.result.F.toFixed(3)}</div>
            <div class="text-kernel-500 mt-1">IC</div>
            <div class="font-mono text-kernel-300">${e.result.IC.toFixed(3)}</div>
            <div class="text-kernel-500 mt-1">Δ</div>
            <div class="font-mono text-kernel-300">${e.result.delta.toFixed(3)}</div>
            <div class="${t} font-bold mt-1">${e.regime.regime}</div>
          </div>`}).join("")}
    </div>`;const C=[{name:"Confinement",from:0,to:1,explanation:"Quarks → Hadrons: color channel dies (1.00 → ε). This is geometric slaughter — one dead channel out of 8 kills IC while F drops only moderately.",key:"Color channel → ε"},{name:"Nuclear Binding",from:1,to:2,explanation:"Hadrons → Nuclei: channels remain similar. Nuclear binding preserves the confined state but reorganizes isospin. IC stays low because color is still dead.",key:"Color still dead, isospin shifts"},{name:"Electronic Restoration",from:2,to:3,explanation:"Nuclei → Atoms: entirely new channels (ionization, electronegativity, radius, affinity) replace confined nuclear channels. IC/F jumps from ~0.01 to ~0.96.",key:"New DOF replace dead channels"},{name:"Chemical Bonding",from:3,to:4,explanation:"Atoms → Molecules: bonding creates new channels (polarity, reactivity, orbital overlap). IC remains high because bonding adds structure without killing channels.",key:"Additional coherent channels"}];document.getElementById("boundaries").innerHTML=C.map(e=>{const t=i[e.from],n=i[e.to],o=n.icf-t.icf<-.1,a=o?"border-red-700/50":"border-green-700/50",s=o?"↓":"↑",r=o?"text-red-400":"text-green-400";return`
      <div class="bg-kernel-800 border ${a} rounded-lg p-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-bold text-kernel-200">${e.name}</span>
          <span class="font-mono text-xs ${r}">${s} IC/F: ${t.icf.toFixed(3)} → ${n.icf.toFixed(3)}</span>
        </div>
        <div class="text-xs text-kernel-500 mb-2">${t.name} → ${n.name}</div>
        <p class="text-xs text-kernel-400 mb-2">${e.explanation}</p>
        <div class="text-xs text-kernel-600">Key: ${e.key}</div>
      </div>`}).join("");const v=document.getElementById("n-channels"),x=document.getElementById("n-dead"),h=document.getElementById("healthy-val");function f(){const e=parseInt(v.value),t=Math.min(parseInt(x.value),e-1),n=parseFloat(h.value);document.getElementById("n-label").textContent=`${e}`,document.getElementById("dead-label").textContent=`${t}`,document.getElementById("healthy-label").textContent=n.toFixed(2),x.max=`${Math.min(4,e-1)}`;const l=Array(e-t).fill(n).concat(Array(t).fill(m)),o=l.map(()=>1/l.length),a=u(l,o),s=p(a),r=a.F>0?a.IC/a.F:0,b=s.regime==="STABLE"?"text-green-400":s.regime==="WATCH"?"text-amber-400":"text-red-400";document.getElementById("slaughter-results").innerHTML=[{l:"F (Fidelity)",v:a.F.toFixed(6),c:"text-green-400"},{l:"IC (Integrity)",v:a.IC.toFixed(6),c:a.IC<.3?"text-red-400":"text-purple-400"},{l:"Δ (Het. Gap)",v:a.delta.toFixed(6),c:a.delta>.3?"text-red-400":"text-kernel-300"},{l:"Regime",v:s.regime+(s.isCritical?" + CRIT":""),c:b}].map(d=>`
      <div class="bg-kernel-800 rounded p-2 text-center">
        <div class="text-xs text-kernel-500">${d.l}</div>
        <div class="font-mono text-sm ${d.c}">${d.v}</div>
      </div>
    `).join("");const c=Math.max(0,Math.min(100,r*100)),g=document.getElementById("explorer-bar");g.style.width=`${c}%`,g.className=`h-full transition-all duration-300 rounded-lg ${c>70?"bg-green-500":c>40?"bg-amber-500":"bg-red-500"}`,document.getElementById("explorer-bar-label").textContent=`IC/F = ${r.toFixed(4)}`}[v,x,h].forEach(e=>e.addEventListener("input",f));f();const $=[{name:"Particle Physics",ladder:"quarks → hadrons → atoms",slaughter:"Color confinement kills IC (98% drop)",recovery:"Electronic DOF restore IC at atomic scale",icon:"⚛️"},{name:"Finance",ladder:"portfolios → crises → recoveries",slaughter:"Subprime collapse → one dead sector channel",recovery:"Diversification into new asset classes",icon:"📈"},{name:"Consciousness",ladder:"waking → sleep stages → dream",slaughter:"Deep sleep: executive function → ε",recovery:"REM restores coherence with new processing modes",icon:"🧠"},{name:"Semiotics",ladder:"formal → pidgin → creole",slaughter:"Language contact kills grammatical channels",recovery:"Creolization introduces new grammatical structure",icon:"📜"},{name:"History",ladder:"empire → collapse → renaissance",slaughter:"Fall of Rome: institutional channels die",recovery:"Renaissance restores with new cultural DOF",icon:"🏛️"},{name:"Evolution",ladder:"species → extinction → radiation",slaughter:"Mass extinction: diversity channels → ε",recovery:"Adaptive radiation fills new niches",icon:"🧬"}];document.getElementById("domain-examples").innerHTML=$.map(e=>`
    <div class="bg-kernel-800 border border-kernel-700 rounded-lg p-4 hover:border-kernel-500 transition">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-xl">${e.icon}</span>
        <span class="text-sm font-bold text-kernel-200">${e.name}</span>
      </div>
      <div class="text-xs text-kernel-400 mb-1">
        <span class="text-kernel-500">Ladder:</span> ${e.ladder}
      </div>
      <div class="text-xs text-red-400/80 mb-1">
        <span class="text-kernel-500">Slaughter:</span> ${e.slaughter}
      </div>
      <div class="text-xs text-green-400/80">
        <span class="text-kernel-500">Recovery:</span> ${e.recovery}
      </div>
    </div>
  `).join("");
