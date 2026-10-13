import { getSupabase } from "@/services/supabase";

/** Tiến trình bài dạy theo khoá (thầy + trợ giảng dùng chung). RPC: migration 20261013230000 / 233000. */

export interface TeachingCourse {
  id: number;
  name: string;
  classId: number;
  className: string;
  schoolYear: string;
  status: string;
  startsAt: string | null;
  endsAt: string | null;
  currentTopicId: number | null;
  schedules: { weekday: number; start: string; end: string; location: string }[];
}

export interface TaughtMark {
  topicId: number;
  taughtOn: string;
  weekStart: string;
  by: string | null;
}

export interface TeachingNote {
  id: number;
  topicId: number;
  body: string;
  schoolYear: string;
  courseId: number | null;
  createdAt: string;
  mine: boolean;
  author: string | null;
}

export interface TeachingState {
  currentTopicId: number | null;
  progress: TaughtMark[];
  notes: TeachingNote[];
}

function fail(error: { message?: string } | null, fallback: string): never {
  throw new Error(error?.message?.trim() || fallback);
}

export async function fetchTeachingCourses(classId?: number | null): Promise<TeachingCourse[]> {
  const { data, error } = await getSupabase().rpc("teaching_courses", { p_class: classId ?? null });
  if (error) fail(error, "Chưa đọc được danh sách khoá.");
  return (data ?? []) as TeachingCourse[];
}

export async function fetchTeachingState(courseId: number): Promise<TeachingState> {
  const { data, error } = await getSupabase().rpc("teaching_get", { p_course: courseId });
  if (error) fail(error, "Chưa đọc được tiến trình dạy.");
  return data as TeachingState;
}

export async function setTaught(courseId: number, topicId: number, taught: boolean, on?: string): Promise<void> {
  const { error } = await getSupabase().rpc("teaching_set", { p_course: courseId, p_topic: topicId, p_taught: taught, p_on: on ?? null });
  if (error) fail(error, "Chưa lưu được.");
}

export async function addTeachingNote(courseId: number, topicId: number, body: string): Promise<void> {
  const { error } = await getSupabase().rpc("teaching_note_add", { p_course: courseId, p_topic: topicId, p_body: body });
  if (error) fail(error, "Chưa lưu được ghi chú.");
}

export async function deleteTeachingNote(id: number): Promise<void> {
  const { error } = await getSupabase().rpc("teaching_note_delete", { p_id: id });
  if (error) fail(error, "Chưa xoá được ghi chú.");
}

/** Thầy mời em đã có trong lớp làm kiểm tra đầu vào (tạo đăng ký joined_late cho khoá). */
export async function inviteEntryDiagnostic(courseId: number, studentId: string): Promise<number> {
  const { data, error } = await getSupabase().rpc("thpt_invite_entry_diagnostic", { p_course: courseId, p_student: studentId });
  if (error) fail(error, "Chưa mời được.");
  return (data as { topicCount: number }).topicCount;
}

/** Thứ Hai của tuần chứa ngày `iso` (yyyy-mm-dd), cùng quy ước date_trunc('week') của Postgres. */
export function weekStartOf(iso: string): string {
  const d = new Date(`${iso}T00:00:00`);
  const shift = (d.getDay() + 6) % 7;
  d.setDate(d.getDate() - shift);
  return localIso(d);
}

export function localIso(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
