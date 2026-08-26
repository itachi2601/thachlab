import { getSupabase } from "@/services/supabase";

export type AttendanceStatus = "present" | "late" | "excused" | "absent";

export interface ThptAttendanceSession {
  id: number;
  class_id: number;
  title: string;
  session_date: string;
  starts_at: string;
  note: string;
}

const SESSION_FIELDS = "id, class_id, title, session_date, starts_at, note";

export interface ThptAttendanceRecord {
  session_id: number;
  student_id: string;
  status: AttendanceStatus;
  note: string;
  marked_at: string;
  profiles?: { full_name: string; class_name: string } | null;
}

export async function fetchAttendanceSessions(classId: number) {
  const { data, error } = await getSupabase().from("thpt_attendance_sessions")
    .select(SESSION_FIELDS).eq("class_id", classId).order("starts_at", { ascending: false });
  if (error) throw error;
  return (data ?? []) as ThptAttendanceSession[];
}

export async function createAttendanceSession(input: { classId: number; title: string; sessionDate: string }) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { data, error } = await supabase.from("thpt_attendance_sessions").insert({
    class_id: input.classId, created_by: auth.user?.id ?? null,
    title: input.title.trim(), session_date: input.sessionDate,
  }).select(SESSION_FIELDS).single();
  if (error) throw error;
  return data as ThptAttendanceSession;
}

export async function updateAttendanceSessionNote(sessionId: number, note: string) {
  const { error } = await getSupabase().from("thpt_attendance_sessions").update({ note }).eq("id", sessionId);
  if (error) throw error;
}

export async function fetchAttendanceRecords(sessionId: number) {
  const { data, error } = await getSupabase().from("thpt_attendance_records")
    .select("session_id, student_id, status, note, marked_at, profiles!thpt_attendance_records_student_id_fkey(full_name, class_name)")
    .eq("session_id", sessionId);
  if (error) throw error;
  return (data ?? []).map((row) => ({ ...row, profiles: Array.isArray(row.profiles) ? row.profiles[0] ?? null : row.profiles })) as ThptAttendanceRecord[];
}

export async function setAttendanceRecord(sessionId: number, studentId: string, status: AttendanceStatus) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase.from("thpt_attendance_records").upsert(
    { session_id: sessionId, student_id: studentId, status, marked_by: auth.user?.id ?? null, marked_at: new Date().toISOString() },
    { onConflict: "session_id,student_id" },
  );
  if (error) throw error;
}

export async function setAttendanceRecordNote(sessionId: number, studentId: string, note: string) {
  const { error } = await getSupabase().from("thpt_attendance_records").update({ note }).eq("session_id", sessionId).eq("student_id", studentId);
  if (error) throw error;
}
