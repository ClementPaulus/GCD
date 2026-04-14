import { c as createComponent } from './astro-component_BX-qrZ11.mjs';
import 'piccolore';
import { b as renderComponent, r as renderTemplate, m as maybeRenderHead, d as renderSlot } from './server_DjVGnHP9.mjs';
import { $ as $$BaseLayout } from './BaseLayout_CFgWoUUk.mjs';

const $$SubpageLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$props, $$slots);
  Astro2.self = $$SubpageLayout;
  const { frontmatter } = Astro2.props;
  const { title = "Sub-page", description = "", domain = "", pageType = "" } = frontmatter || {};
  const typeLabels = {
    contract: "Contract",
    theorems: "Theorems",
    entities: "Entities"
  };
  const typeLabel = typeLabels[pageType] || pageType;
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": title, "description": description }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="mb-8 flex items-center gap-4"> <a href=".." class="text-sm text-kernel-500 hover:text-kernel-300">← Back to ${domain || "domain"}</a> ${typeLabel && renderTemplate`<span class="text-xs font-mono px-2 py-0.5 rounded bg-kernel-800 text-kernel-400 border border-kernel-700"> ${typeLabel} </span>`} </div> <article class="prose prose-invert prose-sm max-w-none
    prose-headings:font-bold prose-headings:tracking-tight
    prose-h2:text-xl prose-h2:mt-10 prose-h2:mb-4 prose-h2:border-b prose-h2:border-kernel-800 prose-h2:pb-2
    prose-h3:text-lg
    prose-table:text-sm
    prose-th:text-left prose-th:text-kernel-400 prose-th:font-normal prose-th:border-b prose-th:border-kernel-700 prose-th:py-2
    prose-td:py-2 prose-td:border-b prose-td:border-kernel-800
    prose-code:text-kernel-300 prose-code:bg-kernel-800 prose-code:px-1 prose-code:rounded
    prose-strong:text-kernel-100
    prose-blockquote:border-kernel-700 prose-blockquote:text-kernel-400
    prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline
    prose-li:marker:text-kernel-600"> ${renderSlot($$result2, $$slots["default"])} </article> ` })}`;
}, "/home/runner/work/GENERATIVE-COLLAPSE-DYNAMICS/GENERATIVE-COLLAPSE-DYNAMICS/web/src/layouts/SubpageLayout.astro", void 0);

export { $$SubpageLayout as $ };
