/**
 * Gọi Edge Function `check-exam`: AI tự giải rồi đối chiếu đáp án/lời giải từng câu trước khi đăng.
 * Kết quả chỉ là gợi ý cho giáo viên — không tự sửa câu nào.
 */
import type { ExamQuestion } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

export type AiVerdict = "ok" | "nghi_ngo" | "loi";

export interface AiCheckItem {
  index: number;
  text: string;
}
/** Bản sửa AI đề xuất. Trường rỗng ("" hoặc []) = giữ nguyên, không đổi. */
export interface AiFix {
  question: string;
  options: string[]; // 4 phương án A–D (trắc nghiệm)
  answer: string; // trắc nghiệm: "A".."D"; trả lời ngắn: giá trị
  statements: { text: string; answer: boolean }[]; // 4 ý a–d (đúng–sai)
  explanation: string;
}
export interface AiCheckResult {
  index: number;
  verdict: AiVerdict;
  note: string;
  fix?: AiFix;
}

/** Các phần AI muốn đổi trên câu `q` — để hiện cho giáo viên trước khi bấm áp dụng. */
export function describeAiFix(q: ExamQuestion, fix: AiFix | undefined): string[] {
  if (!fix) return [];
  const out: string[] = [];
  if (fix.question.trim() && fix.question.trim() !== q.question.trim()) out.push("đề bài");
  if (q.type === "multiple_choice") {
    const letter = fix.answer.trim().toUpperCase();
    if (fix.options.length === 4 && fix.options.some((o, i) => o.trim() && o.trim() !== q.options[i]?.trim()))
      out.push("phương án");
    if (/^[A-D]$/.test(letter) && "ABCD".indexOf(letter) !== q.answer) out.push(`đáp án → ${letter}`);
  } else if (q.type === "true_false") {
    if (fix.statements.length === 4) {
      const changed = fix.statements.some(
        (s, i) => s.text.trim() !== q.statements[i]?.text.trim() || s.answer !== q.statements[i]?.answer,
      );
      if (changed) out.push("các ý a–d");
    }
  } else if (q.type === "short_answer") {
    if (fix.answer.trim() && fix.answer.trim() !== q.answer.trim()) out.push(`đáp án → ${fix.answer.trim()}`);
  }
  if (fix.explanation.trim() && fix.explanation.trim() !== q.explanation.trim()) out.push("lời giải");
  return out;
}

/** Áp bản sửa của AI lên câu `q` (không đụng nhãn chủ đề/dạng/độ khó). Trường rỗng thì giữ nguyên. */
export function applyAiFix(q: ExamQuestion, fix: AiFix | undefined): ExamQuestion {
  if (!fix) return q;
  const next: ExamQuestion = { ...q };
  if (fix.question.trim()) next.question = fix.question.trim();
  if (fix.explanation.trim() && "explanation" in next) next.explanation = fix.explanation.trim();
  if (next.type === "multiple_choice") {
    if (fix.options.length === 4 && fix.options.every((o) => o.trim())) next.options = fix.options.map((o) => o.trim());
    const letter = fix.answer.trim().toUpperCase();
    if (/^[A-D]$/.test(letter)) next.answer = "ABCD".indexOf(letter);
  } else if (next.type === "true_false") {
    if (fix.statements.length === 4 && fix.statements.every((s) => s.text.trim()))
      next.statements = fix.statements.map((s) => ({ text: s.text.trim(), answer: s.answer }));
  } else if (next.type === "short_answer") {
    if (fix.answer.trim()) next.answer = fix.answer.trim();
  }
  return next;
}

async function checkChunk(items: AiCheckItem[]): Promise<AiCheckResult[]> {
  const { data, error } = await getSupabase().functions.invoke("check-exam", { body: { items } });
  if (error) throw new Error(error.message || "Gọi AI kiểm đề lỗi.");
  const results = (data as { results?: AiCheckResult[] } | null)?.results;
  return Array.isArray(results) ? results : [];
}

const BATCH_SIZE = 6; // tự giải cần suy luận → lô nhỏ để mỗi lô về sớm
const CONCURRENCY = 3;

/** Chia lô, gọi song song; `onProgress(đã xong, tổng)`. Chỉ ném lỗi khi MỌI lô đều lỗi. */
export async function checkExamBatched(
  items: AiCheckItem[],
  onProgress?: (done: number, total: number) => void,
): Promise<AiCheckResult[]> {
  if (items.length === 0) return [];
  const chunks: AiCheckItem[][] = [];
  for (let i = 0; i < items.length; i += BATCH_SIZE) chunks.push(items.slice(i, i + BATCH_SIZE));
  const out: AiCheckResult[] = [];
  let done = 0;
  let failed = 0;
  let lastError: unknown = null;
  let next = 0;
  onProgress?.(0, items.length);
  async function worker() {
    while (next < chunks.length) {
      const chunk = chunks[next++];
      try {
        out.push(...(await checkChunk(chunk)));
      } catch (e) {
        failed++;
        lastError = e;
      }
      done += chunk.length;
      onProgress?.(done, items.length);
    }
  }
  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, chunks.length) }, worker));
  if (failed === chunks.length) throw lastError instanceof Error ? lastError : new Error("Gọi AI kiểm đề lỗi.");
  return out;
}
