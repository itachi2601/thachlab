// Chỉ ĐỌC: xuất đề/mục bài bị báo lỗi (26/11/2026) + tải ảnh chụp. Dùng: npx tsx scripts/dump-bao-loi-2026-11-26.mts [thư-mục]
import { createClient } from "@supabase/supabase-js";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const out = process.argv[2] ?? "scripts/logs/bao-loi-1126";
mkdirSync(out, { recursive: true });
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data: exams } = await sb.from("exams").select("id,title,questions").in("id", [1397, 96]);
for (const e of exams ?? []) {
  writeFileSync(`${out}/de-${e.id}.json`, JSON.stringify(e, null, 1));
  console.log("de", e.id, e.title, (e.questions as unknown[])?.length);
}
const { data: item226 } = await sb.from("lesson_items").select("id,lesson_id,kind,title,exam_ids").eq("id", 226);
console.log("item226", JSON.stringify(item226));
const { data: items } = await sb.from("lesson_items").select("id,lesson_id,kind,title,exam_ids,questions,body_html").in("lesson_id", [6, 7, 8, 34, 176, 60]);
for (const it of items ?? []) {
  writeFileSync(`${out}/item-${it.lesson_id}-${it.id}-${it.kind}.json`, JSON.stringify(it, null, 1));
  console.log("item", it.lesson_id, it.id, it.kind, it.title, "exam_ids", JSON.stringify(it.exam_ids), "q", Array.isArray(it.questions) ? it.questions.length : 0, "html", it.body_html?.length ?? 0);
  for (const eid of (it.exam_ids as number[] | null) ?? []) {
    const { data: e } = await sb.from("exams").select("id,title,questions").eq("id", eid).single();
    if (e) { writeFileSync(`${out}/de-${e.id}.json`, JSON.stringify(e, null, 1)); console.log("  de", e.id, e.title, (e.questions as unknown[])?.length); }
  }
}
const { data: bugs } = await sb.from("bug_reports").select("id,screenshot_path").in("id", [161, 169, 171, 172, 174, 176, 177]);
for (const r of bugs ?? []) {
  const { data: f, error } = await sb.storage.from("bug-report-screenshots").download(r.screenshot_path);
  if (error || !f) { console.log("fail", r.id, error?.message); continue; }
  writeFileSync(`${out}/${r.id}.jpg`, Buffer.from(await f.arrayBuffer()));
  console.log("anh", r.id);
}
