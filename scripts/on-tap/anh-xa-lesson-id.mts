// CHỈ ĐỌC DB. Ánh xạ slug bài (content/lesson-samples/<slug>/bundle.json: lớp + tên bài) → lessons.id cho các bài có
// ô Chốt mục, ghi content/on-tap/_lesson-ids.json để rut-the-on.py gắn lesson_id vào bộ thẻ.
//   npx tsx scripts/on-tap/anh-xa-lesson-id.mts
// Cách khớp giống scripts/anh-xa-bai-ly-thuyet.mts (bỏ "Bài N.", bỏ dấu, lớp qua chapter_classes).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, {
  auth: { persistSession: false },
});
const bo = (s: string) =>
  s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/đ/g, "d")
    .replace(/Đ/g, "D")
    .toLowerCase()
    .replace(/^\s*bai\s*\d+\s*[.:]\s*/, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
const soLop = (s: string) => (s.match(/(\d+)\s*$/) ?? [])[1];

const { data: classes } = await sb.from("classes").select("id,name");
const { data: cc } = await sb.from("chapter_classes").select("chapter_id,class_id");
const { data: lessons } = await sb.from("lessons").select("id,title,chapter_id");
const classesOf = new Map<number, number[]>();
for (const c of cc!) classesOf.set(c.chapter_id, [...(classesOf.get(c.chapter_id) ?? []), c.class_id]);

const base = path.join(root, "content/lesson-samples");
const out: Record<string, number> = {};
const loi: string[] = [];
for (const slug of fs.readdirSync(base).sort()) {
  const th = path.join(base, slug, "theory.html");
  const bj = path.join(base, slug, "bundle.json");
  if (!fs.existsSync(th) || !fs.existsSync(bj) || !fs.readFileSync(th, "utf8").includes("tl-chot")) continue;
  const t = JSON.parse(fs.readFileSync(bj, "utf8")).target;
  const cls = classes!.filter((c) => soLop(c.name) === soLop(t.class_name)).map((c) => c.id);
  const cand = lessons!.filter(
    (l) => bo(l.title) === bo(t.lesson_title) && (classesOf.get(l.chapter_id) ?? []).some((x) => cls.includes(x)),
  );
  if (cand.length === 1) out[slug] = cand[0].id;
  else loi.push(`${cand.length ? "TRUNG" : "KHONG_THAY"} ${slug} ${JSON.stringify(t)} ${cand.map((c) => c.id)}`);
}
fs.writeFileSync(path.join(root, "content/on-tap/_lesson-ids.json"), JSON.stringify(out, null, 1) + "\n");
console.log(`Khớp ${Object.keys(out).length} bài; lỗi ${loi.length}`);
for (const l of loi) console.log(l);
