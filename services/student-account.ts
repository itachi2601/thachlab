import { getSupabase } from "./supabase";

export interface StudentAccountInfo {
  login_email: string | null;
  username: string | null;
  contact_email: string | null;
  phone: string | null;
  parent_phone: string | null;
  birth_date: string | null;
  gender: string | null;
  student_code: string | null;
  created_at: string | null;
  last_sign_in_at: string | null;
  from_roster: boolean;
}

/** Thông tin tài khoản học sinh cho admin / giáo viên phụ trách (RPC tự kiểm quyền). */
export async function fetchStudentAccount(studentId: string): Promise<StudentAccountInfo | null> {
  const { data, error } = await getSupabase().rpc("staff_student_account", { p_student: studentId });
  if (error) {
    const message = typeof error.message === "string" && error.message ? error.message : "Chưa đọc được thông tin tài khoản.";
    throw new Error(message);
  }
  const row = Array.isArray(data) ? data[0] : data;
  return (row as StudentAccountInfo | undefined) ?? null;
}
