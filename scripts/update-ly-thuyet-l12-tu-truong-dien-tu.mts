// Cập nhật (UPDATE, không insert) mục "Lý thuyết" (kind=ly_thuyet) cho 6 bài
// Chương 3: Từ trường (Bài 10, 12, 13, 14, 15, 16) — Lớp 12, theo các file GV mới
// ("Chủ đề 2..13 ... - GV.docx"), pipeline LaTeX ở output/bai10-luc-tu, output/bai12-*,
// output/bai13-*, output/bai14-*, output/bai15-*, output/bai16-dien-tu-truong.
//
// Một số bài học LMS (13, 14, 125, 126) gộp nhiều "Chủ đề" GV riêng lẻ vào cùng một
// lesson_items — script nối các phần theo đúng thứ tự Chủ đề, thêm tiêu đề phụ <h2>
// để giữ cấu trúc như nội dung cũ (đối chiếu bằng SQL trước khi ghi đè).
//
//   npx tsx scripts/update-ly-thuyet-l12-tu-truong-dien-tu.mts [--dry-run] [--only=52,66]
//
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy cục bộ.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { applyMediaUrls, uploadLessonMedia, type RasterImageInput } from "@/services/lesson-media";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const OUT_ROOT = path.resolve(scriptDir, "..", "output");

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

interface SourcePart {
  dir: string; // thư mục con trong output/
  heading?: string; // tiêu đề phụ <h2> chèn trước nội dung phần này (khi gộp nhiều Chủ đề)
}

interface Job {
  itemId: number; // lesson_items.id có sẵn (kind=ly_thuyet)
  lessonId: number;
  title: string;
  parts: SourcePart[];
}

const JOBS: Job[] = [
  { itemId: 52, lessonId: 11, title: "Bài 10. Lực từ. Cảm ứng từ", parts: [{ dir: "bai10-luc-tu" }] },
  {
    itemId: 66,
    lessonId: 13,
    title: "Bài 12. Hiện tượng cảm ứng điện từ",
    parts: [
      { dir: "bai12-tu-thong", heading: "1. Từ thông" },
      { dir: "bai12-cam-ung-dien-tu", heading: "2. Hiện tượng cảm ứng điện từ" },
      { dir: "bai12-suat-dien-dong", heading: "3. Suất điện động cảm ứng - định luật Faraday" },
    ],
  },
  {
    itemId: 141,
    lessonId: 14,
    title: "Bài 13. Đại cương về dòng điện xoay chiều",
    parts: [
      { dir: "bai13-nguyen-tac-dxc", heading: "1. Nguyên tắc tạo ra dòng điện xoay chiều" },
      { dir: "bai13-dien-ap-xoay-chieu", heading: "2. Dòng điện và điện áp xoay chiều" },
    ],
  },
  {
    itemId: 143,
    lessonId: 125,
    title: "Bài 14. Máy phát điện xoay chiều. Máy biến áp",
    parts: [
      { dir: "bai14-may-phat-dien", heading: "1. Máy phát điện xoay chiều" },
      { dir: "bai14-ung-dung-an-toan", heading: "2. Ứng dụng và sử dụng an toàn dòng điện xoay chiều" },
      { dir: "bai14-may-bien-ap", heading: "3. Máy biến áp" },
    ],
  },
  {
    itemId: 145,
    lessonId: 126,
    title: "Bài 15. Một số ứng dụng của cảm ứng điện từ",
    parts: [
      { dir: "bai15-dan-ghi-ta-dien", heading: "1. Đàn ghi ta điện và sạc không dây" },
      { dir: "bai15-dong-dien-foucault", heading: "2. Dòng điện Foucault" },
    ],
  },
  { itemId: 183, lessonId: 127, title: "Bài 16. Điện từ trường. Mô hình sóng điện từ", parts: [{ dir: "bai16-dien-tu-truong" }] },
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

interface PartManifestImage {
  file: string;
  web: string;
  alt_goi_y?: string;
}
interface PartManifest {
  slug_goi_y: string;
  parts: {
    ly_thuyet?: {
      file: string;
      images?: PartManifestImage[];
    };
  };
}

async function main() {
  const dryRun = process.argv.includes("--dry-run");
  const onlyArg = process.argv.find((a) => a.startsWith("--only="));
  const only = onlyArg ? new Set(onlyArg.slice("--only=".length).split(",").map((s) => Number(s.trim()))) : null;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ?? (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");

  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  for (const job of JOBS) {
    if (only && !only.has(job.itemId)) continue;
    console.log(`\n=== ${job.title} (lesson_items#${job.itemId}) ===`);

    const { data: existing, error: checkErr } = await supabase
      .from("lesson_items")
      .select("id, kind, lesson_id, title")
      .eq("id", job.itemId)
      .single();
    if (checkErr) fail(`kiểm tra mục #${job.itemId}: ${checkErr.message}`);
    if (!existing || existing.kind !== "ly_thuyet" || existing.lesson_id !== job.lessonId) {
      fail(`mục #${job.itemId} không khớp (kind=${existing?.kind}, lesson_id=${existing?.lesson_id}) — dừng để tránh ghi nhầm.`);
    }

    const htmlPieces: string[] = [];

    for (const part of job.parts) {
      const dir = path.join(OUT_ROOT, part.dir);
      const reportPath = path.join(dir, "html_report.json");
      if (!fs.existsSync(reportPath)) fail(`${part.dir}: chưa có html_report.json — chạy prepare_html.cjs trước`);
      const report = JSON.parse(fs.readFileSync(reportPath, "utf8")) as { ready?: boolean };
      if (!report.ready) fail(`${part.dir}: html_report.json ready=false — không được đăng`);

      const manifest: PartManifest = JSON.parse(fs.readFileSync(path.join(dir, "parts", "parts.json"), "utf8"));
      const lt = manifest.parts.ly_thuyet;
      if (!lt) fail(`${part.dir}: manifest thiếu phần ly_thuyet`);
      const htmlFile = lt.file.replace(/\.tex$/, ".html");
      let html = fs.readFileSync(path.join(dir, htmlFile), "utf8");

      const images = lt.images ?? [];
      if (images.length) {
        const rasters: RasterImageInput[] = images.map((img) => ({
          name: img.file,
          dataUri: fileToDataUri(path.join(dir, "media", img.file)),
          placeholder: img.web,
        }));
        console.log(`  [${part.dir}] tải ${rasters.length} ảnh…`);
        if (!dryRun) {
          // Mạng trong sandbox thỉnh thoảng "fetch failed" thoáng qua — thử lại vài lần
          // trước khi bỏ cuộc, thay vì huỷ cả job giữa chừng.
          let media: Awaited<ReturnType<typeof uploadLessonMedia>> | undefined;
          let lastErr: unknown;
          for (let attempt = 1; attempt <= 4; attempt++) {
            try {
              media = await uploadLessonMedia(supabase, job.lessonId, rasters);
              break;
            } catch (e) {
              lastErr = e;
              const msg = e instanceof Error ? e.message : String(e);
              console.log(`  ⚠ [${part.dir}] lần ${attempt} lỗi: ${msg} — thử lại…`);
              await new Promise((r) => setTimeout(r, attempt * 3000));
            }
          }
          if (!media) fail(`${part.dir}: tải ảnh thất bại sau nhiều lần thử — ${lastErr instanceof Error ? lastErr.message : String(lastErr)}`);
          html = applyMediaUrls(html, media);
          console.log(`  ✓ [${part.dir}] ${media.length} ảnh`);
        }
      }

      if (part.heading) {
        htmlPieces.push(`<h2 class="text-xl font-bold mt-3 mb-1.5">${part.heading}</h2>\n${html}`);
      } else {
        htmlPieces.push(html);
      }
    }

    const combined = htmlPieces.join("\n");
    console.log(`  Tổng độ dài body_html mới: ${combined.length} ký tự (${job.parts.length} phần)`);

    if (dryRun) {
      console.log("  [dry-run] bỏ qua UPDATE Supabase");
      continue;
    }

    const { error } = await supabase.from("lesson_items").update({ body_html: combined }).eq("id", job.itemId);
    if (error) fail(`update lesson_items #${job.itemId}: ${error.message}`);
    console.log(`  ✓ đã cập nhật "${existing.title}" (lesson_id=${job.lessonId})`);
  }

  console.log(`\nXong. Kiểm tra: /lop-hoc/bai/?id=11 , 13 , 14 , 125 , 126 , 127`);
  console.log(`Nhớ chạy lại: node scripts/build-content.mjs   (hoặc npm run build) để nội dung tĩnh lên web.`);
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
