import { getSupabase } from "@/services/supabase";

export interface HomeroomMeeting {
  id: number;
  course_id: number;
  week_label: string;
  meeting_date: string;
  content: string;
  created_at: string;
}

export interface HomeroomTask {
  id: number;
  meeting_id: number;
  course_id: number;
  student_id: string | null;
  title: string;
  note: string;
  created_at: string;
}

export async function fetchHomeroomMeetings(courseId: number) {
  const { data, error } = await getSupabase()
    .from("homeroom_meetings")
    .select("id, course_id, week_label, meeting_date, content, created_at")
    .eq("course_id", courseId)
    .order("meeting_date", { ascending: false });
  if (error) throw error;
  return (data ?? []) as HomeroomMeeting[];
}

export async function createHomeroomMeeting(input: {
  courseId: number;
  weekLabel: string;
  meetingDate: string;
  content: string;
}) {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { data, error } = await supabase
    .from("homeroom_meetings")
    .insert({
      course_id: input.courseId,
      week_label: input.weekLabel,
      meeting_date: input.meetingDate,
      content: input.content,
      created_by: auth.user?.id ?? null,
    })
    .select("id, course_id, week_label, meeting_date, content, created_at")
    .single();
  if (error) throw error;
  return data as HomeroomMeeting;
}

export async function updateHomeroomMeeting(
  meetingId: number,
  patch: { weekLabel?: string; meetingDate?: string; content?: string },
) {
  const payload: Record<string, unknown> = { updated_at: new Date().toISOString() };
  if (patch.weekLabel !== undefined) payload.week_label = patch.weekLabel;
  if (patch.meetingDate !== undefined) payload.meeting_date = patch.meetingDate;
  if (patch.content !== undefined) payload.content = patch.content;
  const { error } = await getSupabase().from("homeroom_meetings").update(payload).eq("id", meetingId);
  if (error) throw error;
}

export async function deleteHomeroomMeeting(meetingId: number) {
  const { error } = await getSupabase().from("homeroom_meetings").delete().eq("id", meetingId);
  if (error) throw error;
}

export async function fetchHomeroomTasks(courseId: number) {
  const { data, error } = await getSupabase()
    .from("homeroom_tasks")
    .select("id, meeting_id, course_id, student_id, title, note, created_at")
    .eq("course_id", courseId)
    .order("created_at");
  if (error) throw error;
  return (data ?? []) as HomeroomTask[];
}

/** Việc trong 1 buổi SHCN dành cho sinh viên đang đăng nhập: student_id null (cả lớp) hoặc = chính mình. */
export async function fetchMyHomeroomTasks(courseId: number, studentId: string) {
  const { data, error } = await getSupabase()
    .from("homeroom_tasks")
    .select("id, meeting_id, course_id, student_id, title, note, created_at")
    .eq("course_id", courseId)
    .or(`student_id.is.null,student_id.eq.${studentId}`)
    .order("created_at");
  if (error) throw error;
  return (data ?? []) as HomeroomTask[];
}

export async function createHomeroomTask(input: {
  meetingId: number;
  courseId: number;
  studentId: string | null;
  title: string;
  note?: string;
}) {
  const { data, error } = await getSupabase()
    .from("homeroom_tasks")
    .insert({
      meeting_id: input.meetingId,
      course_id: input.courseId,
      student_id: input.studentId,
      title: input.title,
      note: input.note ?? "",
    })
    .select("id, meeting_id, course_id, student_id, title, note, created_at")
    .single();
  if (error) throw error;
  return data as HomeroomTask;
}

export async function deleteHomeroomTask(taskId: number) {
  const { error } = await getSupabase().from("homeroom_tasks").delete().eq("id", taskId);
  if (error) throw error;
}

export interface HomeroomTaskCompletion {
  task_id: number;
  student_id: string;
  done_at: string;
}

/** Toàn bộ dấu tick trong lớp — dùng cho GVCN xem việc chung ai đã làm/chưa làm. */
export async function fetchHomeroomTaskCompletions(courseId: number) {
  const { data, error } = await getSupabase()
    .from("homeroom_task_completions")
    .select("task_id, student_id, done_at, homeroom_tasks!inner(course_id)")
    .eq("homeroom_tasks.course_id", courseId);
  if (error) throw error;
  return (data ?? []).map((row) => ({
    task_id: row.task_id as number,
    student_id: row.student_id as string,
    done_at: row.done_at as string,
  })) as HomeroomTaskCompletion[];
}

/** Dấu tick của chính sinh viên đang đăng nhập. */
export async function fetchMyHomeroomTaskCompletions(studentId: string) {
  const { data, error } = await getSupabase()
    .from("homeroom_task_completions")
    .select("task_id, student_id, done_at")
    .eq("student_id", studentId);
  if (error) throw error;
  return (data ?? []) as HomeroomTaskCompletion[];
}

export async function setHomeroomTaskDone(taskId: number, studentId: string, done: boolean) {
  const supabase = getSupabase();
  if (done) {
    const { error } = await supabase
      .from("homeroom_task_completions")
      .upsert({ task_id: taskId, student_id: studentId, done_at: new Date().toISOString() }, { onConflict: "task_id,student_id" });
    if (error) throw error;
  } else {
    const { error } = await supabase
      .from("homeroom_task_completions")
      .delete()
      .eq("task_id", taskId)
      .eq("student_id", studentId);
    if (error) throw error;
  }
}
