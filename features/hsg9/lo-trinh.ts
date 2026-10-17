// Lộ trình 18 buổi thứ Bảy của khoá "Vật lí HSG & chuyên" (KHTN 9), 10/10/2026 → 20/02/2027.
// Nguồn duy nhất cho việc tự học từng tuần: scripts/data/btvn-hsg9/tuan.json (cùng file script gửi BTVN đọc).
// Bản kế hoạch đầy đủ cho thầy: ~/Documents/.../03_Ke_hoach_boi_duong/31_lo-trinh-17-buoi-thu-7.md.
import tuanJson from "@/scripts/data/btvn-hsg9/tuan.json";

export interface Hsg9Session {
  buoi: number;
  /** yyyy-mm-dd, luôn là thứ Bảy */
  date: string;
  chuDe: string;
  lessons: number[];
  /** [nhãn ngày, việc] — nhãn là "Thứ Hai".."Thứ Sáu" hoặc mốc tự do (phiếu Tết) */
  tuHoc: [string, string][];
  btvn: string;
  /** Bài kiểm tra/thi thử của buổi, nếu có */
  kiemTra?: string;
}

export const HSG9_EXAM_DATE = "2027-02-24";
export const HSG9_EXAM_LABEL = "Thứ Tư 24/02/2027";

const KIEM_TRA: Record<number, string> = {
  1: "Pre-test Cơ học",
  6: "Kiểm tra 1 · Cơ",
  10: "Thi thử 1 · 90 phút",
  12: "Kiểm tra 2 · Điện",
  15: "Kiểm tra 3 · Quang",
  17: "Thi thử 2 · 120 phút",
  18: "Thi thử 3 · 120 phút",
};

function isoFromDdMm(ddmm: string): string {
  const [d, m] = ddmm.split("/").map(Number);
  const year = m >= 8 ? 2026 : 2027; // khoá chạy tháng 10/2026 → 02/2027
  return `${year}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
}

type TuanRow = { buoi: number; ngay: string; chu_de: string; lessons: number[]; tu_hoc: string[][]; btvn: string };

export const HSG9_SESSIONS: Hsg9Session[] = [
  { buoi: 1, date: "2026-10-10", chuDe: "Pre-test Cơ học THCS", lessons: [], tuHoc: [], btvn: "" },
  {
    buoi: 2,
    date: "2026-10-17",
    chuDe: "Chữa bộ 12 bài Cơ học VD–VDC; kỹ năng nền CĐ00",
    lessons: [160],
    tuHoc: [],
    btvn: "",
  },
  ...(tuanJson.tuan as TuanRow[]).map((t) => ({
    buoi: t.buoi,
    date: isoFromDdMm(t.ngay),
    chuDe: t.chu_de,
    lessons: t.lessons,
    tuHoc: t.tu_hoc.map(([a, b]) => [a, b] as [string, string]),
    btvn: t.btvn,
  })),
].map((s) => ({
  ...s,
  // Tên buổi đã nói "Kiểm tra…/Thi thử…" thì không gắn nhãn lặp lại (N4).
  kiemTra: /Kiểm tra|Thi thử|Pre-test/.test(s.chuDe) ? undefined : KIEM_TRA[s.buoi],
}));

/** Hôm nay theo giờ Việt Nam, dạng yyyy-mm-dd. */
export function todayVn(now = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Ho_Chi_Minh" }).format(now);
}

/** Giờ hiện tại ở Việt Nam (0–23). */
export function hourVn(now = new Date()): number {
  return Number(
    new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Ho_Chi_Minh", hour: "2-digit", hourCycle: "h23" }).format(now),
  );
}

export function daysBetween(fromIso: string, toIso: string): number {
  return Math.round((Date.parse(`${toIso}T00:00:00Z`) - Date.parse(`${fromIso}T00:00:00Z`)) / 86_400_000);
}

export function addDays(iso: string, days: number): string {
  return new Date(Date.parse(`${iso}T00:00:00Z`) + days * 86_400_000).toISOString().slice(0, 10);
}

/** "07/11" */
export function ddmm(iso: string): string {
  return `${iso.slice(8, 10)}/${iso.slice(5, 7)}`;
}

/** Buổi sắp tới (hoặc hôm nay). null khi khoá đã hết. */
export function upcomingSession(today = todayVn()): Hsg9Session | null {
  return HSG9_SESSIONS.find((s) => s.date >= today) ?? null;
}

const WEEKDAY_LABEL = ["Chủ nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];

export function weekdayLabel(iso: string): string {
  return WEEKDAY_LABEL[new Date(`${iso}T00:00:00Z`).getUTCDay()];
}

/** Chỉ số việc tự học của hôm nay trong tuần của buổi (nhãn "Thứ Hai".."Thứ Sáu"); -1 khi hôm nay không có việc riêng. */
export function todayTaskIndex(session: Hsg9Session, today = todayVn()): number {
  const label = weekdayLabel(today);
  return session.tuHoc.findIndex(([day]) => day === label);
}

/** Ôn cách quãng: chủ đề học cách đây ~4 tuần (21–35 ngày) thì gợi ý làm lại bài đã sai. */
export function reviewDue(today = todayVn()): Hsg9Session[] {
  return HSG9_SESSIONS.filter((s) => {
    const d = daysBetween(s.date, today);
    return s.lessons.length > 0 && d >= 21 && d <= 35;
  });
}

// Dấu "đã làm" của việc tự học: chỉ là ghi chép riêng của em, lưu trên máy (không phải tiến độ thầy xem —
// tiến độ thầy xem lấy từ lesson_progress khi em học trên web).
const TICK_KEY = (userId: string) => `hsg9-lo-trinh:${userId}`;

export function loadTicks(userId: string): Record<string, boolean> {
  try {
    return JSON.parse(window.localStorage.getItem(TICK_KEY(userId)) ?? "{}") as Record<string, boolean>;
  } catch {
    return {};
  }
}

export function saveTicks(userId: string, ticks: Record<string, boolean>) {
  try {
    window.localStorage.setItem(TICK_KEY(userId), JSON.stringify(ticks));
  } catch {
    // bộ nhớ trình duyệt bị chặn: dấu tick chỉ mất khi tải lại trang, không ảnh hưởng việc học
  }
}

export const tickId = (buoi: number, index: number) => `${buoi}-${index}`;
