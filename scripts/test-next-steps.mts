import assert from "node:assert/strict";
import { rankNextSteps } from "../features/learning/next-steps";

const need = { id: 7, label: "Lực ma sát" };
const lesson = { id: 3, chapterId: 2, title: "Bài 3", chapterTitle: "Chương 2" };
const retry = { examId: 9, examTitle: "Đề 15 phút", score: 4.5 };
const kinds = (s: ReturnType<typeof rankNextSteps>) => s.map((x) => x.kind);

assert.deepEqual(kinds(rankNextSteps({ need, needAvailableAt: null, retryExam: retry, nextLesson: lesson })), ["unlock", "retry", "lesson"]);
// đang chờ giãn cách → đẩy xuống cuối, có lockedUntil
const wait = new Date(Date.now() + 3600_000);
const cooling = rankNextSteps({ need, needAvailableAt: wait, retryExam: retry, nextLesson: lesson });
assert.deepEqual(kinds(cooling), ["retry", "lesson", "unlock"]);
assert.equal(cooling[2].lockedUntil, wait);
// điểm đã đạt → không gợi ý làm lại
assert.deepEqual(kinds(rankNextSteps({ need: null, needAvailableAt: null, retryExam: { ...retry, score: 8 }, nextLesson: lesson })), ["lesson"]);
// hết việc → ôn lại
assert.deepEqual(kinds(rankNextSteps({ need: null, needAvailableAt: null, retryExam: null, nextLesson: null })), ["review"]);
// kỹ năng yếu: thay chủ đề phụ đạo khi không có; không chen khi đã có phụ đạo; vẫn giữ chỗ cho bài kế
const weak = { topicId: 5, topicName: "Định luật II", lessonId: 4, chapterId: 2, pct: 40 };
assert.deepEqual(kinds(rankNextSteps({ need: null, needAvailableAt: null, retryExam: retry, nextLesson: lesson, weak })), ["weak", "retry", "lesson"]);
assert.deepEqual(kinds(rankNextSteps({ need, needAvailableAt: null, retryExam: null, nextLesson: lesson, weak })), ["unlock", "lesson"]);
// hết việc có bài đã học → ôn lại đúng bài, trỏ vào bài
const review = rankNextSteps({ need: null, needAvailableAt: null, retryExam: null, nextLesson: null, reviewLesson: { id: 2, chapterId: 1, title: "Bài 2" } });
assert.equal(review[0].href, "/lop-hoc/bai?id=2&chapter=1");
console.log("next-steps: OK");
