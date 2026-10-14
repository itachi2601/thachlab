// Quét nhãn chữ trong hình SVG của bài lý thuyết (lesson_items.kind='ly_thuyet') — CHỈ ĐỌC, không ghi DB.
//   npx tsx scripts/quet-nhan-svg.mts [--json=scripts/logs/quet-nhan-svg.json]
// Đo theo cỡ chữ HIỂN THỊ ở 375px (cột bài ≈ 343px): cỡ chữ SVG × (343 / rộng viewBox), vì SVG co theo khung.
// Báo mỗi hình: viewBox, cỡ chữ nhỏ nhất đã quy ra px, số nhãn < 13px, màu chữ nhạt (độ sáng tương đối cao, tương phản <4,5:1 trên nền trắng).
// K4 (docs/PHAN-CONG-UI-2026-10-13.md): đọc kết quả rồi mới quyết sửa — nâng cỡ chữ trong hình đã dàn sẵn dễ làm chữ đè nhau.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}
const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const sb = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const COLUMN_PX = 343;
const lum = (hex: string) => {
  const h = hex.replace("#", "");
  const f = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  if (!/^[0-9a-f]{6}$/i.test(f)) return null;
  const c = [0, 2, 4].map((i) => parseInt(f.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
};
const contrastOnWhite = (hex: string) => { const l = lum(hex); return l == null ? null : 1.05 / (l + 0.05); };

const { data, error } = await sb.from("lesson_items").select("id, lesson_id, title, body_html").eq("kind", "ly_thuyet");
if (error) { console.error(error.message); process.exit(1); }

type Row = { item: number; lesson: number; title: string; svgs: number; svgNhoNhat: number | null; minPx: number | null; nhanNho: number; nhanTong: number; nhanNhat: number };
const rows: Row[] = [];
for (const it of data ?? []) {
  const html: string = it.body_html ?? "";
  let nhanNho = 0, nhanTong = 0, nhanNhat = 0, minPx: number | null = null, svgs = 0;
  for (const m of html.matchAll(/<svg\b[^>]*>[\s\S]*?<\/svg>/gi)) {
    svgs++;
    const svg = m[0];
    const vb = svg.match(/viewBox="[\d.\s-]*?([\d.]+)\s+[\d.]+"/i);
    const vbW = vb ? parseFloat(vb[1]) : null;
    const scale = vbW ? Math.min(1, COLUMN_PX / vbW) : 1;
    for (const t of svg.matchAll(/<text\b([^>]*)>/gi)) {
      nhanTong++;
      const fs = parseFloat(t[1].match(/font-size="([\d.]+)/i)?.[1] ?? t[1].match(/font-size:\s*([\d.]+)/i)?.[1] ?? "16");
      const px = fs * scale;
      if (minPx == null || px < minPx) minPx = px;
      if (px < 13) nhanNho++;
      const fill = t[1].match(/fill="(#[0-9a-f]{3,6})"/i)?.[1];
      const c = fill ? contrastOnWhite(fill) : null;
      if (c != null && c < 4.5) nhanNhat++;
    }
  }
  if (svgs) rows.push({ item: it.id, lesson: it.lesson_id, title: it.title, svgs, svgNhoNhat: null, minPx: minPx == null ? null : Math.round(minPx * 10) / 10, nhanNho, nhanTong, nhanNhat });
}
rows.sort((a, b) => b.nhanNho - a.nhanNho);
const sum = (k: "nhanNho" | "nhanTong" | "nhanNhat") => rows.reduce((n, r) => n + r[k], 0);
console.log(`Bài có SVG: ${rows.length}/${data?.length}; nhãn tổng ${sum("nhanTong")}; <13px hiển thị ở 375: ${sum("nhanNho")}; màu nhạt (<4,5:1): ${sum("nhanNhat")}`);
for (const r of rows.slice(0, 40)) console.log(`bài ${String(r.lesson).padStart(4)} · mục ${String(r.item).padStart(4)} · ${r.svgs} hình · nhỏ nhất ${r.minPx}px · ${r.nhanNho}/${r.nhanTong} nhãn <13px · ${r.nhanNhat} nhạt · ${r.title.slice(0, 40)}`);
const out = process.argv.find((a) => a.startsWith("--json="))?.slice(7);
if (out) { fs.writeFileSync(path.join(root, out), JSON.stringify(rows, null, 1)); console.log("→", out); }
