// Xuất lô viết lại lời giải ĐÚNG–SAI và TRẢ LỜI NGẮN (không ảnh/SVG, không cờ lỗi) chưa theo chuẩn mục 7–8 QUY-TAC-LOI-GIAI.
//   npx tsx scripts/xuat-viet-lai-ds.mts <thư-mục> [soLo=0 chỉ đếm] [coLo=40] [--loai=true_false|short_answer] [--lop=12]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const a = process.argv.slice(2).filter((x) => !x.startsWith("--"));
const name = a[0], soLo = +(a[1] ?? 0), coLo = +(a[2] ?? 40);
const flag = (n: string) => process.argv.find((x) => x.startsWith(`--${n}=`))?.split("=")[1];
const loaiF = flag("loai"), lopF = flag("lop");
const daXong = new Set<number>();
for (const d of fs.readdirSync("scripts/data/giai-lai").filter((d) => /^viet-lai\d*$/.test(d)))
  for (const f of fs.readdirSync("scripts/data/giai-lai/" + d).filter((f) => /^lo-\d+\.json$/.test(f)))
    for (const x of JSON.parse(fs.readFileSync(`scripts/data/giai-lai/${d}/${f}`, "utf8"))) daXong.add(x.id);
const rows: any[] = [];
for (let from = 0; ; from += 500) {
  let d: any; for (let t = 0; t < 5; t++) { const r = await sb.from("question_bank").select("id,grade,topic_name,question,lint_flags").eq("archived", false).order("id").range(from, from + 499);
    if (!r.error) { d = r.data; break; } await new Promise((s) => setTimeout(s, 2000)); }
  if (!d) throw new Error("timeout"); rows.push(...d); if (d.length < 500) break;
}
const plain = (h: string) => String(h ?? "").replace(/<[^>]+>/g, " ");
export const chuanDS = (q: any) => {
  const ex = String(q.explanation ?? ""), ps = [...ex.matchAll(/<p class="text-base leading-relaxed my-2">(.*?)<\/p>/gs)].map((m) => plain(m[1]).trim());
  if (q.type === "true_false") return ["a", "b", "c", "d"].every((c) => ps.some((p) => new RegExp(`^${c}\\)\\s*(Đúng|Sai)\\.`, "i").test(p)));
  return /Đáp số/i.test(plain(ex)) && ps.length >= 2;
};
const cand = rows.filter((r) => {
  const q = r.question ?? {}; if (q.type !== "true_false" && q.type !== "short_answer") return false; if (loaiF && q.type !== loaiF) return false;
  if (/<img|<svg|image_url|"image"|\.png|\.webp|\.jpg/i.test(JSON.stringify(q.question) + JSON.stringify(q.statements))) return false;
  if ((r.lint_flags ?? []).length || daXong.has(r.id) || (lopF && String(r.grade) !== lopF)) return false;
  return !chuanDS(q);
});
const by: Record<string, number> = {}; cand.forEach((r) => { const k = r.question.type + "/L" + r.grade; by[k] = (by[k] ?? 0) + 1; });
console.log("ứng viên", cand.length, by);
if (!soLo) process.exit(0);
const dir = `scripts/data/giai-lai/${name}/`; fs.mkdirSync(dir, { recursive: true });
const pick = cand.sort(() => 0).slice(0, soLo * coLo);
for (let i = 0; i < soLo; i++) {
  const part = pick.slice(i * coLo, (i + 1) * coLo); if (!part.length) break;
  fs.writeFileSync(dir + `lo-${String(i + 1).padStart(2, "0")}.json`, JSON.stringify(part.map((r) => { const q = r.question;
    return { id: r.id, lop: String(r.grade), chu_de: r.topic_name, loai: q.type, de: q.question, cac_y: q.statements?.map((s: any) => s.text), dap_an: q.type === "true_false" ? q.statements.map((s: any) => !!s.answer) : String(q.answer), loi_giai_cu: q.explanation }; }), null, 1));
}
console.log("đã xuất", Math.min(soLo, Math.ceil(pick.length / coLo)), "lô vào", dir);
