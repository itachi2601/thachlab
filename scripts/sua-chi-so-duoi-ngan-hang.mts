// Sửa ký hiệu thiếu chỉ số dưới trong question_bank: S1 → $S_1$, p2 → $p_2$ (ngoài công thức); trong $…$ viết S_1.
//   npx tsx scripts/sua-chi-so-duoi-ngan-hang.mts                        # DRY-RUN: chỉ ghi báo cáo vào scripts/logs/
//   npx tsx scripts/sua-chi-so-duoi-ngan-hang.mts --apply                # sao lưu nguyên văn ra scripts/logs/ rồi ghi, rồi đọc lại đối chiếu
//   npx tsx scripts/sua-chi-so-duoi-ngan-hang.mts --undo <file-backup>   # hoàn tác từ file sao lưu
// Chỉ đụng chữ cái vật lí trong WHITELIST + MỘT chữ số. Bỏ qua hoá học (N2, O2, H2), đơn vị (m2, m3, /s2), URL, thẻ HTML,
// chỉ số đã nằm trong _{…}/^{…}, chuỗi lẻ dấu $. Không đổi content_hash.
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
const UNDO = process.argv.includes("--undo") ? process.argv[process.argv.indexOf("--undo") + 1] : null;
const logs = path.join(scriptDir, "logs");
const stamp = Date.now();

// Id đã dò tay (15/10/2026) thấy m2/x2/v2 là đơn vị/bình phương, URL hoặc \frac d2 — giữ nguyên bản gốc, KHÔNG sửa lại.
const EXCLUDE_IDS = new Set([674791,685403,1475085,682980,673821,382975,393403,393606,401573,412937,421597,423778,424738,453385,456281,456548,456620,456675,456761,456903,456959,456980,457714,457747,458482,458579,465848,465849,523774,523850,523814,570413,571220,579738,583765,589471,592110,594378,595379,595383,595384,600507,614490,627230,642053,647461,650382,655619,655626,655627,661767,668251,673195,673203,673753,673766,673769,673801,673940,673966,673994,674261,680715,681346,681898,683015,683437,683799,684028,685079,1182344,1473296,1473476,1475857,1476160,456191,7955,680969,681570,684059,646583,603560,1167005,1245670,681402]);
const WHITELIST = "pTVtmMvFqdRQIUSyanPEkrhL"; // bỏ x: x2 thường là bình phương
const RE = new RegExp(`(?<![A-Za-z_\\\\.,^₀-₉⁰-⁹])([${WHITELIST}])([0-9])(?!(?![A-Za-z][0-9])[A-Za-z0-9_])`, "g");
const SKIP_KEYS = new Set(["answer", "topic", "type", "form", "difficulty", "difficultySource", "id", "key", "kind"]);
const MATH_OR_TAG = /https?:\/\/[^\s"'<>)]+|\$\$[\s\S]*?\$\$|\$[^$]*\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|<[^>]*>/g;

function inSubSup(zone: string, off: number): boolean {
  const stack: boolean[] = [];
  for (let i = 0; i < off; i++) {
    const c = zone[i];
    if (c === "\\") { i++; continue; }
    if (c === "{") stack.push(i > 0 && (zone[i - 1] === "_" || zone[i - 1] === "^"));
    else if (c === "}") stack.pop();
  }
  return stack.some(Boolean);
}

type Change = { before: string; after: string };
function fixString(s: string, changes: Change[], skipped: string[]): string {
  if (/^(https?:|data:)/.test(s)) return s;
  const stripped = s.replace(/\\\$/g, "");
  if ((stripped.match(/\$/g)?.length ?? 0) % 2 === 1) { if (RE.test(s)) skipped.push("lẻ $: " + s.slice(0, 60)); RE.lastIndex = 0; return s; }
  const zones = [...s.matchAll(MATH_OR_TAG)].map((m) => ({ a: m.index!, b: m.index! + m[0].length, k: m[0].startsWith("<") || m[0].startsWith("http") ? "tag" : "math" }));
  let out = "", last = 0, lastWrapEnd = -1;
  for (const m of s.matchAll(RE)) {
    const i = m.index!;
    const z = zones.find((x) => i >= x.a && i < x.b);
    if (z?.k === "tag") continue;
    const [tok, letter, digit] = m;
    const prev = s[i - 1] ?? "";
    // đối số không ngoặc của \dfrac d2, \sqrt x2: d_2 sẽ lỗi KaTeX/sai nghĩa
    if (z && /\\(?:[dt]?frac|sqrt)\s*[A-Za-z0-9]?\s*$/.test(s.slice(Math.max(0, i - 14), i))) continue;
    // 2p1, 3T2 được sửa; nhưng 3x2 (đa thức), 1E5 (khoa học), 2m3/5h2 (đơn vị) thì giữ
    if (/\d/.test(prev) && "mdhxE".includes(letter)) continue;
    // km/h2, N/m2: đơn vị có mũ
    if (prev === "/" && "mh".includes(letter) && /[A-Za-z]$/.test(s.slice(Math.max(0, i - 3), i - 1))) continue;
    // chữ thường + 2/3 sau số/phép nhân, hoặc trước "/": thường là bình phương (2t2, m2⋅A2, v2/r)
    if (digit === "2" || digit === "3") {
      if ("matdrh".includes(letter) && /\d$/.test(s.slice(Math.max(0, i - 2), i).trimEnd())) continue;
      if ("mh".includes(letter) && /[⋅·*]$/.test(s.slice(Math.max(0, i - 2), i).trimEnd())) continue;
      if ("mvatrh".includes(letter) && s[i + tok.length] === "/") continue;
    }
    // đơn vị m2/m3 (có số hoặc / đứng trước): bỏ qua
    if (letter === "m" && (digit === "2" || digit === "3") && /(\d|\/)\s*$/.test(s.slice(Math.max(0, i - 3), i))) continue;
    // chữ cái ghép liền sau là tên hàm (sin, cos, ...) đã bị lookbehind chặn; tránh nằm trong \text{…}
    if (z && inSubSup(s.slice(z.a, z.b), i - z.a)) continue;
    let rep = z ? `${letter}_${digit}` : `$${letter}_${digit}$`;
    // p1V1 → $p_1V_1$ (không để "$$" liền nhau vì sẽ thành công thức khối)
    if (!z && last === i && i > 0 && out.endsWith("$") && lastWrapEnd === i) { out = out.slice(0, -1); rep = rep.slice(1); }
    out += s.slice(last, i) + rep; last = i + tok.length;
    lastWrapEnd = z ? -1 : last;
    changes.push({ before: s.slice(Math.max(0, i - 20), i + 20).replace(/\s+/g, " "), after: (s.slice(Math.max(0, i - 20), i) + rep + s.slice(i + tok.length, i + 20)).replace(/\s+/g, " ") });
  }
  const res = out + s.slice(last);
  // tự kiểm: số $ vẫn chẵn, không sinh "$$" mới
  if (res !== s && ((res.replace(/\\\$/g, "").match(/\$/g)?.length ?? 0) % 2 === 1 || (res.match(/\$\$/g)?.length ?? 0) > (s.match(/\$\$/g)?.length ?? 0))) {
    skipped.push("TỰ KIỂM HỎNG: " + s.slice(0, 80)); changes.length = 0; return s;
  }
  return res;
}
function mapStrings(v: any, f: (s: string) => string, key = ""): any {
  if (typeof v === "string") return SKIP_KEYS.has(key) ? v : f(v);
  if (Array.isArray(v)) return v.map((x) => mapStrings(x, f, key));
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, mapStrings(x, f, k)]));
  return v;
}

if (UNDO) {
  const bk = JSON.parse(fs.readFileSync(UNDO, "utf8")) as { id: number; question: unknown }[];
  for (const r of bk) {
    const { error } = await sb.from("question_bank").update({ question: r.question }).eq("id", r.id);
    if (error) { console.error("LỖI id", r.id, error.message); process.exit(1); }
  }
  console.log("ĐÃ HOÀN TÁC", bk.length, "câu từ", UNDO);
  process.exit(0);
}

// SIM=<file-sao-lưu>: chạy luật hiện tại trên bản sao lưu rồi so với DB hiện tại, in id nào khác (đã sửa bằng luật cũ/lỏng hơn).
if (process.env.SIM) {
  const canon = (v: any): any => Array.isArray(v) ? v.map(canon) : v && typeof v === "object" ? Object.fromEntries(Object.keys(v).sort().map((k) => [k, canon(v[k])])) : v;
  const bk = JSON.parse(fs.readFileSync(process.env.SIM, "utf8")) as { id: number; question: any }[];
  const diff: number[] = [];
  for (let i = 0; i < bk.length; i += 200) {
    const part = bk.slice(i, i + 200);
    const { data } = await sb.from("question_bank").select("id, question").in("id", part.map((b) => b.id));
    const cur = new Map((data ?? []).map((r: any) => [r.id, r.question]));
    for (const b of part) {
      const nq = EXCLUDE_IDS.has(b.id) ? b.question : mapStrings(b.question, (x) => fixString(x, [], []));
      // so riêng các khoá có trong bản sao lưu (DB có thể có thêm khoá backfill sau này)
      const c = cur.get(b.id);
      const sub = (n: any, o: any) => JSON.stringify(canon(Object.fromEntries(Object.keys(n).map((k) => [k, o?.[k]]))));
      if (sub(nq, c) !== JSON.stringify(canon(nq))) {
        diff.push(b.id);
        if (process.env.SIMV && diff.length <= Number(process.env.SIMV)) {
          const a = JSON.stringify(canon(nq)), d = sub(nq, c); let j = 0; while (a[j] === d[j]) j++;
          console.log("#" + b.id, "\n  mới(luật):", a.slice(Math.max(0, j - 50), j + 60), "\n  DB      :", d.slice(Math.max(0, j - 50), j + 60));
        }
      }
    }
  }
  if (process.env.SIM_OUT) fs.writeFileSync(process.env.SIM_OUT, JSON.stringify(diff));
  console.log("SIM: id khác DB hiện tại:", diff.length, JSON.stringify(diff));
  process.exit(0);
}
const report: { id: number; changes: Change[] }[] = [], backup: { id: number; question: unknown }[] = [], news = new Map<number, unknown>();
const skipped: string[] = [];
let from = 0, scanned = 0, nChange = 0;
for (;;) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("archived", false).order("id").range(from, from + 999);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const r of data) {
    scanned++;
    const changes: Change[] = [];
    const nq = EXCLUDE_IDS.has(r.id) ? r.question : mapStrings(r.question, (s) => fixString(s, changes, skipped));
    if (changes.length) { report.push({ id: r.id, changes }); backup.push({ id: r.id, question: r.question }); news.set(r.id, nq); nChange += changes.length; }
  }
  from += 1000;
}
for (const id of (process.env.SHOW ?? "").split(",").filter(Boolean).map(Number)) console.log("\n#" + id, JSON.stringify(news.get(id), null, 1).slice(0, 1800));
const rp = path.join(logs, `sua-chi-so-duoi-${APPLY ? "apply" : "dry"}-${stamp}.json`);
fs.writeFileSync(rp, JSON.stringify({ skipped, report }, null, 2));
console.log(APPLY ? "ĐANG GHI" : "DRY-RUN", `· quét ${scanned} · câu đổi ${backup.length} · chỗ đổi ${nChange} · bỏ qua(lẻ $) ${skipped.length} →`, path.relative(process.cwd(), rp));
if (APPLY) {
  const bp = path.join(logs, `backup-chi-so-duoi-${stamp}.json`);
  fs.writeFileSync(bp, JSON.stringify(backup));
  console.log("Sao lưu:", path.relative(process.cwd(), bp));
  for (const b of backup) {
    const { error } = await sb.from("question_bank").update({ question: news.get(b.id) }).eq("id", b.id);
    if (error) { console.error("LỖI id", b.id, error.message, "→ hoàn tác: --undo", bp); process.exit(1); }
  }
  // đối chiếu: đọc lại từ DB
  let bad = 0;
  const ids = backup.map((b) => b.id);
  for (let i = 0; i < ids.length; i += 200) {
    const { data } = await sb.from("question_bank").select("id, question").in("id", ids.slice(i, i + 200));
    for (const r of data ?? []) if (JSON.stringify(r.question) !== JSON.stringify(news.get(r.id))) bad++;
  }
  console.log(bad ? `LỆCH ${bad} câu sau khi ghi!` : `Đã đọc lại ${ids.length} câu: khớp bản mới.`);
}
