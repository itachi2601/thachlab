import { getSupabase } from "@/services/supabase";
import type { TeacherNoteStatus, TeacherNoteTag } from "@/lib/teacher-note-labels";

export interface TeacherLessonNote {
  id: number;
  created_at: string;
  lesson_id: number;
  item_id: number | null;
  page_key: string;
  page_heading: string;
  tag: TeacherNoteTag;
  body: string;
  status: TeacherNoteStatus;
  resolution: string;
}

/** Lưu một ghi chú lúc dạy. RLS chỉ cho giáo viên/trợ giảng; user_id lấy từ auth.uid() ở DB. */
export async function addTeacherNote(input: {
  lessonId: number;
  itemId: number | null;
  pageKey: string;
  pageHeading: string;
  tag: TeacherNoteTag;
  body: string;
}): Promise<void> {
  const { error } = await getSupabase().from("teacher_lesson_notes").insert({
    lesson_id: input.lessonId,
    item_id: input.itemId,
    page_key: input.pageKey,
    page_heading: input.pageHeading,
    tag: input.tag,
    body: input.body.trim(),
  });
  if (error) throw error;
}
