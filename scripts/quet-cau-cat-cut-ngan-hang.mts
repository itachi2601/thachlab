// Quét question_bank (archived=false) tìm câu cắt cụt / lỗi hiển thị — CHỈ ĐỌC.
//   npx tsx scripts/quet-cau-cat-cut-ngan-hang.mts [--mau]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.dirname(fileURLToPath(import.meta.url));
const envTxt = fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n");
const env = (k: string) => envTxt.find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim()!;
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });

if (process.argv.includes("--mau")) {
  const { data } = await sb.from("question_bank").select("id,qtype,question").eq("archived", false).limit(3);
  console.log(JSON.stringify(data, null, 1).slice(0, 3000));
  process.exit(0);
}

import { lintQuestion } from "../lib/question-lint";
type Hit = { id: number; grade: string; rule: string; level: string; ctx: string };
const hits: Hit[] = [];
let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, grade, qtype, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    total++;
    for (const f of lintQuestion(r.question, r.qtype)) hits.push({ id: r.id, grade: r.grade, rule: f.code, level: f.level, ctx: f.ctx });
  }
  from += 1000;
}
const outFile = path.join(dir, "logs", `quet-cat-cut-${Date.now()}.json`);
fs.writeFileSync(outFile, JSON.stringify(hits, null, 2));
const byRule: Record<string, Set<number>> = {};
for (const h of hits) (byRule[h.rule] ??= new Set()).add(h.id);
console.log(`Quét ${total} câu →`, path.relative(process.cwd(), outFile));
for (const [k, v] of Object.entries(byRule)) console.log(k.padEnd(24), v.size);
