import { getSupabase } from "./supabase";

function supabaseError(error: unknown, fallback: string): Error {
  const raw = error as { message?: unknown; hint?: unknown } | null;
  const message = typeof raw?.message === "string" && raw.message.trim() ? raw.message.trim() : fallback;
  const hint = typeof raw?.hint === "string" && raw.hint.trim() ? ` ${raw.hint.trim()}` : "";
  return new Error(`${message}${hint}`);
}

export type CourseStatus = "draft" | "active" | "completed" | "archived";
export type RegistrationStatus = "pending" | "catchup" | "active" | "rejected" | "left";
export type PaymentStatus = "unpaid" | "paid_center" | "paid_transfer";

export const WEEKDAY_LABEL: Record<number, string> = {
  1: "Thứ 2", 2: "Thứ 3", 3: "Thứ 4", 4: "Thứ 5", 5: "Thứ 6", 6: "Thứ 7", 7: "Chủ nhật",
};

export const REGISTRATION_STATUS_LABEL: Record<RegistrationStatus, string> = {
  pending: "Chờ duyệt",
  catchup: "Đang bù bài",
  active: "Đã vào lớp",
  rejected: "Từ chối",
  left: "Đã nghỉ",
};

export const PAYMENT_STATUS_LABEL: Record<PaymentStatus, string> = {
  unpaid: "Chưa đóng",
  paid_center: "Đã đóng tại trung tâm",
  paid_transfer: "Đã chuyển khoản",
};

export interface CourseSchedule {
  id?: number;
  weekday: number;
  start_time: string; // "18:00"
  end_time: string;
  location: string;
}

export interface ThptCourse {
  id: number;
  class_id: number;
  className: string;
  name: string;
  description: string;
  school_year: string;
  starts_at: string | null;
  ends_at: string | null;
  capacity: number | null;
  fee_note: string;
  is_public: boolean;
  status: CourseStatus;
  schedules: CourseSchedule[];
  /** Số chỗ đã lấy (pending + catchup + active). */
  taken: number;
}

const COURSE_SELECT =
  "id, class_id, name, description, school_year, starts_at, ends_at, capacity, fee_note, is_public, status, classes(name), thpt_course_schedules(id, weekday, start_time, end_time, location)";

type CourseRow = {
  id: number; class_id: number; name: string; description: string; school_year: string;
  starts_at: string | null; ends_at: string | null; capacity: number | null; fee_note: string;
  is_public: boolean; status: CourseStatus;
  classes: { name: string } | { name: string }[] | null;
  thpt_course_schedules: { id: number; weekday: number; start_time: string; end_time: string; location: string }[] | null;
};

function hhmm(t: string) {
  return t.slice(0, 5);
}

function toCourse(row: CourseRow, taken: number): ThptCourse {
  const cls = Array.isArray(row.classes) ? row.classes[0] : row.classes;
  const schedules = (row.thpt_course_schedules ?? [])
    .map((s) => ({ id: s.id, weekday: s.weekday, start_time: hhmm(s.start_time), end_time: hhmm(s.end_time), location: s.location }))
    .sort((a, b) => a.weekday - b.weekday || a.start_time.localeCompare(b.start_time));
  return {
    id: row.id, class_id: row.class_id, className: cls?.name ?? "", name: row.name, description: row.description,
    school_year: row.school_year, starts_at: row.starts_at, ends_at: row.ends_at, capacity: row.capacity,
    fee_note: row.fee_note, is_public: row.is_public, status: row.status, schedules, taken,
  };
}

async function attachSeats(rows: CourseRow[]): Promise<ThptCourse[]> {
  if (rows.length === 0) return [];
  const { data } = await getSupabase().rpc("thpt_course_seats", { p_course_ids: rows.map((r) => r.id) });
  const taken = new Map<number, number>();
  for (const r of (data ?? []) as { course_id: number; taken: number }[]) taken.set(r.course_id, r.taken);
  return rows.map((r) => toCourse(r, taken.get(r.id) ?? 0));
}

/** Khoá đang mở, ai cũng xem được (trang /khoa-hoc) — RLS chỉ trả khoá is_public + active. */
export async function fetchPublicCourses(): Promise<ThptCourse[]> {
  const { data, error } = await getSupabase()
    .from("thpt_courses")
    .select(COURSE_SELECT)
    .eq("is_public", true)
    .eq("status", "active")
    .order("class_id")
    .order("starts_at", { ascending: true, nullsFirst: false });
  if (error) throw supabaseError(error, "Chưa đọc được danh sách khoá học.");
  return attachSeats((data ?? []) as unknown as CourseRow[]);
}

export async function fetchCourse(id: number): Promise<ThptCourse | null> {
  const { data, error } = await getSupabase().from("thpt_courses").select(COURSE_SELECT).eq("id", id).maybeSingle();
  if (error) throw supabaseError(error, "Chưa đọc được khoá học.");
  if (!data) return null;
  const [course] = await attachSeats([data as unknown as CourseRow]);
  return course;
}

/** Mọi khoá của một khối — cho giáo viên phụ trách (RLS manages_class). */
export async function fetchCoursesForClass(classId: number): Promise<ThptCourse[]> {
  const { data, error } = await getSupabase()
    .from("thpt_courses")
    .select(COURSE_SELECT)
    .eq("class_id", classId)
    .order("status")
    .order("created_at", { ascending: false });
  if (error) throw supabaseError(error, "Chưa đọc được khoá học của khối.");
  return attachSeats((data ?? []) as unknown as CourseRow[]);
}

export interface CourseInput {
  class_id: number;
  name: string;
  description: string;
  school_year: string;
  starts_at: string | null;
  ends_at: string | null;
  capacity: number | null;
  fee_note: string;
  is_public: boolean;
  status: CourseStatus;
}

export async function createCourse(input: CourseInput, schedules: CourseSchedule[]): Promise<number> {
  const supabase = getSupabase();
  const { data: auth } = await supabase.auth.getUser();
  const { data, error } = await supabase
    .from("thpt_courses")
    .insert({ ...input, created_by: auth.user?.id ?? null })
    .select("id")
    .single();
  if (error) throw supabaseError(error, "Chưa tạo được khoá học.");
  const id = (data as { id: number }).id;
  await replaceSchedules(id, schedules);
  return id;
}

export async function updateCourse(id: number, patch: Partial<CourseInput>): Promise<void> {
  const { error } = await getSupabase().from("thpt_courses").update(patch).eq("id", id);
  if (error) throw supabaseError(error, "Chưa lưu được khoá học.");
}

/** Ghi đè toàn bộ lịch tuần của khoá. */
export async function replaceSchedules(courseId: number, schedules: CourseSchedule[]): Promise<void> {
  const supabase = getSupabase();
  const { error: delError } = await supabase.from("thpt_course_schedules").delete().eq("course_id", courseId);
  if (delError) throw supabaseError(delError, "Chưa cập nhật được lịch.");
  if (schedules.length === 0) return;
  const { error } = await supabase.from("thpt_course_schedules").insert(
    schedules.map((s) => ({
      course_id: courseId, weekday: s.weekday, start_time: s.start_time, end_time: s.end_time, location: s.location.trim(),
    })),
  );
  if (error) throw supabaseError(error, "Chưa lưu được lịch.");
}

export async function deleteCourse(id: number): Promise<void> {
  const { error } = await getSupabase().from("thpt_courses").delete().eq("id", id);
  if (error) throw supabaseError(error, "Chưa xoá được khoá học.");
}

export interface RegisterResult {
  registration_id: number;
  status: RegistrationStatus;
  joined_late: boolean;
  course_name: string;
}

/**
 * Ghi danh. studentId = chính mình hoặc con đã nối; null = con chưa có tài khoản (kèm childName).
 * RPC tự kiểm quyền, sức chứa, và thêm user_classes 'pending' để đi đúng hàng chờ duyệt.
 */
export async function registerCourse(input: {
  courseId: number;
  studentId: string | null;
  childName?: string;
  contact?: string;
  note?: string;
}): Promise<RegisterResult> {
  const { data, error } = await getSupabase().rpc("thpt_register", {
    p_course_id: input.courseId,
    p_student_id: input.studentId,
    p_child_name: input.childName ?? "",
    p_contact: input.contact ?? "",
    p_note: input.note ?? "",
  });
  if (error) throw supabaseError(error, "Chưa đăng ký được.");
  return data as RegisterResult;
}

export interface Registration {
  id: number;
  course_id: number;
  student_id: string | null;
  registered_by: string | null;
  child_name: string;
  contact: string;
  note: string;
  status: RegistrationStatus;
  joined_late: boolean;
  payment_status: PaymentStatus;
  payment_note: string;
  created_at: string;
  studentName: string;
  studentClass: string;
  registrantName: string;
}

const REG_SELECT =
  "id, course_id, student_id, registered_by, child_name, contact, note, status, joined_late, payment_status, payment_note, created_at, " +
  "student:profiles!thpt_registrations_student_id_fkey(full_name, class_name), " +
  "registrant:profiles!thpt_registrations_registered_by_fkey(full_name)";

type RegRow = Omit<Registration, "studentName" | "studentClass" | "registrantName"> & {
  student: { full_name: string; class_name: string } | { full_name: string; class_name: string }[] | null;
  registrant: { full_name: string } | { full_name: string }[] | null;
};

function toRegistration(row: RegRow): Registration {
  const student = Array.isArray(row.student) ? row.student[0] : row.student;
  const registrant = Array.isArray(row.registrant) ? row.registrant[0] : row.registrant;
  const { student: _s, registrant: _r, ...rest } = row;
  void _s; void _r;
  return {
    ...rest,
    studentName: student?.full_name ?? row.child_name,
    studentClass: student?.class_name ?? "",
    registrantName: registrant?.full_name ?? "",
  };
}

export async function fetchRegistrationsForCourse(courseId: number): Promise<Registration[]> {
  const { data, error } = await getSupabase()
    .from("thpt_registrations")
    .select(REG_SELECT)
    .eq("course_id", courseId)
    .order("created_at", { ascending: true });
  if (error) throw supabaseError(error, "Chưa đọc được danh sách đăng ký.");
  return ((data ?? []) as unknown as RegRow[]).map(toRegistration);
}

/** Đăng ký của chính mình + của các con (RLS "own registrations"), kèm tên khoá. */
export interface MyRegistration extends Registration {
  courseName: string;
  className: string;
}

export async function fetchMyRegistrations(): Promise<MyRegistration[]> {
  const { data, error } = await getSupabase()
    .from("thpt_registrations")
    .select(REG_SELECT + ", thpt_courses(name, classes(name))")
    .order("created_at", { ascending: false });
  if (error) throw supabaseError(error, "Chưa đọc được đăng ký.");
  return ((data ?? []) as unknown as (RegRow & {
    thpt_courses: { name: string; classes: { name: string } | { name: string }[] | null } | null;
  })[]).map((row) => {
    const course = Array.isArray(row.thpt_courses) ? row.thpt_courses[0] : row.thpt_courses;
    const cls = course ? (Array.isArray(course.classes) ? course.classes[0] : course.classes) : null;
    return { ...toRegistration(row), courseName: course?.name ?? "", className: cls?.name ?? "" };
  });
}

export async function reviewRegistration(id: number, status: "active" | "rejected" | "left" | "pending"): Promise<void> {
  const { error } = await getSupabase().rpc("thpt_review_registration", { p_id: id, p_status: status });
  if (error) throw supabaseError(error, "Chưa cập nhật được.");
}

export async function setPayment(id: number, payment_status: PaymentStatus, payment_note = ""): Promise<void> {
  const { error } = await getSupabase()
    .from("thpt_registrations")
    .update({ payment_status, payment_note })
    .eq("id", id);
  if (error) throw supabaseError(error, "Chưa lưu được trạng thái phí.");
}

export async function attachStudent(id: number, studentId: string): Promise<void> {
  const { error } = await getSupabase().rpc("thpt_attach_student", { p_id: id, p_student_id: studentId });
  if (error) throw supabaseError(error, "Chưa gắn được tài khoản.");
}

export function formatSchedule(s: CourseSchedule): string {
  return `${WEEKDAY_LABEL[s.weekday] ?? ""} ${s.start_time}–${s.end_time}${s.location ? ` · ${s.location}` : ""}`;
}

export function formatDate(d: string | null): string {
  if (!d) return "";
  const [y, m, day] = d.split("-");
  return `${day}/${m}/${y}`;
}
