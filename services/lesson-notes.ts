import { getSupabase } from "@/services/supabase";

/** Một ghi chú của em ở một mục (h2/h3) của bài. `at` = ms lúc sửa cuối, để chọn bản mới hơn khi gộp máy ↔ tài khoản. */
export interface LessonNote {
  heading: string;
  body: string;
  at: number;
}

export type LessonNotes = Record<string, LessonNote>;

// Bảng lesson_notes (migration 20261024190000) có thể chưa chạy hoặc mạng lỗi: lỗi lần nào thì tắt đồng bộ
// tới khi tải lại trang, ghi chú vẫn lưu trên máy — không bao giờ làm hỏng trang bài.
let remoteOff = false;

async function currentUserId(): Promise<string | null> {
  const { data } = await getSupabase().auth.getSession();
  return data.session?.user.id ?? null;
}

/** Ghi chú đã lưu trên tài khoản cho bài này; null nếu chưa đăng nhập hoặc chưa đồng bộ được. */
export async function fetchRemoteNotes(lessonId: number): Promise<LessonNotes | null> {
  if (remoteOff) return null;
  try {
    const userId = await currentUserId();
    if (!userId) return null;
    const { data, error } = await getSupabase()
      .from("lesson_notes")
      .select("heading_id, heading_text, body, updated_at")
      .eq("user_id", userId)
      .eq("lesson_id", lessonId);
    if (error) throw error;
    const out: LessonNotes = {};
    for (const row of data ?? []) {
      out[row.heading_id as string] = {
        heading: (row.heading_text as string) ?? "",
        body: row.body as string,
        at: Date.parse(row.updated_at as string) || 0,
      };
    }
    return out;
  } catch {
    remoteOff = true;
    return null;
  }
}

/** Ghi (hoặc xoá, nếu rỗng) ghi chú của một mục lên tài khoản. Im lặng khi lỗi. */
export async function pushRemoteNote(lessonId: number, headingId: string, note: LessonNote): Promise<void> {
  if (remoteOff) return;
  try {
    const userId = await currentUserId();
    if (!userId) return;
    const table = getSupabase().from("lesson_notes");
    const { error } = note.body.trim()
      ? await table.upsert({
          user_id: userId,
          lesson_id: lessonId,
          heading_id: headingId,
          heading_text: note.heading.slice(0, 200),
          body: note.body,
          updated_at: new Date(note.at).toISOString(),
        })
      : await table.delete().eq("user_id", userId).eq("lesson_id", lessonId).eq("heading_id", headingId);
    if (error) throw error;
  } catch {
    remoteOff = true;
  }
}
