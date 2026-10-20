// Giải ĐỘC LẬP (không cho xem đáp án) các câu VL10 bóc từ Word, rồi so với đáp án gạch chân/Đ–S trong file gốc.
// Chỉ đọc/ghi file cục bộ trong scripts/data/nap-ngan-hang-vl10/, KHÔNG đụng DB.
//   npx tsx scripts/batch-nap-vl10.mts nop [--model=haiku|sonnet] [--gioi-han=N]   nộp Batch (-50%)
//   npx tsx scripts/batch-nap-vl10.mts thu                                          chờ xong → ket-qua.json + bao-cao
// Câu trả lời ngắn: đáp án nguồn = số cuối cùng trong lời giải gốc, do một lượt hỏi riêng (loi-giai-goc) rút ra.
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
import { SYSTEM, prompt, dbAnswer, khop, tachMuiTen, loiMuiTen, katexLoi } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const anth = new Anthropic({ apiKey: env("ANTHROPIC_API_KEY") });
const DIR = "scripts/data/nap-ngan-hang-vl10/", STATE = DIR + "batch-state.json";
const arg = (n: string) => process.argv.find((a) => a.startsWith(`--${n}=`))?.split("=")[1];
const MODELS: Record<string, { id: string; in: number; out: number }> = {
  haiku: { id: "claude-haiku-5-5", in: 0.05, out: 0.25 },
  sonnet: { id: "claude-sonnet-5-5", in: 1.5, out: 7.5 },
};
const strip = (s: string) => s.replace(/<[^>]+>/g, "").trim();
const cmd = process.argv[2];
const cau: any[] = JSON.parse(fs.readFileSync(DIR + "cau-bank.json", "utf8"));
// Chuẩn hoá về dạng prompt() của thư viện: question là chuỗi, statements[].text
const forPrompt = (q: any) => ({ ...q, question: strip(q.question), options: q.options?.map(strip) });

if (cmd === "nop") {
  if (fs.existsSync(STATE)) { console.error("Đã có", STATE, "— xoá nếu muốn nộp lại."); process.exit(1); }
  const m = MODELS[arg("model") ?? "haiku"];
  let ds = cau; const gh = arg("gioi-han"); if (gh) ds = ds.slice(0, Number(gh));
  const tu = arg("chi-cau-chua-khop-trong");
  if (tu) { const cu: any[] = JSON.parse(fs.readFileSync(DIR + tu, "utf8")); const ok = new Set(cu.filter((o) => o.trangThai === "khop").map((o) => o.key)); ds = ds.filter((q) => !ok.has(q.key)); }
  const reqs: any[] = [];
  for (const q of ds) {
    reqs.push({ custom_id: `g_${q.key}`, params: { model: m.id, max_tokens: 8000, system: SYSTEM, messages: [{ role: "user", content: prompt(forPrompt(q)) }], ...(m.id.includes("sonnet") ? { output_config: { effort: "medium" } } : {}) } });
    if (q.type === "short_answer")
      reqs.push({ custom_id: `n_${q.key}`, params: { model: m.id, max_tokens: 300, system: "Đọc lời giải gốc và cho biết kết quả cuối cùng của bài (đáp số). Chỉ trả JSON {\"answer\":\"<số, dấu phẩy thập phân>\",\"don_vi\":\"…\"}. Lời giải không nêu rõ kết quả thì {\"answer\":null}.", messages: [{ role: "user", content: `Đề: ${strip(q.question)}\n\nLời giải gốc:\n${q.gocLoiGiai}` }] } });
  }
  const batch = await anth.messages.batches.create({ requests: reqs });
  fs.writeFileSync(STATE, JSON.stringify({ batch_id: batch.id, model: arg("model") ?? "haiku", n: reqs.length, keys: ds.map((q) => q.key), at: new Date().toISOString() }));
  console.log(`Đã nộp ${reqs.length} yêu cầu (${ds.length} câu) · ${batch.id} · ${m.id}`);
} else if (cmd === "thu") {
  const st = JSON.parse(fs.readFileSync(STATE, "utf8")); const m = MODELS[st.model];
  for (;;) {
    const b = await anth.messages.batches.retrieve(st.batch_id);
    console.log(new Date().toLocaleTimeString(), b.processing_status, JSON.stringify(b.request_counts));
    if (b.processing_status === "ended") break;
    await new Promise((r) => setTimeout(r, 60000));
  }
  const byKey = new Map(cau.map((q) => [q.key, q]));
  const res: Record<string, any> = {}; let tin = 0, tout = 0;
  const jparse = (m: any) => { const t = m.content.filter((b: any) => b.type === "text").map((b: any) => b.text).join(""); return JSON.parse(t.slice(Math.max(0, t.search(/\{\s*"answer"/)), t.lastIndexOf("}") + 1)); };
  for await (const r of await anth.messages.batches.results(st.batch_id)) {
    const [kind, key] = [r.custom_id.slice(0, 1), r.custom_id.slice(2)];
    const e = (res[key] ??= {});
    if (r.result.type !== "succeeded") { e[kind + "_loi"] = r.result.type; continue; }
    tin += r.result.message.usage.input_tokens; tout += r.result.message.usage.output_tokens;
    try { e[kind] = jparse(r.result.message); } catch (x: any) { e[kind + "_loi"] = "parse: " + String(x.message).slice(0, 60); }
  }
  const out: any[] = [];
  for (const [key, q] of byKey) {
    const e = res[key] ?? {}; const g = e.g, n = e.n;
    const nguon = q.type === "short_answer" ? n?.answer : dbAnswer({ ...q, answer: q.answer });
    let trangThai = "chua-co-ket-qua";
    if (g) {
      if (q.type === "short_answer") {
        trangThai = nguon == null ? "khong-co-dap-so-nguon" : khop({ ...q, answer: nguon }, g.answer) ? "khop" : "LECH";
      } else trangThai = khop(q, g.answer) ? "khop" : "LECH";
    }
    const ex = g ? tachMuiTen(String(g.explanation ?? "")) : "";
    out.push({ key, type: q.type, nguon, giai: g?.answer, trangThai, ghi_chu: g?.ghi_chu ?? "", explanation: ex, mui_ten_con: loiMuiTen(ex), katex_loi: katexLoi(ex), loi: e.g_loi ?? e.n_loi });
  }
  fs.writeFileSync(DIR + "ket-qua.json", JSON.stringify(out, null, 1));
  const dem: Record<string, number> = {}; out.forEach((o) => (dem[o.trangThai] = (dem[o.trangThai] ?? 0) + 1));
  console.log(JSON.stringify(dem), `· chi phí ≈ $${((tin * m.in + tout * m.out) / 1e6).toFixed(2)} (${tin} in / ${tout} out)`);
  console.log("KaTeX lỗi:", out.filter((o) => o.katex_loi).length, "· dòng ⇒ sai chỗ:", out.filter((o) => o.mui_ten_con).length);
}
