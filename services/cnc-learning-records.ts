import type { RealtimeChannel } from "@supabase/supabase-js";
import { getSupabase } from "@/services/supabase";

export type CncLearningRecord = {
  course_id: number; student_id: string; lesson_id: string; assessment_id: string; completed: boolean;
  latest_score: number | null; best_score: number | null; total_questions: number | null;
  attempt_count: number; last_activity_at: string;
};

const fields = "course_id, student_id, lesson_id, assessment_id, completed, latest_score, best_score, total_questions, attempt_count, last_activity_at";

export async function recordCncLearningResult(input: { courseId: number; lessonId: string; assessmentId?: string; score?: number; total?: number; completed?: boolean }) {
  const { error } = await getSupabase().rpc("record_cnc_learning_result", {
    p_course_id: input.courseId, p_lesson_id: input.lessonId,
    p_assessment_id: input.assessmentId ?? "final",
    p_score: input.score ?? null, p_total: input.total ?? null, p_completed: input.completed ?? false,
  });
  if (error) throw error;
}

export async function fetchCncLearningRecords(courseId: number, studentId?: string) {
  let query = getSupabase().from("cnc_learning_records").select(fields).eq("course_id", courseId);
  if (studentId) query = query.eq("student_id", studentId);
  const { data, error } = await query.order("last_activity_at", { ascending: false });
  if (error) throw error;
  return (data ?? []) as CncLearningRecord[];
}

export function subscribeToCncLearningRecords(courseId: number, onChange: () => void): RealtimeChannel {
  return getSupabase().channel(`cnc-learning-${courseId}`).on("postgres_changes", {
    event: "*", schema: "public", table: "cnc_learning_records", filter: `course_id=eq.${courseId}`,
  }, onChange).subscribe();
}

export async function unsubscribeFromCncLearningRecords(channel: RealtimeChannel) {
  await getSupabase().removeChannel(channel);
}
