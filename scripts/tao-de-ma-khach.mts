// Tạo đề (không gắn bài học, published=false) từ một bundle chỉ-có-đề + mã làm bằng QR/nhập mã + bảng điểm.
//   npx tsx scripts/tao-de-ma-khach.mts <bundle.json> "CĐCK 24A" [--apply]
// Không có --apply: chỉ in việc sẽ làm. Chạy lại không tạo trùng (đề trùng tiêu đề trong cùng môn thì dùng lại).
import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";

const [bundlePath, gradebookArg] = process.argv.slice(2).filter((a) => !a.startsWith("--"));
// "@đường-dẫn": đọc tên bảng điểm từ file (tránh gõ ký tự có dấu trên dòng lệnh)
const gradebook = gradebookArg?.startsWith("@") ? readFileSync(gradebookArg.slice(1), "utf8").trim() : gradebookArg;
const APPLY = process.argv.includes("--apply");
if (!bundlePath || !gradebook) throw new Error('Cách dùng: tao-de-ma-khach.mts <bundle.json> "<tên bảng điểm>" [--apply]');
const env = Object.fromEntries(
  readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#")).map((l) => {
    const i = l.indexOf("=");
    return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, "")];
  }),
);
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const exam = JSON.parse(readFileSync(bundlePath, "utf8")).exam;
console.log(`Đề "${exam.title}": ${exam.questions.length} câu, ${exam.duration_minutes} phút → bảng điểm "${gradebook}"`);

const { data: old } = await sb.from("exams").select("id").eq("title", exam.title).eq("subject_code", exam.subject_code).maybeSingle();
if (!APPLY) {
  console.log(old ? `(sẽ dùng lại đề #${old.id})` : "(sẽ tạo đề mới, published=false)");
  process.exit(0);
}
let examId = old?.id as number | undefined;
if (examId) {
  // đề đã có: cập nhật nội dung (chỉ an toàn khi chưa có lượt làm nào cần giữ nguyên thứ tự câu)
  const { error } = await sb.from("exams").update({ questions: exam.questions, duration_minutes: exam.duration_minutes }).eq("id", examId);
  if (error) throw error;
} else {
  const { data, error } = await sb
    .from("exams")
    .insert({ title: exam.title, topic: exam.topic, difficulty: exam.difficulty, duration_minutes: exam.duration_minutes, subject_code: exam.subject_code, published: false, questions: exam.questions })
    .select("id")
    .single();
  if (error) throw error;
  examId = data.id;
}
const { data: have } = await sb.from("guest_exam_links").select("code").eq("exam_id", examId!).eq("gradebook", gradebook).maybeSingle();
let code = have?.code as string | undefined;
if (!code) {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  code = Array.from({ length: 6 }, () => chars[Math.floor(Math.random() * chars.length)]).join("");
  const { error } = await sb.from("guest_exam_links").insert({ code, exam_id: examId, gradebook });
  if (error) throw error;
}
console.log(`Đề #${examId} · mã ${code}\nLink: https://thachlab.id.vn/thi/?ma=${code}\nQuản trị: /quan-tri/bang-diem-ma`);
