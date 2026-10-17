// Chạy thử sinh lời giải bằng Haiku 5.5 và DeepSeek flash trên 12 câu mẫu (scripts/data/giai-lai-thu/mau12.json) → ket-qua-thu.json.
//   npx tsx scripts/chay-thu-giai-lai.mts      (tốn tiền thật, ~vài cent; key đọc từ .env.local)
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => (L.find((l) => l.startsWith(k + "=")) ?? L.find((l) => l.replace(/^#\s*/, "").startsWith(k + "=")) ?? "").replace(/^#\s*/, "").slice(k.length + 1).trim();
const dir = "scripts/data/giai-lai-thu/";
const mau = JSON.parse(fs.readFileSync(dir + "mau12.json", "utf8")) as any[];
const SYSTEM = `Bạn là giáo viên Vật lí THPT Việt Nam. Tự giải câu hỏi từ đầu rồi viết lời giải. Đề lấy từ Word nên có thể lỗi ký tự (vd "l kg" = 1 kg, công thức vỡ) — sửa ngầm nếu chắc chắn, nếu mơ hồ thì nói rõ trong "ghi_chu".
Lời giải là HTML + LaTeX $...$ (công thức có < > viết \\lt \\gt), mỗi bước một <p class="text-base leading-relaxed my-2">…</p>. Phong cách: nêu định luật và điều kiện áp dụng trước (hệ kín? va chạm mềm hay đàn hồi?), chọn chiều dương rõ ràng, công thức chữ trước rồi thay số, kết luận có đơn vị. Đúng–sai: mỗi ý a), b), c), d) một đoạn riêng kết luận Đúng/Sai. Không dùng vai "thầy". Ngắn gọn.
Các bước suy ra: KHÔNG viết liền một dòng; mỗi phép suy ra một <p> riêng, đầu dòng là $\\Rightarrow$ (vd dòng 1 công thức, dòng 2 bắt đầu bằng $\\Rightarrow$ kèm bước biến đổi tiếp theo).
Chỉ trả về MỘT đối tượng JSON: {"answer": ..., "explanation": "<html>", "ghi_chu": ""}. answer: trắc nghiệm = "A"|"B"|"C"|"D"; trả lời ngắn = số dạng chuỗi (dấu phẩy thập phân VN); đúng–sai = mảng 4 boolean cho ý a,b,c,d.`;
const prompt = (r: any) => {
  const q = r.question;
  let s = `Loại: ${q.type}\nĐề: ${q.question}\n`;
  if (q.options) s += "Phương án:\n" + q.options.map((o: string, i: number) => "ABCD"[i] + ". " + o).join("\n");
  if (q.statements) s += "Các ý:\n" + q.statements.map((x: any, i: number) => "abcd"[i] + ") " + x.text).join("\n");
  return s;
};
const parse = (raw: string) => { const a = raw.indexOf("{"), b = raw.lastIndexOf("}"); return JSON.parse(raw.slice(a, b + 1)); };
const out: any = { haiku: {}, deepseek: {}, tong: { haiku: { in: 0, out: 0 }, deepseek: { in: 0, out: 0 } } };
const anth = new Anthropic({ apiKey: env("ANTHROPIC_API_KEY") });
const dsKey = env("DEEPSEEK_API_KEY");
await Promise.all(mau.map(async (r) => {
  const id = r.id;
  try {
    const m = await anth.messages.create({ model: "claude-haiku-5-5", max_tokens: 16000, system: SYSTEM, messages: [{ role: "user", content: prompt(r) }] });
    const text = m.content.filter((b: any) => b.type === "text").map((b: any) => b.text).join("");
    out.haiku[id] = { ...parse(text), in: m.usage.input_tokens, out: m.usage.output_tokens };
    out.tong.haiku.in += m.usage.input_tokens; out.tong.haiku.out += m.usage.output_tokens;
  } catch (e: any) { out.haiku[id] = { loi: String(e.message ?? e).slice(0, 300) }; }
  try {
    const res = await fetch("https://api.deepseek.com/chat/completions", { method: "POST", headers: { "content-type": "application/json", authorization: `Bearer ${dsKey}` },
      body: JSON.stringify({ model: "deepseek-flash", max_tokens: 16000, response_format: { type: "json_object" }, messages: [{ role: "system", content: SYSTEM }, { role: "user", content: prompt(r) }] }) });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 200)}`);
    const d: any = await res.json();
    out.deepseek[id] = { ...parse(d.choices[0].message.content), in: d.usage.prompt_tokens, out: d.usage.completion_tokens };
    out.tong.deepseek.in += d.usage.prompt_tokens; out.tong.deepseek.out += d.usage.completion_tokens;
  } catch (e: any) { out.deepseek[id] = { loi: String(e.message ?? e).slice(0, 300) }; }
}));
fs.writeFileSync(dir + "ket-qua-thu.json", JSON.stringify(out, null, 1));
console.log(JSON.stringify(out.tong), Object.values(out.haiku).filter((x: any) => x.loi).length, "lỗi haiku;", Object.values(out.deepseek).filter((x: any) => x.loi).length, "lỗi deepseek");
