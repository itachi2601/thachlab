// Xuất lô viết "Sai vì" cho trắc nghiệm còn thiếu (theo khong-chuan-ids.json → thieuSaiVi), chưa nằm trong viet-lai*/lo-*.json.
// Tách không ảnh → <dir-chu>, có ảnh → <dir-anh> (tải ảnh về truc-tiep-anh/img, thêm "anh").
//   npx tsx scripts/xuat-sai-vi.mts <dir-chu> <dir-anh> [coLo=40]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import crypto from "node:crypto";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const [dChu, dAnh] = process.argv.slice(2), coLo = +(process.argv[4] ?? 40);
const G = "scripts/data/giai-lai/", IMG = G + "truc-tiep-anh/img/";
const daXong = new Set<number>();
for (const d of fs.readdirSync(G).filter((d) => /^viet-lai\d*$/.test(d)))
  for (const f of fs.readdirSync(G + d).filter((f) => /^lo-\d+\.json$/.test(f)))
    for (const x of JSON.parse(fs.readFileSync(`${G}${d}/${f}`, "utf8"))) daXong.add(x.id);
const ids = (JSON.parse(fs.readFileSync(G + "khong-chuan-ids.json", "utf8")).thieuSaiVi as number[]).filter((i) => !daXong.has(i));
const rows: any[] = [];
for (let i = 0; i < ids.length; i += 200) { const { data, error } = await sb.from("question_bank").select("id,grade,topic_name,question,lint_flags").in("id", ids.slice(i, i + 200)).eq("archived", false); if (error) throw error; rows.push(...data!); }
async function tai(url: string): Promise<string | null> {
  const ext = (url.match(/\.(png|jpe?g|webp|gif)(\?|$)/i)?.[1] ?? "jpg").toLowerCase();
  const f = IMG + crypto.createHash("md5").update(url).digest("hex").slice(0, 12) + "." + ext;
  if (!fs.existsSync(f)) for (let t = 0; t < 3; t++) { try { const r = await fetch(url); if (r.ok) { fs.writeFileSync(f, Buffer.from(await r.arrayBuffer())); break; } } catch {} if (t === 2) return null; }
  return "/Users/MAC/Projects/thachlab/" + f;
}
const chu: any[] = [], anh: any[] = []; let hu = 0;
for (const r of rows) {
  if ((r.lint_flags ?? []).length) { hu++; continue; }
  const q = r.question, o: any = { id: r.id, lop: String(r.grade), chu_de: r.topic_name, de: q.question ?? q.text, phuong_an: q.options ?? q.choices, dap_an: q.answer ?? q.correct, loi_giai_cu: q.explanation };
  const blob = JSON.stringify(o);
  if (/<img|<svg|\.png|\.webp|\.jpg/i.test(JSON.stringify(q))) {
    const urls = [...blob.matchAll(/<img[^>]*?src=\\"([^"\\]+)\\"/g)].map((m) => m[1]);
    o.anh = (await Promise.all(urls.map(tai))).filter(Boolean); o.co_svg = /<svg/.test(blob) || undefined; anh.push(o);
  } else chu.push(o);
}
console.log({ chu: chu.length, anh: anh.length, bo_lint: hu });
for (const [dir, arr, hd] of [[dChu, chu, "viet-lai3"], [dAnh, anh, "viet-lai3"]] as const) {
  fs.mkdirSync(G + dir, { recursive: true });
  for (let i = 0; i * coLo < arr.length; i++) fs.writeFileSync(`${G}${dir}/lo-${String(i + 1).padStart(2, "0")}.json`, JSON.stringify(arr.slice(i * coLo, (i + 1) * coLo), null, 1));
  fs.copyFileSync(`${G}${hd}/HUONG-DAN.md`, `${G}${dir}/HUONG-DAN.md`);
  console.log(dir, Math.ceil(arr.length / coLo), "lô");
}
