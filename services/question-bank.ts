// Ngân hàng câu hỏi (public.question_bank) — bản sao có chỉ mục của mọi câu trong
// exams.questions, chống trùng theo content_hash, xếp theo năng lực cần đạt
// (question_topics). Trigger phía DB tự nạp câu khi đề được tạo/sửa; app chỉ đọc,
// gắn nhãn và lấy câu ra soạn đề. Xem docs/supabase-migration-question-bank.sql.

import type { Difficulty, ExamQuestion, QuestionForm } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

export interface BankQuestion {
  id: number;
  createdAt: string;
  updatedAt: string;
  subjectCode: string;
  grade: string;
  topicId: number | null;
  topicName: string;
  form: QuestionForm | "";
  qtype: ExamQuestion["type"];
  difficulty: Difficulty;
  question: ExamQuestion;
  contentHash: string;
  sourceExamId: number | null;
  sourceIndex: number | null;
  archived: boolean;
  note: string;
}

interface BankRow {
  id: number;
  created_at: string;
  updated_at: string;
  subject_code: string;
  grade: string;
  topic_id: number | null;
  topic_name: string;
  form: string;
  qtype: string;
  difficulty: string;
  question: ExamQuestion;
  content_hash: string;
  source_exam_id: number | null;
  source_index: number | null;
  archived: boolean;
  note: string;
}

const COLS =
  "id, created_at, updated_at, subject_code, grade, topic_id, topic_name, form, qtype, difficulty, question, content_hash, source_exam_id, source_index, archived, note";

function fromRow(r: BankRow): BankQuestion {
  return {
    id: r.id,
    createdAt: r.created_at,
    updatedAt: r.updated_at,
    subjectCode: r.subject_code,
    grade: r.grade,
    topicId: r.topic_id,
    topicName: r.topic_name,
    form: r.form === "ly_thuyet" || r.form === "bai_tap" ? r.form : "",
    qtype: r.qtype as ExamQuestion["type"],
    difficulty: (r.difficulty as Difficulty) || "",
    question: r.question,
    contentHash: r.content_hash,
    sourceExamId: r.source_exam_id,
    sourceIndex: r.source_index,
    archived: r.archived,
    note: r.note ?? "",
  };
}

export interface BankFilter {
  grade?: string;
  /** Lọc theo một hoặc nhiều chủ đề; `null` trong mảng = câu chưa gắn nhãn. */
  topicIds?: (number | null)[];
  form?: QuestionForm | "";
  qtype?: ExamQuestion["type"] | "";
  difficulty?: Difficulty | "all";
  includeArchived?: boolean;
  /** Tìm trong nội dung câu hỏi (ilike). */
  search?: string;
  limit?: number;
}

export async function fetchBankQuestions(filter: BankFilter = {}): Promise<BankQuestion[]> {
  let q = getSupabase()
    .from("question_bank")
    .select(COLS)
    .order("topic_id", { ascending: true, nullsFirst: false })
    .order("source_exam_id", { ascending: true })
    .order("source_index", { ascending: true })
    .limit(filter.limit ?? 500);
  if (filter.grade) q = q.eq("grade", filter.grade);
  if (filter.topicIds && filter.topicIds.length) {
    const ids = filter.topicIds.filter((t): t is number => t !== null);
    const wantNull = filter.topicIds.includes(null);
    if (ids.length && wantNull) q = q.or(`topic_id.in.(${ids.join(",")}),topic_id.is.null`);
    else if (ids.length) q = q.in("topic_id", ids);
    else q = q.is("topic_id", null);
  }
  if (filter.form) q = q.eq("form", filter.form);
  if (filter.qtype) q = q.eq("qtype", filter.qtype);
  if (filter.difficulty !== undefined && filter.difficulty !== "all") q = q.eq("difficulty", filter.difficulty);
  if (!filter.includeArchived) q = q.eq("archived", false);
  if (filter.search?.trim()) q = q.ilike("question->>question", `%${filter.search.trim()}%`);
  const { data, error } = await q;
  if (error) throw new Error(error.message);
  return ((data as BankRow[]) ?? []).map(fromRow);
}

export async function fetchBankQuestionsByIds(ids: number[]): Promise<BankQuestion[]> {
  if (!ids.length) return [];
  const { data, error } = await getSupabase().from("question_bank").select(COLS).in("id", ids);
  if (error) throw new Error(error.message);
  const map = new Map(((data as BankRow[]) ?? []).map((r) => [r.id, fromRow(r)]));
  return ids.map((id) => map.get(id)).filter((x): x is BankQuestion => !!x);
}

/** Số câu theo chủ đề của một khối: key = topic_id (0 = chưa gắn nhãn). */
export interface BankTopicCount {
  topicId: number | null;
  active: number;
  archived: number;
}

export async function fetchBankTopicCounts(grade: string): Promise<BankTopicCount[]> {
  const { data, error } = await getSupabase()
    .from("question_bank_topic_counts")
    .select("topic_id, archived, n")
    .eq("grade", grade);
  if (error) throw new Error(error.message);
  const acc = new Map<number | null, BankTopicCount>();
  for (const r of (data as { topic_id: number | null; archived: boolean; n: number }[]) ?? []) {
    const cur = acc.get(r.topic_id) ?? { topicId: r.topic_id, active: 0, archived: 0 };
    if (r.archived) cur.archived += r.n;
    else cur.active += r.n;
    acc.set(r.topic_id, cur);
  }
  return [...acc.values()];
}

/** Câu chưa rõ khối (đề chưa gán lớp và chủ đề chưa gắn) — hiện riêng để thầy xếp vào. */
export async function fetchBankUnknownGradeCount(): Promise<number> {
  const { count, error } = await getSupabase()
    .from("question_bank")
    .select("id", { count: "exact", head: true })
    .eq("grade", "")
    .eq("archived", false);
  if (error) throw new Error(error.message);
  return count ?? 0;
}

export interface SimilarPair {
  topicId: number | null;
  topicName: string;
  id1: number;
  id2: number;
  similarity: number;
}

/** Cặp câu nghi giống nhau trong cùng chủ đề (trigram trên nội dung câu, bỏ thẻ HTML) — chỉ để
 * cảnh báo, thầy tự xem và lưu trữ câu thừa. Xem docs/supabase-migration-question-bank-similarity.sql. */
export async function fetchSimilarBankQuestions(grade: string, threshold = 0.5): Promise<SimilarPair[]> {
  const { data, error } = await getSupabase().rpc("find_similar_bank_questions", {
    p_grade: grade,
    p_threshold: threshold,
  });
  if (error) throw new Error(error.message);
  return ((data as { topic_id: number | null; topic_name: string; id1: number; id2: number; similarity: number }[]) ?? []).map(
    (r) => ({ topicId: r.topic_id, topicName: r.topic_name, id1: r.id1, id2: r.id2, similarity: r.similarity }),
  );
}

export interface BankPatch {
  topicName?: string; // '' = bỏ nhãn; trigger DB tự tra topic_id + khối theo tên
  form?: QuestionForm | "";
  difficulty?: Difficulty;
  archived?: boolean;
  note?: string;
  grade?: string;
}

export async function updateBankQuestion(id: number, patch: BankPatch): Promise<void> {
  const payload: Record<string, unknown> = {};
  if (patch.topicName !== undefined) payload.topic_name = patch.topicName;
  if (patch.form !== undefined) payload.form = patch.form;
  if (patch.difficulty !== undefined) payload.difficulty = patch.difficulty;
  if (patch.archived !== undefined) payload.archived = patch.archived;
  if (patch.note !== undefined) payload.note = patch.note;
  if (patch.grade !== undefined) payload.grade = patch.grade;
  const { error } = await getSupabase().from("question_bank").update(payload).eq("id", id);
  if (error) throw new Error(error.message);
}

export async function updateBankQuestions(ids: number[], patch: BankPatch): Promise<void> {
  if (!ids.length) return;
  const payload: Record<string, unknown> = {};
  if (patch.topicName !== undefined) payload.topic_name = patch.topicName;
  if (patch.form !== undefined) payload.form = patch.form;
  if (patch.difficulty !== undefined) payload.difficulty = patch.difficulty;
  if (patch.archived !== undefined) payload.archived = patch.archived;
  if (patch.grade !== undefined) payload.grade = patch.grade;
  const { error } = await getSupabase().from("question_bank").update(payload).in("id", ids);
  if (error) throw new Error(error.message);
}

export interface SourceLabelPatch {
  sourceExamId: number;
  sourceIndex: number;
  topicName?: string;
  form?: QuestionForm | "";
}

/**
 * Ghi nhãn ngược vào đúng câu trong `exams.questions` của đề gốc (source_exam_id/source_index),
 * để đề đã đăng cũng có nhãn — không chỉ bản sao trong ngân hàng — phục vụ phân tích/cảnh báo
 * phụ đạo (đọc `topic` thẳng từ exams.questions, không đọc từ question_bank). Giới hạn đã biết:
 * nếu câu trùng content_hash với một đề khác có trước, source_exam_id trỏ về đề CŨ đó (trigger
 * DB không cập nhật lại khi trùng) — lượt vá này sẽ không chạm tới đề đang xem.
 */
export async function syncLabelsToSourceExams(
  patches: SourceLabelPatch[],
): Promise<{ examsUpdated: number; failed: number }> {
  const byExam = new Map<number, SourceLabelPatch[]>();
  for (const p of patches) {
    const arr = byExam.get(p.sourceExamId) ?? [];
    arr.push(p);
    byExam.set(p.sourceExamId, arr);
  }
  const sb = getSupabase();
  let examsUpdated = 0;
  let failed = 0;
  for (const [examId, list] of byExam) {
    try {
      const { data, error } = await sb.from("exams").select("questions").eq("id", examId).single();
      if (error || !data || !Array.isArray(data.questions)) {
        failed++;
        continue;
      }
      const questions = [...(data.questions as ExamQuestion[])];
      let changed = false;
      for (const p of list) {
        const q = questions[p.sourceIndex];
        if (!q || typeof q !== "object") continue;
        const next = { ...q } as ExamQuestion;
        if (p.topicName !== undefined) next.topic = p.topicName;
        if (p.form !== undefined) next.form = p.form;
        questions[p.sourceIndex] = next;
        changed = true;
      }
      if (!changed) continue;
      const { error: updErr } = await sb.from("exams").update({ questions }).eq("id", examId);
      if (updErr) {
        failed++;
        continue;
      }
      examsUpdated++;
    } catch {
      failed++;
    }
  }
  return { examsUpdated, failed };
}

// ---------- Giỏ câu (chọn từ ngân hàng → mang sang trang Đăng đề) ----------
export const BANK_BASKET_KEY = "thachlab.bank-basket.v1";
export const BANK_HANDOFF_KEY = "thachlab.bank-handoff.v1";

export interface BankHandoff {
  title: string;
  grade: string;
  questions: ExamQuestion[];
  bankIds: number[];
}

export function readBasket(): number[] {
  try {
    const raw = window.sessionStorage.getItem(BANK_BASKET_KEY);
    const arr = raw ? (JSON.parse(raw) as unknown) : [];
    return Array.isArray(arr) ? arr.filter((x): x is number => typeof x === "number") : [];
  } catch {
    return [];
  }
}

export function writeBasket(ids: number[]): void {
  try {
    window.sessionStorage.setItem(BANK_BASKET_KEY, JSON.stringify(ids));
  } catch {
    /* private mode */
  }
}

export function writeHandoff(h: BankHandoff): void {
  try {
    window.sessionStorage.setItem(BANK_HANDOFF_KEY, JSON.stringify(h));
  } catch {
    /* private mode */
  }
}

/** Đọc rồi xoá ngay — chỉ nhận một lần khi trang Đăng đề mở. */
export function takeHandoff(): BankHandoff | null {
  try {
    const raw = window.sessionStorage.getItem(BANK_HANDOFF_KEY);
    if (!raw) return null;
    window.sessionStorage.removeItem(BANK_HANDOFF_KEY);
    const h = JSON.parse(raw) as BankHandoff;
    if (!h || !Array.isArray(h.questions)) return null;
    return h;
  } catch {
    return null;
  }
}

/** Câu lấy từ ngân hàng ra đề: bỏ trường thừa, giữ nhãn hiện tại của ngân hàng. */
export function toExamQuestion(b: BankQuestion): ExamQuestion {
  const q = { ...b.question } as ExamQuestion & { bank_id?: number };
  delete q.bank_id;
  return { ...q, topic: b.topicName || undefined, form: b.form || undefined } as ExamQuestion;
}
