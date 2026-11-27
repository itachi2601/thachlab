// Tạo đề kiểm tra 15 câu trắc nghiệm cho Chương 1 "Những khái niệm cơ bản" — CNCTM 1, lớp CĐ CK 25C.
// Đề gắn vào mục "Kiểm tra" của Bài 1 (lesson 203), chỉ mở cho lớp nội dung 23 (exam_classes).
//   npx tsx scripts/tao-de-cnctm-chuong-1.mts         # xem trước
//   npx tsx scripts/tao-de-cnctm-chuong-1.mts --yes   # ghi DB
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { validateBundle, bundleToRows, type LessonBundle } from "@/services/lesson-import";
import type { MultipleChoiceQuestion } from "@/features/exams/types";

const CLASS_ID = 23; // Công nghệ chế tạo máy 1 (CĐ CK 25C)
const LESSON_ID = 203; // Bài 1. Những khái niệm cơ bản
const TITLE = "Kiểm tra 15 câu — Chương 1. Những khái niệm cơ bản";
const DURATION = 20; // phút
const PASS_SCORE = 7.5;
const yes = process.argv.includes("--yes");

const Q = (
  question: string,
  options: [string, string, string, string],
  answer: number,
  explanation: string,
  difficulty: "de" | "trung-binh" | "kho",
  form: "ly_thuyet" | "bai_tap",
): MultipleChoiceQuestion => ({
  type: "multiple_choice",
  question,
  options,
  answer,
  explanation,
  difficulty,
  form,
  difficultySource: "ai",
});

const questions: MultipleChoiceQuestion[] = [
  Q(
    "Việc nào sau đây thuộc quá trình công nghệ?",
    [
      "Xe nâng chở phôi từ kho ra máy tiện",
      "Tôi bề mặt trục để tăng độ cứng",
      "Mài lại dao tiện bị mòn",
      "Sơn vỏ thùng đựng chi tiết",
    ],
    1,
    "Tôi làm thay đổi tính chất của chính chi tiết đang sản xuất nên thuộc quá trình công nghệ. Chở phôi, sơn thùng là việc phụ; mài dao là sửa dụng cụ, không sửa chi tiết.",
    "trung-binh",
    "ly_thuyet",
  ),
  Q(
    "Quá trình công nghệ là:",
    [
      "Toàn bộ hoạt động có ích trong nhà máy, từ nhập nguyên liệu đến xuất sản phẩm",
      "Phần trực tiếp làm thay đổi đối tượng sản xuất: hình dáng, kích thước, tính chất, vị trí tương quan các mặt",
      "Bản ghi các bước làm việc đã được thống nhất trong xưởng",
      "Công đoạn bảo quản, đóng gói và vận chuyển thành phẩm",
    ],
    1,
    "Quá trình công nghệ chỉ là phần trực tiếp làm thay đổi đối tượng sản xuất; nó nằm trong quá trình sản xuất.",
    "de",
    "ly_thuyet",
  ),
  Q(
    "Quy trình công nghệ là:",
    [
      "Mọi cách làm ra một chi tiết, kể cả cách chưa hợp lý",
      "Quá trình công nghệ hợp lý nhất, đã được ghi thành văn kiện (phiếu công nghệ, bảng tiến trình)",
      "Bản vẽ chi tiết với đầy đủ dung sai và yêu cầu kỹ thuật",
      "Danh sách máy và dao cụ hiện có của phân xưởng",
    ],
    1,
    "Quy trình công nghệ = quá trình công nghệ hợp lý nhất + đã ghi thành văn kiện để cả xưởng làm theo.",
    "de",
    "ly_thuyet",
  ),
  Q(
    "Hai dấu hiệu của một nguyên công là:",
    [
      "Cùng một dao và cùng một chế độ cắt",
      "Một chỗ làm việc và làm liên tục trên cùng đối tượng gia công",
      "Một lần định vị và một lần kẹp chặt",
      "Cùng một bề mặt và một lần hớt lớp vật liệu",
    ],
    1,
    "Nguyên công gắn với một chỗ làm việc (máy, người đứng máy) và được làm liên tục. Đổi máy hoặc bị ngắt quãng là sang nguyên công mới.",
    "de",
    "ly_thuyet",
  ),
  Q(
    "Phát biểu nào đúng về gá và vị trí?",
    [
      "Gá là một lần định vị và kẹp chặt; vị trí là phôi đổi chỗ so với máy hoặc dao mà không bị tháo ra.",
      "Gá là phôi đổi chỗ mà không tháo ra; vị trí là tháo phôi ra rồi kẹp lại.",
      "Gá và vị trí là một, chỉ khác tên gọi.",
      "Chỉ khi tháo phôi ra khỏi đồ gá mới tính là một vị trí mới.",
    ],
    0,
    "Gá = một lần định vị + kẹp chặt (tháo ra kẹp lại là gá mới). Vị trí = phôi đổi chỗ so với máy/dao nhưng không tháo ra.",
    "trung-binh",
    "ly_thuyet",
  ),
  Q(
    "Ba điều không đổi trong một bước gia công là:",
    [
      "Cùng bề mặt gia công, cùng dụng cụ cắt, cùng chế độ cắt",
      "Cùng máy, cùng người đứng máy, cùng ca làm việc",
      "Cùng đồ gá, cùng vị trí, cùng đường chuyển dao",
      "Cùng phôi, cùng bản vẽ, cùng phiếu công nghệ",
    ],
    0,
    "Một bước chỉ kết thúc khi đổi một trong ba thứ: bề mặt gia công, dụng cụ cắt hoặc chế độ cắt.",
    "de",
    "ly_thuyet",
  ),
  Q(
    "Tiện thô một mặt trụ bằng 3 lần hớt, cùng dao và cùng chế độ cắt, rồi tiện tinh đúng mặt đó. Kết luận đúng là:",
    [
      "1 bước, 4 đường chuyển dao",
      "2 bước; bước thô có 3 đường chuyển dao",
      "4 bước, 1 đường chuyển dao",
      "3 bước, 2 đường chuyển dao",
    ],
    1,
    "Thô sang tinh là đổi chế độ cắt nên thành bước mới. Ba lần hớt cùng chế độ nằm trong một bước thô và là 3 đường chuyển dao.",
    "kho",
    "bai_tap",
  ),
  Q(
    "Phay 4 mặt của đầu vuông bằng đầu phân độ: mỗi lần xoay 90°, phôi không tháo ra. Nguyên công phay có:",
    [
      "1 lần gá, 4 vị trí",
      "4 lần gá, 1 vị trí",
      "4 lần gá, 4 vị trí",
      "1 lần gá, 1 vị trí",
    ],
    0,
    "Phôi không tháo ra nên vẫn một lần gá; mỗi lần xoay 90° là một vị trí mới.",
    "trung-binh",
    "bai_tap",
  ),
  Q(
    "Cũng nguyên công phay 4 mặt, nhưng thay đầu phân độ bằng cách tháo phôi ra, xoay 90° rồi kẹp lại sau mỗi mặt. Khi đó nguyên công phay có:",
    [
      "1 lần gá, 4 vị trí",
      "4 lần gá, mỗi lần gá 1 vị trí",
      "4 nguyên công, 1 lần gá",
      "1 lần gá, 4 bước",
    ],
    1,
    "Tháo ra kẹp lại là một lần định vị + kẹp chặt mới nên mỗi mặt là một lần gá (một vị trí). Máy không đổi, làm liên tục nên vẫn là 1 nguyên công.",
    "kho",
    "bai_tap",
  ),
  Q(
    "Trên cùng một máy tiện, thợ tiện đầu C cho cả loạt 100 chi tiết, sau đó mới trở đầu tiện đầu A cho cả loạt. Số nguyên công là:",
    ["1", "2", "3", "4"],
    1,
    "Công việc bị ngắt quãng giữa hai đầu nên không còn liên tục: mỗi lần vào làm là một nguyên công, dù vẫn cùng máy.",
    "kho",
    "bai_tap",
  ),
  Q(
    "Bước ghép là:",
    [
      "Nhiều dao cùng cắt đồng thời nhiều bề mặt, mỗi dao có chế độ cắt riêng",
      "Nhiều nguyên công được ghi chung vào một phiếu công nghệ",
      "Một dao cắt nhiều lần trên cùng một bề mặt",
      "Ghép nhiều chi tiết lại để gia công trong cùng một lần gá",
    ],
    0,
    "Bước ghép dùng nhiều dao cắt đồng thời để tăng năng suất, ví dụ vừa khoan lỗ vừa tiện ngoài trên máy tiện.",
    "trung-binh",
    "ly_thuyet",
  ),
  Q(
    "Trong khi tiện, thợ bấm nút khởi động trục chính rồi quay tay quay cho dao tiến vào. Hai thao tác đó là:",
    ["Hai bước", "Hai đường chuyển dao", "Hai động tác", "Hai nguyên công"],
    2,
    "Động tác là một hành động của người thợ (bấm nút, quay tay quay…); nó nằm trong mọi thành phần, không phải bước hay nguyên công.",
    "de",
    "ly_thuyet",
  ),
  Q(
    "Một nhà máy lắp ráp 2.000 máy bơm mỗi năm, mỗi máy có 2 trục bơm. Tỉ lệ phế phẩm 4%, chế tạo dự trữ 6%. Sản lượng trục bơm hằng năm $N$ là:",
    ["2.000 chiếc", "4.000 chiếc", "4.400 chiếc", "4.800 chiếc"],
    2,
    "$N = 2000 \\cdot 2 \\cdot (1 + \\dfrac{4+6}{100}) = 4400$ chiếc/năm.",
    "trung-binh",
    "bai_tap",
  ),
  Q(
    "Một trục bơm nặng 2,5 kg, sản lượng $N = 4.400$ chiếc/năm. Dạng sản xuất của trục bơm là:",
    ["Đơn chiếc", "Hàng loạt nhỏ", "Hàng loạt vừa", "Hàng khối"],
    2,
    "2,5 kg < 4 kg nên tra cột đầu; 4.400 nằm trong khoảng 500 – 5.000 → hàng loạt vừa.",
    "trung-binh",
    "bai_tap",
  ),
  Q(
    "Thân máy bơm nặng 60 kg, mỗi máy dùng 1 thân, nhà máy lắp 2.000 máy/năm, phế phẩm 4%, dự trữ 6%. Dạng sản xuất của thân máy là:",
    ["Hàng loạt nhỏ", "Hàng loạt vừa", "Hàng loạt lớn", "Hàng khối"],
    2,
    "$N = 2200$ chiếc/năm. Khối lượng 60 kg thuộc cột 4 – 200 kg, khoảng 500 – 5.000 là hàng loạt lớn. Cùng sản lượng nhưng chi tiết nặng hơn thì lên hạng sản xuất.",
    "kho",
    "bai_tap",
  ),
];

// ---- Soát máy: 4 phương án, đáp án 0–3, không trùng phương án, đủ lời giải ----
if (questions.length !== 15) throw new Error(`Phải đúng 15 câu, đang có ${questions.length}.`);
questions.forEach((q, i) => {
  if (q.options.length !== 4) throw new Error(`Câu ${i + 1}: phải có 4 phương án.`);
  if (q.answer < 0 || q.answer > 3) throw new Error(`Câu ${i + 1}: đáp án ngoài 0–3.`);
  if (new Set(q.options.map((o) => o.trim())).size !== 4) throw new Error(`Câu ${i + 1}: phương án trùng nhau.`);
  if (!q.explanation.trim()) throw new Error(`Câu ${i + 1}: thiếu lời giải.`);
});

const bundle: LessonBundle = {
  schema: "thachlab.lesson-bundle/v1",
  theory_html: "",
  worked_examples: [],
  exam: {
    title: TITLE,
    duration_minutes: DURATION,
    subject_code: "cnctm",
    difficulty: "",
    questions,
  },
};
const check = validateBundle(bundle);
if (!check.ok) throw new Error(`Gói đề lỗi: ${check.errors.join("; ")}`);
for (const w of check.warnings) console.log("⚠", w);

const env = Object.fromEntries(
  fs
    .readFileSync(".env.local", "utf8")
    .split("\n")
    .filter((l) => l.includes("="))
    .map((l) => [l.slice(0, l.indexOf("=")), l.slice(l.indexOf("=") + 1).trim()]),
);
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const rows = bundleToRows(bundle, LESSON_ID);

console.log(`Đề: ${rows.exam.title}`);
console.log(`  ${questions.length} câu trắc nghiệm · ${DURATION} phút · đạt ${PASS_SCORE}/10 · môn ${rows.exam.subject_code}`);
console.log(`  Gắn mục "Kiểm tra" của bài ${LESSON_ID}, mở cho lớp ${CLASS_ID}.`);
if (!yes) {
  console.log("DRY-RUN: thêm --yes để ghi DB.");
  process.exit(0);
}

// Không tạo trùng nếu chạy lại.
const { data: dup } = await sb.from("exams").select("id").eq("title", TITLE);
if (dup?.length) throw new Error(`Đã có đề cùng tên (#${dup[0].id}) — không tạo lại.`);

const { data: ex, error: e1 } = await sb
  .from("exams")
  .insert({ ...rows.exam, published: true, pass_score: PASS_SCORE })
  .select("id")
  .single();
if (e1 || !ex) throw new Error(`Tạo đề lỗi: ${e1?.message}`);
const examId = ex.id as number;
console.log(`  ✓ đề #${examId}`);

const { error: e2 } = await sb.from("exam_classes").insert({ exam_id: examId, class_id: CLASS_ID });
if (e2) throw new Error(`Gán lớp lỗi: ${e2.message}`);
console.log(`  ✓ gán lớp ${CLASS_ID}`);

const { data: item, error: e3 } = await sb
  .from("lesson_items")
  .insert({
    lesson_id: LESSON_ID,
    kind: "kiem_tra",
    title: "Kiểm tra chương 1",
    subtitle: `${questions.length} câu — ${DURATION} phút`,
    body_html: "",
    video_url: "",
    pdf_url: "",
    questions: [],
    exam_ids: [examId],
    sort_order: 6,
    published_at: new Date().toISOString(),
  })
  .select("id")
  .single();
if (e3 || !item) throw new Error(`Tạo mục Kiểm tra lỗi: ${e3?.message}`);
console.log(`  ✓ mục Kiểm tra #${item.id} trong bài ${LESSON_ID}`);

console.log(`\nMã đề: ${examId}`);
console.log(`Link:  https://thachlab.id.vn/kiem-tra/lam/?id=${examId}`);
console.log(`Vào học: https://thachlab.id.vn/lop-hoc/bai/?id=${LESSON_ID}`);
