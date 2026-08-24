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
