/**
 * Gọi Edge Function `check-exam`: AI tự giải rồi đối chiếu đáp án/lời giải từng câu trước khi đăng.
 * Kết quả chỉ là gợi ý cho giáo viên — không tự sửa câu nào.
 */
import { getSupabase } from "@/services/supabase";

export type AiVerdict = "ok" | "nghi_ngo" | "loi";

export interface AiCheckItem {
  index: number;
  text: string;
}
export interface AiCheckResult {
  index: number;
  verdict: AiVerdict;
  note: string;
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
