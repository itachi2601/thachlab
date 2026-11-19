// Dựng dữ liệu mục "Luyện từ" (luyện tập kiểu lượt ngắn) cho các chương Anh văn chuyên ngành Cơ khí.
// Nguồn: content/lesson-samples/avcn-chapter-*/data/bai.json (tu_vung) + public/assets/avcn/chapter-N/audio.json (mp3).
// Ra: public/assets/avcn/chapter-N/luyen-tu.json — file tĩnh, trang bài học tải khi mở mục Luyện tập (không đụng DB).
// Chạy lại sau khi sửa từ vựng của chương:  node scripts/avcn-luyen-tu.mjs
import { readFileSync, readdirSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const SAMPLES = join(ROOT, "content/lesson-samples");
const strip = (s) => String(s ?? "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();

let total = 0;
for (const dir of readdirSync(SAMPLES).filter((d) => /^avcn-chapter-\d+-/.test(d)).sort()) {
  const bai = JSON.parse(readFileSync(join(SAMPLES, dir, "data/bai.json"), "utf8"));
  const ch = Number(bai.meta?.chapter);
  if (!ch || !Array.isArray(bai.tu_vung)) continue;
  const assets = join(ROOT, "public/assets/avcn", `chapter-${ch}`);
  const audioMap = existsSync(join(assets, "audio.json")) ? JSON.parse(readFileSync(join(assets, "audio.json"), "utf8")) : {};
  const words = [];
  for (const cum of bai.tu_vung) {
    for (const t of cum.tu ?? []) {
      const term = strip(t.term);
      const vi = strip(t.vi);
      if (!term || !vi) continue;
      const file = audioMap[t.term] ?? audioMap[term];
      words.push({
        term,
        vi,
        ipa: strip(t.ipa) || undefined,
        audio: file ? `/assets/avcn/chapter-${ch}/audio/${file}` : undefined,
      });
    }
  }
  // Từ bổ sung: chỉ làm phương án nhiễu (không có phát âm/IPA để hỏi chính).
  const them = (bai.tu_vung_them ?? []).map((t) => ({ term: strip(t.term), vi: strip(t.vi) })).filter((t) => t.term && t.vi);
  const out = { chapter: ch, title: strip(bai.meta?.title_en), words, them };
  writeFileSync(join(assets, "luyen-tu.json"), JSON.stringify(out) + "\n");
  total += words.length;
  console.log(`chapter-${ch}: ${words.length} từ (${words.filter((w) => w.audio).length} có mp3), ${them.length} từ nhiễu`);
}
console.log(`Xong: ${total} từ.`);
