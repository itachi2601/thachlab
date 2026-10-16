// Sửa áp suất mất mũ: "105 Pa" → 10^5 Pa, "106Pa" → 10^6 Pa, "104 N/m3"… (cùng bộ lọc với scripts/quet-ap-suat-mu.mts). Sao lưu ra scripts/logs/.
//   npx tsx scripts/sua-ap-suat-mu.mts          # DRY-RUN
//   npx tsx scripts/sua-ap-suat-mu.mts --apply
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const SKIP = new Set([444978]); // "giảm xuống còn 107 Pa": không rõ 10^7 hay 10^-7 → đưa thầy duyệt
const RE = /(?<![\d.,^{_A-Za-z])(10[3-9])((?:\s|\\,|\\ |&nbsp;)*(?:Pa|pa|PA|N\/m(?:<sup>2<\/sup>|\^?2|²)?)(?![A-Za-z]))/g;
const ZONE = /\$\$[\s\S]*?\$\$|\$[^$]*\$|<[^>]*>/g;
function fix(s: string, log: string[]): string {
  const z = [...s.matchAll(ZONE)].map((m) => ({ a: m.index!, b: m.index! + m[0].length, tag: m[0].startsWith("<") }));
  return s.replace(RE, (m, tok: string, rest: string, off: number) => {
    const zone = z.find((x) => off >= x.a && off < x.b);
    if (zone?.tag) return m;
    const e = tok.slice(2);
    const r = zone ? `10^{${e}}${rest}` : `10<sup>${e}</sup>${rest}`;
    log.push(s.slice(Math.max(0, off - 25), off + m.length + 8).replace(/\s+/g, " ") + "  =>  " + r);
    return r;
  });
}
const map = (v: any, f: (s: string) => string): any => typeof v === "string" ? f(v) : Array.isArray(v) ? v.map((x) => map(x, f)) : v && typeof v === "object" ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, map(x, f)])) : v;
const backup: any[] = [], log: string[] = []; let from = 0, n = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    if (SKIP.has(r.id)) continue;
    const l: string[] = []; const nq = map(r.question, (s) => fix(s, l));
    if (!l.length) continue;
    log.push(...l.map((x) => `${r.id} ${x}`)); n++;
    backup.push({ id: r.id, question: r.question });
    if (APPLY) { fs.writeFileSync(`scripts/logs/backup-ap-suat-mu-${(globalThis as any).__t ??= Date.now()}.json`, JSON.stringify(backup)); const { error: e2 } = await sb.from("question_bank").update({ question: nq }).eq("id", r.id); if (e2) { console.error(r.id, e2.message); process.exit(1); } }
  }
  from += 1000;
}
fs.writeFileSync(`scripts/logs/sua-ap-suat-mu-${APPLY ? "apply" : "dry"}-${Date.now()}.log`, log.join("\n"));
console.log(APPLY ? "ĐÃ GHI" : "DRY-RUN", "· câu đổi", n, "· chỗ", log.length);
if (!APPLY) console.log(log.filter((_, i) => i % 6 === 0).join("\n"));
