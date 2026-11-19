import { getSupabase } from "@/services/supabase";

export type CncGradeModule = "tien" | "phay";

export interface CncGradeCriterion {
  name: string;
  level: string | null; // E/G/P/F
  points: number | null;
  max: number;
}

export interface CncGrade {
  course_id: number;
  module: CncGradeModule;
  ky_thuat: number | null;
  thanh_phan: number | null;
  total: number;
  grade: string | null;
  detail: { criteria?: CncGradeCriterion[]; violations?: string[] };
  graded_at: string;
}

// RLS chỉ trả dòng của chính người đăng nhập (admin thấy hết).
export async function fetchMyCncGrades(studentId: string): Promise<CncGrade[]> {
  const { data, error } = await getSupabase()
    .from("cnc_grades")
    .select("course_id, module, ky_thuat, thanh_phan, total, grade, detail, graded_at")
    .eq("student_id", studentId);
  if (error) throw new Error(error.message);
  return (data ?? []) as CncGrade[];
}
