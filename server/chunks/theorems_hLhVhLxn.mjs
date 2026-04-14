import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate } from './server_DjVGnHP9.mjs';
import { g as getCollection, r as renderEntry } from './_astro_content_DlhPuBG1.mjs';
import { $ as $$SubpageLayout } from './SubpageLayout_DyWA_FvM.mjs';

async function getStaticPaths() {
  const theorems = await getCollection("theorems");
  return theorems.map((entry) => {
    const domain = entry.id.split("/")[0];
    return {
      params: { domain },
      props: { entry, domain }
    };
  });
}
const $$Theorems = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$Theorems;
  const { entry, domain } = Astro2.props;
  const { Content } = await renderEntry(entry);
  return renderTemplate`${renderComponent($$result, "SubpageLayout", $$SubpageLayout, { "frontmatter": { ...entry.data, domain, pageType: "theorems" } }, { "default": async ($$result2) => renderTemplate` ${renderComponent($$result2, "Content", Content, {})} ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/[domain]/theorems.astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/[domain]/theorems.astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/[domain]/theorems";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Theorems,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
