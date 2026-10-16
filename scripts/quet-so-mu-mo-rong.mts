// Quét MỞ RỘNG số mũ mất ^ trong question_bank — CHỈ ĐỌC. Bắt cả "a.108", "k.109", "3.108", "2,5.10-5" (hệ số là chữ cái cũng tính).
//   npx tsx scripts/quet-so-mu-mo-rong.mts
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
// hệ số (số/chữ/ngoặc đóng) + dấu nhân + 10 + số mũ 1–2 chữ số (có thể âm), không phải 10^, 10_, 10{ ; số mũ KHÔNG toàn số 0 (loại ×100, ×1000)
const RE = /(?<![\d.,])([A-Za-zα-ω\d)\]}][ \s]?)(?:[.·×*]|\\cdot|\\times)\s*10([-−–]?[1-9]\d?)(?![\d^_{])(?!\s*(?:[.,]\d))/g;
const strings = (v: unknown, o: string[] = []): string[] => { if (typeof v === "string") o.push(v); else if (Array.isArray(v)) v.forEach((x) => strings(x, o)); else if (v && typeof v === "object") Object.values(v).forEach((x) => strings(x, o)); return o; };
const hits: any[] = []; let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, grade, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) { total++; for (const s of strings(r.question)) for (const m of s.matchAll(RE)) { const i = m.index!; hits.push({ id: r.id, grade: r.grade, exp: m[2], ctx: s.slice(Math.max(0, i - 25), i + m[0].length + 20).replace(/\s+/g, " ") }); } }
  from += 1000;
}
const f = path.join(scriptDir, "logs", `quet-so-mu-mo-rong-${Date.now()}.json`);
fs.writeFileSync(f, JSON.stringify(hits, null, 2));
const ids = new Set(hits.map((h) => h.id));
console.log(`Quét ${total} câu · ${ids.size} câu · ${hits.length} chỗ →`, path.relative(process.cwd(), f));
const byExp: Record<string, number> = {}; hits.forEach((h) => (byExp[h.exp] = (byExp[h.exp] ?? 0) + 1)); console.log(byExp);
for (const h of hits.slice(0, 60)) console.log(h.id, h.exp, "|", h.ctx);
