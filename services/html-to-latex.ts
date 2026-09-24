/**
 * Chiều ngược của services/latex-converter.ts: từ cây khối html-doc-model.ts
 * (đọc được từ body_html lưu trong LMS) dựng lại văn bản LaTeX — để giáo viên
 * tải bài học xuống, sửa tiếp bằng trình soạn LaTeX quen thuộc.
 *
 * Công thức toán trong body_html vốn đã ở dạng LaTeX trần (`$...$`) nên chỉ
 * cần bọc lại dấu `$`, không phải đi qua OMML như chiều Word.
 */

import type { Block, Inline } from "./html-doc-model";
import { parseHtmlToBlocks } from "./html-doc-model";

export function escapeLatexText(s: string): string {
  return s
    .replace(/\\/g, "\\textbackslash{}")
    .replace(/([&%$#_{}])/g, "\\$1")
    .replace(/~/g, "\\textasciitilde{}")
    .replace(/\^/g, "\\textasciicircum{}");
}

function inlinesToLatex(inlines: Inline[]): string {
  return inlines.map(inlineToLatex).join("");
}

function inlineToLatex(n: Inline): string {
  switch (n.k) {
    case "text":
      return escapeLatexText(n.v);
    case "math":
      return n.display ? `$$${n.latex}$$` : `$${n.latex}$`;
    case "bold":
      return `\\textbf{${inlinesToLatex(n.children)}}`;
    case "italic":
      return `\\textit{${inlinesToLatex(n.children)}}`;
    case "underline":
      return `\\underline{${inlinesToLatex(n.children)}}`;
    case "code":
      return `\\texttt{${inlinesToLatex(n.children)}}`;
    case "br":
      return "\\newline\n";
  }
}

function imageFileName(src: string): string {
  const clean = src.split(/[?#]/)[0];
  const base = clean.split("/").pop() || "hinh.png";
  return base;
}

function blockToLatex(b: Block, next: Block | undefined): string | null {
  switch (b.k) {
    case "heading": {
      const cmd = b.level === 2 ? "section*" : b.level === 3 ? "subsection*" : "subsubsection*";
      return `\\${cmd}{${inlinesToLatex(b.children)}}`;
    }
    case "para":
      return inlinesToLatex(b.children);
    case "caption":
      // Caption đứng riêng (không ngay sau ảnh) — giữ làm đoạn văn thường, khỏi tạo figure rỗng.
      return inlinesToLatex(b.children);
    case "list": {
      const env = b.ordered ? "enumerate" : "itemize";
      const items = b.items.map((it) => `  \\item ${inlinesToLatex(it)}`).join("\n");
      return `\\begin{${env}}\n${items}\n\\end{${env}}`;
    }
    case "image": {
      const caption = next?.k === "caption" ? inlinesToLatex(next.children) : "";
      const file = imageFileName(b.src);
      const lines = [
        `% Hình gốc: ${b.src}`,
        "\\begin{figure}[h]",
        "\\centering",
        `\\includegraphics[width=0.75\\linewidth]{${file}}`,
      ];
      if (caption) lines.push(`\\caption{${caption}}`);
      lines.push("\\end{figure}");
      return lines.join("\n");
    }
    case "table": {
      const nCols = Math.max(1, ...b.rows.map((r) => r.cells.reduce((n, c) => n + c.colspan, 0)));
      const spec = "l".repeat(nCols);
      const rowLines = b.rows.map((row, i) => {
        const cells = row.cells.map((c) => {
          const text = inlinesToLatex(c.children);
          const body = c.header ? `\\textbf{${text}}` : text;
          return c.colspan > 1 ? `\\multicolumn{${c.colspan}}{l}{${body}}` : body;
        });
        const sep = i === 0 ? "\\hline\n" : "";
        return `${sep}${cells.join(" & ")} \\\\\n\\hline`;
      });
      return `\\begin{tabular}{${spec}}\n${rowLines.join("\n")}\n\\end{tabular}`;
    }
  }
}

export function blocksToLatex(blocks: Block[]): string {
  const out: string[] = [];
  for (let i = 0; i < blocks.length; i++) {
    const b = blocks[i];
    // Caption đã được gộp vào figure của ảnh đứng ngay trước — khỏi lặp lại.
    if (b.k === "caption" && blocks[i - 1]?.k === "image") continue;
    const s = blockToLatex(b, blocks[i + 1]);
    if (s !== null && s.trim()) out.push(s);
  }
  return out.join("\n\n");
}

/** body_html → LaTeX. */
export function htmlToLatex(html: string): string {
  return blocksToLatex(parseHtmlToBlocks(html));
}
