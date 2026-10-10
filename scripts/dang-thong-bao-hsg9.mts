// Đăng thông báo/học liệu cho lớp HSG (scripts/data/thong-bao-hsg9/*.json) vào bảng `posts` qua RPC create_post_with_targets.
// Mặc định DRY-RUN; thêm --yes mới ghi thật. CHẠY TRÊN MAC (cần service role).
//   npx tsx scripts/dang-thong-bao-hsg9.mts [--yes]
// File JSON: { title, body_html, subject_code, class_ids, content_type }. Đăng xong tự ghi posted_id (chống đăng trùng).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIR = path.join(root, "scripts", "data", "thong-bao-hsg9");
const yes = process.argv.includes("--yes");

function envLocal(key: string): string | undefined {
  const line = fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const url = envLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = envLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) throw new Error("thiếu khoá Supabase trong .env.local");
const sb = createClient(url, key);

for (const f of fs.readdirSync(DIR).filter((x) => x.endsWith(".json")).sort()) {
  const fp = path.join(DIR, f);
  const n = JSON.parse(fs.readFileSync(fp, "utf8"));
  if (n.posted_id) { console.log(`= ${f}: đã đăng (post ${n.posted_id})`); continue; }
  if (/\n|<script|javascript:/i.test(n.body_html)) throw new Error(`${f}: body_html có xuống dòng hoặc script`);
  const { data: dup } = await sb.from("posts").select("id").eq("title", n.title).limit(1);
  if (dup?.length) { console.log(`≈ ${f}: trùng tiêu đề post ${dup[0].id} — bỏ qua`); continue; }
  console.log(`${yes ? "→ đăng" : "○ sẽ đăng"} ${f}: "${n.title}" [lớp ${n.class_ids.join(",")}]`);
  if (!yes) continue;
  const { data, error } = await sb.rpc("create_post_with_targets", {
    p_title: n.title, p_body: n.body_html, p_video_url: "", p_content_type: n.content_type,
    p_subject_code: n.subject_code, p_class_ids: n.class_ids, p_course_ids: [],
  });
  if (error) throw new Error(error.message);
  n.posted_id = data;
  fs.writeFileSync(fp, JSON.stringify(n, null, 2) + "\n");
  const { data: row } = await sb.from("posts").select("published").eq("id", data).single();
  console.log(`  ✓ post ${data} — ${row?.published ? "ĐANG HIỆN" : "đang ẨN (bật Hiện ở /quan-tri/bai-dang)"}`);
}
