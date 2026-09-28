// Đăng MỘT file đề .docx đã chuẩn (từ xuat_thachlab.py: có `*`, "Lời giải:", Chủ đề/Dạng nếu có)
// vào một mục đề của bài học — đường script thay cho trang /quan-tri/dang-de khi không có
// phiên đăng nhập trình duyệt. Dùng chung readDocx → docxTextToBundle → bundleToRows với trang,
// nên quy tắc tách câu/đáp án/ảnh không lệch.
//
//   npx tsx scripts/upload-exam-docx.mts <de_thachlab.docx> --title "<Tên đề>" \
//        --lesson <lesson_id> --item <lesson_item_id> [--duration 50] [--dry] [--drop-vector-marks] [--log <log.json> --src "<tên file gốc>"]
//
// - Ảnh phải được nén sẵn (script không có canvas). Ảnh lên bucket lesson-media/<lesson_id>/.
// - Gắn vào mục theo kiểu "Giữ + thêm": đọc lại exam_ids ngay trước khi ghi, append id mới.
// - KHÔNG gắn nhãn AI (Edge Function classify-questions cần phiên người dùng) — câu chưa có
//   Chủ đề giữ nguyên trống, sửa sau ở /quan-tri/sua-de nếu cần.
// - Đọc NEXT_PUBLIC_SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY từ .env.local, không in khoá ra.
import { DOMParser as XmlDomParser } from "@xmldom/xmldom";
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readDocx, SHAPE_MARK, VECTOR_IMAGE_MARK } from "@/services/docx-reader";
import { docxTextToBundle } from "@/services/docx-exam-parser";
import { applyMediaToBundle, bundleToRows, typeCountSubtitle, validateBundle } from "@/services/lesson-import";
import { removeLessonMedia, uploadLessonMedia } from "@/services/lesson-media";
import { questionsMissingFigure } from "@/services/question-figures";

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

function fail(msg: string): never {
  console.error("✕ " + msg);
  process.exit(1);
}
function arg(name: string): string | undefined {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : undefined;
}

const file = process.argv[2];
if (!file || file.startsWith("--")) fail("thiếu đường dẫn file .docx");
const title = arg("--title") ?? fail("thiếu --title");
const lessonId = Number(arg("--lesson") ?? fail("thiếu --lesson"));
const itemId = Number(arg("--item") ?? fail("thiếu --item"));
const duration = Number(arg("--duration") ?? 50);
const dry = process.argv.includes("--dry");
const logPath = arg("--log");
const srcName = arg("--src");

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const env = Object.fromEntries(
  fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").filter((l) => l.includes("=") && !l.startsWith("#"))
    .map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^"|"$/g, "")]; }),
);
const url = env.NEXT_PUBLIC_SUPABASE_URL ?? fail("thiếu NEXT_PUBLIC_SUPABASE_URL trong .env.local");
const key = env.SUPABASE_SERVICE_ROLE_KEY ?? fail("thiếu SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const read = await readDocx(new Uint8Array(fs.readFileSync(file)));
if (read.mathTypeCount > 0) fail(`còn ${read.mathTypeCount} công thức MathType chưa chuyển (⟦CT⟧) — chạy mtef trước`);
let text = read.text;
if (process.argv.includes("--drop-vector-marks")) {
  const n = (text.match(new RegExp(`${VECTOR_IMAGE_MARK}|${SHAPE_MARK}`, "g")) ?? []).length;
  text = text.split(VECTOR_IMAGE_MARK).join("").split(SHAPE_MARK).join("");
  console.log(`  bỏ ${n} mốc ảnh WMF/hình vẽ Word (--drop-vector-marks)`);
}
const draft = docxTextToBundle(text, { title, durationMinutes: duration, images: read.images });
const bundle = draft.bundle;
const qs = bundle.exam.questions;
console.log(`Đọc ${path.basename(file)}: ${qs.length}/${draft.markerCount} câu dựng được · ${read.images.length} ảnh`);
for (const n of [...read.warnings, ...draft.notes]) console.log("  ! " + n);
if (qs.length !== draft.markerCount) fail("số câu dựng được khác số mốc 'Câu n.' — xem lại file");
const check = validateBundle(bundle);
if (!check.ok) fail("bundle không hợp lệ: " + check.errors.join("; "));
for (const w of check.warnings ?? []) console.log("  ~ " + w);
const missingFig = questionsMissingFigure(qs);
if (missingFig.length) console.log(`  ! Câu nhắc hình mà không có ảnh: ${missingFig.join(", ")}`);
const byType = qs.reduce<Record<string, number>>((m, q) => ((m[q.type] = (m[q.type] ?? 0) + 1), m), {});
console.log("  Dạng câu:", JSON.stringify(byType), "· không đáp án:", qs.filter((q) => !("answer" in q) || q.answer === "" || q.answer == null).length);
console.log("  Có Chủ đề:", qs.filter((q) => (q.topic ?? "").trim()).length, "/", qs.length);

if (dry) { console.log("(--dry: không ghi gì)"); process.exit(0); }

const { data: item, error: itemErr } = await supabase.from("lesson_items").select("id, lesson_id, exam_ids, kind").eq("id", itemId).single();
if (itemErr || !item) fail(`không đọc được lesson_items ${itemId}: ${itemErr?.message}`);
if (item.lesson_id !== lessonId) fail(`mục ${itemId} thuộc lesson ${item.lesson_id}, không phải ${lessonId}`);

let uploaded: string[] = [];
let examId: number | null = null;
try {
  let resolved = bundle;
  if (read.images.length) {
    const media = await uploadLessonMedia(supabase, lessonId, read.images);
    uploaded = media.map((m) => m.storagePath);
    resolved = applyMediaToBundle(bundle, media);
    console.log(`  ✓ tải ${media.length} ảnh`);
  }
  const rows = bundleToRows(resolved, lessonId);
  const ins = await supabase.from("exams").insert(rows.exam).select("id").single();
  if (ins.error || !ins.data) throw new Error("tạo đề lỗi: " + ins.error?.message);
  examId = ins.data.id as number;
  console.log(`  ✓ đề số ${examId}`);

  const { data: cur, error: curErr } = await supabase.from("lesson_items").select("exam_ids").eq("id", itemId).single();
  if (curErr || !cur) throw new Error("đọc lại exam_ids lỗi: " + curErr?.message);
  const nextIds = [...(cur.exam_ids as number[]), examId];
  const upd = await supabase.from("lesson_items").update({ exam_ids: nextIds, subtitle: typeCountSubtitle(rows.exam.questions, rows.exam.duration_minutes) }).eq("id", itemId);
  if (upd.error) throw new Error("gắn vào mục lỗi: " + upd.error.message);
  console.log(`  ✓ mục ${itemId}: ${cur.exam_ids.length} → ${nextIds.length} đề`);

  if (logPath && srcName) {
    const log = fs.existsSync(logPath) ? JSON.parse(fs.readFileSync(logPath, "utf8")) : {};
    log[srcName] = examId;
    fs.writeFileSync(logPath, JSON.stringify(log, null, 2) + "\n");
  }
  console.log(`Xong: "${title}" → exam ${examId}, sửa tại https://thachlab.id.vn/quan-tri/sua-de/?id=${examId}`);
} catch (e) {
  console.error("✕ " + (e instanceof Error ? e.message : String(e)));
  if (examId !== null) await supabase.from("exams").delete().eq("id", examId);
  if (uploaded.length) await removeLessonMedia(supabase, uploaded).catch(() => {});
  process.exit(1);
}
