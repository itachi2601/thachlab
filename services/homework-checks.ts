import { getSupabase } from "@/services/supabase";

// ============================================================
// Trợ giảng/giáo viên chấm % học sinh đã làm BTVN ngay trên lớp — cộng RP theo tỉ lệ.
// Xem docs/supabase-migration-homework-check.sql.
// ============================================================

export interface HomeworkCheck {
  studentId: string;
  percent: number;
  checkedAt: string;
}

/** % đã chấm của mỗi em cho một bài tập về nhà (announcement_id) — để prefill UI. */
export async function fetchHomeworkChecks(announcementId: number): Promise<Record<string, HomeworkCheck>> {
  const { data, error } = await getSupabase()
    .from("class_homework_checks")
    .select("student_id, percent, checked_at")
    .eq("announcement_id", announcementId);
  if (error) throw error;
  const out: Record<string, HomeworkCheck> = {};
  for (const row of data ?? []) {
    out[row.student_id as string] = {
      studentId: row.student_id as string,
      percent: row.percent as number,
      checkedAt: row.checked_at as string,
    };
  }
  return out;
}

/** Chấm % đã làm cho một em — RP chỉ cộng khi truyền seasonId (lớp đang có mùa rank mở). */
export async function setHomeworkCheck(input: {
  announcementId: number;
  studentId: string;
  percent: number;
  seasonId?: number | null;
}): Promise<void> {
  const { error } = await getSupabase().rpc("homework_check_set", {
    p_announcement_id: input.announcementId,
    p_student_id: input.studentId,
    p_percent: input.percent,
    p_season: input.seasonId ?? null,
  });
  if (error) throw error;
}
