// Tìm ảnh "trống" trong ngân hàng câu hỏi: ảnh còn nguyên file nhưng toàn một màu (nền xám/trắng), lúc đăng bị mất nội dung.
// Bản kiểm kê cũ (kiem-ke-anh-ngan-hang) chỉ đo dung lượng/kích thước nên bỏ sót loại này. CHỈ ĐỌC, tải ảnh nhỏ qua URL công khai.
//   npx tsx scripts/kiem-anh-trong.mts            # ảnh < 2500 byte (ảnh trống nén rất nhỏ, ~340 B)
// Ra: scripts/data/kiem-ke-anh-ngan-hang/anh-trong.json + anh-trong.md (câu, ảnh, độ lệch chuẩn điểm ảnh)
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "data", "kiem-ke-anh-ngan-hang");
type Row = { id: number; grade: string | null; topic: string | null; loai: string; anh?: { src: string; bytes: number | null; w: number | null; h: number | null }[] };
const rows: Row[] = JSON.parse(fs.readFileSync(path.join(dir, "rows.json"), "utf8"));
const MAX = Number(process.argv[2] ?? 2500);
const jobs = rows.flatMap((r) => (r.anh ?? []).filter((a) => a.bytes !== null && a.bytes < MAX).map((a) => ({ r, a })));
console.log(`kiểm ${jobs.length} ảnh < ${MAX} B của ${new Set(jobs.map((j) => j.r.id)).size} câu`);
const seen = new Map<string, number | string>();
const res: { id: number; src: string; bytes: number; sd: number | string }[] = [];
let done = 0;
async function work() {
  for (;;) {
    const j = jobs.shift();
    if (!j) return;
    let sd = seen.get(j.a.src);
    if (sd === undefined) {
      try {
        const buf = Buffer.from(await (await fetch(j.a.src, { signal: AbortSignal.timeout(30000) })).arrayBuffer());
        const st = await sharp(buf).removeAlpha().greyscale().stats();
        sd = Math.round(st.channels[0].stdev * 100) / 100;
      } catch (e) { sd = "loi: " + (e as Error).message; }
      seen.set(j.a.src, sd);
    }
    res.push({ id: j.r.id, src: j.a.src, bytes: j.a.bytes!, sd });
    if (++done % 50 === 0) console.log(`  ${done}…`);
  }
}
await Promise.all(Array.from({ length: 32 }, work));
const trong = res.filter((x) => typeof x.sd === "number" && x.sd < 3);
const loi = res.filter((x) => typeof x.sd === "string");
fs.writeFileSync(path.join(dir, "anh-trong.json"), JSON.stringify({ trong, loi }, null, 1));
const byQ = new Map<number, number>();
for (const t of trong) byQ.set(t.id, (byQ.get(t.id) ?? 0) + 1);
const md = `# Ảnh trống (toàn một màu) — ${new Date().toISOString().slice(0, 10)}\n\n- Đã kiểm ${res.length} ảnh · trống ${trong.length} ảnh · ${byQ.size} câu · lỗi tải ${loi.length}\n\n` +
  [...byQ].map(([id, n]) => `- #${id}: ${n} ảnh trống · ${rows.find((r) => r.id === id)?.loai} · L${rows.find((r) => r.id === id)?.grade}`).join("\n") + "\n";
fs.writeFileSync(path.join(dir, "anh-trong.md"), md);
console.log(md.split("\n").slice(0, 6).join("\n"));
