// Chèn mục "Lý thuyết trọng tâm" (kind=ly_thuyet) cho 4 bài Chương 2 lớp 12 (Khí lí tưởng)
// — Bài 5,6,7,8 vốn chỉ có mục Luyện tập, chưa từng có lý thuyết. Chỉ INSERT dòng mới,
// không đụng tới các mục luyen_tap/exam đã có sẵn.
//
//   npx tsx scripts/insert-ly-thuyet-l12-khi-li-tuong.mts
//
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy cục bộ.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import { applyMediaUrls, uploadLessonMedia, type RasterImageInput } from "@/services/lesson-media";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const SRC = "/private/tmp/claude-501/-Users-MAC-Projects-thachlab/02a46dbc-01b5-45ab-86be-3a85a492195c/scratchpad/l12-chuyen-de-2-khi-li-tuong";

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
  lessonId: number;
  title: string;
  htmlFile: string;
  slug: string; // như trong src="/lessons/<slug>/media/xxx"
  images: string[]; // tên file trong media/
}

const JOBS: Job[] = [
  { lessonId: 6, title: "Bài 5. Thuyết động học phân tử chất khí", htmlFile: "bai5.html", slug: "l12-cd2-bai5", images: ["fig01.png", "fig02.png", "fig03.png"] },
  {
    lessonId: 7,
    title: "Bài 6. Định luật Boyle. Định luật Charles",
    htmlFile: "bai6.html",
    slug: "l12-cd2-bai6",
    images: ["fig04.png", "fig05.gif", "fig06.gif", "d12.png", "fig07.png", "fig08.png", "fig09.gif", "fig10.png", "fig11.png", "fig12.png"],
  },
  { lessonId: 8, title: "Bài 7. Phương trình trạng thái của khí lí tưởng", htmlFile: "bai7.html", slug: "l12-cd2-bai7", images: ["fig13.png", "fig14.png", "fig16.png"] },
  { lessonId: 9, title: "Bài 8. Áp suất - động năng của phân tử khí", htmlFile: "bai8.html", slug: "l12-cd2-bai8", images: ["fig15.png"] },
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

function stripLeadingStrayP(html: string): string {
  return html.replace(/^<p class="text-base leading-relaxed my-2">\n(?=<h3)/, "");
}

async function main() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
  if (!key) fail("thiếu SUPABASE_SERVICE_ROLE_KEY");

  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

  for (const job of JOBS) {
    console.log(`\n=== Lesson #${job.lessonId} — ${job.title} ===`);

    const { data: existing, error: checkErr } = await supabase
      .from("lesson_items")
      .select("id, kind")
      .eq("lesson_id", job.lessonId)
      .eq("kind", "ly_thuyet");
    if (checkErr) fail(`kiểm tra mục có sẵn (lesson ${job.lessonId}): ${checkErr.message}`);
    if (existing && existing.length > 0) {
      console.log(`  đã có mục ly_thuyet (id ${existing.map((e) => e.id).join(",")}) — bỏ qua, không ghi đè.`);
      continue;
    }

    let html = fs.readFileSync(path.join(SRC, "final-html", job.htmlFile), "utf8");
    html = stripLeadingStrayP(html);

    const rasters: RasterImageInput[] = job.images.map((name) => ({
      name,
      dataUri: fileToDataUri(path.join(SRC, "media", name)),
      placeholder: `/lessons/${job.slug}/media/${name}`,
    }));

    console.log(`  Tải ${rasters.length} ảnh…`);
    const media = await uploadLessonMedia(supabase, job.lessonId, rasters);
    html = applyMediaUrls(html, media);
    console.log(`  ✓ ${media.length} ảnh`);

    const { error } = await supabase.from("lesson_items").insert({
      lesson_id: job.lessonId,
      kind: "ly_thuyet",
      title: "Lý thuyết trọng tâm",
      subtitle: "",
      body_html: html,
      video_url: "",
      pdf_url: "",
      questions: [],
      exam_ids: [],
      sort_order: 1,
    });
    if (error) fail(`insert lesson_items (lesson ${job.lessonId}): ${error.message}`);
    console.log(`  ✓ đã thêm mục "Lý thuyết trọng tâm"`);
  }

  console.log(`\nXong. Kiểm tra: /lop-hoc/bai/?id=6 , 7 , 8 , 9`);
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
