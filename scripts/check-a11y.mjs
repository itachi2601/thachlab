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
const PAIRS = [
  ["ink tối / bg", "#f1f5f9", "#05070b", 4.5],
  ["muted tối / panel", "#94a3b8", "#0b1020", 4.5],
  ["ink sáng / trắng", "#0f172a", "#ffffff", 4.5],
  ["muted sáng / trắng", "#475569", "#ffffff", 4.5],
  ["cyan / bg tối", "#22d3ee", "#05070b", 4.5],
  ["accent vàng / bg tối", "#facc15", "#05070b", 4.5],
  ["nhấn tiêu đề tối #60a5fa / bg", "#60a5fa", "#05070b", 4.5],
  ["nhấn tiêu đề sáng #1d4ed8 / #f8fafc", "#1d4ed8", "#f8fafc", 4.5],
  ["nhấn ấm tối #fb923c / bg", "#fb923c", "#05070b", 4.5],
  ["nhấn ấm sáng #c2410c / trắng", "#c2410c", "#ffffff", 4.5],
  ["dịu mắt ink / kem", "#33291a", "#f5efe0", 4.5],
  ["dịu mắt muted / kem", "#6b5a3e", "#f5efe0", 4.5],
  ["override sáng cyan #0e7490", "#0e7490", "#ffffff", 4.5],
  ["override sáng emerald #047857", "#047857", "#ffffff", 4.5],
  ["override sáng amber #a16207", "#a16207", "#ffffff", 4.5],
  ["override sáng red #b91c1c", "#b91c1c", "#ffffff", 4.5],
  ["override sáng violet #6d28d9", "#6d28d9", "#ffffff", 4.5],
  ["slate-500 theme sáng #64748b / trắng", "#64748b", "#ffffff", 4.5],
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
