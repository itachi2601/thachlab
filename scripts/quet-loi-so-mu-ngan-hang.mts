// Quét question_bank tìm số mũ/đơn vị bị mất dấu ^ (2.105 Pa thay vì 2.10^5 Pa; m3, m2, m/s2...) — CHỈ ĐỌC.
//   npx tsx scripts/quet-loi-so-mu-ngan-hang.mts
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function env(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

import { MU_RULES as RULES } from "../lib/question-lint";

type Hit = { id: number; grade: string; rule: string; ctx: string };
const hits: Hit[] = [];
const strings = (v: unknown, out: string[] = []): string[] => {
  if (typeof v === "string") out.push(v);
  else if (Array.isArray(v)) v.forEach((x) => strings(x, out));
  else if (v && typeof v === "object") Object.values(v).forEach((x) => strings(x, out));
  return out;
};

let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, grade, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    total++;
    for (const s of strings(r.question)) {
      for (const [rule, re] of Object.entries(RULES)) {
        for (const m of s.matchAll(re)) {
          const i = m.index ?? 0;
          hits.push({ id: r.id, grade: r.grade, rule, ctx: s.slice(Math.max(0, i - 25), i + m[0].length + 20).replace(/\s+/g, " ") });
        }
      }
    }
  }
  from += 1000;
}
const outFile = path.join(scriptDir, "logs", `quet-so-mu-${Date.now()}.json`);
fs.writeFileSync(outFile, JSON.stringify(hits, null, 2));
const byRule: Record<string, number> = {};
const ids = new Set<number>();
for (const h of hits) { byRule[h.rule] = (byRule[h.rule] ?? 0) + 1; ids.add(h.id); }
console.log(`Quét ${total} câu · ${ids.size} câu nghi lỗi · ${hits.length} chỗ`, byRule, "→", path.relative(process.cwd(), outFile));
for (const h of hits.slice(0, 40)) console.log(h.id, h.rule, "|", h.ctx);
