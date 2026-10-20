// Gắn Chủ đề (tên lá trong question_topics) + mức độ cho cau-final.json bằng Haiku qua Batch. Không đụng DB.
//   npx tsx scripts/batch-gan-nhan-vl10.mts nop <id-dau>-<id-cuoi>     vd 119-131 (Chương III)
//   npx tsx scripts/batch-gan-nhan-vl10.mts thu                        → gan-nhan.json (chỉ nhận nhãn khớp NGUYÊN VĂN danh mục)
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const key = L.find((l) => l.startsWith("ANTHROPIC_API_KEY="))!.slice(18).trim();
const anth = new Anthropic({ apiKey: key });
const DIR = (process.env.VL10_DIR ?? "scripts/data/nap-ngan-hang-vl10") + "/", STATE = DIR + "gan-nhan-state.json";
const daCo: Record<string, any> = fs.existsSync(DIR + "gan-nhan.json") ? JSON.parse(fs.readFileSync(DIR + "gan-nhan.json", "utf8")) : {};
const cau: any[] = JSON.parse(fs.readFileSync(DIR + "cau-final.json", "utf8")).filter((q: any) => !daCo[q.key]); // chỉ câu chưa có nhãn hợp lệ
const topics: any[] = JSON.parse(fs.readFileSync("scripts/data/nap-ngan-hang-vl10/chu-de-lop10.json", "utf8")).topics;
const strip = (s: string) => s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
const body = (q: any) => `Loại: ${q.type}\nĐề: ${strip(q.question)}\n` + (q.options ? q.options.map((o: string, i: number) => "ABCD"[i] + ". " + strip(o)).join("\n") : "") + (q.statements ? q.statements.map((s: any, i: number) => "abcd"[i] + ") " + strip(s.text)).join("\n") : "");
if (process.argv[2] === "nop") {
  const [a, b] = process.argv[3].split("-").map(Number);
  const cat = topics.filter((t) => t.id >= a && t.id <= b).map((t) => t.name);
  const sys = `Gắn nhãn câu hỏi Vật lí 10. Chọn ĐÚNG MỘT chủ đề, chép NGUYÊN VĂN từ danh mục:\n${cat.map((c) => "- " + c).join("\n")}\nVà mức độ cho học sinh THPT trung bình: "de" (nhận biết/áp dụng công thức trực tiếp, 1 bước), "trung-binh" (2–3 bước hoặc kết hợp 2 khái niệm), "kho" (nhiều bước, tình huống phức tạp). Chỉ trả JSON {"topic":"…","difficulty":"de|trung-binh|kho"}.`;
  const batch = await anth.messages.batches.create({ requests: cau.map((q) => ({ custom_id: q.key, params: { model: "claude-haiku-5-5", max_tokens: 2000, system: sys, messages: [{ role: "user" as const, content: body(q) }] } })) });
  fs.writeFileSync(STATE, JSON.stringify({ batch_id: batch.id, cat }));
  console.log("Đã nộp", cau.length, batch.id);
} else {
  const st = JSON.parse(fs.readFileSync(STATE, "utf8"));
  for (;;) { const b = await anth.messages.batches.retrieve(st.batch_id); console.log(new Date().toLocaleTimeString(), b.processing_status, JSON.stringify(b.request_counts)); if (b.processing_status === "ended") break; await new Promise((r) => setTimeout(r, 30000)); }
  const out: Record<string, any> = { ...daCo }; let bad = 0;
  for await (const r of await anth.messages.batches.results(st.batch_id)) {
    if (r.result.type !== "succeeded") { bad++; continue; }
    try {
      const t = r.result.message.content.filter((c: any) => c.type === "text").map((c: any) => c.text).join("");
      const j = JSON.parse(t.slice(t.indexOf("{"), t.lastIndexOf("}") + 1));
      if (st.cat.includes(j.topic) && ["de", "trung-binh", "kho"].includes(j.difficulty)) out[r.custom_id] = j; else bad++;
    } catch { bad++; }
  }
  fs.writeFileSync(DIR + "gan-nhan.json", JSON.stringify(out, null, 1));
  console.log("Gắn được", Object.keys(out).length, "(còn thiếu", bad, ")");
}
