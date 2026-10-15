// Quét question_bank tìm ký hiệu thiếu chỉ số dưới (S1, F1, v2… thay vì S_1, F_1, v_2) — CHỈ ĐỌC.
//   npx tsx scripts/quet-chi-so-duoi-ngan-hang.mts
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

// một chữ cái (không dính chữ/số/\ phía trước) + 1–2 chữ số, không theo sau bởi chữ số/chữ cái/_
const RE = /(?<![A-Za-z0-9_\\.,])([A-Za-z])([0-9]{1,2})(?![A-Za-z0-9_])/g;
const strings = (v: unknown, out: string[] = []): string[] => {
  if (typeof v === "string") out.push(v);
  else if (Array.isArray(v)) v.forEach((x) => strings(x, out));
  else if (v && typeof v === "object") Object.values(v).forEach((x) => strings(x, out));
  return out;
};
const byTok: Record<string, Set<number>> = {};
const SKIP = new Set(["N2","O2","H2","H3","C8","C2","C1","C3","S0","v1","s2","m3","s1","A1","A2","A3","A4","D1","D2","B1","B2","H1","H0","N1","N0"]);
const idsAll = new Set<number>(), idsPlain = new Set<number>(), idsMath = new Set<number>();
const sampM: string[] = [], sampP: string[] = [];
const samples: Record<string, string> = {};
let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    total++;
    for (const s0 of strings(r.question)) {
      if (/^https?:/.test(s0) || s0.length > 20000) continue;
      const s = s0.replace(/<[^>]+>/g, " ").replace(/data:image[^"')\s]*/g, "");
      for (const m of s.matchAll(RE)) {
        const tok = m[1] + m[2];
        const iPos = m.index ?? 0;
        const inMath = (s.slice(0, iPos).replace(/\\\$/g, "").match(/\$/g)?.length ?? 0) % 2 === 1;
        if (!SKIP.has(tok) && !/[\/\d]\s?$/.test(s.slice(Math.max(0, iPos - 2), iPos)) && !/^[ms][23]$/.test(tok)) {
          idsAll.add(r.id); (inMath ? idsMath : idsPlain).add(r.id);
          const smp = `${r.id} ${inMath ? "M" : "P"}: ${s.slice(Math.max(0, iPos - 30), iPos + 25).replace(/\s+/g, " ")}`;
          if (inMath && sampM.length < 12) sampM.push(smp); if (!inMath && sampP.length < 12) sampP.push(smp);
        }
        (byTok[tok] ??= new Set()).add(r.id);
        const i = m.index ?? 0;
        samples[tok] ??= `${r.id}: ${s.slice(Math.max(0, i - 30), i + 25).replace(/\s+/g, " ")}`;
      }
    }
  }
  from += 1000;
}
const rows0 = 0;
const rows = Object.entries(byTok).map(([t, s]) => [t, s.size] as const).sort((a, b) => b[1] - a[1]);
const outFile = path.join(scriptDir, "logs", `quet-chi-so-duoi-${Date.now()}.json`);
fs.writeFileSync(outFile, JSON.stringify(Object.fromEntries(Object.entries(byTok).map(([t, s]) => [t, [...s]])), null, 2));
console.log(`Quét ${total} câu · ${rows.length} ký hiệu →`, path.relative(process.cwd(), outFile));
for (const [t, n] of rows.slice(0, 70)) console.log(t.padEnd(5), String(n).padStart(5), "|", samples[t]);

console.log("--- Sau loại hoá học/đơn vị ---");
console.log("câu nghi lỗi:", idsAll.size, "· có chỗ ngoài $…$:", idsPlain.size, "· có chỗ trong $…$:", idsMath.size);
console.log(sampP.join("\n")); console.log(sampM.join("\n"));
