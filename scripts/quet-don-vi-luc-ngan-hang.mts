// Quét CHỈ ĐỌC question_bank: (A) đơn vị gia tốc thiếu ^ (m/s2, cm/s2, km/h2) ; (B) lực F1, F2… thiếu chỉ số dưới.
//   npx tsx scripts/quet-don-vi-luc-ngan-hang.mts
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const RES: Record<string, RegExp> = {
  donvi: /(?<![A-Za-z_\\^{])((?:[kcmdµ]|)m|km)\s*\/\s*(s|h)\s*([23])(?![\d_^{A-Za-z])/g,
  luc: /(?<![A-Za-z_\\^{.,\d])F([1-9])(?![\d_^{A-Za-z])/g,
};
const strings = (v: unknown, o: string[] = []): string[] => { if (typeof v === "string") o.push(v); else if (Array.isArray(v)) v.forEach((x) => strings(x, o)); else if (v && typeof v === "object") Object.values(v).forEach((x) => strings(x, o)); return o; };
const hits: any[] = []; let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) { total++; for (const s of strings(r.question)) for (const [k, re] of Object.entries(RES)) for (const m of s.matchAll(re)) { const i = m.index!; hits.push({ id: r.id, k, tok: m[0], ctx: s.slice(Math.max(0, i - 25), i + m[0].length + 20).replace(/\s+/g, " ") }); } }
  from += 1000;
}
const f = path.join(scriptDir, "logs", `quet-don-vi-luc-${Date.now()}.json`);
fs.writeFileSync(f, JSON.stringify(hits, null, 2));
for (const k of Object.keys(RES)) { const h = hits.filter((x) => x.k === k); const by: Record<string, number> = {}; h.forEach((x) => (by[x.tok] = (by[x.tok] ?? 0) + 1)); console.log(k, "câu", new Set(h.map((x) => x.id)).size, "chỗ", h.length, by); }
console.log("Quét", total, "→", path.relative(process.cwd(), f));
