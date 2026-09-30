// Dùng chung cho list-sections / validate-quiz / publish-theory-quiz. Không cần DB, không gọi mạng.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { wrapTheorySections } from "../../../../features/lessons/theory-sections";

const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(here, "../../../..");
export const QUIZ_DIR = path.join(ROOT, "scripts/data/theory-quiz");
export const TOPICS_FILE = path.join(ROOT, "scripts/data/question-topics.json");

export interface SectionInfo { index: number; heading: string; length: number }
export interface TheoryItemInfo { itemId: number; title: string; sections: SectionInfo[]; existingExamIds: number[] }
export interface LessonInfo { id: number; title: string; items: TheoryItemInfo[] }

/** Đọc public/data/lessons/<id>.json và chia đoạn bằng ĐÚNG wrapTheorySections (nguồn duy nhất cho theorySection). */
export function getLessonInfo(lessonId: number): LessonInfo {
  const file = path.join(ROOT, "public/data/lessons", `${lessonId}.json`);
  if (!fs.existsSync(file)) throw new Error(`không có ${path.relative(ROOT, file)}`);
  const data = JSON.parse(fs.readFileSync(file, "utf8"));
  const items: TheoryItemInfo[] = (data.items ?? [])
    .filter((it: { kind: string }) => it.kind === "ly_thuyet")
    .map((it: { id: number; title: string; body_html?: string; exam_ids?: number[] }) => {
      const { html, sections } = wrapTheorySections(it.body_html ?? "", it.id);
      const marks = sections.map((s) => html.indexOf(`id="${s.id}"`));
      return {
        itemId: it.id,
        title: it.title,
        existingExamIds: it.exam_ids ?? [],
        sections: sections.map((s, i) => {
          const end = i + 1 < marks.length ? marks[i + 1] : html.length;
          const text = html.slice(marks[i], end).replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
          return { index: i, heading: s.heading, length: text.length };
        }),
      };
    });
  return { id: lessonId, title: data.lesson?.title ?? "", items };
}

export function loadTopics(): Map<number, string[]> | null {
  if (!fs.existsSync(TOPICS_FILE)) return null;
  const rows = JSON.parse(fs.readFileSync(TOPICS_FILE, "utf8")) as { lesson_id: number; name: string }[];
  const m = new Map<number, string[]>();
  for (const r of rows) m.set(r.lesson_id, [...(m.get(r.lesson_id) ?? []), r.name]);
  return m;
}

export const KEY = (s: string) => s.trim().replace(/\s+/g, " ").toLowerCase();
const DIFFICULTIES = ["de", "trung-binh"]; // "kho" không dùng cho quiz này
const KINDS = ["dinh_nghia", "dinh_luat", "hien_tuong", "dieu_kien", "cong_thuc", "don_vi", "tinh_nhanh", "bien_doi"];
const KNOWLEDGE_GROUP = ["dinh_nghia", "dinh_luat", "hien_tuong", "dieu_kien"];

function dollarsBalanced(s: string): boolean {
  return ((s.replace(/\\\$/g, "").match(/\$/g) ?? []).length % 2) === 0;
}

export interface QuizResult { errors: string[]; warnings: string[] }

export function validateQuiz(data: any, opts: { topics?: Map<number, string[]> | null } = {}): QuizResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  const err = (m: string) => errors.push(m);
  if (!data || typeof data !== "object") return { errors: ["file không phải object JSON"], warnings };

  const lessonId = data.lesson_id;
  if (!Number.isInteger(lessonId)) err("thiếu/sai lesson_id");
  let info: LessonInfo | null = null;
  if (Number.isInteger(lessonId)) {
    try { info = getLessonInfo(lessonId); } catch (e) { err(String((e as Error).message)); }
  }
  if (!data.lesson_title) err("thiếu lesson_title");
  else if (info && info.title !== data.lesson_title) err(`lesson_title "${data.lesson_title}" ≠ "${info.title}" trong public/data`);

  const item = info?.items.find((i) => i.itemId === data.item_id) ?? null;
  if (info && !item) err(`item_id ${data.item_id} không phải mục ly_thuyet của bài (có: ${info.items.map((i) => i.itemId).join(", ") || "không"})`);
  const nSections = item?.sections.length ?? 0;

  const qs: any[] = Array.isArray(data.questions) ? data.questions : [];
  if (!Array.isArray(data.questions)) err("questions không phải mảng");
  if (qs.length < 18) err(`chỉ có ${qs.length} câu (cần ≥ 18)`);
  if (qs.length > 20) warnings.push(`${qs.length} câu (> 20)`);
  const expectMin = Math.ceil(qs.length * 0.75);
  if (data.quiz_min_correct !== expectMin) err(`quiz_min_correct = ${data.quiz_min_correct}, phải là ${expectMin} (75% của ${qs.length}, làm tròn lên)`);
  if (!data.review?.checked) err("review.checked phải là true (chưa qua kiểm chéo)");
  if (!Array.isArray(data.review?.removed)) err("thiếu review.removed (mảng, có thể rỗng)");
  const counts = data.review?.counts;
  const seen = new Set<string>();
  let kien = 0, cong = 0, easy = 0;
  const topicList = opts.topics?.get(lessonId);

  qs.forEach((q, i) => {
    const at = (m: string) => err(`Câu ${i + 1}: ${m}`);
    const texts: string[] = [];
    if (!["multiple_choice", "true_false", "short_answer"].includes(q?.type)) return at(`type "${q?.type}" không hợp lệ`);
    if (typeof q.question !== "string" || !q.question.trim()) at("thiếu question");
    else {
      texts.push(q.question);
      const k = KEY(q.question);
      if (seen.has(k)) at("trùng nguyên văn với câu trước");
      seen.add(k);
    }
    if (q.type === "multiple_choice") {
      if (!Array.isArray(q.options) || q.options.length !== 4) at("cần đúng 4 options");
      else {
        if (new Set(q.options.map((o: string) => KEY(String(o)))).size !== 4) at("4 options phải khác nhau");
        if (q.options.some((o: unknown) => typeof o !== "string" || !(o as string).trim())) at("option rỗng");
        texts.push(...q.options.map(String));
      }
      if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer > 3) at(`answer ${q.answer} ngoài 0–3`);
    } else if (q.type === "true_false") {
      if (!Array.isArray(q.statements) || q.statements.length !== 4) at("cần đúng 4 ý (statements)");
      else {
        if (q.statements.some((s: any) => !s?.text?.trim() || typeof s.answer !== "boolean")) at("mỗi ý cần text + answer boolean");
        if (!q.statements.some((s: any) => s?.answer === false)) at("cần ít nhất 1 ý sai");
        texts.push(...q.statements.map((s: any) => String(s?.text ?? "")));
      }
    } else {
      if (typeof q.answer !== "string" || !/^[0-9,\-]+$/.test(q.answer) || q.answer.length > 4)
        at(`answer "${q.answer}" phải là chuỗi ≤ 4 ký tự gồm 0-9 , -`);
    }
    if (typeof q.explanation !== "string" || !q.explanation.trim()) at("thiếu explanation");
    else texts.push(q.explanation);
    if (texts.some((t) => !dollarsBalanced(t))) at("LaTeX lệch dấu $");
    if (q.form !== "ly_thuyet") at('form phải là "ly_thuyet"');
    if (!DIFFICULTIES.includes(q.difficulty)) at(`difficulty "${q.difficulty}" phải thuộc {${DIFFICULTIES.join(", ")}} (mã, không phải nhãn "Dễ"/"Trung bình")`);
    else if (q.difficulty === "de") easy++;
    if (q.difficultySource !== "ai") at('difficultySource phải là "ai"');
    if (typeof q.topic !== "string" || !q.topic.trim()) at("thiếu topic");
    else if (topicList && !topicList.some((t) => KEY(t) === KEY(q.topic)) && KEY(q.topic) !== KEY(data.lesson_title ?? ""))
      warnings.push(`Câu ${i + 1}: topic "${q.topic}" không có trong YCCĐ của bài (question-topics.json)`);
    if (!KINDS.includes(q.kind)) at(`kind "${q.kind}" phải thuộc {${KINDS.join(", ")}}`);
    else if (KNOWLEDGE_GROUP.includes(q.kind)) kien++;
    else cong++;
    if (nSections === 0) {
      if (q.theorySection !== undefined) at("bài không có đoạn nào (list-sections) nên không được có theorySection");
    } else if (q.theorySection === undefined) {
      // Nội dung nằm trước mốc đầu tiên (hoặc ngoài mọi đoạn): "Ôn ngay" về đầu mục, hợp lệ nhưng nên biết.
      warnings.push(`Câu ${i + 1}: không có theorySection (nội dung ngoài mọi đoạn?) — "Ôn ngay" sẽ về đầu mục`);
    } else if (!Number.isInteger(q.theorySection) || q.theorySection < 0 || q.theorySection >= nSections) {
      at(`theorySection ${q.theorySection} ngoài 0–${nSections - 1}`);
    }
  });

  if (qs.length && easy < Math.ceil(qs.length * 0.7)) warnings.push(`chỉ ${easy}/${qs.length} câu Dễ (mục tiêu ≥ 70%)`);
  if (counts && (counts.kien_thuc !== kien || counts.cong_thuc !== cong))
    err(`review.counts (${counts.kien_thuc}/${counts.cong_thuc}) ≠ đếm theo kind (${kien}/${cong})`);
  if (!counts) err("thiếu review.counts");
  const byType = (t: string) => qs.filter((q) => q.type === t).length;
  if (qs.length === 20 && (byType("multiple_choice") !== 10 || byType("true_false") !== 4 || byType("short_answer") !== 6))
    warnings.push(`cơ cấu ${byType("multiple_choice")} TN / ${byType("true_false")} Đ-S / ${byType("short_answer")} TLN (mẫu: 10/4/6)`);
  return { errors, warnings };
}

export function quizFilesIn(target: string): string[] {
  const p = path.resolve(target);
  if (fs.statSync(p).isDirectory()) return fs.readdirSync(p).filter((f) => /^\d+\.json$/.test(f)).sort((a, b) => parseInt(a) - parseInt(b)).map((f) => path.join(p, f));
  return [p];
}
