// Phía thầy/trợ giảng của "Đố vui lớp học" — bộ câu (quiz_sets), mở phòng, điều khiển, tìm câu trong ngân hàng.
import { type QuizQuestion } from "@/features/quiz-live/text";
import type { HostState } from "@/features/quiz-live/types";
import { getSupabase } from "@/services/supabase";

export interface QuizSet {
  id: number;
  title: string;
  grade: string;
  questions: QuizQuestion[];
  updatedAt: string;
  bankedAt: string | null;
}

interface SetRow {
  id: number;
  title: string;
  grade: string;
  questions: QuizQuestion[];
  updated_at: string;
  banked_at: string | null;
}

const fromRow = (r: SetRow): QuizSet => ({
  id: r.id,
  title: r.title,
  grade: r.grade,
  questions: Array.isArray(r.questions) ? r.questions : [],
  updatedAt: r.updated_at,
  bankedAt: r.banked_at,
});

async function rpc<T>(fn: string, args: Record<string, unknown>): Promise<T> {
  const { data, error } = await getSupabase().rpc(fn, args);
  if (error) throw new Error(error.message);
  return data as T;
}

export async function fetchQuizSets(): Promise<QuizSet[]> {
  const { data, error } = await getSupabase()
    .from("quiz_sets")
    .select("id, title, grade, questions, updated_at, banked_at")
    .order("updated_at", { ascending: false })
    .limit(100);
  if (error) throw new Error(error.message);
  return ((data as SetRow[]) ?? []).map(fromRow);
}

export async function saveQuizSet(
  id: number | null,
  v: { title: string; grade: string; questions: QuizQuestion[] },
): Promise<number> {
  const sb = getSupabase();
  const row = { title: v.title.trim(), grade: v.grade, questions: v.questions, updated_at: new Date().toISOString() };
  if (id === null) {
    const { data, error } = await sb.from("quiz_sets").insert(row).select("id").single();
    if (error) throw new Error(error.message);
    return (data as { id: number }).id;
  }
  const { error } = await sb.from("quiz_sets").update(row).eq("id", id);
  if (error) throw new Error(error.message);
  return id;
}

export async function deleteQuizSet(id: number): Promise<void> {
  const { error } = await getSupabase().from("quiz_sets").delete().eq("id", id);
  if (error) throw new Error(error.message);
}

export const createRoom = (setId: number, timeLimit: number) =>
  rpc<{ room_id: number; pin: string }>("quiz_host_create", { p_set: setId, p_time_limit: timeLimit });
export const getHostState = (room: number) => rpc<HostState>("quiz_host_state", { p_room: room });
export const advanceRoom = (room: number) => rpc<void>("quiz_host_advance", { p_room: room });
export const kickPlayer = (room: number, player: number) => rpc<void>("quiz_host_kick", { p_room: room, p_player: player });
export const endRoom = (room: number) => rpc<void>("quiz_host_end", { p_room: room });

export interface BankHit {
  id: number;
  grade: string;
  topic_id: number | null;
  topic_name: string;
  difficulty: string;
  question: unknown;
}

export const searchBank = (f: { grade: string; topicId: number | null; difficulty: string; search: string; limit: number; random: boolean }) =>
  rpc<BankHit[]>("quiz_bank_search", {
    p_grade: f.grade,
    p_topic_id: f.topicId,
    p_difficulty: f.difficulty,
    p_search: f.search,
    p_limit: f.limit,
    p_random: f.random,
  });

export const setToBank = (setId: number, grade: string, topicName: string, form: string) =>
  rpc<{ added: number; skipped: number }>("quiz_set_to_bank", {
    p_set: setId,
    p_grade: grade,
    p_topic_name: topicName,
    p_form: form,
  });
