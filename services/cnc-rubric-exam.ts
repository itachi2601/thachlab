import { getSupabase } from "@/services/supabase";
import type { RubricLevel } from "@/services/cnc-rubric";

export type RubricExamMachine = "tien" | "phay";
export type RubricExamRole = "self" | "teacher";

export interface RubricExamAttempt {
  id: number;
  course_id: number;
  student_id: string;
  machine: RubricExamMachine;
  role: RubricExamRole;
  grader_id: string | null;
  item_levels: Record<string, RubricLevel>;
  zero_tolerance_confirmed: Record<number, boolean>;
  ky_thuat_score: number;
  thanh_phan_score: number;
  total_score: number;
  xep_loai: string;
  notes: string;
  created_at: string;
  updated_at: string;
  profiles?: { full_name: string; class_name: string } | null;
}

const FIELDS = "id, course_id, student_id, machine, role, grader_id, item_levels, zero_tolerance_confirmed, ky_thuat_score, thanh_phan_score, total_score, xep_loai, notes, created_at, updated_at";

export interface RubricExamSubmission {
  courseId: number;
  studentId: string;
  machine: RubricExamMachine;
  itemLevels: Record<string, RubricLevel>;
  zeroToleranceConfirmed: Record<number, boolean>;
  kyThuatScore: number;
  thanhPhanScore: number;
  totalScore: number;
  xepLoai: string;
  notes: string;
}

export async function fetchMyRubricExamAttempts(courseId: number, machine: RubricExamMachine) {
  const supabase = getSupabase();
  const { data: authData } = await supabase.auth.getUser();
  if (!authData.user) return [];
  const { data, error } = await supabase
    .from("rubric_exam_attempts")
    .select(FIELDS)
    .eq("course_id", courseId)
    .eq("student_id", authData.user.id)
    .eq("machine", machine);
  if (error) throw error;
  return (data ?? []) as RubricExamAttempt[];
}

export async function fetchRubricExamAttemptsForStudent(courseId: number, studentId: string, machine: RubricExamMachine) {
  const { data, error } = await getSupabase()
    .from("rubric_exam_attempts")
    .select(FIELDS)
    .eq("course_id", courseId)
    .eq("student_id", studentId)
    .eq("machine", machine);
  if (error) throw error;
  return (data ?? []) as RubricExamAttempt[];
}

export async function fetchRubricExamAttemptsByCourse(courseId: number, machine: RubricExamMachine) {
  const { data, error } = await getSupabase()
    .from("rubric_exam_attempts")
    .select(`${FIELDS}, profiles!rubric_exam_attempts_student_id_fkey(full_name, class_name)`)
    .eq("course_id", courseId)
    .eq("machine", machine)
    .order("updated_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((item) => ({
    ...item,
    profiles: Array.isArray(item.profiles) ? (item.profiles[0] ?? null) : item.profiles,
  })) as RubricExamAttempt[];
}

export async function submitSelfRubricAssessment(input: RubricExamSubmission) {
  const supabase = getSupabase();
  const { data: authData, error: authError } = await supabase.auth.getUser();
  if (authError || !authData.user) throw new Error("Hãy đăng nhập bằng tài khoản sinh viên trước khi tự đánh giá.");
  const payload = {
    course_id: input.courseId,
    student_id: authData.user.id,
    machine: input.machine,
    role: "self" as const,
    grader_id: null,
    item_levels: input.itemLevels,
    zero_tolerance_confirmed: input.zeroToleranceConfirmed,
    ky_thuat_score: input.kyThuatScore,
    thanh_phan_score: input.thanhPhanScore,
    total_score: input.totalScore,
    xep_loai: input.xepLoai,
    notes: input.notes.trim(),
    updated_at: new Date().toISOString(),
  };
  const { data, error } = await supabase
    .from("rubric_exam_attempts")
    .upsert(payload, { onConflict: "course_id,student_id,machine,role" })
    .select(FIELDS)
    .single();
  if (error) throw error;
  return data as RubricExamAttempt;
}

export async function submitTeacherRubricGrade(input: RubricExamSubmission) {
  const supabase = getSupabase();
  const { data: authData, error: authError } = await supabase.auth.getUser();
  if (authError || !authData.user) throw new Error("Phiên đăng nhập quản trị không hợp lệ.");

  const payload = {
    course_id: input.courseId,
    student_id: input.studentId,
    machine: input.machine,
    role: "teacher" as const,
    grader_id: authData.user.id,
    item_levels: input.itemLevels,
    zero_tolerance_confirmed: input.zeroToleranceConfirmed,
    ky_thuat_score: input.kyThuatScore,
    thanh_phan_score: input.thanhPhanScore,
    total_score: input.totalScore,
    xep_loai: input.xepLoai,
    notes: input.notes.trim(),
    updated_at: new Date().toISOString(),
  };
  const { data, error } = await supabase
    .from("rubric_exam_attempts")
    .upsert(payload, { onConflict: "course_id,student_id,machine,role" })
    .select(FIELDS)
    .single();
  if (error) throw error;

  const lessonId = input.machine === "tien" ? "lesson-5" : "lesson-6";
  const passed = !input.xepLoai.startsWith("Không đạt");
  const { error: recordError } = await supabase.from("cnc_learning_records").upsert({
    course_id: input.courseId,
    student_id: input.studentId,
    lesson_id: lessonId,
    assessment_id: "rubric-exam",
    completed: passed,
    latest_score: Math.round(input.totalScore),
    best_score: Math.round(input.totalScore),
    total_questions: 10,
    attempt_count: 1,
    last_activity_at: new Date().toISOString(),
  }, { onConflict: "course_id,student_id,lesson_id,assessment_id" });
  if (recordError) throw recordError;

  return data as RubricExamAttempt;
}
