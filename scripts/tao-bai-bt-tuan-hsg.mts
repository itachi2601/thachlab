// Tạo bài "Bài tập tuần này: 12 bài tự luận Cơ học VD–VDC" ở đầu chương Cơ học (khoá HSG, chương 32) + 1 mục bai_tap_mau rỗng.
// Bài tạo với published=false; bật khi nội dung đã đăng và kiểm xong. Idempotent theo tiêu đề. Chạy trên Mac (service role).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = Object.fromEntries(fs.readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=")).map((l) => [l.slice(0, l.indexOf("=")), l.slice(l.indexOf("=") + 1).trim()]));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const TITLE = "Bài tập tuần này: 12 bài tự luận Cơ học (Vận dụng → Vận dụng cao)";
const CHAPTER = 32;
const { data: ex } = await sb.from("lessons").select("id").eq("chapter_id", CHAPTER).eq("title", TITLE);
if (ex?.length) { console.log("đã có bài", ex[0].id); process.exit(0); }
const { data: ls, error } = await sb.from("lessons").insert({
  chapter_id: CHAPTER, title: TITLE, sort_order: 0, published: false, lesson_kind: "bai_hoc",
  description: "Mỗi ngày 2 bài, làm từng ý, có gợi ý mở dần. Thứ Bảy 17/10 sửa bài.",
}).select("id").single();
if (error) throw error;
const { error: e2 } = await sb.from("lesson_items").insert({
  lesson_id: ls.id, kind: "bai_tap_mau", title: "12 bài tự luận", subtitle: "12 bài kèm gợi ý từng bước",
  sort_order: 1, required: true, questions: [], published_at: new Date().toISOString(),
});
if (e2) throw e2;
console.log("đã tạo bài", ls.id);
