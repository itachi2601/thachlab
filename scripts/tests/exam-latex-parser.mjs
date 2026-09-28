// Kiểm câu dẫn bắt đầu bằng "Đáp án"/"Đáp số" không bị cắt nhầm thành dòng khai
// báo đáp án: node scripts/tests/exam-latex-parser.mjs
import assert from "node:assert/strict";
import { parseExamLatex } from "../../services/exam-latex-parser.ts";

const mcPart = "\\subsection*{PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn}";
const saPart = "\\subsection*{PHẦN III. Câu trắc nghiệm trả lời ngắn}";

// Câu dẫn tự nhiên bắt đầu bằng "Đáp án nào sau đây…" (không có dấu hai chấm) —
// không được coi là dòng khai báo đáp án, phần dẫn và 4 phương án phải còn nguyên.
{
  const latex = `${mcPart}
\\textbf{Câu 1.} Đáp án nào sau đây gồm có một đơn vị cơ bản và một đơn vị dẫn xuất?
A. mét, giây   B. mét, mét trên giây   C. giây, kilôgam   D. kilôgam, mol
\\textbf{Đáp án:} B
\\textbf{Lời giải:} Vì mét là đơn vị cơ bản, mét trên giây là đơn vị dẫn xuất.
`;
  const r = parseExamLatex(latex, { lenient: true });
  assert.deepEqual(r.warnings, []);
  assert.equal(r.questions.length, 1);
  const q = r.questions[0];
  assert.equal(q.question, "Đáp án nào sau đây gồm có một đơn vị cơ bản và một đơn vị dẫn xuất?");
  assert.deepEqual(q.options, ["mét, giây", "mét, mét trên giây", "giây, kilôgam", "kilôgam, mol"]);
  assert.equal(q.answer, 1); // B — không bị lệch sang đáp án bịa từ chữ cái lạc trong câu dẫn
}

// Câu dẫn bắt đầu bằng "Đáp số là…" ở phần trả lời ngắn — vẫn phải giữ nguyên câu dẫn.
{
  const latex = `${saPart}
\\textbf{Câu 1.} Đáp số là quãng đường vật đi được sau 2 giây, tính bằng mét.
\\textbf{Đáp án:} 8
`;
  const r = parseExamLatex(latex, { lenient: true });
  assert.deepEqual(r.warnings, []);
  assert.equal(r.questions.length, 1);
  const q = r.questions[0];
  assert.equal(q.question, "Đáp số là quãng đường vật đi được sau 2 giây, tính bằng mét.");
  assert.equal(q.answer, "8");
}

// Dòng khai báo thật vẫn nhận đúng như trước, kể cả biến thể "Đáp án đúng:".
{
  const latex = `${mcPart}
\\textbf{Câu 1.} Vận tốc là đại lượng gì?
A. Vô hướng   B. Hữu hướng   C. Véc-tơ   D. Không xác định
\\textbf{Đáp án đúng:} C
`;
  const r = parseExamLatex(latex, { lenient: true });
  assert.equal(r.questions.length, 1);
  assert.equal(r.questions[0].answer, 2); // C
}

// Không dấu hai chấm và không phải dòng khai báo → không lấy được đáp án, phải cảnh báo
// thay vì âm thầm gán bừa một chữ cái lạc trong câu dẫn.
{
  const latex = `${mcPart}
\\textbf{Câu 1.} Đáp án nào sau đây là đúng về gia tốc?
A. Vô hướng   B. Hữu hướng   C. Véc-tơ   D. Không xác định
\\textbf{Lời giải:} Gia tốc là đại lượng véc-tơ.
`;
  const r = parseExamLatex(latex, { lenient: true });
  assert.equal(r.questions.length, 1);
  assert.equal(r.questions[0].question, "Đáp án nào sau đây là đúng về gia tốc?");
  assert.equal(r.questions[0].answer, -1);
  assert.ok(r.warnings.some((w) => /thiếu đáp án đúng/.test(w)));
}

// Quy ước xuat_thachlab.py: dòng đầu lời giải là "Chọn đáp án D" (không dấu hai chấm) — vẫn
// phải nhận được đáp án, và không được nuốt câu dẫn nếu câu dẫn bắt đầu bằng "Đáp án".
{
  const latex = `${mcPart}
\\textbf{Câu 1.} Đáp án nào sau đây là đơn vị của công?
A. N   B. J   C. W   D. Pa
Chọn đáp án B
Công có đơn vị jun.
`;
  const r = parseExamLatex(latex, { lenient: true });
  assert.equal(r.questions.length, 1);
  assert.equal(r.questions[0].question, "Đáp án nào sau đây là đơn vị của công?");
  assert.equal(r.questions[0].answer, 1); // B
}

console.log("✓ exam-latex-parser: 5 phép kiểm đều đạt");
