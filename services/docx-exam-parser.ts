/**
 * Văn bản lấy từ file Word (xem `docx-reader`) → gói bài học `thachlab.lesson-bundle/v1`
 * chỉ gồm phần đề, để đăng thẳng vào mục Kiểm tra / Luyện tập.
 *
 * Nhận đúng cách trình bày kiểu Azota mà thầy cô vẫn gõ:
 *
 *   PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn   (không có cũng được)
 *   Câu 1. Nội dung câu hỏi…
 *   A. …    *B. …    C. …    D. …        ← dấu * là đáp án đúng
 *   Lời giải: …
 *
 *   PHẦN II. Câu trắc nghiệm đúng sai
 *   Câu 5. …
 *   *a) …   b) …   *c) …   d) …           ← ý nào có * là Đúng
 *
 *   PHẦN III. Câu trắc nghiệm trả lời ngắn
 *   Câu 9. … Đáp án: 2,5
 *
 * Câu nào thiếu (chưa đủ 4 phương án, chưa rõ đáp án) vẫn giữ lại để người dùng
 * điền nốt trong trình sửa — không tự đoán đáp án.
 */

import { parseExamLatex } from "@/services/exam-latex-parser";
import { BUNDLE_SCHEMA, type LessonBundle } from "@/services/lesson-import";
import type { RasterImageInput } from "@/services/lesson-media";

const QUESTION_LINE = /^\s*(?:\*\s*)?C[âa]u\s*\d+\s*[.:)]/i;
const PART_LINE = /^\s*PH[ẦA]N\b/i;
/** Cùng mẫu trên nhưng dò trên cả bài (nhiều dòng). */
const PART_ANYWHERE = /^\s*PH[ẦA]N\b/im;
const DEFAULT_PART = "PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn";

export interface DocxExamOptions {
  title?: string;
  subjectCode?: string;
  durationMinutes?: number;
  images?: RasterImageInput[];
}

export interface DocxExamDraft {
  bundle: LessonBundle;
  notes: string[];
  /** Số mốc "Câu n." đếm được trong file — để đối chiếu với số câu dựng được. */
  markerCount: number;
}

/** Đếm số mốc "Câu n." trong văn bản. */
export function countQuestionMarkers(text: string): number {
  return text.split("\n").filter((l) => QUESTION_LINE.test(l)).length;
}

/**
 * Đáp án đánh dấu bằng `*` (kiểu Azota) → thêm dòng "Đáp án: …" ở cuối mỗi câu,
 * đúng thứ mà parser đọc được. Dòng "Đáp án" có sẵn trong đề vẫn được ưu tiên.
 */
function applyStarAnswers(text: string): { text: string; count: number } {
  const out: string[] = [];
  let upper: string[] = [];
  let lower: string[] = [];
  let count = 0;

  const flush = () => {
    if (upper.length) {
      out.push(`Đáp án: ${upper[0]}`);
      count += 1;
    } else if (lower.length) {
      const line = ["a", "b", "c", "d"]
        .map((letter) => `${letter}) ${lower.includes(letter) ? "Đ" : "S"}`)
        .join(" ");
      out.push(`Đáp án: ${line}`);
      count += 1;
    }
    upper = [];
    lower = [];
  };

  for (const line of text.split("\n")) {
    if (QUESTION_LINE.test(line) || PART_LINE.test(line)) flush();
    out.push(
      line.replace(/(^|[\s\t(])\*\s*([A-Da-d])([.)])/g, (_m, before: string, letter: string, punct: string) => {
        if (letter === letter.toUpperCase()) upper.push(letter);
        else lower.push(letter);
        return `${before}${letter}${punct}`;
      }),
    );
  }
  flush();

  return { text: out.join("\n"), count };
}

function guessTitle(text: string): string {
  for (const line of text.split("\n").slice(0, 12)) {
    const t = line.replace(/\s+/g, " ").trim();
    if (!t || PART_LINE.test(t) || QUESTION_LINE.test(t)) continue;
    if (/(ĐỀ|KIỂM TRA|ÔN TẬP|LUYỆN TẬP)/i.test(t)) return t.slice(0, 120);
  }
  return "";
}

function guessDuration(text: string): number | null {
  const m = text.match(/(\d{2,3})\s*ph[úu]t/i);
  if (!m) return null;
  const n = Number(m[1]);
  return n >= 5 && n <= 180 ? n : null;
}

export function docxTextToBundle(text: string, opts: DocxExamOptions = {}): DocxExamDraft {
  const notes: string[] = [];
  const markerCount = countQuestionMarkers(text);

  const starred = applyStarAnswers(text);
  let body = starred.text;
  if (starred.count === 0 && !/Đ[áa]p\s*[áa]n/i.test(text))
    notes.push(
      'Không thấy dấu * đánh dấu đáp án — đề phải có dòng "Đáp án: B" thì mới tự lấy được đáp án, ' +
        "nếu không thì chọn tay ở phần sửa bên dưới.",
    );

  if (!PART_ANYWHERE.test(body)) {
    notes.push('Không thấy "PHẦN I/II/III" — coi toàn bộ là trắc nghiệm 4 phương án.');
    body = `${DEFAULT_PART}\n${body}`;
  }

  const parsed = parseExamLatex(body, { lenient: true });
  notes.push(...parsed.warnings);

  if (markerCount === 0)
    notes.push(
      'Không thấy mốc "Câu 1." nào. Nếu trong Word các câu được đánh số tự động, ' +
        "hãy bỏ đánh số tự động (gõ số bằng tay) rồi tải lên lại.",
    );
  else if (parsed.questions.length !== markerCount)
    notes.push(
      `File có ${markerCount} mốc "Câu n." nhưng dựng được ${parsed.questions.length} câu — rà lại phần sửa bên dưới.`,
    );

  const duration = opts.durationMinutes ?? guessDuration(text) ?? 45;
  const title = opts.title?.trim() || guessTitle(text) || "Đề kiểm tra";

  return {
    bundle: {
      schema: BUNDLE_SCHEMA,
      theory_html: "",
      worked_examples: [],
      exam: {
        title,
        topic: "",
        difficulty: "",
        duration_minutes: duration,
        subject_code: opts.subjectCode || "vat-ly",
        questions: parsed.questions,
      },
      raster_images: opts.images ?? [],
    },
    notes,
    markerCount,
  };
}
