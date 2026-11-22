/**
 * Kiểm link mọi thẻ trong lib/data/thu-vien-mo-phong.json.
 *  - mô phỏng: trang /mo-phong/<slug> có thật (dev server nếu --base, không thì kiểm thư mục/danh sách)
 *  - bài học: ?next= giải mã ra đúng /lop-hoc/bai?id=<lesson_id> (giữ đủ query)
 *  - clip: poster + mp4 (hoặc ảnh bìa YouTube) trả 200; PhET trả 200
 * Chạy: npx tsx scripts/kiem-link-thu-vien-mo-phong.mts [--base http://localhost:3000] [--mang]
 * --mang kiểm cả URL ngoài (Supabase Storage, YouTube, PhET); cần ra ngoài internet (tab terminal trên Mac).
 */
import fs from "node:fs";
import path from "node:path";
import { MO_PHONG_TRANG } from "../lib/mo-phong-trang.ts";

const args = process.argv.slice(2);
const base = args.includes("--base") ? args[args.indexOf("--base") + 1] : null;
const mang = args.includes("--mang");
const data = JSON.parse(fs.readFileSync(path.join(process.cwd(), "lib/data/thu-vien-mo-phong.json"), "utf8"));
const loi: string[] = [];
const slugs = new Set(MO_PHONG_TRANG.map((m) => m.slug));

async function ok(url: string, method = "HEAD") {
  try {
    const r = await fetch(url, { method, redirect: "follow" });
    return r.status;
  } catch (e) {
    return `lỗi ${(e as Error).message}`;
  }
}
async function pool<T>(items: T[], n: number, fn: (x: T) => Promise<void>) {
  let i = 0;
  await Promise.all(Array.from({ length: n }, async () => { while (i < items.length) await fn(items[i++]); }));
}

const ids = new Set<string>();
const viec: Array<() => Promise<void>> = [];
for (const t of data.the) {
  if (ids.has(t.id)) loi.push(`${t.id}: trùng id`);
  ids.add(t.id);
  if (!t.ten || !t.nhin_vao) loi.push(`${t.id}: thiếu tên hoặc "Nhìn vào"`);
  if (t.loai === "mo_phong") {
    const slug = t.href.replace(/^\/mo-phong\//, "");
    if (!slugs.has(slug)) loi.push(`${t.id}: slug ${slug} không có trong mo-phong-trang.ts`);
    if (base) viec.push(async () => { const s = await ok(base + t.href + "/", "GET"); if (s !== 200) loi.push(`${t.id}: ${t.href} → ${s}`); });
  } else if (t.loai === "clip") {
    const u = new URL(t.href, "http://x");
    const next = u.searchParams.get("next");
    if (u.pathname !== "/dang-nhap" || next !== `/lop-hoc/bai?id=${t.lesson_id}`) loi.push(`${t.id}: ?next= sai: ${t.href}`);
    if (!t.mp4 && !t.youtube_id) loi.push(`${t.id}: clip không có mp4 lẫn youtube_id`);
    if (mang) {
      for (const u2 of [t.poster, t.mp4].filter(Boolean)) viec.push(async () => { const s = await ok(u2); if (s !== 200) loi.push(`${t.id}: ${u2} → ${s}`); });
    }
  } else if (t.loai === "phet") {
    if (!t.nguon?.includes("CC BY 4.0")) loi.push(`${t.id}: thiếu ghi nguồn CC BY 4.0`);
    if (mang) viec.push(async () => { const s = await ok(t.href); if (s !== 200) loi.push(`${t.id}: ${t.href} → ${s}`); });
  }
}
await pool(viec, 8, (f) => f());
const dem = data.the.reduce((a: Record<string, number>, t: { loai: string }) => ((a[t.loai] = (a[t.loai] ?? 0) + 1), a), {});
console.log(`Đã kiểm ${data.the.length} thẻ`, dem, `· ${viec.length} lượt gọi mạng`);
if (loi.length) { console.log(`LỖI ${loi.length}:\n` + loi.join("\n")); process.exit(1); }
console.log("Mọi link đạt.");
