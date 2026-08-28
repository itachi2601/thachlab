// Tạo bài học mẫu đầy đủ 5 mục (Lý thuyết, Video, Các dạng bài tập, Luyện tập, Kiểm tra)
// cho "Bài 1. Làm quen với Vật lí" — Chương 1: Mở đầu, Vật lí lớp 10.
//
// Bài học và chương này đã có sẵn trong CSDL (lesson_id=46, chapter_id=10, class "10" id=16);
// script chỉ thêm 2 đề (exams) và 5 lesson_items cho bài học, không đổi gì khác.
//
// App này export tĩnh (next.config output: "export"), không có server Node.js ở production,
// nên insert cần service role key và CHỈ chạy cục bộ trên máy bạn:
//
//   node scripts/seed-lesson-vatly10-bai1.mjs
//
// Script tự đọc NEXT_PUBLIC_SUPABASE_URL từ .env.local, rồi hỏi bạn dán SUPABASE_SERVICE_ROLE_KEY
// (gõ vào sẽ ẩn, không lưu vào lịch sử terminal). Lấy key này ở Supabase Dashboard → Settings → API
// → service_role (secret, KHÔNG commit, KHÔNG dán vào chat). Script bỏ qua nếu bài đã có mục (idempotent).

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));

function readEnvLocal(key) {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs
    .readFileSync(envPath, "utf8")
    .split("\n")
    .find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

function askHidden(query) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl._writeToOutput = (chunk) => {
      rl.output.write(rl.stdoutMuted ? "*" : chunk);
    };
    rl.stdoutMuted = false;
    rl.question(query, (answer) => {
      rl.close();
      process.stdout.write("\n");
      resolve(answer.trim());
    });
    rl.stdoutMuted = true;
  });
}

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
if (!SUPABASE_URL) {
  console.error("Không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local.");
  process.exit(1);
}
const SERVICE_ROLE_KEY =
  process.env.SUPABASE_SERVICE_ROLE_KEY ??
  (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role), rồi Enter: "));
if (!SERVICE_ROLE_KEY) {
  console.error("Thiếu SUPABASE_SERVICE_ROLE_KEY.");
  process.exit(1);
}

const LESSON_ID = 46; // Bài 1. Làm quen với Vật lí (chapter_id=10, lớp 10)
const CLASS_ID = 16; // lớp "10"

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
  auth: { autoRefreshToken: false, persistSession: false },
});

const lyThuyetHtml = `
<h4>1. Đối tượng và mục tiêu nghiên cứu của Vật lí</h4>
<p>Vật lí nghiên cứu các dạng <strong>vận động của vật chất</strong> (cơ, nhiệt, điện, quang, âm, hạt nhân…) và
<strong>năng lượng</strong>, ở mọi cấp độ từ vi mô (hạt, nguyên tử) đến vĩ mô (Trái Đất, vũ trụ). Mục tiêu của Vật lí
là khám phá ra những <strong>quy luật tổng quát nhất</strong> chi phối sự vận động của vật chất, năng lượng và
tương tác giữa chúng.</p>

<h4>2. Quá trình phát triển của Vật lí</h4>
<ul>
  <li><strong>Tiền Vật lí</strong> (trước thế kỉ XVII): quan sát tự nhiên và suy luận chủ quan, chưa có thực nghiệm định lượng.</li>
  <li><strong>Vật lí cổ điển</strong> (thế kỉ XVII – cuối thế kỉ XIX): hình thành cơ học Newton, nhiệt động lực học,
  điện từ học cổ điển (Newton, Faraday, Maxwell…).</li>
  <li><strong>Vật lí hiện đại</strong> (từ cuối thế kỉ XIX): ra đời thuyết tương đối (Einstein) và cơ học lượng tử
  (Planck, Bohr…), mở ra cách hiểu mới về không gian, thời gian và thế giới vi mô.</li>
</ul>

<h4>3. Vai trò của Vật lí đối với khoa học, kĩ thuật và công nghệ</h4>
<p>Vật lí là nền tảng của nhiều ngành khoa học tự nhiên và kĩ thuật. Nhiều thành tựu công nghệ hiện đại là ứng dụng
trực tiếp của Vật lí: hệ thống định vị GPS (thuyết tương đối), thiết bị bán dẫn, laser, pin mặt trời, vệ tinh viễn
thông, năng lượng hạt nhân… Nhờ đó Vật lí ảnh hưởng sâu rộng đến đời sống, sản xuất và sự phát triển của xã hội.</p>

<h4>4. Phương pháp nghiên cứu Vật lí</h4>
<p>Có hai phương pháp nghiên cứu chính, hỗ trợ và bổ sung cho nhau:</p>
<ul>
  <li><strong>Phương pháp thực nghiệm:</strong> dùng thí nghiệm để phát hiện kết quả mới, từ đó kiểm chứng, xác nhận
  hoặc bác bỏ một giả thuyết; kết quả mới có thể gợi ý một mô hình lí thuyết mới.</li>
  <li><strong>Phương pháp lí thuyết:</strong> dùng ngôn ngữ toán học và suy luận logic để dự đoán kết quả mới; kết quả
  này cần được thực nghiệm kiểm chứng lại.</li>
</ul>
<p>Vì vậy, một kết quả nghiên cứu Vật lí chỉ được chấp nhận khi đã được <strong>kiểm chứng bằng thực nghiệm</strong>.</p>
`.trim();

const workedQuestions = [
  {
    label: "Dạng 1",
    body_html: `
<p><strong>Đề bài:</strong> Cho các hiện tượng/ứng dụng sau: (1) đun nước sôi; (2) nam châm hút đinh sắt; (3) cầu vồng
sau mưa; (4) sóng thần. Mỗi hiện tượng trên thuộc lĩnh vực nào của Vật lí?</p>
<p><strong>Lời giải:</strong></p>
<ul>
  <li>(1) Đun nước sôi — liên quan sự truyền nhiệt và chuyển thể → <em>Nhiệt học</em>.</li>
  <li>(2) Nam châm hút đinh sắt — lực tương tác từ → <em>Điện từ học</em>.</li>
  <li>(3) Cầu vồng — ánh sáng bị khúc xạ, tán sắc qua giọt nước → <em>Quang học</em>.</li>
  <li>(4) Sóng thần — sự lan truyền dao động trong nước → <em>Cơ học (sóng)</em>.</li>
</ul>`,
  },
  {
    label: "Dạng 2",
    body_html: `
<p><strong>Đề bài:</strong> Một nhà khoa học đo tốc độ rơi của các vật có khối lượng khác nhau từ cùng một độ cao,
sau đó dùng công thức toán học để dự đoán quãng đường rơi tại các thời điểm chưa đo. Hãy chỉ ra đâu là bước dùng
phương pháp thực nghiệm, đâu là bước dùng phương pháp lí thuyết.</p>
<p><strong>Lời giải:</strong></p>
<ul>
  <li>Bước <em>đo tốc độ rơi bằng thí nghiệm</em> → phương pháp thực nghiệm (thu thập số liệu thực tế).</li>
  <li>Bước <em>dùng công thức toán học để dự đoán</em> quãng đường ở các thời điểm khác → phương pháp lí thuyết
  (suy luận, ngoại suy bằng toán học); kết quả dự đoán này cần được đo lại bằng thí nghiệm để kiểm chứng.</li>
</ul>`,
  },
  {
    label: "Dạng 3",
    body_html: `
<p><strong>Đề bài:</strong> Vì sao nói hệ thống định vị toàn cầu (GPS) là một minh chứng cho vai trò của Vật lí đối
với công nghệ?</p>
<p><strong>Lời giải:</strong> Vệ tinh GPS chuyển động rất nhanh và ở xa Trái Đất nên đồng hồ trên vệ tinh chạy lệch
so với đồng hồ mặt đất theo hiệu ứng được thuyết tương đối (hẹp và rộng) tiên đoán. Nếu không hiệu chỉnh sai lệch
này bằng các công thức của thuyết tương đối, vị trí GPS tính được sẽ sai lệch hàng kilômét mỗi ngày. Đây là ví dụ
cho thấy một lí thuyết Vật lí hiện đại được ứng dụng trực tiếp để tạo ra công nghệ dùng trong đời sống hằng ngày.</p>`,
  },
];

const luyenTapExam = {
  title: "Luyện tập – Bài 1. Làm quen với Vật lí",
  duration_minutes: 20,
  published: true,
  subject_code: "vat-ly",
  topic: "Làm quen với Vật lí",
  difficulty: "de",
  questions: [
    {
      type: "multiple_choice",
      question: "Đối tượng nghiên cứu của Vật lí là gì?",
      options: [
        "Chỉ các hiện tượng hoá học của vật chất",
        "Các dạng vận động của vật chất và năng lượng, cùng tương tác giữa chúng",
        "Chỉ sự sống của sinh vật",
        "Các quy luật của đời sống xã hội",
      ],
      answer: 1,
      explanation: "Vật lí nghiên cứu các dạng vận động của vật chất và năng lượng ở mọi cấp độ, vi mô đến vĩ mô.",
    },
    {
      type: "multiple_choice",
      question: "Mục tiêu của Vật lí là gì?",
      options: [
        "Khám phá quy luật tổng quát nhất chi phối sự vận động của vật chất và năng lượng",
        "Chỉ mô tả lại các hiện tượng đã biết",
        "Chỉ phục vụ mục đích công nghiệp",
        "Thay thế hoàn toàn các ngành khoa học khác",
      ],
      answer: 0,
      explanation: "Vật lí hướng tới các quy luật tổng quát nhất, làm nền tảng cho nhiều ngành khoa học khác.",
    },
    {
      type: "multiple_choice",
      question: "Giai đoạn Vật lí cổ điển gắn liền với đóng góp nổi bật của nhà khoa học nào sau đây?",
      options: ["Newton", "Einstein", "Bohr", "Planck"],
      answer: 0,
      explanation: "Cơ học Newton (thế kỉ XVII) là nền tảng của Vật lí cổ điển; Einstein, Bohr, Planck thuộc Vật lí hiện đại.",
    },
    {
      type: "multiple_choice",
      question: "Vật lí hiện đại ra đời gắn liền với sự xuất hiện của lí thuyết nào sau đây?",
      options: [
        "Định luật vạn vật hấp dẫn",
        "Thuyết tương đối và cơ học lượng tử",
        "Định luật bảo toàn khối lượng",
        "Thuyết nhật tâm",
      ],
      answer: 1,
      explanation: "Thuyết tương đối (Einstein) và cơ học lượng tử (Planck, Bohr…) mở đầu giai đoạn Vật lí hiện đại.",
    },
    {
      type: "multiple_choice",
      question: "Hai phương pháp nghiên cứu chính của Vật lí là gì?",
      options: [
        "Thực nghiệm và lí thuyết",
        "Quan sát và thống kê xã hội",
        "Thực nghiệm và khảo sát lịch sử",
        "Lí thuyết và mô tả văn học",
      ],
      answer: 0,
      explanation: "Phương pháp thực nghiệm và phương pháp lí thuyết hỗ trợ, bổ sung lẫn nhau.",
    },
    {
      type: "multiple_choice",
      question: "Hệ thống định vị toàn cầu (GPS) cần hiệu chỉnh chính xác nhờ ứng dụng thành tựu của lí thuyết Vật lí nào?",
      options: ["Quang học hình học", "Thuyết tương đối", "Nhiệt động lực học", "Cơ học chất lưu"],
      answer: 1,
      explanation: "Đồng hồ trên vệ tinh GPS lệch so với mặt đất theo hiệu ứng thuyết tương đối, cần hiệu chỉnh để định vị chính xác.",
    },
    {
      type: "true_false",
      question: "Xét các phát biểu sau về đối tượng và mục tiêu nghiên cứu của Vật lí:",
      statements: [
        { text: "Vật lí nghiên cứu các dạng vận động của vật chất và năng lượng.", answer: true },
        { text: "Vật lí chỉ nghiên cứu các hiện tượng ở cấp độ vĩ mô, nhìn thấy được bằng mắt thường.", answer: false },
        { text: "Mục tiêu của Vật lí là khám phá quy luật tổng quát chi phối sự vận động của vật chất và năng lượng.", answer: true },
        { text: "Vật lí không liên quan gì đến sự phát triển của công nghệ hiện đại.", answer: false },
      ],
      explanation: "Vật lí nghiên cứu cả vi mô lẫn vĩ mô và là nền tảng của nhiều công nghệ hiện đại.",
    },
    {
      type: "true_false",
      question: "Xét các phát biểu sau về phương pháp nghiên cứu Vật lí:",
      statements: [
        { text: "Phương pháp thực nghiệm dùng thí nghiệm để kiểm chứng hoặc gợi ý giả thuyết mới.", answer: true },
        { text: "Phương pháp lí thuyết dùng ngôn ngữ toán học và suy luận để dự đoán kết quả mới.", answer: true },
        { text: "Kết quả của phương pháp lí thuyết luôn đúng nên không cần thực nghiệm kiểm chứng.", answer: false },
        { text: "Hai phương pháp thực nghiệm và lí thuyết hỗ trợ, bổ sung cho nhau.", answer: true },
      ],
      explanation: "Một lí thuyết chỉ được chấp nhận khi được thực nghiệm kiểm chứng; hai phương pháp luôn bổ sung nhau.",
    },
    {
      type: "short_answer",
      question: "Vật lí hiện đại được xem là bắt đầu từ khoảng cuối thế kỉ mấy? (ghi số, vd 19)",
      answer: "19",
      explanation: "Vật lí hiện đại hình thành từ cuối thế kỉ XIX, đầu thế kỉ XX.",
    },
    {
      type: "short_answer",
      question: "Có bao nhiêu phương pháp nghiên cứu chính trong Vật lí? (ghi số)",
      answer: "2",
      explanation: "Hai phương pháp: thực nghiệm và lí thuyết.",
    },
  ],
};

const kiemTraExam = {
  title: "Kiểm tra – Bài 1. Làm quen với Vật lí",
  duration_minutes: 25,
  published: true,
  subject_code: "vat-ly",
  topic: "Làm quen với Vật lí",
  difficulty: "trung-binh",
  questions: [
    {
      type: "multiple_choice",
      question: "Lĩnh vực nào sau đây KHÔNG thuộc các lĩnh vực chính của Vật lí?",
      options: ["Cơ học", "Điện từ học", "Hoá hữu cơ", "Quang học"],
      answer: 2,
      explanation: "Hoá hữu cơ thuộc Hoá học, không phải một lĩnh vực của Vật lí.",
    },
    {
      type: "multiple_choice",
      question: "Ứng dụng laser trong y học và công nghiệp là minh chứng cho vai trò của Vật lí đối với",
      options: ["Văn học", "Khoa học, kĩ thuật và công nghệ", "Lịch sử", "Địa lí"],
      answer: 1,
      explanation: "Laser là thành tựu của Vật lí quang học, ứng dụng rộng rãi trong khoa học kĩ thuật và công nghệ.",
    },
    {
      type: "multiple_choice",
      question: "Trong nghiên cứu Vật lí, thí nghiệm chủ yếu được dùng để",
      options: [
        "Thay thế hoàn toàn suy luận lí thuyết",
        "Kiểm chứng, phát hiện kết quả mới, xác nhận hoặc bác bỏ giả thuyết",
        "Chỉ minh hoạ cho bài giảng thêm sinh động",
        "Không có vai trò đáng kể trong nghiên cứu",
      ],
      answer: 1,
      explanation: "Thí nghiệm là công cụ cốt lõi của phương pháp thực nghiệm: kiểm chứng và phát hiện kết quả mới.",
    },
    {
      type: "multiple_choice",
      question: "Cơ học Newton là nền tảng của giai đoạn nào trong quá trình phát triển của Vật lí?",
      options: ["Tiền Vật lí", "Vật lí cổ điển", "Vật lí hiện đại", "Vật lí lượng tử"],
      answer: 1,
      explanation: "Cơ học Newton (thế kỉ XVII) mở đầu giai đoạn Vật lí cổ điển.",
    },
    {
      type: "true_false",
      question: "Xét các phát biểu sau về vai trò của Vật lí:",
      statements: [
        { text: "Vật lí là cơ sở của nhiều ngành khoa học tự nhiên và kĩ thuật.", answer: true },
        { text: "Thiết bị bán dẫn và vệ tinh viễn thông là thành tựu ứng dụng của Vật lí.", answer: true },
        { text: "Sự phát triển của Vật lí không ảnh hưởng đến đời sống hằng ngày của con người.", answer: false },
        { text: "Vật lí chỉ có giá trị lí thuyết, không có ứng dụng thực tế.", answer: false },
      ],
      explanation: "Vật lí vừa là nền tảng khoa học vừa có nhiều ứng dụng thực tế ảnh hưởng đến đời sống.",
    },
    {
      type: "true_false",
      question: "Xét các phát biểu sau về quá trình phát triển của Vật lí:",
      statements: [
        { text: "Giai đoạn tiền Vật lí chủ yếu dựa trên quan sát và suy luận chủ quan, chưa có thực nghiệm định lượng.", answer: true },
        { text: "Vật lí cổ điển gồm cơ học, nhiệt động lực học và điện từ học cổ điển.", answer: true },
        { text: "Thuyết tương đối và cơ học lượng tử thuộc giai đoạn Vật lí cổ điển.", answer: false },
        { text: "Vật lí hiện đại ra đời từ cuối thế kỉ XIX, đầu thế kỉ XX.", answer: true },
      ],
      explanation: "Thuyết tương đối và cơ học lượng tử là nền tảng của Vật lí hiện đại, không phải Vật lí cổ điển.",
    },
    {
      type: "short_answer",
      question: "Vật lí có bao nhiêu phương pháp nghiên cứu chính? (ghi số)",
      answer: "2",
      explanation: "Hai phương pháp: thực nghiệm và lí thuyết, hỗ trợ và bổ sung cho nhau.",
    },
    {
      type: "short_answer",
      question: "Cơ học Newton được xây dựng chủ yếu trong thế kỉ mấy? (ghi 2 chữ số, vd 17)",
      answer: "17",
      explanation: "Newton công bố các định luật cơ học nền tảng vào thế kỉ XVII.",
    },
  ],
};

async function insertExam(exam) {
  const { data, error } = await supabase.from("exams").insert(exam).select("id").single();
  if (error) throw error;
  await supabase.from("exam_classes").insert({ exam_id: data.id, class_id: CLASS_ID });
  return data.id;
}

async function main() {
  const { data: lesson, error: lessonError } = await supabase
    .from("lessons")
    .select("id, title, chapter_id")
    .eq("id", LESSON_ID)
    .single();
  if (lessonError || !lesson) {
    console.error("Không tìm thấy lesson_id", LESSON_ID, lessonError?.message);
    process.exit(1);
  }
  console.log(`Bài học: #${lesson.id} "${lesson.title}"`);

  const { data: existingItems, error: existingError } = await supabase
    .from("lesson_items")
    .select("id")
    .eq("lesson_id", LESSON_ID);
  if (existingError) throw existingError;
  if ((existingItems ?? []).length > 0) {
    console.log(`Bài học đã có ${existingItems.length} mục — bỏ qua để tránh trùng lặp.`);
    return;
  }

  console.log("Đang tạo đề Luyện tập…");
  const luyenTapId = await insertExam(luyenTapExam);
  console.log(`  → exam id ${luyenTapId}`);

  console.log("Đang tạo đề Kiểm tra…");
  const kiemTraId = await insertExam(kiemTraExam);
  console.log(`  → exam id ${kiemTraId}`);

  const items = [
    {
      lesson_id: LESSON_ID,
      kind: "ly_thuyet",
      title: "Lý thuyết trọng tâm",
      subtitle: "Đối tượng, mục tiêu, quá trình phát triển, vai trò và phương pháp nghiên cứu Vật lí",
      body_html: lyThuyetHtml,
      video_url: "",
      pdf_url: "",
      questions: [],
      exam_ids: [],
      sort_order: 1,
    },
    {
      lesson_id: LESSON_ID,
      kind: "video",
      title: "Video bài giảng",
      subtitle: "Chưa gắn video — dán link YouTube của bạn ở đây khi có bản ghi bài giảng",
      body_html: "",
      video_url: "",
      pdf_url: "",
      questions: [],
      exam_ids: [],
      sort_order: 2,
    },
    {
      lesson_id: LESSON_ID,
      kind: "bai_tap_mau",
      title: "Các dạng bài tập",
      subtitle: "3 dạng bài thường gặp kèm lời giải chi tiết",
      body_html: "",
      video_url: "",
      pdf_url: "",
      questions: workedQuestions,
      exam_ids: [],
      sort_order: 3,
    },
    {
      lesson_id: LESSON_ID,
      kind: "luyen_tap",
      title: "Luyện tập",
      subtitle: "10 câu (6 TN · 2 ĐS · 2 TLN) — 20 phút",
      body_html: "",
      video_url: "",
      pdf_url: "",
      questions: [],
      exam_ids: [luyenTapId],
      sort_order: 4,
    },
    {
      lesson_id: LESSON_ID,
      kind: "kiem_tra",
      title: "Kiểm tra",
      subtitle: "8 câu (4 TN · 2 ĐS · 2 TLN) — 25 phút",
      body_html: "",
      video_url: "",
      pdf_url: "",
      questions: [],
      exam_ids: [kiemTraId],
      sort_order: 5,
    },
  ];

  const { error: insertError } = await supabase.from("lesson_items").insert(items);
  if (insertError) throw insertError;
  console.log(`Đã thêm ${items.length} mục cho bài "${lesson.title}".`);
}

main().catch((err) => {
  console.error("Lỗi:", err.message ?? err);
  process.exit(1);
});
