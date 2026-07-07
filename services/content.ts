import type { Difficulty } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

export interface ExamMeta {
  id: number;
  title: string;
  duration_minutes: number;
  question_count: number;
  topic: string;
  difficulty: Difficulty;
  created_at: string;
  classIds: number[];
}

export interface PostMeta {
  id: number;
  created_at: string;
  title: string;
  body: string;
  video_url: string;
  classIds: number[];
}

interface ClassRef {
  class_id: number;
}

export async function fetchPublishedExams(): Promise<ExamMeta[]> {
  const { data } = await getSupabase()
    .from("exams")
    .select(
      "id, title, duration_minutes, question_count, topic, difficulty, created_at, exam_classes(class_id)",
    )
    .eq("published", true)
    .order("created_at", { ascending: false });
  return (data ?? []).map((e) => ({
    ...e,
    classIds: ((e.exam_classes as ClassRef[]) ?? []).map((c) => c.class_id),
  })) as ExamMeta[];
}

export async function fetchPublishedPosts(): Promise<PostMeta[]> {
  const { data } = await getSupabase()
    .from("posts")
    .select(
      "id, created_at, title, body, video_url, post_classes(class_id)",
    )
    .eq("published", true)
    .order("created_at", { ascending: false });
  return (data ?? []).map((p) => ({
    ...p,
    classIds: ((p.post_classes as ClassRef[]) ?? []).map((c) => c.class_id),
  })) as PostMeta[];
}

/** Nội dung không gán lớp = toàn trường; có gán = phải trùng lớp người xem. */
export function visibleTo(itemClassIds: number[], myClassIds: number[] | null) {
  if (itemClassIds.length === 0) return true;
  if (myClassIds === null) return true; // admin / chưa lọc
  return itemClassIds.some((id) => myClassIds.includes(id));
}
