import { getSupabase } from "@/services/supabase";
import { compressImageFile } from "@/services/image-compress";

const AVATAR_BUCKET = "avatars";
const AVATAR_MAX_DIMENSION = 480;

export async function updateMyAvatar(studentId: string, file: File) {
  if (!file.type.startsWith("image/")) throw new Error("Chỉ nhận file ảnh (PNG, JPEG, WEBP).");
  const supabase = getSupabase();
  const compressed = await compressImageFile(file, { maxDimension: AVATAR_MAX_DIMENSION });
  const safeName = compressed.name.replace(/[^a-zA-Z0-9.\-_]/g, "_");
  const path = `${studentId}/${Date.now()}-${Math.random().toString(36).slice(2, 8)}-${safeName}`;
  const { error: uploadError } = await supabase.storage
    .from(AVATAR_BUCKET)
    .upload(path, compressed, { contentType: compressed.type || "image/jpeg", upsert: false });
  if (uploadError) throw uploadError;

  const { data } = supabase.storage.from(AVATAR_BUCKET).getPublicUrl(path);
  const { error } = await supabase.from("profiles").update({ avatar_url: data.publicUrl }).eq("id", studentId);
  if (error) {
    await supabase.storage.from(AVATAR_BUCKET).remove([path]);
    throw error;
  }
  return data.publicUrl;
}

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
