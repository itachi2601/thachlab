// Chuẩn hoá HÌNH THỨC lời giải (không đổi nội dung): bọc từng dòng <br> thành <p class="text-base leading-relaxed my-2">,
// thêm dòng "Chọn X." cho trắc nghiệm thiếu. Chỉ ghi question_bank (không đụng exams).
//   npx tsx scripts/chuan-hoa-loi-giai.mts [--apply] [--max=N] [--mau=N]
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const apply = process.argv.includes("--apply");
const arg = (n: string) => process.argv.find((x) => x.startsWith(`--${n}=`))?.split("=")[1];
const max = +(arg("max") ?? 1e9), nMau = +(arg("mau") ?? 6);
const P = '<p class="text-base leading-relaxed my-2">';
const plain = (h: string) => String(h ?? "").replace(/<[^>]+>/g, " ");
const rows: any[] = [];
for (let f = 0; ; f += 1000) { const { data, error } = await sb.from("question_bank").select("id,question").eq("archived", false).order("id").range(f, f + 999);
  if (error) throw new Error(error.message); rows.push(...data!); if (data!.length < 1000) break; }
const letter = (q: any): string | null => { const a = q.answer ?? q.correct; if (typeof a === "number" && a >= 0 && a < 4) return "ABCD"[a]; if (typeof a === "string" && /^[A-D]$/.test(a.trim())) return a.trim(); return null; };
const thaydoi: { id: number; truoc: any; sau: any; loai: string[] }[] = [];
const bo: Record<string, number> = {};
for (const r of rows) {
  const q = r.question ?? {}; let ex = String(q.explanation ?? ""); if (plain(ex).trim().length < 80) continue;
  const loai: string[] = []; let moi = ex;
  if (!moi.includes(P)) {
    if (/<(p|table|ul|ol|img|div|svg)[\s>]/i.test(moi)) { bo.cau_truc_la = (bo.cau_truc_la ?? 0) + 1; continue; }
    const parts = moi.split(/<br\s*\/?>|\n+/i).map((s) => s.trim()).filter(Boolean);
    if (!parts.length) continue;
    moi = parts.map((s) => `${P}${s}</p>`).join(""); loai.push("boc_p");
  }
  if (q.type === "multiple_choice" && !/Chọn\s+[A-D]/i.test(plain(moi)) && !/Đáp án( đúng)?\s*:?\s*[A-D]\b/i.test(plain(moi))) {
    const l = letter(q); if (l) { moi += `${P}Chọn ${l}.</p>`; loai.push("chon"); } else bo.khong_co_dap_an = (bo.khong_co_dap_an ?? 0) + 1;
  }
  if (loai.length) thaydoi.push({ id: r.id, truoc: q, sau: { ...q, explanation: moi }, loai });
}
const dem: Record<string, number> = {}; thaydoi.forEach((t) => t.loai.forEach((l) => (dem[l] = (dem[l] ?? 0) + 1)));
if (arg("xuat")) {
  const s = thaydoi.filter((t) => t.loai.includes("chon")).sort(() => Math.random() - 0.5).slice(0, +arg("xuat")!);
  fs.writeFileSync(arg("out")!, JSON.stringify(s.map((t) => ({ id: t.id, de: t.truoc.question ?? t.truoc.text, phuong_an: t.truoc.options, chon_them: t.sau.explanation.match(/Chọn [A-D]\./)?.[0], loi_giai: plain(t.sau.explanation) })), null, 1));
}
console.log("sẽ đổi", thaydoi.length, dem, "bỏ", bo);
for (const t of thaydoi.filter((_, i) => i % Math.max(1, Math.floor(thaydoi.length / nMau)) === 0).slice(0, nMau)) console.log("==", t.id, t.loai.join("+"), "\n", t.sau.explanation.slice(0, 500));
if (!apply) process.exit(0);
const todo = thaydoi.slice(0, max);
const bp = `scripts/logs/chuan-hoa-loi-giai-backup-${Date.now()}.json`;
fs.writeFileSync(bp, JSON.stringify(todo.map((t) => ({ id: t.id, question: t.truoc }))));
console.log("sao lưu", bp);
let ok = 0, loi = 0; const q = [...todo];
await Promise.all(Array.from({ length: 8 }, async () => { while (q.length) { const p = q.shift()!;
  for (let t = 1; t <= 3; t++) { const { error } = await sb.from("question_bank").update({ question: p.sau }).eq("id", p.id); if (!error) { ok++; break; } if (t === 3) { loi++; console.log("LỖI", p.id, error.message); } } } }));
console.log({ ok, loi });
