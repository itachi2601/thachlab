// Kiểm splitQuestions không cắt nhầm câu khi lời giải nhắc "Câu n" giữa đoạn,
// và câu dẫn bắt đầu bằng "Đáp án"/"Đáp số" không bị cắt nhầm thành dòng khai báo
// đáp án: node scripts/tests/exam-latex-parser.mjs
import assert from "node:assert/strict";
import { parseExamLatex } from "../../services/exam-latex-parser.ts";

const mcPart = "\\subsection*{PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn}";
const saPart = "\\subsection*{PHẦN III. Câu trắc nghiệm trả lời ngắn}";

// Lời giải của Câu 1 nhắc lại "Câu 4" (đánh số cũ, không phải mốc câu hỏi thật) —
// không có dấu chấm/hai chấm/ngoặc đơn ngay sau số nên không được coi là mốc "Câu n.".
{
  const latex = `${saPart}
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
}

// Mốc câu hợp lệ vẫn nhận đủ các kiểu dấu sau số: ".", ":", ")"
{
  const variants = `${saPart}
Câu 1: Câu đầu tiên.
Đáp án: 1

Câu 2) Câu thứ hai.
Đáp án: 2

Câu 3. Câu thứ ba.
Đáp án: 3
`;
  assert.equal(parseExamLatex(variants).questions.length, 3, "phải nhận cả 3 kiểu dấu sau số câu: . : )");
}

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

console.log("✓ exam-latex-parser: tất cả phép kiểm đều đạt");
