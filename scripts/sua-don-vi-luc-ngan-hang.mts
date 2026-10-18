// Sửa question_bank: đơn vị gia tốc m/s2 → $m/s^2$ ; lực F1, F2, F3 → $F_1$, $F_2$, $F_3$ (trong $…$ thì không thêm $).
//   npx tsx scripts/sua-don-vi-luc-ngan-hang.mts            # DRY-RUN, ghi báo cáo scripts/logs/ ; mẫu: SHOW=id,id
//   npx tsx scripts/sua-don-vi-luc-ngan-hang.mts --apply    # sao lưu rồi ghi, đọc lại đối chiếu
//   npx tsx scripts/sua-don-vi-luc-ngan-hang.mts --undo <file-backup>
// Bỏ qua: URL, thẻ HTML, khối <svg>, chuỗi lẻ dấu $, ký hiệu nằm trong \text{…}, chỉ số đã có. Không đổi content_hash.
// Mọi chuỗi đổi đều được KaTeX render thử (throwOnError); chuỗi lỗi bị bỏ nguyên.
import { createClient } from "@supabase/supabase-js";
import katex from "katex";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const UNDO = process.argv.includes("--undo") ? process.argv[process.argv.indexOf("--undo") + 1] : null;
const logs = path.join(scriptDir, "logs");
const stamp = Date.now();
const EXCLUDE_IDS = new Set<number>([]);
const SKIP_KEYS = new Set(["answer", "topic", "type", "form", "difficulty", "difficultySource", "id", "key", "kind"]);
const ZONES = /<svg[\s\S]*?<\/svg>|https?:\/\/[^\s"'<>)]+|\$\$[\s\S]*?\$\$|\$[^$]*\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|<[^>]*>/g;
const UNIT = /(?<![A-Za-z_\\^])((?:[kcmdµ]|)m|km)\s*\/\s*([sh])\s*([23])(?![\d_^A-Za-z])/g;
const FORCE = /(?<![A-Za-z_\\^.,\d])F([1-9])(?![\d_^A-Za-z])/g;

function braceInfo(z: string, off: number) { // [trong _{}/^{}, trong \text{}]
  const st: string[] = [];
  for (let i = 0; i < off; i++) {
    const c = z[i];
    if (c === "\\") { if (z[i + 1] === "{" || z[i + 1] === "}") { i++; continue; } const m = /^\\([A-Za-z]+)/.exec(z.slice(i)); if (m && /^\{/.test(z.slice(i + m[0].length))) { st.push("@" + m[1]); i += m[0].length; continue; } continue; }
    if (c === "{") st.push(i > 0 && (z[i - 1] === "_" || z[i - 1] === "^") ? "sub" : "g");
    else if (c === "}") st.pop();
  }
  return [st.includes("sub"), st.some((x) => /^@(text|textrm|textbf|mbox|textit)$/.test(x))];
}
const rewrite = (s: string, inMath: boolean, ch: string[]): string => {
  const f = (re: RegExp, build: (m: RegExpMatchArray) => string, s2: string) => {
    let out = "", last = 0;
    for (const m of s2.matchAll(re)) {
      const i = m.index!;
      if (inMath) { const [sub, txt] = braceInfo(s2, i); if (sub || txt) continue; }
      const rep = build(m); out += s2.slice(last, i) + (inMath ? rep : `$${rep}$`); last = i + m[0].length;
      ch.push(s2.slice(Math.max(0, i - 15), i + m[0].length + 10).replace(/\s+/g, " ") + "  →  " + rep);
    }
    return out + s2.slice(last);
  };
  return f(FORCE, (m) => `F_${m[1]}`, f(UNIT, (m) => `${m[1]}/${m[2]}^${m[3]}`, s));
};
function fixString(s: string, ch: string[], skipped: string[]): string {
  if (/^(https?:|data:)/.test(s)) return s;
  if (!UNIT.test(s) && !FORCE.test(s)) { UNIT.lastIndex = FORCE.lastIndex = 0; return s; }
  UNIT.lastIndex = FORCE.lastIndex = 0;
  if (((s.replace(/\\\$/g, "").match(/\$/g)?.length ?? 0) % 2) === 1) { skipped.push("lẻ $: " + s.slice(0, 70)); return s; }
  const mine: string[] = [];
  let out = "", last = 0;
  const parts: { a: number; b: number; k: string }[] = [...s.matchAll(ZONES)].map((m) => ({ a: m.index!, b: m.index! + m[0].length, k: m[0].startsWith("<") || m[0].startsWith("http") ? "skip" : "math" }));
  const seg = (a: number, b: number, k: string) => {
    let t = s.slice(a, b);
    if (k === "skip") return t;
    if (k === "math") { // bỏ dấu phân cách để braceInfo đúng
      const m = /^(\$\$|\$|\\\(|\\\[)([\s\S]*?)(\$\$|\$|\\\)|\\\])$/.exec(t);
      return m ? m[1] + rewrite(m[2], true, mine) + m[3] : t;
    }
    return rewrite(t, false, mine);
  };
  for (const p of parts) { out += seg(last, p.a, "text") + seg(p.a, p.b, p.k); last = p.b; }
  out += seg(last, s.length, "text");
  if (out === s) return s;
  if (((out.replace(/\\\$/g, "").match(/\$/g)?.length ?? 0) % 2) === 1 || (out.match(/\$\$/g)?.length ?? 0) > (s.match(/\$\$/g)?.length ?? 0)) { skipped.push("TỰ KIỂM $: " + s.slice(0, 70)); return s; }
  for (const m of out.matchAll(/\$\$([\s\S]*?)\$\$|\$([^$]*)\$/g)) {
    try { katex.renderToString(m[1] ?? m[2], { throwOnError: true, strict: "ignore" }); } catch (e) { skipped.push("KATEX LỖI: " + (m[1] ?? m[2]).slice(0, 70)); return s; }
  }
  ch.push(...mine);
  return out;
}
function mapStrings(v: any, f: (s: string) => string, key = ""): any {
  if (typeof v === "string") return SKIP_KEYS.has(key) ? v : f(v);
  if (Array.isArray(v)) return v.map((x) => mapStrings(x, f, key));
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, mapStrings(x, f, k)]));
  return v;
}
if (UNDO) {
  const bk = JSON.parse(fs.readFileSync(UNDO, "utf8")) as { id: number; question: unknown }[];
  for (const r of bk) { const { error } = await sb.from("question_bank").update({ question: r.question }).eq("id", r.id); if (error) { console.error("LỖI id", r.id, error.message); process.exit(1); } }
  console.log("ĐÃ HOÀN TÁC", bk.length); process.exit(0);
}
const report: { id: number; changes: string[] }[] = [], backup: { id: number; question: unknown }[] = [], news = new Map<number, unknown>(), skipped: string[] = [];
let from = 0, scanned = 0, nChange = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    scanned++;
    const ch: string[] = [];
    const nq = EXCLUDE_IDS.has(r.id) ? r.question : mapStrings(r.question, (s) => fixString(s, ch, skipped));
    if (ch.length) { report.push({ id: r.id, changes: ch }); backup.push({ id: r.id, question: r.question }); news.set(r.id, nq); nChange += ch.length; }
  }
  from += 1000;
}
for (const id of (process.env.SHOW ?? "").split(",").filter(Boolean).map(Number)) console.log("\n#" + id, JSON.stringify(news.get(id), null, 1).slice(0, 1800));
const rp = path.join(logs, `sua-don-vi-luc-${APPLY ? "apply" : "dry"}-${stamp}.json`);
fs.writeFileSync(rp, JSON.stringify({ skipped, report }, null, 2));
console.log(APPLY ? "ĐANG GHI" : "DRY-RUN", `· quét ${scanned} · câu đổi ${backup.length} · chỗ đổi ${nChange} · bỏ qua ${skipped.length} →`, path.relative(process.cwd(), rp));
if (APPLY) {
  const bp = path.join(logs, `backup-don-vi-luc-${stamp}.json`);
  fs.writeFileSync(bp, JSON.stringify(backup));
  console.log("Sao lưu:", path.relative(process.cwd(), bp));
  for (const b of backup) { const { error } = await sb.from("question_bank").update({ question: news.get(b.id) }).eq("id", b.id); if (error) { console.error("LỖI id", b.id, error.message, "→ --undo", bp); process.exit(1); } }
  let bad = 0; const ids = backup.map((b) => b.id);
  for (let i = 0; i < ids.length; i += 200) { const { data } = await sb.from("question_bank").select("id, question").in("id", ids.slice(i, i + 200)); for (const r of data ?? []) if (JSON.stringify(r.question) !== JSON.stringify(news.get(r.id))) bad++; }
  console.log(bad ? `LỆCH ${bad} câu sau khi ghi!` : `Đã đọc lại ${ids.length} câu: khớp bản mới.`);
}
