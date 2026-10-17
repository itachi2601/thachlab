// Gỡ exam_classes của mọi đề subject_code='avcn' — lớp AVCN vào tự do (migration 20261013180000 đã cố ý bỏ gán cho đề 914;
// đợt gán lớp 17/10/2026 gán nhầm lại → 51 lượt làm của sinh viên không xem lại được vì RLS). Sao lưu ra scripts/logs/.
//   npx tsx scripts/go-gan-lop-de-avcn.mts [--apply]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const d = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(d, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const { data: exams, error } = await sb.from("exams").select("id,title,exam_classes(class_id)").eq("subject_code", "avcn");
if (error) { console.error(error.message); process.exit(1); }
const rows = exams!.flatMap((e) => e.exam_classes.map((c: { class_id: number }) => ({ exam_id: e.id, class_id: c.class_id, title: e.title })));
console.log(`Đề avcn: ${exams!.length} · dòng exam_classes sẽ gỡ: ${rows.length}`);
for (const r of rows) console.log(`  #${r.exam_id} lớp ${r.class_id} | ${r.title}`);
if (!APPLY || rows.length === 0) process.exit(0);
const bak = path.resolve(d, "logs", `go-gan-lop-de-avcn-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
fs.writeFileSync(bak, JSON.stringify(rows, null, 1));
const { error: e2 } = await sb.from("exam_classes").delete().in("exam_id", rows.map((r) => r.exam_id));
if (e2) { console.error(e2.message); process.exit(1); }
const { data: after } = await sb.from("exam_classes").select("exam_id").in("exam_id", rows.map((r) => r.exam_id));
console.log(`Đã gỡ. Còn lại: ${after?.length ?? "?"} dòng. Sao lưu: ${bak}`);
