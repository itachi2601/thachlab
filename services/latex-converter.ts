/**
 * LaTeX → HTML Converter
 * Chuyển cấu trúc tài liệu LaTeX + công thức toán sang HTML cho LMS.
 *
 * Công thức toán được giữ nguyên ở dạng delimiter trần `$...$` / `$$...$$` —
 * đúng cái mà `components/exams/ContentHtml.tsx` mong đợi (nó tự regex tìm
 * `$...$` rồi gọi `katex.renderToString`). KHÔNG bọc `<span data-latex>` nữa.
 */

interface ConversionResult {
  html: string;
  latex: string; // Lưu LaTeX gốc
  mathCount: number;
}

// Ký tự NUL không có trong LaTeX nguồn và không bị regex nào đụng tới —
// dùng làm mốc giấu công thức / ký tự escape trong lúc convert.
const NUL = String.fromCharCode(0);
const mathRe = new RegExp(`${NUL}M(\\d+)${NUL}`, "g");
const escRe = new RegExp(`${NUL}E(\\d+)${NUL}`, "g");

/** Thay `\cmd{...}` (khớp ngoặc lồng nhau) bằng chuỗi do `render` trả về. */
function replaceBalanced(
  input: string,
  command: string,
  render: (inner: string) => string,
): string {
  const marker = `\\${command}{`;
  let out = "";
  let i = 0;
  while (i < input.length) {
    const at = input.indexOf(marker, i);
    if (at === -1) {
      out += input.slice(i);
      break;
    }
    out += input.slice(i, at);
    let depth = 1;
    let j = at + marker.length;
    for (; j < input.length && depth > 0; j++) {
      if (input[j] === "{") depth++;
      else if (input[j] === "}") depth--;
    }
    const inner = input.slice(at + marker.length, j - 1);
    out += render(inner);
    i = j;
  }
  return out;
}

export function latexToHtml(latexText: string, imageBase = ""): ConversionResult {
  let html = latexText;
  let mathCount = 0;
  const base = imageBase.trim().replace(/\/+$/, "");
  const maths: string[] = [];
  const escapes: string[] = [];

  // --- Bước 0: bỏ comment `%` (giữ `\%`) và dòng preamble hay gặp ---
  html = html.replace(/(^|[^\\])%.*$/gm, "$1");
  html = html.replace(/\\(documentclass|usepackage|newcommand|renewcommand|def)\b[^\n]*\n?/g, "");
  html = html.replace(/\\(?:begin|end)\{document\}/g, "");
  html = html.replace(/\\(maketitle|centering|noindent|par|small|large|Large|bigskip|medskip|smallskip)\b/g, "");

  // --- Bước 1: giấu ký tự escape ---
  html = html.replace(/\\([&%#_${}])/g, (_m, ch: string) => {
    const idx = escapes.push(ch === "&" ? "&amp;" : ch === "$" ? "&#36;" : ch) - 1;
    return `${NUL}E${idx}${NUL}`;
  });

  // --- Bước 2: tách vùng công thức, chuẩn hoá về `$...$` / `$$...$$` ---
  const stashMath = (raw: string, display: boolean) => {
    mathCount++;
    const body = raw.trim();
    const idx = maths.push(display ? `$$${body}$$` : `$${body}$`) - 1;
    return `${NUL}M${idx}${NUL}`;
  };
  html = html.replace(
    /\\begin\{(equation\*?|align\*?|gather\*?)\}([\s\S]*?)\\end\{\1\}/g,
    (_m, _env, body: string) => stashMath(body.replace(/\\label\{[^}]*\}/g, ""), true),
  );
  html = html.replace(/\$\$([\s\S]*?)\$\$/g, (_m, body: string) => stashMath(body, true));
  html = html.replace(/\\\[([\s\S]*?)\\\]/g, (_m, body: string) => stashMath(body, true));
  html = html.replace(/\\\(([\s\S]*?)\\\)/g, (_m, body: string) => stashMath(body, false));
  html = html.replace(/\$([^$\n]+?)\$/g, (_m, body: string) => stashMath(body, false));

  // --- Bước 3: escape ký tự HTML còn lại ---
  html = html
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // --- Bước 4: figure / caption / label ---
  html = html.replace(/\\begin\{figure\}(?:\[[^\]]*\])?/g, "").replace(/\\end\{figure\}/g, "");
  html = html.replace(/\\begin\{center\}/g, "").replace(/\\end\{center\}/g, "");
  html = replaceBalanced(html, "caption", (inner) => `\n<p class="lc-caption">${inner.trim()}</p>\n`);
  html = html.replace(/\\label\{[^}]*\}/g, "");
  html = html.replace(/\\(?:eq)?ref\{[^}]*\}/g, "");

  // --- Bước 5: heading ---
  html = replaceBalanced(html, "section*", (s) => `<h2>${s}</h2>`);
  html = replaceBalanced(html, "section", (s) => `<h2>${s}</h2>`);
  html = replaceBalanced(html, "subsection*", (s) => `<h3>${s}</h3>`);
  html = replaceBalanced(html, "subsection", (s) => `<h3>${s}</h3>`);
  html = replaceBalanced(html, "subsubsection*", (s) => `<h4>${s}</h4>`);
  html = replaceBalanced(html, "subsubsection", (s) => `<h4>${s}</h4>`);
  html = replaceBalanced(html, "paragraph", (s) => `<h4>${s}</h4>`);

  // --- Bước 6: \newline ---
  html = html.replace(/\\newline\s*/g, "<br />");

  // --- Bước 7: bảng \begin{tabular} -> <table> (bọc overflow-x-auto cho điện thoại) ---
  html = html.replace(
    /\\begin\{tabular\}\s*(?:\{[^}]*\})?([\s\S]*?)\\end\{tabular\}/g,
    (_m, body: string) => {
      const rows = body
        .split(/\\\\/)
        .map((r: string) => r.replace(/\\hline/g, "").trim())
        .filter((r: string) => r.length > 0);
      if (rows.length === 0) return "";
      const cellCls = "border border-white/10 p-2 align-top";
      const splitCells = (r: string): { text: string; span: number }[] =>
        r.split(/&amp;/).map((raw: string) => {
          const mc = raw.match(/\\multicolumn\{(\d+)\}\{[^}]*\}\{([\s\S]*?)\}\s*$/);
          return mc
            ? { text: mc[2].trim(), span: parseInt(mc[1], 10) || 1 }
            : { text: raw.trim(), span: 1 };
        });
      const head = splitCells(rows[0]);
      const thead =
        '<thead><tr class="bg-white/5">' +
        head
          .map(
            (c) =>
              `<th class="${cellCls} text-left font-bold"${c.span > 1 ? ` colspan="${c.span}"` : ""}>${c.text}</th>`,
          )
          .join("") +
        "</tr></thead>";
      const tbody =
        "<tbody>" +
        rows
          .slice(1)
          .map(
            (r: string) =>
              "<tr>" +
              splitCells(r)
                .map(
                  (c) =>
                    `<td class="${cellCls}"${c.span > 1 ? ` colspan="${c.span}"` : ""}>${c.text}</td>`,
                )
                .join("") +
              "</tr>",
          )
          .join("") +
        "</tbody>";
      const minw = Math.max(360, head.reduce((n, c) => n + c.span, 0) * 140);
      return (
        `<div class="my-3 overflow-x-auto"><table class="w-full border-collapse text-sm" ` +
        `style="min-width:${minw}px">${thead}${tbody}</table></div>`
      );
    },
  );

  // --- Bước 8: \includegraphics -> <img class="figure"> ---
  html = html.replace(
    /\\includegraphics\s*(?:\[[^\]]*\])?\{([^}]+)\}/g,
    (_m, pathRaw: string) => {
      const file = pathRaw.trim().replace(/^.*\//, "");
      const src = base ? `${base}/${file}` : file;
      return `<img class="figure" src="${src}" alt="Hình minh họa">`;
    },
  );

  // --- Bước 9: danh sách kiểu "+" đầu dòng ---
  html = html.replace(/(?:^|\n)((?:\+[ \t]*[^\n]+\n?)+)/g, (_m, blk: string) => {
    const items = blk
      .trim()
      .split(/\n/)
      .map((l) => l.replace(/^\+[ \t]*/, "").trim())
      .filter(Boolean);
    return `\n\n<ul>${items.map((t) => `<li>${t}</li>`).join("")}</ul>\n\n`;
  });

  // --- Bước 10: itemize / enumerate (xử lý theo block) ---
  const listBlock = (tag: "ul" | "ol") => (_m: string, body: string) => {
    const items = body
      .split(/\\item\s+/)
      .map((s) => s.trim().replace(/\n+/g, " "))
      .filter(Boolean);
    if (items.length === 0) return "";
    return `\n\n<${tag}>${items.map((t) => `<li>${t}</li>`).join("")}</${tag}>\n\n`;
  };
  html = html.replace(/\\begin\{itemize\}([\s\S]*?)\\end\{itemize\}/g, listBlock("ul"));
  html = html.replace(/\\begin\{enumerate\}([\s\S]*?)\\end\{enumerate\}/g, listBlock("ol"));
  html = html.replace(/\\item\s+/g, "<br />• "); // \item lạc ra ngoài môi trường

  // --- Bước 11: lệnh định dạng inline (khớp ngoặc lồng nhau) ---
  html = replaceBalanced(html, "textbf", (s) => `<strong>${s}</strong>`);
  html = replaceBalanced(html, "textit", (s) => `<em>${s}</em>`);
  html = replaceBalanced(html, "emph", (s) => `<em>${s}</em>`);
  html = replaceBalanced(html, "texttt", (s) => `<code>${s}</code>`);
  html = replaceBalanced(html, "underline", (s) => `<u>${s}</u>`);
  html = html.replace(/\\textcolor\{[^}]+\}/g, "");
  html = html.replace(/\\\\\s*/g, "<br />");

  // --- Bước 12: đoạn văn ---
  html = html.replace(/\n\n+/g, "</p><p>");
  html = "<p>" + html + "</p>";

  // --- Bước 13: dọn dẹp ---
  html = html.replace(/<p>\s*<\/p>/g, "");
  html = html.replace(/<p[^>]*>(?:\s|<br\s*\/?>)*<\/p>/g, "");
  html = html.replace(/<p>(<[hu][1-4]|<[ou]l|<ol)/g, "$1");
  html = html.replace(/(<\/[hu][1-4]>|<\/[ou]l>|<\/ol>)<\/p>/g, "$1");
  html = html.replace(/<p>\s*(<div|<table)/g, "$1");
  html = html.replace(/(<\/div>|<\/table>)\s*<\/p>/g, "$1");

  // --- Bước 14: gắn class Tailwind ---
  html = html.replace(/<h2>/g, '<h2 class="text-xl font-bold mt-3 mb-1.5">');
  html = html.replace(/<h3>/g, '<h3 class="text-lg font-semibold mt-2 mb-1">');
  html = html.replace(/<h4>/g, '<h4 class="font-semibold mt-2 mb-1">');
  html = html.replace(/<p>/g, '<p class="text-base leading-relaxed my-2">');
  html = html.replace(/<p class="lc-caption">/g, '<p class="my-1 text-sm text-slate-400 text-center">');
  html = html.replace(/<ul>/g, '<ul class="list-disc list-inside my-2 ml-4">');
  html = html.replace(/<ol>/g, '<ol class="list-decimal list-inside my-2 ml-4">');
  html = html.replace(/<li>/g, '<li class="my-1">');
  html = html.replace(/<strong>/g, '<strong class="font-bold">');
  html = html.replace(/<em>/g, '<em class="italic">');
  html = html.replace(/<code>/g, '<code class="bg-slate-200 text-slate-900 px-1 rounded font-mono text-sm">');

  // --- Bước 15: trả công thức + ký tự escape về ---
  html = html.replace(mathRe, (_m, i: string) => maths[+i] ?? "");
  html = html.replace(escRe, (_m, i: string) => escapes[+i] ?? "");

  return { html, latex: latexText, mathCount };
}

/**
 * Kiểm tra cú pháp LaTeX (mức cơ bản).
 */
export function validateLatexSyntax(latex: string): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  let braceCount = 0;
  for (const char of latex) {
    if (char === "{") braceCount++;
    if (char === "}") braceCount--;
    if (braceCount < 0) {
      errors.push("Dấu } không khớp với {");
      break;
    }
  }
  if (braceCount > 0) {
    errors.push("Thiếu dấu }");
  }

  const mathCount = (latex.match(/(?<!\\)\$/g) || []).length;
  if (mathCount % 2 !== 0) {
    errors.push("Thiếu dấu $ để đóng công thức");
  }

  const beginCount = (latex.match(/\\begin\{/g) || []).length;
  const endCount = (latex.match(/\\end\{/g) || []).length;
  if (beginCount !== endCount) {
    errors.push("Thiếu \\end để đóng \\begin");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
