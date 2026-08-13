import { getSupabase } from "@/services/supabase";

export type AttendanceStatus = "present" | "late" | "excused" | "absent";

export interface AttendanceSession {
  id: number; course_id: number; title: string; session_date: string; starts_at: string;
  closes_at: string; late_after: string; code: string; status: "open" | "closed"; created_at: string;
}

export interface AttendanceRecord {
  session_id: number; student_id: string; status: AttendanceStatus; checked_in_at: string | null;
  note: string; profiles?: { full_name: string; class_name: string } | null;
}

export async function fetchAttendanceSessions(courseId: number) {
  const { data, error } = await getSupabase().from("attendance_sessions").select("id, course_id, title, session_date, starts_at, closes_at, late_after, code, status, created_at").eq("course_id", courseId).order("starts_at", { ascending: false });
  if (error) throw error;
  return (data ?? []) as AttendanceSession[];
}

export async function createAttendanceSession(input: { courseId: number; title: string; startsAt: string; durationMinutes: number; lateMinutes: number }) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const start = new Date(input.startsAt);
  const code = String(crypto.getRandomValues(new Uint32Array(1))[0] % 1_000_000).padStart(6, "0");
  const { data, error } = await supabase.from("attendance_sessions").insert({
    course_id: input.courseId, created_by: auth.user?.id, title: input.title.trim(),
    session_date: start.toISOString().slice(0, 10), starts_at: start.toISOString(),
    late_after: new Date(start.getTime() + input.lateMinutes * 60_000).toISOString(),
    closes_at: new Date(start.getTime() + input.durationMinutes * 60_000).toISOString(), code, status: "open",
  }).select("id, course_id, title, session_date, starts_at, closes_at, late_after, code, status, created_at").single();
  if (error) throw error;
  return data as AttendanceSession;
}

export async function closeAttendanceSession(sessionId: number) {
  const { error } = await getSupabase().from("attendance_sessions").update({ status: "closed", closes_at: new Date().toISOString() }).eq("id", sessionId);
  if (error) throw error;
}

export async function fetchAttendanceRecords(sessionId: number) {
  const { data, error } = await getSupabase().from("attendance_records").select("session_id, student_id, status, checked_in_at, note, profiles!attendance_records_student_id_fkey(full_name, class_name)").eq("session_id", sessionId);
  if (error) throw error;
  return (data ?? []).map((row) => ({ ...row, profiles: Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles })) as AttendanceRecord[];
}

export async function setAttendanceRecord(sessionId: number, studentId: string, status: AttendanceStatus, note = "") {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase.from("attendance_records").upsert({ session_id: sessionId, student_id: studentId, status, note, marked_by: auth.user?.id, checked_in_at: status === "present" || status === "late" ? new Date().toISOString() : null }, { onConflict: "session_id,student_id" });
  if (error) throw error;
}

export async function submitAttendanceCode(courseId: number, code: string) {
  const { data, error } = await getSupabase().rpc("submit_attendance_code", { p_course_id: courseId, p_code: code.trim() });
  if (error) throw error;
  return data as { status: AttendanceStatus; session_title: string; checked_in_at: string };
}

export async function fetchMyAttendance(courseId: number, studentId: string) {
  const { data, error } = await getSupabase().from("attendance_records").select("session_id, student_id, status, checked_in_at, note, attendance_sessions!inner(id, course_id, title, session_date, starts_at)").eq("student_id", studentId).eq("attendance_sessions.course_id", courseId).order("checked_in_at", { ascending: false });
  if (error) throw error;
  return data ?? [];
}
