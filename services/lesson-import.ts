/**
 * Thư viện thuần (không React, không getSupabase) để nhập một "gói bài học" JSON
 * vào LMS: validate, map sang payload hàng, và parse .tex thành nháp gói.
 * Dùng chung bởi trang `/quan-tri/nhap-bai` và script `scripts/upload-lesson.mjs`.
 */

import type { ExamQuestion } from "@/features/exams/types";
import type { LessonWorkedQuestion } from "@/features/lessons/types";
import type { RasterImageInput, UploadedMedia } from "@/services/lesson-media";
import { latexToHtml } from "@/services/latex-converter";
import { parseExamLatex } from "@/services/exam-latex-parser";

export const BUNDLE_SCHEMA = "thachlab.lesson-bundle/v1";

export type Difficulty = "" | "de" | "trung-binh" | "kho";

export interface LessonBundle {
  schema: string;
  target?: { class_name?: string; chapter_title?: string; lesson_title?: string };
  theory_title?: string;
  theory_subtitle?: string;
  theory_html: string;
  worked_examples: LessonWorkedQuestion[];
  exam: {
    title: string;
    topic?: string;
    difficulty?: Difficulty;
    duration_minutes?: number;
    subject_code?: string;
    questions: ExamQuestion[];
  };
  raster_images?: RasterImageInput[];
}

export interface BundleCheck {
  ok: boolean;
  errors: string[];
  warnings: string[];
}

const HTML_ITEM_WARN = 500 * 1024;
const HTML_ITEM_ERROR = 1.5 * 1024 * 1024;
const IMG_WARN = 400 * 1024;
const IMG_ERROR = 1.5 * 1024 * 1024;

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function leftoverLatex(html: string): string[] {
  const bad: string[] = [];
  if (/\\includegraphics\{/.test(html)) bad.push("\\includegraphics{…}");
  if (/\\begin\{tabular\}/.test(html)) bad.push("\\begin{tabular}");
  if (/\\section\{|\\subsection\{/.test(html)) bad.push("\\section{…}");
  if (/\\\[|\\\]/.test(html)) bad.push("\\[ … \\]");
  if (/\\textbf\{|\\textit\{/.test(html)) bad.push("\\textbf{…}");
  return bad;
}

function unbalancedDollars(html: string): boolean {
  const singles = (html.match(/(?<!\\)\$/g) || []).length;
  return singles % 2 !== 0;
}

function checkTags(html: string, label: string, out: string[]) {
  if (/<script\b/i.test(html) || /<style\b/i.test(html))
    out.push(`${label}: có thẻ <script>/<style> — không được phép.`);
  if (/\son\w+\s*=/i.test(html)) out.push(`${label}: có thuộc tính on*= (JS) — không được phép.`);
}

function approxBytes(s: string): number {
  return typeof Buffer !== "undefined"
    ? Buffer.byteLength(s, "utf8")
    : new TextEncoder().encode(s).length;
}

function checkHtmlBudget(html: string, label: string, check: BundleCheck) {
  const n = approxBytes(html);
  if (n > HTML_ITEM_ERROR) check.errors.push(`${label}: HTML quá lớn (${Math.round(n / 1024)} KB > 1.5 MB).`);
  else if (n > HTML_ITEM_WARN) check.warnings.push(`${label}: HTML khá lớn (${Math.round(n / 1024)} KB) — cân nhắc rút gọn SVG.`);
}

function checkQuestion(q: unknown, i: number, check: BundleCheck) {
  const label = `Câu ${i + 1}`;
  if (!isRecord(q)) return check.errors.push(`${label}: không phải object.`);
  const type = q.type;
  const explanation = typeof q.explanation === "string" ? q.explanation.trim() : "";
  if (!explanation && type !== "essay") check.warnings.push(`${label}: thiếu lời giải (explanation).`);
  if (typeof q.question !== "string" || !q.question.trim())
    check.errors.push(`${label}: thiếu nội dung câu hỏi.`);

  if (type === "multiple_choice") {
    if (!Array.isArray(q.options) || q.options.length !== 4)
      check.errors.push(`${label}: trắc nghiệm phải có đúng 4 phương án.`);
    if (typeof q.answer !== "number" || q.answer < 0 || q.answer > 3)
      check.errors.push(`${label}: đáp án phải là số 0–3.`);
  } else if (type === "true_false") {
    if (!Array.isArray(q.statements) || q.statements.length !== 4)
      check.errors.push(`${label}: đúng/sai phải có đúng 4 ý.`);
    else if (!q.statements.every((s) => isRecord(s) && typeof s.answer === "boolean"))
      check.errors.push(`${label}: mỗi ý đúng/sai cần answer là true/false.`);
  } else if (type === "short_answer") {
    const a = typeof q.answer === "string" ? q.answer.trim() : "";
    if (!a) check.errors.push(`${label}: thiếu đáp án.`);
    else if (a.length > 4) check.errors.push(`${label}: đáp án "${a}" dài quá 4 ký tự.`);
    else if (!/^-?\d+([.,]\d+)?$/.test(a))
      check.warnings.push(`${label}: đáp án "${a}" không phải dạng số.`);
  } else if (type === "essay") {
    check.warnings.push(`${label}: câu tự luận không được chấm tự động.`);
  } else {
    check.errors.push(`${label}: loại câu không hợp lệ ("${String(type)}").`);
  }
}

export function validateBundle(input: unknown): BundleCheck {
  const check: BundleCheck = { ok: false, errors: [], warnings: [] };
  if (!isRecord(input)) {
    check.errors.push("Gói không phải JSON object.");
    return check;
  }
  if (input.schema !== BUNDLE_SCHEMA)
    check.errors.push(`Sai schema (cần "${BUNDLE_SCHEMA}").`);

  const theory = typeof input.theory_html === "string" ? input.theory_html : "";
  if (!theory.trim()) check.errors.push("Thiếu theory_html.");
  else {
    const bad = leftoverLatex(theory);
    if (bad.length) check.errors.push(`Lý thuyết còn sót LaTeX chưa chuyển: ${bad.join(", ")}.`);
    if (unbalancedDollars(theory)) check.errors.push("Lý thuyết: số dấu $ lẻ — công thức chưa đóng.");
    checkTags(theory, "Lý thuyết", check.errors);
    checkHtmlBudget(theory, "Lý thuyết", check);
  }

  const worked = Array.isArray(input.worked_examples) ? input.worked_examples : [];
  if (!Array.isArray(input.worked_examples))
    check.errors.push("worked_examples phải là mảng.");
  worked.forEach((w, i) => {
    const label = `Dạng bài ${i + 1}`;
    if (!isRecord(w) || typeof w.body_html !== "string" || !w.body_html.trim())
      return check.errors.push(`${label}: thiếu body_html.`);
    if (typeof w.label !== "string" || !w.label.trim())
      check.warnings.push(`${label}: thiếu nhãn ngắn (label).`);
    const bad = leftoverLatex(w.body_html);
    if (bad.length) check.errors.push(`${label}: còn sót LaTeX: ${bad.join(", ")}.`);
    if (unbalancedDollars(w.body_html)) check.errors.push(`${label}: số dấu $ lẻ.`);
    checkTags(w.body_html, label, check.errors);
    checkHtmlBudget(w.body_html, label, check);
  });

  const exam = isRecord(input.exam) ? input.exam : null;
  if (!exam) check.errors.push("Thiếu khối exam.");
  else {
    if (typeof exam.title !== "string" || !exam.title.trim())
      check.errors.push("exam.title trống.");
    const diff = exam.difficulty ?? "";
    if (!["", "de", "trung-binh", "kho"].includes(diff as string))
      check.errors.push(`exam.difficulty không hợp lệ ("${String(diff)}").`);
    const qs = Array.isArray(exam.questions) ? exam.questions : [];
    if (qs.length === 0) check.errors.push("Đề chưa có câu hỏi nào.");
    qs.forEach((q, i) => checkQuestion(q, i, check));
  }

  const imgs = Array.isArray(input.raster_images) ? input.raster_images : [];
  imgs.forEach((img, i) => {
    const label = `Ảnh ${i + 1}`;
    if (!isRecord(img)) return check.errors.push(`${label}: không phải object.`);
    if (typeof img.dataUri !== "string" || !/^data:image\//.test(img.dataUri))
      return check.errors.push(`${label}: dataUri phải bắt đầu bằng "data:image/".`);
    if (typeof img.placeholder !== "string" || !img.placeholder.trim())
      check.errors.push(`${label}: thiếu placeholder.`);
    const b64 = img.dataUri.split(",")[1] ?? "";
    const bytes = Math.floor(b64.length * 0.75);
    if (bytes > IMG_ERROR) check.errors.push(`${label}: nặng ${Math.round(bytes / 1024)} KB (> 1.5 MB) — nén lại.`);
    else if (bytes > IMG_WARN) check.warnings.push(`${label}: nặng ${Math.round(bytes / 1024)} KB — cân nhắc nén.`);
  });

  // placeholder chưa thay hết
  const allHtml = [theory, ...worked.map((w) => (isRecord(w) ? String(w.body_html ?? "") : ""))].join("\n");
  const declared = new Set(imgs.map((i) => (isRecord(i) ? String(i.placeholder) : "")));
  for (const m of allHtml.matchAll(/\bmedia\/[\w./-]+/g)) {
    if (!declared.has(m[0]))
      check.errors.push(`Còn placeholder ảnh chưa khai báo trong raster_images: "${m[0]}".`);
  }

  check.ok = check.errors.length === 0;
  return check;
}

// ---------- Map sang payload hàng ----------

export function typeCountSubtitle(questions: ExamQuestion[], minutes?: number): string {
  const short: Record<string, string> = { multiple_choice: "TN", true_false: "ĐS", short_answer: "TLN" };
  const counts: Record<string, number> = {};
  for (const q of questions) counts[q.type] = (counts[q.type] ?? 0) + 1;
  const parts = Object.entries(short)
    .filter(([t]) => counts[t])
    .map(([t, s]) => `${counts[t]} ${s}`);
  const total = questions.length;
  const tail = minutes ? ` — ${minutes} phút` : "";
  return `${total} câu${parts.length ? ` (${parts.join(" · ")})` : ""}${tail}`;
}

export function applyMediaToBundle(bundle: LessonBundle, media: UploadedMedia[]): LessonBundle {
  const swap = (html: string) => {
    let out = html;
    for (const m of media) out = out.split(m.placeholder).join(m.url);
    return out;
  };
  return {
    ...bundle,
    theory_html: swap(bundle.theory_html),
    worked_examples: bundle.worked_examples.map((w) => ({ ...w, body_html: swap(w.body_html) })),
    exam: {
      ...bundle.exam,
      questions: bundle.exam.questions.map((q) => JSON.parse(swap(JSON.stringify(q))) as ExamQuestion),
    },
  };
}

export interface ExamRow {
  title: string;
  duration_minutes: number;
  published: boolean;
  subject_code: string;
  topic: string;
  difficulty: Difficulty;
  questions: ExamQuestion[];
}

export interface LessonItemRow {
  lesson_id: number;
  kind: "ly_thuyet" | "bai_tap_mau";
  title: string;
  subtitle: string;
  body_html: string;
  video_url: "";
  pdf_url: "";
  questions: LessonWorkedQuestion[];
  exam_ids: number[];
  sort_order: number;
}

export function bundleToRows(bundle: LessonBundle, lessonId: number): {
  lyThuyet: LessonItemRow;
  baiTapMau: LessonItemRow;
  exam: ExamRow;
} {
  const e = bundle.exam;
  return {
    lyThuyet: {
      lesson_id: lessonId,
      kind: "ly_thuyet",
      title: bundle.theory_title?.trim() || "Lý thuyết trọng tâm",
      subtitle: bundle.theory_subtitle?.trim() || "",
      body_html: bundle.theory_html,
      video_url: "",
      pdf_url: "",
      questions: [],
      exam_ids: [],
      sort_order: 1,
    },
    baiTapMau: {
      lesson_id: lessonId,
      kind: "bai_tap_mau",
      title: "Các dạng bài tập",
      subtitle: bundle.worked_examples.length
        ? `${bundle.worked_examples.length} dạng bài kèm lời giải`
        : "",
      body_html: "",
      video_url: "",
      pdf_url: "",
      questions: bundle.worked_examples.filter((w) => w.body_html.trim() !== ""),
      exam_ids: [],
      sort_order: 3,
    },
    exam: {
      title: e.title.trim(),
      duration_minutes: e.duration_minutes ?? 20,
      published: true,
      subject_code: e.subject_code || "vat-ly",
      topic: e.topic?.trim() || "",
      difficulty: e.difficulty ?? "",
      questions: e.questions,
    },
  };
}

// ---------- Parse .tex → nháp gói (đường prefill, không bắt buộc) ----------

const THEORY_RE = /L[ÍI]\s*THUY[ẾE]T|LÝ\s*THUY[ẾE]T|KI[ẾE]N\s*TH[ỨU]C|T[ÓO]M\s*T[ẮA]T|C[ƠO]\s*S[ỞO]/i;
const WORKED_RE = /B[ÀA]I\s*T[ẬA]P\s*(MINH\s*H[ỌO]A|M[ẪA]U|V[ÍI]\s*D[ỤU])|V[ÍI]\s*D[ỤU]|D[ẠA]NG\s*\d/i;
const EXERCISE_RE = /T[ỰU]\s*LUY[ỆE]N|LUY[ỆE]N\s*T[ẬA]P|TR[ẮA]C\s*NGHI[ỆE]M|V[ỀE]\s*NH[ÀA]|PH[ẦA]N\s*[IVX\d]/i;

export interface LessonTexDraft {
  theory_html: string;
  worked_examples: LessonWorkedQuestion[];
  exercise_block: string;
  notes: string[];
}

export function parseLessonTex(tex: string): LessonTexDraft {
  const notes: string[] = [];
  const headRe = /\\(sub)?section\*?\{([^}]+)\}/g;
  const heads: { title: string; sub: boolean; start: number; contentStart: number }[] = [];
  let m: RegExpExecArray | null;
  while ((m = headRe.exec(tex))) {
    heads.push({
      title: m[2],
      sub: !!m[1],
      start: m.index,
      contentStart: m.index + m[0].length,
    });
  }

  const regions = heads.map((h, i) => ({
    title: h.title,
    sub: h.sub,
    body: tex.slice(h.contentStart, i + 1 < heads.length ? heads[i + 1].start : tex.length),
    rawFrom: h.start,
  }));

  const theoryParts: string[] = [];
  const worked: LessonWorkedQuestion[] = [];
  let exerciseFrom = -1;

  for (const r of regions) {
    if (exerciseFrom === -1 && EXERCISE_RE.test(r.title)) {
      exerciseFrom = r.rawFrom;
      break;
    }
    if (WORKED_RE.test(r.title)) {
      worked.push({
        label: shortLabel(r.title),
        body_html: latexToHtml(r.body, "media").html,
      });
    } else if (THEORY_RE.test(r.title) || theoryParts.length === 0) {
      // Bỏ tiêu đề cấp \section (thường là tên bài/chương — đã có ở cột title);
      // chỉ giữ tiêu đề \subsection làm <h3> trong body_html.
      const head = r.sub ? `\\subsection{${r.title}}\n` : "";
      theoryParts.push(latexToHtml(`${head}${r.body}`, "media").html);
    }
  }

  if (heads.length === 0) {
    notes.push("Không thấy \\section/\\subsection — coi toàn bộ là lý thuyết.");
    theoryParts.push(latexToHtml(tex, "media").html);
  }
  if (exerciseFrom === -1) notes.push("Không thấy phần bài tập (TỰ LUYỆN / PHẦN I…).");

  return {
    theory_html: theoryParts.join("\n"),
    worked_examples: worked,
    exercise_block: exerciseFrom === -1 ? "" : tex.slice(exerciseFrom),
    notes,
  };
}

function shortLabel(title: string): string {
  const d = title.match(/D[ẠA]NG\s*(\d+)/i);
  if (d) return `Dạng ${d[1]}`;
  const v = title.match(/V[ÍI]\s*D[ỤU]\s*(\d+)?/i);
  if (v) return v[1] ? `Ví dụ ${v[1]}` : "Ví dụ";
  return title.trim().slice(0, 24);
}

/** Tiện ích: parse .tex thành nháp LessonBundle đầy đủ (câu đề cần rà lại tay). */
export function texToBundleDraft(tex: string, examTitle: string): { bundle: LessonBundle; notes: string[] } {
  const draft = parseLessonTex(tex);
  const parsed = draft.exercise_block ? parseExamLatex(draft.exercise_block) : { questions: [], warnings: [] };
  return {
    bundle: {
      schema: BUNDLE_SCHEMA,
      theory_html: draft.theory_html,
      worked_examples: draft.worked_examples,
      exam: {
        title: examTitle,
        difficulty: "",
        duration_minutes: 20,
        subject_code: "vat-ly",
        questions: parsed.questions,
      },
      raster_images: [],
    },
    notes: [...draft.notes, ...("warnings" in parsed ? parsed.warnings : [])],
  };
}
