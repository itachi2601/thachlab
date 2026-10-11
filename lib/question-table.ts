// Dựng bảng dữ liệu trong câu hỏi: ngân hàng lưu bảng ở 2 dạng không phải <table>
//  (1) các dòng cách nhau bằng <br>, ô cách nhau bằng ký tự TAB  →  trình duyệt gộp TAB thành 1 dấu cách nên dữ liệu dính nhau;
//  (2) mã LaTeX thô \begin{tabular}…\end{tabular}  →  hiện nguyên chuỗi ký tự.
// Thuần TypeScript (dùng được ở trình duyệt và script Node). Bảng dồn dòng KHÔNG có TAB thì không đoán ở đây —
// đã gom vào trang duyệt scripts/data/bang-ngan-hang/duyet.html.

const NUM = /^[\s$\-−–+]*\d[\d.,]*\s*(?:[^\s\d]{0,6})?[\s$]*$|^[-–−?=\s]+$|^[\s$]*[-−–]?\d+[\d.,]*[\s$]*(?:∘|°|\^\{?\\circ\}?)?\s*[A-Za-z]{0,2}\s*[\s$]*$/;

const esc = (s: string) => s;

function tableHtml(rows: string[][], opts: { headerRow?: boolean } = {}): string {
  const horizontal = rows.length >= 2 && rows[0].length > 1 && rows[0].slice(1).every((c) => NUM.test(c.replace(/<[^>]+>/g, "").trim()));
  const body = rows
    .map((cells, ri) => {
      const tr = cells
        .map((c, ci) => {
          const head = opts.headerRow ? ri === 0 : horizontal ? ci === 0 : ri === 0;
          return head ? `<th>${esc(c)}</th>` : `<td>${esc(c)}</td>`;
        })
        .join("");
      return `<tr>${tr}</tr>`;
    })
    .join("");
  return `<div class="q-table-wrap"><table class="q-table"><tbody>${body}</tbody></table></div>`;
}

/** Dòng có TAB cách nhau bằng <br> → <table>. Ít nhất 2 dòng liên tiếp, hoặc 1 dòng ≥3 ô. */
export function tabLinesToTable(html: string): string {
  if (!html.includes("\t")) return html;
  const parts = html.split(/<br\s*\/?>/i);
  const out: string[] = [];
  let i = 0;
  while (i < parts.length) {
    if (!parts[i].includes("\t")) { out.push(parts[i]); i++; continue; }
    let j = i;
    while (j < parts.length && parts[j].includes("\t")) j++;
    const grp = parts.slice(i, j);
    const rows = grp.map((l) => l.split("\t").map((c) => c.trim()));
    // dòng đầu có thể kèm chữ dẫn trước thẻ <p…> — giữ nguyên phần HTML đứng trước ô đầu
    const lead = (grp[0].match(/^(\s*(?:<[^>]+>\s*)+)/)?.[1] ?? "");
    if (lead) rows[0][0] = rows[0][0].slice(lead.length).trim();
    const wide = Math.max(...rows.map((r) => r.length));
    const ok = (grp.length >= 2 && wide >= 2) || wide >= 3;
    if (!ok) { out.push(...grp); i = j; continue; }
    out.push(lead + tableHtml(rows));
    i = j;
  }
  // <br> cạnh bảng thì bỏ (bảng tự là khối)
  return out.reduce((acc, seg, k) => {
    if (k === 0) return seg;
    const prevTable = out[k - 1].includes('class="q-table-wrap"');
    const thisTable = seg.includes('class="q-table-wrap"');
    return acc + (prevTable || thisTable ? "" : "<br>") + seg;
  }, "");
}

const unLatexCell = (c: string) =>
  c
    .replace(/\\newline/g, "<br>")
    .replace(/\\textit\{([^}]*)\}/g, "<i>$1</i>")
    .replace(/\\textbf\{([^}]*)\}/g, "<b>$1</b>")
    .replace(/\\%/g, "%")
    .trim();

/** \begin{tabular}{…} … \end{tabular} → <table>. */
export function tabularToTable(html: string): string {
  if (!html.includes("\\begin{tabular}")) return html;
  return html.replace(/\\begin\{tabular\}\{[^}]*\}([\s\S]*?)\\end\{tabular\}/g, (_m, body: string) => {
    const rows = body
      .replace(/\\hline/g, "")
      .split(/\\\\/)
      .map((r) => r.trim())
      .filter(Boolean)
      .map((r) => r.split("&").map(unLatexCell));
    if (!rows.length) return _m;
    const w = Math.max(...rows.map((r) => r.length));
    rows.forEach((r) => { while (r.length < w) r.push(""); });
    const isStrong = (c: string) => /^<strong>[\s\S]*<\/strong>/.test(c);
    return tableHtml(rows, { headerRow: rows[0].filter(Boolean).every(isStrong) });
  });
}

export function withQuestionTables(html: string): string {
  if (!html) return html;
  if (!html.includes("\t") && !html.includes("\\begin{tabular}")) return html;
  return tabLinesToTable(tabularToTable(html));
}
