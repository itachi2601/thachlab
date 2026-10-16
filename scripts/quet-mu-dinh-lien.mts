// Quét MỌI đơn vị: "10"+số mũ dính liền, không có dấu nhân/^ trước (105 Pa, 109 Hz, 1019 J, 1023 hạt, 10-19 C…) — CHỈ ĐỌC, gom theo đơn vị.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const RE = /(?<![\d.,^{_\-−A-Za-z\/])(10(?:[-−–][1-9]\d?|[2-9]|[1-3]\d))(?![\d,.]\d|\d)(?=(?:\s|\\,|\\ |&nbsp;|<[^>]*>)*([A-Za-zΩμ°%][A-Za-zΩμ°\/%·.\-]*(?:<sup>[^<]*<\/sup>)?|\$|\)|[,;.]|$))/g;
const strs = (v: unknown, o: string[] = []): string[] => { if (typeof v === "string") o.push(v); else if (Array.isArray(v)) v.forEach((x) => strs(x, o)); else if (v && typeof v === "object") Object.values(v).forEach((x) => strs(x, o)); return o; };
const hits: any[] = []; let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) { total++; for (const s of strs(r.question)) for (const m of s.matchAll(RE)) { const i = m.index!; hits.push({ id: r.id, tok: m[1], unit: (m[2] ?? "").replace(/<.*/, ""), ctx: s.slice(Math.max(0, i - 40), i + m[0].length + 25).replace(/\s+/g, " ") }); } }
  from += 1000;
}
fs.writeFileSync(`scripts/logs/quet-mu-dinh-lien-${Date.now()}.json`, JSON.stringify(hits));
console.log(`Quét ${total} câu · ${new Set(hits.map((h) => h.id)).size} câu · ${hits.length} chỗ`);
const g: Record<string, number> = {}; for (const h of hits) g[h.unit || "(rỗng)"] = (g[h.unit || "(rỗng)"] ?? 0) + 1;
console.log(Object.entries(g).sort((a, b) => b[1] - a[1]).slice(0, 60).map(([k, v]) => `${k}:${v}`).join("  "));
