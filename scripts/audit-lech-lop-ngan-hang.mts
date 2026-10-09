// Rà ngân hàng câu hỏi tìm câu lớp 11 bị lẫn vào lớp 10 (CHỈ ĐỌC, không ghi DB).
//
//   npx tsx scripts/audit-lech-lop-ngan-hang.mts            # lớp đang kiểm = 10, so với 11
//   npx tsx scripts/audit-lech-lop-ngan-hang.mts 11 10      # chiều ngược lại
//
// Ra scripts/logs/lech-lop-<ngày>.csv với 3 loại nghi ngờ:
//   TOPIC_LECH  — grade của câu khác grade của chủ đề (question_topics) mà câu gắn vào
//   TU_KHOA     — nội dung câu chứa từ khoá đặc trưng lớp kia (gợi ý, cần xem tay)
//   CUNG_DE     — câu lớp kia nằm trong đề nguồn mà phần lớn câu thuộc lớp đang kiểm
// Cần SUPABASE_SERVICE_ROLE_KEY trong env hoặc .env.local (không hỏi, thiếu thì dừng).

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { questionTextForAi } from "@/services/exam-question-text";
import type { ExamQuestion } from "@/features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const gradeOf = (s: string | null | undefined) => (s ?? "").match(/\d+/)?.[0] ?? "";
const TARGET = process.argv[2] ?? "10"; // lớp đang kiểm
const OTHER = process.argv[3] ?? "11"; // lớp nghi bị lẫn vào

// Từ khoá đặc trưng — chỉ là gợi ý. Tránh từ có ở cả hai lớp (chuyển động tròn đều, lực...).
const KEYWORDS: Record<string, RegExp> = {
  "11": /dao động điều hòa|dao động điều hoà|con lắc|phương trình dao động|li độ|tần số góc|sóng cơ|bước sóng|sóng dừng|giao thoa|điện tích điểm|định luật cu-?lông|cường độ điện trường|điện thế|tụ điện|hiệu điện thế|dòng điện|cường độ dòng điện|điện trở|suất điện động/i,
  "10": /chuyển động thẳng|gia tốc|rơi tự do|ném ngang|ném xiên|định luật (I|II|III|1|2|3)\b.*newton|lực ma sát|momen lực|công suất|động năng|thế năng|cơ năng|động lượng|va chạm|chuyển động tròn đều|lực hướng tâm|biến dạng|định luật hooke/i,
};

function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line?.slice(key.length + 1).trim().replace(/^["']|["']$/g, "");
}

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
  process.exit(1);
}
const sb = createClient(url, key, { auth: { persistSession: false } });

type Row = {
  id: number; grade: string; topic_id: number | null; topic_name: string | null;
  source_exam_id: number | null; source_index: number | null; archived: boolean; question: unknown;
};

const rows: Row[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb
    .from("question_bank")
    .select("id, grade, topic_id, topic_name, source_exam_id, source_index, archived, question")
    .order("id")
    .range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  rows.push(...(data as Row[]));
  if (!data || data.length < 1000) break;
}
const { data: topics, error: tErr } = await sb.from("question_topics").select("id, grade, name");
if (tErr) { console.error(tErr.message); process.exit(1); }
const topicGrade = new Map((topics ?? []).map((t) => [t.id as number, gradeOf(t.grade as string)]));

const dist: Record<string, number> = {};
for (const r of rows) dist[r.grade || "(trống)"] = (dist[r.grade || "(trống)"] ?? 0) + 1;
console.log(`Tổng ${rows.length} câu. Phân bố grade:`, dist);

// Tỉ lệ lớp theo đề nguồn
const byExam = new Map<number, Record<string, number>>();
for (const r of rows) {
  if (r.source_exam_id == null) continue;
  const m = byExam.get(r.source_exam_id) ?? {};
  m[gradeOf(r.grade)] = (m[gradeOf(r.grade)] ?? 0) + 1;
  byExam.set(r.source_exam_id, m);
}

const esc = (s: string) => `"${s.replace(/"/g, '""').replace(/\s+/g, " ").slice(0, 160)}"`;
const out = ["loai,id,grade_cau,grade_chu_de,chu_de,de_nguon,cau_so,archived,ghi_chu,trich"];
const kwRe = KEYWORDS[OTHER];

for (const r of rows) {
  const g = gradeOf(r.grade);
  const tg = r.topic_id != null ? topicGrade.get(r.topic_id) ?? "" : "";
  let text = "";
  try { text = questionTextForAi(r.question as ExamQuestion); } catch { /* câu lỗi định dạng */ }
  const add = (loai: string, note: string) =>
    out.push([loai, r.id, g, tg, esc(r.topic_name ?? ""), r.source_exam_id ?? "", r.source_index ?? "", r.archived, esc(note), esc(text)].join(","));

  if (g === TARGET && tg === OTHER) add("TOPIC_LECH", `câu lớp ${TARGET} nhưng chủ đề lớp ${OTHER}`);
  if (g === OTHER && tg === TARGET) add("TOPIC_LECH", `câu lớp ${OTHER} nhưng chủ đề lớp ${TARGET}`);
  if (g === TARGET && kwRe && kwRe.test(text)) add("TU_KHOA", `có từ khoá lớp ${OTHER}: ${text.match(kwRe)?.[0]}`);
  if (g === OTHER && r.source_exam_id != null) {
    const m = byExam.get(r.source_exam_id) ?? {};
    const total = Object.values(m).reduce((a, b) => a + b, 0);
    if (total >= 5 && (m[TARGET] ?? 0) / total >= 0.7) add("CUNG_DE", `đề ${r.source_exam_id}: ${m[TARGET]}/${total} câu lớp ${TARGET}`);
  }
}

fs.mkdirSync(path.resolve(scriptDir, "logs"), { recursive: true });
const file = path.resolve(scriptDir, "logs", `lech-lop-${new Date().toISOString().slice(0, 10)}.csv`);
fs.writeFileSync(file, "﻿" + out.join("\n"));
const count = (t: string) => out.filter((l) => l.startsWith(t + ",")).length;
console.log(`TOPIC_LECH ${count("TOPIC_LECH")} · TU_KHOA ${count("TU_KHOA")} · CUNG_DE ${count("CUNG_DE")}\n→ ${file}`);
