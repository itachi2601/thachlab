// Đếm câu (chưa lưu trữ) có lời giải dài nhưng KHÔNG theo chuẩn docs/QUY-TAC-LOI-GIAI.md.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const rows: any[] = [];
for (let f = 0; ; f += 1000) { const { data, error } = await sb.from("question_bank").select("id,grade,question").eq("archived", false).order("id").range(f, f + 999);
  if (error) throw new Error(error.message); rows.push(...data!); if (data!.length < 1000) break; }
const plain = (h: string) => String(h ?? "").replace(/<[^>]+>/g, " ");
const stat: Record<string, number> = {}; const ids: Record<string, number[]> = {};
const add = (k: string, id: number) => { stat[k] = (stat[k] ?? 0) + 1; (ids[k] ??= []).push(id); };
let dai = 0, chuan = 0;
for (const r of rows) { const q = r.question ?? {}, ex = String(q.explanation ?? ""); if (plain(ex).trim().length < 80) continue; dai++;
  const ps = ex.match(/<p[ >]/g)?.length ?? 0, bad: string[] = [];
  if (!/<p class="text-base leading-relaxed my-2">/.test(ex)) bad.push("khongP");
  if (ps < 2 && plain(ex).length > 200) bad.push("mot_khoi");
  if ([...ex.matchAll(/<p[^>]*>(.*?)<\/p>/gs)].some((m) => (m[1].match(/Rightarrow|⇒/g)?.length ?? 0) >= 2)) bad.push("2mui_ten");
  const mc = q.type === "multiple_choice";
  if (mc && !/Chọn\s+[A-D]/i.test(plain(ex))) bad.push("thieuChon");
  if (mc && (q.options ?? []).filter((o: string) => /\d/.test(plain(o))).length >= 4 && !/(sai|không đúng|không khớp) vì/i.test(plain(ex))) bad.push("thieuSaiVi");
  if (/\\"/.test(ex)) bad.push("gachCheo");
  if (!bad.length) chuan++; bad.forEach((b) => add(b, r.id)); if (bad.length) add("KHONG_CHUAN", r.id); }
console.log({ tong: rows.length, loiGiaiDai: dai, chuan, ...stat });
fs.writeFileSync("scripts/data/giai-lai/khong-chuan-ids.json", JSON.stringify(ids));
