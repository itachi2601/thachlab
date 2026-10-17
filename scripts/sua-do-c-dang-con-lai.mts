// Sửa các dạng độ C còn sót sau sua-do-c-mat-dau-do.mts: "27^0C" -> "27^\circ C", "27 0C" -> "27°C", "50C" (một chữ số + 0C) -> "5°C" khi có ngữ cảnh nhiệt độ.
// Mặc định DRY-RUN; --apply ghi thật, sao lưu ra scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const APPLY = process.argv.includes("--apply");
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const CARET = /(?<![\d.,A-Za-z^_{])([-−–‒]?\d{1,4}(?:[.,]\d+)?)\^\{?0\}?\s?C(?![A-Za-z0-9])/g; // 27^0C (trong $…$)
const SPACED = /(?<![\d.,A-Za-z^_{])([-−–‒]?\d{1,4}(?:[.,]\d+)?) 0C(?![A-Za-z0-9])/g; // 27 0C
const ONE = /(?<![\d.,A-Za-z^_{])([-−–‒]?\d)0C(?![A-Za-z0-9])/g; // 50C = 5°C
const TEMP = /nhiệt độ|nhiệt|sôi|đá|nóng|lạnh|đun|celsius|tăng thêm|giảm|Δt|\\Delta t/i;
const ELEC = /culông|coulomb|tụ điện|μ|µ|\\mu|điện tích|\bnC\b/i;
const strs = (v: unknown, o: string[] = []): string[] => { if (typeof v === "string") o.push(v); else if (Array.isArray(v)) v.forEach((x) => strs(x, o)); else if (v && typeof v === "object") Object.values(v).forEach((x) => strs(x, o)); return o; };
const fixed: any[] = [], backup: any[] = [], doubtful: any[] = [];
let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    total++;
    const all = strs(r.question).join(" \n ");
    const hasC = CARET.test(all) || SPACED.test(all), hasOne = ONE.test(all);
    CARET.lastIndex = SPACED.lastIndex = ONE.lastIndex = 0;
    if (!hasC && !hasOne) continue;
    const ctx = all;
    const tempOk = TEMP.test(ctx) && !ELEC.test(ctx);
    if (!tempOk && !hasC) { doubtful.push({ id: r.id, sample: all.match(ONE)?.slice(0, 3) }); continue; }
    let js = JSON.stringify(r.question);
    // JSON.stringify nhân đôi dấu \ nên "\\circ"
    js = js.replace(CARET, (_m, n: string) => `${n}^\\\\circ C`).replace(SPACED, (_m, n: string) => `${n}°C`);
    if (tempOk) js = js.replace(ONE, (_m, n: string) => `${n}°C`);
    if (js === JSON.stringify(r.question)) continue;
    fixed.push({ id: r.id, sample: [...all.matchAll(CARET), ...all.matchAll(SPACED), ...(tempOk ? all.matchAll(ONE) : [])].slice(0, 4).map((m) => m[0]) });
    backup.push({ id: r.id, question: r.question });
    if (APPLY) {
      const { error: e2 } = await sb.from("question_bank").update({ question: JSON.parse(js) }).eq("id", r.id);
      if (e2) console.log(r.id, "LỖI", e2.message);
    }
  }
  from += 1000;
}
const ts = Date.now();
fs.writeFileSync(`scripts/logs/do-c-con-lai-${APPLY ? "apply" : "dry"}-${ts}.json`, JSON.stringify({ fixed, doubtful }, null, 2));
if (APPLY) fs.writeFileSync(`scripts/logs/backup-do-c-con-lai-${ts}.json`, JSON.stringify(backup));
console.log(`${APPLY ? "ĐÃ GHI" : "DRY-RUN"}: quét ${total} · sửa ${fixed.length} · nghi ngờ ${doubtful.length} · ts=${ts}`);
for (const f of fixed.slice(0, 25)) console.log(f.id, f.sample.join(" | "));
