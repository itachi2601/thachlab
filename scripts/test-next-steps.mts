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
// kỹ năng yếu: đứng đầu khi có; tối đa 2; vẫn giữ chỗ cho bài kế
const w = (id: number, name: string) => ({ topicId: id, topicName: name, lessonId: 4, lessonTitle: "Bài 4", chapterId: 2, pct: 40 });
assert.deepEqual(kinds(rankNextSteps({ need: null, needAvailableAt: null, retryExam: retry, nextLesson: lesson, weak: [w(5, "A"), w(6, "B"), w(7, "C")] })), ["weak", "weak", "retry", "lesson"]);
// phụ đạo vẫn đứng trước kỹ năng yếu
assert.deepEqual(kinds(rankNextSteps({ need, needAvailableAt: null, retryExam: null, nextLesson: lesson, weak: [w(5, "A")] })), ["unlock", "weak", "lesson"]);
// không có chỗ hổng: bài kế đứng đầu và có lời động viên; có chỗ hổng thì không động viên
const calm = rankNextSteps({ need: null, needAvailableAt: null, retryExam: null, nextLesson: lesson });
assert.ok(calm[0].hint.includes("tăng tốc"));
assert.ok(!rankNextSteps({ need: null, needAvailableAt: null, retryExam: null, nextLesson: lesson, weak: [w(5, "A")] })[1].hint.includes("tăng tốc"));
// bài đang dở hiện tiến độ mục
assert.ok(rankNextSteps({ need: null, needAvailableAt: null, retryExam: null, nextLesson: { ...lesson, completed: 3, total: 8 } })[0].hint.startsWith("Đang dở: 3/8 mục"));
// hết việc có bài đã học → ôn lại đúng bài, trỏ vào bài
const review = rankNextSteps({ need: null, needAvailableAt: null, retryExam: null, nextLesson: null, reviewLesson: { id: 2, chapterId: 1, title: "Bài 2" } });
assert.equal(review[0].href, "/lop-hoc/bai?id=2&chapter=1");
console.log("next-steps: OK");
