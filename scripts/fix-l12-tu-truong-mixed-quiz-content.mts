// Sửa lỗi: phần "Câu hỏi trắc nghiệm" (nhiều phương án / đúng sai / trả lời ngắn, có
// "Hướng dẫn giải") bị lồng thẳng vào body_html của mục Lý thuyết (kind=ly_thuyet), thay vì
// nằm ở mục "Các dạng bài tập" (kind=bai_tap_mau) — 6 bài Lớp 12 chương Từ trường + Điện từ
// (lesson_id 11, 13, 14, 125, 126, 127) đăng lại 26/9/2026 từ file GV mới (xem
// scripts/update-ly-thuyet-l12-tu-truong-dien-tu.mts). Nguyên nhân gốc: parts.json của các
// thư mục output/bai1*-*/ liệt kê thu_tu_dang: [ly_thuyet, bai_tap, bai_tap_ve_nha] nhưng chỉ
// có 1 part "ly_thuyet" — pipeline tách phần của skill latex không tách được "Bài tập" ra
// khỏi "Lý thuyết" trong file .tex nguồn, nên toàn bộ dồn vào 01_ly_thuyet.tex.
//
// Script này KHÔNG đụng vào .tex nguồn / pipeline latex — chỉ sửa dữ liệu đã có trên Supabase:
// tách các khối trắc nghiệm ra khỏi body_html (ly_thuyet), gộp mỗi "Câu N" thành 1 phần tử
// {label, body_html} thêm vào questions[] của mục bai_tap_mau cùng bài (tạo mới cho lesson_id
// 126 — bài này chưa có mục bai_tap_mau nào). Đồng thời dọn thuộc tính alt="..." của mọi <img>
// (đang chứa rác từ script trích ảnh gốc, xem parts.json/alt_goi_y) — không có nội dung alt
// đúng để thay vào nên đặt alt="" (ảnh đã có chú thích trong đoạn văn xung quanh).
//
// Tách khối theo mốc tiêu đề CHÍNH XÁC trong .tex nguồn (giữ lại y nguyên khi build_html):
//   "CÂU HỎI TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN" / "CÂU HỎI TRẮC NGHIỆM ĐÚNG SAI" /
//   "CÂU HỎI TRẮC NGHIỆM TRẢ LỜI NGẮN" — ranh giới việc "còn thuộc câu hỏi" hay "đã quay lại lý
//   thuyết" xác định bằng số thứ tự "Câu N" phải tăng đúng 1 đơn vị liên tục sau mỗi tiêu đề;
//   gặp số không khớp (hoặc hết block) thì coi là hết phần trắc nghiệm, quay lại lý thuyết.
//
// Mặc định CHỈ IN BÁO CÁO (dry-run) — không ghi gì vào Supabase. Xem kỹ số liệu (đặc biệt
// dòng "câu bắt được so với đếm thô") trước khi thêm --write.
//
//   npx tsx scripts/fix-l12-tu-truong-mixed-quiz-content.mts               # dry-run, in báo cáo
//   npx tsx scripts/fix-l12-tu-truong-mixed-quiz-content.mts --only=145    # dry-run 1 bài
//   npx tsx scripts/fix-l12-tu-truong-mixed-quiz-content.mts --write       # ghi thật + backup
//
// App export tĩnh, không có server ở production → cần service role key, CHỈ chạy cục bộ
// (đọc từ .env.local, không dán vào hội thoại).

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LOG_DIR = path.resolve(scriptDir, "logs");

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

function fail(msg: string): never {
  console.error("Lỗi:", msg);
  process.exit(1);
}

// ---------------------------------------------------------------------------------------
// Tách body_html thành các block cấp-1 (mỗi <p>/<div>/<ul>/<h2>/<h3>/<img> ở gốc là 1 block),
// bất kể lồng bao nhiêu tầng bên trong (table/tr/td/strong/...). Dựa vào đếm độ sâu thẻ mở/đóng
// thay vì regex tham lam, để không cắt nhầm giữa chừng 1 bảng hay 1 khối lồng.
// ---------------------------------------------------------------------------------------
const VOID_TAGS = new Set(["img", "br", "hr", "input", "meta", "link"]);
// CHỈ khớp đúng các thẻ THẬT sự xuất hiện trong body_html của 6 bài này (kiểm bằng script đối
// chiếu tần suất thẻ trước khi chốt danh sách) — KHÔNG dùng \w+ chung chung, vì công thức LaTeX
// thô có chỗ chứa bất đẳng thức kiểu "...<U_{2}$" (dấu "<" toán học, không phải mở thẻ); nếu
// khớp mọi chữ cái sau "<", chuỗi "<U" sẽ bị hiểu nhầm thành thẻ <u> (gạch chân) và làm lệch
// đếm độ sâu khi tách block cấp-1, có thể gộp nhầm 2 block liền kề thành 1.
const KNOWN_TAGS = "p|strong|em|br|img|div|table|thead|tbody|tr|td|th|ul|li|h1|h2|h3|h4";
const TAG_RE = new RegExp(`<(\\/)?(${KNOWN_TAGS})((?:\\s+[^<>]*?)?)(\\/?)>`, "gi");

function splitTopLevelBlocks(html: string): string[] {
  const blocks: string[] = [];
  let i = 0;
  const n = html.length;
  while (i < n) {
    TAG_RE.lastIndex = i;
    const m = TAG_RE.exec(html);
    if (!m) {
      const rest = html.slice(i);
      if (rest.trim()) blocks.push(rest);
      break;
    }
    if (m.index > i) {
      const gap = html.slice(i, m.index);
      if (gap.trim()) blocks.push(gap);
    }
    const isClose = !!m[1];
    const tagName = m[2].toLowerCase();
    const selfClose = !!m[4] || VOID_TAGS.has(tagName);
    if (isClose) {
      // thẻ đóng mồ côi ở cấp gốc — bỏ qua, không nên xảy ra với HTML hợp lệ
      i = TAG_RE.lastIndex;
      continue;
    }
    if (selfClose) {
      blocks.push(html.slice(m.index, TAG_RE.lastIndex));
      i = TAG_RE.lastIndex;
      continue;
    }
    // thẻ mở cấp gốc — quét tới thẻ đóng khớp (đếm độ sâu, không phân biệt tên thẻ con)
    let depth = 1;
    const localRe = new RegExp(`<(\\/)?(${KNOWN_TAGS})((?:\\s+[^<>]*?)?)(\\/?)>`, "gi");
    localRe.lastIndex = TAG_RE.lastIndex;
    let endPos = -1;
    let mm: RegExpExecArray | null;
    while ((mm = localRe.exec(html))) {
      const cf = !!mm[1];
      const nm = mm[2].toLowerCase();
      const self = !!mm[4] || VOID_TAGS.has(nm);
      if (self) continue;
      if (cf) {
        depth--;
        if (depth === 0) {
          endPos = localRe.lastIndex;
          break;
        }
      } else {
        depth++;
      }
    }
    if (endPos === -1) endPos = n; // phòng hờ HTML hỏng — lấy tới hết, log riêng ở nơi gọi
    blocks.push(html.slice(m.index, endPos));
    i = endPos;
  }
  return blocks;
}

function textOf(block: string): string {
  return block
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/\s+/g, " ")
    .trim();
}

const QUIZ_HEADINGS: Record<string, string> = {
  "CÂU HỎI TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN": "TN nhiều lựa chọn",
  "CÂU HỎI TRẮC NGHIỆM ĐÚNG SAI": "TN đúng sai",
  "CÂU HỎI TRẮC NGHIỆM TRẢ LỜI NGẮN": "TN trả lời ngắn",
};

// Khớp trên TEXT đã bóc hết thẻ (không khớp trên HTML thô) — vì một số câu hỏi nằm trong
// bảng (<table><th><strong>Câu 46:</strong>...</th>...) chứ không phải <p><strong> thường,
// nhưng sau khi bóc thẻ thì "Câu 46:" luôn là ký tự đầu của block.
const CAU_START_RE = /^Câu\s*(\d+)\s*[.:]/;

interface QuizGroup {
  headingRaw: string;
  headingShort: string;
  questions: { num: number; blocks: string[] }[];
}

interface SplitResult {
  theoryBlocks: string[];
  quizGroups: QuizGroup[];
  totalBlocks: number;
}

const DEBUG = process.argv.includes("--debug");

// CHỈ nhận đúng <h2 class="text-xl font-bold mt-3 mb-1.5"> — tiêu đề phụ do
// scripts/update-ly-thuyet-l12-tu-truong-dien-tu.mts tự chèn khi gộp nhiều "Chủ đề" GV
// (xem SourcePart.heading trong script đó). KHÔNG khớp các <h3> nhỏ hơn mà bản dựng HTML từ
// .tex tự sinh cho các mục con kiểu "I./II./III." bên trong 1 câu Đúng-Sai — nếu coi cả h3 là
// ranh giới, sẽ cắt oan giữa chừng 1 nhóm trắc nghiệm đang xử lý (đã gặp ở bài 12/lesson_id=13).
const SUBTOPIC_BREAK_RE = /^<h2\s+class="text-xl font-bold mt-3 mb-1\.5"/;

function splitTheoryAndQuiz(html: string): SplitResult {
  const blocks = splitTopLevelBlocks(html);
  const theoryBlocks: string[] = [];
  const quizGroups: QuizGroup[] = [];
  let mode: "theory" | "quiz" = "theory";
  let current: QuizGroup | null = null;

  for (const block of blocks) {
    const txt = textOf(block);

    // Ranh giới sang chủ đề con khác (script gộp bài chèn <h2>/<h3> giữa các "Chủ đề" GV) —
    // LUÔN quay lại lý thuyết, bất kể đang ở giữa 1 nhóm trắc nghiệm dở hay không. Đây là mốc
    // đáng tin hơn số thứ tự "Câu N" (nguồn GV có vài chỗ đánh số nhảy/lặp, không liên tục).
    if (SUBTOPIC_BREAK_RE.test(block.trimStart())) {
      if (current) {
        quizGroups.push(current);
        current = null;
      }
      mode = "theory";
      theoryBlocks.push(block);
      continue;
    }

    // Tiêu đề có thể chiếm trọn block (thường gặp) HOẶC bị dính vào cuối 1 đoạn lý thuyết
    // qua "<br />" (vd bài 10: "...ra ngoài. <br /><strong>CÂU HỎI...CHỌN</strong></p>") — tìm
    // theo substring trong text đã bóc thẻ, không yêu cầu khớp nguyên block.
    let matchedHeadingKey: string | null = null;
    for (const key of Object.keys(QUIZ_HEADINGS)) {
      if (txt === key || txt.endsWith(key)) {
        matchedHeadingKey = key;
        break;
      }
    }
    if (matchedHeadingKey) {
      if (txt !== matchedHeadingKey) {
        // còn sót lý thuyết phía trước tiêu đề trong CÙNG block — cắt bỏ đúng cụm
        // <thẻ-in-line>TIÊU ĐỀ</thẻ-in-line> khỏi HTML gốc, phần còn lại (nếu có nội dung
        // thật) vẫn là lý thuyết, giữ lại.
        const cutRe = new RegExp(`<(strong|b|em)[^>]*>\\s*${matchedHeadingKey.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\s*</\\1>`);
        const remainder = block.replace(cutRe, "");
        if (textOf(remainder).length > 0) theoryBlocks.push(remainder);
      }
      if (current) quizGroups.push(current);
      current = { headingRaw: matchedHeadingKey, headingShort: QUIZ_HEADINGS[matchedHeadingKey], questions: [] };
      mode = "quiz";
      continue;
    }
    if (mode === "theory") {
      theoryBlocks.push(block);
      continue;
    }
    // mode === "quiz" — nguồn GV thỉnh thoảng đánh số "Câu N" nhảy/lặp (lỗi đánh máy gốc,
    // không phải lỗi tách dữ liệu) nên KHÔNG dùng số thứ tự để quyết định thoát nhóm; chỉ
    // <h2>/<h3> hoặc tiêu đề trắc nghiệm mới ở trên mới được coi là ranh giới thật.
    const cauMatch = CAU_START_RE.exec(txt);
    if (cauMatch) {
      if (DEBUG && current!.questions.length > 0) {
        const prevNum = current!.questions[current!.questions.length - 1].num;
        const n = Number(cauMatch[1]);
        if (n !== prevNum + 1) console.log(`    [debug] số nhảy trong nhóm "${current?.headingShort}": Câu ${prevNum} → Câu ${n} (vẫn giữ, không tách nhóm)`);
      }
      current!.questions.push({ num: Number(cauMatch[1]), blocks: [block] });
      continue;
    }
    // block phụ (đáp án / hướng dẫn giải / bảng...) thuộc về câu hỏi hiện tại
    if (current && current.questions.length > 0) {
      current.questions[current.questions.length - 1].blocks.push(block);
    } else {
      // chưa có câu nào bắt đầu ngay sau tiêu đề — hiếm gặp, log để soát tay
      if (DEBUG) console.log(`    [debug] không thấy "Câu 1" ngay sau tiêu đề "${current?.headingShort}" — block kế tiếp: ${txt.slice(0, 90)}`);
      current?.questions.push({ num: 0, blocks: [block] });
    }
  }
  if (current) quizGroups.push(current);
  return { theoryBlocks, quizGroups, totalBlocks: blocks.length };
}

function cleanAlt(html: string): string {
  return html.replace(/\salt="[^"]*"/g, ' alt=""');
}

// ---------------------------------------------------------------------------------------

interface LessonJob {
  theoryItemId: number;
  lessonId: number;
  lessonTitle: string;
  baiTapMauItemId: number | null; // null = chưa có, phải tạo mới
}

const JOBS: LessonJob[] = [
  { theoryItemId: 52, lessonId: 11, lessonTitle: "Bài 10. Lực từ. Cảm ứng từ", baiTapMauItemId: 230 },
  { theoryItemId: 66, lessonId: 13, lessonTitle: "Bài 12. Hiện tượng cảm ứng điện từ", baiTapMauItemId: 67 },
  { theoryItemId: 141, lessonId: 14, lessonTitle: "Bài 13. Đại cương về dòng điện xoay chiều", baiTapMauItemId: 231 },
  { theoryItemId: 143, lessonId: 125, lessonTitle: "Bài 14. Máy phát điện xoay chiều. Máy biến áp", baiTapMauItemId: 232 },
  { theoryItemId: 145, lessonId: 126, lessonTitle: "Bài 15. Một số ứng dụng của cảm ứng điện từ", baiTapMauItemId: null },
  { theoryItemId: 183, lessonId: 127, lessonTitle: "Bài 16. Điện từ trường. Mô hình sóng điện từ", baiTapMauItemId: 184 },
];

interface QuestionEntry {
  label: string;
  body_html: string;
}

async function main() {
  const write = process.argv.includes("--write");
  const onlyArg = process.argv.find((a) => a.startsWith("--only="));
  const only = onlyArg ? new Set(onlyArg.slice("--only=".length).split(",").map((s) => Number(s.trim()))) : null;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  if (!url) fail("không đọc được NEXT_PUBLIC_SUPABASE_URL từ .env.local");
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_ANON_KEY");
  if (!anonKey) fail("không đọc được NEXT_PUBLIC_SUPABASE_ANON_KEY từ .env.local");

  let serviceKey: string | undefined;
  if (write) {
    serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY") ?? (await askHidden("Dán SUPABASE_SERVICE_ROLE_KEY (Settings → API → service_role): "));
    if (!serviceKey) fail("thiếu SUPABASE_SERVICE_ROLE_KEY (bắt buộc khi dùng --write)");
  }

  // dry-run chỉ cần đọc → dùng anon key là đủ, không cần xin service role key
  const readClient = createClient(url, serviceKey ?? anonKey, { auth: { autoRefreshToken: false, persistSession: false } });
  const writeClient = write ? createClient(url, serviceKey!, { auth: { autoRefreshToken: false, persistSession: false } }) : null;

  const backup: Record<string, unknown> = {};
  let grandTotalExtracted = 0;
  let grandTotalRawCauCount = 0;

  for (const job of JOBS) {
    if (only && !only.has(job.theoryItemId)) continue;
    console.log(`\n=== ${job.lessonTitle} (lesson_items#${job.theoryItemId}, lesson_id=${job.lessonId}) ===`);

    const { data: theoryRow, error: theoryErr } = await readClient
      .from("lesson_items")
      .select("id, kind, lesson_id, title, body_html")
      .eq("id", job.theoryItemId)
      .single();
    if (theoryErr) fail(`đọc mục lý thuyết #${job.theoryItemId}: ${theoryErr.message}`);
    if (!theoryRow || theoryRow.kind !== "ly_thuyet" || theoryRow.lesson_id !== job.lessonId) {
      fail(`mục #${job.theoryItemId} không khớp (kind=${theoryRow?.kind}, lesson_id=${theoryRow?.lesson_id}) — dừng để tránh sửa nhầm.`);
    }
    const oldHtml: string = theoryRow.body_html ?? "";
    // Đối chiếu: đếm SỐ BLOCK cấp-1 mà văn bản (đã bóc hết thẻ) bắt đầu bằng "Câu N" — đáng tin
    // hơn nhiều so với đếm thô chuỗi "Câu N." trong toàn bộ HTML (chuỗi đó đếm trùng cả những
    // lần "Câu N" bị nhắc lại bên trong lời giải của MỘT câu khác, luôn cao hơn số câu thật).
    const allBlocks = splitTopLevelBlocks(oldHtml);
    const trueCauBlockCount = allBlocks.filter((b) => CAU_START_RE.test(textOf(b))).length;
    grandTotalRawCauCount += trueCauBlockCount;

    const { theoryBlocks, quizGroups, totalBlocks } = splitTheoryAndQuiz(oldHtml);
    const newTheoryHtml = cleanAlt(theoryBlocks.join(""));

    let extractedCount = 0;
    const newQuestions: QuestionEntry[] = [];
    // đếm số nhóm cùng loại tiêu đề để đặt hậu tố khi 1 bài có >1 nhóm cùng loại (do gộp nhiều
    // "Chủ đề" GV vào 1 mục lý thuyết)
    const seenHeadingCount: Record<string, number> = {};
    for (const g of quizGroups) {
      seenHeadingCount[g.headingShort] = (seenHeadingCount[g.headingShort] ?? 0) + 1;
      const suffix = seenHeadingCount[g.headingShort] > 1 ? ` (phần ${seenHeadingCount[g.headingShort]})` : "";
      // Đánh số nhãn theo VỊ TRÍ trong nhóm (1,2,3,...), không dùng số "Câu N" gốc — nguồn GV
      // có vài chỗ đánh số nhảy/lặp/mở đầu bằng "Ví dụ" (xem README kèm script), dùng số gốc
      // làm nhãn sẽ ra nhãn trùng hoặc "Câu 0" khó hiểu. Nội dung hiển thị cho học sinh (trong
      // body_html) vẫn giữ nguyên đúng số "Câu N" gốc do GV soạn, chỉ nhãn quản trị đổi thôi.
      g.questions.forEach((q, idx) => {
        newQuestions.push({
          label: `${g.headingShort}${suffix} - Câu ${idx + 1}`,
          body_html: cleanAlt(q.blocks.join("")),
        });
        extractedCount += 1;
      });
    }
    grandTotalExtracted += extractedCount;

    console.log(`  Block cấp-1: ${totalBlocks} → giữ lý thuyết ${theoryBlocks.length}, ${quizGroups.length} nhóm trắc nghiệm`);
    for (const g of quizGroups) {
      const firstNum = g.questions[0]?.num ?? "?";
      const lastNum = g.questions[g.questions.length - 1]?.num ?? "?";
      console.log(`    - ${g.headingShort}: ${g.questions.length} câu (Câu ${firstNum}..${lastNum})`);
    }
    console.log(`  Tổng câu bắt được: ${extractedCount}  |  số block "Câu N" thật trong HTML gốc: ${trueCauBlockCount}${extractedCount < trueCauBlockCount ? "  ⚠ THIẾU — cần xem lại trước khi --write" : extractedCount > trueCauBlockCount ? "  (dư — do vài mục mở đầu bằng \"Ví dụ\" không khớp \"Câu N\", vẫn được gom vào, xem log --debug)" : "  ✓ khớp"}`);
    console.log(`  body_html lý thuyết: ${oldHtml.length} → ${newTheoryHtml.length} ký tự`);

    if (process.argv.includes("--dump")) {
      const dumpDir = path.resolve(scriptDir, "logs", "dump-preview");
      fs.mkdirSync(dumpDir, { recursive: true });
      fs.writeFileSync(path.join(dumpDir, `theory-${job.theoryItemId}.html`), newTheoryHtml, "utf8");
      fs.writeFileSync(path.join(dumpDir, `questions-${job.theoryItemId}.json`), JSON.stringify(newQuestions, null, 2), "utf8");
      console.log(`  [dump] đã ghi ${dumpDir}/theory-${job.theoryItemId}.html và questions-${job.theoryItemId}.json để soát tay`);
    }

    if (!write) continue;

    // ---- backup trước khi ghi ----
    backup[`theory_${job.theoryItemId}`] = { id: job.theoryItemId, body_html: oldHtml };

    let existingQuestions: QuestionEntry[] = [];
    let baiTapMauId = job.baiTapMauItemId;
    if (baiTapMauId) {
      const { data: btRow, error: btErr } = await readClient
        .from("lesson_items")
        .select("id, lesson_id, kind, questions, subtitle")
        .eq("id", baiTapMauId)
        .single();
      if (btErr) fail(`đọc mục bài tập mẫu #${baiTapMauId}: ${btErr.message}`);
      if (!btRow || btRow.kind !== "bai_tap_mau" || btRow.lesson_id !== job.lessonId) {
        fail(`mục #${baiTapMauId} không khớp bai_tap_mau — dừng để tránh ghi nhầm.`);
      }
      existingQuestions = (btRow.questions as QuestionEntry[]) ?? [];
      backup[`baitapmau_${baiTapMauId}`] = { id: baiTapMauId, questions: existingQuestions, subtitle: btRow.subtitle };
    }

    // 1) cập nhật lý thuyết
    const { error: updTheoryErr } = await writeClient!.from("lesson_items").update({ body_html: newTheoryHtml }).eq("id", job.theoryItemId);
    if (updTheoryErr) fail(`update lý thuyết #${job.theoryItemId}: ${updTheoryErr.message}`);
    console.log(`  ✓ đã cập nhật lý thuyết #${job.theoryItemId}`);

    // 2) cập nhật / tạo mục bài tập mẫu
    const mergedQuestions = [...existingQuestions, ...newQuestions];
    if (baiTapMauId) {
      const subtitle = `${mergedQuestions.length} dạng bài kèm lời giải`;
      const { error: updBtErr } = await writeClient!
        .from("lesson_items")
        .update({ questions: mergedQuestions, subtitle })
        .eq("id", baiTapMauId);
      if (updBtErr) fail(`update bài tập mẫu #${baiTapMauId}: ${updBtErr.message}`);
      console.log(`  ✓ đã cập nhật bài tập mẫu #${baiTapMauId} (${existingQuestions.length} → ${mergedQuestions.length} phần tử)`);
    } else {
      const { data: inserted, error: insErr } = await writeClient!
        .from("lesson_items")
        .insert({
          lesson_id: job.lessonId,
          kind: "bai_tap_mau",
          title: "Các dạng bài tập",
          subtitle: `${mergedQuestions.length} dạng bài kèm lời giải`,
          video_url: "",
          pdf_url: "",
          sort_order: 3,
          exam_ids: [],
          questions: mergedQuestions,
          due_at: null,
          quiz_min_correct: null,
          practice_pass_score: null,
          required: true,
        })
        .select("id")
        .single();
      if (insErr) fail(`insert bài tập mẫu cho lesson_id=${job.lessonId}: ${insErr.message}`);
      baiTapMauId = inserted!.id as number;
      console.log(`  ✓ đã tạo mục bài tập mẫu mới #${baiTapMauId} (${mergedQuestions.length} phần tử)`);
    }
  }

  if (write) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
    const backupPath = path.join(LOG_DIR, `l12-tu-truong-quiz-fix-backup-${Date.now()}.json`);
    fs.writeFileSync(backupPath, JSON.stringify(backup, null, 2), "utf8");
    console.log(`\nĐã backup nội dung cũ vào ${path.relative(process.cwd(), backupPath)} (dùng để khôi phục nếu cần).`);
    console.log(`Nhớ chạy: node scripts/build-content.mjs   rồi kiểm tra /lop-hoc/bai/?id=11,13,14,125,126,127 trước khi deploy.`);
  } else {
    console.log(`\n[dry-run] Tổng: bắt được ${grandTotalExtracted} câu / đếm thô ${grandTotalRawCauCount} câu trên toàn bộ 6 bài.`);
    console.log(`Không có gì được ghi vào Supabase. Chạy lại kèm --write để ghi thật (sẽ tự backup trước).`);
  }
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
