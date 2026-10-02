// Đọc public/data/teaching-schedule.json (sinh bởi scripts/build-content.mjs lúc prebuild) NGAY LÚC BUILD
// cho trang chủ — chỉ dùng trong server component, không import từ client. Thiếu file → null, khối lịch ẩn.
import { readFileSync } from "node:fs";
import { join } from "node:path";

export interface ScheduleSlot {
  weekday: number; // 1 = Thứ 2 … 7 = Chủ nhật
  start: string; // "18:00"
  end: string;
  location: string;
}

export interface ScheduleCourse {
  id: number;
  name: string;
  className: string;
  slots: ScheduleSlot[];
}

export function readTeachingSchedule(): ScheduleCourse[] | null {
  try {
    const raw = readFileSync(join(process.cwd(), "public", "data", "teaching-schedule.json"), "utf8");
    const parsed = JSON.parse(raw) as { courses?: ScheduleCourse[] };
    if (!Array.isArray(parsed.courses) || parsed.courses.length === 0) return null;
    return parsed.courses;
  } catch {
    return null;
  }
}
