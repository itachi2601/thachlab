// Kiểm cấu trúc + KaTeX cho cau.json:  npx tsx scripts/data/soan-cau-dang-thieu/kiem.mts
import katex from "katex";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { activeLintFlags, blockingFlags, flagCodes } from "../../../lib/question-lint";
const dir = path.dirname(fileURLToPath(import.meta.url));
const rows: any[] = JSON.parse(fs.readFileSync(path.join(dir, "cau.json"), "utf8"));
let loi = 0;
const bao = (r: any, m: string) => { loi++; console.log(`#${r.stt} [${r.key}] ${m}`); };
const math = (r: any, s: string) => {
  if ((s.match(/(?<!\\)\$/g) ?? []).length % 2) bao(r, `số dấu $ lẻ: ${s.slice(0, 80)}`);
  for (const m of s.matchAll(/\$([^$]+)\$/g)) {
    try { katex.renderToString(m[1], { throwOnError: true, strict: "ignore" }); } catch (e: any) { bao(r, `KaTeX: ${m[1]} → ${e.message.slice(0, 90)}`); }
    if (/[<>]/.test(m[1])) bao(r, `< > trong $: ${m[1]}`);
  }
  if (s.includes('\\"')) bao(r, 'có \\"');
};
const hashes = new Set<string>();
for (const r of rows) {
  const q = r.q;
  const texts = [q.question, q.explanation, ...(q.options ?? []), ...(q.statements ?? []).map((s: any) => s.text)];
  texts.forEach((t) => math(r, t));
  const k = q.question + JSON.stringify(q.options ?? q.statements);
  if (hashes.has(k)) bao(r, "trùng nội dung"); hashes.add(k);
  if (q.type === "multiple_choice") {
    if (q.options.length !== 4) bao(r, "không đủ 4 phương án");
    if (new Set(q.options).size !== 4) bao(r, "phương án trùng nhau");
    if (!(q.answer >= 0 && q.answer <= 3)) bao(r, "answer ngoài 0..3");
    const chot = q.explanation.match(/Chọn ([A-D])\.<\/p>$/);
    if (!chot || "ABCD".indexOf(chot[1]) !== q.answer) bao(r, `dòng chốt không khớp đáp án ${"ABCD"[q.answer]}`);
    if (q.options.some((o: string) => /^[A-D]\.\s/.test(o))) bao(r, "phương án tự ghi nhãn A.");
  } else if (q.type === "true_false") {
    if (q.statements.length !== 4) bao(r, "không đủ 4 ý");
    const ps = q.explanation.match(/<p[^>]*>([a-d])\) (Đúng|Sai)\./g) ?? [];
    if (ps.length !== 4) bao(r, "lời giải Đ/S không đủ 4 đoạn a)–d)");
    q.statements.forEach((s: any, j: number) => { if (!(ps[j] ?? "").includes(s.answer ? "Đúng" : "Sai")) bao(r, `ý ${"abcd"[j]} lệch đáp án`); });
    if (q.statements.every((s: any) => s.answer) || q.statements.every((s: any) => !s.answer)) bao(r, "4 ý cùng Đúng/Sai");
  } else bao(r, "type lạ");
  if (!["de", "trung-binh", "kho"].includes(q.difficulty)) bao(r, "difficulty lạ");
  if (q.question.includes("$q$") || q.explanation.includes("$q$")) bao(r, "chứa $q$");
  const fl = activeLintFlags(q, q.type);
  if (blockingFlags(fl).length) bao(r, `lint web (mức lỗi → RPC bỏ câu): ${flagCodes(blockingFlags(fl)).join(",")}`);
  else if (fl.length) console.log(`#${r.stt} [${r.key}] lint cảnh báo: ${flagCodes(fl).join(",")}`);
}
const by: Record<string, number> = {};
rows.forEach((r) => (by[r.key] = (by[r.key] ?? 0) + 1));
console.log(`${rows.length} câu, ${Object.keys(by).length} dạng, ${loi} lỗi`);
process.exit(loi ? 1 : 0);
