/**
 * AZOTA iframe formatting utility
 * Helps embed AZOTA exercises with proper styling and metadata
 */

export interface AzotaEmbedOptions {
  src: string;
  title?: string;
  height?: number;
}

/**
 * Extract and validate AZOTA iframe code
 */
export function parseAzotaIframe(iframeCode: string): AzotaEmbedOptions {
  const srcMatch = iframeCode.match(/src=["']([^"']+)["']/);
  const titleMatch = iframeCode.match(/title=["']([^"']+)["']/);

  if (!srcMatch) {
    throw new Error("Không tìm thấy src trong iframe code");
  }

  const src = srcMatch[1];

  // Validate AZOTA URL
  if (!src.includes("azota.vn")) {
    throw new Error("URL phải từ azota.vn");
  }

  return {
    src,
    title: titleMatch?.[1] || "AZOTA Exercise",
    height: 900,
  };
}

/**
 * Format AZOTA embed as responsive HTML
 */
export function formatAzotaEmbed(options: AzotaEmbedOptions): string {
  return `<div class="azota-embed w-full bg-white rounded-lg overflow-hidden border border-slate-200" data-src="${options.src}" style="max-width: 100%;">
  <iframe
    width="100%"
    height="${options.height || 900}"
    src="${options.src}"
    title="${options.title}"
    frameborder="0"
    allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"
    allowfullscreen
    style="display: block; border: none; min-height: 600px;">
  </iframe>
</div>`;
}

/**
 * Extract AZOTA embed from HTML
 */
export function extractAzotaEmbed(html: string): AzotaEmbedOptions | null {
  const azotaDiv = html.match(/<div class="azota-embed[^>]*data-src="([^"]+)"/);
  if (!azotaDiv) return null;

  const titleMatch = html.match(/title="([^"]+)"/);
  return {
    src: azotaDiv[1],
    title: titleMatch?.[1] || "AZOTA Exercise",
  };
}

/**
 * Check if HTML contains AZOTA embed
 */
export function hasAzotaEmbed(html: string): boolean {
  return html.includes('class="azota-embed');
}
