import { getSupabase } from "@/services/supabase";

export interface DailyStreak {
  current: number; // số ngày liên tiếp đã học, tính đến hôm nay hoặc hôm qua
  activeToday: boolean;
}

function localDateKey(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

/**
 * Chuỗi ngày học liên tiếp: gộp ngày làm đề (exam_results) và ngày xem
 * lý thuyết/video/bài tập (lesson_progress) — hoạt động ở ngày nào cũng tính.
 */
export async function fetchStudyStreak(userId: string): Promise<DailyStreak> {
  const supabase = getSupabase();
  const [{ data: examRows }, { data: progressRows }] = await Promise.all([
    supabase.from("exam_results").select("created_at").eq("student_id", userId),
    supabase.from("lesson_progress").select("done_at").eq("user_id", userId),
  ]);

  const days = new Set<string>();
  for (const r of examRows ?? []) days.add(localDateKey(new Date((r as { created_at: string }).created_at)));
  for (const r of progressRows ?? []) days.add(localDateKey(new Date((r as { done_at: string }).done_at)));

  const cursor = new Date();
  const activeToday = days.has(localDateKey(cursor));
  if (!activeToday) cursor.setDate(cursor.getDate() - 1);

  let current = 0;
  while (days.has(localDateKey(cursor))) {
    current += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return { current, activeToday };
}
