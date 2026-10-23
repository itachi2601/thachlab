// Đối chiếu chấm điểm server (migration 20261024150000_exam_answer_server_grading) với điểm đã lưu — CHỈ ĐỌC.
//
// Lấy N bài làm gần nhất trong exam_results (có detail.responses), chấm lại 3 cách rồi in số lệch:
//   (1) TS  = gradeExam/gradeQuestion trong features/exams/types.ts (đúng code client đang chấm)
//   (2) SQL = public.exam_grade_responses(exams.questions, detail.responses) trên DB (nếu migration đã chạy)
//   (3) đã lưu = exam_results.score + exam_question_results.earned/max
// TS ≠ SQL  → lỗi port, PHẢI = 0 trước khi đi chặng 2/3.
// TS ≠ đã lưu → thường do đề bị sửa sau khi em nộp, hoặc client cũ — liệt kê để xem, không phải lỗi port.
//
//   npx tsx scripts/doi-chieu-cham-diem-exam.mts            # 500 bài gần nhất
//   npx tsx scripts/doi-chieu-cham-diem-exam.mts 2000
//
// Không dùng service-role key: đọc qua `supabase db query --linked` (CLI đã login + link trên Mac của Thạch), chỉ SELECT.
// Kết quả lệch (chỉ id bài làm / id đề, không có tên HS) ghi ra scripts/logs/doi-chieu-cham-diem-<thời điểm>.json.

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { gradeExam, gradeQuestion, type ExamQuestion, type QuestionResponse } from "../features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LOG_DIR = path.join(scriptDir, "logs");
const N = Math.max(200, Number(process.argv[2]) || 500);
const EPS = 1e-9;

type Row = Record<string, unknown>;

function query(sql: string): Row[] {
  const f = path.join(os.tmpdir(), `doichieu-${process.pid}-${Math.random().toString(36).slice(2)}.sql`);
  fs.writeFileSync(f, sql);
  try {
    const out = execFileSync("supabase", ["db", "query", "--linked", "-f", f, "-o", "json"], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: 512 * 1024 * 1024,
    });
    // CLI cũ trả {rows:[…]}, CLI mới (≥2.117) trả thẳng mảng […]
    const a = out.indexOf("["), o = out.indexOf("{");
    if (a !== -1 && (o === -1 || a < o)) return JSON.parse(out.slice(a, out.lastIndexOf("]") + 1));
    return JSON.parse(out.slice(o, out.lastIndexOf("}") + 1)).rows;
  } catch (e) {
    const err = e as { stderr?: string; message: string };
    throw new Error((err.stderr || err.message).slice(0, 2000));
  } finally {
    fs.unlinkSync(f);
  }
}
// CLI có thể trả jsonb dạng chuỗi
const js = <T,>(v: unknown): T => (typeof v === "string" ? (JSON.parse(v) as T) : (v as T));
const num = (v: unknown) => (v === null || v === undefined ? null : Number(v));

const hasFn = js<boolean>(
  query("select to_regprocedure('public.exam_grade_responses(jsonb,jsonb)') is not null as ok;")[0]?.ok,
);
if (!hasFn) console.log("! Chưa có public.exam_grade_responses trên DB (migration chưa chạy) — chỉ so TS với điểm đã lưu.");

console.log(`Lấy ${N} bài làm gần nhất…`);
const results = query(`
  select er.id, er.exam_id, er.score::float8 as score, er.detail -> 'responses' as resp,
         coalesce((er.detail ->> 'graded_by_server')::boolean, false) as srv
         ${hasFn ? ", public.exam_grade_responses(e.questions, er.detail -> 'responses') as g" : ""}
  from public.exam_results er join public.exams e on e.id = er.exam_id
  where jsonb_typeof(er.detail -> 'responses') = 'array'
  order by er.id desc limit ${N};`);
if (results.length === 0) {
  console.log("Không có bài làm nào có detail.responses.");
  process.exit(0);
}

const examIds = [...new Set(results.map((r) => Number(r.exam_id)))];
const questionsByExam = new Map<number, ExamQuestion[]>();
for (let i = 0; i < examIds.length; i += 20) {
  const chunk = examIds.slice(i, i + 20);
  for (const r of query(`select id, questions from public.exams where id in (${chunk.join(",")});`)) {
    questionsByExam.set(Number(r.id), js<ExamQuestion[]>(r.questions) ?? []);
  }
}

const resultIds = results.map((r) => Number(r.id));
const eqrByResult = new Map<number, Map<number, { earned: number; max: number }>>();
for (let i = 0; i < resultIds.length; i += 500) {
  const chunk = resultIds.slice(i, i + 500);
  for (const r of query(
    `select exam_result_id, question_index, earned::float8 as earned, max::float8 as max
     from public.exam_question_results where exam_result_id in (${chunk.join(",")});`,
  )) {
    const id = Number(r.exam_result_id);
    if (!eqrByResult.has(id)) eqrByResult.set(id, new Map());
    eqrByResult.get(id)!.set(Number(r.question_index), { earned: Number(r.earned), max: Number(r.max) });
  }
}

type Diff = Record<string, unknown>;
const portExam: Diff[] = [];
const portQuestion: Diff[] = [];
const storedScore: Diff[] = [];
const storedQuestion: Diff[] = [];
let nQuestions = 0;
let crashed = 0;

for (const r of results) {
  const id = Number(r.id);
  const examId = Number(r.exam_id);
  const qs = questionsByExam.get(examId) ?? [];
  const resp = js<QuestionResponse[]>(r.resp) ?? [];
  let ts: ReturnType<typeof gradeExam>;
  try {
    ts = gradeExam(qs, resp);
  } catch {
    crashed += 1; // client cũng văng ở đề này (dữ liệu câu hỏi hỏng) — bỏ qua
    continue;
  }
  const stored = num(r.score);
  if (stored === null || Math.abs(stored - ts.score10) > 0.005 + EPS) {
    storedScore.push({ result_id: id, exam_id: examId, stored, ts: ts.score10, graded_by_server: r.srv });
  }

  const g = hasFn
    ? js<{ score10: number; correct_count: number; per_question: { earned: number; max: number }[] }>(r.g)
    : null;
  if (g && (Math.abs(g.score10 - ts.score10) > EPS || g.correct_count !== ts.correctCount)) {
    portExam.push({ result_id: id, exam_id: examId, ts: ts.score10, sql: g.score10, ts_cc: ts.correctCount, sql_cc: g.correct_count });
  }

  const eqr = eqrByResult.get(id);
  qs.forEach((q, i) => {
    nQuestions += 1;
    const t = gradeQuestion(q, resp[i]);
    const p = g?.per_question?.[i];
    if (p && (Math.abs(p.earned - t.earned) > EPS || Math.abs(p.max - t.max) > EPS)) {
      portQuestion.push({ result_id: id, exam_id: examId, index: i, type: q.type, response: resp[i] ?? null, ts: t, sql: p });
    }
    const s = eqr?.get(i);
    if (s && (Math.abs(s.earned - t.earned) > 0.005 + EPS || Math.abs(s.max - t.max) > 0.005 + EPS)) {
      storedQuestion.push({ result_id: id, exam_id: examId, index: i, type: q.type, stored: s, ts: t });
    }
  });
}

console.log("");
console.log(`Bài làm: ${results.length} (${examIds.length} đề, ${nQuestions} câu)${crashed ? ` · ${crashed} bài đề hỏng, bỏ qua` : ""}`);
if (hasFn) {
  console.log(`(1≠2) Lỗi port TS ≠ SQL — điểm bài: ${portExam.length} · từng câu: ${portQuestion.length}   ← phải = 0`);
} else {
  console.log("(1≠2) Lỗi port: chưa kiểm được (migration chưa chạy)");
}
console.log(`(1≠3) TS ≠ đã lưu — điểm bài: ${storedScore.length} · từng câu (exam_question_results): ${storedQuestion.length}`);
const byType = new Map<string, number>();
for (const d of portQuestion) byType.set(String(d.type), (byType.get(String(d.type)) ?? 0) + 1);
if (byType.size) console.log("   Lỗi port theo dạng câu:", Object.fromEntries(byType));
const storedByExam = new Map<number, number>();
for (const d of storedScore) storedByExam.set(Number(d.exam_id), (storedByExam.get(Number(d.exam_id)) ?? 0) + 1);
if (storedByExam.size) {
  const top = [...storedByExam.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10);
  console.log("   Đề có nhiều bài lệch điểm đã lưu nhất (thường là đề đã sửa sau khi nộp):",
    top.map(([e, n]) => `đề ${e}: ${n}`).join(", "));
}
for (const d of portQuestion.slice(0, 10)) console.log("   PORT", JSON.stringify(d));

fs.mkdirSync(LOG_DIR, { recursive: true });
const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
const out = path.join(LOG_DIR, `doi-chieu-cham-diem-${stamp}.json`);
fs.writeFileSync(out, JSON.stringify({ n: results.length, hasFn, portExam, portQuestion, storedScore, storedQuestion }, null, 1));
console.log(`\nChi tiết: ${path.relative(path.resolve(scriptDir, ".."), out)}`);
process.exit(hasFn && (portExam.length || portQuestion.length) ? 1 : 0);
