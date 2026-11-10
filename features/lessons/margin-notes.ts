/**
 * Cột lề phải của bài lý thuyết (thầy duyệt 27/10/2026, trang mẫu https://claude.ai/artifact/BXikspAiK5RZ9EteMUEc8C).
 *
 * Với mỗi đoạn `<p>` nằm ngay cấp đầu của thân bài, gom những thứ thuộc riêng đoạn đó vào một khối
 * `<div class="tl-sn">` đặt NGAY TRƯỚC đoạn:
 *   - chú thích số `<sup class="tl-fn"><a href="#tl-fn-N">N</a></sup>` → chép chữ của `<li id="tl-fn-N">` trong `<ol class="tl-fns">`;
 *   - thuật ngữ `<span class="tl-term">…<label>từ</label><span class="tl-def">định nghĩa</span></span>` → "từ — định nghĩa" (hiện sẵn);
 *   - ô "Số cần nhớ" `<div class="tl-nums">` đứng liền sau đoạn → chép nguyên các ô (vẫn che, bấm để hiện — L1).
 * Bản gốc giữ nguyên chỗ cũ và được đánh dấu (`tl-term--sn`, `tl-fn--placed`, `tl-nums--sn`) để CSS chọn đúng MỘT bản
 * hiện ở mỗi cỡ màn: ≥ 1280px khối lề float sang phần thẻ đã nới (globals.css, "CỘT LỀ PHẢI"), < 1280px khối lề ẩn và
 * mọi thứ như cũ (N8). Chỉ đọc chuỗi, không cần DOM nên chạy được cả lúc dựng trang tĩnh. Bài không có ba loại trên thì
 * trả nguyên chuỗi.
 */

/** Thẻ khối có thể lồng nhau — đếm để biết một `<p>` có nằm ở cấp đầu (không trong hộp, quiz, bảng…). */
const BLOCK_TAG = /<(\/?)(div|details|section|blockquote|figure|table|ul|ol|aside|p)\b[^>]*>/gi;
const FN_ITEM = /<li\b([^>]*)\bid="(tl-fn-[\w-]+)"([^>]*)>([\s\S]*?)<\/li>/g;
const FN_REF = /<sup class="tl-fn"[^>]*>\s*<a\b[^>]*\bhref="#(tl-fn-[\w-]+)"[^>]*>([^<]*)<\/a>\s*<\/sup>/g;

/** Gom thuật ngữ trong một đoạn (đếm lồng `<span>` — định nghĩa có thể chứa span con) và đánh dấu bản gốc. */
function collectTerms(para: string, notes: string[]): string {
  let out = "";
  let cursor = 0;
  for (let at = para.indexOf('<span class="tl-term">'); at >= 0; at = para.indexOf('<span class="tl-term">', cursor)) {
    const end = closingEnd(para, at, "span");
    if (end < 0) break;
    const term = para.slice(at, end);
    const label = /<label\b[^>]*>([\s\S]*?)<\/label>/.exec(term)?.[1];
    const defAt = term.indexOf('<span class="tl-def">');
    const defEnd = defAt < 0 ? -1 : closingEnd(term, defAt, "span");
    out += para.slice(cursor, at);
    if (label && defEnd > 0) {
      const def = term.slice(defAt + '<span class="tl-def">'.length, defEnd - "</span>".length);
      notes.push(`<div class="tl-sn-item tl-sn-item--term"><b>${label.trim()}</b> — ${def.trim()}</div>`);
      out += term.replace('<span class="tl-term">', '<span class="tl-term tl-term--sn">');
    } else {
      out += term;
    }
    cursor = end;
  }
  return out + para.slice(cursor);
}

/** Vị trí ngay sau thẻ đóng khớp với thẻ mở `tag` bắt đầu tại `from` (đếm lồng cùng tên thẻ). */
function closingEnd(html: string, from: number, tag: string): number {
  const re = new RegExp(`<(/?)${tag}\\b[^>]*>`, "gi");
  re.lastIndex = from;
  let depth = 0;
  for (let m = re.exec(html); m; m = re.exec(html)) {
    depth += m[1] ? -1 : 1;
    if (depth === 0) return m.index + m[0].length;
  }
  return -1;
}

const FIG_CREDIT = /^\s*<ol class="tl-fns">([\s\S]*?)<\/ol>/;

/**
 * Nguồn/ghi chú của hình (`<ol class="tl-fns">` liền sau `</figure>`) → khối lề `<div class="tl-sn tl-sn--fig">` đặt ngay
 * trước `<figure>`, nên ≥ 1280 nó float sang lề phải ngang đầu hình (thầy chốt 30/10/2026: ghi chú bên phải hình, không
 * dưới hình). Chỉ hình ở cấp đầu hoặc nằm thẳng trong mục bấm xem `details.tl-more` (không khung, mép phải trùng cột chữ);
 * hình trong hộp (.tl-box, .tl-trap) giữ nguồn dưới hình vì lề âm sẽ vượt khung hộp.
 */
function withFigureNotes(html: string, placed: Set<string>): string {
  const re = new RegExp(BLOCK_TAG.source, "gi");
  const stack: string[] = [];
  let out = "";
  let cursor = 0;
  for (let m = re.exec(html); m; m = re.exec(html)) {
    const tag = m[2].toLowerCase();
    if (tag === "p") continue;
    if (m[1]) {
      stack.pop();
      continue;
    }
    if (tag === "figure" && (stack.length === 0 || (stack.length === 1 && stack[0] === "more"))) {
      const end = closingEnd(html, m.index, "figure");
      const credit = end > 0 ? FIG_CREDIT.exec(html.slice(end)) : null;
      const items = credit ? [...credit[1].matchAll(FN_ITEM)] : [];
      if (items.length) {
        for (const li of items) placed.add(li[2]);
        const notes = items.map((li) => `<div class="tl-sn-item">${li[4].trim()}</div>`).join("");
        out += html.slice(cursor, m.index) + `<div class="tl-sn tl-sn--fig">${notes}</div>`;
        cursor = m.index;
      }
    }
    stack.push(tag === "details" && /\btl-more\b/.test(m[0]) ? "more" : tag);
  }
  return out + html.slice(cursor);
}

export function withMarginNotes(html: string): string {
  if (!/class="tl-(fns?|term|nums)"/.test(html)) return html;

  const fnText = new Map<string, string>();
  for (const m of html.matchAll(FN_ITEM)) fnText.set(m[2], m[4].trim());
  // Nguồn ảnh (danh sách `.tl-fns` đứng liền sau `</figure>`) thuộc về HÌNH, không thuộc đoạn có số mũ (đoạn đó có khi
  // cách hình cả màn, hình trong `<details>` đóng) → không chép theo đoạn; withFigureNotes đặt nó cạnh đầu hình.
  for (const m of html.matchAll(/<\/figure>\s*<ol class="tl-fns">([\s\S]*?)<\/ol>/g)) {
    for (const li of m[1].matchAll(FN_ITEM)) fnText.delete(li[2]);
  }
  const placed = new Set<string>();
  html = withFigureNotes(html, placed);

  let out = "";
  let cursor = 0;
  let depth = 0;
  BLOCK_TAG.lastIndex = 0;
  for (let m = BLOCK_TAG.exec(html); m; m = BLOCK_TAG.exec(html)) {
    const closing = m[1] === "/";
    const tag = m[2].toLowerCase();
    if (tag !== "p") {
      depth += closing ? -1 : 1;
      continue;
    }
    if (closing || depth !== 0) continue;

    const start = m.index;
    const pEnd = html.indexOf("</p>", start);
    if (pEnd < 0) break;
    const end = pEnd + 4;
    let para = html.slice(start, end);
    const notes: string[] = [];

    const seen = new Set<string>();
    for (const ref of para.matchAll(FN_REF)) {
      const text = fnText.get(ref[1]);
      if (!text || seen.has(ref[1])) continue;
      seen.add(ref[1]);
      notes.push(`<div class="tl-sn-item"><span class="tl-sn-n">${ref[2].trim()}</span>${text}</div>`);
      placed.add(ref[1]);
    }
    para = collectTerms(para, notes);

    // Ô "Số cần nhớ" đứng liền sau đoạn (chỉ cách khoảng trắng) là của đoạn đó.
    let after = end;
    const rest = html.slice(end);
    const gap = /^\s*/.exec(rest)?.[0].length ?? 0;
    const numsOpen = /^<div class="tl-nums">/.exec(rest.slice(gap));
    let numsHtml = "";
    if (numsOpen) {
      const numsStart = end + gap;
      const numsEnd = closingEnd(html, numsStart, "div");
      if (numsEnd > 0) {
        const inner = html.slice(numsStart + numsOpen[0].length, numsEnd - "</div>".length);
        notes.push(`<div class="tl-sn-item tl-sn-item--nums"><span>Số cần nhớ — nhớ lại rồi bấm để kiểm:</span><div class="tl-sn-nums">${inner}</div></div>`);
        numsHtml = html.slice(end, numsStart) + '<div class="tl-nums tl-nums--sn">' + html.slice(numsStart + numsOpen[0].length, numsEnd);
        after = numsEnd;
      }
    }

    if (notes.length === 0) continue;
    out += html.slice(cursor, start) + `<div class="tl-sn">${notes.join("")}</div>` + para + numsHtml;
    cursor = after;
    BLOCK_TAG.lastIndex = after;
  }
  out += html.slice(cursor);

  if (placed.size === 0) return out;
  // Chú thích đã có ở lề: đánh dấu từng dòng trong danh sách cuối bài; cả danh sách đều đã chép thì đánh dấu cả danh sách.
  out = out.replace(FN_ITEM, (all, pre: string, id: string, post: string, body: string) => {
    if (!placed.has(id)) return all;
    const attrs = `${pre}id="${id}"${post}`;
    return /\bclass="/.test(attrs)
      ? `<li${attrs.replace(/\bclass="/, 'class="tl-fn--placed ')}>${body}</li>`
      : `<li class="tl-fn--placed"${attrs}>${body}</li>`;
  });
  // Danh sách nào chép hết lên lề thì ẩn cả danh sách (mỗi danh sách tự xét: chú thích hình đặt dưới hình, danh sách cuối bài).
  out = out.replace(/<ol class="tl-fns">([\s\S]*?)<\/ol>/g, (all, inner: string) =>
    /<li\b(?![^>]*tl-fn--placed)/.test(inner) ? all : all.replace('<ol class="tl-fns">', '<ol class="tl-fns tl-fns--placed">'),
  );
  return out;
}
