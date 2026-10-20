// Áp phản hồi duyệt SAU dò lần 2 (phan-hoi-do2.json): 'ai' → đổi đáp án + lời giải theo Sonnet (CHỈ khi lượt giải lại cho đúng cùng đáp án), 'nguon' → giữ, rồi bật Hiện; còn lại giữ Ẩn.
//   VL10_DIR=… VL10_NOTE=… npx tsx scripts/ap-do2-vl10.mts [--apply]
import fs from "node:fs";
import { execSync } from "node:child_process";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const U = env("NEXT_PUBLIC_SUPABASE_URL"), K = env("SUPABASE_SERVICE_ROLE_KEY");
const DIR = (process.env.VL10_DIR ?? "scripts/data/nap-ngan-hang-vl10") + "/", NOTE = process.env.VL10_NOTE!;
const J = (f: string) => JSON.parse(fs.readFileSync(DIR + f, "utf8"));
const dec = J("duyet/phan-hoi-do2.json"), items = new Map<string, any>(J("duyet/items-do2.json").map((x: any) => [x.key, x]));
const do2 = new Map<string, any>(J("do2-ket-qua.json").map((x: any) => [x.key, x]));
const final = new Map<string, any>(J("cau-final.json").map((q: any) => [q.key, q]));
const norm = (s: string) => s.replace(/<[^>]+>/g, "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").toLowerCase().replace(/[^a-z0-9]+/g, "");
const sig = (q: any) => norm(String(q.question ?? "")).slice(0, 80) + "|" + norm((q.options ?? (q.statements ?? []).map((s: any) => s.text)).join("")).slice(0, 80);
const bySigKey = new Map([...final].map(([k, q]) => [sig({ ...q, question: q.question }), k]));
const rows = await (await fetch(`${U}/rest/v1/question_bank?note=eq.${NOTE}&select=id,question&order=id&limit=1000`, { headers: { apikey: K, Authorization: `Bearer ${K}` } })).json();
const idOf = new Map<string, any>();
for (const r of rows) { const k = bySigKey.get(sig(r.question)); if (k) idOf.set(k, r); }
const sql = ["begin;"]; const bao: string[] = [];
const same = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b);
for (const [k, d] of Object.entries<any>(dec)) {
  const row = idOf.get(k); if (!row) { bao.push(`${k}: không thấy hàng DB`); continue; }
  const q = JSON.parse(JSON.stringify(row.question));
  if (d.choice === "nguon") { sql.push(`update public.question_bank set archived = false where id = ${row.id} and note = '${NOTE}';`); bao.push(`${k}: HIỆN (giữ đáp án)`); continue; }
  if (d.choice !== "ai") { bao.push(`${k}: giữ ẨN (${d.choice ?? "chưa chọn"})`); continue; }
  const n = do2.get(k), old = items.get(k).sonnet;
  if (!n || n.kq === "khong-co-ket-qua" || !same(n.ai, old) || !n.expl) { bao.push(`${k}: giữ ẨN — giải lại KHÔNG ra cùng đáp án (${JSON.stringify(old)} vs ${JSON.stringify(n?.ai)})`); continue; }
  const a = n.ai;
  if (q.type === "multiple_choice") q.answer = "ABCD".indexOf(String(a).trim().toUpperCase()[0]);
  else if (q.type === "true_false") q.statements = q.statements.map((s: any, i: number) => ({ ...s, answer: !!a[i] }));
  else q.answer = String(a);
  q.explanation = n.expl;
  const js = JSON.stringify(q);
  sql.push(`update public.question_bank set question = $q$${js}$q$::jsonb, content_hash = public.question_content_hash($q$${js}$q$::jsonb), archived = false, updated_at = now() where id = ${row.id} and note = '${NOTE}';`);
  bao.push(`${k}: HIỆN, đổi đáp án ${JSON.stringify(row.question.answer ?? row.question.statements?.map((s: any) => s.answer))} → ${JSON.stringify(a)}`);
}
sql.push(`select count(*) filter (where archived) an, count(*) filter (where not archived) hien, count(*) tong from public.question_bank where note = '${NOTE}';`, "commit;");
fs.writeFileSync(DIR + "ap-do2.sql", sql.join("\n")); console.log(bao.join("\n"));
if (process.argv.includes("--apply")) console.log(execSync(`supabase db query --linked -f ${DIR}ap-do2.sql`, { encoding: "utf8" }).slice(-300)); else console.log("DRY-RUN — chưa ghi DB.");
