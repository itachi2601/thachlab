// Tìm ảnh có LỀ TRẮNG quá lớn: nét vẽ chỉ chiếm một khoảng nhỏ giữa khung, phần còn lại là nền (kiểu câu 11, 13 đề 918).
// CHỈ ĐỌC, KHÔNG GHI DB. Đo hộp bao của điểm ảnh khác màu nền (màu phổ biến nhất ở 4 góc) rồi so với cả khung ảnh.
//   npx tsx scripts/kiem-anh-le-trang.mts --exam 918        # một đề (cột exams.questions)
//   npx tsx scripts/kiem-anh-le-trang.mts --bank            # toàn ngân hàng (archived=false)
//   thêm --max 0.35 để đổi ngưỡng (mặc định: hộp nét vẽ < 35% diện tích khung thì báo)
// Ra: scripts/data/kiem-ke-anh-ngan-hang/anh-le-trang.{json,md}
import { createClient } from "@supabase/supabase-js";
import sharp from "sharp";
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

const arg = (n: string) => { const i = process.argv.indexOf(n); return i >= 0 ? process.argv[i + 1] : undefined; };
const EXAM = arg("--exam");
const BANK = process.argv.includes("--bank");
const MAX_FRAC = Number(arg("--max") ?? 0.35);
const ALL = process.argv.includes("--all"); // đo mọi ảnh (chậm); mặc định chỉ đo ảnh cao ≥ --min-h (900 px)
const MIN_H = Number(arg("--min-h") ?? 900);
if (!EXAM && !BANK) { console.error("cần --exam <id> hoặc --bank"); process.exit(1); }

const SITE = "https://thachlab.id.vn";
const IMG_RE = /<img\b[^>]*?src="([^"]+)"/gi;
type Q = Record<string, unknown>;
function srcsOf(q: Q): string[] {
  const parts: string[] = [];
  if (typeof q.question === "string") parts.push(q.question);
  if (Array.isArray(q.options)) parts.push(...(q.options as string[]));
  if (Array.isArray(q.statements)) parts.push(...(q.statements as { text?: string }[]).map((s) => s.text ?? ""));
  return parts.flatMap((p) => [...p.matchAll(IMG_RE)].map((m) => m[1])).filter((s) => !s.startsWith("data:"));
}

type Job = { label: string; id: number; idx?: number; src: string };
const jobs: Job[] = [];
if (EXAM) {
  const { data, error } = await supabase.from("exams").select("id, title, questions").eq("id", Number(EXAM)).single();
  if (error) { console.error(error.message); process.exit(1); }
  ((data.questions ?? []) as Q[]).forEach((q, i) => srcsOf(q).forEach((src) => jobs.push({ label: `đề ${data.id}`, id: data.id, idx: i + 1, src })));
} else {
  for (let from = 0; ; from += 1000) {
    const { data, error } = await supabase.from("question_bank").select("id, question").eq("archived", false)
      .or("question->>question.imatch.<img,question->>options.imatch.<img,question->>statements.imatch.<img")
      .order("id").range(from, from + 999);
    if (error) { console.error(error.message); process.exit(1); }
    for (const r of data ?? []) srcsOf(r.question as Q).forEach((src) => jobs.push({ label: "ngân hàng", id: r.id, src }));
    process.stderr.write(`\rđọc ${jobs.length} ảnh`);
    if (!data || data.length < 1000) break;
  }
  process.stderr.write("\n");
}

type Res = { label: string; id: number; idx?: number; src: string; w: number; h: number; frac: number; wFrac: number; hFrac: number } | { src: string; loi: string };
const cache = new Map<string, Res>();
async function measure(src: string): Promise<Res> {
  try {
    const full = src.startsWith("http") ? src : SITE + src;
    // ảnh nhỏ không thể có lề trắng kiểu "nguyên trang": chỉ đọc đầu file PNG (IHDR) để biết cỡ, chưa tải hết
    if (!ALL) {
      const head = Buffer.from(await (await fetch(full, { headers: { Range: "bytes=0-31" }, signal: AbortSignal.timeout(30000) })).arrayBuffer());
      if (head.length >= 24 && head.toString("latin1", 1, 4) === "PNG") {
        const hw = head.readUInt32BE(16), hh = head.readUInt32BE(20);
        if (hh < MIN_H) return { label: "", id: 0, src, w: hw, h: hh, frac: 1, wFrac: 1, hFrac: 1 };
      }
    }
    const buf = Buffer.from(await (await fetch(full, { signal: AbortSignal.timeout(30000) })).arrayBuffer());
    const { data, info } = await sharp(buf).flatten({ background: "#ffffff" }).greyscale().raw().toBuffer({ resolveWithObject: true });
    const { width: w, height: h } = info;
    // nền = màu phổ biến nhất (lượng tử 8 mức) trên viền ảnh
    const cnt = new Map<number, number>();
    const at = (x: number, y: number) => data[y * w + x];
    for (let x = 0; x < w; x++) for (const y of [0, h - 1]) cnt.set(at(x, y) >> 3, (cnt.get(at(x, y) >> 3) ?? 0) + 1);
    for (let y = 0; y < h; y++) for (const x of [0, w - 1]) cnt.set(at(x, y) >> 3, (cnt.get(at(x, y) >> 3) ?? 0) + 1);
    const bg = ([...cnt.entries()].sort((a, b) => b[1] - a[1])[0][0] << 3) + 4;
    let x0 = w, y0 = h, x1 = -1, y1 = -1;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (Math.abs(at(x, y) - bg) > 40) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    if (x1 < 0) return { label: "", id: 0, src, w, h, frac: 0, wFrac: 0, hFrac: 0 };
    const bw = x1 - x0 + 1, bh = y1 - y0 + 1;
    return { label: "", id: 0, src, w, h, frac: (bw * bh) / (w * h), wFrac: bw / w, hFrac: bh / h };
  } catch (e) { return { src, loi: (e as Error).message }; }
}
const queue = [...jobs];
const hits: (Res & { label: string; id: number; idx?: number })[] = [];
const errs: { src: string; loi: string }[] = [];
let done = 0;
async function work() {
  for (;;) {
    const j = queue.shift();
    if (!j) return;
    let r = cache.get(j.src);
    if (!r) { r = await measure(j.src); cache.set(j.src, r); }
    if ("loi" in r) { if (!errs.some((e) => e.src === r!.src)) errs.push(r); }
    else if (r.frac < MAX_FRAC) hits.push({ ...r, label: j.label, id: j.id, idx: j.idx });
    if (++done % 100 === 0) process.stderr.write(`\r${done}/${jobs.length}`);
  }
}
await Promise.all(Array.from({ length: 48 }, work));
process.stderr.write("\n");

const dir = path.join(scriptDir, "data", "kiem-ke-anh-ngan-hang");
fs.mkdirSync(dir, { recursive: true });
hits.sort((a, b) => (a as { frac: number }).frac - (b as { frac: number }).frac);
fs.writeFileSync(path.join(dir, "anh-le-trang.json"), JSON.stringify({ nguong: MAX_FRAC, hits, errs }, null, 1));
const md = [`# Ảnh có lề trắng quá lớn (nét vẽ < ${Math.round(MAX_FRAC * 100)}% khung)`, "", `Quét ${jobs.length} ảnh (${cache.size} file khác nhau), ${hits.length} ảnh bị báo, ${errs.length} lỗi tải.`, "",
  "| Nguồn | Câu | Khung (px) | Nét vẽ / khung | Ảnh |", "|---|---|---|---|---|",
  ...hits.map((h) => { const r = h as Extract<Res, { frac: number }>; return `| ${h.label} | ${h.idx ?? h.id} | ${r.w}×${r.h} | ${Math.round(r.frac * 100)}% (rộng ${Math.round(r.wFrac * 100)}%, cao ${Math.round(r.hFrac * 100)}%) | ${r.src} |`; })].join("\n");
fs.writeFileSync(path.join(dir, "anh-le-trang.md"), md + "\n");
console.log(md.split("\n").slice(0, 40).join("\n"));
