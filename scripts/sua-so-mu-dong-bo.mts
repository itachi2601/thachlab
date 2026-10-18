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
const APPLY = false;
const ONLY = process.argv.find((a) => a.startsWith("--only="))?.slice(7); // --only=mu10 : chỉ sửa số mũ 10, bỏ qua đơn vị m2/m3
// Mất dấu trừ chứ không chỉ mất ^ (10.103 m3 = 10.10^-3 m3; câu anh em 1476080 viết 10.10-3): không tự sửa, dò tay
const EXCLUDE_IDS = new Set([1475529]);

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
    re: /(\d|(?<![A-Za-z0-9_\\])[xXyYzZaAbBN])(\s*(?:[.·×x*]|\\cdot|\\times)\s*)10([-−–]?)(\d{1,2})(?![\d^_{]|[,.]\d)/g,
    make: (m, math) => {
      const [, d, op, sign, e] = m;
      if (e.startsWith("0")) return null;
      const n = Number(e);
      // hệ số là chữ cái (x.105 Pa, a.109 Hz): chắc chắn là a·10^n; chỉ bỏ ca "x.102%" (ký tự rác của Word)
      if (/[A-Za-z]/.test(d)) return /^\s*%/.test(m.input.slice(m.index + m[0].length)) ? null : `${d}${op}10${sup((sign ? (math ? "-" : "−") : "") + e, math)}`;
      const before = m.input.slice(Math.max(0, m.index - 12), m.index + 1);
      const after = m.input.slice(m.index + m[0].length, m.index + m[0].length + 6);
      const mantissaThapPhan = /,\d*$/.test(before); // 1,3.102 — có dấu phẩy thập phân → chắc là dạng khoa học
      const sauLaDonVi = /^\s*(?:[A-Za-zΩμ°%]|$|[.,;)])/.test(after) && !/^\s*[=+\-*\/×]/.test(after);
      if (n < 3 && !(sauLaDonVi && (mantissaThapPhan || (sign && !math)))) return null; // mũ 1,2 dễ nhầm với phép nhân
      // Siết sau soát mẫu 18/10 (agent kiem-code, 70 ca → 4 sai + 6 nghi): mũ DƯƠNG mất cả dấu trừ / số nguyên nhiều chữ số là ca mơ hồ → để duyệt tay
      if (!sign && /\d/.test(m.input[m.index - 1] ?? "") && !mantissaThapPhan) return null; // 63\cdot 105, 360.103: 105/360 là số thường
      if (!sign && (/^\s*[A-Za-zμ]+1(?![\d])/.test(after) || (/^\s*[μnp]C\b/.test(after) && n >= 3))) return null; // s1, năm1 (mất cả mũ −1), μC/nC với mũ dương
      if (!sign && mantissaThapPhan && (n <= 2 || /(?<![\d,])0,\d*$/.test(before))) return null; // 0,9.102 m, 8,1.102 m: có thể 10^-2
      if (!sign && /^\s*(?:J|T|C|F|H)(?![A-Za-z])/.test(after) && (n >= 19 || /^\s*T\b/.test(after) || /,\d*$/.test(before) && /^\s*T/.test(after))) return null; // k=1,38.1023 J/K, B=2,5.105 T: phần lớn là mũ âm
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
    if (ONLY && rule.name !== ONLY) continue;
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
  if (ONLY) return s;
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

// ---- Phần riêng: sửa mất ^ ở ngân hàng + MỌI bản sao trong exams.questions, trong một giao dịch có tắt trigger (xem sự cố hash/trigger 18/10).
//   npx tsx scripts/sua-so-mu-dong-bo.mts [--only=mu10] [--cap=cờ]   → dry-run: ghi scripts/data/gon-ngan-hang/mu/{mau.json,chunk-NN.sql,bao-cao.json}
//   chạy từng file: supabase db query --linked -f scripts/data/gon-ngan-hang/mu/chunk-NN.sql  (sao lưu trước đó ở backup-mu.json)
import { katexLoi } from "./lib/giai-lai-chung.mts";
import { execSync } from "node:child_process";
const OUT = "scripts/data/gon-ngan-hang/mu/"; fs.mkdirSync(OUT, { recursive: true });
const CAP = process.argv.find((a) => a.startsWith("--cap="))?.slice(6) ?? "matMu";
const flagged = new Set<number>(JSON.parse(fs.readFileSync("scripts/data/gon-ngan-hang/de-hu.json", "utf8")).filter((x: any) => x.flags.includes(CAP)).map((x: any) => x.id));
execSync("supabase db query --linked -f scripts/data/gon-ngan-hang/in-use.sql -o json > scripts/data/gon-ngan-hang/in-use.raw 2>/dev/null", { shell: "/bin/bash" });
const raw = fs.readFileSync("scripts/data/gon-ngan-hang/in-use.raw", "utf8"); const byHash = new Map<string, { exam: number; idx: number }[]>();
for (const r of JSON.parse(raw.slice(raw.indexOf("{"), raw.lastIndexOf("}") + 1)).rows) (byHash.get(r.h) ?? byHash.set(r.h, []).get(r.h)!).push({ exam: r.exam_id, idx: r.idx });
const need = new Set<number>(); const bank: any[] = [];
for (let f = 0; ; f += 500) { let d: any; for (let t = 0; t < 5; t++) { const r = await sb.from("question_bank").select("id,content_hash,question").eq("archived", false).in("id", [...flagged].slice(f, f + 500)); if (!r.error) { d = r.data; break; } await new Promise((s) => setTimeout(s, 2000)); } if (!d) throw new Error("timeout"); bank.push(...d); if (f + 500 >= flagged.size) break; }
const exCache = new Map<number, any[]>(); const exOf = async (id: number) => { if (!exCache.has(id)) { const { data, error } = await sb.from("exams").select("questions").eq("id", id).single(); if (error) throw error; exCache.set(id, data!.questions); } return exCache.get(id)!; };
const items: any[] = [], mau: any[] = [], bk: any[] = [], ambigAll: any[] = []; let katexBo = 0, khongDoi = 0, chuaKhop = 0;
for (const r of bank) {
  if (EXCLUDE_IDS.has(r.id)) continue;
  const changes: Change[] = [], ambig: Change[] = [];
  const nq = mapStrings(r.question, (s) => fixString(s, changes, ambig));
  if (!changes.length) { khongDoi++; if (ambig.length) ambigAll.push({ id: r.id, ambig: ambig.slice(0, 3) }); continue; }
  const strs: string[] = []; mapStrings(nq, (s) => (strs.push(s), s)); if (strs.some((s) => katexLoi(s) > 0)) { katexBo++; ambigAll.push({ id: r.id, loi: "katex", changes: changes.slice(0, 3) }); continue; }
  const ex: any[] = [];
  for (const u of byHash.get(r.content_hash) ?? []) { const qs = await exOf(u.exam); const el = qs[u.idx]; if (!el) continue; ex.push({ exam: u.exam, idx: u.idx, el: mapStrings(el, (s) => fixString(s, [], [])) }); }
  if (!(byHash.get(r.content_hash) ?? []).length) chuaKhop++;
  items.push({ id: r.id, nq, ex }); bk.push({ id: r.id, question: r.question, ex: ex.map((e) => ({ exam: e.exam, idx: e.idx })) });
  mau.push({ id: r.id, changes: changes.slice(0, 2).map((c) => c.before + "  →  " + c.after), ambig: ambig.length });
  if (ambig.length) ambigAll.push({ id: r.id, conLai: ambig.slice(0, 3) });
}
mau.sort(() => Math.random() - 0.5); fs.writeFileSync(OUT + "mau.json", JSON.stringify(mau.slice(0, 70), null, 1)); fs.writeFileSync(OUT + "bao-cao.json", JSON.stringify(ambigAll, null, 1)); fs.writeFileSync(OUT + "backup-mu.json", JSON.stringify(bk));
const eqTag = (s: string) => { let t = "j"; while (s.includes("$" + t + "$")) t += "x"; return "$" + t + "$"; };
for (let i = 0, n = 1; i < items.length; i += 120, n++) { const part = JSON.stringify(items.slice(i, i + 120)); const tg = eqTag(part);
  fs.writeFileSync(OUT + `chunk-${String(n).padStart(2, "0")}.sql`, `begin;\nalter table public.exams disable trigger trg_exams_sync_bank;\ndo $do$ declare r jsonb; e jsonb; h text; begin\n  for r in select * from jsonb_array_elements(${tg}${part}${tg}::jsonb) loop\n    h := public.question_content_hash(r->'nq');\n    if exists (select 1 from public.question_bank where content_hash = h and id <> (r->>'id')::bigint) then raise notice 'TRUNG %', r->>'id'; continue; end if;\n    update public.question_bank set question = r->'nq', content_hash = h, updated_at = now() where id = (r->>'id')::bigint;\n    for e in select * from jsonb_array_elements(r->'ex') loop\n      update public.exams set questions = jsonb_set(questions, array[e->>'idx'], e->'el') where id = (e->>'exam')::bigint;\n    end loop;\n  end loop;\nend $do$;\nalter table public.exams enable trigger trg_exams_sync_bank;\ncommit;\n`); }
console.log(`cờ ${CAP}: ${flagged.size} câu · sẽ sửa ${items.length} · bản sao đề ${items.reduce((s, x) => s + x.ex.length, 0)} · không đổi ${khongDoi} · bỏ vì KaTeX ${katexBo} · không thấy trong đề nào ${chuaKhop}`);
