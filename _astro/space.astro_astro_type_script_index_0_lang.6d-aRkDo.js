import{g as ct,a as Tt,c as nt}from"./kernel.CLAplkPS.js";import{B as O,h as Lt,e as St,g as yt}from"./spacetime.-7WOE-tC.js";import"./constants.6x37F0HI.js";function X(){return new Float32Array(16)}function dt(){const e=X();return e[0]=e[5]=e[10]=e[15]=1,e}function _t(e,r,s,t){const n=X(),l=1/Math.tan(e*.5),a=1/(s-t);return n[0]=l/r,n[5]=l,n[10]=(t+s)*a,n[11]=-1,n[14]=2*t*s*a,n}function rt(e,r){const s=X();for(let t=0;t<4;t++)for(let n=0;n<4;n++)s[n*4+t]=e[t]*r[n*4]+e[4+t]*r[n*4+1]+e[8+t]*r[n*4+2]+e[12+t]*r[n*4+3];return s}function Ft(e){const r=dt(),s=Math.cos(e),t=Math.sin(e);return r[5]=s,r[6]=t,r[9]=-t,r[10]=s,r}function it(e){const r=Math.sqrt(e[0]*e[0]+e[1]*e[1]+e[2]*e[2])||1;return[e[0]/r,e[1]/r,e[2]/r]}function at(e,r){return[e[1]*r[2]-e[2]*r[1],e[2]*r[0]-e[0]*r[2],e[0]*r[1]-e[1]*r[0]]}function Bt(e,r,s){const t=it([e[0]-r[0],e[1]-r[1],e[2]-r[2]]),n=it(at(s,t)),l=at(t,n),a=dt();return a[0]=n[0],a[4]=n[1],a[8]=n[2],a[12]=-(n[0]*e[0]+n[1]*e[1]+n[2]*e[2]),a[1]=l[0],a[5]=l[1],a[9]=l[2],a[13]=-(l[0]*e[0]+l[1]*e[1]+l[2]*e[2]),a[2]=t[0],a[6]=t[1],a[10]=t[2],a[14]=-(t[0]*e[0]+t[1]*e[1]+t[2]*e[2]),a[3]=0,a[7]=0,a[11]=0,a[15]=1,a}const wt=`
attribute vec2 aPos;
varying vec2 vUV;
void main() {
  vUV = aPos * 0.5 + 0.5;
  gl_Position = vec4(aPos, 0.0, 1.0);
}
`,It=`
precision highp float;
varying vec2 vUV;
uniform vec2 uBHScreen;      // black hole center in screen [0,1]
uniform float uBHRadius;     // angular radius of event horizon
uniform float uLensStrength;  // gravitational lensing magnitude
uniform float uTime;

// Pseudo-random hash for star generation
float hash(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

// Procedural starfield
vec3 starfield(vec2 uv) {
  vec3 col = vec3(0.0);
  // Multiple layers at different scales
  for (int layer = 0; layer < 3; layer++) {
    float scale = 80.0 + float(layer) * 120.0;
    vec2 id = floor(uv * scale);
    vec2 f = fract(uv * scale) - 0.5;
    float h = hash(id + float(layer) * 100.0);
    if (h > 0.97) {
      float brightness = (h - 0.97) / 0.03;
      float r = length(f);
      float star = smoothstep(0.15, 0.0, r) * brightness;
      // Star color temperature variation
      float temp = hash(id * 2.0 + 7.0);
      vec3 starCol = mix(
        mix(vec3(0.6, 0.7, 1.0), vec3(1.0, 1.0, 0.95), temp),
        vec3(1.0, 0.8, 0.5),
        max(0.0, temp - 0.7) * 3.33
      );
      // Twinkling
      float twinkle = 0.7 + 0.3 * sin(uTime * (1.0 + h * 3.0) + h * 100.0);
      col += starCol * star * twinkle;
    }
  }
  // Subtle nebula glow
  float nebula = hash(floor(uv * 8.0)) * 0.015;
  col += vec3(0.15, 0.05, 0.2) * nebula;
  return col;
}

void main() {
  vec2 uv = vUV;
  vec2 centered = uv - uBHScreen;
  float dist = length(centered);
  vec2 dir = centered / max(dist, 0.001);

  // ── Gravitational lensing distortion ──
  // Einstein ring radius: R_E ∝ √(lensStrength)
  float rEinstein = sqrt(uLensStrength) * 0.15;
  // Deflection angle: θ = R_E² / dist (point mass approximation)
  float deflection = rEinstein * rEinstein / max(dist, 0.001);
  // Limit max deflection to avoid artifacts
  deflection = min(deflection, 0.5);
  // Apply radial deflection outward (light bends toward mass)
  vec2 lensedUV = uv + dir * deflection;

  // ── Event horizon shadow ──
  float horizonR = uBHRadius;
  // Photon sphere at 1.5× horizon
  float photonR = horizonR * 1.5;
  // Shadow is larger than horizon due to photon capture
  float shadowR = horizonR * 2.6;

  // ── Render starfield with lensing ──
  vec3 col = starfield(lensedUV);

  // ── Photon ring (bright ring at photon sphere) ──
  float ringDist = abs(dist - photonR);
  float photonRing = exp(-ringDist * ringDist / (0.0004 * photonR * photonR)) * 1.2;
  // Secondary ring (inner)
  float ring2Dist = abs(dist - photonR * 0.75);
  float ring2 = exp(-ring2Dist * ring2Dist / (0.0002 * photonR * photonR)) * 0.5;
  vec3 ringColor = vec3(1.0, 0.85, 0.4);
  col += ringColor * (photonRing + ring2);

  // ── Einstein ring glow ──
  float eRingDist = abs(dist - rEinstein);
  float eRing = exp(-eRingDist * eRingDist / (0.0008 * rEinstein * rEinstein)) * 0.4;
  col += vec3(0.5, 0.7, 1.0) * eRing;

  // ── Event horizon shadow (black disk) ──
  float shadowEdge = smoothstep(shadowR, shadowR * 0.85, dist);
  col *= (1.0 - shadowEdge);

  // ── Horizon edge glow (Hawking radiation analog) ──
  float edgeGlow = exp(-(dist - shadowR) * (dist - shadowR) / (0.001 * shadowR * shadowR));
  col += vec3(0.8, 0.3, 0.1) * edgeGlow * 0.3;

  gl_FragColor = vec4(col, 1.0);
}
`,zt=`
attribute vec3 aPosition;
attribute vec2 aTexCoord;
uniform mat4 uMVP;
varying vec2 vTexCoord;
varying vec3 vWorldPos;

void main() {
  gl_Position = uMVP * vec4(aPosition, 1.0);
  vTexCoord = aTexCoord;
  vWorldPos = aPosition;
}
`,Dt=`
precision highp float;
varying vec2 vTexCoord;
varying vec3 vWorldPos;
uniform float uTime;
uniform float uInnerR;
uniform float uOuterR;

float noise(vec2 p) {
  return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
  float r = length(vWorldPos.xz);
  float angle = atan(vWorldPos.z, vWorldPos.x);

  // Normalized radial position in disk
  float t = (r - uInnerR) / (uOuterR - uInnerR);
  t = clamp(t, 0.0, 1.0);

  // Temperature profile: hotter at inner edge
  float temp = 1.0 - t * 0.7;

  // Keplerian velocity for Doppler beaming
  float orbitalV = 1.0 / sqrt(max(r, 0.1));

  // Turbulent spiral structure
  float spiral = sin(angle * 4.0 - log(max(r, 0.01)) * 8.0 + uTime * orbitalV * 2.0)
               * 0.5 + 0.5;
  spiral = mix(0.6, 1.0, spiral);

  // Fine structure turbulence
  float turb = noise(vec2(angle * 20.0 + uTime * 0.5, r * 15.0)) * 0.2 + 0.8;

  // Color: hot inner = blue-white, outer = red-orange
  vec3 innerColor = vec3(0.9, 0.95, 1.0);    // blue-white
  vec3 midColor = vec3(1.0, 0.7, 0.2);       // yellow-orange
  vec3 outerColor = vec3(0.8, 0.15, 0.05);   // deep red

  vec3 diskColor = mix(innerColor, midColor, smoothstep(0.0, 0.4, t));
  diskColor = mix(diskColor, outerColor, smoothstep(0.4, 1.0, t));

  // Doppler beaming: approaching side brighter
  float doppler = 1.0 + 0.4 * sin(angle + uTime * 0.3) * orbitalV;

  float brightness = temp * spiral * turb * doppler;

  // Edge softness
  float innerEdge = smoothstep(0.0, 0.05, t);
  float outerEdge = smoothstep(1.0, 0.9, t);
  brightness *= innerEdge * outerEdge;

  // Opacity falloff
  float alpha = brightness * 0.85;
  alpha *= innerEdge * outerEdge;

  gl_FragColor = vec4(diskColor * brightness, alpha);
}
`,Vt=`
attribute vec3 aPosition;
attribute vec3 aColor;
attribute float aSize;
uniform mat4 uMVP;
varying vec3 vColor;

void main() {
  gl_Position = uMVP * vec4(aPosition, 1.0);
  vColor = aColor;
  gl_PointSize = aSize;
}
`,Ut=`
precision mediump float;
varying vec3 vColor;

void main() {
  vec2 c = gl_PointCoord - 0.5;
  float r = length(c);
  if (r > 0.5) discard;
  float glow = exp(-r * r * 8.0);
  gl_FragColor = vec4(vColor * glow, glow * 0.8);
}
`;function Ot(e,r,s,t){const n=(t+1)*s,l=new Float32Array(n*5);let a=0;for(let u=0;u<=t;u++){const h=u/t,M=e+h*(r-e);for(let x=0;x<s;x++){const P=x/s*Math.PI*2;l[a++]=M*Math.cos(P),l[a++]=0,l[a++]=M*Math.sin(P),l[a++]=h,l[a++]=x/s}}const d=t*s*6,g=new Uint16Array(d);let b=0;for(let u=0;u<t;u++)for(let h=0;h<s;h++){const M=u*s+h,x=u*s+(h+1)%s,P=(u+1)*s+h,H=(u+1)*s+(h+1)%s;g[b++]=M,g[b++]=P,g[b++]=x,g[b++]=x,g[b++]=P,g[b++]=H}return{verts:l,indices:g}}function k(e,r,s){if(e==="accretion"){const t=r+Math.random()*(s-r),n=Math.random()*Math.PI*2,l=1/Math.sqrt(t);return{x:t*Math.cos(n),y:(Math.random()-.5)*.05,z:t*Math.sin(n),vx:-l*Math.sin(n)*.3,vy:0,vz:l*Math.cos(n)*.3,life:0,maxLife:3+Math.random()*5,size:2+Math.random()*3,type:e,cr:1,cg:.7+Math.random()*.3,cb:.2+Math.random()*.3}}else if(e==="jet"){const t=Math.random()>.5?1:-1,n=.1;return{x:(Math.random()-.5)*n,y:t*r*.3,z:(Math.random()-.5)*n,vx:(Math.random()-.5)*.05,vy:t*(1.5+Math.random()),vz:(Math.random()-.5)*.05,life:0,maxLife:1.5+Math.random()*2,size:1.5+Math.random()*2,type:e,cr:.4+Math.random()*.3,cg:.5+Math.random()*.4,cb:1}}else{const t=Math.random()*Math.PI*2,n=s*(1.2+Math.random()*.5);return{x:n*Math.cos(t),y:(Math.random()-.5)*.3,z:n*Math.sin(t),vx:-Math.cos(t)*.2,vy:0,vz:-Math.sin(t)*.2,life:0,maxLife:4+Math.random()*4,size:1.5+Math.random()*2.5,type:e,cr:.9,cg:.5,cb:.2}}}function q(e,r){const n=Math.min(.98,.01+(1-Math.min(e/20,1))*(r-.01)),l=ct(n),a=Tt(nt(O[0].c,O[0].w)),d=nt(O[0].c,O[0].w);return{omega:n,gamma:l,regime:a.regime+(a.isCritical?" (Critical)":""),redshift:yt(n),escapeV:St(n),hawkingT:Lt(d.kappa),distance:e,F:d.F,IC:d.IC,kappa:d.kappa,S:d.S,C:d.C,delta:d.delta}}function kt(e,r){const s=e.getContext("webgl",{antialias:!0,alpha:!1,premultipliedAlpha:!1});if(!s)return console.error("WebGL not available"),{destroy:()=>{},getHUD:()=>q(10,.95)};const t=s;t.getExtension("OES_standard_derivatives"),t.enable(t.DEPTH_TEST),t.enable(t.BLEND),t.blendFunc(t.SRC_ALPHA,t.ONE_MINUS_SRC_ALPHA),t.clearColor(0,0,0,1);function n(i,m){const c=t.createShader(i);return t.shaderSource(c,m),t.compileShader(c),t.getShaderParameter(c,t.COMPILE_STATUS)||console.error("Shader:",t.getShaderInfoLog(c)),c}function l(i,m){const c=t.createProgram();return t.attachShader(c,n(t.VERTEX_SHADER,i)),t.attachShader(c,n(t.FRAGMENT_SHADER,m)),t.linkProgram(c),t.getProgramParameter(c,t.LINK_STATUS)||console.error("Link:",t.getProgramInfoLog(c)),c}const a=l(wt,It),d=l(zt,Dt),g=l(Vt,Ut),b=t.createBuffer();t.bindBuffer(t.ARRAY_BUFFER,b),t.bufferData(t.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),t.STATIC_DRAW);const u=.6,h=3,M=Ot(u,h,128,32),x=t.createBuffer();t.bindBuffer(t.ARRAY_BUFFER,x),t.bufferData(t.ARRAY_BUFFER,M.verts,t.STATIC_DRAW);const P=t.createBuffer();t.bindBuffer(t.ELEMENT_ARRAY_BUFFER,P),t.bufferData(t.ELEMENT_ARRAY_BUFFER,M.indices,t.STATIC_DRAW);const H=400,A=[];for(let i=0;i<200;i++){const m=i<120?"accretion":i<160?"jet":"infalling",c=k(m,u,h);c.life=Math.random()*c.maxLife,A.push(c)}const ut=t.createBuffer();let D=0,w=.35,E=8,L=!1,_=0,F=0,V=!0,U=0,C=.35,I=8;e.addEventListener("mousedown",i=>{L=!0,V=!1,_=i.clientX,F=i.clientY,e.style.cursor="grabbing"}),e.addEventListener("mousemove",i=>{L&&(U+=(i.clientX-_)*.005,C+=(i.clientY-F)*.005,C=Math.max(-Math.PI*.45,Math.min(Math.PI*.45,C)),_=i.clientX,F=i.clientY)}),e.addEventListener("mouseup",()=>{L=!1,e.style.cursor="grab"}),e.addEventListener("mouseleave",()=>{L=!1,e.style.cursor="grab"}),e.addEventListener("touchstart",i=>{L=!0,V=!1,_=i.touches[0].clientX,F=i.touches[0].clientY,i.preventDefault()},{passive:!1}),e.addEventListener("touchmove",i=>{L&&(U+=(i.touches[0].clientX-_)*.005,C+=(i.touches[0].clientY-F)*.005,C=Math.max(-Math.PI*.45,Math.min(Math.PI*.45,C)),_=i.touches[0].clientX,F=i.touches[0].clientY,i.preventDefault())},{passive:!1}),e.addEventListener("touchend",()=>{L=!1}),e.addEventListener("wheel",i=>{I+=i.deltaY*.01,I=Math.max(2,Math.min(25,I)),i.preventDefault()},{passive:!1}),e.addEventListener("dblclick",()=>{V=!0,C=.35,I=8}),e.style.cursor="grab";const N=.95,S={aPos:t.getAttribLocation(a,"aPos"),uBHScreen:t.getUniformLocation(a,"uBHScreen"),uBHRadius:t.getUniformLocation(a,"uBHRadius"),uLensStrength:t.getUniformLocation(a,"uLensStrength"),uTime:t.getUniformLocation(a,"uTime")},v={aPosition:t.getAttribLocation(d,"aPosition"),aTexCoord:t.getAttribLocation(d,"aTexCoord"),uMVP:t.getUniformLocation(d,"uMVP"),uTime:t.getUniformLocation(d,"uTime"),uInnerR:t.getUniformLocation(d,"uInnerR"),uOuterR:t.getUniformLocation(d,"uOuterR")},R={aPosition:t.getAttribLocation(g,"aPosition"),aColor:t.getAttribLocation(g,"aColor"),aSize:t.getAttribLocation(g,"aSize"),uMVP:t.getUniformLocation(g,"uMVP")};function J(){const i=Math.min(window.devicePixelRatio||1,2),m=e.clientWidth,c=e.clientHeight;e.width=Math.round(m*i),e.height=Math.round(c*i),t.viewport(0,0,e.width,e.height)}J();const Q=new ResizeObserver(J);Q.observe(e);let Y=q(E,N),Z=!0,G=0;function $(i){if(!Z)return;const m=Math.min((i-G)/1e3,.05);G=i,V&&(U+=m*.08),D+=(U-D)*.05,w+=(C-w)*.05,E+=(I-E)*.05;const c=E*Math.cos(w)*Math.sin(D),ft=E*Math.sin(w),ht=E*Math.cos(w)*Math.cos(D),mt=e.width/e.height,gt=_t(.9,mt,.1,100),pt=Bt([c,ft,ht],[0,0,0],[0,1,0]),B=rt(gt,pt),vt=B[12]/B[15],At=B[13]/B[15],xt=[vt*.5+.5,At*.5+.5],Rt=Math.atan(.5/E)/(.9/2),bt=ct(N)/(E*.5),tt=i/1e3;t.clear(t.COLOR_BUFFER_BIT|t.DEPTH_BUFFER_BIT),t.depthMask(!1),t.disable(t.DEPTH_TEST),t.useProgram(a),t.bindBuffer(t.ARRAY_BUFFER,b),t.enableVertexAttribArray(S.aPos),t.vertexAttribPointer(S.aPos,2,t.FLOAT,!1,0,0),t.uniform2fv(S.uBHScreen,xt),t.uniform1f(S.uBHRadius,Rt),t.uniform1f(S.uLensStrength,bt),t.uniform1f(S.uTime,tt),t.drawArrays(t.TRIANGLE_STRIP,0,4),t.disableVertexAttribArray(S.aPos),t.depthMask(!0),t.enable(t.DEPTH_TEST);const Et=Ft(.12),Mt=rt(B,Et);t.useProgram(d),t.bindBuffer(t.ARRAY_BUFFER,x),t.bindBuffer(t.ELEMENT_ARRAY_BUFFER,P);const et=20;t.enableVertexAttribArray(v.aPosition),t.vertexAttribPointer(v.aPosition,3,t.FLOAT,!1,et,0),v.aTexCoord>=0&&(t.enableVertexAttribArray(v.aTexCoord),t.vertexAttribPointer(v.aTexCoord,2,t.FLOAT,!1,et,12)),t.uniformMatrix4fv(v.uMVP,!1,Mt),t.uniform1f(v.uTime,tt),t.uniform1f(v.uInnerR,u),t.uniform1f(v.uOuterR,h),t.enable(t.BLEND),t.blendFunc(t.SRC_ALPHA,t.ONE_MINUS_SRC_ALPHA),t.drawElements(t.TRIANGLES,M.indices.length,t.UNSIGNED_SHORT,0),t.disableVertexAttribArray(v.aPosition),v.aTexCoord>=0&&t.disableVertexAttribArray(v.aTexCoord);for(let p=A.length-1;p>=0;p--){const o=A[p];if(o.life+=m,o.life>o.maxLife){A[p]=k(o.type,u,h);continue}if(o.type==="accretion"){const f=Math.sqrt(o.x*o.x+o.z*o.z)||.1,ot=1/(f*Math.sqrt(f))*.5,Pt=-o.z/f,Ct=o.x/f;o.vx=Pt*ot-o.x/f*.01,o.vz=Ct*ot-o.z/f*.01}else if(o.type==="jet")o.vy*=1.01;else{const f=Math.sqrt(o.x*o.x+o.z*o.z)||.1;o.vx-=o.x/f*.05*m,o.vz-=o.z/f*.05*m}o.x+=o.vx*m,o.y+=o.vy*m,o.z+=o.vz*m;const y=Math.sqrt(o.x*o.x+o.y*o.y+o.z*o.z);(y<.2||y>15)&&(A[p]=k(o.type,u,h))}for(;A.length<H;){const p=Math.random(),o=p<.5?"accretion":p<.75?"jet":"infalling";A.push(k(o,u,h))}const T=new Float32Array(A.length*7);for(let p=0;p<A.length;p++){const o=A[p],y=Math.min(1,Math.min(o.life/.3,(o.maxLife-o.life)/.5)),f=p*7;T[f]=o.x,T[f+1]=o.y,T[f+2]=o.z,T[f+3]=o.cr*y,T[f+4]=o.cg*y,T[f+5]=o.cb*y,T[f+6]=o.size*(.5+y*.5)}t.useProgram(g),t.bindBuffer(t.ARRAY_BUFFER,ut),t.bufferData(t.ARRAY_BUFFER,T,t.DYNAMIC_DRAW);const W=28;t.enableVertexAttribArray(R.aPosition),t.vertexAttribPointer(R.aPosition,3,t.FLOAT,!1,W,0),t.enableVertexAttribArray(R.aColor),t.vertexAttribPointer(R.aColor,3,t.FLOAT,!1,W,12),t.enableVertexAttribArray(R.aSize),t.vertexAttribPointer(R.aSize,1,t.FLOAT,!1,W,24),t.uniformMatrix4fv(R.uMVP,!1,B),t.blendFunc(t.SRC_ALPHA,t.ONE),t.drawArrays(t.POINTS,0,A.length),t.disableVertexAttribArray(R.aPosition),t.disableVertexAttribArray(R.aColor),t.disableVertexAttribArray(R.aSize),t.blendFunc(t.SRC_ALPHA,t.ONE_MINUS_SRC_ALPHA),Y=q(E,N),r&&r(Y),requestAnimationFrame($)}return requestAnimationFrame(i=>{G=i,$(i)}),{destroy:()=>{Z=!1,Q.disconnect()},getHUD:()=>Y}}const K=document.getElementById("sim-canvas"),Ht=document.getElementById("hud-F"),Nt=document.getElementById("hud-omega"),Yt=document.getElementById("hud-IC"),Gt=document.getElementById("hud-kappa"),Wt=document.getElementById("hud-S"),qt=document.getElementById("hud-delta"),Xt=document.getElementById("hud-gamma"),Kt=document.getElementById("hud-redshift"),jt=document.getElementById("hud-vesc"),Jt=document.getElementById("hud-hawking"),Qt=document.getElementById("hud-dist"),st=document.getElementById("hud-regime"),Zt=document.getElementById("regime-bar");let lt=0;function $t(e){const r=performance.now();if(r-lt<66)return;lt=r,Ht.textContent=e.F.toFixed(4),Nt.textContent=e.omega.toFixed(4),Yt.textContent=e.IC.toFixed(4),Gt.textContent=e.kappa.toFixed(4),Wt.textContent=e.S.toFixed(4),qt.textContent=e.delta.toFixed(4),Xt.textContent=e.gamma.toFixed(3),Kt.textContent=e.redshift.toFixed(4),jt.textContent=e.escapeV.toFixed(4)+" c",Jt.textContent=e.hawkingT.toFixed(6),Qt.textContent=e.distance.toFixed(1)+" r_s";const s=e.regime.split(" ")[0];st.textContent=e.regime,st.className="hud-value regime-"+s.toLowerCase();const t={STABLE:"#059669",WATCH:"#d97706",COLLAPSE:"#dc2626"};Zt.style.backgroundColor=t[s]||"#333"}kt(K,$t);const z=document.getElementById("controls-overlay");let j=setTimeout(()=>z.classList.add("hidden"),6e3);K.addEventListener("mousedown",()=>{clearTimeout(j),z.classList.add("hidden")});K.addEventListener("touchstart",()=>{clearTimeout(j),z.classList.add("hidden")});z.addEventListener("click",()=>{clearTimeout(j),z.classList.add("hidden")});
