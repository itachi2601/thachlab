import { getSupabase } from "@/services/supabase";

export interface ClassExamResult {
  id: number;
  created_at: string;
  score: number;
  duration_seconds: number;
  exam_id: number;
  student_id: string;
  exams: { title: string } | null;
}

/** Kết quả kiểm tra của các học sinh thuộc 1 khối lớp — dùng cho dashboard giáo viên THPT. */
export async function fetchClassExamResults(studentIds: string[], sinceIso?: string): Promise<ClassExamResult[]> {
  if (studentIds.length === 0) return [];
  let query = getSupabase().from("exam_results")
    .select("id, created_at, score, duration_seconds, exam_id, student_id, exams(title)")
    .in("student_id", studentIds);
  if (sinceIso) query = query.gte("created_at", sinceIso);
  const { data, error } = await query.order("created_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((row) => ({ ...row, exams: Array.isArray(row.exams) ? row.exams[0] ?? null : row.exams })) as ClassExamResult[];
}
