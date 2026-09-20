import { getSupabase } from "@/services/supabase";

export async function fetchMyStudentCode(studentId: string) {
  const { data, error } = await getSupabase().from("profiles").select("student_code").eq("id", studentId).single();
  if (error) throw error;
  return (data?.student_code as string | null) ?? "";
}

export async function updateMyStudentCode(studentId: string, studentCode: string) {
  const normalized = studentCode.trim().toUpperCase();
  if (normalized.length < 2 || normalized.length > 30) throw new Error("Mã số sinh viên phải có từ 2 đến 30 ký tự.");
  const { error } = await getSupabase().from("profiles").update({ student_code: normalized }).eq("id", studentId);
  if (error) throw error;
  return normalized;
}

export async function fetchStudentCodes(studentIds: string[]) {
  if (!studentIds.length) return new Map<string, string>();
  const { data, error } = await getSupabase().from("profiles").select("id, student_code").in("id", studentIds);
  if (error) throw error;
  return new Map((data ?? []).map((row) => [row.id as string, (row.student_code as string | null) ?? ""]));
}

export interface StudentRosterInfo {
  studentCode: string;
  /** dd/mm/yyyy, đúng định dạng cột "Ngày Sinh" trong file mẫu. */
  birthDate: string;
}

/**
 * Đặt lại mật khẩu cho học sinh không tự dùng được /quen-mat-khau (tài khoản @thachlab.local,
 * không có email thật). Chạy qua Edge Function vì cần service_role key — xem
 * supabase/functions/reset-student-password/index.ts.
 */
export async function resetStudentPassword(studentId: string, classId: number, newPassword: string) {
  const { data, error } = await getSupabase().functions.invoke("reset-student-password", {
    body: { studentId, classId, newPassword },
  });
  if (error) {
    const message = error instanceof Error ? error.message : String(error);
    if (/failed to send a request|failed to fetch|non-2xx/i.test(message)) {
      throw new Error(
        "Chưa gọi được Edge Function \"reset-student-password\" trên Supabase — nhiều khả năng " +
          "function chưa được deploy. Xem docs/deploy-edge-function.md.",
      );
    }
    throw error instanceof Error ? error : new Error(message);
  }
  if (data?.error) throw new Error(data.error as string);
}

export async function fetchStudentRosterInfo(studentIds: string[]) {
  if (!studentIds.length) return new Map<string, StudentRosterInfo>();
  const { data, error } = await getSupabase().from("profiles").select("id, student_code, birth_date").in("id", studentIds);
  if (error) throw error;
  return new Map((data ?? []).map((row) => {
    const iso = row.birth_date as string | null;
    const match = iso ? /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso) : null;
    return [row.id as string, {
      studentCode: (row.student_code as string | null) ?? "",
      birthDate: match ? `${match[3]}/${match[2]}/${match[1]}` : "",
    }];
  }));
}
