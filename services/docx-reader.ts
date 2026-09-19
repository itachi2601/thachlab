/**
 * Đọc file Word (.docx) ngay trong trình duyệt → văn bản thuần + công thức $...$
 * + ảnh nhúng, để trang /quan-tri/nhap-bai dựng đề mà không cần trợ lý.
 *
 * Giới hạn đã biết (đều được báo lại cho người dùng, không im lặng):
 *  - Công thức MathType còn ở dạng OLE là ảnh WMF → không đọc được, chèn mốc ⟦CT⟧.
 *    Cách xử lý: trong Word bấm MathType → Convert Equations → Microsoft Office Math.
 *  - Đánh số tự động của Word (numbering) không nằm trong văn bản → "Câu 1." biến mất.
 */

import { unzip } from "@/services/docx-zip";
import { ommlToLatex } from "@/services/omml-to-latex";
import type { RasterImageInput } from "@/services/lesson-media";

/** Mốc đánh dấu một công thức MathType chưa chuyển sang Office Math. */
export const MATH_MARK = "⟦CT⟧";
/** Mốc đánh dấu ảnh định dạng WMF/EMF (trình duyệt không hiển thị được). */
export const VECTOR_IMAGE_MARK = "⟦ảnh WMF⟧";

export interface DocxReadResult {
  /** Văn bản thuần: mỗi đoạn một dòng, ô bảng ngăn bằng tab, công thức ở dạng $...$ */
  text: string;
  images: RasterImageInput[];
  /** Số công thức MathType chưa chuyển sang Office Math. */
  mathTypeCount: number;
  /** Số công thức Office Math đọc được. */
  ommlCount: number;
  warnings: string[];
}

const RASTER_MIME: Record<string, string> = {
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  gif: "image/gif",
  webp: "image/webp",
  bmp: "image/bmp",
};

interface Ctx {
  rels: Map<string, string>;
  files: Map<string, Uint8Array>;
  images: RasterImageInput[];
  byRelId: Map<string, string>;
  mathTypeCount: number;
  ommlCount: number;
  vectorImages: number;
  autoNumbered: number;
  missingMedia: number;
}

function els(parent: Element): Element[] {
  return Array.from(parent.children);
}

function child(parent: Element, name: string): Element | null {
  return els(parent).find((e) => e.localName === name) ?? null;
}

function attr(el: Element, local: string): string | null {
  for (const a of Array.from(el.attributes)) if (a.localName === local) return a.value;
  return null;
}

function descendant(el: Element, name: string): Element | null {
  for (const c of els(el)) {
    if (c.localName === name) return c;
    const deep = descendant(c, name);
    if (deep) return deep;
  }
  return null;
}

function parseXml(bytes: Uint8Array, label: string): Document {
  const xml = new TextDecoder("utf-8").decode(bytes);
  const doc = new DOMParser().parseFromString(xml, "application/xml");
  if (doc.querySelector("parsererror")) throw new Error(`Không đọc được ${label} trong file .docx.`);
  return doc;
}

function toDataUri(bytes: Uint8Array, mime: string): string {
  let binary = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
  }
  return `data:${mime};base64,${btoa(binary)}`;
}

/** rId → đường dẫn trong zip (vd "word/media/image3.png"). */
function relTarget(ctx: Ctx, relId: string): string | null {
  const target = ctx.rels.get(relId);
  if (!target || /^https?:/i.test(target)) return null;
  const clean = target.replace(/^\/+/, "").replace(/^\.\.\//, "");
  return ctx.files.has(`word/${clean}`) ? `word/${clean}` : ctx.files.has(clean) ? clean : null;
}

/** Ảnh nhúng → thẻ <img> trỏ tới placeholder media/… (trang sẽ tự upload lên Storage). */
function imageTag(ctx: Ctx, relId: string): string {
  const known = ctx.byRelId.get(relId);
  if (known) return known;

  const path = relTarget(ctx, relId);
  if (!path) {
    ctx.missingMedia += 1;
    return "";
  }
  const ext = (path.split(".").pop() ?? "").toLowerCase();
  const mime = RASTER_MIME[ext];
  if (!mime) {
    ctx.vectorImages += 1;
    return ` ${VECTOR_IMAGE_MARK} `;
  }
  const bytes = ctx.files.get(path);
  if (!bytes) {
    ctx.missingMedia += 1;
    return "";
  }
  const n = ctx.images.length + 1;
  const name = `hinh-${n}.${ext === "jpeg" ? "jpg" : ext}`;
  const placeholder = `media/${name}`;
  ctx.images.push({ name, dataUri: toDataUri(bytes, mime), placeholder });
  const tag = `<img src="${placeholder}" alt="Hình ${n}" class="mx-auto my-2 max-w-full rounded-lg" />`;
  ctx.byRelId.set(relId, tag);
  return tag;
}

function objectText(el: Element, ctx: Ctx): string {
  const ole = descendant(el, "OLEObject");
  const progId = ole ? (attr(ole, "ProgID") ?? "") : "";
  if (/Equation|MathType/i.test(progId)) {
    ctx.mathTypeCount += 1;
    return ` ${MATH_MARK} `;
  }
  const imagedata = descendant(el, "imagedata");
  const relId = imagedata ? attr(imagedata, "id") : null;
  return relId ? imageTag(ctx, relId) : "";
}

function inlineText(node: Element, ctx: Ctx): string {
  let out = "";
  for (const el of els(node)) {
    switch (el.localName) {
      case "oMath":
        ctx.ommlCount += 1;
        out += ` $${ommlToLatex(el)}$ `;
        break;
      case "t":
        out += el.textContent ?? "";
        break;
      case "tab":
        out += "\t";
        break;
      case "br":
      case "cr":
        out += "\n";
        break;
      case "object":
        out += objectText(el, ctx);
        break;
      case "drawing":
      case "pict": {
        const blip = descendant(el, "blip");
        const relId = blip ? attr(blip, "embed") : null;
        if (relId) {
          out += imageTag(ctx, relId);
          break;
        }
        out += objectText(el, ctx);
        break;
      }
      case "AlternateContent": {
        // mc:Choice và mc:Fallback là hai bản của cùng một nội dung — chỉ lấy một.
        const choice = child(el, "Choice") ?? child(el, "Fallback");
        if (choice) out += inlineText(choice, ctx);
        break;
      }
      case "delText": // văn bản đã xóa (theo dõi thay đổi)
      case "instrText":
      case "rPr":
      case "pPr":
      case "sectPr":
        break;
      default:
        out += inlineText(el, ctx);
    }
  }
  return out;
}

function paragraphText(p: Element, ctx: Ctx): string {
  const pPr = child(p, "pPr");
  if (pPr && child(pPr, "numPr")) ctx.autoNumbered += 1;
  return inlineText(p, ctx);
}

function blockText(el: Element, ctx: Ctx): string {
  switch (el.localName) {
    case "p":
      return `${paragraphText(el, ctx)}\n`;
    case "tbl":
      return els(el)
        .filter((r) => r.localName === "tr")
        .map(
          (row) =>
            `${els(row)
              .filter((c) => c.localName === "tc")
              .map((cell) =>
                els(cell)
                  .map((b) => blockText(b, ctx))
                  .join(" ")
                  .replace(/\s*\n\s*/g, " ")
                  .trim(),
              )
              .join("\t")}\n`,
        )
        .join("");
    case "sdt": {
      const content = child(el, "sdtContent");
      return content ? els(content).map((b) => blockText(b, ctx)).join("") : "";
    }
    case "sectPr":
    case "bookmarkStart":
    case "bookmarkEnd":
      return "";
    default:
      return els(el).map((b) => blockText(b, ctx)).join("");
  }
}

export async function readDocx(input: ArrayBuffer | Uint8Array): Promise<DocxReadResult> {
  const bytes = input instanceof Uint8Array ? input : new Uint8Array(input);
  const files = await unzip(bytes);
  const documentXml = files.get("word/document.xml");
  if (!documentXml)
    throw new Error("Không thấy word/document.xml — file này không phải .docx (nếu là .doc cũ, hãy Lưu thành .docx).");

  const rels = new Map<string, string>();
  const relsXml = files.get("word/_rels/document.xml.rels");
  if (relsXml) {
    for (const r of Array.from(parseXml(relsXml, "danh sách liên kết").getElementsByTagName("*"))) {
      if (r.localName !== "Relationship") continue;
      const id = attr(r, "Id");
      const target = attr(r, "Target");
      if (id && target) rels.set(id, target);
    }
  }

  const ctx: Ctx = {
    rels,
    files,
    images: [],
    byRelId: new Map(),
    mathTypeCount: 0,
    ommlCount: 0,
    vectorImages: 0,
    autoNumbered: 0,
    missingMedia: 0,
  };

  const doc = parseXml(documentXml, "nội dung");
  const body = els(doc.documentElement).find((e) => e.localName === "body") ?? null;
  if (!body) throw new Error("File .docx rỗng hoặc hỏng (không thấy phần thân).");

  const text = els(body)
    .map((b) => blockText(b, ctx))
    .join("")
    .replace(/\r\n?/g, "\n")
    .replace(/ /g, " ")
    .replace(/­/g, "")
    .replace(/[ \t]+$/gm, "")
    .replace(/\n{3,}/g, "\n\n");

  const warnings: string[] = [];
  if (ctx.mathTypeCount > 0)
    warnings.push(
      `Còn ${ctx.mathTypeCount} công thức MathType chưa chuyển — chỗ đó hiện là "${MATH_MARK}". ` +
        `Trong Word: tab MathType → Convert Equations → chọn "Microsoft Office Math" → OK, lưu lại rồi tải lên lần nữa.`,
    );
  if (ctx.vectorImages > 0)
    warnings.push(
      `Có ${ctx.vectorImages} ảnh dạng WMF/EMF — web không hiển thị được, chỗ đó là "${VECTOR_IMAGE_MARK}". ` +
        `Trong Word: chuột phải ảnh → Save as Picture → PNG rồi chèn lại.`,
    );
  if (ctx.autoNumbered > 0)
    warnings.push(
      `Có ${ctx.autoNumbered} đoạn dùng đánh số tự động của Word — số thứ tự không nằm trong văn bản. ` +
        `Nếu thiếu câu, bôi đen cả đề → chuột phải → Bullets and Numbering → bỏ đánh số tự động (gõ số bằng tay).`,
    );
  if (ctx.missingMedia > 0) warnings.push(`Có ${ctx.missingMedia} ảnh liên kết ngoài file — đã bỏ qua.`);

  return {
    text,
    images: ctx.images,
    mathTypeCount: ctx.mathTypeCount,
    ommlCount: ctx.ommlCount,
    warnings,
  };
}
