// Soạn câu cho "Đố vui lớp học": dán văn bản kiểu "Câu 1. … A. … B. … Đáp án: B" → danh sách câu trắc nghiệm.
// Toán thuần, không phụ thuộc React/Supabase — kiểm bằng scripts/test-quiz-live-text.mts.

export interface QuizQuestion {
  type: "multiple_choice";
  /** HTML đã escape (công thức $…$ giữ nguyên cho KaTeX). Câu lấy từ ngân hàng là HTML gốc. */
  question: string;
  options: string[];
  /** Chỉ số đáp án đúng (0–3); -1 = chưa chọn (chưa chơi được). */
  answer: number;
  explanation: string;
  /** Có = câu lấy từ ngân hàng (không đưa ngược vào ngân hàng lần nữa). */
  bank_id?: number;
  /** Có = câu tự gõ; giữ văn bản gốc để sửa lại. Bị bỏ khi đưa vào ngân hàng. */
  typed?: { question: string; options: string[]; explanation: string; correct: number };
}

const MATH = /(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$)/g;

/** Văn bản thường → HTML an toàn: escape &lt; &gt; &amp; ngoài công thức; trong $…$ đổi < > thành \lt \gt. */
export function textToHtml(text: string): string {
  return text
    .trim()
    .split(MATH)
    .map((part, i) =>
      i % 2 === 1
        ? part.replace(/</g, "\\lt ").replace(/>/g, "\\gt ")
        : part.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br>"),
    )
    .join("");
}

/**
 * Dựng câu từ văn bản gốc. `correct` = chỉ số đáp án đúng trong ô nhập (kể cả ô trống);
 * đáp án trống bị bỏ khỏi câu chơi và chỉ số đúng được đánh lại theo các đáp án còn lại.
 */
export function makeTypedQuestion(
  src: { question: string; options: string[]; explanation: string },
  correct: number,
): QuizQuestion {
  const kept = src.options.map((o, i) => ({ o, i })).filter((x) => x.o.trim());
  const answer = kept.findIndex((x) => x.i === correct);
  return {
    type: "multiple_choice",
    question: textToHtml(src.question),
    options: kept.map((x) => textToHtml(x.o)),
    answer,
    explanation: textToHtml(src.explanation),
    typed: { question: src.question, options: src.options, explanation: src.explanation, correct },
  };
}

export interface ParseResult {
  questions: QuizQuestion[];
  /** Cảnh báo theo câu (số thứ tự 1-based trong lượt dán). */
  warnings: string[];
}

const Q_START = /^\s*(?:câu|cau)\s*\d+\s*[.:)]\s*(.*)$/i;
const OPT = /^\s*([A-Da-d])\s*[.)]\s*(.*)$/;
const ANS = /^\s*(?:đáp\s*án|dap\s*an|đ\s*\/?\s*a)\s*[:.\-]?\s*([A-Da-d])\b/i;
const EXPL = /^\s*(?:giải\s*thích|lời\s*giải|loi\s*giai|giai\s*thich)\s*[:.\-]?\s*(.*)$/i;

/** Dấu đáp án đúng: `*` ở cuối hoặc đầu dòng đáp án. */
function stripStar(s: string): { text: string; star: boolean } {
  const t = s.trim();
  if (/\*\s*$/.test(t)) return { text: t.replace(/\s*\*\s*$/, ""), star: true };
  if (/^\*\s*/.test(t)) return { text: t.replace(/^\*\s*/, ""), star: true };
  return { text: t, star: false };
}

export function parseQuizText(raw: string): ParseResult {
  const lines = raw.replace(/\r/g, "").split("\n");
  // Gom thành các khối câu: theo "Câu N." nếu có; không có thì tách theo dòng trống.
  const hasMarkers = lines.some((l) => Q_START.test(l));
  const blocks: string[][] = [];
  let cur: string[] = [];
  const flush = () => {
    if (cur.some((l) => l.trim())) blocks.push(cur);
    cur = [];
  };
  for (const l of lines) {
    if (hasMarkers ? Q_START.test(l) : !l.trim()) flush();
    cur.push(l);
  }
  flush();

  const questions: QuizQuestion[] = [];
  const warnings: string[] = [];
  blocks.forEach((block, bi) => {
    const n = bi + 1;
    const stem: string[] = [];
    const opts: string[] = [];
    const expl: string[] = [];
    let answer = -1;
    let starAt = -1;
    let mode: "stem" | "opt" | "expl" = "stem";
    block.forEach((line, li) => {
      const q = li === 0 ? Q_START.exec(line) : null;
      if (q) {
        stem.push(q[1]);
        return;
      }
      const a = ANS.exec(line);
      if (a && mode !== "stem") {
        answer = a[1].toUpperCase().charCodeAt(0) - 65;
        mode = "stem"; // dòng sau đáp án (nếu có) chỉ nhận khi là "Giải thích"
        return;
      }
      const e = EXPL.exec(line);
      if (e) {
        mode = "expl";
        if (e[1]) expl.push(e[1]);
        return;
      }
      const o = OPT.exec(line);
      if (o && o[1].toUpperCase().charCodeAt(0) - 65 === opts.length && mode !== "expl") {
        mode = "opt";
        const { text, star } = stripStar(o[2]);
        if (star) starAt = opts.length;
        opts.push(text);
        return;
      }
      if (!line.trim()) return;
      if (mode === "stem" && opts.length === 0) stem.push(line.trim());
      else if (mode === "opt" && opts.length) opts[opts.length - 1] += " " + line.trim();
      else if (mode === "expl") expl.push(line.trim());
    });
    const label = `Câu ${n}`;
    const question = stem.join("\n").trim();
    if (!question) return void warnings.push(`${label}: thiếu nội dung câu hỏi`);
    if (opts.length < 2) return void warnings.push(`${label}: cần ít nhất 2 đáp án (A., B.…)`);
    if (answer < 0 && starAt >= 0) answer = starAt;
    if (answer >= opts.length) answer = -1;
    if (answer < 0) warnings.push(`${label}: chưa có đáp án đúng — thêm "Đáp án: B" hoặc dấu * sau đáp án đúng`);
    questions.push(makeTypedQuestion({ question, options: opts, explanation: expl.join("\n").trim() }, answer));
  });
  return { questions, warnings };
}

/** Câu trong ngân hàng (jsonb) → câu chơi được; null nếu không phải trắc nghiệm 2–4 đáp án. */
export function bankToQuizQuestion(id: number, q: unknown): QuizQuestion | null {
  const o = q as { type?: string; question?: unknown; options?: unknown; answer?: unknown; explanation?: unknown };
  if (!o || o.type !== "multiple_choice" || typeof o.question !== "string") return null;
  if (!Array.isArray(o.options) || o.options.length < 2 || o.options.length > 4) return null;
  if (typeof o.answer !== "number" || o.answer < 0 || o.answer >= o.options.length) return null;
  return {
    type: "multiple_choice",
    question: o.question,
    options: o.options.map(String),
    answer: o.answer,
    explanation: typeof o.explanation === "string" ? o.explanation : "",
    bank_id: id,
  };
}

/** Câu đã đủ điều kiện chơi chưa (để chặn nút "Chơi"). */
export function quizQuestionIssue(q: QuizQuestion): string | null {
  if (!q.question.trim()) return "thiếu nội dung";
  if (q.options.length < 2 || q.options.some((o) => !o.trim())) return "đáp án trống";
  if (q.answer < 0 || q.answer >= q.options.length) return "chưa chọn đáp án đúng";
  return null;
}
