import type { RealtimeChannel } from "@supabase/supabase-js";
import { getSupabase } from "@/services/supabase";

export type CncMillingQuizAttemptStatus =
  | "in_progress"
  | "passed"
  | "failed";

export type CncMillingQuizAttempt = {
  id: number;
  course_id: number | null;
  student_id: string | null;
  participant_key: string;
  participant_name: string;
  class_name: string;
  answers: Record<string, number>;
  answered_count: number;
  score: number;
  total_questions: number;
  status: CncMillingQuizAttemptStatus;
  started_at: string;
  last_activity_at: string;
  submitted_at: string | null;
  profiles?: { full_name: string; class_name: string } | null;
};

const SELECT_FIELDS =
  "id, course_id, student_id, participant_key, participant_name, class_name, answers, answered_count, score, total_questions, status, started_at, last_activity_at, submitted_at";

function getParticipantKey(courseId?: number) {
  const storageKey = `cnc-milling-live-participant-${courseId ?? "legacy"}`;
  const existing = window.localStorage.getItem(storageKey);
  if (existing) return existing;
  const created = window.crypto.randomUUID();
  window.localStorage.setItem(storageKey, created);
  return created;
}

export async function saveCncMillingQuizAttempt({
  courseId,
  participantName,
  className,
  answers,
  score,
  totalQuestions,
  status,
}: {
  courseId?: number;
  participantName: string;
  className: string;
  answers: Record<string, number>;
  score: number;
  totalQuestions: number;
  status: CncMillingQuizAttemptStatus;
}) {
  // Ghi qua RPC theo participant_key: bảng không còn cho ghi thẳng (migration 20261111200000) vì policy cũ
  // để ai cũng sửa được bài của người khác. student_id do server lấy từ phiên đăng nhập.
  const { error } = await getSupabase().rpc("cnc_milling_quiz_save", {
    p_course_id: courseId ?? null,
    p_participant_key: getParticipantKey(courseId),
    p_participant_name: participantName,
    p_class_name: className,
    p_answers: answers,
    p_score: score,
    p_total: totalQuestions,
    p_status: status,
  });
  if (error) throw error;
}

export async function fetchAllCncMillingQuizAttempts() {
  const { data, error } = await getSupabase()
    .from("cnc_milling_quiz_attempts")
    .select(
      `${SELECT_FIELDS}, profiles!cnc_milling_quiz_attempts_student_id_fkey(full_name, class_name)`,
    )
    .order("last_activity_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((item) => ({
    ...item,
    profiles: Array.isArray(item.profiles)
      ? (item.profiles[0] ?? null)
      : item.profiles,
  })) as CncMillingQuizAttempt[];
}

export async function resetAllCncMillingQuizAttempts() {
  const { error } = await getSupabase()
    .from("cnc_milling_quiz_attempts")
    .delete()
    .gte("id", 0);
  if (error) throw error;
}

export function subscribeToCncMillingQuizAttempts(
  onChange: () => void,
): RealtimeChannel {
  return getSupabase()
    .channel("cnc-milling-quiz-live-monitor")
    .on(
      "postgres_changes",
      {
        event: "*",
        schema: "public",
        table: "cnc_milling_quiz_attempts",
      },
      onChange,
    )
    .subscribe();
}

export async function unsubscribeFromCncMillingQuizAttempts(
  channel: RealtimeChannel,
) {
  await getSupabase().removeChannel(channel);
}
