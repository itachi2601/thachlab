import { gradeQuestion, type ExamQuestion, type QuestionResponse } from "@/features/exams/types";

/**
 * Luyện tập chế độ "Từng câu" (kiểu Duolingo): chọn → Kiểm tra → biết ngay đúng/sai + lời giải, câu sai làm lại
 * cuối phiên, "Làm câu tương tự", giãn cách ôn câu sai. Mọi thứ ở client; kết quả cuối phiên vẫn đi qua
 * savePracticeSession (đúng/sai LẦN ĐẦU của mỗi câu) nên mastery/danh hiệu/thang độ khó chạy như cũ.
 *
 * Giống practice-ladder.ts, lựa chọn và lịch ôn lưu localStorage theo học sinh — cố tình KHÔNG thêm round-trip
 * Supabase cho trang bài học đã tối ưu (đổi máy thì mất lịch ôn, chấp nhận được).
 */
export type PracticeMode = "step" | "whole";

const MODE_PREFIX = "thachlab:practice-mode:";
const SPACING_PREFIX = "thachlab:practice-spacing:";

export function readPracticeMode(studentId: string): PracticeMode {
  try {
    return window.localStorage.getItem(MODE_PREFIX + studentId) === "whole" ? "whole" : "step";
  } catch {
    return "step";
  }
}

export function writePracticeMode(studentId: string, mode: PracticeMode) {
  try {
    window.localStorage.setItem(MODE_PREFIX + studentId, mode);
  } catch {
    /* bỏ qua */
  }
}

/** Trung vị thực tế ≈ 50 giây/câu ở chế độ từng câu (có đọc lời giải) — dùng để ước lượng thời gian. */
export const STEP_SECONDS_PER_QUESTION = 50;

// ---------- Khoá nhận diện một câu ----------
/** FNV-1a 32-bit trên phần nội dung câu (đề bài, phương án, các ý) — đủ ổn định để nhận lại cùng câu giữa các phiên. */
export function questionHash(q: ExamQuestion): string {
  const parts: string[] = [q.type, q.question];
  if (q.type === "multiple_choice") parts.push(...q.options);
  if (q.type === "true_false") parts.push(...q.statements.map((s) => s.text));
  const s = parts.join("␟");
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h.toString(36);
}

// ---------- Giãn cách ôn câu sai: 2 ngày → 1 tuần → 1 tháng ----------
const DAY = 86_400_000;
export const SPACING_INTERVALS_MS = [2 * DAY, 7 * DAY, 30 * DAY];
const SPACING_MAX = 200;

interface SpacingEntry {
  h: string;
  /** Mốc ôn kế tiếp (epoch ms). */
  due: number;
  /** 0 = lần ôn sau 2 ngày, 1 = sau 1 tuần, 2 = sau 1 tháng. */
  step: number;
}

function readSpacing(studentId: string): SpacingEntry[] {
  try {
    const raw = window.localStorage.getItem(SPACING_PREFIX + studentId);
    const parsed: unknown = raw ? JSON.parse(raw) : [];
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(
      (e): e is SpacingEntry =>
        !!e && typeof e === "object" && typeof (e as SpacingEntry).h === "string" && typeof (e as SpacingEntry).due === "number" && typeof (e as SpacingEntry).step === "number",
    );
  } catch {
    return [];
  }
}

function writeSpacing(studentId: string, entries: SpacingEntry[]) {
  try {
    const trimmed = [...entries].sort((a, b) => a.due - b.due).slice(0, SPACING_MAX);
    window.localStorage.setItem(SPACING_PREFIX + studentId, JSON.stringify(trimmed));
  } catch {
    /* bỏ qua */
  }
}

/** Tập khoá câu đã tới hạn ôn (due <= now). */
export function dueQuestionHashes(studentId: string, now: number): Set<string> {
  return new Set(readSpacing(studentId).filter((e) => e.due <= now).map((e) => e.h));
}

/**
 * Cập nhật lịch ôn sau phiên theo kết quả LẦN ĐẦU của từng câu:
 *  - sai → (đặt lại) ôn sau 2 ngày;
 *  - đúng câu đang nằm trong lịch và đã tới hạn → sang mốc kế (1 tuần, 1 tháng); xong mốc cuối thì bỏ khỏi lịch;
 *  - đúng câu chưa tới hạn ôn thì giữ nguyên.
 */
export function recordSpacing(studentId: string, results: { hash: string; correct: boolean }[], now: number) {
  const byHash = new Map(readSpacing(studentId).map((e) => [e.h, e]));
  for (const r of results) {
    const cur = byHash.get(r.hash);
    if (!r.correct) {
      byHash.set(r.hash, { h: r.hash, due: now + SPACING_INTERVALS_MS[0], step: 0 });
    } else if (cur && cur.due <= now) {
      const step = cur.step + 1;
      if (step >= SPACING_INTERVALS_MS.length) byHash.delete(r.hash);
      else byHash.set(r.hash, { h: r.hash, due: now + SPACING_INTERVALS_MS[step], step });
    }
  }
  writeSpacing(studentId, [...byHash.values()]);
}

// ---------- Chấm 1 câu ----------
/** Đúng trọn vẹn (earned = max) — cùng luật với buildQuestionResults/is_correct. */
export function isFullyCorrect(q: ExamQuestion, r: QuestionResponse): boolean {
  const g = gradeQuestion(q, r);
  return g.max > 0 && g.earned === g.max;
}

// ---------- Câu tương tự ----------
const LETTERS = ["A", "B", "C", "D"];

/** Câu cùng chủ đề (nhãn `topic`) cùng mức, chưa dùng trong phiên — từ ngân hàng của mục luyện tập. */
export function similarCandidates<T extends { question: ExamQuestion; examId: number; sourceIndex: number }>(
  bank: T[],
  from: ExamQuestion,
  usedKeys: Set<string>,
): T[] {
  const topic = (from.topic ?? "").trim();
  if (!topic) return [];
  const diff = from.difficulty ?? "";
  return bank.filter(
    (p) =>
      !usedKeys.has(pickKey(p)) &&
      (p.question.topic ?? "").trim() === topic &&
      (p.question.difficulty ?? "") === diff &&
      p.question.type !== "essay",
  );
}

export function pickKey(p: { examId: number; sourceIndex: number }): string {
  return `${p.examId}:${p.sourceIndex}`;
}

// ---------- Ghi chú lý do chọn sai ----------
export interface DistractorHint {
  /** Nhãn hiển thị: "B" hoặc "ý b)". */
  label: string;
  note: string;
}

/** Ghi chú cho (các) phương án em chọn sai — rỗng nếu câu chưa có distractorNotes. */
export function distractorHints(q: ExamQuestion, r: QuestionResponse): DistractorHint[] {
  const notes = q.distractorNotes;
  if (!notes) return [];
  if (q.type === "multiple_choice" && typeof r === "number" && r !== q.answer) {
    const key = LETTERS[r];
    const note = key ? notes[key]?.trim() : "";
    return note ? [{ label: key, note }] : [];
  }
  if (q.type === "true_false" && Array.isArray(r)) {
    const out: DistractorHint[] = [];
    q.statements.forEach((s, i) => {
      if (r[i] !== null && r[i] !== s.answer) {
        const note = notes[String(i)]?.trim();
        if (note) out.push({ label: `ý ${["a", "b", "c", "d"][i] ?? i + 1})`, note });
      }
    });
    return out;
  }
  return [];
}
