// Bộ lọc RẺ (không gọi AI) cho MỘT thư mục chứa nhiều file .docx đề Azota — bước đầu tiên
// của quy trình "đăng đề hàng loạt" (xem skill dang-de-hang-loat). Đọc thô từng file bằng
// docx-reader.ts (KHÔNG chạy qua docx-exam-parser.ts vì parser đó chỉ hiểu 1-2 kiểu trình
// bày đáp án — nhiều đề cũ dùng kiểu khác vẫn có đáp án đầy đủ, xem
// scripts/_tmp_check_missing_answers2.mts / project_thachlab_de_thi_thu_truong_so.md).
//
// Phân loại mỗi file vào 1 trong 3 nhóm, để KHÔNG giao việc tốn kém (agent) cho file
// không cần:
//   - "already_uploaded"  : tên file đã có trong log JSON đã cho (--log=)   → bỏ qua
//   - "missing_answers"   : 0 dấu hiệu đáp án nào                          → loại khỏi thư mục
//   - "needs_review"      : còn lại — TẤT CẢ đều cần người/agent gắn nhãn "Chủ đề:"/"Dạng:"
//                           (chưa có auto-labeler), kèm theo các cờ chi tiết để prompt agent
//                           đi thẳng đúng pipeline, không phải tự dò từ đầu (xem
//                           feedback_batch_agent_upload_efficiency.md):
//       hasRealImages      → cần đường "gói JSON qua /quan-tri/nhap-bai" (giữ được ảnh),
//                             KHÔNG dùng đường dán văn bản trực tiếp.
//       hasMathTypeOle     → cần skill "azota" (convert_mtef/mathtype-sang-omml) trước.
//       hasVectorOrShape   → có ảnh WMF/EMF hoặc hình vẽ Word — cần LibreOffice giải mã
//                             hoặc vẽ lại SVG tay, không tự có ảnh raster.
//       answerFormat       → "star" (đã có dấu * sẵn) | "dap_an_line" (có dòng "Đáp án:")
//                             | "answer_table" (bảng "Chọn" + lời giải cuối bài — kiểu cũ,
//                               PHẢI đọc lời giải để đối chiếu, không tự parse máy móc)
//                             | "unclear" (không khớp kiểu nào đã biết — ưu tiên xem tay)
//
// Dùng:
//   npx tsx scripts/classify-exam-folder.mts "<thư mục>" [--log=<log.json>] [--out=<report.json>] [--apply-missing]
//
// --apply-missing: sau khi phân loại, CHUYỂN (không xoá) toàn bộ file "missing_answers"
// vào thư mục con "_thieu_dap_an" bên trong <thư mục> — đúng bước "loại đề thiếu đáp án
// ra khỏi thư mục" của skill dang-de-hang-loat. Không có cờ này thì chỉ báo cáo, không
// đụng file nào.

import { DOMParser as XmlDomParser } from "@xmldom/xmldom";
import fs from "node:fs";
import path from "node:path";

class NodeDOMParser {
  parseFromString(str: string, type: string) {
    let fatal: string | null = null;
    const doc = new XmlDomParser({
      onError: (level: string, msg: string) => {
        if ((level === "error" || level === "fatalError") && !fatal) fatal = msg;
      },
    } as ConstructorParameters<typeof XmlDomParser>[0]).parseFromString(str, type as never);
    if (fatal) throw new Error(String(fatal));
    (doc as unknown as { querySelector: (s: string) => null }).querySelector = () => null;
    return doc;
  }
}
(globalThis as unknown as { DOMParser: typeof NodeDOMParser }).DOMParser = NodeDOMParser;

import { readDocx } from "@/services/docx-reader";
import { countQuestionMarkers } from "@/services/docx-exam-parser";

type AnswerFormat = "star" | "dap_an_line" | "answer_table" | "unclear";

interface FileReport {
  file: string;
  bucket: "already_uploaded" | "missing_answers" | "needs_review" | "read_error";
  markerCount: number;
  answerFormat?: AnswerFormat;
  hasTopicFormLabels: boolean;
  hasRealImages: boolean;
  imageCount: number;
  hasMathTypeOle: boolean;
  mathTypeCount: number;
  hasVectorOrShape: boolean;
  readerWarnings: string[];
  error?: string;
}

function countAnswerSignals(text: string) {
  const star = (text.match(/(^|[\s(])\*\s*[A-Da-d][.)]/gm) || []).length;
  const danAnLine = (text.match(/Đ[áa]p\s*[áa]n\s*:/gi) || []).length;
  const chonDapAn = (text.match(/Ch[ọo]n\s*đ[áa]p\s*[áa]n/gi) || []).length;
  const dapSo = (text.match(/Đ[áa]p\s*s[ốo]/gi) || []).length;
  const tableRow = (text.match(/\n\s*Ch[ọo]n[\s\t]+[A-DĐa-dđ0-9]/g) || []).length;
  const hasHeading = /Đ[ÁA]P\s*[ÁA]N\b/i.test(text);
  return { star, danAnLine, chonDapAn, dapSo, tableRow, hasHeading };
}

function classifyAnswerFormat(sig: ReturnType<typeof countAnswerSignals>): AnswerFormat | undefined {
  const total = sig.star + sig.danAnLine + sig.chonDapAn + sig.dapSo + sig.tableRow;
  if (total === 0 && !sig.hasHeading) return undefined; // missing_answers xử lý riêng
  if (sig.star > 0) return "star";
  if (sig.danAnLine > 0) return "dap_an_line";
  if (sig.chonDapAn > 0 || sig.dapSo > 0 || sig.tableRow > 0 || sig.hasHeading) return "answer_table";
  return "unclear";
}

async function main() {
  const args = process.argv.slice(2).filter((a) => !a.startsWith("--"));
  const dir = args[0];
  if (!dir) {
    console.error("Dùng: npx tsx scripts/classify-exam-folder.mts <thư mục> [--log=<log.json>] [--out=<report.json>]");
    process.exit(1);
  }
  const DOCX_DIR = path.resolve(dir);
  if (!fs.existsSync(DOCX_DIR)) {
    console.error(`Không thấy thư mục: ${DOCX_DIR}`);
    process.exit(1);
  }
  const logArg = process.argv.find((a) => a.startsWith("--log="));
  const outArg = process.argv.find((a) => a.startsWith("--out="));
  const LOG_PATH = logArg ? path.resolve(logArg.slice("--log=".length)) : null;
  const OUT_PATH = outArg
    ? path.resolve(outArg.slice("--out=".length))
    : path.join(DOCX_DIR, "_classify-report.json");

  const uploaded = new Set<string>(
    LOG_PATH && fs.existsSync(LOG_PATH) ? Object.keys(JSON.parse(fs.readFileSync(LOG_PATH, "utf8"))) : [],
  );

  const files = fs
    .readdirSync(DOCX_DIR, { withFileTypes: true })
    .filter((e) => e.isFile() && /\.docx$/i.test(e.name) && !e.name.startsWith("~$") && !e.name.startsWith("_"))
    .map((e) => e.name)
    .sort();

  console.log(`Tìm thấy ${files.length} file .docx trong ${DOCX_DIR}${LOG_PATH ? ` (log: ${uploaded.size} đã đăng)` : ""}\n`);

  const reports: FileReport[] = [];
  const counts: Record<FileReport["bucket"], number> = {
    already_uploaded: 0,
    missing_answers: 0,
    needs_review: 0,
    read_error: 0,
  };
  const formatCounts: Record<AnswerFormat, number> = { star: 0, dap_an_line: 0, answer_table: 0, unclear: 0 };

  for (const file of files) {
    if (uploaded.has(file)) {
      reports.push({
        file,
        bucket: "already_uploaded",
        markerCount: 0,
        hasTopicFormLabels: false,
        hasRealImages: false,
        imageCount: 0,
        hasMathTypeOle: false,
        mathTypeCount: 0,
        hasVectorOrShape: false,
        readerWarnings: [],
      });
      counts.already_uploaded += 1;
      continue;
    }
    try {
      const bytes = new Uint8Array(fs.readFileSync(path.join(DOCX_DIR, file)));
      const read = await readDocx(bytes.buffer);
      const markerCount = countQuestionMarkers(read.text);
      const sig = countAnswerSignals(read.text);
      const answerFormat = classifyAnswerFormat(sig);
      const hasTopicFormLabels = /Ch[ủu]\s*đ[ềe]\s*:/i.test(read.text) && /D[ạa]ng\s*:/i.test(read.text);
      const hasVectorOrShape = read.warnings.some((w) => /WMF|EMF|hình vẽ Word|⟦/.test(w));

      const bucket: FileReport["bucket"] = answerFormat === undefined ? "missing_answers" : "needs_review";
      reports.push({
        file,
        bucket,
        markerCount,
        answerFormat,
        hasTopicFormLabels,
        hasRealImages: read.images.length > 0,
        imageCount: read.images.length,
        hasMathTypeOle: read.mathTypeCount > 0,
        mathTypeCount: read.mathTypeCount,
        hasVectorOrShape,
        readerWarnings: read.warnings,
      });
      counts[bucket] += 1;
      if (answerFormat) formatCounts[answerFormat] += 1;
    } catch (e) {
      reports.push({
        file,
        bucket: "read_error",
        markerCount: 0,
        hasTopicFormLabels: false,
        hasRealImages: false,
        imageCount: 0,
        hasMathTypeOle: false,
        mathTypeCount: 0,
        hasVectorOrShape: false,
        readerWarnings: [],
        error: e instanceof Error ? e.message : String(e),
      });
      counts.read_error += 1;
    }
  }

  fs.writeFileSync(OUT_PATH, JSON.stringify(reports, null, 2) + "\n", "utf8");

  console.log("=== Tổng kết ===");
  console.log(`  Đã đăng trước đó       : ${counts.already_uploaded}`);
  console.log(`  Thiếu đáp án (loại ra) : ${counts.missing_answers}`);
  console.log(`  Cần rà soát/agent      : ${counts.needs_review}`);
  console.log(`    trong đó kiểu đáp án — star: ${formatCounts.star}, dap_an_line: ${formatCounts.dap_an_line}, answer_table: ${formatCounts.answer_table}, unclear: ${formatCounts.unclear}`);
  const withImages = reports.filter((r) => r.bucket === "needs_review" && r.hasRealImages).length;
  const withOle = reports.filter((r) => r.bucket === "needs_review" && r.hasMathTypeOle).length;
  const withVector = reports.filter((r) => r.bucket === "needs_review" && r.hasVectorOrShape).length;
  const withLabels = reports.filter((r) => r.bucket === "needs_review" && r.hasTopicFormLabels).length;
  console.log(`    có ảnh nhúng thật: ${withImages} | có OLE MathType: ${withOle} | có ảnh WMF/EMF/hình vẽ Word: ${withVector} | đã có nhãn Chủ đề/Dạng: ${withLabels}`);
  console.log(`  Lỗi đọc file           : ${counts.read_error}`);
  console.log(`  Tổng file xét          : ${files.length}`);
  console.log(`\nBáo cáo chi tiết: ${OUT_PATH}`);

  if (process.argv.includes("--apply-missing")) {
    const missing = reports.filter((r) => r.bucket === "missing_answers");
    if (missing.length === 0) {
      console.log("\n[--apply-missing] Không có file nào thiếu đáp án — không cần chuyển gì.");
      return;
    }
    const OUT_DIR = path.join(DOCX_DIR, "_thieu_dap_an");
    fs.mkdirSync(OUT_DIR, { recursive: true });
    for (const r of missing) fs.renameSync(path.join(DOCX_DIR, r.file), path.join(OUT_DIR, r.file));
    console.log(`\n✓ [--apply-missing] Đã chuyển ${missing.length} file thiếu đáp án vào: ${OUT_DIR}`);
  }
}

main().catch((err) => {
  console.error("Lỗi:", err instanceof Error ? (err.stack ?? err.message) : String(err));
  process.exit(1);
});
