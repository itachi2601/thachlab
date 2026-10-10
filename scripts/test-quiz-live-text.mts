// Kiểm toán thuần của features/quiz-live/text.ts — chạy: npx tsx scripts/test-quiz-live-text.mts
import assert from "node:assert/strict";
import { bankToQuizQuestion, parseQuizText, quizQuestionIssue, textToHtml } from "../features/quiz-live/text";

const r = parseQuizText(`Câu 1. Đơn vị của lực là gì?
A. Jun
B. Niutơn *
C. Oát
D. Pascal
Giải thích: F = ma nên đơn vị là kg·m/s².

Câu 2: Vận tốc $v$ thoả $v<c$ khi nào?
a) luôn luôn
b) không bao giờ
c) khi v nhỏ
Đáp án: C`);
assert.equal(r.questions.length, 2);
assert.equal(r.questions[0].answer, 1);
assert.equal(r.questions[0].options[1], "Niutơn");
assert.match(r.questions[0].explanation, /kg·m/);
assert.equal(r.questions[1].answer, 2);
assert.equal(r.questions[1].options.length, 3);
assert.ok(r.questions[1].question.includes("$v\\lt c$"));
assert.equal(r.warnings.length, 0);

const noAns = parseQuizText("Câu 1. Hỏi?\nA. x\nB. y");
assert.equal(noAns.questions[0].answer, -1);
assert.equal(noAns.warnings.length, 1);
assert.equal(quizQuestionIssue(noAns.questions[0]), "chưa chọn đáp án đúng");

// không có "Câu N" → tách theo dòng trống; đáp án nhiều dòng
const blank = parseQuizText("Hai điện tích cùng dấu thì?\nA. hút\nnhau\nB. đẩy *\n\nNước sôi ở?\nA. 100\nB. 50\nĐáp án: A");
assert.equal(blank.questions.length, 2);
assert.equal(blank.questions[0].options[0], "hút nhau");
assert.equal(blank.questions[0].answer, 1);
assert.equal(blank.questions[1].answer, 0);

assert.equal(textToHtml("a<b & c>d"), "a&lt;b &amp; c&gt;d");
assert.equal(bankToQuizQuestion(1, { type: "essay" }), null);
assert.equal(bankToQuizQuestion(7, { type: "multiple_choice", question: "q", options: ["a", "b", "c", "d"], answer: 2, explanation: "" })?.bank_id, 7);
console.log("quiz-live text: OK");
