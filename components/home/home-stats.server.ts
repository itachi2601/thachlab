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

export interface HomeStats {
  generatedAt: string;
  totals: { classes: number; chapters: number; lessons: number; items: number };
  classes: HomeClassStats[];
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
