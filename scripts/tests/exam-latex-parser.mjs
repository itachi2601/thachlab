// Kiểm splitQuestions không cắt nhầm câu khi lời giải nhắc "Câu n" giữa đoạn:
//   node scripts/tests/exam-latex-parser.mjs
import assert from "node:assert/strict";
import { parseExamLatex } from "../../services/exam-latex-parser.ts";

// Lời giải của Câu 1 nhắc lại "Câu 4" (đánh số cũ, không phải mốc câu hỏi thật) —
// không có dấu chấm/hai chấm/ngoặc đơn ngay sau số nên không được coi là mốc "Câu n.".
const latex = `
\\subsection*{PHẦN III. Câu trắc nghiệm trả lời ngắn}
\\textbf{Câu 1.} Một khối đồng có khối lượng 2kg ở 20°C. Tính nhiệt lượng cần cung cấp để đồng đạt đến nhiệt độ nóng chảy (đơn vị kJ, làm tròn).
\\textbf{Đáp án:} 5
\\textbf{Lời giải:} Ta có công thức Q = mcΔt.
Câu 4 chỉ hỏi nhiệt lượng cần cung cấp để đồng đạt đến nhiệt độ nóng chảy, không cần tính thêm nhiệt nóng chảy.
Vậy đáp án là 5.

\\textbf{Câu 2.} Một vật khác có khối lượng 1kg. Tính nhiệt lượng toả ra.
\\textbf{Đáp án:} 10
`;

const { questions, warnings } = parseExamLatex(latex);

assert.equal(
  questions.length,
  2,
  `phải parse đúng 2 câu, không tách thêm câu ma từ "Câu 4" trong lời giải (parse được ${questions.length})`,
);
assert.equal(questions[0].answer, "5");
assert.equal(questions[1].answer, "10");
assert.ok(
  !questions.some((q) => q.answer === ""),
  "không được có câu nào với đáp án rỗng (dấu hiệu câu ma bị tách nhầm)",
);
void warnings;

// Mốc câu hợp lệ vẫn nhận đủ các kiểu dấu sau số: ".", ":", ")"
const variants = `
\\subsection*{PHẦN III. Câu trắc nghiệm trả lời ngắn}
Câu 1: Câu đầu tiên.
Đáp án: 1

Câu 2) Câu thứ hai.
Đáp án: 2

Câu 3. Câu thứ ba.
Đáp án: 3
`;
assert.equal(parseExamLatex(variants).questions.length, 3, "phải nhận cả 3 kiểu dấu sau số câu: . : )");

console.log("✓ exam-latex-parser: 5 phép kiểm đều đạt");
