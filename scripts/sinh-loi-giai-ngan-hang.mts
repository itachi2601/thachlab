// Sinh lời giải mới bằng Haiku 5.5 cho câu ngân hàng có lời giải trống/quá ngắn (<80 ký tự chữ). CHỈ ĐỌC DB, không ghi DB.
//   npx tsx scripts/sinh-loi-giai-ngan-hang.mts --mau=200 [--seed=1] [--conc=8]   chạy mẫu (gọi thường) → scripts/data/giai-lai/mau<N>.json
// Câu hợp lệ: chưa lưu trữ, loại trắc nghiệm/đúng–sai/trả lời ngắn, không có ảnh/SVG trong đề hoặc phương án.
// Mỗi kết quả: đáp án Haiku, so khớp với đáp án DB (trả lời ngắn lệch ≤2% coi là khớp), kiểm quy tắc dòng ⇒, token.
import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const arg = (k: string, d: string) => process.argv.find((a) => a.startsWith(`--${k}=`))?.slice(k.length + 3) ?? d;
const N = Number(arg("mau", "200")), SEED = Number(arg("seed", "1")), CONC = Number(arg("conc", "8")), CAP = Number(arg("tran", "3"));
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const anth = new Anthropic({ apiKey: env("ANTHROPIC_API_KEY") });
const PRICE = { in: 0.1, out: 0.5 }; // Haiku 5.5, $/1M token, gọi thường

export const SYSTEM = `Bạn là giáo viên Vật lí THPT Việt Nam. Tự giải câu hỏi từ đầu rồi viết lời giải. Đề lấy từ Word nên có thể lỗi ký tự (vd "l kg" = 1 kg, công thức vỡ, mất ^) — sửa ngầm nếu chắc chắn, nếu mơ hồ thì nói rõ trong "ghi_chu".
Lời giải là HTML + LaTeX $...$ (công thức có < > viết \\lt \\gt), mỗi bước một <p class="text-base leading-relaxed my-2">…</p>. Phong cách: nêu định luật và điều kiện áp dụng trước, chọn chiều dương/hệ quy chiếu rõ ràng khi cần, công thức chữ trước rồi thay số, kết luận có đơn vị. Đúng–sai: mỗi ý a), b), c), d) một đoạn riêng kết luận Đúng/Sai. Không dùng vai "thầy". Ngắn gọn.
Các bước suy ra: KHÔNG viết liền một dòng; mỗi phép suy ra một <p> riêng, đầu dòng là $\\Rightarrow$ (vd dòng 1 công thức, dòng 2 bắt đầu bằng $\\Rightarrow$ kèm bước biến đổi tiếp theo).
Chỉ trả về MỘT đối tượng JSON: {"answer": ..., "explanation": "<html>", "ghi_chu": ""}. answer: trắc nghiệm = "A"|"B"|"C"|"D"; trả lời ngắn = số dạng chuỗi (dấu phẩy thập phân VN); đúng–sai = mảng 4 boolean cho ý a,b,c,d.`;

const plain = (s: string) => (s ?? "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
const hasImg = (q: any) => /<img|<svg|\bsrc=/i.test(JSON.stringify([q.question, q.options, q.statements]));
const prompt = (q: any) => {
  let s = `Loại: ${q.type}\nĐề: ${q.question}\n`;
  if (q.options) s += "Phương án:\n" + q.options.map((o: string, i: number) => "ABCD"[i] + ". " + o).join("\n");
  if (q.statements) s += "Các ý:\n" + q.statements.map((x: any, i: number) => "abcd"[i] + ") " + x.text).join("\n");
  return s;
};
const dbAnswer = (q: any) => (q.type === "multiple_choice" ? "ABCD"[q.answer] : q.type === "short_answer" ? String(q.answer) : (q.statements ?? []).map((s: any) => !!s.answer));
const num = (s: string) => { const m = String(s).replace(/\s/g, "").replace(",", ".").match(/-?\d+(\.\d+)?(e-?\d+)?/i); return m ? parseFloat(m[0]) : NaN; };
const khop = (q: any, a: any) => {
  const d = dbAnswer(q);
  if (q.type === "true_false") return Array.isArray(a) && a.length === 4 && a.every((v: any, i: number) => !!v === d[i]);
  if (q.type === "multiple_choice") return String(a).trim().toUpperCase().charAt(0) === d;
  const x = num(a), y = num(d as string);
  return String(a).trim().replace(".", ",") === String(d).trim().replace(".", ",") || (isFinite(x) && isFinite(y) && Math.abs(x - y) <= 0.02 * Math.max(Math.abs(y), 1e-9));
};
/** Số đoạn <p> có dấu ⇒ không nằm ở đầu dòng, hoặc có ≥2 dấu ⇒ trong một đoạn. */
const loiMuiTen = (html: string) => (html.match(/<p[^>]*>.*?<\/p>/gs) ?? []).filter((p) => {
  const t = p.replace(/<\/?p[^>]*>/g, "").trim();
  const n = (t.match(/\\Rightarrow|\\rightarrow|⇒/g) ?? []).length;
  return n >= 2 || (n === 1 && !/^\$?\s*(\\Rightarrow|\\rightarrow|⇒)/.test(t));
}).length;

// mulberry32 để lấy mẫu lặp lại được
let st = SEED; const rnd = () => { st |= 0; st = (st + 0x6d2b79f5) | 0; let t = Math.imul(st ^ (st >>> 15), 1 | st); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };

const all: any[] = [];
for (let o = 0; ; o += 1000) {
  const { data, error } = await sb.from("question_bank").select("id,qtype,question").eq("archived", false).order("id").range(o, o + 999);
  if (error) { console.error(error.message); process.exit(1); }
  all.push(...data!); if (data!.length < 1000) break;
}
const cand = all.filter((r) => ["multiple_choice", "true_false", "short_answer"].includes(r.question?.type) && plain(r.question.explanation) .length < 80);
const ok = cand.filter((r) => !hasImg(r.question));
console.log(`ngân hàng ${all.length} · trống/ngắn ${cand.length} · bỏ vì ảnh ${cand.length - ok.length} · hợp lệ ${ok.length}`);
const pick = [...ok].sort(() => rnd() - 0.5).slice(0, N);

let spent = 0, done = 0, stop = false;
const out: any[] = [];
const parse = (raw: string) => JSON.parse(raw.slice(raw.indexOf("{"), raw.lastIndexOf("}") + 1));
async function one(r: any) {
  if (stop) return;
  try {
    const m = await anth.messages.create({ model: "claude-haiku-5-5", max_tokens: 16000, system: SYSTEM, messages: [{ role: "user", content: prompt(r.question) }] });
    const text = m.content.filter((b: any) => b.type === "text").map((b: any) => b.text).join("");
    const j = parse(text);
    const usd = (m.usage.input_tokens * PRICE.in + m.usage.output_tokens * PRICE.out) / 1e6;
    spent += usd;
    out.push({ id: r.id, type: r.question.type, db: dbAnswer(r.question), answer: j.answer, khop: khop(r.question, j.answer), ghi_chu: j.ghi_chu ?? "", explanation: j.explanation, loi_mui_ten: loiMuiTen(String(j.explanation ?? "")), tin: m.usage.input_tokens, tout: m.usage.output_tokens, usd });
  } catch (e: any) { out.push({ id: r.id, type: r.question.type, loi: String(e.message ?? e).slice(0, 200) }); }
  if (++done % 20 === 0) console.log(`  ${done}/${pick.length} · $${spent.toFixed(4)}`);
  if (spent > CAP) { stop = true; console.log("CHẠM TRẦN", CAP); }
}
const q = [...pick]; await Promise.all(Array.from({ length: CONC }, async () => { while (q.length) await one(q.shift()!); }));

fs.mkdirSync("scripts/data/giai-lai", { recursive: true });
fs.writeFileSync(`scripts/data/giai-lai/mau${N}.json`, JSON.stringify(out, null, 1));
const good = out.filter((x) => !x.loi);
const by = (t: string) => good.filter((x) => x.type === t);
const rate = (a: any[]) => `${a.filter((x) => !x.khop).length}/${a.length} lệch`;
console.log(`\nXong ${out.length} câu · lỗi gọi ${out.length - good.length} · chi phí thật $${spent.toFixed(4)} (Batch ≈ $${(spent / 2).toFixed(4)})`);
console.log(`Lệch đáp án: tổng ${rate(good)} · trắc nghiệm ${rate(by("multiple_choice"))} · đúng–sai ${rate(by("true_false"))} · trả lời ngắn ${rate(by("short_answer"))}`);
console.log(`Token ra TB ${Math.round(good.reduce((s, x) => s + x.tout, 0) / good.length)}/câu · có ghi chú mơ hồ ${good.filter((x) => x.ghi_chu).length} · vi phạm quy tắc ⇒ ${good.filter((x) => x.loi_mui_ten > 0).length} câu`);
