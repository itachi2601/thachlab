// Lưu `questions` hiện có của mục bai_tap_mau (các bài chỉ định) ra scripts/data/bai-tap-mau/old/<id>.json — nguồn cho
// "ví dụ cũ" khi soạn lại (skill soan-bai-tap-mau). Chạy trên Mac (service role, chỉ ĐỌC).  npx tsx scripts/dump-bai-tap-mau-cu.mts 49 50 52
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const env = (k: string) => process.env[k] ?? fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((l) => l.startsWith(k + "="))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
for (const id of process.argv.slice(2).map(Number)) {
  const { data, error } = await sb.from("lesson_items").select("id, questions").eq("lesson_id", id).eq("kind", "bai_tap_mau");
  if (error || !data || data.length !== 1) { console.error(id, "lỗi", error?.message ?? `${data?.length} mục`); continue; }
  fs.writeFileSync(path.join(root, "scripts/data/bai-tap-mau/old", `${id}.json`), JSON.stringify({ lesson_id: id, item_id: data[0].id, questions: data[0].questions }, null, 1));
  console.log(id, (data[0].questions as unknown[]).length, "dạng cũ → old/" + id + ".json");
}
