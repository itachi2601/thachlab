/**
 * "Chỗ dừng" của một bài trên máy này: mục lý thuyết đang đọc (tên mốc, thứ tự, tổng số mốc, số phút còn lại).
 * Trang bài ghi khi mục lục đổi mục đang đọc; trang chương đọc để khối "Học tiếp" ghi "Dừng ở mục IV. Trả bài ·
 * còn ~8 phút" và dòng bài ghi "Đang học · mục 4/6" (bản duyệt 26/10/2026). Chỉ localStorage — không round-trip.
 */
const RESUME_SPOT_STORE = "thachlab-resume-spot-";

export type ResumeSpot = { heading: string; index: number; total: number; minutesLeft: number };

// Khoá gắn userId: máy dùng chung không lộ chỗ học của em trước.
const key = (userId: string, lessonId: number) => `${RESUME_SPOT_STORE}${userId}-${lessonId}`;

export function writeResumeSpot(userId: string, lessonId: number, spot: ResumeSpot) {
  try {
    window.localStorage.setItem(key(userId, lessonId), JSON.stringify(spot));
  } catch {}
}

/** Học xong mục lý thuyết → bỏ chỗ dừng, khối "Học tiếp" về lại "Đã học x/y mục". */
export function clearResumeSpot(userId: string, lessonId: number) {
  try {
    window.localStorage.removeItem(key(userId, lessonId));
  } catch {}
}

export function readResumeSpot(userId: string | undefined, lessonId: number): ResumeSpot | null {
  if (typeof window === "undefined" || !userId) return null;
  try {
    const raw = window.localStorage.getItem(key(userId, lessonId));
    if (!raw) return null;
    const spot = JSON.parse(raw) as Partial<ResumeSpot>;
    if (typeof spot.heading !== "string" || typeof spot.index !== "number" || typeof spot.total !== "number") return null;
    return { heading: spot.heading, index: spot.index, total: spot.total, minutesLeft: Number(spot.minutesLeft) || 0 };
  } catch {
    return null;
  }
}
