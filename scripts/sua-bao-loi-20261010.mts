// Sửa lỗi hiển thị/đáp án do báo lỗi #67, #75–82 (đề 910, 759). Mặc định DRY-RUN; thêm --ghi để ghi thật. Sao lưu ra scripts/logs/.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));
const GHI = process.argv.includes("--ghi");
type Rep = [string, string];
const edits: Record<number, Record<number, { question?: Rep[]; explanation?: Rep[]; options?: Rep[]; set?: Record<string, unknown> }>> = {
  910: {
    1: {
      question: [["0,5 m3", "$0{,}5\\ \\text{m}^3$"], ["1,013.105 Pa", "$1{,}013\\cdot10^{5}\\ \\text{Pa}$"], ["4.106 m2/s2", "$4\\cdot10^{6}\\ \\text{m}^2/\\text{s}^2$"]],
      options: [["5, 42.1028.", "$5{,}42\\cdot10^{28}$."], ["4,01.1025.", "$4{,}01\\cdot10^{25}$."], ["1,14.1025.", "$1{,}14\\cdot10^{25}$."], ["4, 11.1025.", "$4{,}11\\cdot10^{25}$."]],
      explanation: [["$n=\\frac{m}{M}=\\frac{0,0379875}{2}=0,01899375\\left(mol\\right)$", "$n=\\frac{m}{M}=\\frac{37{,}9875\\ \\text{g}}{2\\ \\text{g/mol}}\\approx 18{,}99\\ \\text{mol}$"], ["$N=n.N_A=,01899375.6,02.10^{23}\\approx 1,14.10^{25}$", "$N=n.N_A=18{,}99\\cdot6{,}02\\cdot10^{23}\\approx 1{,}14\\cdot10^{25}$"]],
    },
    6: {
      question: [["acohol", "alcohol"], ["Nhiệt độ sôi (C)", "Nhiệt độ sôi (°C)"], ["0,9.106", "$0{,}9\\cdot10^{6}$"], ["2,3.106", "$2{,}3\\cdot10^{6}$"], ["78 C xấp xỉ", "78 °C xấp xỉ"]],
      explanation: [["acohol", "alcohol"], ["78 C,", "78 °C,"], ["100 C", "100 °C"]],
    },
    10: {
      question: [["đến 2000C", "đến $200\\ ^\\circ\\text{C}$"], ["nhiệt lượng kể", "nhiệt lượng kế"], ["ở 200C.", "ở $20\\ ^\\circ\\text{C}$."], ["là 22,40C.", "là $22{,}4\\ ^\\circ\\text{C}$."]],
    },
    17: {
      question: [["bằng   lần", "bằng $\\frac{5}{9}$ lần"], ["là 0∘R", "là $0\\ ^\\circ\\text{R}$"]],
      explanation: [["Chênh lệch 10R", "Chênh lệch $1\\ ^\\circ\\text{R}$"], [/<br>Sử dụng dữ kiện sau đây[\s\S]*$/ as unknown as string, ""]],
    },
    24: {
      set: { question: "Nhôm nóng chảy ở nhiệt độ bao nhiêu °C? (làm tròn đến hàng đơn vị)", explanation: "Nhôm nóng chảy ở 660 °C." },
    },
    27: {
      question: [["1, 44.105 J", "$1{,}44\\cdot10^{5}\\ \\text{J}$"]],
      explanation: [["1,44.10^5/0,8", "$1{,}44\\cdot10^{5}/0{,}8$"]],
    },
  },
  759: {
    18: {
      set: { answer: "39,9" },
      explanation: [["\\approx 40\\ \\mu", "\\approx 39{,}9\\ \\mu"]],
    },
  },
};
function app(s: string, reps: Rep[] | undefined, tag: string): string {
  let out = s;
  for (const [a, b] of reps ?? []) {
    const hit = typeof a === "string" ? out.includes(a) : (a as unknown as RegExp).test(out);
    if (!hit) { console.log("  ! KHÔNG KHỚP", tag, String(a).slice(0, 40)); continue; }
    out = typeof a === "string" ? out.split(a).join(b) : out.replace(a as unknown as RegExp, b);
  }
  return out;
}
for (const [examId, byQ] of Object.entries(edits)) {
  const { data, error } = await sb.from("exams").select("id,questions").eq("id", Number(examId)).single();
  if (error || !data) { console.error(examId, error); process.exit(1); }
  fs.writeFileSync(`scripts/logs/sao-luu-exam-${examId}-20261010.json`, JSON.stringify(data.questions));
  const qs = data.questions as any[];
  for (const [qn, e] of Object.entries(byQ)) {
    const q = qs[Number(qn) - 1];
    console.log(`exam ${examId} câu ${qn}`);
    if (e.question) q.question = app(q.question, e.question, "question");
    if (e.explanation) q.explanation = app(q.explanation ?? "", e.explanation, "explanation");
    if (e.options) q.options = q.options.map((o: string, i: number) => app(o, [e.options![i]], "option" + i));
    if (e.set) Object.assign(q, e.set);
  }
  if (GHI) {
    const { error: e2 } = await sb.from("exams").update({ questions: qs }).eq("id", Number(examId));
    console.log(examId, e2 ? "LỖI " + e2.message : "đã ghi");
  } else console.log(examId, "(dry-run, chưa ghi)");
}
