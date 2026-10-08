// "Bước tiếp theo" ở trang chủ học sinh (thẻ "Hôm nay em làm gì", components/dashboard/TodayCard.tsx) — rule-based, chỉ dùng dữ liệu
// trang chủ đã tải sẵn (tutoring_needs, điểm bài làm, kỹ năng yếu, tiến độ bài). Không có RPC/migration mới. Xem docs/ROADMAP.md, Giai đoạn 2.
// Thầy chốt 8/10/2026: trang chủ chỉ gợi việc THÍCH ỨNG theo hồ sơ em, không còn việc/bài giao chung cho cả lớp.

export type NextStepKind = "unlock" | "weak" | "retry" | "lesson" | "review";

export interface NextStep {
  kind: NextStepKind;
  key: string;
  /** Nhãn hành động ngắn, in nhỏ phía trên tên ("Mở khoá", "Luyện kỹ năng yếu", "Làm lại", "Học tiếp", "Ôn lại"). */
  action: string;
  /** Tên việc, không kèm nhãn hành động. */
  title: string;
  hint: string;
  /** Có href → liên kết; không có → bấm gọi onUnlock (unlock) hoặc onQuickPractice (weak). */
  href?: string;
  needId?: number;
  /** Chỉ bước weak: luyện nhanh 10 câu mở ngay tại trang chủ (href là đường lui khi không mở được). */
  practice?: { lessonId: number; topicName: string };
  /** Chỉ bước unlock: chưa tới giờ làm lượt tiếp theo. */
  lockedUntil?: Date;
}

export interface WeakInput {
  topicId: number;
  topicName: string;
  lessonId: number;
  lessonTitle: string;
  chapterId: number;
  pct: number;
}

export interface NextStepInput {
  need: { id: number; label: string } | null;
  /** Thời điểm được làm lượt tiếp theo của chủ đề (null = làm được ngay). */
  needAvailableAt: Date | null;
  retryExam: { examId: number; examTitle: string; score: number } | null;
  /** completed/total: mục đã xong trong bài đang dở (hiện "Đang dở: 3/8 mục" để em muốn làm nốt). */
  nextLesson: { id: number; chapterId: number; title: string; chapterTitle?: string; completed?: number; total?: number } | null;
  /** Kỹ năng (YCCĐ) yếu nhất, tối đa 2 mục đầu được dùng. */
  weak?: WeakInput[];
  /** Bài đã học xong gần nhất — việc "ôn lại" khi hết việc khác. */
  reviewLesson?: { id: number; chapterId: number; title: string } | null;
}

/** Điểm tốt nhất của đề dưới ngưỡng này mới gợi ý làm lại. */
export const RETRY_BELOW_SCORE = 6.5;

/** Số việc tối đa trên thẻ: 1 nút nổi + 3 lựa chọn. */
export const MAX_STEPS = 4;

/** Lời động viên khi em không có chỗ hổng nào: bài kế thành việc đầu, kèm lời này. */
export const ENCOURAGE = "Em đang học rất tốt, hãy tiếp tục tăng tốc. Thử sức mình với những bài thầy chưa dạy nhé.";

/**
 * Thứ tự: mở khoá chủ đề phụ đạo → kỹ năng yếu (tối đa 2) → làm lại đề điểm thấp → học bài kế.
 * Việc sửa lỗi đứng đầu khi có; không có thì "Học tiếp" đứng đầu kèm lời động viên. "Học tiếp" luôn có mặt khi còn bài
 * (còn trong 4 việc), để em không toàn việc sửa lỗi. Chủ đề đang chờ giãn cách bị đẩy xuống cuối.
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

  const weak = input.weak ?? [];
  for (const w of weak.slice(0, 2)) {
    steps.push({
      kind: "weak",
      key: `weak-${w.topicId}`,
      action: "Luyện kỹ năng yếu",
      title: w.topicName,
      hint: `Đang đúng ${w.pct}% · 10 câu, khoảng 5 phút`,
      href: `/lop-hoc/bai?id=${w.lessonId}&chapter=${w.chapterId}`,
      practice: { lessonId: w.lessonId, topicName: w.topicName },
    });
  }

  if (input.retryExam && input.retryExam.score < RETRY_BELOW_SCORE) {
    steps.push({
      kind: "retry",
      key: `retry-${input.retryExam.examId}`,
      action: "Làm lại",
      title: input.retryExam.examTitle,
      hint: `Lần trước ${input.retryExam.score.toLocaleString("vi-VN")} điểm. Làm lại không cộng thêm RP bài này`,
      href: `/kiem-tra/lam?id=${input.retryExam.examId}`,
    });
  }

  if (input.nextLesson) {
    const l = input.nextLesson;
    const remedial = steps.length > 0;
    const part = l.total && l.completed ? `Đang dở: ${l.completed}/${l.total} mục` : (l.chapterTitle ?? "");
    steps.push({
      kind: "lesson",
      key: `lesson-${l.id}`,
      action: "Học tiếp",
      title: l.title,
      hint: remedial ? part : [part, ENCOURAGE].filter(Boolean).join(". "),
      href: `/lop-hoc/bai?id=${l.id}&chapter=${l.chapterId}`,
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
            hint: "Đọc lại, làm lại phần kiểm tra nhanh và thử câu thử thách ⭐⭐⭐. Ôn cách vài ngày giúp nhớ lâu",
            href: `/lop-hoc/bai?id=${r.id}&chapter=${r.chapterId}`,
          }
        : { kind: "review", key: "review", action: "Ôn lại", title: "Các bài đã học", hint: "Chọn một bài bất kỳ để luyện thêm", href: "/lop-hoc" },
    );
  }
  if (locked) steps.push(locked);
  return steps.slice(0, MAX_STEPS);
}
