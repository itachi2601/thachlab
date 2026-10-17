// Sinh lời giải hàng loạt bằng Haiku 5.5 qua Message Batches (giá -50%). CHỈ ĐỌC DB, không ghi DB.
//   npx tsx scripts/batch-giai-lai.mts nop [--gioi-han=N]   chọn câu trống/ngắn không ảnh → nộp Batch, ghi scripts/data/giai-lai/batch-state.json
//   npx tsx scripts/batch-giai-lai.mts thu                  chờ Batch xong → scripts/data/giai-lai/ket-qua.json + báo cáo (lệch đáp án, chi phí thật, ⇒, KaTeX)
// Câu có đáp án khớp DB thì giữ lời giải (đã tự tách dòng ⇒); câu lệch để lượt kiểm thứ hai / trang duyệt.
import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { SYSTEM, TYPES, plain, hasImg, prompt, dbAnswer, khop, loiMuiTen, tachMuiTen, katexLoi } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const anth = new Anthropic({ apiKey: env("ANTHROPIC_API_KEY") });
const DIR = "scripts/data/giai-lai/", STATE = DIR + "batch-state.json";
const PRICE = { in: 0.05, out: 0.25 }; // Haiku 5.5 qua Batch, $/1M token
const cmd = process.argv[2];

async function layCau() {
  const all: any[] = [];
  for (let o = 0; ; o += 1000) {
    const { data, error } = await sb.from("question_bank").select("id,question").eq("archived", false).order("id").range(o, o + 999);
    if (error) throw new Error(error.message);
    all.push(...data!); if (data!.length < 1000) break;
  }
  return all.filter((r) => TYPES.includes(r.question?.type) && plain(r.question.explanation).length < 80 && !hasImg(r.question));
}

if (cmd === "nop") {
  fs.mkdirSync(DIR, { recursive: true });
  if (fs.existsSync(STATE)) { console.error("Đã có", STATE, "- xoá nếu muốn nộp lại."); process.exit(1); }
  let cau = await layCau();
  const gh = process.argv.find((a) => a.startsWith("--gioi-han="))?.slice(11);
  if (gh) cau = cau.slice(0, Number(gh));
  const batch = await anth.messages.batches.create({
    requests: cau.map((r) => ({ custom_id: `q${r.id}`, params: { model: "claude-haiku-5-5", max_tokens: 8000, system: SYSTEM, messages: [{ role: "user" as const, content: prompt(r.question) }] } })),
  });
  fs.writeFileSync(STATE, JSON.stringify({ batch_id: batch.id, n: cau.length, ids: cau.map((r) => r.id), at: new Date().toISOString() }));
  console.log(`Đã nộp ${cau.length} câu · batch ${batch.id}`);
} else if (cmd === "thu") {
  const st = JSON.parse(fs.readFileSync(STATE, "utf8"));
  for (;;) {
    const b = await anth.messages.batches.retrieve(st.batch_id);
    console.log(new Date().toLocaleTimeString(), b.processing_status, JSON.stringify(b.request_counts));
    if (b.processing_status === "ended") break;
    await new Promise((r) => setTimeout(r, 60000));
  }
  const cau = new Map((await layCau()).map((r) => [r.id, r.question]));
  const out: any[] = [];
  let tin = 0, tout = 0;
  for await (const r of await anth.messages.batches.results(st.batch_id)) {
    const id = Number(r.custom_id.slice(1)); const q = cau.get(id);
    if (r.result.type !== "succeeded" || !q) { out.push({ id, loi: r.result.type }); continue; }
    const m = r.result.message; tin += m.usage.input_tokens; tout += m.usage.output_tokens;
    try {
      const text = m.content.filter((b: any) => b.type === "text").map((b: any) => b.text).join("");
      const j = JSON.parse(text.slice(Math.max(0, text.search(/\{\s*"answer"/)), text.lastIndexOf("}") + 1));
      const ex = tachMuiTen(String(j.explanation ?? ""));
      out.push({ id, type: q.type, db: dbAnswer(q), answer: j.answer, khop: khop(q, j.answer), ghi_chu: j.ghi_chu ?? "", explanation: ex, mui_ten_con: loiMuiTen(ex), katex_loi: katexLoi(ex), tout: m.usage.output_tokens });
    } catch (e: any) { out.push({ id, loi: "parse: " + String(e.message).slice(0, 80) }); }
  }
  fs.writeFileSync(DIR + "ket-qua.json", JSON.stringify(out));
  const good = out.filter((x) => !x.loi), by = (t: string) => good.filter((x) => x.type === t);
  const lech = (a: any[]) => `${a.filter((x) => !x.khop).length}/${a.length}`;
  const usd = (tin * PRICE.in + tout * PRICE.out) / 1e6;
  console.log(`\n=== Xong ${out.length}/${st.n} câu · lỗi gọi/parse ${out.length - good.length}`);
  console.log(`Chi phí thật (Batch): $${usd.toFixed(3)} · token ${tin} vào / ${tout} ra`);
  console.log(`Lệch đáp án: tổng ${lech(good)} · trắc nghiệm ${lech(by("multiple_choice"))} · đúng–sai ${lech(by("true_false"))} · trả lời ngắn ${lech(by("short_answer"))}`);
  console.log(`Khớp & dùng được: ${good.filter((x) => x.khop && !x.katex_loi && !x.mui_ten_con).length} · khớp nhưng KaTeX lỗi ${good.filter((x) => x.khop && x.katex_loi).length} · khớp nhưng còn ⇒ sai chỗ ${good.filter((x) => x.khop && x.mui_ten_con).length} · Haiku ghi chú mơ hồ ${good.filter((x) => x.ghi_chu).length}`);
} else if (cmd === "nop2") {
  // Lượt kiểm thứ hai: Sonnet 5.5 giải MÙ lại các câu Haiku lệch DB (và 8 câu parse lỗi)
  const S2 = DIR + "batch2-state.json";
  if (fs.existsSync(S2)) { console.error("Đã có", S2); process.exit(1); }
  const k1: any[] = JSON.parse(fs.readFileSync(DIR + "ket-qua.json", "utf8"));
  const ids = new Set(k1.filter((x) => x.loi || x.khop === false).map((x) => x.id));
  const cau = (await layCau()).filter((r) => ids.has(r.id));
  const batch = await anth.messages.batches.create({
    requests: cau.map((r) => ({ custom_id: `q${r.id}`, params: { model: "claude-sonnet-5-5", max_tokens: 16000, output_config: { effort: "medium" }, system: SYSTEM, messages: [{ role: "user" as const, content: prompt(r.question) }] } as any })),
  });
  fs.writeFileSync(S2, JSON.stringify({ batch_id: batch.id, n: cau.length, at: new Date().toISOString() }));
  console.log(`Đã nộp ${cau.length} câu cho Sonnet 5.5 · batch ${batch.id}`);
} else if (cmd === "thu2") {
  const st = JSON.parse(fs.readFileSync(DIR + "batch2-state.json", "utf8"));
  for (;;) {
    const b = await anth.messages.batches.retrieve(st.batch_id);
    console.log(new Date().toLocaleTimeString(), b.processing_status, JSON.stringify(b.request_counts));
    if (b.processing_status === "ended") break;
    await new Promise((r) => setTimeout(r, 60000));
  }
  const cau = new Map((await layCau()).map((r) => [r.id, r.question]));
  const k1 = new Map((JSON.parse(fs.readFileSync(DIR + "ket-qua.json", "utf8")) as any[]).map((x) => [x.id, x]));
  const same = (t: string, a: any, b: any) => t === "true_false" ? Array.isArray(a) && Array.isArray(b) && a.length === 4 && a.every((v: any, i: number) => !!v === !!b[i])
    : String(a).trim().replace(".", ",").toUpperCase() === String(b).trim().replace(".", ",").toUpperCase();
  const out: any[] = []; let tin = 0, tout = 0;
  for await (const r of await anth.messages.batches.results(st.batch_id)) {
    const id = Number(r.custom_id.slice(1)); const q = cau.get(id); const h = k1.get(id);
    if (r.result.type !== "succeeded" || !q) { out.push({ id, loi: r.result.type }); continue; }
    const m = r.result.message; tin += m.usage.input_tokens; tout += m.usage.output_tokens;
    try {
      const text = m.content.filter((b: any) => b.type === "text").map((b: any) => b.text).join("");
      const j = JSON.parse(text.slice(Math.max(0, text.search(/\{\s*"answer"/)), text.lastIndexOf("}") + 1));
      const ex = tachMuiTen(String(j.explanation ?? ""));
      const khopDB = khop(q, j.answer);
      const haikuCo = h && !h.loi;
      const loai = khopDB ? "db_dung" : haikuCo && same(q.type, j.answer, h.answer) ? "db_nghi_sai" : "ba_ben_khac";
      out.push({ id, type: q.type, db: dbAnswer(q), haiku: haikuCo ? h.answer : null, sonnet: j.answer, loai, ghi_chu: j.ghi_chu ?? "", explanation: ex, mui_ten_con: loiMuiTen(ex), katex_loi: katexLoi(ex) });
    } catch (e: any) { out.push({ id, loi: "parse: " + String(e.message).slice(0, 80) }); }
  }
  fs.writeFileSync(DIR + "ket-qua2.json", JSON.stringify(out));
  const good = out.filter((x) => !x.loi), c = (l: string) => good.filter((x) => x.loai === l).length;
  console.log(`\n=== Sonnet xong ${out.length}/${st.n} · lỗi ${out.length - good.length} · chi phí thật (Batch) $${((tin * 1 + tout * 5) / 1e6).toFixed(3)} · ${tin} vào / ${tout} ra`);
  console.log(`DB đúng (Sonnet khớp DB, Haiku sai): ${c("db_dung")} · DB nghi sai (Sonnet = Haiku ≠ DB): ${c("db_nghi_sai")} · ba bên khác nhau: ${c("ba_ben_khac")}`);
} else console.log("dùng: nop | thu | nop2 | thu2");
