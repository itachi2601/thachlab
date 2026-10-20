// DÒ LẦN 2 cho các câu đã ghi vào ngân hàng (Ẩn): (1) máy: cấu trúc, KaTeX, dấu vết markup Word; (2) Sonnet giải độc lập lần nữa, so với đáp án CUỐI CÙNG đã ghi.
//   npx tsx scripts/batch-do-lan2-vl10.mts nop      nộp Batch Sonnet cho các key trong ghi-bao-cao.json
//   npx tsx scripts/batch-do-lan2-vl10.mts thu      → do2-ket-qua.json + báo cáo
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
import { SYSTEM, prompt, khop, katexLoi } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const anth = new Anthropic({ apiKey: L.find((l) => l.startsWith("ANTHROPIC_API_KEY="))!.slice(18).trim() });
const DIR = "scripts/data/nap-ngan-hang-vl10/", STATE = DIR + "do2-state.json";
const ghi: string[] = JSON.parse(fs.readFileSync(DIR + "ghi-bao-cao.json", "utf8")).ghi;
const final = new Map<string, any>(JSON.parse(fs.readFileSync(DIR + "cau-final.json", "utf8")).map((q: any) => [q.key, q]));
const strip = (s: string) => s.replace(/<[^>]+>/g, "").trim();
const forP = (q: any) => ({ ...q, question: strip(q.question), options: q.options?.map(strip) });
if (process.argv[2] === "nop") {
  const reqs = ghi.map((k) => ({ custom_id: k, params: { model: "claude-sonnet-5-5", max_tokens: 16000, output_config: { effort: "medium" }, system: SYSTEM, messages: [{ role: "user" as const, content: prompt(forP(final.get(k))) }] } as any }));
  const b = await anth.messages.batches.create({ requests: reqs });
  fs.writeFileSync(STATE, JSON.stringify({ batch_id: b.id, n: reqs.length })); console.log("Đã nộp", reqs.length, b.id);
} else {
  const st = JSON.parse(fs.readFileSync(STATE, "utf8"));
  for (;;) { const b = await anth.messages.batches.retrieve(st.batch_id); console.log(new Date().toLocaleTimeString(), b.processing_status, JSON.stringify(b.request_counts)); if (b.processing_status === "ended") break; await new Promise((r) => setTimeout(r, 30000)); }
  const ai: Record<string, any> = {}; let tin = 0, tout = 0;
  for await (const r of await anth.messages.batches.results(st.batch_id)) {
    if (r.result.type !== "succeeded") { ai[r.custom_id] = { loi: r.result.type }; continue; }
    tin += r.result.message.usage.input_tokens; tout += r.result.message.usage.output_tokens;
    try { const t = r.result.message.content.filter((c: any) => c.type === "text").map((c: any) => c.text).join(""); ai[r.custom_id] = JSON.parse(t.slice(Math.max(0, t.search(/\{\s*"answer"/)), t.lastIndexOf("}") + 1)); } catch { ai[r.custom_id] = { loi: "parse" }; }
  }
  const out: any[] = [];
  for (const k of ghi) {
    const q = final.get(k); const flags: string[] = [];
    const blob = JSON.stringify([q.question, q.options, q.statements, q.explanation]);
    if (q.type === "multiple_choice" && (q.options?.length !== 4 || !(q.answer >= 0 && q.answer < 4))) flags.push("cau-truc-MC");
    if (q.type === "true_false" && q.statements?.length !== 4) flags.push("cau-truc-DS");
    if (q.type === "short_answer" && !String(q.answer ?? "").trim()) flags.push("TLN-rong-dap-so");
    if (/mathit|mathbf|\{\.underline\}|\{\.mark\}|\*\*|Hướng dẫn giải|!\[|\]\(/.test(blob)) flags.push("dau-vet-markup");
    if (/\$\s*\$|\\\\\s*\\\\/.test(blob)) flags.push("cong-thuc-rong");
    const kl = katexLoi(q.question + (q.options ?? []).join(" ") + (q.statements ?? []).map((s: any) => s.text).join(" ") + (q.explanation ?? ""));
    if (kl) flags.push("katex-loi:" + kl);
    if (!q.explanation) flags.push("khong-co-loi-giai");
    const a = ai[k]; let kq = "khong-co-ket-qua";
    if (a && !a.loi) kq = khop(q, a.answer) ? "khop" : "LECH";
    out.push({ key: k, type: q.type, final: q.type === "multiple_choice" ? "ABCD"[q.answer] : q.type === "true_false" ? q.statements.map((s: any) => s.answer) : q.answer, ai: a?.answer, kq, flags, duyet: q.duyet });
  }
  fs.writeFileSync(DIR + "do2-ket-qua.json", JSON.stringify(out, null, 1));
  const dem: Record<string, number> = {}; out.forEach((o) => (dem[o.kq] = (dem[o.kq] ?? 0) + 1));
  const fl: Record<string, number> = {}; out.forEach((o) => o.flags.forEach((f: string) => (fl[f.split(":")[0]] = (fl[f.split(":")[0]] ?? 0) + 1)));
  console.log(JSON.stringify(dem), JSON.stringify(fl), `· ≈ $${((tin * 1.5 + tout * 7.5) / 1e6).toFixed(2)}`);
}
