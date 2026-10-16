// Sửa số mũ dính liền (không dấu nhân/^): (A) mũ ÂM "10-9 C", "10−6 N" tự sửa theo luật chặt; (B) mũ dương chỉ sửa theo danh sách ĐÃ DUYỆT TAY
// (id + cụm ngữ cảnh), vì "108 km/h", "1030 kg/m3 nước biển" là số thật. Ca còn lại → scripts/data/duyet/mu-dinh-lien-2026-10-16/items.json.
//   npx tsx scripts/sua-mu-dinh-lien.mts [--apply]   (sao lưu ra scripts/logs/backup-mu-dinh-lien-*.json)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const NEG = /(?<![\d.,^{_\-−–A-Za-z\/(])10([-−])(\d{1,2})(?![\d,.]?\d)(?=(?:\s|\\,|&nbsp;|<br\s*\/?>)*(?:C|N|T|J|F|V|s|giây|Wb|W|m|kg|g|A|Hz|K|mT|\.|,|\)|;|$|\$|<))/g;
// [id, cụm ngữ cảnh (khoảng trắng tuỳ ý), token mũ dương trong cụm]
const POS: [number, string, string][] = [
  [457123, "bắn vào 1010 hạt", "1010"], [673211, "kích thích cho 1010 hạt", "1010"], [673588, "kích thích cho 1010 hạt", "1010"],
  [453387, "mỗi 1012 nguyên tử", "1012"], [393373, "bao nhiêu 1025 J", "1025"], [432517, "đơn vị 1013 J", "1013"], [465823, "đơn vị 1013 J", "1013"],
  [456902, "đơn vị 102 T", "102"], [626989, "đơn vị 1025 MeV", "1025"], [672151, "×1026 MeV", "1026"], [1193590, "theo 104 V/m", "104"],
  [642763, "đơn vị: 104 J/kg", "104"], [590993, "đơn vị 106 là", "106"], [1195397, "đơn vị 103V", "103"], [682316, "đơn vị 108W", "108"],
  [682513, "công 107J", "107"], [578111, "tần số 106 Hz", "106"], [1228662, "f = 1014 Hz", "1014"], [1229394, "tần số 108 Hz", "108"],
  [1248403, "tần số 108 Hz", "108"], [1237376, "f = 106 Hz", "106"], [523793, "ban đầu là 109 Bq", "109"], [681056, "1 kN = 103 N", "103"],
  [670227, "1MJ = 106J", "106"], [413924, "nước là 103 kg", "103"], [571246, "nước là 103 kg", "103"], [672537, "nước là 103 kg", "103"],
  [672581, "ρ = 103 kg", "103"], [672656, "nước là 103 kg", "103"], [672689, "ρ = 103 kg", "103"], [661768, "v = 105 m/s", "105"],
  [1194584, "ban đầu là 106 m/s", "106"], [1180470, "E = 104 V/m", "104"], [1182048, "giá trị 104 V/m", "104"], [1187849, "E = 106 V/m", "106"],
  [1186340, "cường độ 106 V/m", "106"], [1185396, "x 106 V/m", "106"], [607417, "khoảng 104)", "104"],
];
const ZONE = /\$\$[\s\S]*?\$\$|\$[^$]*\$|<[^>]*>/g;
const mk = (zone: "math" | "text", sign: string, e: string) => (zone === "math" ? `10^{${sign}${e}}` : `10<sup>${sign}${e}</sup>`);
function fix(s: string, id: number, log: string[]): string {
  const zs = [...s.matchAll(ZONE)].map((m) => ({ a: m.index!, b: m.index! + m[0].length, tag: m[0].startsWith("<") }));
  const zoneAt = (i: number) => zs.find((x) => i >= x.a && i < x.b);
  const edits: { a: number; b: number; r: string }[] = [];
  for (const m of s.matchAll(NEG)) {
    const z = zoneAt(m.index!); if (z?.tag) continue;
    if (/\d\s*$/.test(s.slice(Math.max(0, m.index! - 3), m.index!))) continue;
    edits.push({ a: m.index!, b: m.index! + m[0].length, r: mk(z ? "math" : "text", "−".replace("−", z ? "-" : "−"), m[2]) });
  }
  for (const [pid, ctx, tok] of POS) {
    if (pid !== id) continue;
    const re = new RegExp(ctx.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/ /g, "(?:\\s|&nbsp;)*"), "g");
    for (const m of s.matchAll(re)) {
      const off = m[0].indexOf(tok), i = m.index! + off, z = zoneAt(i);
      if (z?.tag) continue;
      edits.push({ a: i, b: i + tok.length, r: mk(z ? "math" : "text", "", tok.slice(2)) });
    }
  }
  edits.sort((x, y) => x.a - y.a);
  let out = "", last = 0;
  for (const e of edits) { if (e.a < last) continue; out += s.slice(last, e.a) + e.r; last = e.b; log.push(`${id} ${s.slice(Math.max(0, e.a - 25), e.b + 10).replace(/\s+/g, " ")}  =>  ${e.r}`); }
  return out + s.slice(last);
}
const map = (v: any, f: (s: string) => string): any => typeof v === "string" ? f(v) : Array.isArray(v) ? v.map((x) => map(x, f)) : v && typeof v === "object" ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, map(x, f)])) : v;
const backup: any[] = [], log: string[] = []; let from = 0, n = 0; const T = Date.now();
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    const l: string[] = []; const nq = map(r.question, (s) => fix(s, r.id, l));
    if (!l.length) continue;
    log.push(...l); n++; backup.push({ id: r.id, question: r.question });
    if (APPLY) { fs.writeFileSync(`scripts/logs/backup-mu-dinh-lien-${T}.json`, JSON.stringify(backup)); const { error: e2 } = await sb.from("question_bank").update({ question: nq }).eq("id", r.id); if (e2) { console.error(r.id, e2.message); process.exit(1); } }
  }
  from += 1000;
}
fs.writeFileSync(`scripts/logs/sua-mu-dinh-lien-${APPLY ? "apply" : "dry"}-${T}.log`, log.join("\n"));
console.log(APPLY ? "ĐÃ GHI" : "DRY-RUN", "· câu", n, "· chỗ", log.length); if (!APPLY) console.log(log.join("\n"));
