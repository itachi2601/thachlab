// "Bước tiếp theo" ở trang chủ học sinh (thẻ "Hôm nay em làm gì", components/dashboard/TodayCard.tsx) — rule-based, chỉ dùng dữ liệu
// trang chủ đã tải sẵn (tutoring_needs, điểm bài làm, kỹ năng yếu, tiến độ bài). Không có RPC/migration mới. Xem docs/ROADMAP.md, Giai đoạn 2.
// Thầy chốt 8/10/2026: trang chủ chỉ gợi việc THÍCH ỨNG theo hồ sơ em. Thầy chốt lại 17/10/2026: đề KIỂM TRA lớp đã giao mà em
// chưa làm (class_assessments, 21 ngày gần nhất) quay lại thẻ, chung 2 suất đầu với BTVN — em bỏ lỡ chuông thì vẫn thấy.

export type NextStepKind = "homework" | "assigned" | "unlock" | "weak" | "retry" | "lesson" | "review";

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

export interface HomeworkInput {
  examId: number;
  examTitle: string;
  /** ISO; null = không đặt hạn. */
  dueAt: string | null;
  note: string;
}

export interface AssignedInput {
  examId: number;
  examTitle: string;
  /** ISO — ngày thầy giao đề cho lớp. */
  publishedAt: string;
  /** "Giữa kỳ" / "Cuối kỳ" / … (rỗng nếu không rõ). */
  kindLabel: string;
}

export interface NextStepInput {
  /** Đề kiểm tra lớp đã giao, em chưa làm — xếp sau BTVN, chung 2 suất đầu. */
  assigned?: AssignedInput[];
  /** BTVN trợ giảng giao riêng cho em và em chưa nộp — việc đầu tiên (giao đích danh, có hạn). */
  homework?: HomeworkInput[];
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

/** "Hạn 21:00 thứ Sáu 23/10" / "Quá hạn, làm bù vẫn được" / "" khi không đặt hạn. */
export function homeworkDueText(dueAt: string | null, now: Date = new Date()): string {
  if (!dueAt) return "";
  const due = new Date(dueAt);
  if (Number.isNaN(due.getTime())) return "";
  if (due.getTime() < now.getTime()) return "Quá hạn, làm bù vẫn được";
  const day = due.toLocaleDateString("vi-VN", { weekday: "long", day: "2-digit", month: "2-digit" });
  const hm = due.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit", hour12: false });
  return `Hạn ${hm} ${day}`;
}

/** Điểm tốt nhất của đề dưới ngưỡng này mới gợi ý làm lại. */
export const RETRY_BELOW_SCORE = 6.5;

/** Số việc tối đa trên thẻ: 1 nút nổi + 3 lựa chọn. */
export const MAX_STEPS = 4;

/** Lời động viên khi em không có chỗ hổng nào: bài kế thành việc đầu, kèm lời này. */
export const ENCOURAGE = "Em đang học rất tốt, hãy tiếp tục tăng tốc. Thử sức mình với những bài thầy chưa dạy nhé.";

/**
 * Thứ tự: BTVN trợ giảng giao riêng → đề kiểm tra lớp chưa làm (chung 2 suất) → mở khoá chủ đề phụ đạo → kỹ năng yếu (tối đa 2) → làm lại đề điểm thấp → học bài kế.
 * Việc sửa lỗi đứng đầu khi có; không có thì "Học tiếp" đứng đầu kèm lời động viên. "Học tiếp" luôn có mặt khi còn bài
 * (còn trong 4 việc), để em không toàn việc sửa lỗi. Chủ đề đang chờ giãn cách bị đẩy xuống cuối.
 */
export function rankNextSteps(input: NextStepInput): NextStep[] {
  const steps: NextStep[] = [];
  let locked: NextStep | null = null;

  // Tối đa 2 bài BTVN đứng đầu (bài hạn gần nhất trước, do my_pending_homework đã sắp). Còn chỗ cho việc thích ứng.
  for (const h of (input.homework ?? []).slice(0, 2)) {
    steps.push({
      kind: "homework",
      key: `homework-${h.examId}`,
      action: "Bài tập về nhà",
      title: h.examTitle,
      hint: [homeworkDueText(h.dueAt), h.note].filter(Boolean).join(". "),
      href: `/kiem-tra/lam?id=${h.examId}`,
    });
  }

  // Đề kiểm tra lớp đã giao mà em chưa làm: lấp suất còn lại trong 2 suất đầu (đề giao mới nhất trước).
  const homeworkIds = new Set((input.homework ?? []).map((h) => h.examId));
  const assigned = (input.assigned ?? []).filter((a) => !homeworkIds.has(a.examId));
  for (const a of assigned.slice(0, Math.max(0, 2 - steps.length))) {
    const d = new Date(a.publishedAt);
    const day = `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}`;
    steps.push({
      kind: "assigned",
      key: `assigned-${a.examId}`,
      action: "Kiểm tra của lớp",
      title: a.examTitle,
      hint: [a.kindLabel, `Thầy giao ngày ${day}, em chưa làm`].filter(Boolean).join(". "),
      href: `/kiem-tra/lam?id=${a.examId}`,
    });
  }
  const homeworkCount = steps.length; // BTVN + đề lớp đã giao (tối đa 2)

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
  // Có BTVN thì chỉ 1 kỹ năng yếu, để "Học tiếp" không bị cắt khỏi 4 việc.
  for (const w of weak.slice(0, homeworkCount > 0 ? 1 : 2)) {
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

  const retryIsHomework = steps.some((st) => st.href === `/kiem-tra/lam?id=${input.retryExam?.examId}`);
  if (input.retryExam && !retryIsHomework && input.retryExam.score < RETRY_BELOW_SCORE) {
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
