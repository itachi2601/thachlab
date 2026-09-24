/**
 * Đọc `body_html` lưu trong LMS (HTML do latex-converter.ts sinh ra, công thức
 * để trần dạng `$...$`/`$$...$$` — xem services/latex-converter.ts) thành một
 * cây khối/dòng đơn giản, dùng chung cho cả hai chiều xuất ngược: html-to-latex.ts
 * và docx-writer.ts. Gom một chỗ để hai bên khỏi mỗi nơi tự viết một bộ walk DOM.
 *
 * Chạy ở trình duyệt (web xuất tĩnh, không có server) nên dùng thẳng DOMParser.
 */

export interface TextInline {
  k: "text";
  v: string;
}
export interface MathInline {
  k: "math";
  latex: string; // không kèm dấu $
  display: boolean;
}
export interface MarkInline {
  k: "bold" | "italic" | "underline" | "code";
  children: Inline[];
}
export interface BreakInline {
  k: "br";
}
export type Inline = TextInline | MathInline | MarkInline | BreakInline;

export interface HeadingBlock {
  k: "heading";
  level: 2 | 3 | 4;
  children: Inline[];
}
export interface ParaBlock {
  k: "para";
  children: Inline[];
}
export interface CaptionBlock {
  k: "caption";
  children: Inline[];
}
export interface ListBlock {
  k: "list";
  ordered: boolean;
  items: Inline[][];
}
export interface TableCell {
  children: Inline[];
  colspan: number;
  header: boolean;
}
export interface TableRow {
  cells: TableCell[];
}
export interface TableBlock {
  k: "table";
  rows: TableRow[];
}
export interface ImageBlock {
  k: "image";
  src: string;
  alt: string;
}
export type Block = HeadingBlock | ParaBlock | CaptionBlock | ListBlock | TableBlock | ImageBlock;

function requireDom(): void {
  if (typeof DOMParser === "undefined")
    throw new Error("Tính năng này cần chạy trong trình duyệt (không có DOMParser).");
}

/** Tách văn bản có công thức trần `$...$` / `$$...$$` thành Inline[] (giống regex trong ContentHtml.tsx). */
function textToInlines(text: string): Inline[] {
  if (!text) return [];
  if (!text.includes("$")) return [{ k: "text", v: text }];
  const out: Inline[] = [];
  const re = /\$\$([^$]+)\$\$|\$([^$]+)\$/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push({ k: "text", v: text.slice(last, m.index) });
    const display = m[1] !== undefined;
    out.push({ k: "math", latex: (m[1] ?? m[2] ?? "").trim(), display });
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push({ k: "text", v: text.slice(last) });
  return out;
}

const TRANSPARENT_INLINE = new Set(["SPAN", "A", "SUP", "SUB"]); // bỏ qua thẻ, chỉ lấy nội dung con

function parseInlineNode(node: ChildNode, out: Inline[]): void {
  if (node.nodeType === Node.TEXT_NODE) {
    out.push(...textToInlines(node.textContent ?? ""));
    return;
  }
  if (node.nodeType !== Node.ELEMENT_NODE) return;
  const el = node as Element;
  const tag = el.tagName;
  if (tag === "BR") {
    out.push({ k: "br" });
    return;
  }
  if (tag === "STRONG" || tag === "B") {
    out.push({ k: "bold", children: parseInlineChildren(el) });
    return;
  }
  if (tag === "EM" || tag === "I") {
    out.push({ k: "italic", children: parseInlineChildren(el) });
    return;
  }
  if (tag === "U") {
    out.push({ k: "underline", children: parseInlineChildren(el) });
    return;
  }
  if (tag === "CODE") {
    out.push({ k: "code", children: parseInlineChildren(el) });
    return;
  }
  if (tag === "P" || tag === "DIV") {
    // Đoạn/khung lồng bên trong 1 ô/dòng (thường gặp trong <li> dán từ Word) —
    // coi như xuống dòng rồi gộp tiếp, khỏi vỡ cấu trúc khối cha.
    if (out.length) out.push({ k: "br" });
    out.push(...parseInlineChildren(el));
    return;
  }
  if (TRANSPARENT_INLINE.has(tag)) {
    out.push(...parseInlineChildren(el));
    return;
  }
  // Thẻ lạ: lấy text thô, còn hơn mất nội dung.
  out.push(...textToInlines(el.textContent ?? ""));
}

function parseInlineChildren(el: Element): Inline[] {
  const out: Inline[] = [];
  el.childNodes.forEach((n) => parseInlineNode(n, out));
  return out;
}

function cellColspan(el: Element): number {
  const v = parseInt(el.getAttribute("colspan") ?? "1", 10);
  return Number.isFinite(v) && v > 0 ? v : 1;
}

function parseTable(tableEl: Element): TableBlock {
  const rows: TableRow[] = [];
  tableEl.querySelectorAll("tr").forEach((tr) => {
    const cells: TableCell[] = [];
    tr.querySelectorAll("th,td").forEach((cell) => {
      cells.push({
        children: parseInlineChildren(cell),
        colspan: cellColspan(cell),
        header: cell.tagName === "TH",
      });
    });
    rows.push({ cells });
  });
  return { k: "table", rows };
}

function parseBlockEl(el: Element, out: Block[]): void {
  const tag = el.tagName;
  if (tag === "H1" || tag === "H2" || tag === "H3" || tag === "H4") {
    const level = (tag === "H1" ? 2 : Number(tag[1])) as 2 | 3 | 4;
    out.push({ k: "heading", level, children: parseInlineChildren(el) });
    return;
  }
  if (tag === "P") {
    const children = parseInlineChildren(el);
    if (children.length === 0) return; // đoạn rỗng (thường do dọn HTML) — bỏ qua
    if (el.classList.contains("lc-caption")) out.push({ k: "caption", children });
    else out.push({ k: "para", children });
    return;
  }
  if (tag === "UL" || tag === "OL") {
    const items: Inline[][] = [];
    el.querySelectorAll(":scope > li").forEach((li) => items.push(parseInlineChildren(li)));
    if (items.length) out.push({ k: "list", ordered: tag === "OL", items });
    return;
  }
  if (tag === "TABLE") {
    out.push(parseTable(el));
    return;
  }
  if (tag === "IMG") {
    out.push({ k: "image", src: el.getAttribute("src") ?? "", alt: el.getAttribute("alt") ?? "" });
    return;
  }
  if (tag === "DIV") {
    // Khung bọc (vd overflow-x-auto quanh table, hoặc div.table-scroll của ContentHtml) — xuyên qua.
    const nestedTable = el.querySelector(":scope > table");
    if (nestedTable) {
      out.push(parseTable(nestedTable));
      return;
    }
    parseBlocks(el, out);
    return;
  }
  if (tag === "SPAN" || tag === "A") {
    const children = parseInlineChildren(el);
    if (children.length) out.push({ k: "para", children });
    return;
  }
  // Text/thẻ lạ ở cấp khối: gói vào 1 đoạn văn cho khỏi mất nội dung.
  const children = parseInlineChildren(el);
  if (children.length) out.push({ k: "para", children });
}

function parseBlocks(root: Element, out: Block[]): void {
  root.childNodes.forEach((node) => {
    if (node.nodeType === Node.ELEMENT_NODE) {
      parseBlockEl(node as Element, out);
    } else if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent ?? "";
      if (text.trim()) out.push({ k: "para", children: textToInlines(text) });
    }
  });
}

/** body_html (đúng dạng lưu trong lesson_items / worked_examples) → cây khối. */
export function parseHtmlToBlocks(html: string): Block[] {
  requireDom();
  const doc = new DOMParser().parseFromString(`<div id="root">${html}</div>`, "text/html");
  const root = doc.getElementById("root");
  const out: Block[] = [];
  if (root) parseBlocks(root, out);
  return out;
}
