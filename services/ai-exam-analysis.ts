/**
 * Gọi Edge Function `analyze-exam-results`: AI đọc số liệu gộp cả lớp của một đề rồi gợi ý chủ đề cần ôn,
 * chẩn đoán lỗi sai ở câu khó và thứ tự chữa. Kết quả nhớ trong localStorage theo (đề, lớp, số lượt nộp)
 * để mở lại bảng chữa bài không phải gọi AI lần nữa; có thêm bài nộp thì khoá đổi → phân tích lại.
 */
import type { AiAnalysisPayload } from "@/lib/review-analysis";
import { edgeFunctionErrorMessage } from "@/services/edge-function-error";
import { getSupabase } from "@/services/supabase";

export interface AiTopicSuggestion {
  topic: string;
  priority: "cao" | "vua" | "thap";
  reason: string;
  reviewTip: string;
  questionIndexes: number[];
}
export interface AiQuestionNote {
  index: number;
  misconception: string;
  teachingTip: string;
}
export interface AiExamAnalysis {
  overview: string;
  topics: AiTopicSuggestion[];
  questions: AiQuestionNote[];
  reviewOrder: number[];
  model?: string;
  createdAt?: string;
}

function cacheKey(examId: number, classId: number, attempts: number) {
  return `ai-phan-tich:${examId}:${classId}:${attempts}`;
}

export function readCachedAnalysis(examId: number, classId: number, attempts: number): AiExamAnalysis | null {
  try {
    const raw = localStorage.getItem(cacheKey(examId, classId, attempts));
    return raw ? (JSON.parse(raw) as AiExamAnalysis) : null;
  } catch {
    return null;
  }
}

export async function analyzeExamResults(
  examId: number,
  classId: number,
  payload: AiAnalysisPayload,
): Promise<AiExamAnalysis> {
  const { data, error } = await getSupabase().functions.invoke("analyze-exam-results", { body: payload });
  if (error) throw new Error(await edgeFunctionErrorMessage(error, "Gọi AI phân tích bài làm lỗi."));
  const d = (data ?? {}) as Partial<AiExamAnalysis>;
  const result: AiExamAnalysis = {
    overview: d.overview ?? "",
    topics: Array.isArray(d.topics) ? d.topics : [],
    questions: Array.isArray(d.questions) ? d.questions : [],
    reviewOrder: Array.isArray(d.reviewOrder) ? d.reviewOrder : [],
    model: d.model,
    createdAt: new Date().toISOString(),
  };
  try {
    localStorage.setItem(cacheKey(examId, classId, payload.attempts), JSON.stringify(result));
  } catch {
    /* hết chỗ/chế độ riêng tư — bỏ qua */
  }
  return result;
}
