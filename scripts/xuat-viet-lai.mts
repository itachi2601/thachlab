// Xuất lô viết lại "Sai vì" cho trắc nghiệm tính toán chưa có đoạn đó (không ảnh/SVG).
//   npx tsx scripts/xuat-viet-lai.mts <tên-thư-mục> [soLo=0 chỉ đếm] [coLo=40] [--lop=12]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const a = process.argv.slice(2).filter((x) => !x.startsWith("--"));
const name = a[0], soLo = +(a[1] ?? 0), coLo = +(a[2] ?? 40);
const lopF = process.argv.find((x) => x.startsWith("--lop="))?.slice(6);
const daXong = new Set<number>();
for (const d of fs.readdirSync("scripts/data/giai-lai").filter((d) => /^viet-lai\d*$/.test(d)))
  for (const f of fs.readdirSync("scripts/data/giai-lai/" + d).filter((f) => /^lo-\d+\.json$/.test(f)))
    for (const x of JSON.parse(fs.readFileSync(`scripts/data/giai-lai/${d}/${f}`, "utf8"))) daXong.add(x.id);
const rows: any[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("question_bank").select("id,grade,topic_name,archived,question").eq("archived", false).range(from, from + 999);
  if (error) throw new Error(error.message); rows.push(...data!); if (data!.length < 1000) break;
}
const plain = (h: string) => String(h ?? "").replace(/<[^>]+>/g, " ");
const cand = rows.filter((r) => {
  const q = r.question ?? {}; if (q.type !== "multiple_choice" && q.type !== undefined && q.type !== "mcq") return false;
  const opts: string[] = q.options ?? q.choices ?? []; if (opts.length !== 4) return false;
  const blob = JSON.stringify(q); if (/<img|<svg|image_url|"image"|\.png|\.webp|\.jpg/i.test(blob)) return false;
  if (/(sai|không đúng|không khớp) vì/i.test(plain(q.explanation))) return false;
  if (opts.filter((o) => /\d/.test(plain(o)) && plain(o).replace(/\$/g, "").length < 40).length < 4) return false;
  return !daXong.has(r.id) && (!lopF || String(r.grade) === lopF);
});
const byG: Record<string, number> = {}; cand.forEach((r) => (byG[r.grade] = (byG[r.grade] ?? 0) + 1));
console.log("ứng viên", cand.length, byG, "mẫu khoá question:", Object.keys(rows[0].question));
if (!soLo) process.exit(0);
const dir = `scripts/data/giai-lai/${name}/`; fs.mkdirSync(dir, { recursive: true });
const pick = cand.slice(0, soLo * coLo);
for (let i = 0; i < soLo; i++) {
  const part = pick.slice(i * coLo, (i + 1) * coLo); if (!part.length) break;
  fs.writeFileSync(dir + `lo-${String(i + 1).padStart(2, "0")}.json`, JSON.stringify(part.map((r) => { const q = r.question;
    return { id: r.id, lop: String(r.grade), chu_de: r.topic_name, de: q.question ?? q.text, phuong_an: q.options ?? q.choices, dap_an: q.answer ?? q.correct, loi_giai_cu: q.explanation }; }), null, 1));
}
fs.copyFileSync("scripts/data/giai-lai/viet-lai3/HUONG-DAN.md", dir + "HUONG-DAN.md");
console.log("đã xuất", Math.min(soLo, Math.ceil(pick.length / coLo)), "lô vào", dir);
