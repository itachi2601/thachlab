// Khoá hành vi: thang luyện tập, trạng thái tiến độ (điểm ngưỡng đạt), chấm 1 câu luyện tập.
import { describe, expect, it } from "vitest";
import { LADDER_MIN_QUESTIONS, LADDER_PASS_RATIO, nextLadderLevel, pickForLevel } from "@/features/lessons/practice-ladder";
import { isFullyCorrect } from "@/features/lessons/practice-step";
import {
  deriveGradedStatus,
  derivePracticeStatus,
  deriveTheoryStatus,
  dominantStatus,
  pickFirstLatestBest,
  summarizeProgress,
  suggestedMinCorrect,
  type GradedAttemptSummary,
} from "@/features/progress/types";
import type { ExamQuestion } from "@/features/exams/types";

describe("thang luyện tập", () => {
  it("ngưỡng 80%, tối thiểu 5 câu", () => {
    expect(LADDER_PASS_RATIO).toBe(0.8);
    expect(LADDER_MIN_QUESTIONS).toBe(5);
  });
  it("lên mức khi ≥80% và ≥5 câu", () => {
    expect(nextLadderLevel("de", 0.8, 5)).toEqual({ level: "trung-binh", moved: true, atTop: false });
    expect(nextLadderLevel("trung-binh", 1, 10)).toEqual({ level: "kho", moved: true, atTop: false });
  });
  it("giữ mức khi <80% hoặc <5 câu; ở đỉnh báo atTop", () => {
    expect(nextLadderLevel("de", 0.79, 10)).toEqual({ level: "de", moved: false, atTop: false });
    expect(nextLadderLevel("de", 1, 4)).toEqual({ level: "de", moved: false, atTop: false });
    expect(nextLadderLevel("kho", 0.9, 5)).toEqual({ level: "kho", moved: false, atTop: true });
    expect(nextLadderLevel("kho", 0.5, 5)).toEqual({ level: "kho", moved: false, atTop: false });
  });
  it("pickForLevel: đủ câu đúng mức thì chỉ lấy đúng mức; thiếu thì bù nhãn rỗng rồi mức kề", () => {
    const bank = [
      ...[1, 2].map((i) => ({ id: `de${i}`, question: { difficulty: "de" as const } })),
      { id: "x", question: { difficulty: "" as const } },
      { id: "tb", question: { difficulty: "trung-binh" as const } },
      { id: "kho", question: { difficulty: "kho" as const } },
    ];
    expect(pickForLevel(bank, "de", 2).map((p) => p.id).sort()).toEqual(["de1", "de2"]);
    const three = pickForLevel(bank, "de", 3).map((p) => p.id).sort();
    expect(three).toEqual(["de1", "de2", "x"]);
    const four = pickForLevel(bank, "de", 4).map((p) => p.id);
    expect(four).toContain("tb"); // mức kề gần hơn "kho"
    expect(four).not.toContain("kho");
  });
});

describe("isFullyCorrect (luyện tập từng câu)", () => {
  const tf: ExamQuestion = { type: "true_false", question: "q", statements: [true, false, true, false].map((answer) => ({ text: "t", answer })), explanation: "" };
  it("Đúng/Sai chỉ 'trọn vẹn' khi đủ 4 ý", () => {
    expect(isFullyCorrect(tf, [true, false, true, false])).toBe(true);
    expect(isFullyCorrect(tf, [true, false, true, true])).toBe(false);
  });
  it("tự luận không bao giờ", () => {
    expect(isFullyCorrect({ type: "essay", question: "", suggestedAnswer: "", gradingGuide: "", explanation: "" }, "x")).toBe(false);
  });
});

const att = (createdAt: string, score10: number, finalScore10: number | null = null, pendingEssayCount = 0): GradedAttemptSummary => ({
  createdAt, score10, finalScore10, pendingEssayCount,
});

describe("trạng thái đề/bài tập (deriveGradedStatus)", () => {
  it("chưa làm / đang dở", () => {
    expect(deriveGradedStatus({ hasOpenAttempt: false, results: [], passScore: 5 }).status).toBe("not_started");
    expect(deriveGradedStatus({ hasOpenAttempt: true, results: [], passScore: 5 }).status).toBe("in_progress");
  });
  it("so ngưỡng bằng điểm cuối (đã cộng tự luận) nếu có", () => {
    const r = deriveGradedStatus({ hasOpenAttempt: false, results: [att("2026-01-01", 4, 6)], passScore: 5 });
    expect(r.status).toBe("passed");
    const r2 = deriveGradedStatus({ hasOpenAttempt: false, results: [att("2026-01-01", 6, 4)], passScore: 5 });
    expect(r2.status).toBe("completed_not_passed");
  });
  it("điểm đúng bằng ngưỡng là đạt; không ngưỡng → 'submitted'", () => {
    expect(deriveGradedStatus({ hasOpenAttempt: false, results: [att("2026-01-01", 5)], passScore: 5 }).status).toBe("passed");
    expect(deriveGradedStatus({ hasOpenAttempt: false, results: [att("2026-01-01", 1)], passScore: null }).status).toBe("submitted");
  });
  it("chờ chấm: lượt tốt nhất còn tự luận → pending; lượt cũ đã đạt + lượt mới chờ → vẫn passed", () => {
    expect(deriveGradedStatus({ hasOpenAttempt: false, results: [att("2026-01-01", 9, null, 1)], passScore: 5 }).status).toBe("pending_grading");
    const both = deriveGradedStatus({ hasOpenAttempt: false, results: [att("2026-01-01", 8), att("2026-01-02", 3, null, 2)], passScore: 5 });
    expect(both.status).toBe("passed");
    const notPassed = deriveGradedStatus({ hasOpenAttempt: false, results: [att("2026-01-01", 2), att("2026-01-02", 3, null, 2)], passScore: 5 });
    expect(notPassed.status).toBe("pending_grading");
  });
  it("pickFirstLatestBest", () => {
    const r = pickFirstLatestBest([att("2026-01-03", 5), att("2026-01-01", 9), att("2026-01-02", 7)]);
    expect([r.first?.score10, r.latest?.score10, r.best?.score10]).toEqual([9, 5, 9]);
  });
});

describe("luyện tập / lý thuyết / tổng hợp", () => {
  it("derivePracticeStatus", () => {
    expect(derivePracticeStatus({ sessionCount: 0, bestScore10: null, passScore: 5 }).status).toBe("not_started");
    expect(derivePracticeStatus({ sessionCount: 2, bestScore10: 4, passScore: null }).status).toBe("submitted");
    expect(derivePracticeStatus({ sessionCount: 2, bestScore10: 5, passScore: 5 }).status).toBe("passed");
    expect(derivePracticeStatus({ sessionCount: 2, bestScore10: 4.99, passScore: 5 }).status).toBe("completed_not_passed");
  });
  it("deriveTheoryStatus", () => {
    const q = (n: number) => ({ createdAt: "x", correctCount: n });
    expect(deriveTheoryStatus({ confirmedRead: false, quizAttempts: [], minCorrect: null }).status).toBe("not_started");
    expect(deriveTheoryStatus({ confirmedRead: true, quizAttempts: [], minCorrect: null }).status).toBe("submitted");
    expect(deriveTheoryStatus({ confirmedRead: true, quizAttempts: [], minCorrect: 7 }).status).toBe("in_progress");
    expect(deriveTheoryStatus({ confirmedRead: false, quizAttempts: [q(6), q(7)], minCorrect: 7 }).status).toBe("passed");
    expect(deriveTheoryStatus({ confirmedRead: false, quizAttempts: [q(3)], minCorrect: 7 }).status).toBe("completed_not_passed");
  });
  it("suggestedMinCorrect = ceil(2n/3), tối thiểu 1", () => {
    expect([0, 1, 3, 10, 20].map(suggestedMinCorrect)).toEqual([1, 1, 2, 7, 14]);
  });
  it("dominantStatus & summarizeProgress", () => {
    expect(dominantStatus([])).toBeNull();
    expect(dominantStatus(["passed", "pending_grading", "submitted"])).toBe("pending_grading");
    const s = summarizeProgress([
      { required: true, status: "passed", hasThreshold: true },
      { required: true, status: "submitted", hasThreshold: false }, // không ngưỡng: hoàn thành = đạt
      { required: true, status: "completed_not_passed", hasThreshold: true },
      { required: true, status: "in_progress", hasThreshold: false },
      { required: false, status: "passed", hasThreshold: true },
    ]);
    expect(s).toEqual({ totalRequired: 4, completedRequired: 3, passedRequired: 2 });
  });
});
