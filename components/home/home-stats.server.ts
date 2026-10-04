// Đọc public/data/home-stats.json (sinh bởi scripts/build-content.mjs lúc prebuild) NGAY LÚC BUILD
// cho trang chủ — chỉ dùng trong server component (app/(public)/page.tsx), không import từ client.
// Thiếu file (chưa chạy prebuild, Supabase lỗi lúc build) → trả null, trang chủ ẩn phần số liệu
// chứ không fail build và không gọi Supabase khi tải trang (quy tắc "không thêm round-trip cho /").
import { readFileSync } from "node:fs";
import { join } from "node:path";

export interface HomeClassStats {
  id: number;
  slug: string;
  name: string;
  color: string;
  icon: string;
  chapters: number;
  lessons: number;
  items: number;
}

/** Một buổi trong lịch tuần của lớp học thêm. weekday: 1 = Thứ 2 … 7 = Chủ nhật. */
export interface HomeCourseSession {
  weekday: number;
  /** "18:00" */
  start: string;
  end: string;
  location: string;
}

/** Lớp học thêm đang mở đăng ký (thpt_courses is_public + active), đọc lúc build. */
export interface HomeCourse {
  id: number;
  name: string;
  /** Tên khối: "10" / "11" / "12". */
  className: string;
  schoolYear: string;
  startsAt: string | null;
  schedules: HomeCourseSession[];
}

export interface HomeStats {
  generatedAt: string;
  totals: {
    classes: number;
    chapters: number;
    lessons: number;
    items: number;
    /** Học sinh có tài khoản (profiles.role = 'student'). null = build không có service role key. */
    students?: number | null;
    /** Lượt làm đề đã chấm (exam_results). null = không đếm được lúc build. */
    attempts?: number | null;
    /** Câu trong ngân hàng câu hỏi (question_bank chưa archive). null = không đếm được lúc build. */
    questions?: number | null;
  };
  classes: HomeClassStats[];
  /** Thiếu (build cũ) hoặc null (không đọc được) → trang chủ hiện câu "chưa có lịch". */
  courses?: HomeCourse[] | null;
}

export function readHomeStats(): HomeStats | null {
  try {
    const raw = readFileSync(join(process.cwd(), "public", "data", "home-stats.json"), "utf8");
    const parsed = JSON.parse(raw) as Partial<HomeStats>;
    if (!parsed || typeof parsed !== "object" || !parsed.totals || !Array.isArray(parsed.classes)) return null;
    return parsed as HomeStats;
  } catch {
    return null;
  }
}
