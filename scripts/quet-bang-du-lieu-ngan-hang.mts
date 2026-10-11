// Quét question_bank: câu nhắc "bảng" nhưng dữ liệu không nằm trong <table> (CHỈ ĐỌC, không ghi DB).
//   npx tsx scripts/quet-bang-du-lieu-ngan-hang.mts
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => process.env[k] ?? fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

const textOf = (q: any) => [q?.stem, q?.question, q?.content, ...(Array.isArray(q?.options) ? q.options.map((o: any) => (typeof o === "string" ? o : o?.text ?? "")) : []), q?.explanation].filter((x) => typeof x === "string").join("\n");
const rows: any[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("question_bank").select("id, grade, topic_name, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  rows.push(...data);
}
const tab: any[] = [];
const res = { tong: rows.length, coTable: 0, nhacBangKhongTable: [] as any[], tableKhongVien: 0, keys: {} as Record<string, number> };
for (const r of rows) {
  for (const k of Object.keys(r.question ?? {})) res.keys[k] = (res.keys[k] ?? 0) + 1;
  const t = textOf(r.question);
  const hasTable = /<table/i.test(t);
  if (hasTable) res.coTable++;
  if (/\\begin\{tabular\}/.test(t)) tab.push({ id: r.id, grade: r.grade, chude: r.topic_name, truong: ["question","explanation"].filter((k) => /\\begin\{tabular\}/.test(String(r.question?.[k] ?? ""))) });
  const nhac = /\b(bảng|bang)\s*(số liệu|dữ liệu|sau|dưới|kết quả|\d)/i.test(t) || /\|\s*[^|\n]+\s*\|\s*[^|\n]+\|/.test(t);
  if (nhac && !hasTable) res.nhacBangKhongTable.push({ id: r.id, grade: r.grade, chude: r.topic_name, trich: t.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").slice(0, 260) });
}
fs.writeFileSync(path.join(dir, "logs", "quet-bang-ngan-hang.json"), JSON.stringify({ ...res, tabular: tab }, null, 2));
console.log(JSON.stringify({ tong: res.tong, coTable: res.coTable, nhacBangKhongTable: res.nhacBangKhongTable.length, tabularTho: tab.length, theoLop: tab.reduce((a: any, x) => (a[x.grade] = (a[x.grade] ?? 0) + 1, a), {}), keys: res.keys }, null, 1));
