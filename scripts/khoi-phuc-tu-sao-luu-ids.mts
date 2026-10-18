// Trả một số câu question_bank về đúng bản trong một file sao lưu ({id, question}[]) — dùng khi lỡ ghi đè nhầm.
//   npx tsx scripts/khoi-phuc-tu-sao-luu-ids.mts <file sao lưu> <id,id,...> [--apply]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const [file, idsArg] = process.argv.slice(2);
const APPLY = process.argv.includes("--apply");
const ids = new Set(idsArg.split(",").map(Number));
const bk: { id: number; question: any }[] = JSON.parse(fs.readFileSync(file, "utf8")).filter((x: any) => ids.has(x.id));
console.log(`tìm thấy ${bk.length}/${ids.size} câu trong sao lưu`);
const { data: cur, error } = await sb.from("question_bank").select("id,question").in("id", [...ids]);
if (error) throw new Error(error.message);
const bp = `scripts/logs/khoi-phuc-ids-backup-${Date.now()}.json`;
if (APPLY) fs.writeFileSync(bp, JSON.stringify(cur));
for (const x of bk) {
  const now = cur!.find((c) => c.id === x.id)?.question;
  console.log(x.id, "hiện:", JSON.stringify(now?.answer ?? now?.statements?.map((s: any) => s.answer)), "→ sao lưu:", JSON.stringify(x.question.answer ?? x.question.statements?.map((s: any) => s.answer)));
  if (!APPLY) continue;
  const { error: e } = await sb.from("question_bank").update({ question: x.question }).eq("id", x.id);
  console.log(e ? `  LỖI ${e.message}` : "  đã ghi");
}
if (APPLY) console.log("sao lưu trước khi ghi:", bp); else console.log("dry-run — thêm --apply để ghi");
