// Ghi lời giải mới (scripts/data/giai-lai-thu/loi-giai-moi.json) vào question_bank + bản sao trong exams.questions (cùng đề nguồn, cùng nội dung câu).
//   npx tsx scripts/ap-dung-giai-lai.mts           dry-run   |   --apply  ghi thật (sao lưu ra scripts/logs/ trước)
// Chỉ đổi explanation; ngoại lệ FIX_TF: sửa đáp án ý đúng–sai đã được 2 lần giải độc lập đồng thuận.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const e = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(e("NEXT_PUBLIC_SUPABASE_URL"), e("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const FIX_TF: Record<number, { idx: number; from: boolean; to: boolean }> = { 347819: { idx: 2, from: true, to: false } };
const news = JSON.parse(fs.readFileSync("scripts/data/giai-lai-thu/loi-giai-moi.json", "utf8")) as { id: number; explanation: string }[];
const { data: rows } = await sb.from("question_bank").select("id,question,source_exam_id,source_index").in("id", news.map((n) => n.id));
const strip = (q: any) => JSON.stringify({ ...q, explanation: undefined, answer: undefined, statements: q.statements?.map((s: any) => s.text) });
const backup: any = { bank: rows, exams: [] };
const plan: any[] = [];
const edit = (q: any, id: number, ex: string) => {
  const n = structuredClone(q); n.explanation = ex;
  const f = FIX_TF[id]; if (f) { if (n.statements[f.idx].answer !== f.from) return null; n.statements[f.idx].answer = f.to; }
  return n;
};
const examCache: Record<number, any> = {};
for (const n of news) {
  const r = rows!.find((x) => x.id === n.id)!;
  const nq = edit(r.question, n.id, n.explanation);
  if (!nq) { console.log(n.id, "BỎ QUA: đáp án hiện tại không khớp kỳ vọng"); continue; }
  let exNote = "không có đề nguồn";
  let examUpd: any = null;
  if (r.source_exam_id != null) {
    const ex = examCache[r.source_exam_id] ??= (await sb.from("exams").select("id,questions").eq("id", r.source_exam_id).single()).data;
    const cur = ex?.questions?.[r.source_index];
    if (cur && strip(cur) === strip(r.question)) { examUpd = { exam: ex, idx: r.source_index, q: edit(cur, n.id, n.explanation) }; exNote = `đề ${ex.id} câu ${r.source_index}`; }
    else exNote = `đề ${r.source_exam_id}: nội dung lệch, chỉ ghi ngân hàng`;
  }
  console.log(n.id, "→ ngân hàng +", exNote, FIX_TF[n.id] ? "(+sửa đáp án)" : "");
  plan.push({ id: n.id, nq, examUpd });
}
if (!APPLY) { console.log("dry-run xong, thêm --apply để ghi"); process.exit(0); }
backup.exams = Object.values(examCache);
const bp = `scripts/logs/giai-lai-backup-${Date.now()}.json`; fs.writeFileSync(bp, JSON.stringify(backup)); console.log("sao lưu:", bp);
for (const p of plan) {
  const { error } = await sb.from("question_bank").update({ question: p.nq }).eq("id", p.id);
  if (error) { console.error(p.id, error.message); continue; }
  if (p.examUpd) { const ex = examCache[p.examUpd.exam.id]; ex.questions = ex.questions.slice(); ex.questions[p.examUpd.idx] = p.examUpd.q; }
}
for (const ex of Object.values(examCache) as any[]) {
  const touched = plan.some((p) => p.examUpd?.exam.id === ex.id); if (!touched) continue;
  const { error } = await sb.from("exams").update({ questions: ex.questions }).eq("id", ex.id);
  console.log("exams", ex.id, error ? error.message : "ok");
}
