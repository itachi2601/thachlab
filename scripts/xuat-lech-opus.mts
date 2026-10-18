// Gộp các câu trong lech.json (truc-tiep + truc-tiep-anh) kèm đề, ảnh, đáp án DB, bài giải + ghi chú của agent Sonnet → lô cho Opus kiểm tra.
//   npx tsx scripts/xuat-lech-opus.mts [soCau/lo=40] → scripts/data/giai-lai/opus/lo-NN.json
import fs from "node:fs";
const B = "scripts/data/giai-lai/", OUT = B + "opus/", N = Number(process.argv[2] ?? 40);
fs.mkdirSync(OUT, { recursive: true });
const rows: any[] = [];
for (const d of ["truc-tiep", "truc-tiep-anh"]) {
  const lech: any[] = JSON.parse(fs.readFileSync(B + d + "/lech.json", "utf8"));
  const ids = new Set(lech.map((x) => x.id));
  const src = new Map<number, any>(), kq = new Map<number, any>();
  const dapan = JSON.parse(fs.readFileSync(B + d + "/dapan.json", "utf8"));
  for (const f of fs.readdirSync(B + d)) {
    if (/^lo-\d+\.json$/.test(f)) for (const x of JSON.parse(fs.readFileSync(B + d + "/" + f, "utf8"))) src.set(x.id, x);
    if (/^kq-\d+\.json$/.test(f)) for (const x of JSON.parse(fs.readFileSync(B + d + "/" + f, "utf8"))) kq.set(x.id, x);
  }
  for (const id of ids) { const s = src.get(id), k = kq.get(id); if (!s || !k) continue;
    rows.push({ id, loai: s.loai, lop: s.lop, chu_de: s.chu_de, de: s.de, phuong_an: s.phuong_an, cac_y: s.cac_y, anh: s.anh, co_svg: s.co_svg,
      dap_an_db: dapan[id], dap_an_sonnet: k.answer, ghi_chu_sonnet: k.ghi_chu || "", loi_giai_sonnet: k.explanation }); }
}
rows.sort((a, b) => a.id - b.id);
for (let i = 0; i < rows.length; i += N) fs.writeFileSync(`${OUT}lo-${String(i / N + 1).padStart(2, "0")}.json`, JSON.stringify(rows.slice(i, i + N)));
console.log(rows.length, "câu →", Math.ceil(rows.length / N), "lô");
