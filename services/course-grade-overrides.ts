import { getSupabase } from "@/services/supabase";

export interface CourseGradeOverride {
  course_id: number;
  student_id: string;
  grade_key: string;
  score: number;
  updated_at: string;
}

export async function fetchCourseGradeOverrides(courseId: number) {
  const { data, error } = await getSupabase().from("course_grade_overrides")
    .select("course_id, student_id, grade_key, score, updated_at")
    .eq("course_id", courseId);
  if (error) throw error;
  return (data ?? []) as CourseGradeOverride[];
}

export async function setCourseGradeOverride(courseId: number, studentId: string, gradeKey: string, score: number) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { error } = await supabase.from("course_grade_overrides").upsert({
    course_id: courseId,
    student_id: studentId,
    grade_key: gradeKey,
    score: gradeKey === "bonus" ? Math.min(10, Math.max(-10, score)) : Math.min(10, Math.max(0, score)),
    updated_by: auth.user?.id ?? null,
    updated_at: new Date().toISOString(),
  }, { onConflict: "course_id,student_id,grade_key" });
  if (error) throw error;
}
