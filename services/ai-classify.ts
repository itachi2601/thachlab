/**
 * Gọi Edge Function `classify-questions`: AI gợi ý Chủ đề (yêu cầu cần đạt)/Dạng cho các câu
 * hỏi còn thiếu nhãn ở trang Đăng đề — giới hạn trong đúng danh mục YCCĐ của bài đang soạn,
 * không tự bịa nhãn ngoài danh mục (server đã lọc, nhưng vẫn coi kết quả là gợi ý cần đối chiếu).
 */
import type { Difficulty, QuestionForm } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

export interface AiClassifyItem {
  index: number;
  text: string;
}

export interface AiClassifyResult {
  index: number;
  topic?: string;
  form?: QuestionForm;
  difficulty?: Exclude<Difficulty, "">;
}

export async function classifyQuestionTags(
  topics: string[],
  items: AiClassifyItem[],
): Promise<AiClassifyResult[]> {
  if (topics.length === 0 || items.length === 0) return [];
  const { data, error } = await getSupabase().functions.invoke("classify-questions", {
    body: { topics, items },
  });
  if (error) throw new Error(error.message || "Gọi AI phân loại lỗi.");
  const results = (data as { results?: AiClassifyResult[] } | null)?.results;
  return Array.isArray(results) ? results : [];
}
