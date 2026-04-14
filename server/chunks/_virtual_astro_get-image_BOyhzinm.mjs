import { g as getImage$1 } from './deterministic-string_CxFaRE72.mjs';
import '@astrojs/internal-helpers/remote';
import '@astrojs/internal-helpers/path';

const imageConfig = {"endpoint":{"route":"/_image","entrypoint":"astro/assets/endpoint/node"},"service":{"entrypoint":"astro/assets/services/sharp","config":{}},"domains":[],"remotePatterns":[],"responsiveStyles":false};
								Object.defineProperty(imageConfig, 'assetQueryParams', {
									value: undefined,
									enumerable: false,
									configurable: true,
								});
								const getImage = async (options) => await getImage$1(options, imageConfig);

export { getImage, imageConfig };
