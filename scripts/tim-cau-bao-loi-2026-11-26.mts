// Chỉ ĐỌC: tìm câu báo lỗi #171/#172 (26/11/2026) trong question_bank lớp 12 + mọi exams có chứa.
import { createClient } from "@supabase/supabase-js";
import { readFileSync, writeFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const tests: [string, (s: string) => boolean][] = [
  ["172-charles-khong-dung", (s) => /không đúng với/.test(s) && /Charles|đẳng áp/i.test(s) && /\\\\frac\{V\}\{T\}|V\/T/.test(s)],
  ["171-nut-chai", (s) => /nút/.test(s) && /330/.test(s)],
  ["176-p2", (s) => /p_2\s*=\s*4/.test(s) || /4\\\\cdot\s*10\^5|4\.10\^5|4\.10\^\{5\}/.test(s) && /van/.test(s)],
  ["174-6,68", (s) => /6,68|6\{,\}68/.test(s) && /0,2 kg|200 g/.test(s)],
];
const found: Record<string, any[]> = {};
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("question_bank").select("id,grade,topic_name,archived,content_hash,question").range(from, from + 999);
  if (error) { console.log(error.message); break; }
  if (!data?.length) break;
  for (const q of data) { const s = JSON.stringify(q.question); for (const [k, t] of tests) if (t(s)) (found[k] ??= []).push(q); }
}
for (const [k, arr] of Object.entries(found)) {
  console.log("==", k, arr.length);
  for (const q of arr) console.log(" bank", q.id, q.grade, q.topic_name, "archived", q.archived, JSON.stringify(q.question).slice(0, 300));
}
writeFileSync("scripts/logs/bao-loi-1126/tim-bank.json", JSON.stringify(found, null, 1));
// exams chứa
for (let from = 0; ; from += 200) {
  const { data, error } = await sb.from("exams").select("id,title,questions").range(from, from + 199);
  if (error) { console.log(error.message); break; }
  if (!data?.length) break;
  for (const e of data) (e.questions as any[] ?? []).forEach((q, i) => { const s = JSON.stringify(q); for (const [k, t] of tests) if (t(s)) console.log(" exam", k, e.id, e.title, "idx", i); });
}
