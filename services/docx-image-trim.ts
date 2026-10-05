/**
 * Ảnh công thức/hình trong file Word thường được LibreOffice xuất thành PNG cả trang A4 (794×1123, nền trắng,
 * nội dung nhỏ ở giữa) còn kích thước thật chỉ nằm ở khung ảnh trong Word. Web không biết khung đó nên hiện
 * nguyên trang → mỗi ký hiệu thành một khối trắng cao ~1100px. Hàm này (chỉ chạy bằng Node, cần sharp) cắt sát
 * nội dung rồi đặt lại đúng cỡ theo khung Word; ảnh nhỏ (công thức) gắn class `eq` để nằm cùng dòng chữ.
 *
 * Cần `readDocx(..., { imageSizes: true })` — nếu không, thẻ <img> không có data-w/data-h và hàm này không làm gì.
 */
import sharp from "sharp";
import type { RasterImageInput } from "@/services/lesson-media";

const TAG_RE = /<img\b[^>]*?\bdata-w="[\d.]+"[^>]*?\/>/g;
/** Ảnh có khung ≤ ngưỡng này (px) là công thức nằm cùng dòng; lớn hơn là hình minh hoạ. */
const INLINE_MAX_H = 80;
const INLINE_MAX_W = 260;

export function isPageSizedPng(width: number, height: number): boolean {
  return width >= 700 && height >= 950;
}

export interface TrimStats {
  trimmed: number;
  skipped: number;
}

/** Cắt các ảnh cả-trang trong `images` (sửa tại chỗ) và trả bảng thay thẻ <img> theo placeholder. */
export async function trimPageImages(
  images: RasterImageInput[],
  usedText: string,
): Promise<{ rewrite: (s: string) => string; stats: TrimStats; finals: Map<string, { w: number; h: number }>; trimmedPlaceholders: Set<string> }> {
  const frames = new Map<string, { w: number; h: number }>();
  for (const m of usedText.replace(/\\"/g, '"').matchAll(/<img\b[^>]*?src="([^"]+)"[^>]*?data-w="([\d.]+)"[^>]*?data-h="([\d.]+)"/g)) {
    frames.set(m[1], { w: Number(m[2]), h: Number(m[3]) });
  }
  const final = new Map<string, { w: number; h: number }>();
  const stats: TrimStats = { trimmed: 0, skipped: 0 };
  const trimmedPlaceholders = new Set<string>();
  for (const im of images) {
    const frame = frames.get(im.placeholder);
    if (!frame) continue;
    const buf = Buffer.from(im.dataUri.slice(im.dataUri.indexOf(",") + 1), "base64");
    const meta = await sharp(buf).metadata();
    if (!isPageSizedPng(meta.width ?? 0, meta.height ?? 0)) {
      final.set(im.placeholder, frame);
      stats.skipped += 1;
      continue;
    }
    const flat = await sharp(buf).flatten({ background: "#ffffff" }).toBuffer();
    const { data, info } = await sharp(flat).trim({ background: "#ffffff", threshold: 12 }).png().toBuffer({ resolveWithObject: true });
    if (info.width < 2 || info.height < 2 || info.width >= (meta.width ?? 0) * 0.98) {
      final.set(im.placeholder, frame); // không có gì để cắt
      stats.skipped += 1;
      continue;
    }
    // nội dung phải nằm gọn trong khung Word → tỉ lệ co = min(khung/nội dung theo 2 chiều)
    const k = Math.min(frame.w / info.width, frame.h / info.height);
    final.set(im.placeholder, { w: info.width * k, h: info.height * k });
    im.dataUri = "data:image/png;base64," + data.toString("base64");
    im.name = im.name.replace(/\.[^.]+$/, "") + ".png";
    stats.trimmed += 1;
    trimmedPlaceholders.add(im.placeholder);
  }
  const rewrite = (s: string): string => s.replace(TAG_RE, rewriteTag);
  function rewriteTag(tag: string): string {
    const src = tag.match(/\bsrc="([^"]+)"/)?.[1] ?? "";
    const alt = tag.match(/\balt="([^"]*)"/)?.[1] ?? "Hình";
    const f = final.get(src);
    if (!f) return tag.replace(/\sdata-(?:w|h)="[\d.]+"/g, "");
    return buildImgTag(src, alt, f);
  }
  return { rewrite, stats, finals: final, trimmedPlaceholders };
}

/** Thẻ <img> cuối cùng: công thức nhỏ → `eq` cùng dòng chữ; hình lớn → khối giữa trang đúng cỡ Word. */
export function buildImgTag(src: string, alt: string, f: { w: number; h: number }): string {
  const w = Math.round(f.w * 10) / 10;
  const h = Math.round(f.h * 10) / 10;
  if (h <= INLINE_MAX_H && w <= INLINE_MAX_W) return `<img src="${src}" alt="${alt}" class="eq" style="width:${w}px;height:${h}px" />`;
  return `<img src="${src}" alt="${alt}" class="mx-auto my-2 max-w-full rounded-lg" style="width:${w}px;height:auto" />`;
}
