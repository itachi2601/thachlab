// Chỉ ĐỌC: xuất đề bị báo lỗi (nhóm A, 12/11/2026) + tải ảnh chụp ra thư mục. Dùng: npx tsx scripts/dump-de-bao-loi-2026-11-12.mts <thư-mục>
import { createClient } from "@supabase/supabase-js";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const out = process.argv[2] ?? "scripts/logs/de-bao-loi-1112";
mkdirSync(out, { recursive: true });
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const { data: exams } = await sb.from("exams").select("id,title,questions").in("id", [1354, 1298, 753, 23, 945, 476]);
for (const e of exams ?? []) {
  writeFileSync(`${out}/de-${e.id}.json`, JSON.stringify(e, null, 1));
  console.log("de", e.id, e.title, (e.questions as unknown[])?.length);
}
const { data: bugs } = await sb.from("bug_reports").select("id,screenshot_path").in("id", [149, 151, 160]);
for (const r of bugs ?? []) {
  const { data: f, error } = await sb.storage.from("bug-report-screenshots").download(r.screenshot_path);
  if (error || !f) { console.log("fail", r.id, error?.message); continue; }
  writeFileSync(`${out}/${r.id}.jpg`, Buffer.from(await f.arrayBuffer()));
  console.log("anh", r.id);
}
