// Sửa chữ Hy Lạp + chỉ số dán liền (λ1, φ2, θ1…) trong question_bank hoặc exams.questions (--exams): ngoài công thức → $\lambda_1$; trong $…$ → \lambda_1.
//   npx tsx scripts/sua-lambda-chi-so-ngan-hang.mts            # DRY-RUN: ghi báo cáo scripts/logs/
//   npx tsx scripts/sua-lambda-chi-so-ngan-hang.mts --apply    # sao lưu nguyên văn rồi ghi, đọc lại đối chiếu
// Bỏ qua URL, thẻ HTML, chuỗi lẻ dấu $, λ + nhiều chữ số (λ10). Không đổi content_hash.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function env(key: string): string | undefined {
  const line = fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const EXAMS = process.argv.includes("--exams");
const ONLY = (process.argv.find((a) => a.startsWith("--only=")) ?? "").slice(7); // vd --only=λφθ
const TABLE = EXAMS ? "exams" : "question_bank";
const COL = EXAMS ? "questions" : "question";
const GREEK: Record<string, string> = { α: "alpha", β: "beta", γ: "gamma", δ: "delta", ε: "varepsilon", θ: "theta", λ: "lambda", μ: "mu", ν: "nu", ρ: "rho", σ: "sigma", τ: "tau", φ: "varphi", ω: "omega", Δ: "Delta", Φ: "Phi", Ω: "Omega", Θ: "Theta" };
const LET = Object.keys(GREEK).filter((c) => c !== "ω" && (!ONLY || ONLY.includes(c))).join("");
const stamp = Date.now();
const SKIP_KEYS = new Set(["answer", "topic", "type", "form", "difficulty", "difficultySource", "id", "key", "kind"]);
const ZONE = /https?:\/\/[^\s"'<>)]+|\$\$[\s\S]*?\$\$|\$[^$]*\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|<[^>]*>/g;
const BARE = new RegExp(`([${LET}])([0-9])(?![0-9])`, "g");
const TEXLAM = new RegExp(`\\\\(${Object.values(GREEK).join("|")})([0-9])(?![0-9])`, "g");
const cmd = (l: string) => "\\" + GREEK[l];

type Change = { before: string; after: string };
function fixString(s: string, changes: Change[], skipped: string[]): string {
  BARE.lastIndex = 0; TEXLAM.lastIndex = 0;
  if (!(BARE.test(s) || (BARE.lastIndex = 0, TEXLAM.test(s))) || /^(https?:|data:)/.test(s)) return s;
  if ((s.replace(/\\\$/g, "").match(/\$/g)?.length ?? 0) % 2 === 1) { skipped.push("lẻ $: " + s.slice(0, 80)); return s; }
  let out = "", last = 0;
  const flushText = (t: string) => t.replace(BARE, (_m, l, d) => `$${cmd(l)}_${d}$`);
  for (const m of s.matchAll(ZONE)) {
    out += flushText(s.slice(last, m.index!));
    const z = m[0];
    out += z.startsWith("<") || z.startsWith("http") ? z : z.replace(BARE, (_m, l, d) => `${cmd(l)}_${d}`).replace(TEXLAM, "\\$1_$2");
    last = m.index! + z.length;
  }
  out += flushText(s.slice(last));
  if (out !== s) changes.push({ before: s, after: out });
  return out;
}
function walk(v: any, changes: Change[], skipped: string[]): any {
  if (typeof v === "string") return fixString(v, changes, skipped);
  if (Array.isArray(v)) return v.map((x) => walk(x, changes, skipped));
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, SKIP_KEYS.has(k) ? x : walk(x, changes, skipped)]));
  return v;
}

const rows: any[] = [];
for (let from = 0; ; from += 500) {
  let data: any[] | null = null, error: any = null;
  for (let t = 0; t < 4 && !data; t++) {
    try { ({ data, error } = await sb.from(TABLE).select(`id, ${COL}`).order("id").range(from, from + 499)); } catch (e) { error = e; }
    if (error) { data = null; await new Promise((r) => setTimeout(r, 1500)); }
  }
  if (!data) { console.error("đọc lỗi:", error?.message ?? error); process.exit(1); }
  rows.push(...data.map((r: any) => ({ id: r.id, question: r[COL] })));
  if (data.length < 500) break;
}
const plan: { id: number; old: any; neu: any; changes: Change[] }[] = [];
const skipped: string[] = [];
for (const r of rows) {
  const changes: Change[] = [];
  const neu = walk(r.question, changes, skipped);
  if (changes.length) plan.push({ id: r.id, old: r.question, neu, changes });
}
console.log(`Quét ${rows.length} câu → ${plan.length} câu cần sửa, ${skipped.length} chuỗi bỏ qua`);
fs.writeFileSync(path.join(scriptDir, "logs", `greek-${TABLE}-${APPLY ? "apply" : "dry"}-${stamp}.json`), JSON.stringify({ plan: plan.map((p) => ({ id: p.id, changes: p.changes })), skipped }, null, 1));
for (const p of plan.slice(0, 8)) console.log(p.id, "\n  -", p.changes[0].before.replace(/<[^>]*>/g, "").slice(0, 140), "\n  +", p.changes[0].after.replace(/<[^>]*>/g, "").slice(0, 140));
if (!APPLY) process.exit(0);
const backup = path.join(scriptDir, "logs", `greek-backup-${stamp}.json`);
fs.writeFileSync(backup, JSON.stringify(plan.map((p) => ({ id: p.id, question: p.old }))));
let bad = 0;
for (const p of plan) {
  const { error } = await sb.from(TABLE).update({ [COL]: p.neu }).eq("id", p.id);
  if (error) { console.error(p.id, error.message); bad++; }
}
const { data: chk } = await sb.from(TABLE).select(`id, ${COL}`).in("id", plan.map((p) => p.id).slice(0, 1000));
const mismatch = (chk ?? []).filter((r) => JSON.stringify((r as any)[COL]) !== JSON.stringify(plan.find((p) => p.id === r.id)!.neu));
console.log(`Đã ghi ${plan.length - bad}/${plan.length}; lệch khi đọc lại: ${mismatch.length}; sao lưu: ${path.relative(process.cwd(), backup)}`);
