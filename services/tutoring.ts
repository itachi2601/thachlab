import { getSupabase } from "@/services/supabase";

// ============================================================
// Phụ đạo theo chủ đề — "em nào hổng phần nào, đã được dạy phần nào"
// Bảng: tutoring_needs (mục cần phụ đạo) + tutoring_session_topics (buổi đã dạy gì).
// Xem docs/supabase-migration-tutoring-needs.sql.
// ============================================================

export type NeedStatus = "open" | "assigned" | "tutored" | "cleared" | "dismissed";

export const NEED_STATUS_LABEL: Record<NeedStatus, string> = {
  open: "Cần phụ đạo",
  assigned: "Đã có người nhận",
  tutored: "Đã phụ đạo",
  cleared: "Đã khắc phục",
  dismissed: "Bỏ qua",
};

/** Trạng thái còn phải làm gì đó — dùng để lọc danh sách mặc định. */
export const ACTIVE_NEED_STATUSES: NeedStatus[] = ["open", "assigned", "tutored"];

export interface TutoringNeed {
  id: number;
  studentId: string;
  classId: number | null;
  topicId: number;
  topicName: string;
  lessonId: number | null;
  chapterId: number | null;
  form: string; // "ly_thuyet" | "bai_tap" | ""
  wrong: number;
  total: number;
  pct: number;
  status: NeedStatus;
  source: "auto" | "manual";
  assignedTo: string | null;
  note: string;
  firstSeenAt: string;
  lastSeenAt: string;
  tutoredAt: string | null;
  clearedAt: string | null;
}

interface NeedRow {
  id: number;
  student_id: string;
  class_id: number | null;
  topic_id: number;
  form: string;
  wrong: number;
  total: number;
  pct: number;
  status: NeedStatus;
  source: "auto" | "manual";
  assigned_to: string | null;
  note: string;
  first_seen_at: string;
  last_seen_at: string;
  tutored_at: string | null;
  cleared_at: string | null;
  question_topics: { name: string; lesson_id: number | null; chapter_id: number | null } | { name: string; lesson_id: number | null; chapter_id: number | null }[] | null;
}

const NEED_SELECT =
  "id, student_id, class_id, topic_id, form, wrong, total, pct, status, source, assigned_to, note, first_seen_at, last_seen_at, tutored_at, cleared_at, question_topics(name, lesson_id, chapter_id)";

export const FORM_LABEL: Record<string, string> = {
  ly_thuyet: "lý thuyết",
  bai_tap: "bài tập",
  "": "",
};

function toNeed(row: NeedRow): TutoringNeed {
  const topic = Array.isArray(row.question_topics) ? row.question_topics[0] ?? null : row.question_topics;
  return {
    id: row.id,
    studentId: row.student_id,
    classId: row.class_id,
    topicId: row.topic_id,
    topicName: topic?.name ?? "Chủ đề đã xoá",
    lessonId: topic?.lesson_id ?? null,
    chapterId: topic?.chapter_id ?? null,
    form: row.form,
    wrong: row.wrong,
    total: row.total,
    pct: row.pct,
    status: row.status,
    source: row.source,
    assignedTo: row.assigned_to,
    note: row.note,
    firstSeenAt: row.first_seen_at,
    lastSeenAt: row.last_seen_at,
    tutoredAt: row.tutored_at,
    clearedAt: row.cleared_at,
  };
}

/** Nhãn gọn để hiện trên thẻ: "Sóng dừng · bài tập". */
export function needLabel(need: TutoringNeed): string {
  const form = FORM_LABEL[need.form] ?? "";
  return form ? `${need.topicName} · ${form}` : need.topicName;
}

/** Mục cần phụ đạo của cả lớp (trang giáo viên / trợ giảng). */
export async function fetchNeedsForStudents(
  studentIds: string[],
  statuses: NeedStatus[] = ACTIVE_NEED_STATUSES,
): Promise<TutoringNeed[]> {
  if (studentIds.length === 0) return [];
  let query = getSupabase()
    .from("tutoring_needs")
    .select(NEED_SELECT)
    .in("student_id", studentIds);
  if (statuses.length > 0) query = query.in("status", statuses);
  const { data, error } = await query.order("pct", { ascending: false });
  if (error) throw error;
  return ((data ?? []) as unknown as NeedRow[]).map(toNeed);
}

/** Mục cần phụ đạo của chính học sinh đang đăng nhập. */
export async function fetchMyNeeds(userId: string): Promise<TutoringNeed[]> {
  const { data, error } = await getSupabase()
    .from("tutoring_needs")
    .select(NEED_SELECT)
    .eq("student_id", userId)
    .order("status")
    .order("pct", { ascending: false });
  if (error) throw error;
  return ((data ?? []) as unknown as NeedRow[]).map(toNeed);
}

export async function updateNeed(
  id: number,
  patch: { status?: NeedStatus; assignedTo?: string | null; note?: string },
): Promise<void> {
  const body: Record<string, unknown> = {};
  if (patch.status !== undefined) body.status = patch.status;
  if (patch.assignedTo !== undefined) body.assigned_to = patch.assignedTo;
  if (patch.note !== undefined) body.note = patch.note;
  const { error } = await getSupabase().from("tutoring_needs").update(body).eq("id", id);
  if (error) throw error;
}

/** Thầy/trợ giảng tự thêm một mục cần phụ đạo (không đợi bài kiểm tra). */
export async function addManualNeed(input: {
  studentId: string;
  classId: number | null;
  topicId: number;
  form?: string;
  note?: string;
}): Promise<void> {
  const { error } = await getSupabase().from("tutoring_needs").insert({
    student_id: input.studentId,
    class_id: input.classId,
    topic_id: input.topicId,
    form: input.form ?? "",
    source: "manual",
    status: "open",
    note: input.note ?? "",
  });
  if (error) throw error;
}

/** Dựng lại toàn bộ mục cần phụ đạo của lớp — dùng sau khi mới gắn nhãn chủ đề cho đề cũ. */
export async function refreshClassNeeds(classId: number): Promise<number> {
  const { data, error } = await getSupabase().rpc("refresh_class_tutoring_needs", { p_class: classId });
  if (error) throw error;
  return (data as number) ?? 0;
}

// ============================================================
// Buổi phụ đạo đã dạy chủ đề nào
// ============================================================
export interface TutoringCoverage {
  id: number;
  sessionId: string;
  studentId: string;
  topicId: number;
  topicName: string;
  note: string;
  createdAt: string;
  workDate: string | null;
  assistantName: string | null;
}

interface CoverageRow {
  id: number;
  session_id: string;
  student_id: string;
  topic_id: number;
  note: string;
  created_at: string;
  question_topics: { name: string } | { name: string }[] | null;
  ta_sessions: {
    work_date: string;
    ta_assistants: { short_name: string } | { short_name: string }[] | null;
  } | {
    work_date: string;
    ta_assistants: { short_name: string } | { short_name: string }[] | null;
  }[] | null;
}

function one<T>(value: T | T[] | null): T | null {
  return Array.isArray(value) ? value[0] ?? null : value;
}

const COVERAGE_SELECT =
  "id, session_id, student_id, topic_id, note, created_at, question_topics(name), ta_sessions(work_date, ta_assistants(short_name))";

function toCoverage(row: CoverageRow): TutoringCoverage {
  const session = one(row.ta_sessions);
  const assistant = session ? one(session.ta_assistants) : null;
  return {
    id: row.id,
    sessionId: row.session_id,
    studentId: row.student_id,
    topicId: row.topic_id,
    topicName: one(row.question_topics)?.name ?? "",
    note: row.note,
    createdAt: row.created_at,
    workDate: session?.work_date ?? null,
    assistantName: assistant?.short_name ?? null,
  };
}

/** Lịch sử "đã được phụ đạo phần nào" của một nhóm học sinh. */
export async function fetchCoverageForStudents(studentIds: string[]): Promise<TutoringCoverage[]> {
  if (studentIds.length === 0) return [];
  const { data, error } = await getSupabase()
    .from("tutoring_session_topics")
    .select(COVERAGE_SELECT)
    .in("student_id", studentIds)
    .order("created_at", { ascending: false });
  if (error) throw error;
  return ((data ?? []) as unknown as CoverageRow[]).map(toCoverage);
}

export interface CoverageInput {
  studentId: string;
  topicId: number;
  needId?: number | null;
  note?: string;
}

/** Ghi nhận buổi phụ đạo vừa ghi đã dạy chủ đề nào cho em nào. */
export async function saveSessionCoverage(sessionId: string, items: CoverageInput[]): Promise<void> {
  if (items.length === 0) return;
  const { error } = await getSupabase().from("tutoring_session_topics").insert(
    items.map((item) => ({
      session_id: sessionId,
      student_id: item.studentId,
      topic_id: item.topicId,
      need_id: item.needId ?? null,
      note: item.note ?? "",
    })),
  );
  if (error) throw error;
}
