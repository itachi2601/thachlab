// Gộp giai/out-*.json (subagent giải độc lập) + đáp án tô vàng trong cau-bank.json -> ket-qua.json (cùng dạng batch-nap-vl10 thu).
//   VL10_DIR=scripts/data/nap-ngan-hang-vl12/c1 npx tsx scripts/data/nap-ngan-hang-vl12/gop-ket-qua.mts
import fs from "node:fs";
import { tachMuiTen, loiMuiTen, katexLoi, dbAnswer } from "../../lib/giai-lai-chung.mts";
const DIR = process.env.VL10_DIR + "/";
const cau: any[] = JSON.parse(fs.readFileSync(DIR + "cau-bank.json", "utf8"));
const res: Record<string, any> = {};
for (const f of fs.readdirSync(DIR + "giai").filter((x) => /^out-\d+\.json$/.test(x))) Object.assign(res, JSON.parse(fs.readFileSync(DIR + "giai/" + f, "utf8")));
const out = cau.map((q) => {
  const g = res[q.key]; const nguon = dbAnswer(q);
  const a = g?.answer == null || g.answer === "null" ? null : String(g.answer).trim().toUpperCase().charAt(0);
  const trangThai = !g ? "chua-co-ket-qua" : a == null ? "khong-chac" : a === nguon ? "khop" : "LECH";
  const ex = tachMuiTen(String(g?.explanation ?? ""));
  return { key: q.key, type: q.type, nguon, giai: a, trangThai, ghi_chu: g?.ghi_chu ?? "", explanation: ex, mui_ten_con: loiMuiTen(ex), katex_loi: katexLoi(ex) };
});
fs.writeFileSync(DIR + "ket-qua.json", JSON.stringify(out, null, 1));
const dem: Record<string, number> = {}; out.forEach((o) => (dem[o.trangThai] = (dem[o.trangThai] ?? 0) + 1));
console.log(JSON.stringify(dem), "· KaTeX lỗi:", out.filter((o) => o.katex_loi).length, "· ⇒ sai chỗ:", out.filter((o) => o.mui_ten_con).length);
for (const o of out.filter((o) => o.trangThai !== "khop")) console.log(o.key, o.trangThai, "nguồn", o.nguon, "giải", o.giai, "|", String(o.ghi_chu).slice(0, 90));
