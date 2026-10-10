/* eslint-disable @typescript-eslint/no-explicit-any */
// Quy tắc phát hiện câu hỏi lỗi (cắt cụt, `$` lẻ, mất dấu ^, phương án rỗng…) — dùng CHUNG cho
// trang soạn đề (trình duyệt) và script quét (Node). Thuần TypeScript: không import Node/Supabase.
// Nguồn gốc: scripts/quet-cau-cat-cut-ngan-hang.mts + scripts/quet-loi-so-mu-ngan-hang.mts (đã tách về đây).
// Thêm/sửa quy tắc ở ĐÂY; chạy lại scripts/cap-nhat-lint-flags.mts để cập nhật cột question_bank.lint_flags.

export type LintCode =
  | "deTrong" | "deQuaNgan" | "deCutCuoi" | "deKhongDauKetThuc" | "deThieuGiaTri"
  | "dungSaiThieuY" | "dollarLe" | "nguoacLech" | "latexLa" | "thePhanCuaHong"
  | "nhacHinhKhongCoHinh" | "anhSrcTuongDoi"
  | "phuongAnLanDe" | "soPhuongAnSai" | "phuongAnRong" | "phuongAnMathLoi" | "phuongAnConNhan"
  | "phuongAnCoTab" | "phuongAnNhanNhung" | "phuongAnTrung" | "dapAnNgoaiKhoang"
  | "matMu";

export type LintFlag = {
  code: LintCode;
  /** "loi" = chặn Lưu/Đăng; "canhBao" = chỉ hiện huy hiệu vàng (quy tắc hay bắt nhầm). */
  level: "loi" | "canhBao";
  /** Đoạn văn bản gây cờ (rút gọn) để người soạn tìm chỗ sửa. */
  ctx: string;
};

/** Nhãn tiếng Việt ngắn cho huy hiệu. */
export const LINT_LABEL: Record<LintCode, string> = {
  deTrong: "Đề trống",
  deQuaNgan: "Đề quá ngắn",
  deCutCuoi: "Đề cụt cuối câu",
  deKhongDauKetThuc: "Đề không có dấu kết thúc",
  deThieuGiaTri: "Đề thiếu giá trị",
  dungSaiThieuY: "Đúng/sai thiếu ý",
  dollarLe: "Dấu $ lẻ",
  nguoacLech: "Ngoặc công thức lệch",
  latexLa: "LaTeX lạ",
  thePhanCuaHong: "Thẻ HTML hỏng",
  nhacHinhKhongCoHinh: "Nhắc hình nhưng không có hình",
  anhSrcTuongDoi: "Ảnh đường dẫn tương đối",
  phuongAnLanDe: "Phương án lẫn trong đề",
  soPhuongAnSai: "Số phương án ≠ 4",
  phuongAnRong: "Phương án rỗng",
  phuongAnMathLoi: "Phương án lỗi công thức",
  phuongAnConNhan: "Phương án còn nhãn A–D",
  phuongAnCoTab: "Phương án dính tab",
  phuongAnNhanNhung: "Phương án có nhãn nhúng",
  phuongAnTrung: "Phương án trùng nhau",
  dapAnNgoaiKhoang: "Đáp án ngoài khoảng",
  matMu: "Mất dấu ^ (số mũ/đơn vị)",
};

// Cờ "canhBao": quy tắc hay bắt nhầm. Đo 10/10/2026 trên 19.577 câu: deCutCuoi 5.792 + deKhongDauKetThuc 8.092 đều là
// câu dạng "…bước sóng là" + 4 phương án (hợp lệ) nên KHÔNG được chặn; phuongAnTrung có thể là phương án chỉ có ảnh.
const CANH_BAO = new Set<LintCode>(["deCutCuoi", "deKhongDauKetThuc", "nhacHinhKhongCoHinh", "latexLa", "phuongAnTrung", "phuongAnNhanNhung"]);

const strip = (h: string) => h.replace(/<img[^>]*>/gi, " [IMG] ").replace(/<br\s*\/?>/gi, " ").replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
const mathOdd = (t: string) => { const n = (t.replace(/\\\$/g, "").match(/\$/g) ?? []).length; return n % 2 === 1; };
const braceBad = (t: string) => { let b = 0; for (const m of t.matchAll(/\$([^$]+)\$/g)) { for (const c of m[1].replace(/\\[{}]/g, "")) { if (c === "{") b++; else if (c === "}") b--; } if (b !== 0) return true; } return false; };
const CUT_END = /(?:\b(?:là|bằng|của|và|với|khi|thì|có|được|là:|ở|trong|cho|từ|đến|như|một|các|những|để|nếu|do|vì|tại|trên|dưới|biết|cần|theo)|[,;:(\-–])$/i;

// 2.105 / 3,5.10-5 / 1,2×104 : "10" dính liền số mũ, không có ^ hay {  ·  5 m3, 2 cm2  ·  m/s2, kg/m3…
export const MU_RULES: Record<string, RegExp> = {
  muMatDau: /\d\s*(?:[.·×x*]|\\cdot|\\times)\s*10[-−–]?\d{1,2}(?![\d^_{])(?!\s*(?:[.,]\d))/g,
  donViDai: /\d\s*(?:\\,|\s)?(?:mm|cm|dm|km|m)[23]\b(?![\^_{])/g,
  donViThuong: /\b(?:m|rad|km|cm)\/s[23]\b|\b(?:kg|g|N|C)\/(?:m|cm|dm)[23]\b/g,
};

const strings = (v: unknown, out: string[] = []): string[] => {
  if (typeof v === "string") out.push(v);
  else if (Array.isArray(v)) v.forEach((x) => strings(x, out));
  else if (v && typeof v === "object") Object.values(v as object).forEach((x) => strings(x, out));
  return out;
};

/**
 * Chạy mọi quy tắc trên MỘT câu (object `question` như trong exams.questions / question_bank.question).
 * `qtype` chỉ cần khi object không có `type` (cột question_bank.qtype). Không bỏ qua `lint_ignored` —
 * việc đó là của giao diện (xem `activeLintFlags`).
 */
export function lintQuestion(q: any, qtype?: string): LintFlag[] {
  const out: LintFlag[] = [];
  const add = (code: LintCode, ctx: string) => out.push({ code, level: CANH_BAO.has(code) ? "canhBao" : "loi", ctx: ctx.slice(0, 160) });
  q = q ?? {};
  const type = qtype ?? q.type;
  const raw = String(q.question ?? "");
  const t = strip(raw);

  if (!t) { add("deTrong", ""); return out; }
  const txt = t.replace(/\[IMG\]/g, "").trim();
  const tail = txt.slice(-40);
  if (txt.length < 12 && !/\[IMG\]/.test(t)) add("deQuaNgan", t);
  if (CUT_END.test(txt.replace(/[.?…]+$/, (m) => m === "" ? m : "§")) && !/[.?!…:]$/.test(txt)) add("deCutCuoi", tail);
  if (!/[.?!…:)\]$"”]$/.test(txt) && !/\$$/.test(txt) && type !== "short" && !/\[IMG\]$/.test(t)) add("deKhongDauKetThuc", tail);
  {
    const nm = raw.replace(/\$[^$]*\$/g, "M").replace(/<br\s*\/?>|<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/\s+/g, " ");
    const m = nm.match(/.{0,40}(?:[^M\s]\s{2,}[,.;:](?:\s|$)|(?:là|bằng|với|lực|bán kính|tốc độ|khối lượng|điện áp|cường độ)\s{2,}(?!M)[^\s,.;:]).{0,20}/);
    if (m) add("deThieuGiaTri", m[0]);
  }
  if (type === "true_false") {
    const st = q.statements ?? q.items ?? q.options;
    if (!Array.isArray(st) || st.length < 2 || st.some((z: any) => !strip(String(typeof z === "string" ? z : z?.text ?? z?.statement ?? "")))) add("dungSaiThieuY", JSON.stringify(Object.keys(q)));
  }
  if (mathOdd(raw)) add("dollarLe", tail);
  if (braceBad(raw)) add("nguoacLech", raw.slice(0, 100));
  if (/\\\(|\\\)|\\\[|\\begin\{(?!aligned|cases|array|matrix|pmatrix)/.test(raw)) add("latexLa", raw.slice(0, 100));
  if ((raw.match(/<(?:sup|sub|strong|em|b|i|u|span)\b/g) ?? []).length !== (raw.match(/<\/(?:sup|sub|strong|em|b|i|u|span)>/g) ?? []).length) add("thePhanCuaHong", tail);
  if (/\b(?:Hình|hình)\s*(?:vẽ|bên|dưới|sau|\d)/.test(txt) && !/<img|<svg/i.test(raw) && !q.figure && !q.ai_figure) add("nhacHinhKhongCoHinh", tail);
  if (/<img[^>]+src="(?!https?:\/\/|data:)/i.test(raw)) add("anhSrcTuongDoi", raw.slice(0, 100));
  if (/\b(?:A|B|C|D)\s*[.)]\s+\S/.test(txt.slice(-200)) && /\bA\s*[.)].*\bB\s*[.)]/.test(txt)) add("phuongAnLanDe", tail);

  if (type === "multiple_choice") {
    const o: unknown[] = q.options ?? [];
    if (o.length !== 4) add("soPhuongAnSai", String(o.length));
    o.forEach((x, i) => {
      const ot = strip(String(x ?? ""));
      if (!ot) add("phuongAnRong", `idx ${i}`);
      else if (mathOdd(String(x)) || braceBad(String(x))) add("phuongAnMathLoi", ot);
      else if (/^[A-D]\s*[.)]\s/.test(ot)) add("phuongAnConNhan", ot);
    });
    o.forEach((x) => {
      const raw2 = String(x ?? "");
      if (/\t/.test(raw2)) add("phuongAnCoTab", strip(raw2));
      else if (/(?:^|\s)[A-D]\s*[.)]\s*\S/.test(strip(raw2).replace(/^[A-D]\s*[.)]\s*/, "")) && strip(raw2).length < 60) add("phuongAnNhanNhung", strip(raw2));
    });
    if (/(?:^|\s)A\s*[.)]\s+\S/.test(txt) && /\sB\s*[.)]\s+\S/.test(txt)) add("phuongAnLanDe", txt.slice(-80));
    if (new Set(o.map((x) => strip(String(x)))).size < o.length) add("phuongAnTrung", "");
    if (typeof q.answer !== "number" || q.answer < 0 || q.answer >= o.length) add("dapAnNgoaiKhoang", String(q.answer));
  }

  // Số mũ / đơn vị mất dấu ^ — quét mọi chuỗi trong câu (đề, phương án, lời giải…)
  for (const s of strings(q)) {
    for (const [rule, re] of Object.entries(MU_RULES)) {
      re.lastIndex = 0;
      for (const m of s.matchAll(re)) {
        const i = m.index ?? 0;
        add("matMu", `${rule}: ${s.slice(Math.max(0, i - 25), i + m[0].length + 20).replace(/\s+/g, " ")}`);
        break;
      }
    }
  }
  return out;
}

/** Cờ còn hiệu lực: rỗng nếu giáo viên đã bấm "Bỏ qua cảnh báo" (`lint_ignored`). */
export function activeLintFlags(q: any, qtype?: string): LintFlag[] {
  if (q?.lint_ignored) return [];
  return lintQuestion(q, qtype);
}

/** Chỉ các cờ mức "loi" — dùng để khoá nút Lưu/Đăng. */
export const blockingFlags = (flags: LintFlag[]) => flags.filter((f) => f.level === "loi");

/** Mã cờ không trùng lặp, dạng ghi vào question_bank.lint_flags (text[]). */
export const flagCodes = (flags: LintFlag[]): string[] => [...new Set(flags.map((f) => f.code))].sort();

/** Số câu còn cờ mức "loi" chưa được bỏ qua — dùng để khoá nút Lưu/Đăng ở mọi trang soạn đề. */
export const countBlockingQuestions = (questions: any[]): number =>
  questions.filter((q) => blockingFlags(activeLintFlags(q)).length > 0).length;
