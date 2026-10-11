import { getSupabase } from "@/services/supabase";

export interface MistakeTopicCount {
  topic_id: number;
  name: string;
  count: number;
}

export interface MistakeStats {
  total_active: number;
  due_count: number;
  cleared_count: number;
  weak_topics: MistakeTopicCount[];
}

export interface MistakeQuestionItem {
  mistake_id: number;
  exam_id: number;
  question_index: number;
  stage: number;
  type: "multiple_choice" | "true_false" | "short_answer";
  question: string;
  options: string[];
  statements: { text: string }[];
}

export interface MistakeQuizStart {
  ok: boolean;
  reason?: string;
  attempt_id: number;
  total: number;
  questions: MistakeQuestionItem[];
}

export interface MistakeQuestionResult {
  mistake_id: number;
  correct: boolean;
  answer: unknown;
  explanation: string;
}

export interface MistakeQuizSubmitResult {
  ok: boolean;
  correct: number;
  total: number;
  rp_awarded: number;
  results: MistakeQuestionResult[];
}

/** Thống kê sổ tay câu sai của học sinh hiện tại */
export async function fetchMistakeStats(): Promise<MistakeStats | null> {
  try {
    const { data, error } = await getSupabase().rpc("mistake_stats_of");
    if (error || !data) return null;
    return data as MistakeStats;
  } catch {
    return null;
  }
}

/** Bắt đầu một phiên mini-quiz ôn câu sai (ưu tiên câu đến hạn) */
export async function startMistakeReviewQuiz(count = 5): Promise<MistakeQuizStart> {
  const { data, error } = await getSupabase().rpc("mistake_review_quiz_start", {
    p_count: count,
  });
  if (error) throw new Error(error.message);
  return data as MistakeQuizStart;
}

/** Nộp bài ôn câu sai và nhận kết quả + RP thưởng */
export async function submitMistakeReviewQuiz(
  attemptId: number,
  responses: Record<string, unknown>,
): Promise<MistakeQuizSubmitResult> {
  const { data, error } = await getSupabase().rpc("mistake_review_quiz_submit", {
    p_attempt_id: attemptId,
    p_responses: responses,
  });
  if (error) throw new Error(error.message);
  return data as MistakeQuizSubmitResult;
}
