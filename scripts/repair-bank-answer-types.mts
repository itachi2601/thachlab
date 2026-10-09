// Sửa kiểu dữ liệu đáp án sau đợt áp 9/10/2026: mc phải là CHỈ SỐ (0-3), short phải là CHUỖI, tf phải là mảng boolean.
// Chỉ đụng câu thuộc đợt 9/10 (scripts/data/audit-9-10-applied.json) mà đáp án hiện tại đang SAI KIỂU. Mặc định dry-run; --apply để ghi.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
type Fix = { id: number; kind: "mc" | "short" | "tf"; neu: number | string | boolean[] };
const fixes = Object.values(JSON.parse(fs.readFileSync(path.join(dir, "data", "audit-9-10-applied.json"), "utf8"))) as Fix[];
const backup: unknown[] = []; let need = 0, done = 0, fine = 0;
for (const f of fixes) {
  const { data } = await sb.from("question_bank").select("id, question").eq("id", f.id).single();
  if (!data) { console.log(`? ${f.id} không đọc được`); continue; }
  const q = data.question as Record<string, any>;
  let next: Record<string, any> | null = null;
  if (f.kind === "mc") { if (q.answer !== f.neu) next = { ...q, answer: f.neu }; }
  else if (f.kind === "short") { if (String(q.answer) !== f.neu || typeof q.answer !== "string") next = { ...q, answer: f.neu }; }
  else { const want = f.neu as boolean[]; const cur = (q.statements ?? []).map((s: any) => s.answer); if (!(cur.length === 4 && cur.every((v: any, i: number) => v === want[i]))) next = { ...q, statements: (q.statements ?? []).map((s: any, i: number) => ({ ...s, answer: want[i] })) }; }
  if (!next) { fine++; continue; }
  need++; backup.push({ id: f.id, question: q });
  console.log(`• ${f.id} [${f.kind}] ${JSON.stringify(f.kind === "tf" ? q.statements?.map((s: any) => s.answer) : q.answer)} → ${JSON.stringify(f.neu)}`);
  if (APPLY) { const { error } = await sb.from("question_bank").update({ question: next }).eq("id", f.id); if (error) console.log(`   ✗ ${error.message}`); else done++; }
}
const bk = path.join(dir, "logs", `repair-types-backup-${Date.now()}.json`); fs.writeFileSync(bk, JSON.stringify(backup));
console.log(`\nĐã đúng kiểu: ${fine} · cần sửa: ${need} · ${APPLY ? `đã ghi ${done}` : "DRY-RUN"} · sao lưu → ${path.relative(process.cwd(), bk)}`);
