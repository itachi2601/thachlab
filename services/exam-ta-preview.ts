import { getSupabase } from "@/services/supabase";

/** Đường dẫn trợ giảng làm thử một đề (giữ `?exam=` — trang /tro-giang/xem-truoc đọc đúng tham số này). */
export function taPreviewPath(examId: number, classId?: number): string {
  return `/tro-giang/xem-truoc/?exam=${examId}${classId ? `&class=${classId}` : ""}`;
}

export interface TaPreviewRow {
  exam_id: number;
  class_id: number;
  sent_at: string;
  exams: { title: string; questions: unknown[] | null } | null;
  classes: { name: string } | null;
}

/** Lớp nào đã được gửi đề này (để panel hiện sẵn tick). */
export async function fetchTaPreviewClassIds(examId: number): Promise<number[]> {
  const { data, error } = await getSupabase().from("exam_ta_previews").select("class_id").eq("exam_id", examId);
  if (error) throw error;
  return (data ?? []).map((r) => r.class_id as number);
}

/** Đặt danh sách lớp được gửi đề: thêm lớp mới tick, bỏ lớp bỏ tick. */
export async function setTaPreviewClasses(examId: number, classIds: number[]): Promise<void> {
  const supabase = getSupabase();
  const current = await fetchTaPreviewClassIds(examId);
  const add = classIds.filter((id) => !current.includes(id));
  const drop = current.filter((id) => !classIds.includes(id));
  if (add.length) {
    const { error } = await supabase.from("exam_ta_previews").insert(add.map((class_id) => ({ exam_id: examId, class_id })));
    if (error) throw error;
  }
  if (drop.length) {
    const { error } = await supabase.from("exam_ta_previews").delete().eq("exam_id", examId).in("class_id", drop);
    if (error) throw error;
  }
}

/** Các đề thầy đã gửi cho trợ giảng, mới nhất trước. */
export async function fetchMyTaPreviews(): Promise<TaPreviewRow[]> {
  const { data, error } = await getSupabase()
    .from("exam_ta_previews")
    .select("exam_id, class_id, sent_at, exams(title, questions), classes(name)")
    .order("sent_at", { ascending: false });
  if (error) throw error;
  return (data ?? []) as unknown as TaPreviewRow[];
}

export async function fetchPreviewExam(examId: number) {
  const { data, error } = await getSupabase()
    .from("exams")
    .select("id, title, duration_minutes, published, questions")
    .eq("id", examId)
    .single();
  if (error || !data) throw error ?? new Error("Không tìm thấy đề đã gửi.");
  return data;
}
