// Chuẩn hoá hình thức đợt 2: thêm dòng chốt "Chọn X." cho trắc nghiệm còn thiếu (kể cả lời giải đã có <p> kiểu khác / bảng),
// đổi <p> trần thành <p class="text-base leading-relaxed my-2">. Bỏ câu mà lời giải nêu chữ cái KHÁC đáp án DB (in ra để xem).
// Chỉ ghi question_bank. Dùng: npx tsx scripts/chuan-hoa-loi-giai-2.mts [--apply] [--mau=N]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const apply = process.argv.includes("--apply");
const nMau = +(process.argv.find((x) => x.startsWith("--mau="))?.split("=")[1] ?? 5);
const P = '<p class="text-base leading-relaxed my-2">';
const plain = (h: string) => String(h ?? "").replace(/<[^>]+>/g, " ");
const rows: any[] = [];
for (let f = 0; ; f += 1000) { const { data, error } = await sb.from("question_bank").select("id,question").eq("archived", false).order("id").range(f, f + 999);
  if (error) throw new Error(error.message); rows.push(...data!); if (data!.length < 1000) break; }
const letter = (q: any): string | null => { const a = q.answer ?? q.correct; if (typeof a === "number" && a >= 0 && a < 4) return "ABCD"[a]; if (typeof a === "string" && /^[A-D]$/.test(a.trim())) return a.trim(); return null; };
const todo: { id: number; truoc: any; sau: any }[] = []; const bo: Record<string, number[]> = {};
const ghi = (k: string, id: number) => (bo[k] ??= []).push(id);
for (const r of rows) {
  const q = r.question ?? {}; const ex = String(q.explanation ?? "");
  if (q.type !== "multiple_choice" || plain(ex).trim().length < 80) continue;
  const pl = plain(ex);
  if (/Chọn\s+[A-D]/i.test(pl)) continue;
  const l = letter(q); if (!l) { ghi("khong_dap_an", r.id); continue; }
  // lời giải nêu chữ cái khác đáp án DB?
  const nhac = [...pl.matchAll(/(?:Đáp án(?: đúng)?|Chọn|đáp án)\s*(?:là)?\s*:?\s*\(?([A-D])\b/g)].map((m) => m[1]);
  if (nhac.length && nhac[nhac.length - 1] !== l) { ghi("nhac_chu_khac", r.id); continue; }
  let moi = ex;
  if (!/<p[\s>]/i.test(moi)) { // dạng <br>/xuống dòng thuần
    if (/<(table|ul|ol|img|div|svg)[\s>]/i.test(moi)) { ghi("cau_truc_la", r.id); continue; }
    moi = moi.split(/<br\s*\/?>|\n+/i).map((s) => s.trim()).filter(Boolean).map((s) => `${P}${s}</p>`).join("");
  } else moi = moi.replace(/<p>/gi, P);
  moi += `${P}Chọn ${l}.</p>`;
  todo.push({ id: r.id, truoc: q, sau: { ...q, explanation: moi } });
}
console.log("sẽ đổi", todo.length, Object.fromEntries(Object.entries(bo).map(([k, v]) => [k, v.length])));
fs.mkdirSync("scripts/data/giai-lai", { recursive: true });
fs.writeFileSync("scripts/data/giai-lai/chuan-hoa-2-bo.json", JSON.stringify(bo));
const step = Math.max(1, Math.floor(todo.length / nMau));
for (const t of todo.filter((_, i) => i % step === 0).slice(0, nMau)) console.log("==", t.id, "\n", plain(t.sau.explanation).slice(-300));
if (!apply) process.exit(0);
const bp = `scripts/logs/chuan-hoa-loi-giai-2-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(todo.map((t) => ({ id: t.id, question: t.truoc })))); console.log("sao lưu", bp);
let ok = 0, loi = 0; const q = [...todo];
await Promise.all(Array.from({ length: 8 }, async () => { while (q.length) { const p = q.shift()!;
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id); if (!error) { ok++; break; } if (t === 3) { loi++; console.log("LỖI", p.id, error.message); } } } }));
console.log({ ok, loi });
