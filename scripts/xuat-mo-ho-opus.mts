// Xuất 214 câu "đề mơ hồ" (hỏi/ẩn/đổi/sửa — đúng tập của trang duyệt lap-duyet-mo-ho.mts) thành lô cho agent Opus soát lại + viết lại đề/lời giải.
//   npx tsx scripts/xuat-mo-ho-opus.mts [soCau/lo=36]  → scripts/data/giai-lai/mo-ho/opus/lo-NN.json
import fs from "node:fs";
const DIR = "scripts/data/giai-lai/mo-ho/", OUT = DIR + "opus/";
const N = Number(process.argv[2] ?? 36);
const ls = fs.readdirSync(DIR), rd = (f: string) => JSON.parse(fs.readFileSync(DIR + f, "utf8")) as any[];
const src = new Map<number, any>(), kq = new Map<number, any>();
for (const f of ls.filter((f) => /^lo-\d+\.json$/.test(f))) rd(f).forEach((x) => src.set(x.id, x));
for (const f of ls.filter((f) => /^kq-\d+\.json$/.test(f))) rd(f).forEach((x) => kq.set(x.id, x));
if (ls.includes("kq-08b.json")) rd("kq-08b.json").forEach((x) => kq.set(x.id, x));
const trungDb = (k: any) => k.kl === "doi" && String(k.dap_an_dung ?? "").replace(/\s/g, "").charAt(0).toUpperCase() === String(src.get(k.id)?.dap_an_db ?? "").charAt(0).toUpperCase();
const rows = [...kq.values()].filter((k) => !trungDb(k) && (k.kl !== "ghi" || k.sua)).sort((a, b) => a.id - b.id).map((k) => {
  const s = src.get(k.id);
  return { id: k.id, lop: s.lop, chu_de: s.chu_de, cau_hoi: s.cau_hoi, dap_an_db: s.dap_an_db, ghi_chu_haiku: s.ghi_chu_haiku ?? "",
    sonnet: { kl: k.kl, tu_giai: k.tu_giai, dap_an_dung: k.dap_an_dung ?? "", sua: k.sua ?? "", ly_do: k.ly_do ?? "" } };
});
fs.mkdirSync(OUT, { recursive: true });
for (let i = 0; i * N < rows.length; i++) fs.writeFileSync(OUT + `lo-${String(i + 1).padStart(2, "0")}.json`, JSON.stringify(rows.slice(i * N, (i + 1) * N), null, 1));
console.log(rows.length, "câu →", Math.ceil(rows.length / N), "lô");
