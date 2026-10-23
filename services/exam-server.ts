import { getSupabase } from "@/services/supabase";
import type {
  Exam,
  ExamForTaking,
  ExamQuestion,
  ExamSubmitResult,
  PracticeAnswerCheck,
  QuestionResponse,
} from "@/features/exams/types";

// Đường duy nhất để HỌC SINH lấy đề / nộp bài / xem đáp án (P0 #1, 24/10/2026).
// exams.questions không còn đọc trực tiếp được — mọi thứ đi qua RPC trong
// supabase/migrations/20261024150000_exam_answer_server_grading.sql.

/** Đề để LÀM (đã lược đáp án với học sinh). Thứ tự theo ids; đề không có quyền thì vắng mặt. */
export async function fetchExamsForTaking(ids: number[]): Promise<ExamForTaking[]> {
  if (ids.length === 0) return [];
  const { data, error } = await getSupabase().rpc("get_exam_for_taking", { p_exam_ids: ids });
  if (error) throw error;
  return (data ?? []) as unknown as ExamForTaking[];
}

export async function fetchExamForTaking(id: number): Promise<ExamForTaking | null> {
  const rows = await fetchExamsForTaking([id]);
  return rows[0] ?? null;
}

export interface ExamViolationPayload {
  type: string;
  at: string;
  away_ms: number;
}

/** Nộp bài: server chấm + ghi. Idempotent theo clientToken nên gọi lại sau lỗi mạng là an toàn. */
export async function submitExamAttempt(args: {
  examId: number;
  clientToken: string;
  responses: QuestionResponse[];
  durationSeconds: number;
  violations: ExamViolationPayload[];
}): Promise<ExamSubmitResult> {
  const { data, error } = await getSupabase().rpc("submit_exam_attempt", {
    p_exam_id: args.examId,
    p_client_token: args.clientToken,
    p_responses: args.responses,
    p_duration_seconds: Math.max(0, Math.round(args.durationSeconds)),
    p_violations: args.violations,
  });
  if (error) throw error;
  if (!data) throw new Error("Server không trả kết quả");
  return data as unknown as ExamSubmitResult;
}

/** Đề ĐỦ đáp án + lời giải của các đề em đã nộp (hoặc staff được phép). Đề không có quyền thì vắng mặt. */
export async function fetchExamReviews(
  ids: number[],
): Promise<Map<number, { id: number; title: string; pass_score: number | null; questions: ExamQuestion[] }>> {
  const out = new Map<number, { id: number; title: string; pass_score: number | null; questions: ExamQuestion[] }>();
  const uniq = [...new Set(ids)];
  for (let i = 0; i < uniq.length; i += 200) {
    const { data, error } = await getSupabase().rpc("get_exam_review", { p_exam_ids: uniq.slice(i, i + 200) });
    if (error) throw error;
    for (const row of (data ?? []) as unknown as { id: number; title: string; pass_score: number | null; questions: ExamQuestion[] }[]) {
      out.set(row.id, row);
    }
  }
  return out;
}

/** Luyện tập "Từng câu": chấm đúng 1 câu ở server, trả đáp án + lời giải của câu đó. */
export async function checkPracticeAnswer(
  examId: number,
  index: number,
  response: QuestionResponse,
): Promise<PracticeAnswerCheck> {
  const { data, error } = await getSupabase().rpc("check_practice_answer", {
    p_exam_id: examId,
    p_index: index,
    p_response: response,
  });
  if (error) throw error;
  return data as unknown as PracticeAnswerCheck;
}

/** Giá trị "chưa trả lời" hợp lệ để gửi cho check_practice_answer (RPC từ chối null) — chấm ra 0 điểm, vẫn trả đáp án. */
export function unansweredSentinel(q: { type: string }): QuestionResponse {
  if (q.type === "true_false") return [null, null, null, null];
  if (q.type === "short_answer" || q.type === "essay" || q.type === "translation") return "";
  return -1;
}

/** Ghép đề metadata + câu hỏi đầy đủ thành Exam (dùng cho màn xem lại). */
export function toFullExam(
  base: { id: number; title: string; duration_minutes?: number; published?: boolean; pass_score?: number | null },
  questions: ExamQuestion[],
): Exam {
  return {
    id: base.id,
    title: base.title,
    duration_minutes: base.duration_minutes ?? 0,
    published: base.published ?? true,
    pass_score: base.pass_score ?? null,
    questions,
  };
}
