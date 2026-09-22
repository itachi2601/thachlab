// Trạng thái "quá trình học tập": tách bạch hoàn thành hoạt động vs. đạt ngưỡng
// giáo viên cấu hình. Hàm thuần — không gọi Supabase — để dễ ghép ở nhiều nơi
// (trang bài học, bảng giáo viên, hồ sơ học sinh) và dễ tự kiểm bằng script.

export type ActivityStatus =
  | "not_started" // chưa có bất kỳ ghi nhận nào
  | "in_progress" // đã bắt đầu, chưa nộp/xác nhận xong
  | "submitted" // đã nộp/xác nhận xong, chưa có ngưỡng để đánh giá đạt
  | "completed_not_passed" // đã làm, có ngưỡng, chưa đạt
  | "passed" // đạt ngưỡng
  | "pending_grading"; // có câu tự luận chưa chấm tay

export const STATUS_LABELS: Record<ActivityStatus, string> = {
  not_started: "Chưa bắt đầu",
  in_progress: "Đang thực hiện",
  submitted: "Đã hoàn thành",
  completed_not_passed: "Đã hoàn thành nhưng chưa đạt",
  passed: "Đã đạt",
  pending_grading: "Chờ chấm",
};

// ---------- Lý thuyết ----------
export interface TheoryQuizAttempt {
  createdAt: string;
  correctCount: number;
}

export interface TheoryStatusInput {
  confirmedRead: boolean;
  quizAttempts: TheoryQuizAttempt[]; // rỗng nếu mục không gắn quiz
  minCorrect: number | null; // null = mục không gắn quiz kiểm tra nhanh
}

export interface TheoryStatusResult {
  status: ActivityStatus;
  label: string;
  bestCorrect: number | null;
  attemptCount: number;
}

/**
 * Không gắn quiz: chỉ 2 trạng thái, "Đã tự xác nhận đọc" — không gọi là "Đã đạt"
 * (đề bài §2: bài chưa có câu hỏi kiểm tra không được gắn nhãn "Đã đạt").
 * Có gắn quiz: đọc-xác-nhận và đạt-quiz là 2 việc tách biệt; badge ưu tiên kết
 * quả quiz vì đó là tín hiệu "đạt yêu cầu" thật, đọc-xác-nhận chỉ là hoàn thành.
 */
export function deriveTheoryStatus(input: TheoryStatusInput): TheoryStatusResult {
  const { confirmedRead, quizAttempts, minCorrect } = input;
  const attemptCount = quizAttempts.length;
  const bestCorrect = attemptCount > 0 ? Math.max(...quizAttempts.map((a) => a.correctCount)) : null;

  if (minCorrect === null) {
    if (!confirmedRead) return { status: "not_started", label: STATUS_LABELS.not_started, bestCorrect, attemptCount };
    return { status: "submitted", label: "Đã tự xác nhận đọc", bestCorrect, attemptCount };
  }

  if (!confirmedRead && attemptCount === 0) {
    return { status: "not_started", label: STATUS_LABELS.not_started, bestCorrect, attemptCount };
  }
  if (bestCorrect !== null && bestCorrect >= minCorrect) {
    return { status: "passed", label: STATUS_LABELS.passed, bestCorrect, attemptCount };
  }
  if (attemptCount > 0) {
    return {
      status: "completed_not_passed",
      label: STATUS_LABELS.completed_not_passed,
      bestCorrect,
      attemptCount,
    };
  }
  return { status: "in_progress", label: STATUS_LABELS.in_progress, bestCorrect, attemptCount };
}

// ---------- Luyện tập ----------
export interface PracticeStatusInput {
  sessionCount: number;
  bestScore10: number | null; // null nếu chưa luyện lần nào
  passScore: number | null; // null = giáo viên chưa cấu hình ngưỡng
}

export interface PracticeStatusResult {
  status: ActivityStatus;
  label: string;
}

export function derivePracticeStatus(input: PracticeStatusInput): PracticeStatusResult {
  const { sessionCount, bestScore10, passScore } = input;
  if (sessionCount === 0) return { status: "not_started", label: STATUS_LABELS.not_started };
  if (passScore === null) return { status: "submitted", label: "Đã luyện tập" };
  if (bestScore10 !== null && bestScore10 >= passScore) return { status: "passed", label: STATUS_LABELS.passed };
  return { status: "completed_not_passed", label: STATUS_LABELS.completed_not_passed };
}

// ---------- Đề kiểm tra / bài tập về nhà / quiz lý thuyết (đều qua ExamRunner) ----------
export interface GradedAttemptSummary {
  createdAt: string;
  score10: number; // exam_results.score — điểm tự động, CHƯA cộng tự luận đã chấm
  finalScore10: number | null; // exam_result_scores.final_score10 — đã cộng tự luận (null nếu view chưa sẵn sàng)
  pendingEssayCount: number;
}

export interface GradedStatusInput {
  hasOpenAttempt: boolean; // exam_attempts có dòng started_at gần đây, submitted_at null
  results: GradedAttemptSummary[];
  passScore: number | null; // null = giáo viên chưa cấu hình ngưỡng
}

export interface GradedStatusResult {
  status: ActivityStatus;
  label: string;
  best: GradedAttemptSummary | null;
  latest: GradedAttemptSummary | null;
  first: GradedAttemptSummary | null;
  attemptCount: number;
}

/** Điểm dùng để so ngưỡng/xếp hạng: điểm cuối đã cộng tự luận nếu có, không thì điểm tự động. */
function effectiveScore(r: GradedAttemptSummary): number {
  return r.finalScore10 ?? r.score10;
}

export function pickFirstLatestBest(results: GradedAttemptSummary[]): {
  first: GradedAttemptSummary | null;
  latest: GradedAttemptSummary | null;
  best: GradedAttemptSummary | null;
} {
  if (results.length === 0) return { first: null, latest: null, best: null };
  const byTime = [...results].sort((a, b) => Date.parse(a.createdAt) - Date.parse(b.createdAt));
  const best = results.reduce((a, b) => (effectiveScore(b) > effectiveScore(a) ? b : a));
  return { first: byTime[0], latest: byTime[byTime.length - 1], best };
}

/**
 * "Chờ chấm" thắng mọi trạng thái khác khi lượt gần nhất/tốt nhất có câu tự
 * luận chưa chấm — đúng đề bài §3: "có tự luận chưa chấm thì hiển thị Chờ chấm".
 * Xét trên lượt TỐT NHẤT (không phải mới nhất): một lượt cũ đã đạt vẫn nên báo
 * "Đã đạt" dù em vừa nộp thêm một lượt mới có tự luận đang chờ chấm.
 */
export function deriveGradedStatus(input: GradedStatusInput): GradedStatusResult {
  const { hasOpenAttempt, results, passScore } = input;
  const { first, latest, best } = pickFirstLatestBest(results);
  const attemptCount = results.length;

  if (attemptCount === 0) {
    return {
      status: hasOpenAttempt ? "in_progress" : "not_started",
      label: hasOpenAttempt ? STATUS_LABELS.in_progress : STATUS_LABELS.not_started,
      best,
      latest,
      first,
      attemptCount,
    };
  }

  const anyPendingEssay = results.some((r) => r.pendingEssayCount > 0);
  if (best && best.pendingEssayCount > 0) {
    return { status: "pending_grading", label: STATUS_LABELS.pending_grading, best, latest, first, attemptCount };
  }
  if (anyPendingEssay) {
    // Lượt tốt nhất đã chấm xong nhưng còn lượt khác chờ chấm — vẫn ưu tiên báo Chờ chấm
    // để giáo viên không bỏ sót, nhưng không đè lên kết quả Đã đạt đã chắc chắn.
    if (best && passScore !== null && effectiveScore(best) >= passScore) {
      return { status: "passed", label: STATUS_LABELS.passed, best, latest, first, attemptCount };
    }
    return { status: "pending_grading", label: STATUS_LABELS.pending_grading, best, latest, first, attemptCount };
  }

  if (passScore === null) {
    return { status: "submitted", label: "Đã nộp", best, latest, first, attemptCount };
  }
  if (best && effectiveScore(best) >= passScore) {
    return { status: "passed", label: STATUS_LABELS.passed, best, latest, first, attemptCount };
  }
  return { status: "completed_not_passed", label: STATUS_LABELS.completed_not_passed, best, latest, first, attemptCount };
}

/** Gợi ý mặc định khi soạn quiz lý thuyết: đúng ít nhất 2/3 số câu, làm tròn lên. */
export function suggestedMinCorrect(questionCount: number): number {
  return Math.max(1, Math.ceil((questionCount * 2) / 3));
}

// ---------- Tổng hợp % hoàn thành / % đạt trên các mục bắt buộc ----------
export function isCompletedStatus(status: ActivityStatus): boolean {
  return status !== "not_started" && status !== "in_progress";
}

export interface ProgressCountable {
  required: boolean;
  status: ActivityStatus;
  /** Mục có ngưỡng "đạt" được giáo viên cấu hình không (quiz/luyện tập/đề). */
  hasThreshold: boolean;
}

export interface ProgressSummary {
  totalRequired: number;
  completedRequired: number;
  passedRequired: number;
}

/**
 * % đạt chỉ trừ điểm những mục THỰC SỰ có ngưỡng mà chưa đạt — mục không có
 * ngưỡng nào được cấu hình (video, bài tập mẫu, lý thuyết không quiz…) thì
 * "hoàn thành" cũng coi là "đạt" luôn, vì không có gì để "chưa đạt" cả.
 */
// Từ "đáng lo" nhất đến "tốt" nhất — dùng để gộp nhiều mục cùng loại (vd nhiều mục
// lý thuyết trong 1 bài) thành 1 trạng thái đại diện cho bảng giáo viên: ưu tiên lộ ra
// người chưa bắt đầu / còn chờ chấm / làm nhiều lần vẫn chưa đạt, đúng yêu cầu đề bài.
const STATUS_PRIORITY: ActivityStatus[] = [
  "not_started",
  "in_progress",
  "pending_grading",
  "completed_not_passed",
  "submitted",
  "passed",
];

export function dominantStatus(statuses: ActivityStatus[]): ActivityStatus | null {
  if (statuses.length === 0) return null;
  let worst = statuses[0];
  let worstRank = STATUS_PRIORITY.indexOf(worst);
  for (const s of statuses.slice(1)) {
    const rank = STATUS_PRIORITY.indexOf(s);
    if (rank < worstRank) {
      worst = s;
      worstRank = rank;
    }
  }
  return worst;
}

export function summarizeProgress(items: ProgressCountable[]): ProgressSummary {
  const required = items.filter((i) => i.required);
  const completedRequired = required.filter((i) => isCompletedStatus(i.status)).length;
  const passedRequired = required.filter(
    (i) => i.status === "passed" || (isCompletedStatus(i.status) && !i.hasThreshold),
  ).length;
  return { totalRequired: required.length, completedRequired, passedRequired };
}
