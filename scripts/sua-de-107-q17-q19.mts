// Báo lỗi #119/#120/#121 (bài 73, đề 107 Luyện tập Bài 28 Động lượng):
//  - Q19: phương án B mất \vec nên trùng D → thêm vectơ.
//  - Q17: hình là bảng LaTeX rỗng → viết lại không cần hình (đáp án A).
//   npx tsx scripts/sua-de-107-q17-q19.mts           # dry-run
//   npx tsx scripts/sua-de-107-q17-q19.mts --apply   # sao lưu questions → ghi exams.107 + question_bank 341522
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
for (const l of fs.readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const APPLY = process.argv.includes("--apply");

const { data: e, error } = await sb.from("exams").select("questions").eq("id", 107).single();
if (error || !e) throw new Error("không đọc được đề 107: " + error?.message);
const orig = e.questions as any[];
const qs = structuredClone(orig);
const q19 = qs[18], q17 = qs[16];
console.log("Q19 trước:", JSON.stringify({ question: q19.question, options: q19.options, answer: q19.answer }));
console.log("Q17 trước:", JSON.stringify({ question: q17.question, options: q17.options, answer: q17.answer }));
if (!/tabular/.test(JSON.stringify(q17))) throw new Error("Q17 không còn bảng rỗng (đã sửa rồi?)");
if (q19.options[1] !== q19.options[3]) throw new Error("Q19 B≠D (đã sửa rồi?)");

q19.options[1] = "$m_{1}\\vec{v}_{1}+m_{2}\\vec{v}_{2}.$";
q17.question = "Vật chuyển động ngược chiều dương của trục toạ độ. Phát biểu nào sau đây đúng về vectơ vận tốc $\\vec{v}$ và vectơ động lượng $\\vec{p}$ của vật?";
q17.options = [
  "$\\vec{v}$ và $\\vec{p}$ cùng hướng, đều hướng theo chiều âm.",
  "$\\vec{v}$ hướng theo chiều âm, $\\vec{p}$ hướng theo chiều dương.",
  "$\\vec{v}$ hướng theo chiều dương, $\\vec{p}$ hướng theo chiều âm.",
  "$\\vec{p}$ không có hướng.",
];
q17.answer = 0;
console.log("Q19 sau:", JSON.stringify(q19.options));
console.log("Q17 sau:", JSON.stringify(q17));
if (!APPLY) { console.log("dry-run xong, chưa ghi gì."); process.exit(0); }

const ts = new Date().toISOString().replace(/[:.]/g, "-");
fs.writeFileSync(`scripts/logs/sao-luu-de-107-${ts}.json`, JSON.stringify(orig));
const { error: e1 } = await sb.from("exams").update({ questions: qs }).eq("id", 107);
if (e1) throw new Error("ghi đề lỗi: " + e1.message);
const { data: bank } = await sb.from("question_bank").select("id,options").eq("id", 341522).single();
if (bank && Array.isArray(bank.options) && bank.options[1] === bank.options[3]) {
  const o = [...bank.options]; o[1] = q19.options[1];
  const { error: e2 } = await sb.from("question_bank").update({ options: o }).eq("id", 341522);
  console.log("question_bank 341522:", e2 ? "lỗi " + e2.message : "đã sửa");
}
const { data: after } = await sb.from("exams").select("questions").eq("id", 107).single();
const a = after!.questions as any[];
const diff = a.map((q, i) => (JSON.stringify(q) !== JSON.stringify(orig[i]) ? i + 1 : 0)).filter(Boolean);
console.log("câu đã đổi:", diff.join(","), diff.length === 2 && a.length === orig.length ? "OK" : "LỆCH!");
console.log("hoàn tác: ghi lại cột questions từ file sao lưu scripts/logs/sao-luu-de-107-" + ts + ".json");
