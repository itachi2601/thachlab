import { getSupabase } from "@/services/supabase";

export interface ChecklistSession {
  id: number; course_id: number; lesson_id: "lesson-4-turn" | "lesson-4-mill"; title: string;
  starts_at: string; closes_at: string; code: string; status: "open" | "closed"; created_at: string;
}

export interface ChecklistAttempt {
  id: number; session_id: number; course_id: number; lesson_id: string; student_id: string;
  grader_id: string | null; grader_role: "teacher" | "peer"; item_results: Record<string, boolean>;
  score: number; total: number; critical_ok: boolean; zero_tolerance_ok: boolean; passed: boolean; created_at: string;
}

export interface Classmate { student_id: string; full_name: string; class_name: string }

export async function startChecklistAttempt(input:{courseId:number;code:string;studentId:string;lessonId:string}){const{data,error}=await getSupabase().rpc("start_checklist_attempt",{p_course_id:input.courseId,p_code:input.code,p_student_id:input.studentId,p_lesson_id:input.lessonId});if(error)throw error;return data as{started_at:string;minimum_submit_at:string}}

export async function fetchChecklistSessions(courseId: number, lessonId?: string) {
  let query = getSupabase().from("checklist_sessions").select("id, course_id, lesson_id, title, starts_at, closes_at, code, status, created_at").eq("course_id", courseId);
  if (lessonId) query = query.eq("lesson_id", lessonId);
  const { data, error } = await query.order("starts_at", { ascending: false });
  if (error) throw error;
  return (data ?? []) as ChecklistSession[];
}

export async function createChecklistSession(input: { courseId: number; lessonId: "lesson-4-turn" | "lesson-4-mill"; title: string; startsAt: string; durationMinutes: number }) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const start = new Date(input.startsAt);
  const code = String(crypto.getRandomValues(new Uint32Array(1))[0] % 1_000_000).padStart(6, "0");
  const { data, error } = await supabase.from("checklist_sessions").insert({
    course_id: input.courseId, lesson_id: input.lessonId, created_by: auth.user?.id, title: input.title.trim(),
    starts_at: start.toISOString(), closes_at: new Date(start.getTime() + input.durationMinutes * 60_000).toISOString(),
    code, status: "open",
  }).select("id, course_id, lesson_id, title, starts_at, closes_at, code, status, created_at").single();
  if (error) throw error;
  return data as ChecklistSession;
}

export async function closeChecklistSession(sessionId: number) {
  const { error } = await getSupabase().from("checklist_sessions").update({ status: "closed", closes_at: new Date().toISOString() }).eq("id", sessionId);
  if (error) throw error;
}

export async function fetchCourseClassmates(courseId: number) {
  const { data, error } = await getSupabase().rpc("list_cnc_course_classmates", { p_course_id: courseId });
  if (error) throw error;
  return (data ?? []) as Classmate[];
}

export async function submitChecklistResult(input: {
  courseId: number; code: string; studentId: string; lessonId: string; itemResults: Record<string, boolean>;
  score: number; criticalOk: boolean; zeroToleranceOk: boolean; passed: boolean;
}) {
  const { data, error } = await getSupabase().rpc("submit_checklist_result", {
    p_course_id: input.courseId, p_code: input.code, p_student_id: input.studentId, p_lesson_id: input.lessonId,
    p_item_results: input.itemResults, p_score: input.score, p_critical_ok: input.criticalOk,
    p_zero_tolerance_ok: input.zeroToleranceOk, p_passed: input.passed,
  });
  if (error) throw error;
  return data as { passed: boolean; score: number; grader_role: "teacher" | "peer"; session_title: string };
}

export async function fetchChecklistAttempts(courseId: number, options?: { studentId?: string; sessionId?: number }) {
  let query = getSupabase().from("checklist_attempts").select("id, session_id, course_id, lesson_id, student_id, grader_id, grader_role, item_results, score, total, critical_ok, zero_tolerance_ok, passed, created_at").eq("course_id", courseId);
  if (options?.studentId) query = query.eq("student_id", options.studentId);
  if (options?.sessionId) query = query.eq("session_id", options.sessionId);
  const { data, error } = await query.order("created_at", { ascending: false });
  if (error) throw error;
  return (data ?? []) as ChecklistAttempt[];
}
