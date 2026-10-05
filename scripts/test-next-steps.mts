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
console.log("next-steps: OK");
