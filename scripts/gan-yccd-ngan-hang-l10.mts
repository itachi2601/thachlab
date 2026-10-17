// Gán YCCĐ (topic) cho câu của các đề "Kiểm tra nhanh" lớp 10 đã đăng, theo bảng thầy đã duyệt
// (scripts/data/duyet/gan-yccd-l10/de-xuat.json: {lesson_id, i, topic_id, topic, conf}; topic_id null = giữ nguyên).
//
//   npx tsx scripts/gan-yccd-ngan-hang-l10.mts            # DRY-RUN: chỉ in kế hoạch + kiểm đề khớp file
//   npx tsx scripts/gan-yccd-ngan-hang-l10.mts --apply    # sao lưu → sinh scripts/logs/gan-yccd-l10-<giờ>.sql (chạy bằng supabase db query)
//   npx tsx scripts/gan-yccd-ngan-hang-l10.mts --verify   # sau khi chạy SQL: kiểm lại đề + ngân hàng
//   npx tsx scripts/gan-yccd-ngan-hang-l10.mts --undo scripts/logs/<file sao lưu>
//
// Cách ghi: chỉ đổi trường `topic` của từng câu trong exams.questions (hash câu bỏ qua `topic` nên không sinh
// dòng ngân hàng trùng); trigger trg_exams_sync_bank tự cập nhật question_bank.topic_id/topic_name theo TÊN topic.
// Bài → đề: exam_id = lesson_id + 895 (kiểm lại bằng tiêu đề đề trước khi ghi).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const envFile = fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n");
const env = (k: string) => envFile.find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });

const args = process.argv.slice(2);
const apply = args.includes("--apply");
const verify = args.includes("--verify");
const undoFile = args.includes("--undo") ? args[args.indexOf("--undo") + 1] : null;

type Row = { lesson_id: number; i: number; topic_id: number | null; topic: string | null; conf: string };
type Q = Record<string, unknown> & { question?: string; topic?: string };

async function loadExam(id: number) {
  const { data, error } = await sb.from("exams").select("id, title, questions").eq("id", id).single();
  if (error) throw new Error(`đọc đề ${id}: ${error.message}`);
  return data as { id: number; title: string; questions: Q[] };
}

if (undoFile) {
  const bk = JSON.parse(fs.readFileSync(path.resolve(root, undoFile), "utf8")) as {
    exams: { id: number; questions: Q[] }[];
    bank: { id: number; topic_id: number | null; topic_name: string }[];
  };
  for (const e of bk.exams) {
    const { error } = await sb.from("exams").update({ questions: e.questions }).eq("id", e.id);
    if (error) throw new Error(`hoàn tác đề ${e.id}: ${error.message}`);
  }
  // trigger chỉ ghi topic_id mới khi khác null → trả topic_id/topic_name cũ trực tiếp
  for (const b of bk.bank) {
    const { error } = await sb.from("question_bank").update({ topic_id: b.topic_id, topic_name: b.topic_name }).eq("id", b.id);
    if (error) throw new Error(`hoàn tác bank ${b.id}: ${error.message}`);
  }
  console.log(`✓ Đã hoàn tác ${bk.exams.length} đề, ${bk.bank.length} dòng ngân hàng`);
  process.exit(0);
}

const rows: Row[] = JSON.parse(fs.readFileSync(path.join(root, "scripts/data/duyet/gan-yccd-l10/de-xuat.json"), "utf8"));
const lessons = [...new Set(rows.map((r) => r.lesson_id))].sort((a, b) => a - b);
const plan: { examId: number; lessonId: number; changes: { i: number; from: string; to: string; topic_id: number; conf: string }[] }[] = [];
const problems: string[] = [];

for (const lessonId of lessons) {
  const file = JSON.parse(fs.readFileSync(path.join(root, `scripts/data/theory-quiz/${lessonId}.json`), "utf8")) as {
    lesson_title: string;
    questions: { question: string; topic: string }[];
  };
  const examId = lessonId + 895;
  const exam = await loadExam(examId);
  if (!exam.title.includes(file.lesson_title)) problems.push(`đề ${examId}: tiêu đề "${exam.title}" không chứa "${file.lesson_title}"`);
  if (exam.questions.length !== file.questions.length) problems.push(`đề ${examId}: ${exam.questions.length} câu ≠ file ${file.questions.length}`);
  const changes: (typeof plan)[number]["changes"] = [];
  for (const r of rows.filter((x) => x.lesson_id === lessonId)) {
    if (!r.topic_id || !r.topic) continue; // NONE: giữ nguyên
    const q = exam.questions[r.i];
    if (!q) { problems.push(`đề ${examId} câu ${r.i}: không tồn tại`); continue; }
    if (q.question !== file.questions[r.i]?.question) problems.push(`đề ${examId} câu ${r.i}: nội dung lệch file nguồn`);
    if (!verify && q.topic !== file.lesson_title) problems.push(`đề ${examId} câu ${r.i}: topic hiện tại "${q.topic}" ≠ tên bài (đã đổi?)`);
    changes.push({ i: r.i, from: String(q.topic ?? ""), to: r.topic, topic_id: r.topic_id, conf: r.conf });
  }
  plan.push({ examId, lessonId, changes });
}

console.log(verify ? "=== VERIFY ===" : apply ? "=== APPLY ===" : "=== DRY-RUN ===");
for (const p of plan) console.log(`đề ${p.examId} (bài ${p.lessonId}): đổi topic ${p.changes.length} câu`);
const total = plan.reduce((s, p) => s + p.changes.length, 0);
console.log(`Tổng ${total} câu sẽ đổi; ${rows.filter((r) => !r.topic_id).length} câu NONE giữ nguyên.`);
if (problems.length) {
  console.log("\n✗ VẤN ĐỀ (dừng, không ghi):");
  problems.forEach((m) => console.log("  -", m));
  process.exit(1);
}
if (verify) {
  const examIdsV = plan.map((p) => p.examId);
  const bks = fs.readdirSync(path.join(root, "scripts/logs")).filter((f) => f.startsWith("sao-luu-gan-yccd-l10-")).sort();
  const bkLatest = bks.length ? `scripts/logs/${bks[bks.length - 1]}` : null;
  const before = bkLatest ? (JSON.parse(fs.readFileSync(path.join(root, bkLatest), "utf8")) as { exams: { id: number; questions: Q[] }[]; bank: unknown[] }) : null;
  let bad = 0;
  for (const p of plan) {
    const e = await loadExam(p.examId);
    for (const c of p.changes) if (e.questions[c.i].topic !== c.to) { bad++; console.log(`  ✗ đề ${p.examId} câu ${c.i}: topic "${e.questions[c.i].topic}" ≠ "${c.to}"`); }
    const old = before?.exams.find((x) => x.id === p.examId);
    if (old && e.questions.length !== old.questions.length) { bad++; console.log(`  ✗ đề ${p.examId}: đổi số câu`); }
    // các trường khác của câu phải giữ nguyên (chỉ topic đổi)
    if (old) for (let i = 0; i < old.questions.length; i++) {
      const { topic: _a, ...ra } = old.questions[i] as Q; const { topic: _b, ...rb } = e.questions[i] as Q;
      if (JSON.stringify(ra) !== JSON.stringify(rb)) { bad++; console.log(`  ✗ đề ${p.examId} câu ${i}: trường khác ngoài topic bị đổi`); }
    }
  }
  const { data: bankAfter } = await sb.from("question_bank").select("id, topic_id, topic_name, source_exam_id, source_index").in("source_exam_id", examIdsV);
  const exp = new Map<string, number>();
  for (const p of plan) for (const c of p.changes) exp.set(`${p.examId}:${c.i}`, c.topic_id);
  const seen = new Set<string>();
  for (const b of bankAfter ?? []) {
    const k = `${b.source_exam_id}:${b.source_index}`; seen.add(k);
    const want = exp.get(k);
    if (want !== undefined && b.topic_id !== want) { bad++; console.log(`  ✗ bank ${b.id} (đề ${b.source_exam_id} câu ${b.source_index}): topic_id ${b.topic_id} ≠ ${want}`); }
  }
  for (const k of exp.keys()) if (!seen.has(k)) { bad++; console.log(`  ✗ thiếu dòng bank cho ${k}`); }
  const nullAfter = (bankAfter ?? []).filter((b) => b.topic_id === null).length;
  const bankBeforeN = before ? (before.bank as unknown[]).length : null;
  console.log(`Bank: ${bankAfter?.length} dòng (trước: ${bankBeforeN}); topic_id null còn ${nullAfter} (kỳ vọng ${rows.filter((r) => !r.topic_id).length}).`);
  if (bankBeforeN !== null && bankAfter?.length !== bankBeforeN) bad++;
  console.log(bad === 0 ? "✓ KIỂM LẠI ĐẠT" : `✗ KIỂM LẠI: ${bad} lỗi — hoàn tác: npx tsx scripts/gan-yccd-ngan-hang-l10.mts --undo ${bkLatest}`);
  process.exit(bad === 0 ? 0 : 1);
}
if (!apply) { console.log("\nDry-run sạch. Chạy lại với --apply để ghi."); process.exit(0); }

// ---- sao lưu ----
const examIds = plan.map((p) => p.examId);
const { data: bankBefore, error: be } = await sb.from("question_bank").select("id, topic_id, topic_name, source_exam_id, source_index").in("source_exam_id", examIds);
if (be) throw new Error(`đọc bank: ${be.message}`);
const examsBefore: { id: number; questions: Q[] }[] = [];
for (const id of examIds) { const e = await loadExam(id); examsBefore.push({ id: e.id, questions: e.questions }); }
const stamp = new Date().toISOString().replace(/[-:T]/g, "").slice(0, 12);
const bkPath = path.join(root, `scripts/logs/sao-luu-gan-yccd-l10-${stamp}.json`);
fs.writeFileSync(bkPath, JSON.stringify({ exams: examsBefore, bank: (bankBefore ?? []).map((b) => ({ id: b.id, topic_id: b.topic_id, topic_name: b.topic_name })) }));
console.log(`Đã sao lưu: ${path.relative(root, bkPath)} (${examsBefore.length} đề, ${bankBefore?.length ?? 0} dòng bank)`);

// ---- sinh SQL (REST bị statement timeout vì trigger đồng bộ ngân hàng cả đề; db query chạy được với timeout dài) ----
function sqlText(t: string) { if (t.includes("$t$")) throw new Error("topic chứa $t$"); return `$t$${t}$t$`; }
const out: string[] = ["begin;", "set local statement_timeout = '900s';"];
for (const p of plan) {
  const vals = p.changes.map((c) => `(${c.i}, ${sqlText(c.to)})`).join(", ");
  out.push(
    `update public.exams e set questions = (select jsonb_agg(case when m.topic is not null then jsonb_set(q.value, '{topic}', to_jsonb(m.topic::text)) else q.value end order by q.ordinality) ` +
      `from jsonb_array_elements(e.questions) with ordinality as q(value, ordinality) left join (values ${vals}) as m(idx, topic) on m.idx = q.ordinality - 1) where e.id = ${p.examId};`,
  );
}
out.push("commit;");
const sqlPath = path.join(root, `scripts/logs/gan-yccd-l10-${stamp}.sql`);
fs.writeFileSync(sqlPath, out.join("\n") + "\n");
console.log(`Đã sinh SQL: ${path.relative(root, sqlPath)}\nChạy: supabase db query --linked -f ${path.relative(root, sqlPath)}\nSau đó: npx tsx scripts/gan-yccd-ngan-hang-l10.mts --verify`);
process.exit(0);
