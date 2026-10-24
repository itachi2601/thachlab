// Chỉ ĐỌC: tải ảnh báo lỗi + dump đề bị báo (xu-ly-bao-loi, 24/10/2026). Chạy từ thư mục thachlab có .env.local.
import { createClient } from "@supabase/supabase-js";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const out = process.argv[2];
mkdirSync(out, { recursive: true });
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data: reps } = await sb.from("bug_reports").select("id,screenshot_path").in("id", [135, 142, 141]);
for (const r of reps ?? []) {
  if (!r.screenshot_path) continue;
  const { data: f, error } = await sb.storage.from("bug-report-screenshots").download(r.screenshot_path);
  if (error || !f) { console.log("fail", r.id, error?.message); continue; }
  writeFileSync(`${out}/${r.id}.jpg`, Buffer.from(await f.arrayBuffer()));
  console.log("anh", r.id);
}
const { data: exams } = await sb.from("exams").select("id,title,questions").in("id", [978, 979, 751, 1061, 752]);
for (const e of exams ?? []) {
  writeFileSync(`${out}/de-${e.id}.json`, JSON.stringify(e, null, 1));
  console.log("de", e.id, e.title, Array.isArray(e.questions) ? e.questions.length : "?");
}
