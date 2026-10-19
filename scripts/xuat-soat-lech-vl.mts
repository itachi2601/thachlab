// Dò lần 2: gom câu sua_de/doi_dap_an trong lech-vl/kq-NN.json (các lô chỉ định) → soat-N.json cho agent kiem-code (HUONG-DAN-SOAT.md).
//   npx tsx scripts/xuat-soat-lech-vl.mts <lô,lô,...> <soCau/soat=30>   vd: 01,02,03 30
import fs from "node:fs";
const D = "scripts/data/giai-lai/lech-vl/", LO = process.argv[2].split(","), N = Number(process.argv[3] ?? 30);
const rows: any[] = [];
for (const n of LO) {
  const src = new Map<number, any>(JSON.parse(fs.readFileSync(`${D}lo-${n}.json`, "utf8")).map((x: any) => [x.id, x]));
  for (const k of JSON.parse(fs.readFileSync(`${D}kq-${n}.json`, "utf8"))) {
    if (!["sua_de", "doi_dap_an"].includes(k.kl)) continue;
    const s = src.get(k.id), { explanation: lgc, ...cu } = s.cau_hoi, { explanation: lgm, ...moi } = k.cau_hoi_moi;
    rows.push({ id: k.id, kl: k.kl, cu, dap_an_db: s.dap_an_db, loi_giai_cu: lgc, moi, loi_giai_moi: lgm, thay_doi: k.thay_doi, ly_do: k.ly_do, anh: s.anh });
  }
}
let so = fs.readdirSync(D).filter((f) => /^soat-\d+\.json$/.test(f)).length;
for (let i = 0; i < rows.length; i += N) fs.writeFileSync(`${D}soat-${++so}.json`, JSON.stringify(rows.slice(i, i + N), null, 1));
console.log(rows.length, "câu → tới soat-" + so);
