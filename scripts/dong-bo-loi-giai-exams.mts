// Đồng bộ LỜI GIẢI từ question_bank sang bản sao trong exams.questions (khớp theo question_content_hash; hash KHÔNG gồm
// 'explanation' nên không đổi hash, không sinh câu trùng). Chỉ đổi khoá 'explanation' của phần tử; bỏ qua bank đã lưu trữ / lời giải rỗng.
// Mỗi chunk = một giao dịch: tắt trg_exams_sync_bank → update → bật lại. Đếm question_bank trước/sau (phải bằng nhau).
//   npx tsx scripts/dong-bo-loi-giai-exams.mts            # dry-run: đếm + mẫu, ghi scripts/data/gon-ngan-hang/loi-giai-exams/
//   npx tsx scripts/dong-bo-loi-giai-exams.mts --apply    # sao lưu exams bị đổi → chạy từng chunk
import { createClient } from "@supabase/supabase-js";
import { execSync } from "node:child_process";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const OUT = "scripts/data/gon-ngan-hang/loi-giai-exams/"; fs.mkdirSync(OUT, { recursive: true });
const q = (sql: string) => { fs.writeFileSync(OUT + "q.sql", sql); const raw = execSync(`supabase db query --linked -f ${OUT}q.sql -o json 2>/dev/null`, { shell: "/bin/bash", maxBuffer: 1 << 28 }).toString();
  const t = raw.trim(); const j = t.startsWith("[") ? JSON.parse(t) : JSON.parse(t.slice(t.indexOf("{"), t.lastIndexOf("}") + 1)); // CLI bản mới trả mảng trần, bản cũ {rows}
  return (Array.isArray(j) ? j : j.rows) as any[]; };
// phần tử cần đổi: (exam, idx, bank lời giải mới)
const CAND = `with b as materialized (select content_hash h, question->>'explanation' ex from public.question_bank where not archived and coalesce(question->>'explanation','') <> ''),
 el as (select ex.id exam_id, (q.ordinality-1)::int idx, q.value v, public.question_content_hash(q.value) h
        from public.exams ex, jsonb_array_elements(ex.questions) with ordinality q(value, ordinality)
        where jsonb_typeof(ex.questions)='array' and jsonb_typeof(q.value)='object' and coalesce(q.value->>'question','')<>'')
 select el.exam_id, el.idx, b.ex as moi, el.v->>'explanation' as cu from el join b on b.h = el.h where (el.v->>'explanation') is distinct from b.ex`;
const bankTruoc = (await sb.from("question_bank").select("id", { count: "exact", head: true })).count;
const rows = q(CAND);
const exams = [...new Set(rows.map((r) => r.exam_id))].sort((a, b) => a - b);
console.log({ bankTruoc, phanTuCanDoi: rows.length, deCanDoi: exams.length, cuRong: rows.filter((r) => !r.cu).length });
const step = Math.max(1, Math.floor(rows.length / 4));
for (const r of rows.filter((_, i) => i % step === 0).slice(0, 4)) console.log("== đề", r.exam_id, "#", r.idx + 1, "\nCŨ :", String(r.cu ?? "").slice(0, 200), "\nMỚI:", String(r.moi).slice(0, 300));
fs.writeFileSync(OUT + "ke-hoach.json", JSON.stringify(rows.map((r) => ({ e: r.exam_id, i: r.idx })), null, 0));
if (!APPLY) process.exit(0);
// sao lưu nguyên văn các đề bị đổi
const bk: any[] = [];
for (let f = 0; f < exams.length; f += 50) { const { data, error } = await sb.from("exams").select("id,questions").in("id", exams.slice(f, f + 50)); if (error) throw error; bk.push(...data!); }
const bp = `scripts/logs/dong-bo-loi-giai-exams-backup-${Date.now()}.json`; fs.writeFileSync(bp, JSON.stringify(bk)); console.log("sao lưu", bp, bk.length, "đề");
const upd = (ids: number[]) => `begin;
alter table public.exams disable trigger trg_exams_sync_bank;
update public.exams e set questions = (
  select jsonb_agg(case when b.ex is not null and (q.value->>'explanation') is distinct from b.ex then jsonb_set(q.value, '{explanation}', to_jsonb(b.ex)) else q.value end order by q.ordinality)
  from jsonb_array_elements(e.questions) with ordinality q(value, ordinality)
  left join lateral (select question->>'explanation' ex from public.question_bank
     where not archived and coalesce(question->>'explanation','') <> '' and content_hash = case when jsonb_typeof(q.value)='object' then public.question_content_hash(q.value) end limit 1) b on true)
where e.id in (${ids.join(",")}) and jsonb_typeof(e.questions)='array';
alter table public.exams enable trigger trg_exams_sync_bank;
commit;`;
let n = 0;
for (let f = 0; f < exams.length; f += 40, n++) { fs.writeFileSync(OUT + `chunk-${n}.sql`, upd(exams.slice(f, f + 40)));
  execSync(`supabase db query --linked -f ${OUT}chunk-${n}.sql 2>&1`, { shell: "/bin/bash" }); process.stdout.write(`chunk ${n + 1}/${Math.ceil(exams.length / 40)} `); }
const bankSau = (await sb.from("question_bank").select("id", { count: "exact", head: true })).count;
const con = q(CAND);
console.log("\n", { bankTruoc, bankSau, conLech: con.length, triggerBat: q("select tgenabled from pg_trigger where tgname='trg_exams_sync_bank'") });
