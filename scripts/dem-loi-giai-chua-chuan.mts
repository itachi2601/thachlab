// Đếm câu có lời giải DÀI (cũ) chưa từng qua đợt giải lại 17–18/10, phân theo loại và mức vi phạm chuẩn docs/QUY-TAC-LOI-GIAI.md
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const G = "scripts/data/giai-lai/";
const done = new Set<number>();
const add = (f: string) => { try { const j = JSON.parse(fs.readFileSync(f, "utf8")); const arr = Array.isArray(j) ? j : Object.values(j); for (const x of arr as any[]) if (x && typeof x.id === "number") done.add(x.id); } catch {} };
add(G + "ket-qua.json"); add(G + "ket-qua2.json");
for (const d of fs.readdirSync(G, { withFileTypes: true }).filter((d) => d.isDirectory())) {
  const walk = (p: string) => { for (const e of fs.readdirSync(p, { withFileTypes: true })) e.isDirectory() ? walk(p + "/" + e.name) : /^(lo|kq|kl)-.*\.json$/.test(e.name) && add(p + "/" + e.name); };
  walk(G + d.name);
}
const rows: any[] = [];
for (let f = 0; ; f += 1000) { const { data, error } = await sb.from("question_bank").select("id,grade,question").eq("archived", false).order("id").range(f, f + 999); if (error) throw error; rows.push(...data!); if (data!.length < 1000) break; }
const plain = (h: string) => String(h ?? "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
const st: Record<string, number> = {};
const inc = (k: string) => (st[k] = (st[k] ?? 0) + 1);
for (const r of rows) {
  const q = r.question ?? {}; const ex = String(q.explanation ?? ""); const p = plain(ex);
  if (done.has(r.id)) { inc("đã qua đợt giải lại"); continue; }
  if (p.length < 80) { inc("trống/ngắn (chưa làm)"); continue; }
  const hasImg = /<img|<svg|\.png|\.webp|\.jpg/i.test(JSON.stringify(q));
  const ps = ex.match(/<p[ >]/g)?.length ?? 0;
  const viol = [ps < 2 && "một khối", /\\"/.test(ex) && "gạch chéo", /(⇒|\\Rightarrow)[^]*?(⇒|\\Rightarrow)/.test(ex.split(/<\/p>/).find((s) => (s.match(/Rightarrow|⇒/g) ?? []).length > 1) ?? "") && "2 ⇒/dòng",
    q.type === "multiple_choice" && !/Chọn\s+[A-D]/i.test(p) && "thiếu Chọn X", q.type === "multiple_choice" && !/(sai|không đúng|không khớp) vì/i.test(p) && "thiếu Sai vì"].filter(Boolean) as string[];
  inc(`${q.type}${hasImg ? " có ảnh" : ""} · ${viol.length ? "vi phạm" : "đạt"}`);
  for (const v of viol) inc("  ↳ " + v);
}
console.log(rows.length, "câu"); console.log(st);
