// Phần "công khai, ẩn danh" của services/thpt-courses.ts — KHÔNG import
// "@/services/supabase" (tức không kéo theo @supabase/supabase-js/GoTrue, ~211KB).
//
// Trang /khoa-hoc (app/(public)/khoa-hoc/page.tsx, không đăng nhập cũng xem được) import
// từ FILE NÀY thay vì services/thpt-courses.ts — nếu import từ thpt-courses.ts thì dù
// chỉ dùng fetchPublicCourses/formatDate/WEEKDAY_LABEL, cả file đó (dùng chung với các
// hàm quản trị createCourse/updateCourse/...) vẫn có "import { getSupabase } from
// './supabase'" ở đầu, nên bundler vẫn đóng gói cả SDK vào trang công khai.
//
// services/thpt-courses.ts (bản đầy đủ, cho trang cần đăng nhập/quản trị) import lại
// types + hàm thuần từ đây để khỏi định nghĩa 2 lần — chỉ tự giữ riêng các hàm THẬT SỰ
// cần supabase-js (ghi dữ liệu, hoặc đọc có RLS theo người dùng cụ thể).
import { restSelect, restRpc } from "@/lib/supabase-rest";

export type CourseStatus = "draft" | "active" | "completed" | "archived";

export const WEEKDAY_LABEL: Record<number, string> = {
  1: "Thứ 2", 2: "Thứ 3", 3: "Thứ 4", 4: "Thứ 5", 5: "Thứ 6", 6: "Thứ 7", 7: "Chủ nhật",
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
  /** Chủ đề tầng bài (question_topics) lớp đang dạy tới — để tính phần cần bù cho em vào trễ. */
  current_topic_id: number | null;
  schedules: CourseSchedule[];
  /** Số chỗ đã lấy (pending + catchup + active). */
  taken: number;
}

export const COURSE_SELECT =
  "id, class_id, name, description, school_year, starts_at, ends_at, capacity, fee_note, is_public, status, current_topic_id, classes(name), thpt_course_schedules(id, weekday, start_time, end_time, location)";

export type CourseRow = {
  id: number; class_id: number; name: string; description: string; school_year: string;
  starts_at: string | null; ends_at: string | null; capacity: number | null; fee_note: string;
  is_public: boolean; status: CourseStatus; current_topic_id: number | null;
  classes: { name: string } | { name: string }[] | null;
  thpt_course_schedules: { id: number; weekday: number; start_time: string; end_time: string; location: string }[] | null;
};

export function hhmm(t: string) {
  return t.slice(0, 5);
}

export function toCourse(row: CourseRow, taken: number): ThptCourse {
  const cls = Array.isArray(row.classes) ? row.classes[0] : row.classes;
  const schedules = (row.thpt_course_schedules ?? [])
    .map((s) => ({ id: s.id, weekday: s.weekday, start_time: hhmm(s.start_time), end_time: hhmm(s.end_time), location: s.location }))
    .sort((a, b) => a.weekday - b.weekday || a.start_time.localeCompare(b.start_time));
  return {
    id: row.id, class_id: row.class_id, className: cls?.name ?? "", name: row.name, description: row.description,
    school_year: row.school_year, starts_at: row.starts_at, ends_at: row.ends_at, capacity: row.capacity,
    fee_note: row.fee_note, is_public: row.is_public, status: row.status, current_topic_id: row.current_topic_id ?? null,
    schedules, taken,
  };
}

async function attachSeatsRest(rows: CourseRow[]): Promise<ThptCourse[]> {
  if (rows.length === 0) return [];
  const data = (await restRpc("thpt_course_seats", { p_course_ids: rows.map((r) => r.id) })) as
    | { course_id: number; taken: number }[]
    | null;
  const taken = new Map<number, number>();
  for (const r of data ?? []) taken.set(r.course_id, r.taken);
  return rows.map((r) => toCourse(r, taken.get(r.id) ?? 0));
}

/**
 * Khoá đang mở, ai cũng xem được (trang /khoa-hoc) — RLS chỉ trả khoá is_public + active.
 * Dùng fetch REST thuần (lib/supabase-rest.ts), không qua supabase-js.
 */
export async function fetchPublicCourses(): Promise<ThptCourse[]> {
  const qs = new URLSearchParams({
    select: COURSE_SELECT,
    is_public: "eq.true",
    status: "eq.active",
    order: "class_id.asc,starts_at.asc.nullslast",
  });
  const data = (await restSelect("thpt_courses", qs)) as CourseRow[] | null;
  return attachSeatsRest(data ?? []);
}

export function formatDate(d: string | null): string {
  if (!d) return "";
  const [y, m, day] = d.split("-");
  return `${day}/${m}/${y}`;
}

export function formatSchedule(s: CourseSchedule): string {
  return `${WEEKDAY_LABEL[s.weekday] ?? ""} ${s.start_time}–${s.end_time}${s.location ? ` · ${s.location}` : ""}`;
}
