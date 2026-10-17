// Báo lỗi #118 (đề 910 câu 6: bảng số liệu chữ ngăn tab, khó đọc) và rà #119–121 (đề 107 câu 53: bảng LaTeX hỏng, dính câu khác).
//   npx tsx scripts/sua-de-910-q6-107-q53.mts           # dry-run
//   npx tsx scripts/sua-de-910-q6-107-q53.mts --apply   # sao lưu questions của 2 đề → ghi → kiểm lại
// Đề 107: Q53 giữ phần "Câu 10" (đúng với 4 mệnh đề đang lưu); phần 3 kg/4 kg bị dính được tách thành câu mới ở cuối đề.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
for (const l of fs.readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const APPLY = process.argv.includes("--apply");
const P = (s: string) => `<p class="text-base leading-relaxed my-2">${s}</p>`;

const { data: rows, error } = await sb.from("exams").select("id,questions,question_count").in("id", [910, 107]);
if (error || rows?.length !== 2) throw new Error("không đọc được 2 đề: " + error?.message);
const orig = Object.fromEntries(rows.map((r) => [r.id, structuredClone(r.questions) as any[]]));
const q910 = structuredClone(orig[910]);
const q107 = structuredClone(orig[107]);

// ---- đề 910 câu 6: bảng HTML thật ----
const q6 = q910[5];
const re = /bảng số liệu sau:<br>[\s\S]*?(?=Nhiệt lượng cần cung cấp)/;
const done910 = q6.question.includes("tl-table");
if (!done910 && !re.test(q6.question)) throw new Error("910 câu 6: không thấy bảng chữ cũ");
const table =
  `bảng số liệu sau:</p><div class="table-scroll"><table class="tl-table"><thead><tr><th></th><th>Khối lượng riêng (kg/m³)</th><th>Nhiệt độ sôi (°C)</th><th>Nhiệt dung riêng (J/(kg.K))</th><th>Nhiệt hóa hơi riêng (J/kg)</th></tr></thead><tbody>` +
  `<tr><td>Ethylic alcohol</td><td>789</td><td>78</td><td>—</td><td>$0{,}9\\cdot10^{6}$</td></tr>` +
  `<tr><td>Nước</td><td>997</td><td>100</td><td>4 200</td><td>$2{,}3\\cdot10^{6}$</td></tr></tbody></table></div><p class="text-base leading-relaxed my-2">`;
if (!done910) q6.question = q6.question.replace(re, table);
if (!done910 && !/^<p/.test(q6.question)) q6.question = `<p class="text-base leading-relaxed my-2">${q6.question}`;
if (!done910 && !/<\/p>$/.test(q6.question)) q6.question += "</p>";

// ---- đề 107 câu 53: tách ----
const q53 = q107[52];
if (!/tabular/.test(q53.question)) throw new Error("107 câu 53: không còn tabular (đã sửa rồi?)");
const iCau10 = q53.question.indexOf("<strong>Câu 10");
const iHuong = q53.question.indexOf("<strong>Hướng dẫn giải");
if (iCau10 < 0 || iHuong < 0) throw new Error("107 câu 53: không thấy mốc Câu 10 / Hướng dẫn giải");
const cau10 = q53.question.slice(iCau10).replace(/^<strong>Câu 10: \[CTST\]<\/strong>\s*/, "").replace(/<\/p>\s*$/, "");
q53.question = P(cau10.replace(/\s*trong các trường hợp sau\s*$/, ", xét các phát biểu sau."));
const newQ = {
  form: "bai_tap", type: "true_false", topic: q53.topic, difficulty: "trung-binh", difficultySource: "ai",
  question: P("Hai vật có khối lượng $m_{1}=3\\ kg$, $m_{2}=4\\ kg$ chuyển động với độ lớn vận tốc lần lượt là $v_{1}=v_{2}=2\\ m/s$. Xét các phát biểu sau."),
  statements: [
    { text: "Động lượng của vật 1 và vật 2 lần lượt là $8\\ kg.m/s$ và $6\\ kg.m/s$.", answer: false },
    { text: "Khi hai vật chuyển động ngược chiều nhau thì tổng động lượng của hệ là $2\\ kg.m/s$.", answer: true },
    { text: "Khi hai vật chuyển động vuông góc với nhau thì động lượng của hệ là $12\\ kg.m/s$.", answer: false },
    { text: "Khi hai vật chuyển động hợp với nhau góc $60^\\circ$ thì động lượng của hệ là $12{,}2\\ kg.m/s$.", answer: true },
  ],
  explanation:
    P("$p_{1}=m_{1}v_{1}=6\\ kg.m/s$; $p_{2}=m_{2}v_{2}=8\\ kg.m/s$ nên a) sai.") +
    P("Ngược chiều: $p=|p_{2}-p_{1}|=2\\ kg.m/s$ nên b) đúng.") +
    P("Vuông góc: $p=\\sqrt{p_{1}^{2}+p_{2}^{2}}=10\\ kg.m/s$ nên c) sai.") +
    P("Hợp góc $60^\\circ$: $p=\\sqrt{p_{1}^{2}+p_{2}^{2}+2p_{1}p_{2}\\cos60^\\circ}=\\sqrt{148}\\approx12{,}2\\ kg.m/s$ nên d) đúng."),
};
q107.push(newQ);
q53.explanation =
  P("Động lượng hai vật: $p_{1}=m_{1}v_{1}=0{,}4\\ kg.m/s$; $p_{2}=m_{2}v_{2}=0{,}3\\ kg.m/s$. Động lượng của hệ $\\vec{p}=\\vec{p}_{1}+\\vec{p}_{2}$.") +
  P("a) sai vì $p_{1}=0{,}4\\ kg.m/s$; b) đúng.") +
  P("c) Vuông góc nhau: $p=\\sqrt{p_{1}^{2}+p_{2}^{2}}=0{,}5\\ kg.m/s$ nên đúng.") +
  P("d) $\\tan\\alpha=\\dfrac{p_{2}}{p_{1}}=0{,}75\\Rightarrow\\alpha\\approx37^\\circ$ (không phải $42^\\circ$) nên sai.");

console.log("910 Q6 sau:", q6.question);
console.log("107 Q53 sau:", JSON.stringify({ question: q53.question, statements: q53.statements }));
console.log("107 câu mới (#" + q107.length + "):", newQ.question);
if (!APPLY) { console.log("dry-run xong, chưa ghi gì."); process.exit(0); }

const ts = new Date().toISOString().replace(/[:.]/g, "-");
fs.writeFileSync(`scripts/logs/sao-luu-de-910-107-${ts}.json`, JSON.stringify({ orig }));
for (const [id, q] of [[910, q910], [107, q107]] as const) {
  if (id === 910 && done910) continue;
  const { error: e } = await sb.from("exams").update({ questions: q }).eq("id", id);
  if (e) throw new Error(`ghi đề ${id} lỗi: ${e.message}`);
}
const { data: after } = await sb.from("exams").select("id,questions,question_count").in("id", [910, 107]);
for (const r of after!) {
  const was = orig[r.id], now = r.questions as any[];
  const ch = now.map((q, i) => (JSON.stringify(q) !== JSON.stringify(was[i]) ? i + 1 : 0)).filter(Boolean);
  console.log(`đề ${r.id}: số câu ${was.length}→${now.length}, count=${r.question_count}, câu đổi: ${ch.join(",")}`);
}
console.log("hoàn tác: ghi lại cột questions (và question_count đề 107) từ scripts/logs/sao-luu-de-910-107-" + ts + ".json");
