/**
 * Dựng file .docx (OOXML tối thiểu, đủ để Word/LibreOffice mở được) từ cây khối
 * html-doc-model.ts — dùng để "tải bài học về Word". Công thức toán chuyển qua
 * latex-to-omml.ts thành công thức gốc của Word (không phải ảnh chụp).
 *
 * Không dựng numbering.xml (danh sách có số/dấu đầu dòng thật) cho gọn — danh
 * sách xuất ra bằng số/dấu • gõ tay kèm thụt lề, hiển thị giống hệt, chỉ là
 * không phải numbering tự động của Word.
 */

import type { Block, CaptionBlock, Inline, TableBlock } from "./html-doc-model";
import { latexToOmml } from "./latex-to-omml";
import { zip, type ZipInputEntry } from "./docx-zip";

const MAX_IMAGE_WIDTH_PX = 600;
const EMU_PER_PX = 9525;

function escapeXml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

interface RunMarks {
  bold?: boolean;
  italic?: boolean;
  underline?: boolean;
  code?: boolean;
}

function textRun(text: string, marks: RunMarks): string {
  if (text === "") return "";
  const rPr: string[] = [];
  if (marks.bold) rPr.push("<w:b/>");
  if (marks.italic) rPr.push("<w:i/>");
  if (marks.underline) rPr.push('<w:u w:val="single"/>');
  if (marks.code) rPr.push('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>');
  const rPrXml = rPr.length ? `<w:rPr>${rPr.join("")}</w:rPr>` : "";
  const lines = text.split("\n");
  const body = lines
    .map((line, i) => `${i > 0 ? "<w:br/>" : ""}<w:t xml:space="preserve">${escapeXml(line)}</w:t>`)
    .join("");
  return `<w:r>${rPrXml}${body}</w:r>`;
}

function inlineXml(n: Inline, marks: RunMarks): string {
  switch (n.k) {
    case "text":
      return textRun(n.v, marks);
    case "br":
      return "<w:r><w:br/></w:r>";
    case "math": {
      const omml = latexToOmml(n.latex);
      return n.display ? `<m:oMathPara><m:oMath>${omml}</m:oMath></m:oMathPara>` : `<m:oMath>${omml}</m:oMath>`;
    }
    case "bold":
      return runsXml(n.children, { ...marks, bold: true });
    case "italic":
      return runsXml(n.children, { ...marks, italic: true });
    case "underline":
      return runsXml(n.children, { ...marks, underline: true });
    case "code":
      return runsXml(n.children, { ...marks, code: true });
  }
}

function runsXml(inlines: Inline[], marks: RunMarks): string {
  return inlines.map((n) => inlineXml(n, marks)).join("");
}

// ---------- Ảnh: tải bytes, đo kích thước, gán quan hệ rId ----------

interface EmbeddedImage {
  relId: string;
  fileName: string;
  bytes: Uint8Array;
  widthEmu: number;
  heightEmu: number;
  contentType: string;
}

function extAndTypeFromUrl(url: string, headerType: string | null): { ext: string; type: string } {
  const known: Record<string, string> = {
    png: "image/png",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    gif: "image/gif",
    webp: "image/webp",
    bmp: "image/bmp",
    svg: "image/svg+xml",
  };
  const path = url.split(/[?#]/)[0];
  const m = /\.([a-zA-Z0-9]+)$/.exec(path);
  const extFromUrl = m ? m[1].toLowerCase() : "";
  if (extFromUrl in known) return { ext: extFromUrl, type: known[extFromUrl] };
  if (headerType) {
    for (const [ext, type] of Object.entries(known)) if (headerType.includes(type)) return { ext, type };
  }
  return { ext: "png", type: "image/png" };
}

async function loadImageDims(bytes: Uint8Array): Promise<{ w: number; h: number }> {
  try {
    const bitmap = await createImageBitmap(new Blob([bytes as BlobPart]));
    const dims = { w: bitmap.width, h: bitmap.height };
    bitmap.close();
    return dims;
  } catch {
    return { w: MAX_IMAGE_WIDTH_PX, h: Math.round(MAX_IMAGE_WIDTH_PX * 0.6) };
  }
}

/** Tải trước mọi ảnh xuất hiện trong tài liệu (bỏ qua ảnh nào lỗi mạng/CORS — không chặn xuất file). */
async function prepareImages(blocks: Block[]): Promise<Map<string, EmbeddedImage>> {
  const map = new Map<string, EmbeddedImage>();
  let idx = 0;
  for (const b of blocks) {
    if (b.k !== "image" || !b.src || map.has(b.src)) continue;
    idx++;
    try {
      const res = await fetch(b.src);
      if (!res.ok) continue;
      const bytes = new Uint8Array(await res.arrayBuffer());
      const { ext, type } = extAndTypeFromUrl(b.src, res.headers.get("content-type"));
      const { w, h } = await loadImageDims(bytes);
      const scale = Math.min(1, MAX_IMAGE_WIDTH_PX / w);
      map.set(b.src, {
        relId: `rId${idx + 1}`, // rId1 = styles.xml
        fileName: `image${idx}.${ext}`,
        bytes,
        widthEmu: Math.round(w * scale * EMU_PER_PX),
        heightEmu: Math.round(h * scale * EMU_PER_PX),
        contentType: type,
      });
    } catch {
      // Ảnh không tải được (mạng/CORS) — đoạn văn vẫn xuất, chỉ thiếu ảnh đó.
    }
  }
  return map;
}

function imageParagraphXml(img: EmbeddedImage, docPrId: number): string {
  return (
    `<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>` +
    `<wp:inline distT="0" distB="0" distL="0" distR="0">` +
    `<wp:extent cx="${img.widthEmu}" cy="${img.heightEmu}"/>` +
    `<wp:docPr id="${docPrId}" name="Picture ${docPrId}"/>` +
    `<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">` +
    `<pic:pic><pic:nvPicPr><pic:cNvPr id="${docPrId}" name="Picture ${docPrId}"/><pic:cNvPicPr/></pic:nvPicPr>` +
    `<pic:blipFill><a:blip r:embed="${img.relId}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>` +
    `<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${img.widthEmu}" cy="${img.heightEmu}"/></a:xfrm>` +
    `<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>` +
    `</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>`
  );
}

function captionParagraphXml(children: Inline[]): string {
  return `<w:p><w:pPr><w:jc w:val="center"/><w:rPr><w:i/><w:sz w:val="20"/></w:rPr></w:pPr>${runsXml(children, { italic: true })}</w:p>`;
}

// ---------- Khối văn bản khác ----------

function listItemXml(item: Inline[], ordered: boolean, index: number): string {
  const marker = ordered ? `${index + 1}.` : "•";
  return (
    `<w:p><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>` +
    `<w:r><w:t xml:space="preserve">${marker}\t</w:t></w:r>${runsXml(item, {})}</w:p>`
  );
}

function tableXml(b: TableBlock): string {
  const nCols = Math.max(1, ...b.rows.map((r) => r.cells.reduce((n, c) => n + c.colspan, 0)));
  const colW = Math.floor(9026 / nCols);
  const grid = Array.from({ length: nCols }, () => `<w:gridCol w:w="${colW}"/>`).join("");
  const borders =
    '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="999999"/><w:left w:val="single" w:sz="4" w:color="999999"/>' +
    '<w:bottom w:val="single" w:sz="4" w:color="999999"/><w:right w:val="single" w:sz="4" w:color="999999"/>' +
    '<w:insideH w:val="single" w:sz="4" w:color="999999"/><w:insideV w:val="single" w:sz="4" w:color="999999"/></w:tblBorders>';
  const rows = b.rows
    .map((row) => {
      const cells = row.cells
        .map((c) => {
          const span = c.colspan > 1 ? `<w:gridSpan w:val="${c.colspan}"/>` : "";
          const shade = c.header ? '<w:shd w:val="clear" w:fill="E5E7EB"/>' : "";
          return `<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/>${span}${shade}</w:tcPr><w:p>${runsXml(c.children, c.header ? { bold: true } : {})}</w:p></w:tc>`;
        })
        .join("");
      return `<w:tr>${cells}</w:tr>`;
    })
    .join("");
  return `<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>${borders}</w:tblPr><w:tblGrid>${grid}</w:tblGrid>${rows}</w:tbl>`;
}

function headingStyle(level: 2 | 3 | 4): string {
  return level === 2 ? "Heading1" : level === 3 ? "Heading2" : "Heading3";
}

// ---------- Lắp tài liệu ----------

const DOCUMENT_HEADER =
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  "<w:document " +
  'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" ' +
  'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" ' +
  'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ' +
  'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" ' +
  'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" ' +
  'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">' +
  "<w:body>";

const SECT_PR =
  '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>' +
  '<w:pgMar w:top="1417" w:right="1133" w:bottom="1417" w:left="1133" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>';

const DOCUMENT_FOOTER = "</w:body></w:document>";

const STYLES_XML =
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
  '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="24"/></w:rPr></w:rPrDefault></w:docDefaults>' +
  '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>' +
  '<w:pPr><w:spacing w:after="160" w:line="288" w:lineRule="auto"/></w:pPr></w:style>' +
  '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>' +
  '<w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr>' +
  '<w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1F2937"/></w:rPr></w:style>' +
  '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>' +
  '<w:pPr><w:spacing w:before="280" w:after="120"/></w:pPr>' +
  '<w:rPr><w:b/><w:sz w:val="30"/><w:color w:val="1D4ED8"/></w:rPr></w:style>' +
  '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>' +
  '<w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr>' +
  '<w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="1F2937"/></w:rPr></w:style>' +
  '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>' +
  '<w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr>' +
  '<w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="1F2937"/></w:rPr></w:style>' +
  "</w:styles>";

const ROOT_RELS =
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>' +
  "</Relationships>";

function buildDocumentRels(images: Map<string, EmbeddedImage>): string {
  const rels = [
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
  ];
  for (const img of images.values())
    rels.push(
      `<Relationship Id="${img.relId}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/${img.fileName}"/>`,
    );
  return (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    rels.join("") +
    "</Relationships>"
  );
}

const CONTENT_TYPE_EXT: Record<string, string> = {
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  gif: "image/gif",
  webp: "image/webp",
  bmp: "image/bmp",
  svg: "image/svg+xml",
};

function buildContentTypes(images: Map<string, EmbeddedImage>): string {
  const exts = new Set<string>();
  for (const img of images.values()) exts.add(img.fileName.split(".").pop() ?? "png");
  const defaults = Array.from(exts)
    .map((ext) => `<Default Extension="${ext}" ContentType="${CONTENT_TYPE_EXT[ext] ?? "image/png"}"/>`)
    .join("");
  return (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
    '<Default Extension="xml" ContentType="application/xml"/>' +
    defaults +
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>' +
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>' +
    "</Types>"
  );
}

/** title/subtitle in vào đầu tài liệu, rồi tới nội dung các khối. */
export async function buildLessonDocx(title: string, subtitle: string, blocks: Block[]): Promise<Uint8Array> {
  const images = await prepareImages(blocks);
  const body: string[] = [];
  body.push(`<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr>${textRun(title, {})}</w:p>`);
  if (subtitle.trim())
    body.push(
      `<w:p><w:pPr><w:jc w:val="center"/><w:rPr><w:i/><w:color w:val="6B7280"/></w:rPr></w:pPr>${textRun(subtitle, { italic: true })}</w:p>`,
    );

  let docPrId = 1;
  for (let i = 0; i < blocks.length; i++) {
    const b = blocks[i];
    if (b.k === "caption" && blocks[i - 1]?.k === "image") continue; // đã gộp vào ảnh đứng trước
    if (b.k === "image") {
      const img = images.get(b.src);
      const captionBlock = blocks[i + 1]?.k === "caption" ? (blocks[i + 1] as CaptionBlock) : null;
      if (img) {
        docPrId++;
        body.push(imageParagraphXml(img, docPrId));
        if (captionBlock) body.push(captionParagraphXml(captionBlock.children));
      } else {
        body.push(
          `<w:p><w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">[Không tải được hình minh hoạ — xem trực tiếp trên web: ${escapeXml(b.src)}]</w:t></w:r></w:p>`,
        );
      }
      continue;
    }
    if (b.k === "heading") {
      body.push(`<w:p><w:pPr><w:pStyle w:val="${headingStyle(b.level)}"/></w:pPr>${runsXml(b.children, {})}</w:p>`);
    } else if (b.k === "para") {
      body.push(`<w:p>${runsXml(b.children, {})}</w:p>`);
    } else if (b.k === "caption") {
      body.push(captionParagraphXml(b.children));
    } else if (b.k === "list") {
      body.push(b.items.map((it, idx) => listItemXml(it, b.ordered, idx)).join(""));
    } else if (b.k === "table") {
      body.push(tableXml(b));
    }
  }

  const documentXml = DOCUMENT_HEADER + body.join("") + SECT_PR + DOCUMENT_FOOTER;

  const entries: ZipInputEntry[] = [
    { name: "[Content_Types].xml", data: new TextEncoder().encode(buildContentTypes(images)) },
    { name: "_rels/.rels", data: new TextEncoder().encode(ROOT_RELS) },
    { name: "word/document.xml", data: new TextEncoder().encode(documentXml) },
    { name: "word/styles.xml", data: new TextEncoder().encode(STYLES_XML) },
    { name: "word/_rels/document.xml.rels", data: new TextEncoder().encode(buildDocumentRels(images)) },
  ];
  for (const img of images.values()) entries.push({ name: `word/media/${img.fileName}`, data: img.bytes });

  return zip(entries);
}
