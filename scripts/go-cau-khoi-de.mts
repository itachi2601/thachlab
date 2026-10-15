// Gỡ MỘT câu khỏi đề đã đăng (chỉ khi đề chưa có bài làm nào), có sao lưu + kiểm lại sau khi ghi.
//   npx tsx scripts/go-cau-khoi-de.mts <exam_id> <số câu 1-based> <chuỗi nhận diện trong câu> [--apply]
//   npx tsx scripts/go-cau-khoi-de.mts --rollback <file sao lưu>
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.dirname(fileURLToPath(import.meta.url));
const env = fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8");
const g = (k: string) => env.split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(g("NEXT_PUBLIC_SUPABASE_URL"), g("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const a = process.argv.slice(2);
const rb = a.indexOf("--rollback");
if (rb >= 0) {
  const bk = JSON.parse(fs.readFileSync(a[rb + 1], "utf8"));
  const { error } = await sb.from("exams").update({ questions: bk.questions }).eq("id", bk.id);
  console.log(error?.message ?? "đã trả đề về bản cũ"); process.exit(0);
}
const [idS, nS, needle] = a.filter((x) => !x.startsWith("--"));
const id = Number(idS), n = Number(nS), APPLY = a.includes("--apply");
const { data: ex, error } = await sb.from("exams").select("id,title,published,questions,question_count,type_counts").eq("id", id).single();
if (error || !ex) { console.error(error?.message); process.exit(1); }
const qs = ex.questions as { type?: string }[];
if (!JSON.stringify(qs[n - 1]).includes(needle)) { console.error(`Câu ${n} không chứa "${needle}" — dừng.`); process.exit(1); }
for (const t of ["exam_results", "exam_question_results", "exam_attempts"]) {
  const r = await sb.from(t).select("*", { count: "exact", head: true }).eq("exam_id", id);
  if (r.error) { console.error(t, r.error.message); process.exit(1); }
  if (r.count) { console.error(`${t} có ${r.count} dòng của đề ${id} — gỡ câu sẽ lệch chỉ số câu, dừng.`); process.exit(1); }
}
const next = qs.filter((_, i) => i !== n - 1);
const tc: Record<string, number> = {}; for (const q of next) tc[q.type ?? "?"] = (tc[q.type ?? "?"] ?? 0) + 1;
console.log(`Đề ${id} "${ex.title}" (published=${ex.published}): ${qs.length} → ${next.length} câu; type_counts`, ex.type_counts, "→", tc);
if (!APPLY) { console.log("DRY-RUN: chưa ghi."); process.exit(0); }
fs.mkdirSync(path.join(dir, "logs"), { recursive: true });
const f = path.join(dir, "logs", `go-cau-de${id}-${new Date().toISOString().replace(/[:.]/g, "-")}.backup.json`);
fs.writeFileSync(f, JSON.stringify({ id, questions: ex.questions, question_count: ex.question_count, type_counts: ex.type_counts }));
const u = await sb.from("exams").update({ questions: next }).eq("id", id);
if (u.error) { console.error("LỖI", u.error.message); process.exit(1); }
// question_count và type_counts là cột sinh tự động — chỉ ghi questions
const { data: chk } = await sb.from("exams").select("questions,question_count,type_counts").eq("id", id).single();
const ok = chk!.question_count === next.length && (chk!.questions as unknown[]).length === next.length && !JSON.stringify(chk!.questions).includes(needle);
console.log(ok ? `ĐÃ GHI & KIỂM LẠI: còn ${next.length} câu, chuỗi "${needle}" không còn.` : "KIỂM LẠI THẤT BẠI");
console.log("Sao lưu:", f);
