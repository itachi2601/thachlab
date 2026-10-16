// Quét question_bank tìm độ C mất dấu độ: "500C" (=50°C), "-270C", "t0C", "27^0C" — CHỈ ĐỌC.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const RE = /(?<![\d.,A-Za-z^_])([-−–]?\s?\d{1,4}(?:[.,]\d+)?)\s?(?:\^\s?\{?0\}?|0)\s?C(?![A-Za-z0-9])/g;
const strs = (v: unknown, o: string[] = []): string[] => { if (typeof v === "string") o.push(v); else if (Array.isArray(v)) v.forEach((x) => strs(x, o)); else if (v && typeof v === "object") Object.values(v).forEach((x) => strs(x, o)); return o; };
const hits: any[] = []; let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) { total++; for (const s of strs(r.question)) for (const m of s.matchAll(RE)) { const i = m.index!; hits.push({ id: r.id, tok: m[0], ctx: s.slice(Math.max(0, i - 40), i + m[0].length + 25).replace(/\s+/g, " ") }); } }
  from += 1000;
}
fs.writeFileSync(`scripts/logs/quet-do-c-${Date.now()}.json`, JSON.stringify(hits, null, 2));
console.log(`Quét ${total} câu · ${new Set(hits.map((h) => h.id)).size} câu · ${hits.length} chỗ`);
for (const h of hits) console.log(h.id, `[${h.tok}]`, "|", h.ctx);
