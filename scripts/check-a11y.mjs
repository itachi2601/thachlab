#!/usr/bin/env node
// Kiểm khả năng đọc (docs/UI.md): (1) đo tương phản WCAG 2.1 của các cặp token,
// (2) bắt cỡ chữ dưới sàn 12px trong app/components/lib. Thoát mã 1 nếu có vi phạm.
//   node scripts/check-a11y.mjs            # kiểm cả hai
//   node scripts/check-a11y.mjs '#64748b' '#0b1020'   # đo nhanh một cặp
import fs from "node:fs";
import path from "node:path";

const hex = (h) => { h = h.replace("#", ""); if (h.length === 3) h = [...h].map((c) => c + c).join(""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255); };
const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
export const contrast = (a, b) => { const x = lum(hex(a)), y = lum(hex(b)); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };

if (process.argv.length === 4) { console.log(contrast(process.argv[2], process.argv[3]).toFixed(2)); process.exit(0); }

// [tên, chữ, nền, ngưỡng] — ngưỡng 4.5 chữ thường, 3 chữ lớn/icon/viền (WCAG AA)
// Từ 11/10/2026 bảng màu lấy NỀN SÁNG làm mặc định; theme tối vẫn kiểm để không thoái hoá.
const PAIRS = [
  // — Nền sáng (mặc định) —
  ["sáng · ink #0f172a / bg #f5f7fa", "#0f172a", "#f5f7fa", 4.5],
  ["sáng · ink / panel trắng", "#0f172a", "#ffffff", 4.5],
  ["sáng · muted #475569 / bg", "#475569", "#f5f7fa", 4.5],
  ["sáng · muted / panel trắng", "#475569", "#ffffff", 4.5],
  ["sáng · chữ trắng / nút primary #1d4ed8", "#ffffff", "#1d4ed8", 4.5],
  ["sáng · primary #1d4ed8 (chữ/viền) / bg", "#1d4ed8", "#f5f7fa", 4.5],
  ["sáng · primary-soft #eef2ff + primary-dark chữ", "#1e40af", "#eef2ff", 4.5],
  ["sáng · ok #047857 / trắng", "#047857", "#ffffff", 4.5],
  ["sáng · warn #b45309 / trắng", "#b45309", "#ffffff", 4.5],
  ["sáng · danger #b91c1c / trắng", "#b91c1c", "#ffffff", 4.5],
  ["sáng · cyan #0e7490 / trắng", "#0e7490", "#ffffff", 4.5],
  ["sáng · violet #6d28d9 / trắng", "#6d28d9", "#ffffff", 4.5],
  ["sáng · slate-500 #64748b / trắng", "#64748b", "#ffffff", 4.5],
  ["sáng · viền line-strong #cfd6e0 / trắng (1.4.11 cần 3:1)", "#8b93a1", "#ffffff", 3],
  ["sáng · nhấn tiêu đề #1d4ed8 / bg", "#1d4ed8", "#f5f7fa", 4.5],
  ["sáng · nhấn ấm #c2410c / trắng", "#c2410c", "#ffffff", 4.5],
  // — Phụ huynh 45–60: nhắm AAA 7:1 (docs/QUY-TAC-THIET-KE-PHU-HUYNH.md P2) —
  ["PH · ink #14181f / #f7f7f4", "#14181f", "#f7f7f4", 7],
  ["PH · muted #3d4653 / #f7f7f4", "#3d4653", "#f7f7f4", 7],
  ["PH · muted / panel trắng", "#3d4653", "#ffffff", 7],
  ["PH · chữ trắng / nút #1e40af", "#ffffff", "#1e40af", 7],
  ["PH · primary #1e40af / #f7f7f4", "#1e40af", "#f7f7f4", 7],
  ["PH · ok #065f46 / #f7f7f4", "#065f46", "#f7f7f4", 7],
  ["PH · warn #78350f / #f7f7f4", "#78350f", "#f7f7f4", 7],
  ["PH · danger #991b1b / #f7f7f4", "#991b1b", "#f7f7f4", 7],
  // — Theme tối (tuỳ chọn) —
  ["tối · ink / bg", "#f1f5f9", "#05070b", 4.5],
  ["tối · muted / panel", "#94a3b8", "#0b1020", 4.5],
  ["tối · cyan / bg", "#22d3ee", "#05070b", 4.5],
  ["tối · accent vàng / bg", "#facc15", "#05070b", 4.5],
  ["tối · nhấn #60a5fa / bg", "#60a5fa", "#05070b", 4.5],
  ["tối · chữ trắng / nút primary #2563eb", "#ffffff", "#2563eb", 4.5],
  ["tối · nhấn ấm #fb923c / bg", "#fb923c", "#05070b", 4.5],
  ["tối · slate-500 #7c8ba1 / panel", "#7c8ba1", "#0b1020", 4.5],
  ["tối · viền line-strong #cbd5e1 / panel (3:1)", "#cbd5e1", "#0b1020", 3],
  // — Chế độ Dịu mắt (kem/nâu) —
  ["dịu mắt · ink / kem", "#33291a", "#f5efe0", 4.5],
  ["dịu mắt · muted / kem", "#6b5a3e", "#f5efe0", 4.5],
];
let bad = 0;
console.log("— Tương phản —");
for (const [name, fg, bg, min] of PAIRS) {
  const r = contrast(fg, bg);
  const ok = r >= min;
  if (!ok) bad++;
  console.log(`${ok ? "✓" : "✗"} ${r.toFixed(2).padStart(6)}  ${name}  (cần ≥ ${min})`);
}

// Sàn cỡ chữ 12px
const ROOTS = ["app", "components", "lib"];
const TW = /text-\[(?:[0-9]|1[01])(?:\.\d+)?px\]/g;
const CSS = /font-size:\s*(?:[0-9]|1[01])(?:\.\d+)?px/g;
const hits = [];
function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p);
    else if (/\.(tsx?|css)$/.test(e.name) && !p.endsWith("local-preview.css")) {
      const s = fs.readFileSync(p, "utf8");
      const lines = s.split("\n");
      lines.forEach((l, i) => { if (TW.test(l) || CSS.test(l)) hits.push(`${p}:${i + 1}`); TW.lastIndex = 0; CSS.lastIndex = 0; });
    }
  }
}
for (const r of ROOTS) if (fs.existsSync(r)) walk(r);
console.log(`— Sàn cỡ chữ 12px — ${hits.length} chỗ vi phạm`);
for (const h of hits) console.log("  " + h);
if (bad || hits.length) { console.log(`\nKHÔNG ĐẠT: ${bad} cặp màu, ${hits.length} chỗ chữ nhỏ.`); process.exit(1); }
console.log("\nĐẠT.");
