import { getSupabase } from "@/services/supabase";
import { COURSE_SELECT, toCourse, type CourseRow, type ThptCourse } from "@/services/thpt-courses-public";

/* Dữ liệu chỉ-đọc cho trang phụ huynh (/phu-huynh). Mọi hàm nuốt lỗi và trả null/[]:
   một khối phụ (điểm danh, lịch học…) lỗi thì ẩn khối đó, không làm hỏng cả trang. */

export interface ClassStanding {
  rank: number;
  total: number;
  myAvg: number;
  classAvg: number;
}

/** Vị trí của con trong lớp theo điểm trung bình các bài kiểm tra của lớp (RPC có sẵn, cho phép phụ huynh). */
export async function fetchClassStanding(studentId: string, classId: number): Promise<ClassStanding | null> {
  const { data, error } = await getSupabase().rpc("get_periodic_rank_of", { p_student: studentId, p_class_id: classId });
  if (error) return null;
  const row = ((data ?? []) as { rnk: number; total: number; my_avg: number; class_avg: number }[])[0];
  if (!row) return null;
  return { rank: row.rnk, total: row.total, myAvg: Number(row.my_avg), classAvg: Number(row.class_avg) };
}

export type AttendanceStatus = "present" | "late" | "excused" | "absent";

export interface AttendanceRow {
  sessionId: number;
  date: string;
  title: string;
  /** null = thầy chưa điểm danh buổi này cho em — KHÔNG được tính là vắng. */
  status: AttendanceStatus | null;
}

/** null = RPC chưa có trên DB (migration chưa chạy) hoặc lỗi → giao diện ẩn khối điểm danh. */
export async function fetchAttendanceForParent(studentId: string): Promise<AttendanceRow[] | null> {
  const { data, error } = await getSupabase().rpc("parent_attendance_summary", { p_student: studentId, p_limit: 40 });
  if (error) return null;
  return ((data ?? []) as { session_id: number; session_date: string; title: string; status: AttendanceStatus | null }[]).map(
    (r) => ({ sessionId: r.session_id, date: r.session_date, title: r.title, status: r.status }),
  );
}

/** Khoá học (kèm lịch tuần + ghi chú học phí) theo id — để dựng "buổi học sắp tới" và thẻ học phí. */
export async function fetchCoursesByIds(courseIds: number[]): Promise<ThptCourse[]> {
  const ids = [...new Set(courseIds)];
  if (ids.length === 0) return [];
  const { data, error } = await getSupabase().from("thpt_courses").select(COURSE_SELECT).in("id", ids);
  if (error) return [];
  return ((data ?? []) as unknown as CourseRow[]).map((row) => toCourse(row, 0));
}
