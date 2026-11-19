// Dữ liệu riêng của học sinh trên trang /lop-hoc/bai — MỘT RPC gộp get_lesson_page_student
// (migration 20261118150000) thay 7 truy vấn: thông tin đề (exams ×2), lesson_progress,
// exam_results(+điểm), exam_attempts đang dở, practice_sessions, get_lesson_mastery.
// RPC chưa chạy trên DB (hoặc lỗi) → tự lùi về đúng đường cũ và nhớ lại cho các lần mở bài sau
// trong cùng lượt tải trang, không gọi thử RPC lặp lại.

import { isGradedKind, type LessonItem } from "@/features/lessons/types";
import { fetchExamMetas, type LessonExamMeta } from "@/services/lessons";
import { lessonMasteryFromRows, type LessonMastery, type LessonMasteryRow } from "@/services/mastery";
import {
  fetchMyLessonPageProgress,
  lessonPageProgressFromRpc,
  type ItemProgress,
  type LessonPageRpcRows,
} from "@/services/progress";
import { getSupabase } from "@/services/supabase";

interface RpcPayload extends LessonPageRpcRows {
  v: number;
  exams: (LessonExamMeta & { pass_score: number | null; published: boolean })[];
  mastery: LessonMasteryRow[] | null;
}

export interface LessonPageStudentData {
  /** null = lỗi tải thông tin đề (ExamRow hiện "không tải được"). */
  examMetas: Map<number, LessonExamMeta> | null;
  /** null = lỗi tải tiến độ (giữ trạng thái chưa làm như cũ). */
  progress: { progress: Map<number, ItemProgress>; scores: Map<number, number>; done: Set<number> } | null;
  /** undefined = RPC gộp không chạy → LessonMasteryCard tự gọi get_lesson_mastery như cũ. */
  mastery: LessonMastery | null | undefined;
}

let rpcUnavailable = false;

async function viaRpc(lessonId: number, studentId: string, items: LessonItem[]): Promise<LessonPageStudentData | null> {
  if (rpcUnavailable) return null;
  const { data, error } = await getSupabase().rpc("get_lesson_page_student", { p_lesson: lessonId });
  const payload = data as RpcPayload | null;
  if (error || !payload || payload.v !== 1) {
    // Chỉ nhớ "không có RPC" khi hàm chưa tồn tại trên DB; lỗi mạng/phiên chớp nhoáng thì lần sau thử lại.
    if (!error || error.code === "PGRST202" || error.code === "42883") rpcUnavailable = true;
    return null;
  }
  const graded = new Set(items.filter((i) => isGradedKind(i.kind)).flatMap((i) => i.exam_ids));
  const examMetas = new Map<number, LessonExamMeta>();
  for (const e of payload.exams ?? []) {
    if (!e.published || !graded.has(e.id)) continue;
    examMetas.set(e.id, {
      id: e.id,
      title: e.title,
      duration_minutes: e.duration_minutes,
      question_count: e.question_count,
      type_counts: e.type_counts,
      pass_score: e.pass_score ?? null,
    });
  }
  return {
    examMetas,
    progress: lessonPageProgressFromRpc(studentId, items, {
      progress: payload.progress ?? [],
      results: payload.results ?? [],
      open_attempts: payload.open_attempts ?? [],
      practice: payload.practice ?? [],
      exams: payload.exams ?? [],
    }),
    mastery: payload.mastery ? lessonMasteryFromRows(payload.mastery) : null,
  };
}

/** Đường cũ (trước RPC gộp): thông tin đề + tiến độ song song; mastery để LessonMasteryCard tự tải. */
async function viaTables(studentId: string, items: LessonItem[]): Promise<LessonPageStudentData> {
  const examIds = items.filter((i) => isGradedKind(i.kind)).flatMap((i) => i.exam_ids);
  const [examMetas, progress] = await Promise.all([
    examIds.length === 0 ? Promise.resolve(new Map<number, LessonExamMeta>()) : fetchExamMetas(examIds).catch(() => null),
    fetchMyLessonPageProgress(studentId, items).catch(() => null),
  ]);
  return { examMetas, progress, mastery: undefined };
}

export async function fetchLessonPageStudent(
  lessonId: number,
  studentId: string,
  items: LessonItem[],
): Promise<LessonPageStudentData> {
  try {
    const rpc = await viaRpc(lessonId, studentId, items);
    if (rpc) return rpc;
  } catch {
    /* lỗi mạng: lùi về đường cũ cho lần này */
  }
  return viaTables(studentId, items);
}
