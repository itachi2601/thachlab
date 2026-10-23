// CHỈ ĐỌC: in lớp → chương → bài (id, tiêu đề) vào scripts/logs/liet-ke-bai.txt để đối chiếu slug ↔ lesson_id.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const env = (k: string) => process.env[k] ?? fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((x) => x.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const [{ data: cl }, { data: cc }, { data: ch }, { data: ls }] = await Promise.all([
  sb.from("classes").select("id,name"), sb.from("chapter_classes").select("chapter_id,class_id"),
  sb.from("chapters").select("id,title"), sb.from("lessons").select("id,title,chapter_id").order("id")]);
const lines: string[] = [];
for (const c of cl!) for (const cid of cc!.filter((x) => x.class_id === c.id).map((x) => x.chapter_id)) {
  lines.push(`## ${c.id} ${c.name} / ${ch!.find((h) => h.id === cid)?.title}`);
  for (const l of ls!.filter((l) => l.chapter_id === cid)) lines.push(`${l.id}\t${l.title}`);
}
fs.writeFileSync(path.join(root, "scripts/logs/liet-ke-bai.txt"), lines.join("\n"));
console.log(lines.length, "dòng →", "scripts/logs/liet-ke-bai.txt");
