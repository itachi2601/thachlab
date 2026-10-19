// Sinh meta.boi_canh (tình huống mở bài) cho các chương AVCN bằng Messages API (10 lời gọi ngắn, không batch).
//   npx tsx scripts/sinh-boi-canh-avcn.mts            # sinh → scripts/logs/boi-canh-avcn/<n>.json (chưa ghi vào bai.json)
//   npx tsx scripts/sinh-boi-canh-avcn.mts --ap-dung  # ghi các bản đã sinh vào meta.boi_canh của bai.json
// Cần .env.local: ANTHROPIC_API_KEY.
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..");
const SAMPLES = path.join(ROOT, "content/lesson-samples");
const LOG = path.join(ROOT, "scripts/logs/boi-canh-avcn");
fs.mkdirSync(LOG, { recursive: true });
const dirs = fs.readdirSync(SAMPLES).filter((d) => /^avcn-chapter-\d+-/.test(d));
const chapterOf = (d: string) => Number(d.match(/^avcn-chapter-(\d+)-/)![1]);

if (process.argv.includes("--ap-dung")) {
  for (const d of dirs) {
    const f = path.join(LOG, `${chapterOf(d)}.json`);
    if (!fs.existsSync(f)) { console.log(`- bỏ qua ${d} (chưa sinh)`); continue; }
    const p = path.join(SAMPLES, d, "data/bai.json");
    const bai = JSON.parse(fs.readFileSync(p, "utf8"));
    bai.meta.boi_canh = JSON.parse(fs.readFileSync(f, "utf8"));
    fs.writeFileSync(p, JSON.stringify(bai, null, 2) + "\n");
    console.log(`✓ ghi ${d}`);
  }
  process.exit(0);
}

const key = process.env.ANTHROPIC_API_KEY ?? fs.readFileSync(path.join(ROOT, ".env.local"), "utf8").match(/^ANTHROPIC_API_KEY=(.*)$/m)?.[1]?.trim().replace(/^["']|["']$/g, "");
if (!key) { console.error("✗ thiếu ANTHROPIC_API_KEY"); process.exit(1); }
const client = new Anthropic({ apiKey: key });

const SYSTEM = `Bạn viết phần MỞ BÀI cho bài Anh văn chuyên ngành Cơ khí dành cho sinh viên cao đẳng nghề trình độ tiếng Anh yếu.
Mục tiêu: sinh viên thấy ngay "từ này dùng ở xưởng để làm gì", không nói về điểm số hay đề thi.
Trả về DUY NHẤT một JSON object, không markdown, gồm:
- "tieu_de": tiêu đề ngắn tiếng Việt (≤8 chữ) của tình huống, không có dấu hai chấm.
- "tinh_huong": 40–60 chữ tiếng Việt, ngôi "em" (sinh viên là người trong cuộc), một cảnh cụ thể ở xưởng/nhà máy/gara có hành động và một vướng mắc liên quan tiếng Anh (tài liệu, nhãn, hướng dẫn, email, lệnh của thợ cả/khách nước ngoài). Nhúng 2–3 thuật ngữ tiếng Anh của chương, bọc trong <strong></strong>. Không dùng từ "điểm", "thi", "đề".
- "viec_can_lam": MỘT câu tiếng Việt bắt đầu bằng động từ, nêu việc cụ thể em sẽ làm được sau bài này trong tình huống đó.
- "quay_lai": MỘT câu hỏi tiếng Việt ngắn để quay lại tình huống ở cuối bài ("Giờ em ... chưa?").
Tình huống phải thật với nghề cơ khí, không bịa số liệu, không tên thương hiệu, đúng nghĩa các từ.`;

for (const d of dirs) {
  const n = chapterOf(d);
  const out = path.join(LOG, `${n}.json`);
  if (fs.existsSync(out) && !process.argv.includes("--lai")) { console.log(`- có sẵn ${n}`); continue; }
  const bai = JSON.parse(fs.readFileSync(path.join(SAMPLES, d, "data/bai.json"), "utf8"));
  const terms = bai.tu_vung.flatMap((c: any) => c.tu.map((t: any) => `${t.term} = ${t.vi}`)).join("; ");
  const res = await client.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 6000,
    system: SYSTEM,
    messages: [{ role: "user", content: `Chương ${n}: ${bai.meta.title_en} (${bai.meta.title_vi}).\nTừ khoá: ${terms}` }],
  });
  const text = res.content.map((b: any) => b.text ?? "").join("").trim().replace(/^```json\s*|```$/g, "");
  if (res.stop_reason !== "end_turn") console.warn("stop_reason", res.stop_reason);
  const j = JSON.parse(text);
  for (const k of ["tieu_de", "tinh_huong", "viec_can_lam", "quay_lai"]) if (typeof j[k] !== "string" || !j[k]) throw new Error(`chương ${n} thiếu ${k}`);
  fs.writeFileSync(out, JSON.stringify(j, null, 2) + "\n");
  console.log(`✓ ${n} ${bai.meta.title_en}\n  ${j.tieu_de}\n  ${j.tinh_huong}\n  → ${j.viec_can_lam}\n  ↺ ${j.quay_lai}`);
}
