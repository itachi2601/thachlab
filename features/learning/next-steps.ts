// "Bước tiếp theo" ở trang chủ học sinh (thẻ "Hôm nay em làm gì", components/dashboard/TodayCard.tsx) — bản rút gọn, rule-based, chỉ dùng dữ liệu trang chủ đã tải sẵn
// (tutoring_needs, điểm bài làm, tiến độ bài). Không có RPC/migration mới. Xem docs/ROADMAP.md, Giai đoạn 2.

/** "assigned" không do rankNextSteps sinh — trang chủ tự thêm bài kiểm tra/BTVN được giao lên trước. */
export type NextStepKind = "assigned" | "unlock" | "weak" | "retry" | "lesson" | "review";

export interface NextStep {
  kind: NextStepKind;
  key: string;
  /** Nhãn hành động ngắn, in nhỏ phía trên tên ("Mở khoá", "Làm lại", "Học tiếp", "Ôn lại"). */
  action: string;
  /** Tên việc, không kèm nhãn hành động. */
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
  /** Kỹ năng (YCCĐ) yếu nhất từ get_my_weakest_topics — chỉ dùng khi em không có chủ đề phụ đạo (một việc sửa lỗi mỗi lần). */
  weak?: { topicId: number; topicName: string; lessonId: number; chapterId: number; pct: number } | null;
  /** Bài đã học xong gần nhất — việc "ôn lại cách quãng" khi hết việc khác (thay cho dòng "chọn một bài bất kỳ"). */
  reviewLesson?: { id: number; chapterId: number; title: string } | null;
}

/** Điểm tốt nhất của đề dưới ngưỡng này mới gợi ý làm lại. */
export const RETRY_BELOW_SCORE = 6.5;

/**
 * Tối đa 3 việc, đúng thứ tự: mở khoá chủ đề phụ đạo (hoặc, nếu không có, luyện kỹ năng yếu nhất) → làm lại đề điểm thấp
 * → học bài kế. Chỉ MỘT việc sửa lỗi được đưa ra mỗi lần (em yếu không thấy toàn việc sửa lỗi); "học bài kế" luôn
 * giữ chỗ khi còn bài để mỗi ngày có ít nhất một việc dễ thắng. Chủ đề đang chờ giãn cách bị đẩy xuống cuối.
 */
export function rankNextSteps(input: NextStepInput): NextStep[] {
  const steps: NextStep[] = [];
  let locked: NextStep | null = null;

  if (input.need) {
    const step: NextStep = {
      kind: "unlock",
      key: `unlock-${input.need.id}`,
      action: "Mở khoá chủ đề",
      title: input.need.label,
      hint: "Xem lại lý thuyết, làm bài, đạt từ 80% là mở khoá",
      needId: input.need.id,
    };
    if (input.needAvailableAt) locked = { ...step, lockedUntil: input.needAvailableAt };
    else steps.push(step);
  }

  if (!input.need && input.weak) {
    steps.push({
      kind: "weak",
      key: `weak-${input.weak.topicId}`,
      action: "Luyện kỹ năng yếu",
      title: input.weak.topicName,
      hint: `Đang đúng ${input.weak.pct}% — luyện nhanh 10 câu ở cuối bài để nâng mức`,
      href: `/lop-hoc/bai?id=${input.weak.lessonId}&chapter=${input.weak.chapterId}`,
    });
  }

  if (input.retryExam && input.retryExam.score < RETRY_BELOW_SCORE) {
    steps.push({
      kind: "retry",
      key: `retry-${input.retryExam.examId}`,
      action: "Làm lại",
      title: input.retryExam.examTitle,
      hint: `Lần trước ${input.retryExam.score.toLocaleString("vi-VN")} điểm — làm lại để chốt kiến thức`,
      href: `/kiem-tra/lam?id=${input.retryExam.examId}`,
    });
  }

  if (input.nextLesson) {
    steps.push({
      kind: "lesson",
      key: `lesson-${input.nextLesson.id}`,
      action: "Học tiếp",
      title: input.nextLesson.title,
      hint: input.nextLesson.chapterTitle ?? "",
      href: `/lop-hoc/bai?id=${input.nextLesson.id}&chapter=${input.nextLesson.chapterId}`,
    });
  }

  // Không còn việc làm được ngay → "Ôn lại" giữ chỗ nút nổi; chủ đề đang chờ giãn cách (mờ) xếp sau nó.
  if (steps.length === 0) {
    const r = input.reviewLesson;
    steps.push(
      r
        ? {
            kind: "review",
            key: `review-${r.id}`,
            action: "Ôn lại",
            title: r.title,
            hint: "Đọc lại, làm lại phần kiểm tra nhanh và thử câu thử thách ⭐⭐⭐ — ôn cách vài ngày giúp nhớ lâu",
            href: `/lop-hoc/bai?id=${r.id}&chapter=${r.chapterId}`,
          }
        : {
            kind: "review",
            key: "review",
            action: "Ôn lại",
            title: "Các bài đã học",
            hint: "Chọn một bài bất kỳ để luyện thêm",
            href: "/lop-hoc",
          },
    );
  }
  if (locked) steps.push(locked);
  return steps.slice(0, 3);
}
