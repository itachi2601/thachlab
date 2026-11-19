// KHOÁ hành vi chấm điểm hiện tại (features/exams/types.ts). Không phải đặc tả "đúng": ca nào nghi bug được
// đánh dấu `NGHI BUG` và khoá đúng kết quả hiện tại — nếu sau này sửa logic thì cố ý đổi test cùng lúc.
import { describe, expect, it } from "vitest";
import {
  buildQuestionResults,
  emptyResponses,
  gradeExam,
  gradeQuestion,
  isAnswered,
  questionStatus,
  translationScore,
  translationTokens,
  type ExamQuestion,
} from "@/features/exams/types";

const mc = (answer: number): ExamQuestion => ({ type: "multiple_choice", question: "q", options: ["a", "b", "c", "d"], answer, explanation: "" });
const tf = (ans: boolean[]): ExamQuestion => ({
  type: "true_false",
  question: "q",
  statements: ans.map((answer, i) => ({ text: `ý ${i}`, answer })),
  explanation: "",
});
const sa = (answer: string): ExamQuestion => ({ type: "short_answer", question: "q", answer, explanation: "" });
const essay: ExamQuestion = { type: "essay", question: "q", suggestedAnswer: "", gradingGuide: "", explanation: "" };
const tr = (answers: string[], points?: number): ExamQuestion => ({ type: "translation", question: "q", answers, points, explanation: "" });

describe("Phần I — trắc nghiệm A–D (0,25đ/câu)", () => {
  it("đúng/sai/bỏ trống", () => {
    expect(gradeQuestion(mc(2), 2)).toEqual({ earned: 0.25, max: 0.25 });
    expect(gradeQuestion(mc(2), 1)).toEqual({ earned: 0, max: 0.25 });
    expect(gradeQuestion(mc(0), null)).toEqual({ earned: 0, max: 0.25 });
    expect(gradeQuestion(mc(0), 0)).toEqual({ earned: 0.25, max: 0.25 }); // đáp án A (chỉ số 0) không bị coi là falsy
  });
  it("kiểu phản hồi sai kiểu → 0 điểm, không ném lỗi", () => {
    expect(gradeQuestion(mc(0), "0").earned).toBe(0);
    expect(gradeQuestion(mc(0), [true]).earned).toBe(0);
  });
});

describe("Phần II — Đúng/Sai a)–d) chấm luỹ tiến 0 / 0,1 / 0,25 / 0,5 / 1", () => {
  const q = tf([true, false, true, false]);
  it.each([
    [[true, false, true, false], 1],
    [[true, false, true, true], 0.5],
    [[true, false, false, true], 0.25],
    [[true, true, false, true], 0.1],
    [[false, true, false, true], 0],
  ])("picks %j → %s", (picks, earned) => {
    expect(gradeQuestion(q, picks as (boolean | null)[])).toEqual({ earned, max: 1 });
  });
  it("ý bỏ trống (null) tính là sai", () => {
    expect(gradeQuestion(q, [true, null, true, null]).earned).toBe(0.25);
    expect(gradeQuestion(q, [null, null, null, null]).earned).toBe(0);
  });
  it("phản hồi không phải mảng → 0", () => {
    expect(gradeQuestion(q, null).earned).toBe(0);
    expect(gradeQuestion(q, "x").earned).toBe(0);
  });
  it("NGHI BUG: câu có ≠4 ý — TF_SCALE cố định 5 bậc, 5 ý đúng cho điểm 0 (đề lỗi cấu trúc)", () => {
    expect(gradeQuestion(tf([true, true, true, true, true]), [true, true, true, true, true]).earned).toBe(0);
    // 3 ý: đúng cả 3 chỉ được 0,5 (thang 4 ý)
    expect(gradeQuestion(tf([true, true, true]), [true, true, true]).earned).toBe(0.5);
  });
});

describe("Phần III — đáp số (short_answer, 0,25đ/câu)", () => {
  it("khớp chuỗi sau khi trim và đổi dấu chấm → dấu phẩy", () => {
    expect(gradeQuestion(sa("-1,5"), "-1,5").earned).toBe(0.25);
    expect(gradeQuestion(sa("-1,5"), " -1.5 ").earned).toBe(0.25);
    expect(gradeQuestion(sa("12"), "12").earned).toBe(0.25);
  });
  it("sai / bỏ trống", () => {
    expect(gradeQuestion(sa("12"), "13").earned).toBe(0);
    expect(gradeQuestion(sa("12"), "").earned).toBe(0);
    expect(gradeQuestion(sa("12"), null).earned).toBe(0);
  });
  it("NGHI BUG: KHÔNG có dung sai số học — chỉ so chuỗi. '1,50' ≠ '1,5', '0,5' ≠ '.5', '3' ≠ '3,0'", () => {
    expect(gradeQuestion(sa("1,5"), "1,50").earned).toBe(0);
    expect(gradeQuestion(sa("0,5"), ".5").earned).toBe(0);
    expect(gradeQuestion(sa("3"), "3,0").earned).toBe(0);
  });
  it("NGHI BUG: replace('.') chỉ đổi dấu chấm ĐẦU TIÊN → '1.234.5' không bao giờ khớp dạng phẩy", () => {
    expect(gradeQuestion(sa("1,234,5"), "1.234.5").earned).toBe(0);
  });
  it("NGHI BUG: đáp án đúng rỗng → học sinh để trống vẫn 0 điểm (ok), nhưng không bao giờ ai đạt được", () => {
    expect(gradeQuestion(sa(""), "").earned).toBe(0);
  });
});

describe("Tự luận & dịch", () => {
  it("tự luận không cộng điểm tự động (max 0)", () => {
    expect(gradeQuestion(essay, "bài viết")).toEqual({ earned: 0, max: 0 });
  });
  it("tách chữ: bỏ dấu thanh, đ→d, bỏ dấu câu", () => {
    expect(translationTokens("Đường, ĐI! hôm-nay")).toEqual(["duong", "di", "hom", "nay"]);
  });
  it("translationScore: tỉ lệ trùng / max(độ dài), mỗi chữ mẫu khớp 1 lần, lấy bản mẫu tốt nhất", () => {
    expect(translationScore(["con mèo đen"], "con meo den")).toBe(1);
    expect(translationScore(["con mèo đen"], "con mèo")).toBeCloseTo(2 / 3);
    expect(translationScore(["con mèo đen"], "con con con")).toBeCloseTo(1 / 3);
    expect(translationScore(["a b", "con mèo đen"], "con mèo đen")).toBe(1);
    expect(translationScore(["con mèo"], "")).toBe(0);
  });
  it("gradeQuestion translation: điểm mặc định 0,5, làm tròn 2 chữ số", () => {
    expect(gradeQuestion(tr(["con mèo đen"]), "con mèo")).toEqual({ earned: 0.33, max: 0.5 });
    expect(gradeQuestion(tr(["con mèo đen"], 1), "con mèo đen")).toEqual({ earned: 1, max: 1 });
    expect(gradeQuestion(tr(["x"]), null)).toEqual({ earned: 0, max: 0.5 });
  });
});

describe("gradeExam — thang 10 làm tròn 2 chữ số", () => {
  const questions = [mc(0), mc(1), tf([true, false, true, false]), sa("5"), essay];
  it("đúng hết (tự luận bỏ ra ngoài mẫu số)", () => {
    const r = gradeExam(questions, [0, 1, [true, false, true, false], "5", "bài"]);
    expect(r).toEqual({ score10: 10, earned: 1.75, max: 1.75, correctCount: 4 });
  });
  it("sai hết", () => {
    expect(gradeExam(questions, [3, 3, [false, true, false, true], "9", ""])).toEqual({ score10: 0, earned: 0, max: 1.75, correctCount: 0 });
  });
  it("một phần: TN đúng 1, TF đúng 3 ý, đáp số sai", () => {
    const r = gradeExam(questions, [0, 3, [true, false, true, true], "9", ""]);
    expect(r.earned).toBe(0.75);
    expect(r.score10).toBe(4.29); // 0,75/1,75*10 = 4,2857
    expect(r.correctCount).toBe(1); // TF đúng 3 ý chưa tính "đúng trọn"
  });
  it("bài trống/chưa có câu → 0, không NaN", () => {
    expect(gradeExam([], [])).toEqual({ score10: 0, earned: 0, max: 0, correctCount: 0 });
    expect(gradeExam([essay], [""]).score10).toBe(0);
  });
  it("responses ngắn hơn questions → các câu thiếu coi như bỏ trống", () => {
    expect(gradeExam([mc(0), mc(0)], [0]).score10).toBe(5);
  });
  it("làm tròn: 3/7 câu đúng → 4,29", () => {
    const qs = Array.from({ length: 7 }, () => mc(0));
    expect(gradeExam(qs, [0, 0, 0, 1, 1, 1, 1]).score10).toBe(4.29);
  });
});

describe("buildQuestionResults / isAnswered / questionStatus", () => {
  it("khoá dòng exam_question_results (nhãn, is_correct)", () => {
    const qs: ExamQuestion[] = [{ ...mc(0), topic: " Lực ", form: "bai_tap", difficulty: "kho" }, tf([true, false, true, false]), essay];
    const rows = buildQuestionResults(qs, [0, [true, false, true, true], "x"], new Map([["Lực", 7]]));
    expect(rows[0]).toEqual({ question_index: 0, topic_id: 7, topic_name: "Lực", form: "bai_tap", qtype: "multiple_choice", earned: 0.25, max: 0.25, is_correct: true, difficulty: "kho" });
    expect(rows[1]).toMatchObject({ topic_id: null, topic_name: "", earned: 0.5, max: 1, is_correct: false, difficulty: "" });
    expect(rows[2]).toMatchObject({ earned: 0, max: 0, is_correct: false }); // tự luận không bao giờ is_correct
  });
  it("emptyResponses & isAnswered", () => {
    const qs = [mc(0), tf([true, true, true, true]), sa("1"), essay];
    expect(emptyResponses(qs)).toEqual([null, [null, null, null, null], "", ""]);
    expect(isAnswered(qs[0], 0)).toBe(true);
    expect(isAnswered(qs[0], null)).toBe(false);
    expect(isAnswered(qs[1], [null, false, null, null])).toBe(true);
    expect(isAnswered(qs[2], "  ")).toBe(false);
  });
  it("questionStatus", () => {
    expect(questionStatus(essay, "x")).toBe("manual");
    expect(questionStatus(mc(0), null)).toBe("skipped");
    expect(questionStatus(mc(0), 0)).toBe("correct");
    expect(questionStatus(mc(0), 1)).toBe("wrong");
    expect(questionStatus(tf([true, true, true, true]), [true, true, true, false])).toBe("partial");
    expect(questionStatus(tf([true, true, true, true]), [false, false, false, false])).toBe("wrong");
  });
});
