"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { AlertTriangle, CheckCircle2, Eraser, FileText, PencilLine, Sparkles, Upload, WandSparkles } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import ExamDraftEditor from "@/components/admin/ExamDraftEditor";
import { useToast } from "@/components/ui/Toast";
import { QUESTION_FORM_LABELS, auditQuestionTags, type ExamQuestion, type QuestionForm } from "@/features/exams/types";
import { classifyQuestionTags } from "@/services/ai-classify";
import type { QuestionTopic } from "@/services/analytics";
import { questionTextForAi } from "@/services/exam-question-text";
import {
  SAMPLE_TEXT,
  setChoiceAnswer,
  setQuestionTag,
  setQuestionTagMany,
  setShortAnswer,
  toggleStatementAnswer,
  type TagField,
} from "@/services/azota-text";
import { docxTextToBundle } from "@/services/docx-exam-parser";
import { readDocx } from "@/services/docx-reader";
import { compressImageFile } from "@/services/image-compress";
import { BUNDLE_SCHEMA, typeCountSubtitle, type LessonBundle } from "@/services/lesson-import";
import type { RasterImageInput } from "@/services/lesson-media";
import { takeHandoff } from "@/services/question-bank";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const LETTERS = ["A", "B", "C", "D"];

export type TopicGroup = { parent: QuestionTopic; names: string[] };

/** Đưa từ trang gọi vào để "gieo" đề (vd từ gói JSON dán ở chế độ nâng cao) — đổi `token` để áp lại. */
export interface ExamSectionSeed {
  token: number;
  bundle: LessonBundle;
}

export interface ExamSectionProps {
  subjectCode: string;
  topicGroups: TopicGroup[];
  catalogNames: string[];
  lessonPicked: boolean;
  onChange: (bundle: LessonBundle) => void;
  /** Đánh số badge của 2 khối "Nội dung đề" / "Xem trước & đáp án" (mặc định 1, 2). */
  numberOffset?: number;
  /** Lấy sẵn câu từ Ngân hàng câu hỏi khi mở trang (chỉ trang Đăng đề dùng). */
  enableQuestionBankHandoff?: boolean;
  onHandoffGrade?: (grade: string) => void;
  /** Gói ngoài muốn nạp thẳng vào chế độ sửa chi tiết (vd JSON dán ở khối "Nâng cao"). */
  externalSeed?: ExamSectionSeed | null;
}

async function compressRasterInputs(images: RasterImageInput[]): Promise<RasterImageInput[]> {
  const out: RasterImageInput[] = [];
  for (const img of images) {
    try {
      const res = await fetch(img.dataUri);
      const blob = await res.blob();
      if (blob.type === "image/svg+xml" || blob.type === "image/gif") {
        out.push(img);
        continue;
      }
      const file = new File([blob], img.name, { type: blob.type });
      const compressed = await compressImageFile(file, { maxDimension: 1400, quality: 0.8 });
      const dataUri: string = await new Promise((resolve, reject) => {
        const fr = new FileReader();
        fr.onload = () => resolve(String(fr.result));
        fr.onerror = () => reject(fr.error);
        fr.readAsDataURL(compressed);
      });
      out.push({ ...img, name: compressed.name, dataUri });
    } catch {
      out.push(img);
    }
  }
  return out;
}
// Ảnh raster được nén ngay trước khi trang gọi upload — export để publish() dùng lại.
export { compressRasterInputs };

/** Chỗ còn thiếu của một câu — hiện ngay trên thẻ xem trước. */
function problems(q: ExamQuestion): string[] {
  const out: string[] = [];
  if (!q.question.trim()) out.push("chưa có nội dung");
  if (q.type === "multiple_choice") {
    if (q.options.length < 4 || q.options.some((o) => !o.trim())) out.push("thiếu phương án");
    if (q.answer < 0 || q.answer > 3) out.push("chưa có đáp án");
  } else if (q.type === "true_false") {
    if (q.statements.length < 4 || q.statements.some((s) => !s.text.trim())) out.push("thiếu ý a–d");
  } else if (q.type === "short_answer") {
    const a = q.answer.trim();
    if (!a) out.push("chưa có đáp án");
    else if (a.length > 4) out.push("đáp án dài quá 4 ký tự");
  }
  if (!q.explanation.trim()) out.push("chưa có lời giải");
  return out;
}


/**
 * Khối "dán/thả đề kiểu Azota → xem trước, đáp án và nhãn bấm-để-sửa" — dùng chung
 * bởi trang Đăng đề (`/quan-tri/dang-de`) và phần Đề của trang Đăng bài học
 * (`/quan-tri/nhap-bai`), để hai nơi luôn cùng một trải nghiệm và cùng một parser.
 */
export default function ExamSection({
  subjectCode,
  topicGroups,
  catalogNames,
  lessonPicked,
  onChange,
  numberOffset = 1,
  enableQuestionBankHandoff = false,
  onHandoffGrade,
  externalSeed = null,
}: ExamSectionProps) {
  const toast = useToast();
  const fileRef = useRef<HTMLInputElement>(null);

  const [text, setText] = useState("");
  const [debounced, setDebounced] = useState("");
  const [images, setImages] = useState<RasterImageInput[]>([]);
  const [fileNotes, setFileNotes] = useState<string[]>([]);
  const [fileName, setFileName] = useState<string | null>(null);
  const [reading, setReading] = useState(false);
  const [dragging, setDragging] = useState(false);

  const [titleInput, setTitleInput] = useState<string | null>(null);
  const [durationInput, setDurationInput] = useState<number | null>(null);
  const [edited, setEdited] = useState<LessonBundle | null>(null);

  useEffect(() => {
    const t = setTimeout(() => setDebounced(text), 250);
    return () => clearTimeout(t);
  }, [text]);

  useEffect(() => {
    if (!enableQuestionBankHandoff) return;
    const h = takeHandoff();
    if (h && h.questions.length > 0) {
      queueMicrotask(() => {
        setEdited({
          schema: BUNDLE_SCHEMA,
          theory_html: "",
          worked_examples: [],
          exam: { title: h.title || "Đề kiểm tra", duration_minutes: 45, subject_code: subjectCode, questions: h.questions },
        });
        setFileNotes([
          `Đã lấy ${h.questions.length} câu từ Ngân hàng câu hỏi. Sửa tiêu đề/thời gian rồi chọn lớp – bài và Đăng.`,
        ]);
        if (h.grade) onHandoffGrade?.(h.grade);
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const lastSeedToken = useRef<number | null>(null);
  useEffect(() => {
    if (!externalSeed || externalSeed.token === lastSeedToken.current) return;
    lastSeedToken.current = externalSeed.token;
    setText("");
    setEdited(JSON.parse(JSON.stringify(externalSeed.bundle)) as LessonBundle);
  }, [externalSeed]);

  const draft = useMemo(
    () => (debounced.trim() ? docxTextToBundle(debounced, { subjectCode, images }) : null),
    [debounced, subjectCode, images],
  );
  const guessedTitle = draft && draft.bundle.exam.title !== "Đề kiểm tra" ? draft.bundle.exam.title : "";
  const title = titleInput ?? guessedTitle;
  const duration = durationInput ?? draft?.bundle.exam.duration_minutes ?? 45;

  const bundle: LessonBundle = useMemo(() => {
    if (edited) return edited;
    if (!draft)
      return {
        schema: BUNDLE_SCHEMA,
        theory_html: "",
        worked_examples: [],
        exam: { title: title.trim() || "Đề kiểm tra", duration_minutes: duration, subject_code: subjectCode, questions: [] },
      };
    return {
      ...draft.bundle,
      exam: {
        ...draft.bundle.exam,
        title: title.trim() || draft.bundle.exam.title,
        duration_minutes: duration,
        subject_code: subjectCode,
      },
    };
  }, [edited, draft, title, duration, subjectCode]);

  useEffect(() => {
    onChange(bundle);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bundle]);

  const questions = bundle.exam.questions;
  const notes = useMemo(
    () => [...fileNotes, ...(draft?.notes ?? [])].filter((n) => !n.startsWith('Không thấy "PHẦN')),
    [fileNotes, draft],
  );
  const incompleteCount = questions.filter((q) => problems(q).length > 0).length;
  const tagAudit = useMemo(() => auditQuestionTags(questions, catalogNames), [questions, catalogNames]);
  const gridEnabled = !edited && !!draft && draft.markerCount === questions.length && questions.length > 0;
  const imageSrc = useMemo(() => {
    const map = new Map(images.map((im) => [im.placeholder, im.dataUri]));
    return (html: string) =>
      map.size ? html.replace(/src="(media\/[^"]+)"/g, (m, p: string) => (map.has(p) ? `src="${map.get(p)}"` : m)) : html;
  }, [images]);

  async function handleFile(file: File) {
    if (!/\.docx$/i.test(file.name)) {
      toast("error", "Chỉ nhận file .docx (Word). File .doc cũ: mở Word → Save As → .docx.");
      return;
    }
    setReading(true);
    try {
      const read = await readDocx(await file.arrayBuffer());
      setEdited(null);
      setText(read.text);
      setImages(read.images);
      setFileName(file.name);
      const n: string[] = [...read.warnings];
      if (read.mathTypeCount > 0)
        n.push(
          `Còn ${read.mathTypeCount} công thức MathType chưa chuyển (mốc ⟦CT⟧). Trong Word: MathType → Convert Equations → Microsoft Office Math, rồi tải lại.`,
        );
      setFileNotes(n);
      setTitleInput(null);
      setDurationInput(null);
      toast("success", `Đã đọc ${file.name}${read.images.length ? ` · ${read.images.length} ảnh` : ""}.`);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : String(e));
    } finally {
      setReading(false);
    }
  }

  function clearAll() {
    if (text && !window.confirm("Xóa toàn bộ nội dung đề đang soạn?")) return;
    setText("");
    setImages([]);
    setFileName(null);
    setFileNotes([]);
    setEdited(null);
    setTitleInput(null);
    setDurationInput(null);
  }

  function startEditing() {
    setEdited(JSON.parse(JSON.stringify(bundle)) as LessonBundle);
  }
  function stopEditing() {
    if (edited && !window.confirm("Quay lại văn bản sẽ bỏ các sửa đổi chi tiết. Tiếp tục?")) return;
    setEdited(null);
  }

  function pickChoice(i: number, letter: string) {
    setText((t) => setChoiceAnswer(t, i, letter));
  }
  function toggleStatement(i: number, letter: string) {
    setText((t) => toggleStatementAnswer(t, i, letter));
  }
  function commitShort(i: number, value: string) {
    setText((t) => setShortAnswer(t, i, value));
  }
  function commitTag(i: number, field: TagField, value: string) {
    setText((t) => setQuestionTag(t, i, field, value));
  }
  function commitTagMany(indexes: number[], field: TagField, value: string) {
    setText((t) => setQuestionTagMany(t, indexes, field, value));
  }

  return (
    <section className="grid gap-4 lg:grid-cols-2">
      <div className="space-y-3">
        <div className="flex flex-wrap items-center gap-2">
          <span className="admin-badge admin-badge--accent">{numberOffset}</span>
          <span className="text-sm font-semibold text-white">Nội dung đề</span>
          <div className="ml-auto flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => fileRef.current?.click()}
              disabled={reading || !!edited}
              className="admin-chip"
            >
              <Upload size={14} /> {reading ? "Đang đọc…" : "Tải file Word"}
            </button>
            <button
              type="button"
              onClick={() => {
                setEdited(null);
                setText(SAMPLE_TEXT);
                setTitleInput(null);
                setDurationInput(null);
              }}
              disabled={!!edited}
              className="admin-chip"
            >
              <WandSparkles size={14} /> Đề mẫu
            </button>
            <button
              type="button"
              onClick={clearAll}
              className="inline-flex items-center gap-1 rounded-lg bg-white/10 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:bg-white/20"
            >
              <Eraser size={14} /> Xóa
            </button>
          </div>
          <input
            ref={fileRef}
            type="file"
            accept=".docx"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0];
              e.target.value = "";
              if (f) void handleFile(f);
            }}
          />
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <label className="text-xs font-semibold text-slate-400">
            Tên đề
            <input
              value={title}
              onChange={(e) => setTitleInput(e.target.value)}
              placeholder="vd: Luyện tập – Động học"
              className={`${inputCls} mt-1`}
            />
          </label>
          <label className="text-xs font-semibold text-slate-400">
            Thời gian (phút)
            <input
              type="number"
              min={5}
              max={180}
              value={duration}
              onChange={(e) => setDurationInput(Number(e.target.value))}
              className={`${inputCls} mt-1`}
            />
          </label>
        </div>

        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            const f = e.dataTransfer.files[0];
            if (f) void handleFile(f);
          }}
          className={`rounded-2xl border ${dragging ? "border-blue-400 bg-blue-500/10" : "border-white/10"}`}
        >
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            readOnly={!!edited}
            spellCheck={false}
            placeholder={
              "Dán đề vào đây (Ctrl+V từ Word) hoặc kéo file .docx thả vào.\n\n" +
              "Câu 1. Nội dung câu hỏi…\nA. …   *B. …   C. …   D. …      ← dấu * trước đáp án đúng\nLời giải: …\n\n" +
              "PHẦN II: câu đúng–sai đánh * ở ý Đúng (*a) …). PHẦN III: dòng “Đáp án: 2,5”."
            }
            className={`${inputCls} min-h-[50vh] resize-y font-mono text-[13px] leading-relaxed ${edited ? "opacity-60" : ""}`}
          />
        </div>

        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-400">
          {fileName && (
            <span className="inline-flex items-center gap-1">
              <FileText size={13} className="text-blue-300" /> {fileName}
            </span>
          )}
          {draft && (
            <span>
              {questions.length}/{draft.markerCount} câu dựng được
              {questions.length > 0 && ` · ${typeCountSubtitle(questions)}`}
              {images.length > 0 && ` · ${images.length} ảnh`}
            </span>
          )}
          {incompleteCount > 0 && (
            <span className="inline-flex items-center gap-1 text-amber-300">
              <AlertTriangle size={13} /> {incompleteCount} câu còn thiếu
            </span>
          )}
          {questions.length > 0 && incompleteCount === 0 && (
            <span className="inline-flex items-center gap-1 text-emerald-300">
              <CheckCircle2 size={13} /> Đủ đáp án và lời giải
            </span>
          )}
        </div>

        {notes.length > 0 && (
          <ul className="space-y-1 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-xs text-amber-200">
            {notes.map((n, i) => (
              <li key={i}>• {n}</li>
            ))}
          </ul>
        )}

        <details className="text-xs text-slate-400">
          <summary className="cursor-pointer hover:text-slate-200">Cách trình bày đề để trang đọc được hết</summary>
          <ul className="mt-2 list-disc space-y-1 pl-5">
            <li>Mỗi câu bắt đầu bằng <code>Câu 1.</code>, <code>Câu 2.</code> (gõ tay, không dùng đánh số tự động của Word).</li>
            <li>Đáp án đúng: dấu <b>*</b> ngay trước phương án (<code>*B. 5 m/s</code>) hoặc dòng <code>Đáp án: B</code>.</li>
            <li>Câu đúng–sai: <code>*a)</code>, <code>*c)</code> ở các ý Đúng. Trả lời ngắn: <code>Đáp án: 2,5</code>.</li>
            <li>Có <code>PHẦN I / II / III</code> thì tự nhận loại câu; không có thì coi cả đề là trắc nghiệm A–D.</li>
            <li>Công thức gõ trong <code>$…$</code>. Công thức MathType trong Word: Convert Equations → Office Math trước khi tải.</li>
            <li>Lời giải: dòng <code>Lời giải:</code> sau các phương án.</li>
            <li>
              Phân loại (để thống kê chỗ hổng & ngân hàng câu hỏi): thêm dòng <code>Chủ đề: &lt;yêu cầu cần đạt&gt;</code> và{" "}
              <code>Dạng: lý thuyết</code> / <code>Dạng: bài tập</code> vào cuối mỗi câu — hoặc chọn ở bảng “Phân loại câu” bên phải,
              trang tự ghi hai dòng đó vào văn bản.
            </li>
          </ul>
        </details>
      </div>

      <div className="space-y-3 lg:sticky lg:top-4 lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto lg:pr-1">
        <div className="flex flex-wrap items-center gap-2">
          <span className="admin-badge admin-badge--accent">{numberOffset + 1}</span>
          <span className="text-sm font-semibold text-white">Xem trước & đáp án</span>
          <div className="ml-auto">
            {edited ? (
              <button
                type="button"
                onClick={stopEditing}
                className="rounded-lg bg-white/10 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:bg-white/20"
              >
                Quay lại văn bản
              </button>
            ) : (
              <button
                type="button"
                onClick={startEditing}
                disabled={questions.length === 0}
                className="admin-chip"
              >
                <PencilLine size={14} /> Sửa chi tiết từng câu
              </button>
            )}
          </div>
        </div>

        {edited ? (
          <ExamDraftEditor
            bundle={bundle}
            onChange={setEdited}
            topicOptions={topicGroups.flatMap((g) => g.names)}
            aiTopicCandidates={lessonPicked ? (topicGroups[0]?.names ?? []) : []}
          />
        ) : questions.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-white/15 p-8 text-center text-sm text-slate-500">
            Chưa có câu nào. Dán đề hoặc bấm “Đề mẫu” để xem cách trình bày.
          </div>
        ) : (
          <>
            <AnswerGrid
              questions={questions}
              enabled={gridEnabled}
              onChoice={pickChoice}
              onToggle={toggleStatement}
              onShort={commitShort}
            />
            {!gridEnabled && draft && draft.markerCount !== questions.length && (
              <p className="text-xs text-amber-300">
                Số câu dựng được khác số mốc “Câu n.” nên bảng đáp án tạm khoá — sửa trong văn bản cho khớp trước.
              </p>
            )}
            <TagGrid
              questions={questions}
              enabled={gridEnabled}
              groups={topicGroups}
              lessonPicked={lessonPicked}
              audit={tagAudit}
              onTag={commitTag}
              onTagMany={commitTagMany}
            />
            <div className="space-y-3">
              {questions.map((q, i) => (
                <PreviewCard key={i} index={i + 1} q={q} fix={imageSrc} />
              ))}
            </div>
          </>
        )}
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------

function AnswerGrid({
  questions,
  enabled,
  onChoice,
  onToggle,
  onShort,
}: {
  questions: ExamQuestion[];
  enabled: boolean;
  onChoice: (i: number, letter: string) => void;
  onToggle: (i: number, letter: string) => void;
  onShort: (i: number, value: string) => void;
}) {
  return (
    <div className="admin-card">
      <div className="mb-2 text-xs font-semibold text-slate-400">
        Bảng đáp án {enabled ? "— bấm để đổi, văn bản bên trái tự cập nhật" : ""}
      </div>
      <div className="flex flex-wrap gap-2">
        {questions.map((q, i) => (
          <div
            key={i}
            className={`flex items-center gap-1 rounded-lg border px-1.5 py-1 ${
              problems(q).some((p) => p.includes("đáp án")) ? "border-amber-500/40" : "border-white/10"
            }`}
          >
            <span className="w-5 text-right text-[11px] font-bold text-slate-400">{i + 1}</span>
            {q.type === "multiple_choice" &&
              LETTERS.map((L, j) => (
                <button
                  key={L}
                  type="button"
                  disabled={!enabled}
                  onClick={() => onChoice(i, L)}
                  className={`h-6 w-6 rounded text-[11px] font-bold transition ${
                    q.answer === j ? "bg-emerald-500 text-white" : "bg-white/5 text-slate-300 hover:bg-white/15"
                  } disabled:cursor-default`}
                >
                  {L}
                </button>
              ))}
            {q.type === "true_false" &&
              ["a", "b", "c", "d"].map((l, j) => (
                <button
                  key={l}
                  type="button"
                  disabled={!enabled}
                  onClick={() => onToggle(i, l)}
                  title={q.statements[j]?.answer ? "Đúng" : "Sai"}
                  className={`h-6 w-6 rounded text-[11px] font-bold transition ${
                    q.statements[j]?.answer ? "bg-emerald-500 text-white" : "bg-red-500/20 text-red-200 hover:bg-red-500/40"
                  } disabled:cursor-default`}
                >
                  {l}
                </button>
              ))}
            {q.type === "short_answer" && (
              <input
                key={q.answer}
                defaultValue={q.answer}
                disabled={!enabled}
                maxLength={6}
                onBlur={(e) => {
                  if (e.target.value.trim() !== q.answer.trim()) onShort(i, e.target.value);
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") (e.target as HTMLInputElement).blur();
                }}
                placeholder="?"
                className="h-6 w-14 rounded border border-white/10 bg-white/5 px-1 text-center text-[11px] font-bold text-emerald-300 focus:border-primary focus:outline-none"
              />
            )}
            {q.type === "essay" && <span className="text-[11px] text-slate-500">tự luận</span>}
          </div>
        ))}
      </div>
    </div>
  );
}

type TagAuditLite = ReturnType<typeof auditQuestionTags>;

function TagGrid({
  questions,
  enabled,
  groups,
  lessonPicked,
  audit,
  onTag,
  onTagMany,
}: {
  questions: ExamQuestion[];
  enabled: boolean;
  groups: TopicGroup[];
  lessonPicked: boolean;
  audit: TagAuditLite;
  onTag: (i: number, field: TagField, value: string) => void;
  onTagMany: (indexes: number[], field: TagField, value: string) => void;
}) {
  const toast = useToast();
  const [open, setOpen] = useState(true);
  const [aiBusy, setAiBusy] = useState(false);
  const known = useMemo(() => new Set(groups.flatMap((g) => g.names).map((n) => n.toLowerCase())), [groups]);
  const untaggedTopic = questions.map((_, i) => i).filter((i) => !(questions[i].topic ?? "").trim());
  const untaggedForm = questions.map((_, i) => i).filter((i) => !questions[i].form);
  // Bài đang chọn luôn đứng đầu `groups` (composer xếp "mine" trước — xem AzotaExamComposer/LessonImporter),
  // nên khi đã chọn bài, groups[0] chính là danh mục YCCĐ đúng của bài đó.
  const aiCandidates = lessonPicked ? (groups[0]?.names ?? []) : [];
  const aiTargets = useMemo(
    () => Array.from(new Set([...untaggedTopic, ...untaggedForm])).sort((a, b) => a - b),
    [untaggedTopic, untaggedForm],
  );
  const aiAvailable = enabled && aiCandidates.length > 0 && aiTargets.length > 0;

  async function runAutoTag() {
    if (!aiAvailable || aiBusy) return;
    setAiBusy(true);
    try {
      const items = aiTargets.map((i) => ({ index: i, text: questionTextForAi(questions[i]) }));
      const results = await classifyQuestionTags(aiCandidates, items);
      for (const r of results) {
        if (r.topic) onTag(r.index, "topic", r.topic);
        if (r.form) onTag(r.index, "form", QUESTION_FORM_LABELS[r.form].toLowerCase());
      }
      toast(
        results.length > 0 ? "success" : "error",
        results.length > 0 ? `AI đã gắn nhãn cho ${results.length}/${aiTargets.length} câu.` : "AI không gắn được nhãn nào — thử lại hoặc gắn tay.",
      );
    } catch (e) {
      toast("error", e instanceof Error ? e.message : String(e));
    } finally {
      setAiBusy(false);
    }
  }

  const selectCls =
    "h-7 max-w-full rounded border border-white/10 bg-panel px-1 text-[11px] text-slate-200 focus:border-primary focus:outline-none disabled:cursor-default disabled:opacity-60";

  function renderOptions(current: string) {
    const extra = current && !known.has(current.toLowerCase()) ? current : "";
    return (
      <>
        <option value="">— chưa gắn —</option>
        {extra && <option value={extra}>{extra} (không có trong danh mục)</option>}
        {groups.map((g) => (
          <optgroup key={g.parent.id} label={g.parent.name}>
            {g.names.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </optgroup>
        ))}
      </>
    );
  }

  return (
    <div className="admin-card">
      <div className="flex w-full items-center gap-2 text-xs">
        <button type="button" onClick={() => setOpen((o) => !o)} className="flex items-center gap-2 text-left">
          <span className="font-semibold text-slate-400">Phân loại câu — yêu cầu cần đạt & dạng</span>
          <span className={audit.tagged === audit.total ? "text-emerald-300" : "text-amber-300"}>
            {audit.tagged}/{audit.total} câu đã gắn đủ
          </span>
          {audit.unknown.length > 0 && (
            <span className="text-amber-300">· {audit.unknown.length} chủ đề không có trong danh mục</span>
          )}
        </button>
        <div className="ml-auto flex items-center gap-2">
          {aiAvailable && (
            <button
              type="button"
              onClick={runAutoTag}
              disabled={aiBusy}
              className="inline-flex items-center gap-1 rounded-lg bg-primary/20 px-2 py-1 text-[11px] font-semibold text-primary hover:bg-primary/30 disabled:opacity-50"
            >
              <Sparkles size={12} /> {aiBusy ? "Đang phân loại…" : `AI gắn nhãn (${aiTargets.length} câu)`}
            </button>
          )}
          <button type="button" onClick={() => setOpen((o) => !o)} className="text-slate-500 hover:text-slate-300">
            {open ? "thu gọn" : "mở"}
          </button>
        </div>
      </div>
      {open && (
        <div className="mt-2 space-y-2">
          {groups.length === 0 ? (
            <p className="text-[11px] text-slate-500">
              {lessonPicked
                ? "Khối này chưa có danh mục yêu cầu cần đạt — thêm ở trang Chủ đề câu hỏi, hoặc gõ dòng “Chủ đề: …” trong văn bản."
                : "Chọn Lớp – Bài để hiện danh sách yêu cầu cần đạt của bài."}
            </p>
          ) : (
            !lessonPicked && (
              <p className="text-[11px] text-slate-500">Chọn Bài để yêu cầu cần đạt của bài đó lên đầu danh sách.</p>
            )
          )}
          {enabled && questions.length > 0 && (
            <div className="flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
              {untaggedTopic.length > 0 && groups.length > 0 && (
                <label className="inline-flex items-center gap-1">
                  {untaggedTopic.length} câu chưa có chủ đề →
                  <select
                    value=""
                    onChange={(e) => e.target.value && onTagMany(untaggedTopic, "topic", e.target.value)}
                    className={selectCls}
                  >
                    {renderOptions("")}
                  </select>
                </label>
              )}
              {untaggedForm.length > 0 && (
                <span className="inline-flex items-center gap-1">
                  {untaggedForm.length} câu chưa có dạng →
                  {(["ly_thuyet", "bai_tap"] as QuestionForm[]).map((f) => (
                    <button
                      key={f}
                      type="button"
                      onClick={() => onTagMany(untaggedForm, "form", QUESTION_FORM_LABELS[f].toLowerCase())}
                      className="rounded bg-white/10 px-2 py-0.5 font-semibold text-slate-200 hover:bg-white/20"
                    >
                      {QUESTION_FORM_LABELS[f]}
                    </button>
                  ))}
                </span>
              )}
            </div>
          )}
          <div className="grid gap-1">
            {questions.map((q, i) => {
              const topic = (q.topic ?? "").trim();
              const unknown = !!topic && !known.has(topic.toLowerCase());
              return (
                <div key={i} className="grid grid-cols-[1.5rem_minmax(0,1fr)_auto] items-center gap-1">
                  <span className="text-right text-[11px] font-bold text-slate-400">{i + 1}</span>
                  <select
                    value={topic}
                    disabled={!enabled}
                    title={unknown ? "Tên này không có trong danh mục — sẽ lưu nguyên văn" : topic}
                    onChange={(e) => onTag(i, "topic", e.target.value)}
                    className={`${selectCls} w-full ${unknown ? "border-amber-500/50" : ""}`}
                  >
                    {renderOptions(topic)}
                  </select>
                  <div className="flex gap-0.5">
                    {(["ly_thuyet", "bai_tap"] as QuestionForm[]).map((f) => (
                      <button
                        key={f}
                        type="button"
                        disabled={!enabled}
                        onClick={() => onTag(i, "form", q.form === f ? "" : QUESTION_FORM_LABELS[f].toLowerCase())}
                        className={`h-7 rounded px-1.5 text-[11px] font-bold transition disabled:cursor-default ${
                          q.form === f ? "bg-blue-500 text-white" : "bg-white/5 text-slate-300 hover:bg-white/15"
                        }`}
                      >
                        {f === "ly_thuyet" ? "LT" : "BT"}
                      </button>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
          {!enabled && questions.length > 0 && (
            <p className="text-[11px] text-slate-500">
              Đang ở chế độ sửa chi tiết hoặc số câu chưa khớp — gắn nhãn trong từng thẻ câu bên dưới.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

function PreviewCard({ index, q, fix }: { index: number; q: ExamQuestion; fix: (html: string) => string }) {
  const issues = problems(q);
  return (
    <div className={`rounded-2xl border bg-panel p-4 ${issues.length ? "border-amber-500/40" : "border-white/10"}`}>
      <div className="mb-2 flex flex-wrap items-center gap-2 text-xs">
        <span className="font-bold text-primary">Câu {index}</span>
        <span className="text-slate-500">
          {q.type === "multiple_choice" ? "Trắc nghiệm" : q.type === "true_false" ? "Đúng – Sai" : q.type === "short_answer" ? "Trả lời ngắn" : "Tự luận"}
        </span>
        {q.topic && <span className="rounded-full bg-white/10 px-2 py-0.5 text-slate-300">{q.topic}</span>}
        {q.form && <span className="rounded-full bg-blue-500/15 px-2 py-0.5 text-blue-200">{QUESTION_FORM_LABELS[q.form]}</span>}
        {issues.length > 0 && <span className="ml-auto text-amber-300">{issues.join(" · ")}</span>}
      </div>
      <ContentHtml html={fix(q.question)} className="text-sm text-slate-200" />
      {q.type === "multiple_choice" && (
        <ul className="mt-2 grid gap-1 sm:grid-cols-2">
          {q.options.map((o, j) => (
            <li
              key={j}
              className={`flex gap-2 rounded-lg px-2 py-1 text-sm ${
                q.answer === j ? "bg-emerald-500/15 text-emerald-200" : "text-slate-300"
              }`}
            >
              <b>{LETTERS[j]}.</b>
              <ContentHtml html={fix(o)} />
            </li>
          ))}
        </ul>
      )}
      {q.type === "true_false" && (
        <ul className="mt-2 space-y-1">
          {q.statements.map((s, j) => (
            <li key={j} className="flex gap-2 text-sm text-slate-300">
              <b className={`w-5 shrink-0 ${s.answer ? "text-emerald-300" : "text-red-300"}`}>{s.answer ? "Đ" : "S"}</b>
              <span className="shrink-0 font-semibold">{["a", "b", "c", "d"][j]})</span>
              <ContentHtml html={fix(s.text)} />
            </li>
          ))}
        </ul>
      )}
      {q.type === "short_answer" && (
        <p className="mt-2 text-sm text-slate-300">
          Đáp án: <b className="text-emerald-300">{q.answer || "—"}</b>
        </p>
      )}
      {q.explanation.trim() && (
        <details className="mt-2 text-xs text-slate-400">
          <summary className="cursor-pointer hover:text-slate-200">Lời giải</summary>
          <ContentHtml html={fix(q.explanation)} className="mt-1" />
        </details>
      )}
    </div>
  );
}
