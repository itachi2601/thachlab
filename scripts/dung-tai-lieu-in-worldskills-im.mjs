// Tài liệu IN cho giáo viên (A4, đen–trắng, có số trang): ghép các bài bậc 2/3 đã dựng ở content/worldskills-im/_dung/.
//   node scripts/build-worldskills-im.mjs && node scripts/dung-tai-lieu-in-worldskills-im.mjs
// → content/worldskills-im/in/giao-vien.html, rồi in PDF bằng Chrome headless (in ra lệnh nếu không thấy Chrome).
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const IN = path.join(ROOT, "content/worldskills-im/_dung"), OUT = path.join(ROOT, "content/worldskills-im/in");
const idx = JSON.parse(fs.readFileSync(path.join(IN, "index.json"), "utf8"));
const PARTS = [
  ["1-1", "1. Tổng quan đề thi — Overview of the test project"],
  ["5-1", "2. Mô tả nghề và chuẩn WSOS — Technical description and WSOS"],
  ["5-2", "3. Yêu cầu thiết kế đề thi — Test project design requirements"],
  ["4-2", "4. Cách chấm, trừ điểm và thẩm định đề — Marking, penalties, validation"],
  ["1-3", "5. Trang bị bảo hộ và luật riêng của nghề — PPE and skill-specific rules"],
  ["5-3", "6. Máy phay M5 và danh mục file gốc — M5 mill and source files"],
  ["5-4", "7. Ghi chú lỗi trong bản gốc — Errata in the source documents"],
  ["1-4", "8. Thuật ngữ Anh – Việt — Glossary"],
];
const clean = (h) => h
  .replace(/<div class="tl-scroll[^"]*">/g, "<div>")
  .replace(/<details[^>]*>\s*<summary>[\s\S]*?<\/summary>/g, "").replace(/<\/details>/g, "")
  .replace(/<input type="checkbox"[^>]*>/g, "☐")
  .replace(/<h3\b/g, "<h2").replace(/<\/h3>/g, "</h2>").replace(/<h4\b/g, "<h3").replace(/<\/h4>/g, "</h3>");
const body = PARTS.map(([k, t]) => { const f = path.join(IN, `${k}.html`); return `<section><h1>${t}</h1>${clean(fs.readFileSync(f, "utf8"))}</section>`; }).join("");
const toc = PARTS.map(([, t]) => `<li>${t}</li>`).join("");
const css = `
@page { size: A4; margin: 18mm 15mm 20mm; @bottom-center { content: "WorldSkills 2026 · Industrial Mechanics — Tài liệu giáo viên · trang " counter(page) " / " counter(pages); font: 8.5pt system-ui, sans-serif; color: #444; } }
body { font: 10.5pt/1.5 "Be Vietnam Pro", system-ui, sans-serif; color: #000; margin: 0; }
h1 { font-size: 16pt; border-bottom: 2px solid #000; padding-bottom: 4px; margin: 0 0 10px; break-before: page; }
.cover + section h1, section:first-of-type h1 { break-before: auto; }
h2 { font-size: 12.5pt; margin: 16px 0 6px; break-after: avoid; } h3 { font-size: 11pt; margin: 12px 0 4px; break-after: avoid; }
table { width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 9.5pt; } th, td { border: 1px solid #000; padding: 3px 6px; vertical-align: top; text-align: left; } th { background: #e5e5e5; }
tr { break-inside: avoid; }
.tl-bi { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 6px 0; break-inside: avoid; } .tl-bi--vi { grid-template-columns: 1fr; }
.tl-bi-en { border-left: 2px solid #000; padding-left: 8px; font-style: normal; } .tl-bi-vi { border-left: 2px dashed #000; padding-left: 8px; }
.tl-bi-tag { display: block; font-size: 7.5pt; font-weight: 700; letter-spacing: .06em; }
li.tl-bi-li { list-style: none; margin-left: -1.2em; } .tl-box { border: 1px solid #000; padding: 6px 10px; margin: 8px 0; break-inside: avoid; }
.cover { text-align: center; padding-top: 70mm; } .cover h1 { border: 0; font-size: 24pt; break-before: auto; } .cover p { font-size: 12pt; } .toc { margin: 24px auto; display: inline-block; text-align: left; }
img { max-width: 100%; } a { color: #000; text-decoration: none; }`;
const html = `<!doctype html><html lang="vi"><meta charset="utf-8"><title>WorldSkills 2026 Industrial Mechanics — Tài liệu giáo viên</title><style>${css}</style>
<div class="cover"><h1>WorldSkills Shanghai 2026<br>Skill 01 — Industrial Mechanics</h1><p><strong>Tài liệu tham khảo cho giáo viên huấn luyện</strong><br>Song ngữ Anh – Việt · EN bên trái, VI bên phải</p><ol class="toc">${toc}</ol>
<p style="font-size:9pt">Bản dịch phục vụ huấn luyện, không thay thế bản gốc. Lỗi bản gốc được dịch nguyên và ghi chú ở mục 7. Thang điểm đầy đủ 198 mục xem bài "Thang điểm đầy đủ A–G" trên web.</p></div>${body}</html>`;
fs.mkdirSync(OUT, { recursive: true });
const f = path.join(OUT, "giao-vien.html");
fs.writeFileSync(f, html);
const chrome = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"].find((p) => fs.existsSync(p));
if (chrome) { execFileSync(chrome, ["--headless=new", "--disable-gpu", `--print-to-pdf=${path.join(OUT, "giao-vien.pdf")}`, "--no-pdf-header-footer", "file://" + f], { stdio: "ignore" }); console.log("OK", path.join(OUT, "giao-vien.pdf")); }
else console.log("Không thấy Chrome; mở", f, "rồi in PDF");
