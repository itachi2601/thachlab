// Chốt câu lệch viet-lai13/14/15 bằng Claude Batch API (thay agent Opus trong phiên). KHÔNG đụng DB.
//   npx tsx scripts/batch-lech-vl.mts nop [--lo=13,15] [--model=claude-opus-5-5]   nộp các lô chưa có kq-NN.json
//   npx tsx scripts/batch-lech-vl.mts thu                                          chờ xong → ghi kq-NN.json (cùng định dạng agent) + chi phí
// Sau đó chạy tiếp quy trình cũ: ap-dung-mo-ho-opus.mts --dir=…lech-vl/ --offline → xuat-soat-lech-vl.mts → dò lần 2 → --apply.
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const key = L.find((l) => l.startsWith("ANTHROPIC_API_KEY="))!.slice(18).trim();
const anth = new Anthropic({ apiKey: key });
const D = "scripts/data/giai-lai/lech-vl/", STATE = D + "batch-state.json";
const arg = (k: string) => process.argv.find((a) => a.startsWith(`--${k}=`))?.slice(k.length + 3);
const cmd = process.argv[2];
const HD = fs.readFileSync(D + "HUONG-DAN.md", "utf8");
const SYSTEM = HD + `

## Chạy qua API (không có công cụ)
Bạn KHÔNG có Bash/Read: tự tính tay cẩn thận (kiểm hai lần các phép tính). Hình (nếu có) được đính kèm ngay trong tin nhắn.
Bỏ qua phần "Đầu ra" ghi file ở trên. Chỉ trả về MỘT mảng JSON \`[{id, kl, ly_do, thay_doi?, cau_hoi_moi?}]\`, đủ mọi id đúng thứ tự, không chữ nào ngoài JSON, không bọc \`\`\`.`;

const lo = (n: number) => String(n).padStart(2, "0");
const paths = (a: any): string[] => (a ? ([] as string[]).concat(a) : []);
const media = (p: string) => (/\.png$/i.test(p) ? "image/png" : /\.gif$/i.test(p) ? "image/gif" : /\.webp$/i.test(p) ? "image/webp" : "image/jpeg");

if (cmd === "nop") {
  if (fs.existsSync(STATE)) { console.error("Đã có", STATE, "- xoá nếu muốn nộp lại."); process.exit(1); }
  const only = arg("lo")?.split(",");
  const model = arg("model") ?? "claude-opus-5-5";
  const reqs: any[] = [], lots: string[] = [];
  for (let i = 1; i <= 43; i++) {
    const s = lo(i);
    if (only ? !only.includes(s) : fs.existsSync(`${D}kq-${s}.json`)) continue;
    const items: any[] = JSON.parse(fs.readFileSync(`${D}lo-${s}.json`, "utf8"));
    const content: any[] = [{ type: "text", text: `Lô ${s}: ${items.length} câu. Dưới đây là lo-${s}.json (từng câu; ảnh nếu có được đính kèm ngay sau câu đó).` }];
    for (const it of items) {
      const { anh, ...rest } = it;
      content.push({ type: "text", text: `--- CÂU id=${it.id} ---\n${JSON.stringify(rest)}` });
      for (const p of paths(anh)) {
        if (!fs.existsSync(p)) { content.push({ type: "text", text: `(ảnh ${p} không còn trên đĩa)` }); continue; }
        content.push({ type: "image", source: { type: "base64", media_type: media(p), data: fs.readFileSync(p).toString("base64") } });
      }
    }
    content.push({ type: "text", text: `Trả về mảng JSON cho đủ ${items.length} id của lô ${s}.` });
    reqs.push({ custom_id: `lo${s}`, params: { model, max_tokens: 64000, output_config: { effort: "high" }, system: SYSTEM, messages: [{ role: "user", content }] } });
    lots.push(s);
  }
  if (!reqs.length) { console.log("Không có lô nào để nộp."); process.exit(0); }
  const b = await anth.messages.batches.create({ requests: reqs });
  fs.writeFileSync(STATE, JSON.stringify({ batch_id: b.id, lots, model, at: new Date().toISOString() }));
  console.log(`Đã nộp ${lots.length} lô (${lots.join(",")}) · ${model} · batch ${b.id}`);
} else if (cmd === "thu") {
  const st = JSON.parse(fs.readFileSync(STATE, "utf8"));
  for (;;) {
    const b = await anth.messages.batches.retrieve(st.batch_id);
    console.log(new Date().toLocaleTimeString(), b.processing_status, JSON.stringify(b.request_counts));
    if (b.processing_status === "ended") break;
    await new Promise((r) => setTimeout(r, 60000));
  }
  let tin = 0, tout = 0, ok = 0; const hong: string[] = [];
  for await (const r of await anth.messages.batches.results(st.batch_id)) {
    const s = r.custom_id.slice(2);
    if (r.result.type !== "succeeded") { hong.push(`${s}:${r.result.type}`); continue; }
    const m = r.result.message; tin += m.usage.input_tokens; tout += m.usage.output_tokens;
    const text = m.content.filter((c: any) => c.type === "text").map((c: any) => c.text).join("");
    try {
      const arr = JSON.parse(text.slice(text.indexOf("["), text.lastIndexOf("]") + 1));
      const want: number[] = JSON.parse(fs.readFileSync(`${D}lo-${s}.json`, "utf8")).map((x: any) => x.id);
      const got = new Set(arr.map((x: any) => x.id));
      const thieu = want.filter((id) => !got.has(id));
      if (thieu.length) { fs.writeFileSync(`${D}kq-${s}.thieu.json`, JSON.stringify(arr)); hong.push(`${s}:thiếu ${thieu.length} id`); continue; }
      fs.writeFileSync(`${D}kq-${s}.json`, JSON.stringify(want.map((id) => arr.find((x: any) => x.id === id))));
      ok++;
    } catch (e: any) { fs.writeFileSync(`${D}kq-${s}.raw.txt`, text); hong.push(`${s}:parse ${String(e.message).slice(0, 60)}`); }
  }
  console.log(`\nGhi ${ok}/${st.lots.length} lô · token ${tin} vào / ${tout} ra · lỗi: ${hong.join(" | ") || "không"}`);
  console.log("(Chi phí = token × đơn giá Batch của model; xem Console.)");
} else console.log("dùng: nop [--lo=..] [--model=..] | thu");
