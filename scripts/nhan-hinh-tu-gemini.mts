// Nhận out/<id>.json do Gemini ghi → kiểm hợp lệ bằng normalizeFigureSpec → vẽ SVG → trang so sánh.
// KHÔNG ghi DB. Ghi DB là bước sau, sau khi thầy duyệt trên trang so sánh.
//   npx tsx scripts/nhan-hinh-tu-gemini.mts
// Kết quả: scripts/data/gemini-hinh/so-sanh.html + svg/<id>.svg + bao-cao.md
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { normalizeFigureSpec, renderFigureSpec } from "../services/figure-spec";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, "data", "gemini-hinh");
const outDir = path.join(root, "out");
const svgDir = path.join(root, "svg");
fs.mkdirSync(svgDir, { recursive: true });

type Ket = { id: number; trang_thai: "ve_duoc" | "khong_ve_duoc" | "json_loi" | "spec_loi"; do_tin_cay?: number; ghi_chu?: string; mo_ta?: string; loi?: string };
const ket: Ket[] = [];
const cards: string[] = [];
const files = fs.existsSync(outDir) ? fs.readdirSync(outDir).filter((f) => f.endsWith(".json")) : [];
for (const f of files) {
  const id = Number(path.basename(f, ".json"));
  const cauDir = path.join(root, "cau", String(id));
  const anh = fs.existsSync(cauDir) ? fs.readdirSync(cauDir).filter((x) => /^anh-\d+\./.test(x)) : [];
  const deBai = fs.existsSync(path.join(cauDir, "de-bai.md")) ? fs.readFileSync(path.join(cauDir, "de-bai.md"), "utf8") : "";
  let raw: Record<string, unknown>;
  try { raw = JSON.parse(fs.readFileSync(path.join(outDir, f), "utf8")); }
  catch (e) { ket.push({ id, trang_thai: "json_loi", loi: (e as Error).message }); continue; }
  const k: Ket = { id, trang_thai: "ve_duoc", do_tin_cay: raw.do_tin_cay as number, ghi_chu: raw.ghi_chu as string };
  let svg = "";
  if (raw.kind === "khong_ve_duoc") { k.trang_thai = "khong_ve_duoc"; k.mo_ta = raw.mo_ta as string; }
  else {
    const spec = normalizeFigureSpec(raw);
    if (!spec) { k.trang_thai = "spec_loi"; k.loi = "normalizeFigureSpec trả null (thiếu trục/khoảng/series?)"; }
    else { svg = renderFigureSpec(spec); fs.writeFileSync(path.join(svgDir, `${id}.svg`), svg); }
  }
  ket.push(k);
  const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  cards.push(`<section class="card" id="c${id}">
  <h2>#${id} <small>${k.trang_thai} · tin cậy ${k.do_tin_cay ?? "?"}</small></h2>
  <div class="row">
    <div class="col"><h3>Ảnh gốc</h3>${anh.map((a) => `<img src="cau/${id}/${a}">`).join("")}</div>
    <div class="col"><h3>SVG mới</h3>${svg || `<p class="warn">${esc(k.mo_ta ?? k.loi ?? "không vẽ")}</p>`}</div>
  </div>
  ${k.ghi_chu ? `<p class="note">Gemini ghi chú: ${esc(k.ghi_chu)}</p>` : ""}
  <details><summary>Đề bài</summary><pre>${esc(deBai)}</pre></details>
  <details><summary>JSON</summary><pre>${esc(JSON.stringify(raw, null, 1))}</pre></details>
  <p class="duyet"><label><input type="radio" name="d${id}" value="dung"> Dùng</label> <label><input type="radio" name="d${id}" value="sua"> Vẽ lại</label> <label><input type="radio" name="d${id}" value="bo"> Bỏ</label> <input type="text" class="gc" data-id="${id}" placeholder="ghi chú cho Gemini nếu vẽ lại" size="40"></p>
</section>`);
}

const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>So sánh hình Gemini</title>
<style>body{font-family:system-ui;margin:16px;background:#fff;color:#111}.card{border:1px solid #ddd;border-radius:8px;padding:12px;margin:12px 0}.row{display:flex;gap:16px;flex-wrap:wrap}.col{flex:1 1 300px}.col img,.col svg{max-width:100%;border:1px solid #eee;background:#fff}.warn{color:#b91c1c}.note{color:#555}pre{white-space:pre-wrap;font-size:12px}h2 small{font-weight:normal;color:#666;font-size:.7em}
#tong{position:sticky;top:0;background:#fff;padding:8px;border-bottom:1px solid #ddd}</style></head><body>
<div id="tong"><b>${cards.length} câu</b> · <button onclick="xuat()">Xuất quyết định (JSON)</button> <span id="kq"></span></div>
${cards.join("\n")}
<script>function xuat(){const o={};document.querySelectorAll('input[type=radio]:checked').forEach(r=>o[r.name.slice(1)]=r.value);const g={};document.querySelectorAll('.gc').forEach(i=>{if(i.value.trim())g[i.dataset.id]=i.value.trim();});if(Object.keys(g).length)o._ghi_chu=g;const s=JSON.stringify(o);navigator.clipboard.writeText(s);document.getElementById('kq').textContent='đã chép '+document.querySelectorAll('input[type=radio]:checked').length+' quyết định vào clipboard → dán vào quyet-dinh.json';}</script>
</body></html>`;
fs.writeFileSync(path.join(root, "so-sanh.html"), html);

const dem = (t: Ket["trang_thai"]) => ket.filter((k) => k.trang_thai === t).length;
const md = `# Kết quả nhận từ Gemini — ${new Date().toISOString().slice(0, 10)}

| | số câu |
|---|---:|
| vẽ được | ${dem("ve_duoc")} |
| Gemini báo không vẽ được | ${dem("khong_ve_duoc")} |
| JSON lỗi | ${dem("json_loi")} |
| spec không hợp lệ | ${dem("spec_loi")} |
| tin cậy < 1 | ${ket.filter((k) => (k.do_tin_cay ?? 1) < 1).length} |

${ket.filter((k) => k.trang_thai !== "ve_duoc").map((k) => `- #${k.id} ${k.trang_thai}: ${k.loi ?? k.mo_ta ?? ""}`).join("\n")}
`;
fs.writeFileSync(path.join(root, "bao-cao.md"), md);
console.log(md);
console.log(`→ mở ${path.relative(process.cwd(), path.join(root, "so-sanh.html"))}`);
