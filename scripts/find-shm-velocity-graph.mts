// CHỈ ĐỌC — không ghi gì vào DB. Tìm mục "Lý thuyết" của bài Vận tốc, gia tốc
// trong dao động điều hoà (Lớp 11, Chương 1) và xuất các khối <svg>...</svg>
// trong body_html ra file, để soát khối đồ thị (v–t) bị lệch pha rồi sửa đúng
// khối đó (không đụng phần còn lại của bài).
//
//   npx tsx scripts/find-shm-velocity-graph.mts                # tự tìm theo Lớp 11 + từ khoá
//   npx tsx scripts/find-shm-velocity-graph.mts --lesson-id=45  # chỉ định thẳng lesson_id nếu tự tìm sai
//
// Cần .env.local có NEXT_PUBLIC_SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LOG_DIR = path.resolve(scriptDir, "logs");

function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

async function main() {
  const lessonIdArg = process.argv.find((a) => a.startsWith("--lesson-id="));
  const forcedLessonId = lessonIdArg ? Number(lessonIdArg.slice("--lesson-id=".length)) : null;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("thiếu NEXT_PUBLIC_SUPABASE_URL trong .env.local");
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY trong .env.local");

  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  let lessonId = forcedLessonId;

  if (!lessonId) {
    const { data: lessons, error } = await supabase
      .from("lessons")
      .select("id, title, chapter_id, chapters(title, chapter_classes(classes(name)))")
      .ilike("title", "%vận tốc%")
      .ilike("title", "%gia tốc%");
    if (error) fail(`tìm lesson: ${error.message}`);

    type Row = { id: number; title: string; chapter_id: number; chapters: { title: string; chapter_classes?: { classes?: { name?: string } }[] } | null };
    const rows = (lessons ?? []) as unknown as Row[];
    const inClass11 = rows.filter((r) =>
      (r.chapters?.chapter_classes ?? []).some((cc) => (cc.classes?.name ?? "").includes("11"))
    );

    const candidates = inClass11.length ? inClass11 : rows;
    if (candidates.length === 0) {
      fail("không tìm thấy bài nào có tiêu đề chứa 'vận tốc' và 'gia tốc'. Chạy lại với --lesson-id=<id> sau khi tự tra bảng lessons.");
    }
    if (candidates.length > 1) {
      console.log("Tìm thấy nhiều bài khớp, chỉ định lại bằng --lesson-id=<id>:");
      for (const r of candidates) {
        console.log(`  id=${r.id}  "${r.title}"  chương="${r.chapters?.title}"`);
      }
      process.exit(1);
    }
    lessonId = candidates[0].id;
    console.log(`Đã chọn bài id=${lessonId}: "${candidates[0].title}" (chương "${candidates[0].chapters?.title}")`);
  }

  const { data: items, error: itemsErr } = await supabase
    .from("lesson_items")
    .select("id, kind, title, body_html")
    .eq("lesson_id", lessonId)
    .eq("kind", "ly_thuyet");
  if (itemsErr) fail(`tìm lesson_items: ${itemsErr.message}`);
  if (!items || items.length === 0) fail(`lesson_id=${lessonId} không có mục kind=ly_thuyet`);

  fs.mkdirSync(LOG_DIR, { recursive: true });

  for (const item of items as { id: number; kind: string; title: string; body_html: string }[]) {
    const html = item.body_html ?? "";
    const outFile = path.join(LOG_DIR, `lesson-item-${item.id}-body.html`);
    fs.writeFileSync(outFile, html, "utf8");
    console.log(`\n=== lesson_items#${item.id} "${item.title}" — đã ghi toàn bộ body_html vào ${outFile} ===`);

    const svgBlocks = html.match(/<svg[\s\S]*?<\/svg>/g) ?? [];
    console.log(`  Tìm thấy ${svgBlocks.length} khối <svg>.`);

    svgBlocks.forEach((block, i) => {
      const looksLikeVelocity = block.includes("Aω") && !block.includes("Aω²") && block.includes("T/4");
      const marker = looksLikeVelocity ? "  ← NGHI LÀ ĐỒ THỊ v–t (có 'Aω', có 'T/4', không có 'Aω²')" : "";
      const svgFile = path.join(LOG_DIR, `lesson-item-${item.id}-svg-${i}.svg`);
      fs.writeFileSync(svgFile, block, "utf8");
      console.log(`  [${i}] ${block.length} ký tự → ${svgFile}${marker}`);
    });
  }

  console.log(`\nDán nội dung file *-svg-<i>.svg nghi vấn (đánh dấu ←) vào chat cho Claude để soạn bản sửa đúng.`);
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
