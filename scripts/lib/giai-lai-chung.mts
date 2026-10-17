// Phần dùng chung cho sinh lời giải ngân hàng bằng Haiku: prompt, so khớp đáp án, tách dòng ⇒, kiểm KaTeX.
import katex from "katex";

export const SYSTEM = `Bạn là giáo viên Vật lí THPT Việt Nam. Tự giải câu hỏi từ đầu rồi viết lời giải. Đề lấy từ Word nên có thể lỗi ký tự (vd "l kg" = 1 kg, công thức vỡ, mất ^) — sửa ngầm nếu chắc chắn, nếu mơ hồ thì nói rõ trong "ghi_chu".
Lời giải là HTML + LaTeX $...$ (công thức có < > viết \\lt \\gt), mỗi bước một <p class="text-base leading-relaxed my-2">…</p>. Phong cách: nêu định luật và điều kiện áp dụng trước, chọn chiều dương/hệ quy chiếu rõ ràng khi cần, công thức chữ trước rồi thay số, kết luận có đơn vị. Đúng–sai: mỗi ý a), b), c), d) một đoạn riêng kết luận Đúng/Sai. Không dùng vai "thầy". Ngắn gọn.
Các bước suy ra: KHÔNG viết liền một dòng; mỗi phép suy ra một <p> riêng, đầu dòng là $\\Rightarrow$ (vd dòng 1 công thức, dòng 2 bắt đầu bằng $\\Rightarrow$ kèm bước biến đổi tiếp theo).
Chỉ trả về MỘT đối tượng JSON: {"answer": ..., "explanation": "<html>", "ghi_chu": ""}. answer: trắc nghiệm = "A"|"B"|"C"|"D"; trả lời ngắn = số dạng chuỗi (dấu phẩy thập phân VN); đúng–sai = mảng 4 boolean cho ý a,b,c,d.`;

export const plain = (s: string) => (s ?? "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
export const hasImg = (q: any) => /<img|<svg|\bsrc=/i.test(JSON.stringify([q.question, q.options, q.statements]));
export const TYPES = ["multiple_choice", "true_false", "short_answer"];

export function prompt(q: any): string {
  let s = `Loại: ${q.type}\nĐề: ${q.question}\n`;
  if (q.options) s += "Phương án:\n" + q.options.map((o: string, i: number) => "ABCD"[i] + ". " + o).join("\n");
  if (q.statements) s += "Các ý:\n" + q.statements.map((x: any, i: number) => "abcd"[i] + ") " + x.text).join("\n");
  return s;
}
export const dbAnswer = (q: any): any =>
  q.type === "multiple_choice" ? "ABCD"[q.answer] : q.type === "short_answer" ? String(q.answer) : (q.statements ?? []).map((s: any) => !!s.answer);
const num = (s: string) => { const m = String(s).replace(/\s/g, "").replace(",", ".").match(/-?\d+(\.\d+)?(e-?\d+)?/i); return m ? parseFloat(m[0]) : NaN; };
export function khop(q: any, a: any): boolean {
  const d = dbAnswer(q);
  if (q.type === "true_false") return Array.isArray(a) && a.length === 4 && a.every((v: any, i: number) => !!v === d[i]);
  if (q.type === "multiple_choice") return String(a).trim().toUpperCase().charAt(0) === d;
  const x = num(a), y = num(d);
  return String(a).trim().replace(".", ",") === String(d).trim().replace(".", ",") || (isFinite(x) && isFinite(y) && Math.abs(x - y) <= 0.02 * Math.max(Math.abs(y), 1e-9));
}

const ARROW = /\\Rightarrow|\\rightarrow|⇒/g;
const dollars = (s: string) => (s.match(/(?<!\\)\$/g) ?? []).length;
const P_OPEN = '<p class="text-base leading-relaxed my-2">';

/** Số đoạn <p> có ⇒ sai chỗ: ≥2 dấu ⇒, hoặc 1 dấu ⇒ không ở đầu dòng. */
export function loiMuiTen(html: string): number {
  return (html.match(/<p[^>]*>.*?<\/p>/gs) ?? []).filter((p) => {
    const t = p.replace(/<\/?p[^>]*>/g, "").trim();
    const n = (t.match(ARROW) ?? []).length;
    return n >= 2 || (n === 1 && !/^\$?\s*(\\Rightarrow|\\rightarrow|⇒)/.test(t));
  }).length;
}

/** Tách mỗi đoạn <p> tại từng dấu ⇒ (trong hay ngoài $…$) thành đoạn riêng bắt đầu bằng ⇒. Không dùng token. Đoạn có $$ hoặc $ lẻ thì giữ nguyên. */
export function tachMuiTen(html: string): string {
  return html.replace(/<p([^>]*)>(.*?)<\/p>/gs, (whole, attrs: string, inner: string) => {
    if (!/\\Rightarrow|\\rightarrow|⇒/.test(inner) || inner.includes("$$") || dollars(inner) % 2 !== 0) return whole;
    const lines: string[] = [""];
    const startsArrow = (x: string) => /^\s*(\\Rightarrow|\\rightarrow|⇒)/.test(x);
    const add = (piece: string, math: boolean) => {
      if (!piece.trim()) return;
      if (startsArrow(piece) && lines[lines.length - 1].trim() !== "") lines.push("");
      lines[lines.length - 1] += math ? `$${piece.trim()}$` : piece;
    };
    for (const seg of inner.split(/((?<!\\)\$.+?(?<!\\)\$)/s)) {
      if (!seg) continue;
      if (seg.startsWith("$") && seg.endsWith("$") && seg.length > 1) {
        for (const piece of seg.slice(1, -1).split(/(?=\\Rightarrow|\\rightarrow)/)) add(piece, true);
      } else {
        for (const piece of seg.split(/(?=⇒)/)) add(piece, false);
      }
    }
    const clean = lines.map((x) => x.trim()).filter(Boolean);
    if (clean.some((x) => dollars(x) % 2 !== 0)) return whole;
    return clean.map((x, i) => (i === 0 ? `<p${attrs}>` : P_OPEN) + x + "</p>").join("");
  });
}

/** Số đoạn $…$ KaTeX không dựng được. */
export function katexLoi(html: string): number {
  let n = 0;
  for (const m of html.matchAll(/(?<!\\)\$(.+?)(?<!\\)\$/gs)) {
    try { katex.renderToString(m[1], { throwOnError: true, strict: "ignore" }); } catch { n++; }
  }
  return n;
}
