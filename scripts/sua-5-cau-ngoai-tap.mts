// Sửa tay 4/5 câu lệch đáp án ngoài tập giải lại (thầy chốt 18/10/2026): đề 35#10→A, 133#14→B (bản sao đề); ngân hàng của đề 140#8→D, 544#25→"-1,2".
// Đề 73#2 để thầy quyết. Sao lưu trước khi ghi. dry-run mặc định; --apply ghi.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const lech: any[] = JSON.parse(fs.readFileSync("scripts/data/giai-lai/lech-exams-ds.json", "utf8"));
const tim = (exam: number, stt: number) => lech.find((x) => x.exam === exam && x.stt === stt)!;
const viecDe: any[] = [{ exam: 182, stt: 8, mc: 3 }, { exam: 564, stt: 20, sa: "-1,2" }]; // 182/564 = bản sao đề của 140#8/544#25, lộ ra sau khi sửa ngân hàng
const viecBank: any[] = []; // đã sửa ở lượt trước (ngân hàng 429306, 1500185)
const sao: any = { exams: [], bank: [] }; const lam: (() => Promise<void>)[] = [];
for (const v of viecDe) {
  const { data } = await sb.from("exams").select("id,questions").eq("id", v.exam).single();
  const qs = structuredClone(data!.questions); const q = qs[v.stt - 1];
  console.log(`đề ${v.exam}#${v.stt}: answer ${q.answer} → ${v.mc ?? v.sa}  | ${String(q.question).replace(/<[^>]+>/g, "").slice(0, 60)}`);
  sao.exams.push({ id: v.exam, questions: data!.questions }); q.answer = v.mc ?? v.sa;
  lam.push(async () => { const { error } = await sb.from("exams").update({ questions: qs }).eq("id", v.exam); console.log(`  đề ${v.exam}`, error ? "LỖI " + error.message : "ok"); });
}
for (const v of viecBank) {
  const ids: number[] = tim(v.exam, v.stt).bankIds;
  const { data } = await sb.from("question_bank").select("id,question").in("id", ids);
  for (const r of data!) {
    const q = structuredClone(r.question);
    console.log(`ngân hàng ${r.id} (đề ${v.exam}#${v.stt}): answer ${q.answer} → ${v.mc ?? v.sa}`);
    sao.bank.push({ id: r.id, question: r.question }); q.answer = v.mc ?? v.sa;
    lam.push(async () => { const { error } = await sb.from("question_bank").update({ question: q }).eq("id", r.id); console.log(`  bank ${r.id}`, error ? "LỖI " + error.message : "ok"); });
  }
}
if (!APPLY) { console.log("dry-run xong — thêm --apply"); process.exit(0); }
const bp = `scripts/logs/sua-5-cau-ngoai-tap-backup-${Date.now()}.json`; fs.writeFileSync(bp, JSON.stringify(sao)); console.log("sao lưu:", bp);
for (const f of lam) await f();
