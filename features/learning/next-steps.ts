// "Bước tiếp theo" ở trang chủ học sinh — bản rút gọn, rule-based, chỉ dùng dữ liệu trang chủ đã tải sẵn
// (tutoring_needs, điểm bài làm, tiến độ bài). Không có RPC/migration mới. Xem docs/ROADMAP.md, Giai đoạn 2.

export type NextStepKind = "unlock" | "retry" | "lesson" | "review";

export interface NextStep {
  kind: NextStepKind;
  key: string;
  title: string;
  hint: string;
  /** Có href → liên kết; không có → bấm gọi onUnlock. */
  href?: string;
  needId?: number;
  /** Chỉ bước unlock: chưa tới giờ làm lượt tiếp theo. */
  lockedUntil?: Date;
}

export interface NextStepInput {
  need: { id: number; label: string } | null;
  /** Thời điểm được làm lượt tiếp theo của chủ đề (null = làm được ngay). */
  needAvailableAt: Date | null;
  retryExam: { examId: number; examTitle: string; score: number } | null;
  nextLesson: { id: number; chapterId: number; title: string; chapterTitle?: string } | null;
}

/** Điểm tốt nhất của đề dưới ngưỡng này mới gợi ý làm lại. */
export const RETRY_BELOW_SCORE = 6.5;

/**
 * Tối đa 3 việc, đúng thứ tự: mở khoá chủ đề phụ đạo → làm lại đề điểm thấp → học bài kế.
 * Chỉ MỘT chủ đề phụ đạo được đưa ra mỗi lần (em yếu không thấy toàn việc sửa lỗi); "học bài kế" luôn
 * giữ chỗ khi còn bài để mỗi ngày có ít nhất một việc dễ thắng. Chủ đề đang chờ giãn cách bị đẩy xuống cuối.
 */
export function rankNextSteps(input: NextStepInput): NextStep[] {
  const steps: NextStep[] = [];
  let locked: NextStep | null = null;

  if (input.need) {
    const step: NextStep = {
      kind: "unlock",
      key: `unlock-${input.need.id}`,
      title: `Mở khoá chủ đề: ${input.need.label}`,
      hint: "Xem lại lý thuyết, làm bài, đạt từ 80% là mở khoá",
      needId: input.need.id,
    };
    if (input.needAvailableAt) locked = { ...step, lockedUntil: input.needAvailableAt };
    else steps.push(step);
  }

  if (input.retryExam && input.retryExam.score < RETRY_BELOW_SCORE) {
    steps.push({
      kind: "retry",
      key: `retry-${input.retryExam.examId}`,
      title: `Làm lại: ${input.retryExam.examTitle}`,
      hint: `Lần trước ${input.retryExam.score.toLocaleString("vi-VN")} điểm — làm lại để chốt kiến thức`,
      href: `/kiem-tra/lam?id=${input.retryExam.examId}`,
    });
  }

  if (input.nextLesson) {
    steps.push({
      kind: "lesson",
      key: `lesson-${input.nextLesson.id}`,
      title: `Học tiếp: ${input.nextLesson.title}`,
      hint: input.nextLesson.chapterTitle ?? "",
      href: `/lop-hoc/bai?id=${input.nextLesson.id}&chapter=${input.nextLesson.chapterId}`,
    });
  }

  if (locked) steps.push(locked);

  if (steps.length === 0) {
    steps.push({
      kind: "review",
      key: "review",
      title: "Ôn lại các bài đã học",
      hint: "Chọn một bài bất kỳ để luyện thêm",
      href: "/lop-hoc",
    });
  }
  return steps.slice(0, 3);
}
