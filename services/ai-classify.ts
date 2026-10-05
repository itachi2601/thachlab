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

const BATCH_SIZE = 10;
const CONCURRENCY = 4;

/**
 * Chia danh sách câu thành lô nhỏ (10 câu) và gọi song song (4 lô cùng lúc) thay vì một request 60 câu
 * — mỗi lô trả về sớm hơn nhiều, và `onProgress(đã xong, tổng)` cho giao diện hiện tiến độ.
 * Lô lỗi không làm mất kết quả các lô khác; chỉ ném lỗi khi MỌI lô đều lỗi.
 */
export async function classifyQuestionTagsBatched(
  topics: string[],
  items: AiClassifyItem[],
  onProgress?: (done: number, total: number) => void,
): Promise<AiClassifyResult[]> {
  if (topics.length === 0 || items.length === 0) return [];
  const chunks: AiClassifyItem[][] = [];
  for (let i = 0; i < items.length; i += BATCH_SIZE) chunks.push(items.slice(i, i + BATCH_SIZE));
  const out: AiClassifyResult[] = [];
  let done = 0;
  let failed = 0;
  let lastError: unknown = null;
  let next = 0;
  onProgress?.(0, items.length);
  async function worker() {
    while (next < chunks.length) {
      const chunk = chunks[next++];
      try {
        out.push(...(await classifyQuestionTags(topics, chunk)));
      } catch (e) {
        failed++;
        lastError = e;
      }
      done += chunk.length;
      onProgress?.(done, items.length);
    }
  }
  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, chunks.length) }, worker));
  if (failed === chunks.length) throw lastError instanceof Error ? lastError : new Error("Gọi AI phân loại lỗi.");
  return out;
}
