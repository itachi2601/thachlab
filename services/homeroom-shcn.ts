import { getSupabase } from "@/services/supabase";

// Sinh hoạt chủ nhiệm: điểm danh hàng ngày do lớp trưởng nhập + nội dung sinh hoạt tuần.
// Site xuất tĩnh nên không có API route: mọi ràng buộc quyền (chỉ lớp mình, chỉ ngày hôm nay)
// nằm ở RLS trong docs/supabase-migration-shcn.sql, đây chỉ là lớp truy vấn.

export type MonitorRole = "lop_truong" | "lop_pho";

export const MONITOR_ROLE_LABEL: Record<MonitorRole, string> = {
  lop_truong: "Lớp trưởng",
  lop_pho: "Lớp phó",
};

/** Vắng từ ngần này buổi trong tuần thì GVCN được cảnh báo. Ngưỡng tạm, chờ thầy/cô chốt. */
export const ABSENCE_ALERT_THRESHOLD = 3;

export interface HomeroomMonitor {
  course_id: number;
  student_id: string;
  role: MonitorRole;
  assigned_at: string;
  profiles?: { full_name: string; class_name: string } | null;
}

export interface AbsentEntry {
  /** null khi sinh viên chưa có tài khoản trên web — vẫn ghi được tên. */
  student_id: string | null;
  full_name: string;
  reason: string;
}

export interface DailyAttendance {
  id: number;
  course_id: number;
  attendance_date: string;
  headcount: number;
  present_count: number;
  absentees: AbsentEntry[];
  submitted_by: string | null;
  submitted_at: string;
  updated_at: string;
}

export interface WeeklySession {
  id: number;
  course_id: number;
  week_no: number;
  met_on: string | null;
  announcements: { tieu_de: string; ghi_chu?: string }[];
  ethics_topic: string;
  ethics_taught: string[];
  headcount: number | null;
  present_count: number | null;
  created_at: string;
  updated_at: string;
}

const DAILY_FIELDS =
  "id, course_id, attendance_date, headcount, present_count, absentees, submitted_by, submitted_at, updated_at";
const WEEKLY_FIELDS =
  "id, course_id, week_no, met_on, announcements, ethics_topic, ethics_taught, headcount, present_count, created_at, updated_at";

/**
 * Ngày hôm nay theo giờ Việt Nam, dạng YYYY-MM-DD — phải khớp public.vn_today() của RLS, nếu
 * lấy theo UTC thì từ 0h đến 7h sáng trình duyệt sẽ gửi lên ngày hôm qua và bị chặn.
 */
export function vnToday(): string {
  return new Date().toLocaleDateString("sv-SE", { timeZone: "Asia/Ho_Chi_Minh" });
}

/**
 * Cộng/trừ ngày trên chuỗi YYYY-MM-DD. Tính bằng UTC để kết quả không đổi theo múi giờ máy
 * người dùng (ngày ở đây luôn là ngày lịch, không phải một mốc thời gian).
 */
export function shiftDate(date: string, days: number): string {
  const [year, month, day] = date.split("-").map(Number);
  return new Date(Date.UTC(year, month - 1, day + days)).toISOString().slice(0, 10);
}

/** Thứ Hai → Chủ nhật của tuần chứa `date` (dạng YYYY-MM-DD). */
export function weekRange(date: string): { from: string; to: string } {
  const [year, month, day] = date.split("-").map(Number);
  const offset = (new Date(Date.UTC(year, month - 1, day)).getUTCDay() + 6) % 7; // Chủ nhật (0) là ngày thứ 7.
  const from = shiftDate(date, -offset);
  return { from, to: shiftDate(from, 6) };
}

// ---------- Lớp trưởng / lớp phó ----------

export async function fetchHomeroomMonitors(courseId: number) {
  const { data, error } = await getSupabase()
    .from("homeroom_monitors")
    .select("course_id, student_id, role, assigned_at, profiles!homeroom_monitors_student_id_fkey(full_name, class_name)")
    .eq("course_id", courseId)
    .order("role");
  if (error) throw error;
  return (data ?? []).map((row) => ({
    ...row,
    profiles: Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles,
  })) as HomeroomMonitor[];
}

export async function setHomeroomMonitor(courseId: number, studentId: string, role: MonitorRole) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase.from("homeroom_monitors").upsert(
    { course_id: courseId, student_id: studentId, role, assigned_by: auth.user?.id ?? null },
    { onConflict: "course_id,student_id" },
  );
  if (error) throw error;
}

export async function removeHomeroomMonitor(courseId: number, studentId: string) {
  const { error } = await getSupabase()
    .from("homeroom_monitors")
    .delete()
    .eq("course_id", courseId)
    .eq("student_id", studentId);
  if (error) throw error;
}

/** Các lớp mà sinh viên đang đăng nhập được giao điểm danh (thường đúng 1 lớp). */
export async function fetchMyMonitorRoles(studentId: string) {
  const { data, error } = await getSupabase()
    .from("homeroom_monitors")
    .select("course_id, role")
    .eq("student_id", studentId);
  if (error) throw error;
  return (data ?? []) as { course_id: number; role: MonitorRole }[];
}

// ---------- Điểm danh hàng ngày ----------

export async function fetchDailyAttendance(courseId: number, fromDate: string, toDate: string) {
  const { data, error } = await getSupabase()
    .from("homeroom_daily_attendance")
    .select(DAILY_FIELDS)
    .eq("course_id", courseId)
    .gte("attendance_date", fromDate)
    .lte("attendance_date", toDate)
    .order("attendance_date", { ascending: false });
  if (error) throw error;
  return (data ?? []) as DailyAttendance[];
}

export async function fetchDailyAttendanceOn(courseId: number, date: string) {
  const { data, error } = await getSupabase()
    .from("homeroom_daily_attendance")
    .select(DAILY_FIELDS)
    .eq("course_id", courseId)
    .eq("attendance_date", date)
    .maybeSingle();
  if (error) throw error;
  return (data ?? null) as DailyAttendance | null;
}

/**
 * Lớp trưởng nộp/sửa điểm danh. RLS chỉ cho ghi khi `date` đúng ngày hôm nay theo giờ VN và
 * người ghi là lớp trưởng/lớp phó của lớp; GVCN thì ghi được mọi ngày.
 */
export async function submitDailyAttendance(input: {
  courseId: number;
  date: string;
  headcount: number;
  absentees: AbsentEntry[];
}) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const absentees = input.absentees
    .map((item) => ({ ...item, full_name: item.full_name.trim(), reason: item.reason.trim() }))
    .filter((item) => item.full_name);
  const { error } = await supabase.from("homeroom_daily_attendance").upsert(
    {
      course_id: input.courseId,
      attendance_date: input.date,
      headcount: input.headcount,
      present_count: Math.max(0, input.headcount - absentees.length),
      absentees,
      submitted_by: auth.user?.id ?? null,
      updated_at: new Date().toISOString(),
    },
    { onConflict: "course_id,attendance_date" },
  );
  if (error) throw error;
}

/** Đếm số buổi vắng của từng sinh viên trong khoảng đã tải — dùng cho cảnh báo của GVCN. */
export function absenceTally(rows: DailyAttendance[]) {
  const tally = new Map<string, { name: string; days: string[]; reasons: string[] }>();
  for (const row of rows) {
    for (const entry of row.absentees ?? []) {
      const key = entry.student_id ?? entry.full_name.toLocaleLowerCase("vi-VN");
      const current = tally.get(key) ?? { name: entry.full_name, days: [], reasons: [] };
      current.days.push(row.attendance_date);
      if (entry.reason) current.reasons.push(entry.reason);
      tally.set(key, current);
    }
  }
  return [...tally.values()].toSorted((a, b) => b.days.length - a.days.length);
}

// ---------- Nội dung sinh hoạt tuần ----------

export async function fetchWeeklySessions(courseId: number) {
  const { data, error } = await getSupabase()
    .from("homeroom_weekly_sessions")
    .select(WEEKLY_FIELDS)
    .eq("course_id", courseId)
    .order("week_no", { ascending: false });
  if (error) throw error;
  return (data ?? []) as WeeklySession[];
}

export async function upsertWeeklySession(input: {
  courseId: number;
  weekNo: number;
  metOn: string | null;
  announcements: { tieu_de: string; ghi_chu?: string }[];
  ethicsTopic: string;
  ethicsTaught: string[];
  headcount: number | null;
  presentCount: number | null;
}) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const announcements = input.announcements
    .map((item) => ({ tieu_de: item.tieu_de.trim(), ...(item.ghi_chu?.trim() ? { ghi_chu: item.ghi_chu.trim() } : {}) }))
    .filter((item) => item.tieu_de)
    .slice(0, 5);
  const { error } = await supabase.from("homeroom_weekly_sessions").upsert(
    {
      course_id: input.courseId,
      week_no: input.weekNo,
      met_on: input.metOn || null,
      announcements,
      ethics_topic: input.ethicsTopic.trim(),
      ethics_taught: input.ethicsTaught.map((item) => item.trim()).filter(Boolean),
      headcount: input.headcount,
      present_count: input.presentCount,
      created_by: auth.user?.id ?? null,
      updated_at: new Date().toISOString(),
    },
    { onConflict: "course_id,week_no" },
  );
  if (error) throw error;
}

export async function deleteWeeklySession(id: number) {
  const { error } = await getSupabase().from("homeroom_weekly_sessions").delete().eq("id", id);
  if (error) throw error;
}

/**
 * Sĩ số / có mặt điền sẵn cho biên bản tuần: ưu tiên đúng ngày sinh hoạt, không có thì lấy
 * trung bình các ngày lớp trưởng đã điểm danh trong tuần.
 */
export function prefillHeadcount(rows: DailyAttendance[], metOn: string | null) {
  if (!rows.length) return null;
  const exact = metOn ? rows.find((row) => row.attendance_date === metOn) : undefined;
  if (exact) return { headcount: exact.headcount, presentCount: exact.present_count, source: "day" as const };
  const avg = (values: number[]) => Math.round(values.reduce((sum, value) => sum + value, 0) / values.length);
  return {
    headcount: avg(rows.map((row) => row.headcount)),
    presentCount: avg(rows.map((row) => row.present_count)),
    source: "average" as const,
  };
}
