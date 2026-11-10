// Liệt kê chủ đề một lớp (mặc định 10, --lop 12) trong question_bank và xuất câu của chủ đề khớp --chu-de (CHỈ ĐỌC, KHÔNG GHI).
//   npx tsx scripts/quet-cau-can-hinh-l10.mts                 # in danh sách chủ đề lớp 10 + số câu
//   npx tsx scripts/quet-cau-can-hinh-l10.mts --chu-de "lực"   # ghi scripts/data/hinh-cau-hoi/l10-<slug>.json
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function readEnvLocal(key: string): string | undefined {
  for (const p of [path.resolve(scriptDir, "..", ".env.local"), "/Users/MAC/Projects/thachlab/.env.local"]) {
    if (!fs.existsSync(p)) continue;
    const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
    if (line) return line.slice(key.length + 1).trim();
  }
  return undefined;
}
const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const ci = process.argv.indexOf("--chu-de");
const filter = ci > 0 ? process.argv[ci + 1] : null; // regex, không phân biệt hoa thường
const re = filter ? new RegExp(filter, "i") : null;
const li = process.argv.indexOf("--lop");
const lop = li > 0 ? process.argv[li + 1] : "10"; // lớp khác: --lop 12
const ri = process.argv.indexOf("--ra");
const outRel = ri > 0 ? process.argv[ri + 1] : "hinh-cau-hoi/l10-dong-luc-hoc.json"; // tương đối scripts/data/

const rows: any[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await supabase
    .from("question_bank")
    .select("id, grade, topic_name, qtype, figure_not_needed, question")
    .eq("archived", false)
    .eq("subject_code", "vat-ly")
    .ilike("grade", `%${lop}%`)
    .range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  rows.push(...(data ?? []));
  if (!data || data.length < 1000) break;
}
console.log(`lớp ${lop} chưa lưu trữ: ${rows.length} câu`);

if (!filter) {
  const m = new Map<string, number>();
  for (const r of rows) m.set(`${r.grade} | ${r.topic_name}`, (m.get(`${r.grade} | ${r.topic_name}`) ?? 0) + 1);
  for (const [k, v] of [...m].sort()) console.log(String(v).padStart(5), k);
  process.exit(0);
}
const sel = rows.filter((r) => re!.test(r.topic_name ?? ""));
const f = path.join(scriptDir, "data", outRel);
fs.mkdirSync(path.dirname(f), { recursive: true });
fs.writeFileSync(f, JSON.stringify(sel, null, 1));
console.log(`${sel.length} câu → ${path.relative(process.cwd(), f)}`);
