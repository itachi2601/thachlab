import { getSupabase } from "@/services/supabase";

export type LearningActivityType = "lesson" | "video" | "document" | "practice" | "exam";

export async function heartbeatLearningPresence(input: {
  studentId: string;
  lessonId: number;
  activityType?: LearningActivityType;
  openedAt: string;
}) {
  const { error } = await getSupabase().from("student_learning_presence").upsert({
    student_id: input.studentId,
    lesson_id: input.lessonId,
    activity_type: input.activityType ?? "lesson",
    lesson_opened_at: input.openedAt,
    last_seen_at: new Date().toISOString(),
  }, { onConflict: "student_id" });
  if (error) throw error;
}

export interface ClassLearningPresence {
  studentId: string;
  fullName: string;
  className: string;
  lessonId: number | null;
  lessonTitle: string;
  chapterTitle: string;
  activityType: LearningActivityType;
  lessonOpenedAt: string;
  lastSeenAt: string;
}

export async function fetchClassLearningPresence(classId: number): Promise<ClassLearningPresence[]> {
  const supabase = getSupabase();
  const { data: members, error: memberError } = await supabase
    .from("user_classes")
    .select("user_id")
    .eq("class_id", classId)
    .eq("status", "active");
  if (memberError) throw memberError;
  const studentIds = (members ?? []).map((row) => row.user_id as string);
  if (!studentIds.length) return [];

  const { data, error } = await supabase
    .from("student_learning_presence")
    .select("student_id, lesson_id, activity_type, lesson_opened_at, last_seen_at, profiles!student_learning_presence_student_id_fkey(full_name, class_name), lessons(title, chapters(title))")
    .in("student_id", studentIds)
    .gte("last_seen_at", new Date(Date.now() - 15 * 60_000).toISOString())
    .order("last_seen_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((row) => {
    const profileValue = Array.isArray(row.profiles) ? row.profiles[0] : row.profiles;
    const lessonValue = Array.isArray(row.lessons) ? row.lessons[0] : row.lessons;
    const chapterValue = lessonValue && (Array.isArray(lessonValue.chapters) ? lessonValue.chapters[0] : lessonValue.chapters);
    return {
      studentId: row.student_id,
      fullName: profileValue?.full_name ?? "Học sinh",
      className: profileValue?.class_name ?? "",
      lessonId: row.lesson_id,
      lessonTitle: lessonValue?.title ?? "Đang xem chương trình học",
      chapterTitle: chapterValue?.title ?? "",
      activityType: row.activity_type as LearningActivityType,
      lessonOpenedAt: row.lesson_opened_at,
      lastSeenAt: row.last_seen_at,
    };
  });
}

export interface LiveStudySummary {
  /** 0 khi dưới 3 em — xem `few`. */
  total: number;
  /** 1–2 em đang học: chỉ hiện "vài bạn", không lộ số cụ thể. */
  few: boolean;
  topics: { lessonId: number; title: string; n: number }[];
}

let liveCache: { at: number; value: LiveStudySummary } | null = null;

/** Toàn trường, ẩn danh. Cache 60 giây trong tab để nhiều thẻ cùng trang không gọi lặp. */
export async function fetchLiveStudySummary(): Promise<LiveStudySummary> {
  if (liveCache && Date.now() - liveCache.at < 60_000) return liveCache.value;
  const { data, error } = await getSupabase().rpc("live_study_summary");
  if (error) throw error;
  const raw = (data ?? {}) as { total?: number; few?: boolean; topics?: { lesson_id: number; title: string; n: number }[] };
  const value: LiveStudySummary = {
    total: raw.total ?? 0,
    few: !!raw.few,
    topics: (raw.topics ?? []).map((t) => ({ lessonId: t.lesson_id, title: t.title, n: t.n })),
  };
  liveCache = { at: Date.now(), value };
  return value;
}
