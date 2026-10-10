// Sửa số mũ/đơn vị mất dấu ^ trong question_bank (2.105 Pa → 2.10^5 Pa; m/s2 → m/s^2; cm3 → cm^3).
//   npx tsx scripts/sua-so-mu-ngan-hang.mts            # DRY-RUN: chỉ ghi báo cáo vào scripts/logs/
//   npx tsx scripts/sua-so-mu-ngan-hang.mts --apply    # ghi thật (sao lưu nguyên văn các câu đổi ra scripts/logs/ trước)
// Trong $…$ viết ^{n}; ngoài công thức viết <sup>n</sup>. Ca mơ hồ (2.100 = 200, mũ 0/1/2, "m2 =") KHÔNG tự sửa, chỉ liệt kê.
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

const MATH_OR_TAG = /\$\$[\s\S]*?\$\$|\$[^$]*\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|<[^>]*>/g;
// Trả về: "math" | "text" | "tag" cho vị trí i
function zones(s: string): { a: number; b: number; k: "math" | "tag" }[] {
  return [...s.matchAll(MATH_OR_TAG)].map((m) => ({ a: m.index!, b: m.index! + m[0].length, k: m[0].startsWith("<") ? "tag" : "math" }));
}
const sup = (n: string, math: boolean) => (math ? `^{${n}}` : `<sup>${n}</sup>`);

type Rule = { name: string; re: RegExp; make: (m: RegExpExecArray, math: boolean) => string | null /* null = mơ hồ */ };
const RULES: Rule[] = [
  {
    name: "mu10",
    re: /(\d)(\s*(?:[.·×x*]|\\cdot|\\times)\s*)10([-−–]?)(\d{1,2})(?![\d^_{]|[,.]\d)/g,
    make: (m, math) => {
      const [, d, op, sign, e] = m;
      if (e.startsWith("0")) return null;
      const n = Number(e);
      const before = m.input.slice(Math.max(0, m.index - 12), m.index + 1);
      const after = m.input.slice(m.index + m[0].length, m.index + m[0].length + 6);
      const mantissaThapPhan = /,\d*$/.test(before); // 1,3.102 — có dấu phẩy thập phân → chắc là dạng khoa học
      const sauLaDonVi = /^\s*(?:[A-Za-zΩμ°%]|$|[.,;)])/.test(after) && !/^\s*[=+\-*\/×]/.test(after);
      if (n < 3 && !(sauLaDonVi && (mantissaThapPhan || (sign && !math)))) return null; // mũ 1,2 dễ nhầm với phép nhân
      // trong công thức, "63.105+65.245" là số thập phân dùng dấu chấm → chỉ tự sửa khi mũ âm hoặc dùng \cdot/\times
      if (math && !mantissaThapPhan && /^\s*\.\s*$/.test(op)) return null;
      return `${d}${op}10${sup((sign ? (math ? "-" : "−") : "") + e, math)}`;
    },
  },
  {
    name: "donVi-thuong",
    re: /\b((?:m|mm|cm|km|rad)\/s|(?:kg|g|N|C)\/(?:m|cm|dm))([23])\b(?![\^_{])/g,
    make: (m, math) => `${m[1]}${sup(m[2], math)}`,
  },
  {
    name: "donVi-dai",
    re: /(\d\s*(?:\\,|\\ )?)(mm|cm|dm|km|m)([23])\b(?![\^_{])(?!\s*=)/g,
    make: (m, math) => `${m[1]}${m[2]}${sup(m[3], math)}`,
  },
];
const AMBIG: Rule[] = [
  { name: "mu10?", re: RULES[0].re, make: () => null },
  { name: "donVi-dai?", re: /(\d\s*)(mm|cm|dm|km|m)([23])\b(?![\^_{])(?=\s*=)/g, make: () => null },
];

type Change = { rule: string; before: string; after: string };
function fixString(s: string, changes: Change[], ambig: Change[]): string {
  for (const rule of RULES) {
    const z = zones(s);
    let out = "", last = 0, any = false;
    for (const m of s.matchAll(new RegExp(rule.re.source, "g"))) {
      const i = m.index!;
      const zone = z.find((x) => i >= x.a && i < x.b);
      if (zone?.k === "tag") continue;
      const rep = rule.make(m as RegExpExecArray, zone?.k === "math");
      const ctx = s.slice(Math.max(0, i - 20), i + m[0].length + 15).replace(/\s+/g, " ");
      if (rep === null) { ambig.push({ rule: rule.name + "?", before: ctx, after: "" }); continue; }
      out += s.slice(last, i) + rep; last = i + m[0].length; any = true;
      changes.push({ rule: rule.name, before: ctx, after: ctx.replace(m[0], rep) });
    }
    if (any) s = out + s.slice(last);
  }
  // mơ hồ riêng của đơn vị: "m2 =" (có thể là khối lượng m2)
  for (const m of s.matchAll(AMBIG[1].re)) {
    const i = m.index!;
    if (zones(s).some((x) => x.k === "tag" && i >= x.a && i < x.b)) continue;
    ambig.push({ rule: "donVi-dai?", before: s.slice(Math.max(0, i - 20), i + m[0].length + 15).replace(/\s+/g, " "), after: "" });
  }
  return s;
}
function mapStrings(v: any, f: (s: string) => string): any {
  if (typeof v === "string") return f(v);
  if (Array.isArray(v)) return v.map((x) => mapStrings(x, f));
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, mapStrings(x, f)]));
  return v;
}

const report: any[] = [], backup: any[] = [];
const stat: Record<string, number> = {};
let from = 0, scanned = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    scanned++;
    const changes: Change[] = [], ambig: Change[] = [];
    const nq = mapStrings(r.question, (s) => fixString(s, changes, ambig));
    if (changes.length || ambig.length) report.push({ id: r.id, changes, ambig });
    if (changes.length) { backup.push({ id: r.id, question: r.question }); (r as any).nq = nq; }
    for (const c of changes) stat[c.rule] = (stat[c.rule] ?? 0) + 1;
    for (const c of ambig) stat[c.rule] = (stat[c.rule] ?? 0) + 1;
  }
  if (APPLY) {
    // ghi sau khi đã có backup trên đĩa
    if (backup.length) fs.writeFileSync(path.join(scriptDir, "logs", `backup-so-mu-${runId()}.json`), JSON.stringify(backup));
    for (const r of data as any[]) {
      if (!r.nq) continue;
      const { error: e2 } = await sb.from("question_bank").update({ question: r.nq }).eq("id", r.id);
      if (e2) { console.error("LỖI id", r.id, e2.message); process.exit(1); }
    }
  }
  from += 1000;
}
function runId() { return (globalThis as any).__rid ??= Date.now(); }
const out = path.join(scriptDir, "logs", `sua-so-mu-${APPLY ? "apply" : "dry"}-${Date.now()}.json`);
fs.writeFileSync(out, JSON.stringify(report, null, 2));
console.log(APPLY ? "ĐÃ GHI" : "DRY-RUN", `· quét ${scanned} · câu sẽ đổi ${backup.length} ·`, stat, "→", path.relative(process.cwd(), out));
