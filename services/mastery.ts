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

// Cache 3 phút theo (tài khoản, chương), cùng kiểu cache rank_my_status ở services/rank.ts: 24/10/2026
// get_chapter_mastery bị gọi 66k lượt (~97 ms) vì mỗi lần mở /lop-hoc đều chạy lại. Nhãn chỉ là icon
// trang trí nên trễ vài phút không sao; { force: true } để bỏ qua cache.
const CHAPTER_MASTERY_CACHE_MS = 3 * 60 * 1000;
const chapterMasteryCache = new Map<string, { at: number; value: Promise<Map<number, MasteryLevel>> }>();

/**
 * Nhãn mastery từng bài trong một chương, cho học sinh đang đăng nhập — 1 dòng/bài.
 * Ném lỗi khi RPC chưa tồn tại — nơi gọi (app/lop-hoc/page.tsx) tự bắt và bỏ qua lặng lẽ, vì đây
 * chỉ là icon trang trí cạnh tên bài, không phải nội dung chính.
 */
export async function fetchChapterMastery(
  chapterId: number,
  opts?: { force?: boolean },
): Promise<Map<number, MasteryLevel>> {
  const { data: sess } = await getSupabase().auth.getSession();
  const key = `${sess.session?.user.id ?? ""}:${chapterId}`;
  const hit = chapterMasteryCache.get(key);
  if (!opts?.force && hit && Date.now() - hit.at < CHAPTER_MASTERY_CACHE_MS) return hit.value;
  const value = (async () => {
    const { data, error } = await getSupabase().rpc("get_chapter_mastery", { p_chapter: chapterId });
    if (error) throw error;
    const map = new Map<number, MasteryLevel>();
    for (const row of (data ?? []) as ChapterMasteryRow[]) map.set(row.lesson_id, row.level);
    return map;
  })();
  const entry = { at: Date.now(), value };
  chapterMasteryCache.set(key, entry);
  value.catch(() => {
    if (chapterMasteryCache.get(key) === entry) chapterMasteryCache.delete(key);
  });
  return value;
}

export interface WeakTopic {
  topicId: number;
  topicName: string;
  lessonId: number;
  lessonTitle: string;
  pct: number;
  level: MasteryLevel;
}

/**
 * Tối đa `limit` YCCĐ yếu nhất của học sinh đang đăng nhập (chỉ Chưa đạt / Cần luyện thêm, đủ ≥4 lượt).
 * 1 RPC gộp: supabase/migrations/20261005140000_weakest_topics.sql. Ném lỗi khi RPC chưa chạy —
 * nơi gọi (WeakestSkillsCard) tự ẩn thẻ.
 */
export async function fetchMyWeakestTopics(limit = 3): Promise<WeakTopic[]> {
  const { data, error } = await getSupabase().rpc("get_my_weakest_topics", { p_limit: limit });
  if (error) throw error;
  return ((data ?? []) as Array<{
    topic_id: number;
    topic_name: string;
    lesson_id: number;
    lesson_title: string;
    pct: number;
    level: MasteryLevel;
  }>).map((r) => ({
    topicId: r.topic_id,
    topicName: r.topic_name,
    lessonId: r.lesson_id,
    lessonTitle: r.lesson_title,
    pct: r.pct,
    level: r.level,
  }));
}

// ------------------------------------------------------------
// Sơ đồ mạng nhện năng lực theo bài trong chương đang học (13/10/2026).
// RPC: supabase/migrations/20261013150000_chapter_mastery_radar.sql.
// UI: components/results/ChapterMasteryRadar.tsx (xem docs/PROMPT-GEMINI-RADAR-NANG-LUC-2026-10-13.md).
// ------------------------------------------------------------
export interface ChapterLessonMastery {
  chapterId: number;
  chapterTitle: string;
  lessonId: number;
  lessonTitle: string;
  sortOrder: number;
  answeredCount: number;
  /** 0–100, null khi bài chưa có lượt nào. */
  pct: number | null;
  level: MasteryLevel;
  /** Chỉ có từ RPC cả khoá (get_my_course_mastery_pct). */
  chapterSort?: number;
  subjectCode?: string | null;
  isLatest?: boolean;
  /** Σ điểm đạt / Σ điểm tối đa của bài (để gộp % cả chương đúng công thức). */
  earned?: number;
  max?: number;
}

interface ChapterMasteryPctRow {
  chapter_id: number;
  chapter_title: string;
  lesson_id: number;
  lesson_title: string;
  sort_order: number;
  answered_count: number;
  pct: number | null;
  level: MasteryLevel;
}

/**
 * Tỉ lệ đúng từng bài của CHƯƠNG mà học sinh đang đăng nhập làm bài gần nhất (1 RPC).
 * `before` = mốc thời gian để lấy "chính em lúc đó" (ví dụ 30 ngày trước); bỏ trống = hiện tại.
 * Trả [] khi chưa làm bài nào. Ném lỗi khi RPC chưa chạy — nơi gọi tự ẩn thẻ.
 */
export async function fetchMyChapterMasteryPct(before?: Date): Promise<ChapterLessonMastery[]> {
  const { data, error } = await getSupabase().rpc("get_my_chapter_mastery_pct", {
    p_before: before ? before.toISOString() : null,
  });
  if (error) throw error;
  return ((data ?? []) as ChapterMasteryPctRow[]).map((r) => ({
    chapterId: r.chapter_id,
    chapterTitle: r.chapter_title,
    lessonId: r.lesson_id,
    lessonTitle: r.lesson_title,
    sortOrder: r.sort_order,
    answeredCount: r.answered_count,
    pct: r.pct,
    level: r.level,
  }));
}

interface CourseMasteryPctRow extends ChapterMasteryPctRow {
  chapter_sort: number;
  subject_code: string | null;
  is_latest: boolean;
  earned: number | string;
  max: number | string;
}

/**
 * Như fetchMyChapterMasteryPct nhưng trả MỌI bài đã công bố của khoá (các chương cùng môn, chung lớp
 * với chương em làm gần nhất) để sơ đồ chuyển được Theo chương / Cả khoá. Ném lỗi khi RPC chưa chạy —
 * nơi gọi lùi về fetchMyChapterMasteryPct.
 */
export async function fetchMyCourseMasteryPct(before?: Date): Promise<ChapterLessonMastery[]> {
  const { data, error } = await getSupabase().rpc("get_my_course_mastery_pct", {
    p_before: before ? before.toISOString() : null,
  });
  if (error) throw error;
  return ((data ?? []) as CourseMasteryPctRow[]).map((r) => ({
    chapterId: r.chapter_id,
    chapterTitle: r.chapter_title,
    lessonId: r.lesson_id,
    lessonTitle: r.lesson_title,
    sortOrder: r.sort_order,
    answeredCount: r.answered_count,
    pct: r.pct,
    level: r.level,
    chapterSort: r.chapter_sort,
    subjectCode: r.subject_code,
    isLatest: r.is_latest,
    earned: Number(r.earned),
    max: Number(r.max),
  }));
}
