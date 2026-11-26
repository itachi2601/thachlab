/**
 * Đo mức trùng giữa câu hỏi đề và nội dung bài lý thuyết (chỉ đọc file trong repo, không gọi DB).
 *
 * Hai nguồn đề được đo riêng:
 *   - bundle  : `exam.questions` trong content/lesson-samples/<bài>/bundle.json
 *               (skill soan-bai-ly-thuyet-tuong-tac quy ước: CHÍNH các câu tự kiểm trong bài → trùng là chủ ý)
 *   - quiz20  : scripts/data/theory-quiz/<lesson_id>.json (bộ 20 câu "Kiểm tra nhanh", ghép theo lesson_title)
 *
 * Một câu "trùng" khi:
 *   - phần đề (≥ 25 ký tự sau chuẩn hoá) nằm nguyên văn trong lý thuyết, HOẶC
 *   - ≥ (số phương án − 1) phương án (mỗi phương án ≥ 4 ký tự sau chuẩn hoá) nằm nguyên văn trong lý thuyết.
 * Chuẩn hoá: bỏ thẻ HTML, thực thể, lệnh LaTeX (\frac → frac…), $, {}, dấu cách, dấu câu; chữ thường.
 *
 * Chạy: npx tsx scripts/kiem-trung-cau-de-ly-thuyet.mts [--md out.md] [--prefix l10-]
 */
import { readFileSync, readdirSync, existsSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const ROOT = process.cwd();
const SAMPLES = join(ROOT, "content/lesson-samples");
const QUIZ = join(ROOT, "scripts/data/theory-quiz");

const args = process.argv.slice(2);
const mdOut = args.includes("--md") ? args[args.indexOf("--md") + 1] : null;
const prefixArg = args.includes("--prefix") ? args[args.indexOf("--prefix") + 1] : null;
const prefixes = prefixArg ? [prefixArg] : ["l10-", "l11-", "l12-"];

function norm(s: string): string {
  return s
    .replace(/<[^>]+>/g, " ")
    .replace(/&[a-z#0-9]+;/gi, " ")
    .replace(/\\(left|right|mathrm|text|rm|,|;|!|quad)/g, "")
    .replace(/\\([a-zA-Z]+)/g, "$1")
    .replace(/[$\\{}]/g, "")
    .toLowerCase()
    .normalize("NFC")
    .replace(/[\s.,;:!?"'“”‘’()\[\]«»–—-]+/g, "");
}

type Q = { question?: string; options?: unknown[]; statements?: unknown[] };

function optText(o: unknown): string {
  if (typeof o === "string") return o;
  if (o && typeof o === "object") {
    const r = o as Record<string, unknown>;
    return String(r.text ?? r.content ?? r.label ?? "");
  }
  return "";
}

function isDup(q: Q, theory: string): boolean {
  const stem = norm(q.question ?? "");
  if (stem.length >= 25 && theory.includes(stem)) return true;
  const opts = (q.options ?? q.statements ?? []).map(optText).map(norm).filter((s) => s.length >= 4);
  if (opts.length < 2) return false;
  const hit = opts.filter((o) => theory.includes(o)).length;
  return hit >= opts.length - 1;
}

const quizByTitle = new Map<string, { id: string; questions: Q[] }>();
if (existsSync(QUIZ)) {
  for (const f of readdirSync(QUIZ).filter((f) => f.endsWith(".json"))) {
    try {
      const d = JSON.parse(readFileSync(join(QUIZ, f), "utf8"));
      if (d.lesson_title) quizByTitle.set(norm(d.lesson_title), { id: String(d.lesson_id), questions: d.questions ?? [] });
    } catch {
      /* bỏ file hỏng */
    }
  }
}

type Row = { slug: string; bTot: number; bDup: number; qId: string; qTot: number; qDup: number };
const rows: Row[] = [];

for (const slug of readdirSync(SAMPLES).sort()) {
  if (!prefixes.some((p) => slug.startsWith(p))) continue;
  const bp = join(SAMPLES, slug, "bundle.json");
  if (!existsSync(bp)) continue;
  const b = JSON.parse(readFileSync(bp, "utf8"));
  const theory = norm(b.theory_html ?? "");
  const bq: Q[] = b.exam?.questions ?? [];
  const quiz = quizByTitle.get(norm(b.target?.lesson_title ?? ""));
  rows.push({
    slug,
    bTot: bq.length,
    bDup: bq.filter((q) => isDup(q, theory)).length,
    qId: quiz?.id ?? "",
    qTot: quiz?.questions.length ?? 0,
    qDup: quiz ? quiz.questions.filter((q) => isDup(q, theory)).length : 0,
  });
}

const pct = (a: number, b: number) => (b ? `${Math.round((100 * a) / b)}%` : "—");
const sum = (k: keyof Row) => rows.reduce((s, r) => s + (r[k] as number), 0);

const lines: string[] = [];
lines.push(`| Bài | bundle trùng/tổng | % | quiz20 (id) trùng/tổng | % |`);
lines.push(`|---|---|---|---|---|`);
for (const r of rows)
  lines.push(
    `| ${r.slug} | ${r.bDup}/${r.bTot} | ${pct(r.bDup, r.bTot)} | ${r.qId ? `${r.qDup}/${r.qTot} (${r.qId})` : "—"} | ${r.qId ? pct(r.qDup, r.qTot) : "—"} |`,
  );
const withQuiz = rows.filter((r) => r.qId);
lines.push("");
lines.push(
  `Tổng: ${rows.length} bài · bundle ${sum("bDup")}/${sum("bTot")} (${pct(sum("bDup"), sum("bTot"))}) · ` +
    `bài bundle trùng 100%: ${rows.filter((r) => r.bTot && r.bDup === r.bTot).length} · ` +
    `quiz20 có ở ${withQuiz.length} bài: ${withQuiz.reduce((s, r) => s + r.qDup, 0)}/${withQuiz.reduce((s, r) => s + r.qTot, 0)}`,
);

const out = lines.join("\n");
console.log(out);
if (mdOut) writeFileSync(mdOut, out + "\n");
