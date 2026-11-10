// Gắn khung video tương tác (content/thi-nghiem/video-khung/<id>.json) vào hộp video ĐÃ CÓ trong bài lý thuyết:
// chỉ sửa đúng THẺ MỞ của hộp đứng ngay sau `<!--video:<id>-->` (thêm class tl-box--khung + data-khung), KHÔNG gỡ/chèn lại
// khối nào. (Dùng `chen-video-thi-nghiem.mts --lam-lai` cho việc này làm mất hộp thí nghiệm + chú thích ở theory.html bài
// cảm ứng và đoạn "Nếu không xem được video" ở bài chuyển thể — 29/10/2026.)
//
//   npx tsx scripts/gan-khung-video.mts --bai l12-boyle-charles            # xem thử (dry-run)
//   npx tsx scripts/gan-khung-video.mts --bai l12-boyle-charles --apply    # ghi theory.src.html, theory.html, bundle.json
//   npx tsx scripts/gan-khung-video.mts --bai l12-cam-ung-dien-tu --id tn-l12-camungdt-01 --apply   # chỉ một clip
//   npx tsx scripts/gan-khung-video.mts --go --bai l12-boyle-charles --apply   # gỡ khung (về hộp tĩnh)
//
// Chạy lại được (đã gắn thì cập nhật data-khung theo JSON mới). URL clip + ảnh bìa lấy từ chính thẻ <video> của hộp.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const argv = process.argv.slice(2);
const APPLY = argv.includes("--apply");
const GO = argv.includes("--go");
const bai = argv[argv.indexOf("--bai") + 1];
if (!bai || bai.startsWith("--")) {
  console.error("Dùng: npx tsx scripts/gan-khung-video.mts --bai <slug> [--apply] [--go]");
  process.exit(1);
}
const idArg = argv.indexOf("--id") >= 0 ? argv[argv.indexOf("--id") + 1] : "";
const chiId = new Set(idArg ? idArg.split(",") : []); // --id a,b: chỉ làm các thí nghiệm này (mặc định: mọi hộp có JSON khung)
const dir = path.join(root, "content/lesson-samples", bai);
const khungDir = path.join(root, "content/thi-nghiem/video-khung");

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
// <!--video:ID-->\n<div class="tl-box tl-box--video[ tl-box--khung][ tl-note]"[ data-khung="…"]>…<video src=".." poster="..">
const BLOCK =
  /(<!--video:(tn-[a-z0-9-]+)-->\s*<div class="tl-box tl-box--video)((?: [a-z0-9-]+)*)"((?: data-khung="[^"]*")?)>((?:(?!<!--video:)[\s\S])*?<video src="([^"]+)"(?: poster="([^"]+)")?)/g;

function xuLy(html: string): { html: string; ghi: string[]; boQua: string[] } {
  const ghi: string[] = [];
  const boQua: string[] = [];
  const out = html.replace(BLOCK, (m, head, id, cls, _old, rest, mp4, poster) => {
    if (chiId.size && !chiId.has(id)) return m;
    const f = path.join(khungDir, id + ".json");
    const classes = cls.replace(/ tl-box--khung/g, "");
    if (GO) {
      ghi.push(id + " (gỡ)");
      return `${head}${classes}">${rest}`;
    }
    if (!fs.existsSync(f)) {
      boQua.push(id + " (chưa có JSON khung)");
      return m;
    }
    const d = JSON.parse(fs.readFileSync(f, "utf8"));
    if (/-->|\]>|<\/(?:style|title)/i.test(JSON.stringify(d))) throw new Error(id + ": JSON khung chứa --> / ]> / </style — DOMPurify sẽ gỡ data-khung");
    d.video = mp4;
    if (poster) d.poster = poster;
    ghi.push(id);
    return `${head}${classes} tl-box--khung" data-khung="${esc(JSON.stringify(d))}">${rest}`;
  });
  return { html: out, ghi, boQua };
}

let tong = 0;
for (const f of ["theory.src.html", "theory.html"]) {
  const file = path.join(dir, f);
  if (!fs.existsSync(file)) continue;
  const r = xuLy(fs.readFileSync(file, "utf8"));
  console.log(`${f}: ${r.ghi.length} hộp ${GO ? "gỡ khung" : "gắn khung"} ${r.ghi.join(", ")}${r.boQua.length ? " | bỏ qua: " + r.boQua.join(", ") : ""}`);
  tong += r.ghi.length;
  if (APPLY && r.html !== fs.readFileSync(file, "utf8")) fs.writeFileSync(file, r.html, "utf8");
}
const bf = path.join(dir, "bundle.json");
if (fs.existsSync(bf)) {
  const raw = fs.readFileSync(bf, "utf8");
  const b = JSON.parse(raw);
  const r = xuLy(b.theory_html ?? "");
  console.log(`bundle.json (theory_html): ${r.ghi.length} hộp`);
  if (APPLY && r.html !== b.theory_html) {
    b.theory_html = r.html;
    const m = raw.match(/^\{\n( +)"/);
    fs.writeFileSync(bf, JSON.stringify(b, null, m ? m[1].length : 1) + (raw.endsWith("\n") ? "\n" : ""), "utf8");
  }
}
console.log(APPLY ? "ĐÃ GHI" : "XEM THỬ (thêm --apply để ghi)", `— ${tong} hộp ở 2 file HTML`);
