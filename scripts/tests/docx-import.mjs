/**
 * Kiểm thử bộ đọc đề Word (services/docx-*.ts) trong Chromium thật — vì nó dùng
 * DOMParser và DecompressionStream của trình duyệt, chạy thẳng trên Node không được.
 *
 *   npm i --no-save playwright && node scripts/tests/docx-import.mjs
 */

import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { extname, join, resolve } from "node:path";
import { writeFileSync } from "node:fs";
import { sampleDocx } from "./docx-fixture.mjs";

const ROOT = resolve(import.meta.dirname, "../..");
const BUILD = "/tmp/docx-import-build";

function compile() {
  const config = {
    extends: join(ROOT, "tsconfig.json"),
    compilerOptions: {
      noEmit: false,
      outDir: BUILD,
      rootDir: ROOT,
      module: "esnext",
      target: "es2022",
      declaration: false,
      // tsconfig tạm nằm ngoài dự án nên phải chỉ rõ chỗ lấy kiểu của Node/DOM.
      typeRoots: [join(ROOT, "node_modules/@types")],
    },
    include: [join(ROOT, "services/docx-reader.ts"), join(ROOT, "services/docx-exam-parser.ts")],
  };
  const path = "/tmp/tsconfig.docx-test.json";
  writeFileSync(path, JSON.stringify(config));
  execFileSync("npx", ["tsc", "-p", path], { cwd: ROOT, stdio: "inherit" });
}

const PAGE = `<!doctype html><meta charset="utf-8">
<script type="importmap">{"imports":{"@/":"/"}}</script>
<script type="module">
  import { readDocx } from "@/services/docx-reader";
  import { docxTextToBundle } from "@/services/docx-exam-parser";
  window.run = async (base64) => {
    const bin = atob(base64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const read = await readDocx(bytes.buffer);
    const draft = docxTextToBundle(read.text, { subjectCode: "vat-ly", images: read.images });
    return { read: { ...read, images: read.images.map((i) => i.placeholder) }, draft };
  };
</script>`;

const MIME = { ".js": "text/javascript", ".html": "text/html" };

function serve() {
  const server = createServer(async (req, res) => {
    try {
      if (req.url === "/" || req.url === "/index.html") {
        res.writeHead(200, { "content-type": "text/html" }).end(PAGE);
        return;
      }
      const clean = req.url.split("?")[0];
      const file = join(BUILD, extname(clean) ? clean : `${clean}.js`);
      const body = await readFile(file);
      res.writeHead(200, { "content-type": MIME[extname(file)] ?? "application/octet-stream" }).end(body);
    } catch {
      res.writeHead(404).end("not found");
    }
  });
  return new Promise((ok) => server.listen(0, () => ok({ server, port: server.address().port })));
}

let failures = 0;
function check(label, actual, expected) {
  const pass = typeof expected === "function" ? expected(actual) : JSON.stringify(actual) === JSON.stringify(expected);
  if (!pass) {
    failures += 1;
    console.error(`✕ ${label}\n    nhận: ${JSON.stringify(actual)}`);
  } else {
    console.log(`✓ ${label}`);
  }
}

const playwright = await import(process.env.PLAYWRIGHT_MODULE || "playwright")
  .catch(() => import("playwright-core"))
  .catch(() => {
    console.error("Cần playwright: npm i --no-save playwright (hoặc playwright-core + Chromium sẵn có).");
    process.exit(1);
  });
const chromium = playwright.chromium ?? playwright.default?.chromium;

compile();
const { server, port } = await serve();
const browser = await chromium.launch(
  process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {},
);
try {
  const page = await browser.newPage();
  page.on("pageerror", (e) => {
    console.error("Lỗi trang:", e.message);
    failures += 1;
  });
  await page.goto(`http://localhost:${port}/`);
  await page.waitForFunction(() => typeof window.run === "function");

  const base64 = Buffer.from(sampleDocx()).toString("base64");
  const { read, draft } = await page.evaluate((b64) => window.run(b64), base64);
  const qs = draft.bundle.exam.questions;

  check("đọc đủ 5 câu", qs.length, 5);
  check("đếm đúng mốc Câu n.", draft.markerCount, 5);
  check("1 công thức MathType chưa chuyển", read.mathTypeCount, 1);
  check("2 công thức Office Math đọc được", read.ommlCount, 2);
  check("gom được 1 ảnh PNG", read.images, ["media/hinh-1.png"]);

  check("câu 1 là trắc nghiệm", qs[0].type, "multiple_choice");
  check("câu 1 lấy đúng đáp án dấu * (B)", qs[0].answer, 1);
  check("câu 1 có phân số LaTeX", qs[0].question, (v) => v.includes("\\frac{s}{t}"));
  check("câu 1 giữ lời giải", qs[0].explanation, (v) => v.includes("quãng đường chia thời gian"));
  check("câu 1 đủ 4 phương án", qs[0].options, ["1 m/s", "2 m/s", "3 m/s", "4 m/s"]);

  check("câu 2 lấy phương án từ bảng", qs[1].options, ["5", "6", "7", "8"]);
  check("câu 2 đáp án C", qs[1].answer, 2);
  check("câu 2 có căn thức", qs[1].question, (v) => v.includes("\\sqrt{2gh}"));
  check("câu 2 có chỉ số dưới", qs[1].question, (v) => v.includes("a_0") || v.includes("a_{0}"));
  check("câu 2 chuyển α sang \\alpha", qs[1].question, (v) => v.includes("\\alpha"));
  check("câu 2 chèn ảnh đã gom", qs[1].question, (v) => v.includes('src="media/hinh-1.png"'));

  check("câu 3 đánh dấu công thức MathType", qs[2].question, (v) => v.includes("⟦CT⟧"));
  check("câu 3 đọc dòng Đáp án: D", qs[2].answer, 3);

  check("câu 4 là đúng/sai", qs[3].type, "true_false");
  check("câu 4 lấy đúng các ý Đ/S", qs[3].statements?.map((s) => s.answer), [true, false, true, false]);

  check("câu 5 là trả lời ngắn", qs[4].type, "short_answer");
  check("câu 5 đáp án 2", qs[4].answer, "2");

  check("đoán đúng thời gian làm bài", draft.bundle.exam.duration_minutes, 45);
  check("lấy tên đề từ file", draft.bundle.exam.title, (v) => v.includes("ĐỀ KIỂM TRA"));
  check("gói không có lý thuyết", draft.bundle.theory_html, "");
} finally {
  await browser.close();
  server.close();
}

console.log(failures === 0 ? "\nTất cả kiểm thử đạt." : `\n${failures} kiểm thử hỏng.`);
process.exit(failures === 0 ? 0 : 1);
