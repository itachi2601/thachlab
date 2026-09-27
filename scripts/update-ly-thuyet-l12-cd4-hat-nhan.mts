// Cập nhật (UPDATE, không insert) mục "Lý thuyết trọng tâm" (kind=ly_thuyet) cho 5 bài
// Chương 4: Vật lí hạt nhân — Lớp 12 (Bài 14-18), theo file GV mới
// "lý thuyết Chuyên đề 4 Vật lý Hạt nhân file GV.docx".
//
//   npx tsx scripts/update-ly-thuyet-l12-cd4-hat-nhan.mts
//
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy cục bộ.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { applyMediaUrls, uploadLessonMedia, type RasterImageInput } from "@/services/lesson-media";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const SRC = "/private/tmp/claude-501/-Users-MAC-Projects-thachlab/5fd28a5e-fc5a-4962-a7d3-32de57ee237e/scratchpad/l12-cd4-hat-nhan";

function readEnvLocal(key: string): string | undefined {
  const envPath = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(envPath)) return undefined;
  const line = fs.readFileSync(envPath, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

function askHidden(query: string): Promise<string> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const rlAny = rl as unknown as { _writeToOutput: (chunk: string) => void; stdoutMuted: boolean };
    rlAny._writeToOutput = (chunk) => (rl as unknown as { output: NodeJS.WritableStream }).output.write(rlAny.stdoutMuted ? "*" : chunk);
    rlAny.stdoutMuted = false;
    rl.question(query, (answer) => {
      rl.close();
      process.stdout.write("\n");
      resolve(answer.trim());
    });
    rlAny.stdoutMuted = true;
  });
}

const MIME_BY_EXT: Record<string, string> = {
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  gif: "image/gif",
};

interface Job {
  itemId: number; // lesson_items.id có sẵn (kind=ly_thuyet)
  lessonId: number;
  title: string;
  dir: string; // thư mục con trong SRC
  slug: string;
  images: string[]; // tên file trong media/
}

const JOBS: Job[] = [
  { itemId: 138, lessonId: 15, title: "Bài 14. Hạt nhân và mô hình nguyên tử", dir: "bai14", slug: "12-hat-nhan-mo-hinh-nguyen-tu", images: ["fig05.png"] },
  { itemId: 147, lessonId: 16, title: "Bài 15. Năng lượng liên kết hạt nhân", dir: "bai15", slug: "12-nang-luong-lien-ket-hat-nhan", images: [] },
  { itemId: 181, lessonId: 17, title: "Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng", dir: "bai16", slug: "12-phan-hach-nhiet-hach", images: ["fig22.png", "fig23.png", "fig27.png", "fig30.png"] },
  { itemId: 160, lessonId: 18, title: "Bài 17. Hiện tượng phóng xạ", dir: "bai17", slug: "12-hien-tuong-phong-xa", images: [] },
  { itemId: 150, lessonId: 19, title: "Bài 18. An toàn phóng xạ", dir: "bai18", slug: "12-an-toan-phong-xa", images: ["fig26.png", "fig31.jpeg", "fig34.png", "fig37.png"] },
];

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

function fileToDataUri(filePath: string): string {
  const ext = filePath.split(".").pop()?.toLowerCase() ?? "";
  const mime = MIME_BY_EXT[ext] ?? "application/octet-stream";
  const b64 = fs.readFileSync(filePath).toString("base64");
  return `data:${mime};base64,${b64}`;
}

async function main() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");

  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  for (const job of JOBS) {
    console.log(`\n=== ${job.title} (lesson_items#${job.itemId}) ===`);

    const { data: existing, error: checkErr } = await supabase
      .from("lesson_items")
      .select("id, kind, lesson_id")
      .eq("id", job.itemId)
      .single();
    if (checkErr) fail(`kiểm tra mục #${job.itemId}: ${checkErr.message}`);
    if (!existing || existing.kind !== "ly_thuyet" || existing.lesson_id !== job.lessonId) {
      fail(`mục #${job.itemId} không khớp (kind=${existing?.kind}, lesson_id=${existing?.lesson_id}) — dừng để tránh ghi nhầm.`);
    }

    let html = fs.readFileSync(path.join(SRC, job.dir, "parts", "01_ly_thuyet.html"), "utf8");

    if (job.images.length) {
      const rasters: RasterImageInput[] = job.images.map((name) => ({
        name,
        dataUri: fileToDataUri(path.join(SRC, "media", name)),
        placeholder: `/lessons/${job.slug}/media/${name}`,
      }));
      console.log(`  Tải ${rasters.length} ảnh…`);
      const media = await uploadLessonMedia(supabase, job.lessonId, rasters);
      html = applyMediaUrls(html, media);
      console.log(`  ✓ ${media.length} ảnh`);
    }

    const { error } = await supabase
      .from("lesson_items")
      .update({ body_html: html })
      .eq("id", job.itemId);
    if (error) fail(`update lesson_items #${job.itemId}: ${error.message}`);
    console.log(`  ✓ đã cập nhật "Lý thuyết trọng tâm"`);
  }

  console.log(`\nXong. Kiểm tra: /lop-hoc/bai/?id=15 , 16 , 17 , 18 , 19`);
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
