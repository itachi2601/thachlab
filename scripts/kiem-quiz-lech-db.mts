// Chỉ ĐỌC: so bộ quiz trong file với đề đang gắn vào mục ly_thuyet trong DB (khác = DB còn bản cũ).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { readEnvLocal } from "../.claude/skills/soan-quiz-ly-thuyet/scripts/fetch-lessons.mts";
const url = readEnvLocal("NEXT_PUBLIC_SUPABASE_URL"), key = readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu key"); process.exit(1); }
const sb = createClient(url, key, { auth: { persistSession: false } });
const dir = path.resolve(import.meta.dirname, "data/theory-quiz");
const ids = fs.readdirSync(dir).filter((f) => /^\d+\.json$/.test(f)).map((f) => Number(f.slice(0, -5))).sort((a, b) => a - b);
const { data: items } = await sb.from("lesson_items").select("lesson_id, exam_ids").eq("kind", "ly_thuyet").in("lesson_id", ids);
const examIds = [...new Set((items ?? []).flatMap((i: any) => i.exam_ids ?? []))];
const { data: exams } = await sb.from("exams").select("id, questions").in("id", examIds);
const em = new Map((exams ?? []).map((e: any) => [e.id, e.questions as any[]]));
const norm = (s: unknown) => String(s ?? "").replace(/\s+/g, " ").trim();
const tally = (qs: any[]) => { const c: Record<string, number> = {}; qs.forEach((q) => (c[q.type] = (c[q.type] ?? 0) + 1)); return JSON.stringify(c); };
const lech: string[] = [];
for (const id of ids) {
  const f = JSON.parse(fs.readFileSync(path.join(dir, `${id}.json`), "utf8"));
  const it = (items ?? []).find((i: any) => i.lesson_id === id) as any;
  const eid = (it?.exam_ids ?? []).slice(-1)[0];
  const dbq = em.get(eid) ?? [];
  const same = dbq.length === f.questions.length && dbq.every((q: any, i: number) => norm(q.question) === norm(f.questions[i].question));
  if (!same) lech.push(`${id} ${f.lesson_title} | file ${f.questions.length}câu ${tally(f.questions)} | DB exam ${eid} ${dbq.length}câu ${tally(dbq)}`);
}
console.log(`Lệch ${lech.length}/${ids.length}:\n` + lech.join("\n"));
