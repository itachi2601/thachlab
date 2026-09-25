import { getSupabase } from "@/services/supabase";

// ============================================================
// Mức độ thành thạo (mastery) theo YCCĐ — nhánh feat/mastery, 25/9/2026.
// Đọc docs/mastery-rules.md trước khi sửa file này (ngưỡng nhãn, công thức
// earned/max, vì sao câu tầng Bài không lộ ra thành một dòng YCCĐ riêng).
// RPC: supabase/migrations/20260925160000_mastery.sql (get_lesson_mastery,
// get_chapter_mastery) — CHƯA chạy lên production, xem feat/MASTERY_REPORT.md.
// ============================================================

export type MasteryLevel = "mastered" | "practicing" | "weak" | "insufficient";

export const MASTERY_LABEL: Record<MasteryLevel, string> = {
  mastered: "Nắm vững",
  practicing: "Cần luyện thêm",
  weak: "Chưa đạt",
  insufficient: "Chưa đủ dữ liệu",
};

export const MASTERY_ICON: Record<MasteryLevel, string> = {
  mastered: "✅",
  practicing: "🟡",
  weak: "🔴",
  insufficient: "⚪",
};

/** tone cho components/ui/Badge.tsx — dùng đúng bảng màu design system hiện có. */
export const MASTERY_TONE: Record<MasteryLevel, "success" | "warning" | "error" | "neutral"> = {
  mastered: "success",
  practicing: "warning",
  weak: "error",
  insufficient: "neutral",
};

/** Cần luyện thêm — dùng để quyết định có hiện nút "Luyện 10 câu phần này" không. */
export function needsPractice(level: MasteryLevel): boolean {
  return level === "weak" || level === "practicing";
}

/** Số câu tối thiểu cần thêm để đủ dữ liệu tính nhãn — khớp ngưỡng "< 4 lượt" trong RPC. */
export const MIN_ANSWERS_FOR_LABEL = 4;

export interface TopicMastery {
  topicId: number;
  topicName: string;
  sortOrder: number;
  answeredCount: number;
  level: MasteryLevel;
  /** % đúng trên tối đa 10 lượt gần nhất, null khi "insufficient" hoặc chưa có lượt nào. */
  pct: number | null;
}

export interface LessonMastery {
  topics: TopicMastery[];
  /** Nhãn thấp nhất trong các nhóm đủ dữ liệu (kể cả câu gắn thẳng tầng Bài không lộ ra topics[]). */
  lessonLevel: MasteryLevel;
}

interface LessonMasteryRow {
  topic_id: number | null;
  topic_name: string | null;
  sort_order: number;
  answered_count: number | null;
  level: MasteryLevel;
  pct: number | null;
  is_summary: boolean;
}

/**
 * Nhãn mastery từng YCCĐ của một bài + nhãn tổng của cả bài, cho học sinh đang đăng nhập.
 * Ném lỗi khi RPC chưa tồn tại/lỗi mạng — nơi gọi tự quyết định ẩn thẻ hay báo lỗi, KHÔNG tự
 * nuốt lỗi thành "Chưa đủ dữ liệu" ở đây (dễ hiểu nhầm là học sinh chưa làm bài, trong khi thực
 * ra là RPC chưa chạy).
 */
export async function fetchLessonMastery(lessonId: number): Promise<LessonMastery> {
  const { data, error } = await getSupabase().rpc("get_lesson_mastery", { p_lesson: lessonId });
  if (error) throw error;
  const rows = (data ?? []) as LessonMasteryRow[];
  const summary = rows.find((r) => r.is_summary);
  const topics = rows
    .filter((r) => !r.is_summary)
    .map((r) => ({
      topicId: r.topic_id as number,
      topicName: r.topic_name ?? "",
      sortOrder: r.sort_order,
      answeredCount: r.answered_count ?? 0,
      level: r.level,
      pct: r.pct,
    }));
  return { topics, lessonLevel: summary?.level ?? "insufficient" };
}

interface ChapterMasteryRow {
  lesson_id: number;
  lesson_title: string;
  sort_order: number;
  level: MasteryLevel;
}

/**
 * Nhãn mastery từng bài trong một chương, cho học sinh đang đăng nhập — 1 dòng/bài.
 * Ném lỗi khi RPC chưa tồn tại — nơi gọi (app/lop-hoc/page.tsx) tự bắt và bỏ qua lặng lẽ, vì đây
 * chỉ là icon trang trí cạnh tên bài, không phải nội dung chính.
 */
export async function fetchChapterMastery(chapterId: number): Promise<Map<number, MasteryLevel>> {
  const { data, error } = await getSupabase().rpc("get_chapter_mastery", { p_chapter: chapterId });
  if (error) throw error;
  const map = new Map<number, MasteryLevel>();
  for (const row of (data ?? []) as ChapterMasteryRow[]) map.set(row.lesson_id, row.level);
  return map;
}
