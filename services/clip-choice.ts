// Thống kê lựa chọn Dự đoán ở khung video thí nghiệm — chỉ số đếm theo lớp, không có tên HS
// (RPC teacher_clip_choice_stats, migration 20261030120000_clip_choice).

import { getSupabase } from "@/services/supabase";

export type ClipChoiceStat = {
  tn_id: string;
  lesson_id: number;
  class_students: number;
  n: number;
  n_chon: number;
  n_bo_qua: number;
  n_a: number;
  n_b: number;
  n_c: number;
  n_d: number;
  n_dung: number;
  last_at: string | null;
};

export async function fetchClipChoiceStats(classId: number): Promise<ClipChoiceStat[]> {
  const { data, error } = await getSupabase().rpc("teacher_clip_choice_stats", { p_class_id: classId });
  if (error) throw new Error(error.message);
  return (data as ClipChoiceStat[]) ?? [];
}
