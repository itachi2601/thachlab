// Dựng lại public.exam_question_results từ exam_results.detail.responses đã có —
// để tab "Phân tích" và trang "Kết quả học tập" có số liệu ngay cho các lần làm bài cũ.
//
// Chấm lại từng câu bằng đúng luật gradeQuestion (TN 0,25đ; ĐS luỹ tiến; TLN 0,25đ),
// đối chiếu với exams.questions HIỆN TẠI. Nếu đề đã bị sửa/đổi thứ tự sau khi học sinh làm
// thì các dòng này có thể lệch — đánh dấu estimated=true và tab Phân tích không tính chúng
// vào "câu sai nhiều nhất".
//
// App export tĩnh, không có server ở production. Script CHỈ chạy cục bộ, SAU KHI đã chạy
// docs/supabase-migration-exam-analytics.sql:
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co \
//     node scripts/backfill-exam-analytics.mjs
//
// Chạy lại an toàn: bỏ qua exam_result đã có đủ dòng exam_question_results.

import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY.");
  process.exit(1);
}
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const TF_SCALE = [0, 0.1, 0.25, 0.5, 1];

function gradeQuestion(q, r) {
  switch (q.type) {
    case "multiple_choice":
      return { earned: r === q.answer ? 0.25 : 0, max: 0.25 };
    case "true_false": {
      const picks = Array.isArray(r) ? r : [];
      const correct = q.statements.filter((s, i) => picks[i] === s.answer).length;
      return { earned: TF_SCALE[correct] ?? 0, max: 1 };
    }
    case "short_answer": {
      const norm = (v) => String(v ?? "").trim().replace(".", ",");
      return { earned: r && norm(r) === norm(q.answer) ? 0.25 : 0, max: 0.25 };
    }
    default:
      return { earned: 0, max: 0 }; // essay
  }
}

// --- danh mục chủ đề: tên -> id ---
const { data: topics } = await supabase.from("question_topics").select("id, name");
const topicIdByName = new Map((topics ?? []).map((t) => [t.name, t.id]));

// --- các đề đã có kết quả ---
const { data: exams } = await supabase.from("exams").select("id, questions");
const questionsByExam = new Map((exams ?? []).map((e) => [e.id, e.questions ?? []]));

const { data: results, error } = await supabase
  .from("exam_results")
  .select("id, exam_id, student_id, detail")
  .order("id");
if (error) {
  console.error(error.message);
  process.exit(1);
}

const { data: existing } = await supabase
  .from("exam_question_results")
  .select("exam_result_id");
const done = new Set((existing ?? []).map((r) => r.exam_result_id));

let inserted = 0;
let skipped = 0;
let batch = [];

async function flush() {
  if (batch.length === 0) return;
  const { error: e } = await supabase.from("exam_question_results").insert(batch);
  if (e) console.error("insert lỗi:", e.message);
  else inserted += batch.length;
  batch = [];
}

for (const res of results ?? []) {
  if (done.has(res.id)) {
    skipped++;
    continue;
  }
  const questions = questionsByExam.get(res.exam_id);
  const responses = res.detail?.responses;
  if (!Array.isArray(questions) || !Array.isArray(responses)) {
    skipped++;
    continue;
  }
  const lenMismatch = questions.length !== responses.length;
  questions.forEach((q, i) => {
    const g = gradeQuestion(q, responses[i]);
    const name = String(q.topic ?? "").trim();
    batch.push({
      exam_result_id: res.id,
      question_index: i,
      student_id: res.student_id,
      exam_id: res.exam_id,
      topic_id: name ? topicIdByName.get(name) ?? null : null,
      topic_name: name,
      form: q.form ?? "",
      qtype: q.type,
      earned: g.earned,
      max: g.max,
      is_correct: g.max > 0 && g.earned === g.max,
      estimated: lenMismatch,
    });
  });
  if (batch.length >= 500) await flush();
}
await flush();

console.log(`✓ Backfill xong — thêm ${inserted} dòng, bỏ qua ${skipped} lượt làm.`);
