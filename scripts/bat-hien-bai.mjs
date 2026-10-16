// Bật Hiện (lessons.published = true) cho các bài đã được thầy duyệt; in trạng thái trước/sau.
//   node scripts/bat-hien-bai.mjs 164 153        (thêm --tat để ẩn lại)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = Object.fromEntries(fs.readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=")).map((l) => [l.slice(0, l.indexOf("=")), l.slice(l.indexOf("=") + 1).trim()]));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const val = !process.argv.includes("--tat");
const ids = process.argv.slice(2).filter((a) => /^\d+$/.test(a)).map(Number);
if (!ids.length) { console.error("thiếu lesson_id"); process.exit(1); }
const { data: before } = await sb.from("lessons").select("id,title,published").in("id", ids);
console.log("trước:", before.map((l) => `${l.id} ${l.published}`).join(", "));
const { data: after, error } = await sb.from("lessons").update({ published: val }).in("id", ids).select("id,title,published");
if (error) { console.error(error.message); process.exit(1); }
for (const l of after) console.log(`sau: ${l.id} published=${l.published} — ${l.title}`);
if (after.length !== ids.length) { console.error("số bài cập nhật không khớp"); process.exit(1); }
