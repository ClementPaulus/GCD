import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, d as renderSlot } from './server_DjVGnHP9.mjs';
import { g as getCollection, r as renderEntry } from './_astro_content_DlhPuBG1.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$CasepackLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$CasepackLayout;
  const { frontmatter } = Astro2.props;
  const { title = "Casepack", description = "" } = frontmatter || {};
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": title, "description": description }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="mb-8"> <a href=".." class="text-sm text-kernel-500 hover:text-kernel-300">← Back to domain</a> </div> <article class="prose prose-invert prose-sm max-w-none
    prose-headings:font-bold
    prose-code:text-kernel-300 prose-code:bg-kernel-800 prose-code:px-1 prose-code:rounded
    prose-strong:text-kernel-100"> ${renderSlot($$result2, $$slots["default"])} </article> ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/CasepackLayout.astro", void 0);

async function getStaticPaths() {
  const casepacks = await getCollection("casepacks");
  return casepacks.map((entry) => {
    const parts = entry.id.split("/");
    const domain = parts[0];
    const slug = parts.slice(2).join("/");
    return {
      params: { domain, slug },
      props: { entry, domain }
    };
  });
}
const $$slug = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$slug;
  const { entry, domain } = Astro2.props;
  const { Content } = await renderEntry(entry);
  return renderTemplate`${renderComponent($$result, "CasepackLayout", $$CasepackLayout, { "frontmatter": { ...entry.data, domain } }, { "default": async ($$result2) => renderTemplate` ${renderComponent($$result2, "Content", Content, {})} ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/[domain]/casepacks/[slug].astro", void 0);

const $$file = "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/pages/[domain]/casepacks/[slug].astro";
const $$url = "/GENERATIVE-COLLAPSE-DYNAMICS/[domain]/casepacks/[slug]";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$slug,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
