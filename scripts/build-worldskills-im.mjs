// Dựng HTML lý thuyết 16 bài học phần CTTC "WorldSkills — Industrial Mechanics" từ bộ dịch markdown/CSV
// content/worldskills-im/dich/ (nguồn gốc: Documents/CTTC/.../2026/dich/). Không <script>/<style>/on*=.
//   node scripts/build-worldskills-im.mjs   → content/worldskills-im/_dung/<ch>-<so>.html + index.json
import fs from "node:fs";
import path from "node:path";
import { marked } from "marked";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const D = path.join(ROOT, "content/worldskills-im/dich");
const OUT = path.join(ROOT, "content/worldskills-im/_dung");
fs.mkdirSync(OUT, { recursive: true });
const rd = (p) => fs.readFileSync(path.join(D, p), "utf8").replace(/^﻿/, "");
const B1 = "01-bac1-de-thi-va-thang-diem", B2 = "02-bac2-technical-description", B3 = "03-bac3-tom-tat";
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

marked.use({ gfm: true, breaks: false });
/** md → HTML bài học: bỏ H1 đầu, ## → h3, ### → h4, bảng có class, blockquote → hộp, checkbox bật được. */
function md(text, { dropH1 = true, shift = 1 } = {}) {
  let html = marked.parse(text);
  if (dropH1) html = html.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>/, "");
  if (shift) {
    html = html.replace(/<(\/?)h([1-6])(\b[^>]*)>/g, (m, c, n, rest) => `<${c}h${Math.min(6, +n + shift)}${rest}>`);
  }
  html = html
    .replace(/<table>([\s\S]*?)<\/table>/g, (m, inner) => `<div class="tl-scroll"><table class="tl-table">${inner}</table></div>`)
    // "[ ]" trong ô bảng (phiếu tự chấm): marked chỉ đổi task-list trong <li> → tự đổi thành ô tick
    .replace(/<th>\s*\[ \]\s*<\/th>/g, '<th class="tl-nw">Tick</th>')
    .replace(/<td>\s*\[ \]\s*<\/td>/g, '<td class="tl-nw"><input type="checkbox" aria-label="Đạt"></td>')
    .replace(/<td>\s*\[x\]\s*<\/td>/gi, '<td class="tl-nw"><input type="checkbox" checked aria-label="Đạt"></td>')
    // EN:/VI: cùng một đoạn → mỗi thứ tiếng một dòng
    .replace(/([^>])\s*<strong>VI:<\/strong>/g, "$1<br><strong>VI:</strong>")
    .replace(/<blockquote>/g, '<div class="tl-box">').replace(/<\/blockquote>/g, "</div>")
    .replace(/<input (checked="" )?disabled="" type="checkbox">/g, (m, chk) => `<input type="checkbox"${chk ? " checked" : ""}>`)
    .replace(/<a href="(https?:[^"]+)"/g, '<a href="$1" target="_blank" rel="noopener"');
  return html;
}
const idify = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
/** Mục gập được */
const fold = (title, inner, open = false) => `<details class="tl-details"${open ? " open" : ""}><summary><strong>${esc(title)}</strong></summary>${inner}</details>`;

// ---- Thang điểm CSV → bảng theo tiêu chí
function parseCsv(text) {
  const rows = []; let row = [], cell = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
    else if (c !== "\r") cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const [h, ...body] = rows;
  return body.filter((r) => r.length >= 8).map((r) => Object.fromEntries(h.map((k, i) => [k, (r[i] ?? "").trim()])));
}
const CRIT = { A: "Bảo trì dự đoán", B: "Hàn, chế tạo và lấy dấu", C: "Gia công tiện – phay", D: "Lắp ráp cơ khí", E: "Lắp ráp khí nén", F: "Vận hành cuối", G: "Sửa lỗi khí nén" };
const subs = [];
{
  let cur = null, item = null;
  for (const r of parseCsv(rd(`${B1}/08-thang-diem-song-ngu.csv`))) {
    if (!r.Type) { cur = { id: r.SubCriterion, vi: r.Aspect_VI || r.Aspect_EN, en: r.Aspect_EN, items: [] }; subs.push(cur); item = null; continue; }
    if (r.Type === "J" && /^Score/.test(r.Aspect_EN)) { if (item) (item.scale ??= []).push({ en: r.ExtraDesc_EN, vi: r.ExtraDesc_VI }); continue; }
    item = { type: r.Type, en: r.Aspect_EN, vi: r.Aspect_VI, xen: r.ExtraDesc_EN, xvi: r.ExtraDesc_VI, req: r.Requirement, marks: +r.Marks || 0 };
    cur.items.push(item);
  }
}
const subTotal = (s) => s.items.reduce((a, i) => a + i.marks, 0);
const critTotal = (c) => subs.filter((s) => s.id[0] === c).reduce((a, s) => a + subTotal(s), 0);
function markingTable(c) {
  let h = `<div class="tl-scroll tl-scroll--rong"><table class="tl-table"><thead><tr><th class="tl-nw">Mã</th><th>Mục chấm</th><th>Yêu cầu / cách cho điểm</th><th class="tl-nw">Điểm</th></tr></thead><tbody>`;
  for (const s of subs.filter((s) => s.id[0] === c)) {
    h += `<tr><td class="tl-nw"><strong>${esc(s.id)}</strong></td><td colspan="2"><strong>${esc(s.vi)}</strong><br><em>${esc(s.en)}</em></td><td class="tl-nw"><strong>${subTotal(s).toFixed(2)}</strong></td></tr>`;
    for (const i of s.items) {
      const scale = i.scale ? `<ol start="0">${i.scale.map((x) => `<li>${esc(x.vi)}<br><em>${esc(x.en)}</em></li>`).join("")}</ol>` : "";
      h += `<tr><td class="tl-nw">${i.type}</td><td>${esc(i.vi)}<br><em>${esc(i.en)}</em></td><td>${esc(i.xvi)}${i.req ? ` <strong>${esc(i.req)}</strong>` : ""}${i.xen ? `<br><em>${esc(i.xen)}</em>` : ""}${scale}</td><td class="tl-nw">${i.marks.toFixed(2)}</td></tr>`;
    }
  }
  return h + "</tbody></table></div>";
}
const markingNote = `<p class="tl-note">Bảng rộng: vuốt ngang trên điện thoại. M = chấm đo: đạt trọn điểm hoặc 0 (trừ mục ghi nửa điểm). J = chấm đánh giá 0–3: 0 dưới chuẩn công nghiệp, 1 đạt, 2 vượt, 3 xuất sắc; điểm = mức/3 × điểm mục.</p>`;
const markingSection = (c, open = false) =>
  `<h3 id="thang-diem-${c}">Thang điểm tiêu chí ${c} — ${esc(CRIT[c])} — ${critTotal(c).toFixed(1)} điểm</h3>${markingNote}${fold(`Mở bảng thang điểm ${c} (${subs.filter((s) => s.id[0] === c).length} tiêu chí con)`, markingTable(c), open)}`;

// ---- Phiếu tự chấm
const PHIEU = { A: "A-bao-tri-du-doan", B: "B-han-va-lay-dau", C: "C-tien-phay", D: "D-lap-rap-co-khi", E: "E-lap-rap-khi-nen", F: "F-van-hanh-cuoi", G: "G-sua-loi-fluidsim" };
function phieuSection(c) {
  const t = rd(`${B1}/phieu-tu-cham/${PHIEU[c]}.md`);
  const title = (t.match(/^# (.*)$/m) || [, `Phiếu tự chấm ${c}`])[1];
  let body = md(t, { shift: 2 }); // ## → h4, ### → h5 (phiếu nằm dưới h3 của bài)
  const k = body.search(/<h4[^>]*>\s*Bẫy mất điểm/);
  if (k >= 0) body = body.slice(0, k) + '<div class="tl-box tl-trap">' + body.slice(k) + "</div>";
  return `<h3 id="phieu-${c}">${esc(title)}</h3><p class="tl-note">In ra hoặc tick ngay trên màn hình. Mỗi lần thử ghi số tự đo vào cột "Tự đo" rồi so với miền đạt.</p>${body}`;
}

// ---- Thuật ngữ
function glossary() {
  const t = rd("00-dung-chung/thuat-ngu.md");
  const groups = []; let g = null;
  for (const line of t.split("\n")) {
    if (/^## /.test(line)) { g = { title: line.replace(/^## /, ""), rows: [] }; groups.push(g); continue; }
    const m = line.match(/^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$/);
    if (g && m && m[1] !== "English" && !/^-+$/.test(m[1].replace(/[:\s]/g, ""))) g.rows.push([m[1], m[2]]);
  }
  const intro = md(t.split(/^## /m)[0]);
  return intro + groups.map((g, i) => `<h3 id="tn-${i + 1}">${esc(g.title)} (${g.rows.length})</h3><table class="tl-table"><thead><tr><th>English</th><th>Tiếng Việt</th></tr></thead><tbody>${g.rows.map(([e, v]) => `<tr><td>${marked.parseInline(e)}</td><td>${marked.parseInline(v)}</td></tr>`).join("")}</tbody></table>`).join("");
}

// ---- Mỗi bài
const doc = (p, o) => md(rd(p), o);
const LESSONS = [
  { ch: 1, so: 1, html: () => doc(`${B1}/00-tong-quan-de-thi.md`) },
  { ch: 1, so: 2, html: () => doc(`${B1}/06-ban-ve-chu-giai.md`) },
  { ch: 1, so: 3, html: () => `<h3 id="ppe">Mục 7 — Trang bị bảo hộ (PPE)</h3>` + doc(`${B2}/04-muc-7-PPE.md`, { shift: 2 }) + `<h3 id="luat-rieng">Mục 9 — Luật riêng của nghề</h3>` + doc(`${B2}/05-muc-9-luat-rieng-nghe.md`, { shift: 2 }) },
  { ch: 1, so: 4, html: glossary },
  { ch: 2, so: 1, html: () => doc(`${B1}/03-module-B-han-va-lay-dau.md`) + phieuSection("B") + markingSection("B") },
  { ch: 2, so: 2, html: () => doc(`${B1}/04-module-C-tien-phay.md`) + phieuSection("C") + markingSection("C") },
  { ch: 2, so: 3, html: () => doc(`${B1}/07-so-do-khi-nen.md`) + phieuSection("E") + markingSection("E") },
  { ch: 3, so: 1, html: () => doc(`${B1}/05-module-D-lap-rap-van-hanh.md`) + phieuSection("D") + markingSection("D") + phieuSection("F") + markingSection("F") },
  { ch: 3, so: 2, html: () => doc(`${B1}/01-module-A1-bao-tri-du-doan.md`) + phieuSection("A") + markingSection("A") },
  { ch: 3, so: 3, html: () => doc(`${B1}/02-module-A2-sua-loi-fluidsim.md`) + phieuSection("G") + markingSection("G") },
  { ch: 4, so: 1, html: () => `<p>Toàn bộ 198 mục chấm của thang điểm thật (WSC2026_01_Industrial_Mechanics_marking_scheme.xlsx), dịch song ngữ. Dùng cho người đóng vai Expert khi thi thử 20 giờ.</p><table class="tl-table"><thead><tr><th>Tiêu chí</th><th>Điểm</th></tr></thead><tbody>${Object.keys(CRIT).map((c) => `<tr><td>${c} · ${esc(CRIT[c])}</td><td>${critTotal(c).toFixed(1)}</td></tr>`).join("")}<tr><td><strong>Tổng</strong></td><td><strong>${Object.keys(CRIT).reduce((a, c) => a + critTotal(c), 0).toFixed(1)}</strong></td></tr></tbody></table>` + Object.keys(CRIT).map((c) => markingSection(c)).join("") },
  { ch: 4, so: 2, html: () => `<h3 id="cach-cham">Mục 4 — Cách chấm và trừ điểm</h3>` + doc(`${B2}/02-muc-4-cach-cham-va-tru-diem.md`, { shift: 2 }) + `<h3 id="tham-dinh">Thẩm định đề (Statement of Validation)</h3>` + doc(`${B3}/statement-of-validation.md`, { shift: 2 }) },
  { ch: 5, so: 1, html: () => doc(`${B2}/01-muc-1-2-mo-ta-nghe-va-WSOS.md`) },
  { ch: 5, so: 2, html: () => doc(`${B2}/03-muc-5.3-yeu-cau-thiet-ke-de.md`) },
  { ch: 5, so: 3, html: () => `<h3 id="may-phay">Máy phay M5 — thông số</h3>` + doc(`${B3}/may-phay-M5-thong-so.md`, { shift: 2 }) + `<h3 id="danh-muc">Danh mục file gốc</h3>` + doc(`${B3}/danh-muc-file-goc.md`, { shift: 2 }) },
  { ch: 5, so: 4, html: () => `<h3 id="loi-ban-goc">19 chỗ lỗi hoặc chưa nhất quán trong bản gốc</h3><p>Nguyên tắc: dịch đúng bản gốc, chú thích <code>[Ghi chú dịch: …]</code>, không tự sửa. Bảng này để giáo viên biết chỗ nào đề/bản vẽ tự mâu thuẫn và huấn luyện theo giá trị nào.</p>` + doc("00-dung-chung/loi-ban-goc.md") },
];
const index = [];
for (const l of LESSONS) {
  let html = l.html().trim();
  if (!/<h3\b/.test(html)) html = html.replace(/<h4\b/g, "<h3").replace(/<\/h4>/g, "</h3>"); // bài chỉ có mục nhỏ
  // id cho h3 chưa có (Ôn ngay cuộn tới mốc)
  html = html.replace(/<h3>([^<]*)<\/h3>/g, (m, t) => `<h3 id="${idify(t).slice(0, 60)}">${t}</h3>`);
  const file = `${l.ch}-${l.so}.html`;
  fs.writeFileSync(path.join(OUT, file), html);
  index.push({ ch: l.ch, so: l.so, file, bytes: Buffer.byteLength(html) });
}
fs.writeFileSync(path.join(OUT, "index.json"), JSON.stringify(index, null, 1));
console.table(index);
