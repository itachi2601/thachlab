// Sau dò lần 2: (1) dọn lỗi nhỏ trong 337 câu đã ghi (&gt; trong công thức, ** thừa ở phương án), (2) BẬT HIỆN các câu qua dò, giữ ẨN các câu chưa qua.
//   npx tsx scripts/hien-vl10.mts            dry-run: in số liệu, ghi hien.sql
//   npx tsx scripts/hien-vl10.mts --apply    chạy hien.sql (giao dịch)
// Hoàn tác bật Hiện: update public.question_bank set archived = true where note = 'nap-vl10-c3-20261020';
import fs from "node:fs";
import { execSync } from "node:child_process";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const U = env("NEXT_PUBLIC_SUPABASE_URL"), K = env("SUPABASE_SERVICE_ROLE_KEY");
const DIR = (process.env.VL10_DIR ?? "scripts/data/nap-ngan-hang-vl10") + "/", NOTE = process.env.VL10_NOTE ?? "nap-vl10-c3-20261020";
const final = new Map<string, any>(JSON.parse(fs.readFileSync(DIR + "cau-final.json", "utf8")).map((q: any) => [q.key, q]));
const do2: any[] = JSON.parse(fs.readFileSync(DIR + "do2-ket-qua.json", "utf8"));
const norm = (s: string) => s.replace(/<[^>]+>/g, "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").toLowerCase().replace(/[^a-z0-9]+/g, "");
const sig = (q: any) => norm(String(q.question ?? "")).slice(0, 80) + "|" + norm((q.options ?? (q.statements ?? []).map((s: any) => s.text)).join("")).slice(0, 80);
const suaND: Record<string, any> = fs.existsSync(DIR + "sua-noi-dung.json") ? JSON.parse(fs.readFileSync(DIR + "sua-noi-dung.json", "utf8")) : {};
const bySig = new Map([...final].map(([k, q]) => [sig(q), k]));
const r = await (await fetch(`${U}/rest/v1/question_bank?note=eq.${NOTE}&select=id,question,archived&order=id&limit=1000`, { headers: { apikey: K, Authorization: `Bearer ${K}` } })).json();
const giu = new Set(do2.filter((o) => o.kq !== "khop" || o.flags.includes("khong-co-loi-giai")).map((o) => o.key));
giu.add("c3-6-mc-008");
if (fs.existsSync(DIR + "loai-them.json")) for (const k of JSON.parse(fs.readFileSync(DIR + "loai-them.json", "utf8"))) giu.add(k); // câu lỗi hiển thị phát hiện sau dò: giữ ẨN để xoá // lời giải trống + nghi 2 đáp án đúng → chờ viết tay
const fixMath = (s: string) => s.replace(/(?<!\\)\$(?!\$)([^$]+?)\$/g, (_m, t) => "$" + t.replace(/&gt;/g, "\\gt ").replace(/&lt;/g, "\\lt ").replace(/&amp;/g, "&") + "$");
const fixTxt = (s: string) => fixMath(s).replace(/\s*\*{2,}\s*$/g, "").replace(/\*\*(?=[.\s]*$)/g, "").trim();
const sql = ["begin;"]; const show: number[] = []; let sua = 0, khongKhop = 0;
for (const row of r) {
  const key = bySig.get(sig(row.question)); if (!key) { khongKhop++; continue; }
  const q = JSON.parse(JSON.stringify(row.question));
  const ov = suaND[key];
  if (ov?.question) q.question = ov.question;
  if (ov?.options) q.options = ov.options;
  if (ov?.statements_text) q.statements = q.statements.map((st: any, i: number) => ({ ...st, text: ov.statements_text[i] }));
  q.question = fixMath(q.question); q.explanation = q.explanation ? fixMath(q.explanation) : q.explanation;
  if (q.options) q.options = q.options.map(fixTxt);
  if (q.statements) q.statements = q.statements.map((s: any) => ({ ...s, text: fixTxt(s.text) }));
  if (JSON.stringify(q) !== JSON.stringify(row.question)) { sua++; sql.push(`update public.question_bank set question = $q$${JSON.stringify(q)}$q$::jsonb, content_hash = public.question_content_hash($q$${JSON.stringify(q)}$q$::jsonb), updated_at = now() where id = ${row.id} and note = '${NOTE}';`); }
  if (!giu.has(key)) show.push(row.id);
}
for (let i = 0; i < show.length; i += 200) sql.push(`update public.question_bank set archived = false where note = '${NOTE}' and id in (${show.slice(i, i + 200).join(",")});`);
sql.push(`select count(*) filter (where archived) as an, count(*) filter (where not archived) as hien, count(*) as tong from public.question_bank where note = '${NOTE}';`, "commit;");
fs.writeFileSync(DIR + "hien.sql", sql.join("\n"));
console.log(`Hàng DB: ${r.length} · không khớp key: ${khongKhop} · cần sửa nội dung: ${sua} · sẽ BẬT HIỆN: ${show.length} · giữ ẨN: ${r.length - show.length}`);
if (process.argv.includes("--apply")) console.log(execSync(`supabase db query --linked -f ${DIR}hien.sql`, { encoding: "utf8" }).slice(-400)); else console.log("DRY-RUN — chưa ghi DB.");
