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

export interface CourseCncGrade extends CncGrade {
  student_id: string;
  updated_at: string;
}

// Giảng viên (is_admin) đọc bảng điểm cả lớp một module.
export async function fetchCourseCncGrades(courseId: number, module: CncGradeModule): Promise<CourseCncGrade[]> {
  const { data, error } = await getSupabase()
    .from("cnc_grades")
    .select("course_id, student_id, module, ky_thuat, thanh_phan, total, grade, detail, graded_at, updated_at")
    .eq("course_id", courseId)
    .eq("module", module);
  if (error) throw new Error(error.message);
  return (data ?? []) as CourseCncGrade[];
}

export const CNC_GRADES_HREF = "/lop-hoc/cnc/bang-diem/";

/**
 * Gửi điểm chính thức cho MỘT SV: ghi cnc_grades (SV xem ở /lop-hoc/cnc/bang-diem/) + chuông thông báo.
 * Ghi cnc_grades cần migration 20261128100000_cnc_grades_giang_vien_ghi (policy is_admin()).
 */
export async function publishCncGrade(input: {
  courseId: number;
  studentId: string;
  module: CncGradeModule;
  row: { ky_thuat: number; thanh_phan: number; total: number; grade: string; detail: CncGrade["detail"] };
  body: string;
  isUpdate: boolean;
}) {
  const supabase = getSupabase();
  const now = new Date().toISOString();
  const { error } = await supabase.from("cnc_grades").upsert({
    course_id: input.courseId,
    student_id: input.studentId,
    module: input.module,
    ...input.row,
    graded_at: now,
    updated_at: now,
  }, { onConflict: "course_id,student_id,module" });
  if (error) throw new Error(error.message);
  const mod = input.module === "tien" ? "tiện" : "phay";
  const { error: ne } = await supabase.rpc("notify_user_staff", {
    p_user: input.studentId,
    p_kind: `diem-thi-${input.module}-cnc`,
    p_title: input.isUpdate ? `Điểm thi ${mod} CNC đã cập nhật` : `Điểm thi ${mod} CNC`,
    p_body: input.body,
    p_href: CNC_GRADES_HREF,
  });
  // Điểm đã ghi; thông báo hỏng không làm mất điểm — báo lại để giảng viên biết.
  if (ne) throw new Error(`Đã ghi điểm nhưng chưa gửi được thông báo: ${ne.message}`);
}
