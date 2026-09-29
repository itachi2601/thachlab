import { pickRandom, type Difficulty } from "@/features/exams/types";

/**
 * Luyện tập tăng dần độ khó (ROADMAP GĐ 1b): phiên luyện bắt đầu ở mức Dễ, đạt ≥80% mới lên
 * Trung bình rồi Khó — trùng 3 mức của danh hiệu, không thêm khái niệm mới.
 *
 * Mức hiện tại lưu ở localStorage theo (học sinh, mục luyện) — cố tình KHÔNG thêm round-trip
 * Supabase cho trang bài học đã tối ưu. Đổi máy/xoá dữ liệu trình duyệt thì quay về mức Dễ (chấp
 * nhận được: chỉ mất vài phiên leo lại). Học sinh luôn có nút "Luyện tự do" để bỏ ràng buộc.
 */
export type LadderLevel = "de" | "trung-binh" | "kho";

export const LADDER: LadderLevel[] = ["de", "trung-binh", "kho"];
export const LADDER_PASS_RATIO = 0.8;
/** Phiên quá ngắn không đủ căn cứ để lên mức. */
export const LADDER_MIN_QUESTIONS = 5;

const KEY_PREFIX = "thachlab:practice-ladder:";

function key(studentId: string, scope: number | null) {
  return `${KEY_PREFIX}${studentId}:${scope ?? "x"}`;
}

export function readLadderLevel(studentId: string, scope: number | null): LadderLevel {
  try {
    const v = window.localStorage.getItem(key(studentId, scope));
    if (v === "de" || v === "trung-binh" || v === "kho") return v;
  } catch {
    /* localStorage bị chặn → mặc định Dễ */
  }
  return "de";
}

export function writeLadderLevel(studentId: string, scope: number | null, level: LadderLevel) {
  try {
    window.localStorage.setItem(key(studentId, scope), level);
  } catch {
    /* bỏ qua */
  }
}

/** Ngân hàng có đủ câu gắn mức để chạy thang không (cần ít nhất 1 câu Dễ hoặc TB hoặc Khó). */
export function hasLabelledQuestions<T extends { question: { difficulty?: Difficulty } }>(bank: T[]) {
  return bank.some((p) => p.question.difficulty === "de" || p.question.difficulty === "trung-binh" || p.question.difficulty === "kho");
}

/** Bốc `count` câu cho `level`: ưu tiên đúng mức, thiếu thì bù câu chưa gắn nhãn rồi mức kề. */
export function pickForLevel<T extends { question: { difficulty?: Difficulty } }>(
  bank: T[],
  level: LadderLevel,
  count: number,
): T[] {
  const idx = LADDER.indexOf(level);
  const order: Difficulty[] = [
    level,
    "",
    ...LADDER.filter((_, i) => i !== idx).sort((a, b) => Math.abs(LADDER.indexOf(a) - idx) - Math.abs(LADDER.indexOf(b) - idx)),
  ];
  const out: T[] = [];
  for (const d of order) {
    if (out.length >= count) break;
    const tier = bank.filter((p) => (p.question.difficulty ?? "") === d);
    out.push(...pickRandom(tier, count - out.length));
  }
  return pickRandom(out, out.length);
}

/** Kết quả sau phiên: mức mới và lời nhắn hiển thị. */
export function nextLadderLevel(level: LadderLevel, ratio: number, total: number) {
  const idx = LADDER.indexOf(level);
  if (total < LADDER_MIN_QUESTIONS) return { level, moved: false, atTop: false };
  if (ratio < LADDER_PASS_RATIO) return { level, moved: false, atTop: false };
  if (idx === LADDER.length - 1) return { level, moved: false, atTop: true };
  return { level: LADDER[idx + 1], moved: true, atTop: false };
}
