// Kiểm khuôn biến thể đổi số (`bien_the`) trong file nguồn bài tập mẫu — chạy được offline, không đụng DB.
//   npx tsx scripts/kiem-bien-the.mts                 → mọi scripts/data/bai-tap-mau/*.json có bien_the
//   npx tsx scripts/kiem-bien-the.mts 18 [--n 500] [--mau 3]
// Mỗi khuôn: kiểm tĩnh (cú pháp, tên biến, chỗ trống trong $…$), rồi sinh N bộ số (mặc định 200):
//  - một lần bốc (không thử lại): đếm vi phạm ràng buộc, NaN/vô cực, phương án trùng/gần nhau, đáp số > 4 ký tự;
//  - sinh có thử lại như trình duyệt: seed nào KHÔNG ra câu → lỗi; câu ra phải không còn {{…}} và KaTeX dựng được.
// --mau k: in k câu mẫu (đề + phương án + đáp án) để đối chiếu tay.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import katex from "katex";
import { checkTemplate, generate, tryOnce } from "../lib/bien-the";
import type { WorkedVariant } from "../features/lessons/types";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dir = path.join(root, "scripts/data/bai-tap-mau");
const argv = process.argv.slice(2);
const opt = (k: string, d: number) => (argv.includes(k) ? Number(argv[argv.indexOf(k) + 1]) : d);
const N = opt("--n", 200), MAU = opt("--mau", 0);
const ids = argv.filter((a, i) => /^\d+$/.test(a) && !["--n", "--mau"].includes(argv[i - 1]));
const files = ids.length ? ids.map((id) => path.join(dir, `${id}.json`)) : fs.readdirSync(dir).filter((f) => f.endsWith(".json")).map((f) => path.join(dir, f));

function mathErrors(html: string): string[] {
  const out: string[] = [];
  for (const m of html.matchAll(/\$([^$]+)\$/g)) {
    try { katex.renderToString(m[1], { throwOnError: true }); } catch (e) { out.push(`KaTeX: ${(e as Error).message.slice(0, 120)} ← $${m[1]}$`); }
  }
  return out;
}
const plain = (h: string) => h.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();

let bad = 0, total = 0;
for (const file of files) {
  if (!fs.existsSync(file)) { console.error(`không thấy ${path.relative(root, file)}`); bad++; continue; }
  const data = JSON.parse(fs.readFileSync(file, "utf8"));
  const list = ((data.dang_bai ?? []) as { label: string; bien_the?: WorkedVariant; buoc?: unknown[] }[]).filter((d) => d.bien_the);
  for (const d of list) {
    total++;
    const v = d.bien_the!;
    const errs = checkTemplate(v);
    const nSteps = d.buoc?.length ?? 0;
    (v.nhieu ?? []).forEach((x, i) => {
      if (x.buoc != null && (x.buoc < 0 || x.buoc >= nSteps)) errs.push(`nhieu[${i}].buoc = ${x.buoc} ngoài 0…${nSteps - 1}`);
    });
    console.log(`\n${path.basename(file)} · ${d.label}  [${v.kieu}]`);
    if (errs.length) { bad++; errs.forEach((e) => console.log("  ✗ " + e)); continue; }

    const reasons = new Map<string, number>();
    let fails = 0, okRaw = 0, lo = Infinity, hi = -Infinity;
    const render = new Set<string>();
    const letters = new Map<number, number>();
    for (let s = 1; s <= N; s++) {
      const r = tryOnce(v, s);
      if (r.ok) okRaw++;
      else reasons.set(r.loi, (reasons.get(r.loi) ?? 0) + 1);
      const q = generate(v, s);
      if (!q) { fails++; continue; }
      lo = Math.min(lo, q.exact); hi = Math.max(hi, q.exact);
      const qq = q.question;
      const parts = [qq.question, qq.explanation, ...(qq.type === "multiple_choice" ? qq.options : [])];
      if (parts.some((p) => p.includes("{{"))) render.add("còn chỗ trống {{…}} chưa thay");
      parts.forEach((p) => mathErrors(p).forEach((e) => render.add(e)));
      if (qq.type === "multiple_choice") letters.set(qq.answer, (letters.get(qq.answer) ?? 0) + 1);
      if (s <= MAU) {
        console.log(`  · mẫu seed ${s}: ${plain(qq.question).slice(0, 220)}`);
        if (qq.type === "multiple_choice") qq.options.forEach((o, i) => console.log(`      ${"ABCD"[i]}. ${o}${i === qq.answer ? "  ✓" : ""}`));
        else console.log(`      đáp số: ${qq.type === "short_answer" ? qq.answer : ""}  (chính xác ${q.exact})`);
      }
    }
    console.log(`  ${N} bộ số: ${okRaw} đạt ngay (${Math.round((okRaw / N) * 100)} %), đáp số ${lo.toPrecision(3)} … ${hi.toPrecision(3)}`);
    for (const [k, n] of [...reasons].sort((a, b) => b[1] - a[1])) console.log(`    – bốc lại ${n}×: ${k}`);
    if (letters.size) console.log(`    đáp án đúng rơi vào: ${[0, 1, 2, 3].map((i) => `${"ABCD"[i]} ${letters.get(i) ?? 0}`).join(" · ")}`);
    if (okRaw / N < 0.5) console.log("  ! hơn nửa số lần bốc bị loại — nới khoảng biến hoặc ràng buộc");
    if (fails) { bad++; console.log(`  ✗ ${fails}/${N} seed không sinh được câu sau 200 lần thử`); }
    if (render.size) { bad++; [...render].slice(0, 8).forEach((e) => console.log("  ✗ " + e)); }
    if (!fails && !render.size) console.log("  ✓ đạt");
  }
}
console.log(`\n${total} khuôn, ${bad} lỗi`);
process.exit(bad ? 1 : 0);
