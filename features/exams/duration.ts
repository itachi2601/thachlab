import type { ExamQuestion } from "@/features/exams/types";

/**
 * features/exams/duration.ts — ước lượng thời gian làm bài theo SỐ CÂU và DẠNG CÂU.
 *
 * Vì sao có: trước đây mọi đề mới đều nhận mặc định 45 phút (đề 8 câu hay 40 câu cũng vậy), nên
 * thầy phải tự nhẩm rồi sửa tay — hoặc để nguyên con số sai. Một chỗ duy nhất lo việc ước lượng để
 * trang ngân hàng câu hỏi, trang đăng đề và bộ đọc file Word cho ra cùng một con số.
 *
 * Định mức mỗi câu (phút) — theo thời gian THỰC TẾ học sinh làm, không phải theo thang điểm:
 *  - trắc nghiệm A–D: 1,5′ (đọc + tính + khoanh; đề 45′ ↔ 30 câu là nhịp quen thuộc)
 *  - đúng/sai 4 ý: 2′ (mỗi ý phải xét riêng, không đoán được cả câu)
 *  - trả lời ngắn: 2,5′ (phải tính ra số rồi viết, không loại trừ được phương án)
 *  - tự luận: 8′ (trình bày lời giải)
 * Đây là ƯỚC LƯỢNG để gợi ý, không tự áp đặt: nơi gọi chỉ hiện gợi ý + nút dùng một chạm, và tôn
 * trọng con số thầy đã gõ.
 */

const MINUTES_PER_QUESTION: Record<ExamQuestion["type"], number> = {
  multiple_choice: 1.5,
  true_false: 2,
  short_answer: 2.5,
  essay: 8,
};

const SHORT_LABEL: Record<ExamQuestion["type"], string> = {
  multiple_choice: "TN",
  true_false: "ĐS",
  short_answer: "TLN",
  essay: "tự luận",
};

const ORDER: ExamQuestion["type"][] = ["multiple_choice", "true_false", "short_answer", "essay"];

function fmt(n: number): string {
  return String(n).replace(".", ",");
}

export interface DurationEstimate {
  /** Số phút gợi ý, đã làm tròn lên bội số 5 và kẹp trong 5–180. */
  minutes: number;
  /** Vì sao ra số đó, để thầy kiểm được: "24 TN × 1,5′ · 8 ĐS × 2′". */
  note: string;
}

/** Trả `null` khi chưa có câu nào — không đoán bừa. */
export function estimateDuration(questions: ExamQuestion[]): DurationEstimate | null {
  if (questions.length === 0) return null;

  const counts = new Map<ExamQuestion["type"], number>();
  let raw = 0;
  for (const q of questions) {
    const w = MINUTES_PER_QUESTION[q.type] ?? 2;
    raw += w;
    counts.set(q.type, (counts.get(q.type) ?? 0) + 1);
  }

  const minutes = Math.min(180, Math.max(5, Math.ceil(raw / 5) * 5));
  const note = ORDER.filter((t) => counts.get(t))
    .map((t) => `${counts.get(t)} ${SHORT_LABEL[t]} × ${fmt(MINUTES_PER_QUESTION[t])}′`)
    .join(" · ");

  return { minutes, note };
}
