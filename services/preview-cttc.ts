import { getSupabase } from "@/services/supabase";

export interface PreviewCttcCourse {
  subject: "cnc" | "tien-phay" | "gddd-ptnn";
  course_id: number | null;
  course_name: string | null;
}

/** Ghi danh tài khoản admin hiện tại vào khóa mới nhất của 3 môn CTTC (RPC chỉ cho admin). */
export async function previewCttcEnroll(): Promise<PreviewCttcCourse[]> {
  const { data, error } = await getSupabase().rpc("preview_cttc_enroll");
  if (error) throw error;
  return (data ?? []) as PreviewCttcCourse[];
}

/** Gỡ các ghi danh thử đó — trả về số dòng đã xoá. */
export async function previewCttcUnenroll(): Promise<number> {
  const { data, error } = await getSupabase().rpc("preview_cttc_unenroll");
  if (error) throw error;
  return (data ?? 0) as number;
}
