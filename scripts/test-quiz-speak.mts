import assert from "node:assert/strict";
import { quizSpeakText, stripOptionLabel } from "../lib/quiz-speak";

// Nhãn a. / b) như đề thật
assert.equal(stripOptionLabel("a. lathe"), "lathe");
assert.equal(stripOptionLabel("  b)  milling machine "), "milling machine");
assert.equal(stripOptionLabel("lathe"), "lathe");

// Phương án tiếng Anh: đọc đúng phương án vừa bấm (kể cả cụm nhiều chữ, danh từ ghép)
assert.equal(quizSpeakText("a. lathe"), "lathe");
assert.equal(quizSpeakText("b. milling machine"), "milling machine");
assert.equal(quizSpeakText("c. band saw"), "band saw");
assert.equal(quizSpeakText("d. headstock"), "headstock");

// Câu hỏi có phương án tiếng Việt ("workpieces nghĩa là gì?"): đọc từ đang hỏi, không đọc "phôi"
assert.equal(quizSpeakText("a. phoi", "workpieces"), "workpieces");
assert.equal(quizSpeakText("b. phôi", "workpieces"), "workpieces");
assert.equal(quizSpeakText("a. sự phát (điện)", "generate"), "generate");

// Phương án tiếng Việt mà không khai từ đang hỏi: im lặng (tránh giọng Anh đọc tiếng Việt)
assert.equal(quizSpeakText("a. phôi"), "");
assert.equal(quizSpeakText("a. sự phát (điện)"), "");
assert.equal(quizSpeakText("a. bất ngờ"), "");

// True/False và chú thích trong ngoặc: không đọc
assert.equal(quizSpeakText("True (Đúng)"), "");
assert.equal(quizSpeakText("False (Sai)"), "");
assert.equal(quizSpeakText("a. True (Đúng)"), "");

// Chuỗi rỗng, quá dài, không có chữ
assert.equal(quizSpeakText(""), "");
assert.equal(quizSpeakText("a.   "), "");
assert.equal(quizSpeakText("a. " + "word ".repeat(30)), "");

console.log("quiz-speak: OK");
