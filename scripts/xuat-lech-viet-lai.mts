// Gộp câu lệch/ghi chú của viet-lai13/14/15 (lech.json) kèm đề đầy đủ từ question_bank, ảnh, bài giải + ghi chú Sonnet → lô nhỏ cho Opus chốt.
//   npx tsx scripts/xuat-lech-viet-lai.mts [soCau/lo=20] → scripts/data/giai-lai/lech-vl/lo-NN.json (+ ds-id.json)
// Định dạng lô giống mo-ho/opus nên dùng chung HUONG-DAN và scripts/ap-dung-mo-ho-opus.mts --dir=scripts/data/giai-lai/lech-vl/
// Không ghi đè lô đã có kq (chạy lại chỉ thêm câu mới vào lô mới).
import fs from "node:fs";
const B = "scripts/data/giai-lai/", OUT = B + "lech-vl/", N = Number(process.argv[2] ?? 20);
fs.mkdirSync(OUT, { recursive: true });
const rows: any[] = [];
for (const d of ["viet-lai13", "viet-lai14", "viet-lai15"]) {
  const lech: any[] = JSON.parse(fs.readFileSync(B + d + "/lech.json", "utf8"));
  const src = new Map<number, any>(), kq = new Map<number, any>();
  for (const f of fs.readdirSync(B + d)) {
    if (/^lo-\d+\.json$/.test(f)) for (const x of JSON.parse(fs.readFileSync(B + d + "/" + f, "utf8"))) src.set(x.id, x);
    if (/^kq-\d+\.json$/.test(f)) for (const x of JSON.parse(fs.readFileSync(B + d + "/" + f, "utf8"))) kq.set(x.id, x);
  }
  for (const l of lech) {
    const s = src.get(l.id), k = kq.get(l.id); if (!s) continue;
    rows.push({ id: l.id, nguon: d, lop: s.lop, chu_de: s.chu_de, anh: s.anh, co_svg: s.co_svg,
      ly_do_lech: l.loi ?? (l.khop ? "Sonnet khớp đáp án nhưng có ghi chú" : "Sonnet ra đáp án KHÁC DB"),
      sonnet: { answer: k?.answer, ghi_chu: k?.ghi_chu ?? "", explanation: k?.explanation ?? "" } });
  }
}
const daCo = new Set<number>();
for (const f of fs.readdirSync(OUT).filter((f) => /^lo-\d+\.json$/.test(f))) for (const x of JSON.parse(fs.readFileSync(OUT + f, "utf8"))) daCo.add(x.id);
const moi = rows.filter((r) => !daCo.has(r.id));
const { createClient } = await import("@supabase/supabase-js");
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const cur = new Map<number, any>();
const ids = moi.map((r) => r.id);
for (let i = 0; i < ids.length; i += 200) {
  const { data, error } = await sb.from("question_bank").select("id,archived,question").in("id", ids.slice(i, i + 200));
  if (error) throw new Error(error.message);
  data!.forEach((r) => cur.set(r.id, r));
}
const { dbAnswer } = await import("./lib/giai-lai-chung.mts");
const out = moi.filter((r) => cur.has(r.id) && !cur.get(r.id).archived).map((r) => ({ ...r, cau_hoi: cur.get(r.id).question, dap_an_db: dbAnswer(cur.get(r.id).question) }));
// ưu tiên: lệch đáp án trước (rủi ro cao), rồi ghi chú; trong nhóm theo id
out.sort((a, b) => Number(a.ly_do_lech.includes("KHÁC")) - Number(b.ly_do_lech.includes("KHÁC")) || a.id - b.id).reverse();
let so = fs.readdirSync(OUT).filter((f) => /^lo-\d+\.json$/.test(f)).length;
for (let i = 0; i < out.length; i += N) fs.writeFileSync(`${OUT}lo-${String(++so).padStart(2, "0")}.json`, JSON.stringify(out.slice(i, i + N), null, 1));
console.log(`${rows.length} câu lệch · đã có lô ${daCo.size} · bỏ (đã ẩn/không thấy) ${moi.length - out.length} · mới ${out.length} → ${Math.ceil(out.length / N)} lô, tới lo-${so}`);
