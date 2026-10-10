// Trang xem nhanh các ảnh NGHI mất nội dung: file rất nhỏ so với số điểm ảnh (vd 340 B cho 132×100 = chỉ còn nền + khung trục).
// Không tải ảnh về — trang <img> tới thẳng URL Storage. CHỈ ĐỌC.   npx tsx scripts/xem-anh-nghi-hong.mts [maxBytes=1200]
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "data", "kiem-ke-anh-ngan-hang");
type Row = { id: number; grade: string | null; topic: string | null; loai: string; anh?: { src: string; bytes: number | null; w: number | null; h: number | null }[] };
const rows: Row[] = JSON.parse(fs.readFileSync(path.join(dir, "rows.json"), "utf8"));
const MAX = Number(process.argv[2] ?? 1200);
const cards = rows
  .map((r) => ({ r, a: (r.anh ?? []).filter((a) => a.src.startsWith("http") && a.bytes !== null && a.bytes < MAX) }))
  .filter((x) => x.a.length)
  .sort((p, q) => Math.min(...p.a.map((a) => a.bytes!)) - Math.min(...q.a.map((a) => a.bytes!)))
  .map(({ r, a }) => `<section><h3>#${r.id} <small>L${r.grade ?? "?"} · ${r.loai} · ${r.topic ?? ""}</small></h3>${a.map((x, i) => `<figure><img loading="lazy" src="${x.src}" style="max-height:90px"><figcaption>${x.bytes} B · ${x.w ?? "?"}×${x.h ?? "?"}</figcaption><input class="gc" data-id="${r.id}" data-i="${i + 1}" data-src="${x.src}" placeholder="ghi chú" size="22"></figure>`).join("")}</section>`);
fs.writeFileSync(path.join(dir, "anh-nghi-hong.html"), `<!doctype html><meta charset="utf-8"><title>Ảnh nghi mất nội dung</title><style>body{font-family:system-ui;margin:12px}section{display:inline-block;vertical-align:top;border:1px solid #ddd;border-radius:6px;padding:6px 8px;margin:4px;max-width:300px}h3{margin:0 0 4px;font-size:13px}small{color:#666;font-weight:normal}figure{display:inline-block;margin:2px;vertical-align:top}#tong{position:sticky;top:0;background:#fff;padding:6px;border-bottom:1px solid #ddd}figcaption{font-size:10px;color:#666}</style><div id="tong"><button onclick="xuat()">Xuất ghi chú (JSON)</button> <span id="kq"></span></div><h2>${cards.length} câu có ảnh < ${MAX} B (nhỏ nhất trước)</h2>${cards.join("")}<script>function xuat(){const o=[];document.querySelectorAll(".gc").forEach(i=>{if(i.value.trim())o.push({id:Number(i.dataset.id),anh:Number(i.dataset.i),src:i.dataset.src,ghi_chu:i.value.trim()})});const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(o,null,1)],{type:"application/json"}));a.download="ghi-chu-anh.json";a.click();document.getElementById("kq").textContent="đã tải ghi-chu-anh.json ("+o.length+" ảnh có ghi chú) vào Downloads — báo tôi";}</script>`);
console.log(`${cards.length} câu → scripts/data/kiem-ke-anh-ngan-hang/anh-nghi-hong.html`);
