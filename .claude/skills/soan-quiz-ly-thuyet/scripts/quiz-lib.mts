// Logic kiểm bộ câu lý thuyết dùng chung cho validate-quiz.mts và scripts/publish-theory-quiz.mts.
// Không cần DB: đối chiếu với public/data (sinh bằng `node scripts/build-content.mjs`).
import { readLesson, sectionsOf } from "./list-sections.mts";

export const DIFFICULTIES = ["Dễ", "Trung bình", "Khó"] as const;
/** File dùng nhãn tiếng Việt; DB (exams.questions → question_bank) chỉ nhận mã bên phải. */
export const DIFFICULTY_CODE: Record<string, string> = { "Dễ": "de", "Trung bình": "trung-binh", "Khó": "kho" };

const ALLOWED_KEYS = new Set([
  "type", "question", "options", "answer", "statements", "explanation",
  "topic", "form", "difficulty", "difficultySource", "theorySection", "kind",
]);

export interface QuizQuestion {
  type: "multiple_choice" | "true_false" | "short_answer";
  question: string;
  options?: string[];
  answer?: number | string;
  statements?: { text: string; answer: boolean }[];
  explanation: string;
  topic: string;
  form: "ly_thuyet";
  difficulty: string;
  difficultySource: "ai";
  theorySection?: number;
  kind: string;
  [k: string]: unknown;
}

export interface QuizFile {
  lesson_id: number;
  lesson_title: string;
  item_id: number;
  generated_at: string;
  generated_by: string;
  quiz_min_correct: number;
  review: { checked: boolean; removed: { question: string; reason: string }[] };
  questions: QuizQuestion[];
}

export interface Report {
  errors: string[];
  warnings: string[];
}

const isStr = (v: unknown): v is string => typeof v === "string" && v.trim() !== "";
const norm = (s: string) => s.replace(/\s+/g, " ").trim(); // giữ hoa/thường: $t$ ≠ $T$

/** Số dấu $ (bỏ \$) phải chẵn — $...$ và $$...$$ đều cân. */
export function dollarsBalanced(s: string): boolean {
  return ((s.replace(/\\\$/g, "").match(/\$/g) ?? []).length % 2) === 0;
}

export function minCorrectFor(n: number): number {
  return Math.ceil(n * 0.75);
}

export function validateQuiz(data: unknown, label: string, opts: { minQuestions?: number } = {}): Report {
  const errors: string[] = [];
  const warnings: string[] = [];
  const err = (m: string) => errors.push(`${label}: ${m}`);
  const warn = (m: string) => warnings.push(`${label}: ${m}`);
  if (typeof data !== "object" || data === null || Array.isArray(data)) {
    err("không phải object JSON");
    return { errors, warnings };
  }
  const f = data as Partial<QuizFile>;
  if (typeof f.lesson_id !== "number") err("thiếu/sai lesson_id (number)");
  if (!isStr(f.lesson_title)) err("thiếu lesson_title");
  if (typeof f.item_id !== "number") err("thiếu/sai item_id (number)");
  if (!isStr(f.generated_at)) err("thiếu generated_at");
  if (!isStr(f.generated_by)) err("thiếu generated_by");
  if (f.review?.checked !== true) err("review.checked phải là true (chưa qua kiểm chéo)");
  if (!Array.isArray(f.review?.removed)) err("review.removed phải là mảng");
  if (!Array.isArray(f.questions)) {
    err("questions phải là mảng");
    return { errors, warnings };
  }
  const qs = f.questions;
  const min = opts.minQuestions ?? 10;
  if (qs.length < min) err(`chỉ có ${qs.length} câu (< ${min})`);
  if (!Number.isInteger(f.quiz_min_correct) || (f.quiz_min_correct as number) < 1 || (f.quiz_min_correct as number) > qs.length) {
    err(`quiz_min_correct=${f.quiz_min_correct} phải là số nguyên trong 1..${qs.length}`);
  } else if (f.quiz_min_correct !== minCorrectFor(qs.length)) {
    warn(`quiz_min_correct=${f.quiz_min_correct}, quy ước làm tròn lên 75% = ${minCorrectFor(qs.length)}`);
  }

  // Đối chiếu với học liệu tĩnh.
  let sectionTotal: number | null = null;
  if (typeof f.lesson_id === "number") {
    try {
      const lesson = readLesson(f.lesson_id);
      if (f.lesson_title !== lesson.lesson.title) err(`lesson_title "${f.lesson_title}" ≠ "${lesson.lesson.title}" trong public/data`);
      const theory = lesson.items.filter((i) => i.kind === "ly_thuyet");
      const item = theory.find((i) => i.id === f.item_id);
      if (!item) err(`item_id ${f.item_id} không phải mục ly_thuyet của bài (có: ${theory.map((i) => i.id).join(", ") || "không có"})`);
      else sectionTotal = sectionsOf(item).length;
    } catch (e) {
      err((e as Error).message);
    }
  }

  const seen = new Map<string, number>();
  const counts: Record<string, number> = {};
  let nonEasy = 0;
  let noSection = 0;
  qs.forEach((q, i) => {
    const tag = `câu ${i + 1}`;
    const e = (m: string) => err(`${tag}: ${m}`);
    if (typeof q !== "object" || q === null) return e("không phải object");
    counts[q.type] = (counts[q.type] ?? 0) + 1;
    for (const k of Object.keys(q)) if (!ALLOWED_KEYS.has(k)) e(`key lạ "${k}" (sẽ vào DB nguyên xi)`);
    if (!isStr(q.question)) e("thiếu question");
    if (!isStr(q.explanation)) e("thiếu explanation (không rỗng)");
    if (!isStr(q.topic)) e("thiếu topic");
    if (q.form !== "ly_thuyet") e(`form phải là "ly_thuyet", đang là ${JSON.stringify(q.form)}`);
    if (!(DIFFICULTIES as readonly string[]).includes(q.difficulty)) e(`difficulty ${JSON.stringify(q.difficulty)} ∉ {${DIFFICULTIES.join(", ")}}`);
    else if (q.difficulty !== "Dễ") nonEasy += 1;
    if (q.difficulty === "Khó") e("không được có câu Khó trong bộ kiểm tra nhanh");
    if (q.difficultySource !== "ai") e('difficultySource phải là "ai"');
    if (!isStr(q.kind)) e("thiếu kind");
    if (sectionTotal !== null) {
      if (sectionTotal === 0) {
        if (q.theorySection !== undefined) e("mục lý thuyết không có đoạn nào → không được có theorySection");
      } else if (q.theorySection === undefined) {
        noSection += 1; // nội dung nằm trước mốc đầu tiên (không thuộc đoạn nào) → "Ôn ngay" nhảy về đầu mục
      } else if (!Number.isInteger(q.theorySection) || (q.theorySection as number) < 0 || (q.theorySection as number) >= sectionTotal) {
        e(`theorySection=${JSON.stringify(q.theorySection)} ngoài 0..${sectionTotal - 1} (số đoạn thật)`);
      }
    }
    if (isStr(q.question)) {
      const key = norm(q.question) + "|" + q.type;
      if (seen.has(key)) e(`trùng nguyên văn với câu ${seen.get(key)}`);
      else seen.set(key, i + 1);
    }
    const texts: [string, unknown][] = [["question", q.question], ["explanation", q.explanation]];
    if (q.type === "multiple_choice") {
      if (!Array.isArray(q.options) || q.options.length !== 4 || !q.options.every(isStr)) e("cần đúng 4 options không rỗng");
      else {
        if (new Set(q.options.map(norm)).size !== 4) e("4 options phải khác nhau");
        q.options.forEach((o, j) => texts.push([`options[${j}]`, o]));
      }
      if (!Number.isInteger(q.answer) || (q.answer as number) < 0 || (q.answer as number) > 3) e(`answer=${JSON.stringify(q.answer)} phải là số nguyên 0–3`);
    } else if (q.type === "true_false") {
      if (!Array.isArray(q.statements) || q.statements.length !== 4) e("cần đúng 4 statements");
      else {
        q.statements.forEach((s, j) => {
          if (!isStr(s?.text) || typeof s?.answer !== "boolean") e(`statements[${j}] cần {text, answer:boolean}`);
          else texts.push([`statements[${j}]`, s.text]);
        });
        if (q.statements.every((s) => s?.answer === true)) e("đúng–sai phải có ít nhất 1 ý sai");
      }
    } else if (q.type === "short_answer") {
      if (typeof q.answer !== "string" || !/^[0-9,-]{1,4}$/.test(q.answer) || !/\d/.test(q.answer)) e(`answer=${JSON.stringify(q.answer)} phải ≤ 4 ký tự, chỉ gồm 0-9 , -`);
    } else e(`type ${JSON.stringify((q as { type?: unknown }).type)} không hợp lệ (multiple_choice | true_false | short_answer)`);
    for (const [name, t] of texts) if (typeof t === "string" && !dollarsBalanced(t)) e(`${name}: dấu $ LaTeX không cân`);
  });
  if (noSection > 0) warn(`${noSection} câu không có theorySection (chỉ hợp lệ khi căn cứ nằm trước mốc đoạn đầu tiên)`);
  if (qs.length >= 10 && nonEasy > qs.length - 8) warn(`chỉ ${qs.length - nonEasy} câu Dễ (khuyến nghị ≥ 8)`);
  return { errors, warnings };
}
