// Chuẩn hoá hình thức đợt 3 (không agent): (1) bỏ `\"` thừa trong chuỗi, (2) `<p>` trần → <p class=…>,
// (3) đúng–sai dồn một <p>: tách a) b) c) d) mỗi ý một <p> (mục 7 QUY-TAC-LOI-GIAI). Chỉ ghi question_bank.
// Dùng: npx tsx scripts/chuan-hoa-loi-giai-3.mts [--apply] [--mau=N]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const apply = process.argv.includes("--apply");
const nMau = +(process.argv.find((x) => x.startsWith("--mau="))?.split("=")[1] ?? 4);
const P = '<p class="text-base leading-relaxed my-2">';
const plain = (h: string) => String(h ?? "").replace(/<[^>]+>/g, " ");
const rows: any[] = [];
for (let f = 0; ; f += 1000) { const { data, error } = await sb.from("question_bank").select("id,question").eq("archived", false).order("id").range(f, f + 999);
  if (error) throw new Error(error.message); rows.push(...data!); if (data!.length < 1000) break; }
const todo: { id: number; truoc: any; sau: any; loai: string[] }[] = []; const types: Record<string, number> = {};
for (const r of rows) {
  const q = r.question ?? {}; const ex = String(q.explanation ?? ""); if (plain(ex).trim().length < 80) continue;
  let moi = ex; const loai: string[] = [];
  if (/\\"/.test(moi)) { moi = moi.replace(/\\"/g, '"'); loai.push("gachCheo"); }
  if (/<p>/i.test(moi)) { moi = moi.replace(/<p>/gi, P); loai.push("pTran"); }
  // đúng–sai dồn một <p>: đúng một <p>, không <br>/bảng/ảnh, có đủ a) b) c) d) mở đầu bằng Đúng/Sai
  const ps = moi.match(/<p[ >]/g)?.length ?? 0;
  if (ps === 1 && !/<(br|table|img|ul|ol)[\s>\/]/i.test(moi)) {
    const m = moi.match(/^<p[^>]*>(.*)<\/p>$/s);
    if (m) { const t = m[1];
      const re = /(^|[.;:)\s])([abcd])\)\s*(?:<strong>)?\s*(Đúng|Sai|đúng|sai)/g; const pos: { i: number; k: string }[] = [];
      for (const x of t.matchAll(re)) pos.push({ i: x.index! + x[1].length, k: x[2] });
      if (pos.map((p) => p.k).join("") === "abcd" && pos[0].i === 0) {
        const parts = pos.map((p, j) => t.slice(p.i, j + 1 < pos.length ? pos[j + 1].i : undefined).trim().replace(/\s*[;]\s*$/, "."));
        moi = parts.map((s) => `${P}${s}</p>`).join(""); loai.push("tachDS"); types[q.type] = (types[q.type] ?? 0) + 1; } } }
  if (!loai.length) continue;
  todo.push({ id: r.id, truoc: q, sau: { ...q, explanation: moi }, loai });
}
const dem: Record<string, number> = {}; todo.forEach((t) => t.loai.forEach((l) => (dem[l] = (dem[l] ?? 0) + 1)));
console.log("sẽ đổi", todo.length, dem, types);
for (const k of ["gachCheo", "pTran", "tachDS"]) { const c = todo.filter((t) => t.loai.includes(k)); const step = Math.max(1, Math.floor(c.length / nMau));
  for (const t of c.filter((_, i) => i % step === 0).slice(0, nMau)) console.log("==", k, t.id, "\n", t.sau.explanation.slice(0, 700)); }
if (!apply) process.exit(0);
const bp = `scripts/logs/chuan-hoa-loi-giai-3-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(todo.map((t) => ({ id: t.id, question: t.truoc })))); console.log("sao lưu", bp);
let ok = 0, loi = 0; const q = [...todo];
await Promise.all(Array.from({ length: 8 }, async () => { while (q.length) { const p = q.shift()!;
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id); if (!error) { ok++; break; } if (t === 3) { loi++; console.log("LỖI", p.id, error.message); } } } }));
console.log({ ok, loi });
