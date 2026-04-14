import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead } from './server_DjVGnHP9.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$404 = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "404 — Not Found", "description": "Page not found" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="text-center py-20"> <h1 class="text-6xl font-bold tracking-tight mb-2 text-kernel-300">404</h1> <p class="text-sm font-mono text-kernel-500 mb-8">τ_R = ∞_rec — no return detected</p> <p class="text-lg text-kernel-400 mb-8">
The page you're looking for does not exist in the collapse manifold.
</p> <a href="/" class="text-blue-400 hover:text-blue-300 hover:underline">
← Return to domain network
</a> </div> ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/404.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/404.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/404";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$404,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
