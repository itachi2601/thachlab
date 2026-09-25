/**
 * Gắn ảnh (đồ thị / hình vẽ) cho một câu đã nằm trong ngân hàng câu hỏi.
 *
 * Luồng: nén ảnh trong trình duyệt → upload bucket lesson-media (thư mục bank/<id>) →
 * RPC bank_set_question_figure chèn <img> vào câu dẫn của dòng ngân hàng VÀ vào mọi
 * exams.questions đang dùng câu đó (xem docs/supabase-migration-question-bank-figure.sql).
 * Upload xong mà RPC lỗi thì gỡ ảnh vừa tải để Storage không rác.
 */
import type { ExamQuestion } from "@/features/exams/types";
import { compressImageFile } from "@/services/image-compress";
import { removeLessonMedia, uploadLessonMedia } from "@/services/lesson-media";
import { getSupabase } from "@/services/supabase";

export interface SetFigureResult {
  question: ExamQuestion;
  contentHash: string;
  examsUpdated: number;
}

function fileToDataUri(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => resolve(String(fr.result));
    fr.onerror = () => reject(fr.error);
    fr.readAsDataURL(file);
  });
}

export async function attachFigureToBankQuestion(bankId: number, file: File): Promise<SetFigureResult> {
  if (!/^image\//.test(file.type)) throw new Error("Chỉ nhận file ảnh (PNG/JPG/WebP/GIF/SVG).");
  const sb = getSupabase();
  const skipCompress = file.type === "image/svg+xml" || file.type === "image/gif";
  const compressed = skipCompress ? file : await compressImageFile(file, { maxDimension: 1400, quality: 0.8 });
  const dataUri = await fileToDataUri(compressed);
  const media = await uploadLessonMedia(sb, `bank/${bankId}`, [
    { name: compressed.name || file.name || "hinh.png", dataUri, placeholder: "media/hinh" },
  ]);
  const url = media[0]?.url;
  if (!url) throw new Error("Upload ảnh không trả về URL.");
  const html = `<img src="${url}" alt="Hình" class="mx-auto my-2 max-w-full rounded-lg" />`;
  const { data, error } = await sb.rpc("bank_set_question_figure", { p_bank_id: bankId, p_img_html: html });
  if (error) {
    await removeLessonMedia(sb, media.map((m) => m.storagePath)).catch(() => {});
    throw new Error(error.message);
  }
  const r = data as { question: ExamQuestion; content_hash: string; exams_updated: number };
  return { question: r.question, contentHash: r.content_hash, examsUpdated: r.exams_updated ?? 0 };
}
