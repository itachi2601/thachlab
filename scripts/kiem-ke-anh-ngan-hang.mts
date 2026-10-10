// Kiểm kê ảnh trong ngân hàng câu hỏi — CHỈ ĐỌC, KHÔNG GHI DB.
// Liệt kê câu (archived=false) có <img>, phân loại theo đề bài (đồ thị / mạch điện / sơ đồ / hình vẽ / khác),
// tải từng ảnh (chỉ HEAD + vài trăm byte đầu) để đo kích thước điểm ảnh và dung lượng → xếp mức "xấu".
//   npx tsx scripts/kiem-ke-anh-ngan-hang.mts            # toàn bộ
//   npx tsx scripts/kiem-ke-anh-ngan-hang.mts --no-fetch # không tải ảnh, chỉ đếm theo text
// Kết quả: scripts/data/kiem-ke-anh-ngan-hang/{rows.json,summary.md}
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
const NO_FETCH = process.argv.includes("--no-fetch");

type Row = {
  id: number; grade: string | null; topic_name: string | null; qtype: string | null;
  source_exam_id: number | null; question: Record<string, unknown>;
};

const IMG_RE = /<img\b[^>]*?src="([^"]+)"/gi;
const strip = (s: string) => s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").toLowerCase();

function classify(stemText: string): string {
  if (/đồ thị/.test(stemText)) return "do_thi";
  if (/mạch điện|mạch như|sơ đồ mạch/.test(stemText)) return "mach_dien";
  if (/sơ đồ|bố trí thí nghiệm|thí nghiệm như hình/.test(stemText)) return "so_do";
  if (/hình vẽ|hình bên|hình dưới|hình trên|như hình/.test(stemText)) return "hinh_ve";
  return "khac";
}

function htmlParts(q: Record<string, unknown>): { stem: string; rest: string } {
  const stem = typeof q.question === "string" ? q.question : "";
  const parts: string[] = [];
  if (Array.isArray(q.options)) parts.push(...(q.options as string[]));
  if (Array.isArray(q.statements)) parts.push(...(q.statements as { text?: string }[]).map((s) => s.text ?? ""));
  return { stem, rest: parts.join("\n") };
}

// --- đọc toàn bộ ngân hàng theo trang ---
const PAGE = 1000;
const rows: Row[] = [];
for (let from = 0; ; from += PAGE) {
  const { data, error } = await supabase
    .from("question_bank")
    .select("id, grade, topic_name, qtype, source_exam_id, question")
    .eq("archived", false)
    .or("question->>question.imatch.<img,question->>options.imatch.<img,question->>statements.imatch.<img")
    .order("id")
    .range(from, from + PAGE - 1);
  if (error) { console.error(error.message); process.exit(1); }
  rows.push(...((data ?? []) as Row[]));
  process.stderr.write(`\rđọc ${rows.length} câu`);
  if (!data || data.length < PAGE) break;
}
process.stderr.write("\n");

type Out = {
  id: number; grade: string | null; topic: string | null; qtype: string | null; exam: number | null;
  loai: string; srcs: string[]; n_img: number; base64: boolean; o_phuong_an: boolean;
  anh?: { src: string; bytes: number | null; w: number | null; h: number | null; mime: string | null; loi?: string }[];
};
const out: Out[] = [];
for (const r of rows) {
  const { stem, rest } = htmlParts(r.question);
  const srcs = [...stem.matchAll(IMG_RE), ...rest.matchAll(IMG_RE)].map((m) => m[1]);
  if (!srcs.length) continue;
  out.push({
    id: r.id, grade: r.grade, topic: r.topic_name, qtype: r.qtype, exam: r.source_exam_id,
    loai: classify(strip(stem)), srcs, n_img: srcs.length,
    base64: srcs.some((s) => s.startsWith("data:")),
    o_phuong_an: IMG_RE.test(rest) && (IMG_RE.lastIndex = 0, true),
  });
}
console.log(`câu có ảnh: ${out.length} (server lọc trả ${rows.length})`);

// --- đo ảnh: đọc header PNG/JPEG/GIF/WebP từ byte đầu ---
function dims(buf: Uint8Array): { w: number; h: number; mime: string } | null {
  const b = buf;
  if (b.length > 24 && b[0] === 0x89 && b[1] === 0x50) {
    const dv = new DataView(b.buffer, b.byteOffset);
    return { w: dv.getUint32(16), h: dv.getUint32(20), mime: "png" };
  }
  if (b.length > 10 && b[0] === 0x47 && b[1] === 0x49) {
    return { w: b[6] | (b[7] << 8), h: b[8] | (b[9] << 8), mime: "gif" };
  }
  if (b.length > 30 && b[8] === 0x57 && b[9] === 0x45 && b[10] === 0x42 && b[11] === 0x50) {
    // WebP VP8/VP8L/VP8X — lấy kích thước từ VP8X (canvas) nếu có
    if (b[12] === 0x56 && b[13] === 0x50 && b[14] === 0x38 && b[15] === 0x58) {
      return { w: 1 + (b[24] | (b[25] << 8) | (b[26] << 16)), h: 1 + (b[27] | (b[28] << 8) | (b[29] << 16)), mime: "webp" };
    }
    if (b[15] === 0x20) return { w: b[26] | (b[27] << 8), h: b[28] | (b[29] << 8), mime: "webp" };
    return { w: 0, h: 0, mime: "webp" };
  }
  if (b.length > 4 && b[0] === 0xff && b[1] === 0xd8) {
    let i = 2;
    while (i + 9 < b.length) {
      if (b[i] !== 0xff) { i++; continue; }
      const m = b[i + 1];
      if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) {
        return { h: (b[i + 5] << 8) | b[i + 6], w: (b[i + 7] << 8) | b[i + 8], mime: "jpeg" };
      }
      const len = (b[i + 2] << 8) | b[i + 3];
      i += 2 + len;
    }
    return { w: 0, h: 0, mime: "jpeg" };
  }
  if (b.length > 5 && b[0] === 0x3c) return { w: 0, h: 0, mime: "svg" };
  return null;
}

type Anh = NonNullable<Out["anh"]>[number];
const cache = new Map<string, Anh>();
const PUBLIC_DIR = path.resolve(scriptDir, "..", "public");

// Ảnh cục bộ (/lessons/...): đọc thẳng từ public/
function measureLocal(src: string): Anh {
  const rec: Anh = { src, bytes: null, w: null, h: null, mime: null };
  const file = path.join(PUBLIC_DIR, decodeURIComponent(src.split("?")[0]));
  try {
    const fd = fs.openSync(file, "r");
    const buf = new Uint8Array(64 * 1024);
    const n = fs.readSync(fd, buf, 0, buf.length, 0);
    fs.closeSync(fd);
    rec.bytes = fs.statSync(file).size;
    const d = dims(buf.subarray(0, n));
    if (d) Object.assign(rec, d); else rec.loi = "không đọc được header";
  } catch { rec.loi = "không có file trong public/"; }
  return rec;
}

// Ảnh Supabase storage: dung lượng qua API liệt kê thư mục (không tải), kích thước chỉ đo cho nhóm cần.
const STORAGE_RE = /\/storage\/v1\/object\/public\/([^/]+)\/(.+)$/;
async function listSizes(srcs: string[]) {
  const folders = new Map<string, Set<string>>(); // "bucket|folder" → tên file
  for (const s of srcs) {
    const m = s.match(STORAGE_RE); if (!m) continue;
    const full = decodeURIComponent(m[2].split("?")[0]);
    const folder = full.includes("/") ? full.slice(0, full.lastIndexOf("/")) : "";
    const k = `${m[1]}|${folder}`;
    if (!folders.has(k)) folders.set(k, new Set());
    folders.get(k)!.add(full.slice(folder.length + (folder ? 1 : 0)));
  }
  const sizes = new Map<string, { bytes: number; mime: string | null }>();
  let done = 0;
  const keys = [...folders.keys()];
  const workers = Array.from({ length: 6 }, async () => {
    while (keys.length) {
      const k = keys.shift()!;
      const [bucket, folder] = k.split("|");
      for (let offset = 0; ; offset += 1000) {
        const { data, error } = await supabase.storage.from(bucket).list(folder, { limit: 1000, offset });
        if (error || !data) break;
        for (const f of data) {
          const meta = f.metadata as { size?: number; mimetype?: string } | null;
          if (meta?.size !== undefined) sizes.set(`${bucket}/${folder ? folder + "/" : ""}${f.name}`, { bytes: meta.size, mime: meta.mimetype ?? null });
        }
        if (data.length < 1000) break;
      }
      done++;
      if (done % 20 === 0) process.stderr.write(`\rliệt kê thư mục ${done}/${folders.size}`);
    }
  });
  await Promise.all(workers);
  process.stderr.write("\n");
  return sizes;
}

async function measureRemoteDims(rec: Anh) {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 15000);
    const res = await fetch(rec.src, { headers: { Range: "bytes=0-32767" }, signal: ctrl.signal });
    const buf = new Uint8Array(await res.arrayBuffer());
    clearTimeout(t);
    const d = dims(buf);
    if (d) Object.assign(rec, d); else rec.loi = `không đọc được header (HTTP ${res.status})`;
  } catch (e) { rec.loi = (e as Error).message; }
}

if (!NO_FETCH) {
  const all = [...new Set(out.flatMap((o) => o.srcs))];
  console.log(`ảnh duy nhất cần đo: ${all.length}`);
  const remote = all.filter((s) => STORAGE_RE.test(s));
  const local = all.filter((s) => s.startsWith("/"));
  const other = all.filter((s) => !STORAGE_RE.test(s) && !s.startsWith("/"));
  console.log(`  cục bộ public/: ${local.length} · Supabase storage: ${remote.length} · khác (base64/URL ngoài): ${other.length}`);
  for (const s of local) cache.set(s, measureLocal(s));
  for (const s of other) {
    const rec: Anh = { src: s, bytes: null, w: null, h: null, mime: null };
    if (s.startsWith("data:")) {
      const buf = Buffer.from(s.slice(s.indexOf(",") + 1), "base64");
      rec.bytes = buf.length; const d = dims(buf.subarray(0, 64 * 1024)); if (d) Object.assign(rec, d);
    } else rec.loi = "URL ngoài, không đo";
    cache.set(s, rec);
  }
  const sizes = await listSizes(remote);
  for (const s of remote) {
    const m = s.match(STORAGE_RE)!;
    const keyS = `${m[1]}/${decodeURIComponent(m[2].split("?")[0])}`;
    const sz = sizes.get(keyS);
    cache.set(s, { src: s, bytes: sz?.bytes ?? null, w: null, h: null, mime: sz?.mime?.split("/")[1] ?? null, ...(sz ? {} : { loi: "không thấy trong storage" }) });
  }
  // đo kích thước điểm ảnh chỉ cho ảnh của câu đồ thị / mạch điện (nhóm sẽ vẽ lại)
  const need = [...new Set(out.filter((o) => o.loai === "do_thi" || o.loai === "mach_dien").flatMap((o) => o.srcs))]
    .filter((s) => STORAGE_RE.test(s) && !cache.get(s)?.loi);
  console.log(`đo kích thước điểm ảnh cho ${need.length} ảnh đồ thị/mạch điện`);
  let done = 0;
  const workers = Array.from({ length: 16 }, async () => {
    while (need.length) {
      await measureRemoteDims(cache.get(need.shift()!)!);
      done++;
      if (done % 50 === 0) process.stderr.write(`\rđo ${done}`);
    }
  });
  await Promise.all(workers);
  process.stderr.write("\n");
  for (const o of out) o.anh = o.srcs.map((s) => cache.get(s)!);
}

// --- xếp mức xấu: nhỏ (<400px rộng) hoặc jpeg hoặc mật độ thấp ---
function mucXau(o: Out): string {
  if (!o.anh) return "?";
  if (o.base64) return "base64";
  let worst = "ok";
  for (const a of o.anh) {
    if (a.loi) return "loi_tai";
    if (a.mime === "svg") continue;
    const w = a.w ?? 0;
    if (!w) { if (a.bytes !== null && a.bytes < 8000) worst = worst === "ok" ? "nho_<8KB" : worst; continue; }
    if (w < 40 || (a.h ?? 0) < 30) { if (worst === "ok") worst = "cong_thuc_anh"; continue; } // ảnh công thức MathType, không phải hình
    if (w && w < 300) worst = "rat_xau";
    else if ((w && w < 500) || a.mime === "jpeg") worst = worst === "rat_xau" ? worst : "xau";
    else if (a.bytes && w && a.h && a.bytes / (w * a.h) < 0.15) worst = worst === "ok" ? "mo" : worst;
  }
  return worst;
}

const outDir = path.join(scriptDir, "data", "kiem-ke-anh-ngan-hang");
fs.mkdirSync(outDir, { recursive: true });
const final = out.map((o) => ({ ...o, muc: mucXau(o) }));
fs.writeFileSync(path.join(outDir, "rows.json"), JSON.stringify(final, null, 1));

const count = (f: (o: typeof final[number]) => string) => {
  const m = new Map<string, number>();
  for (const o of final) m.set(f(o), (m.get(f(o)) ?? 0) + 1);
  return [...m.entries()].sort((a, b) => b[1] - a[1]);
};
const table = (title: string, pairs: [string, number][]) =>
  `\n### ${title}\n\n| | số câu |\n|---|---:|\n${pairs.map(([k, v]) => `| ${k} | ${v} |`).join("\n")}\n`;

let md = `# Kiểm kê ảnh ngân hàng câu hỏi — ${new Date().toISOString().slice(0, 10)}\n\n`;
md += `- Câu có ảnh: ${final.length}\n- Ảnh duy nhất: ${cache.size || "(không đo)"}\n`;
md += table("Theo loại hình (đoán từ đề bài)", count((o) => o.loai));
md += table("Theo lớp", count((o) => o.grade ?? "?"));
md += table("Theo mức xấu", count((o) => o.muc));
md += table("Loại × mức", count((o) => `${o.loai} / ${o.muc}`));
md += table("Số ảnh trong câu", count((o) => String(o.n_img)));
md += table("Ảnh nằm ở phương án", count((o) => (o.o_phuong_an ? "có" : "không")));
if (cache.size) {
  const ws = [...cache.values()].map((a) => a.w ?? 0).filter(Boolean).sort((a, b) => a - b);
  const q = (p: number) => ws[Math.floor(ws.length * p)];
  md += `\n### Bề rộng ảnh (px)\n\n| p10 | p25 | p50 | p75 | p90 |\n|---:|---:|---:|---:|---:|\n| ${q(0.1)} | ${q(0.25)} | ${q(0.5)} | ${q(0.75)} | ${q(0.9)} |\n`;
  const fm = new Map<string, number>();
  for (const a of cache.values()) { const k = a.mime ?? "?"; fm.set(k, (fm.get(k) ?? 0) + 1); }
  md += table("Định dạng", [...fm.entries()].sort((a, b) => b[1] - a[1]));
}
md += `\n### Ví dụ đồ thị xấu nhất (20 câu)\n\n`;
for (const o of final.filter((o) => o.loai === "do_thi" && (o.muc === "rat_xau" || o.muc === "xau")).slice(0, 20)) {
  md += `- #${o.id} L${o.grade} ${o.topic ?? ""} — ${o.anh?.map((a) => `${a.w}×${a.h} ${a.mime}`).join(", ")}\n`;
}
fs.writeFileSync(path.join(outDir, "summary.md"), md);
console.log(md);
console.log(`→ ${path.relative(process.cwd(), outDir)}/`);
