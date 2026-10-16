// Sửa "500C" -> "50°C" (độ C mất dấu độ) trong question_bank. Mặc định DRY-RUN; --apply ghi thật (sao lưu ra scripts/logs/).
// Chỉ sửa câu có ngữ cảnh nhiệt độ và KHÔNG có ngữ cảnh điện (0C có thể là culông); câu còn lại ghi ra file "nghi-ngo" cho thầy duyệt.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const APPLY = process.argv.includes("--apply");
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const RE = /(?<![\d.,A-Za-z^_{])([-−–‒]?\s?\d{2,4}(?:[.,]\d+)?)0C(?![A-Za-z0-9])/g;
const TEMP = /nhiệt|nước|khí|sôi|đá|°|\bK\b|kelvin|celsius|nóng|lạnh|đun|atm|\bPa\b|thể tích|bình|phích|ấm|kim loại|chảy|bay hơi/i;
const ELEC = /điện|tụ|culông|coulomb|μ|µ|\\mu|tích|dòng|ampe|\bvôn\b|\bnC\b/i;
const strs = (v: unknown, o: string[] = []): string[] => { if (typeof v === "string") o.push(v); else if (Array.isArray(v)) v.forEach((x) => strs(x, o)); else if (v && typeof v === "object") Object.values(v).forEach((x) => strs(x, o)); return o; };
const fixed: any[] = [], doubtful: any[] = [], backup: any[] = [];
let from = 0, total = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    total++;
    const all = strs(r.question).join(" \n ");
    const ms = [...all.matchAll(RE)];
    if (!ms.length) continue;
    const ctx = all.replace(RE, "");
    const ok = TEMP.test(ctx) && !(ELEC.test(ctx) && !/nhiệt|nước|sôi|celsius/i.test(ctx));
    const sample = ms.slice(0, 4).map((m) => m[0].trim());
    if (!ok) { doubtful.push({ id: r.id, sample, deXuat: sample.map((s) => s.replace(/0C$/, "°C")), ghiChu: ELEC.test(ctx) ? "có chữ điện, có thể là culông" : "không thấy ngữ cảnh nhiệt độ" }); continue; }
    let js = JSON.stringify(r.question);
    js = js.replace(RE, (_m, num: string) => `${num.replace(/\s+$/, "")}°C`);
    fixed.push({ id: r.id, n: ms.length, sample });
    backup.push({ id: r.id, question: r.question });
    if (APPLY) {
      const { error: e2 } = await sb.from("question_bank").update({ question: JSON.parse(js) }).eq("id", r.id);
      if (e2) console.log(r.id, "LỖI", e2.message);
    }
  }
  from += 1000;
}
const ts = Date.now();
fs.writeFileSync(`scripts/logs/do-c-sua-${APPLY ? "apply" : "dry"}-${ts}.json`, JSON.stringify(fixed, null, 2));
fs.writeFileSync(`scripts/logs/do-c-nghi-ngo-${ts}.json`, JSON.stringify(doubtful, null, 2));
if (APPLY) fs.writeFileSync(`scripts/logs/backup-do-c-${ts}.json`, JSON.stringify(backup));
console.log(`${APPLY ? "ĐÃ GHI" : "DRY-RUN"}: quét ${total} · sửa ${fixed.length} câu · nghi ngờ ${doubtful.length} câu · ts=${ts}`);
