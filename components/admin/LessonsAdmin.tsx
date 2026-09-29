"use client";

import { useCallback, useEffect, useState } from "react";
import { ChevronDown } from "lucide-react";
import ExamPicker from "@/components/admin/ExamPicker";
import LaTexEditor from "@/components/admin/LaTexEditor";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion, SchoolClass } from "@/features/exams/types";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import {
  LESSON_KIND_META,
  SECTION_META,
  SECTION_ORDER,
  isExamKind,
  isPeriodicExam,
  type Chapter,
  type Lesson,
  type LessonItem,
  type LessonItemKind,
  type LessonKind,
  type LessonWorkedQuestion,
} from "@/features/lessons/types";

const LESSON_KIND_OPTIONS: LessonKind[] = [
  "bai_hoc",
  "kiem_tra_chuong",
  "kiem_tra_giua_ki",
  "kiem_tra_cuoi_ki",
];
import {
  classGrade,
  displayClassesByGrade,
  expandClassIdsByGrade,
  fetchClasses,
  setItemClasses,
} from "@/services/classes";
import { fetchChapters, fetchLessonItems, fetchLessons } from "@/services/lessons";
import { getSupabase } from "@/services/supabase";
import { academicSubject, subjectsForGrade } from "@/services/academic-subjects";
import {
  fetchLessonPracticeWrongest,
  type LessonPracticeWrongQuestion,
} from "@/services/analytics";

const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const chipBtn =
  "admin-chip";

// PostgREST báo lỗi này khi cột chưa tồn tại (migration nháp/đăng chưa chạy) — dùng để
// lùi về lưu thẳng cột sống thay vì chặn admin soạn bài trong lúc chờ Thạch chạy migration.
function isMissingColumnError(error: { message: string } | null): boolean {
  return !!error && error.message.toLowerCase().includes("schema cache");
}

/** ISO -> "YYYY-MM-DDTHH:mm" theo giờ máy, cho <input type="datetime-local">. */
function toLocalInput(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

// ---------- Form thêm/sửa 1 mục trong bài học ----------
function ItemForm({
  lessonId,
  item,
  nextSort,
  onSaved,
  onCancel,
}: {
  lessonId: number;
  item: LessonItem | null;
  nextSort: number;
  onSaved: () => void;
  onCancel: () => void;
}) {
  const toast = useToast();
  // Đang sửa 1 mục đã đăng mà còn nháp dở → soạn tiếp từ nháp, không phải từ bản đã đăng.
  const draft = item?.draft_payload ?? null;
  const initial = draft ?? item;
  const [kind, setKind] = useState<LessonItemKind>(initial?.kind ?? "ly_thuyet");
  const [title, setTitle] = useState(initial?.title ?? "");
  const [subtitle, setSubtitle] = useState(initial?.subtitle ?? "");
  const [videoUrl, setVideoUrl] = useState(initial?.video_url ?? "");
  const [pdfUrl, setPdfUrl] = useState(initial?.pdf_url ?? "");
  const [bodyHtml, setBodyHtml] = useState(initial?.body_html ?? "");
  const [examIds, setExamIds] = useState<number[]>(initial?.exam_ids ?? []);
  const [questions, setQuestions] = useState<LessonWorkedQuestion[]>(
    initial?.questions ?? [],
  );
  // datetime-local cần chuỗi "YYYY-MM-DDTHH:mm" theo giờ máy
  const [dueAt, setDueAt] = useState(toLocalInput(initial?.due_at ?? null));
  const [busy, setBusy] = useState(false);

  const examKind = isExamKind(kind);
  const isVideoKind = kind === "video";
  const isWorkedKind = kind === "bai_tap_mau";
  const isHomework = kind === "bai_tap_ve_nha";
  const hasDraft = draft !== null;
  const neverPublished = item !== null && item.published_at === null;

  function updateQuestion(idx: number, patch: Partial<LessonWorkedQuestion>) {
    setQuestions((current) =>
      current.map((q, i) => (i === idx ? { ...q, ...patch } : q)),
    );
  }

  function removeQuestion(idx: number) {
    setQuestions((current) => current.filter((_, i) => i !== idx));
  }

  // Nội dung đang soạn — dùng chung cho cả "Lưu nháp" (ghi vào draft_payload, jsonb nên
  // due_at luôn gửi được) lẫn "Đăng chính thức" (ghi thẳng vào các cột sống).
  function buildContent() {
    return {
      kind,
      title: title.trim(),
      subtitle: subtitle.trim(),
      body_html: kind === "ly_thuyet" ? bodyHtml : "",
      video_url: isVideoKind ? videoUrl.trim() : "",
      pdf_url: examKind ? "" : pdfUrl.trim(),
      exam_ids: examKind ? examIds : [],
      questions: isWorkedKind ? questions.filter((q) => q.body_html.trim() !== "") : [],
      due_at: isHomework ? (dueAt ? new Date(dueAt).toISOString() : null) : null,
    };
  }

  // Cùng nội dung trên nhưng cho các cột sống của lesson_items — chỉ gửi due_at khi là
  // bài tập về nhà, để mục kiểu cũ vẫn lưu được khi DB chưa chạy migration v4 (cột due_at).
  function buildLivePayload() {
    const content = buildContent();
    return {
      kind: content.kind,
      title: content.title,
      subtitle: content.subtitle,
      body_html: content.body_html,
      video_url: content.video_url,
      pdf_url: content.pdf_url,
      exam_ids: content.exam_ids,
      questions: content.questions,
      lesson_id: lessonId,
      sort_order: item?.sort_order ?? nextSort,
      ...(isHomework ? { due_at: content.due_at } : {}),
    };
  }

  async function saveDraft() {
    if (!title.trim()) {
      toast("error", "Mục cần có tiêu đề.");
      return;
    }
    setBusy(true);
    const supabase = getSupabase();
    const attempt = item
      ? await supabase
          .from("lesson_items")
          .update({ draft_payload: buildContent(), draft_saved_at: new Date().toISOString() })
          .eq("id", item.id)
      : await supabase.from("lesson_items").insert({ ...buildLivePayload(), published_at: null });
    // DB chưa chạy migration nháp/đăng (docs/supabase-migration-lesson-item-draft-publish.sql,
    // xem cột published_at/draft_payload) → lùi về lưu thẳng vào cột sống như "Lưu mục" cũ,
    // để soạn bài không bị chặn hoàn toàn trong lúc chờ Thạch chạy migration.
    const error = isMissingColumnError(attempt.error)
      ? (item
          ? await supabase.from("lesson_items").update(buildLivePayload()).eq("id", item.id)
          : await supabase.from("lesson_items").insert(buildLivePayload())
        ).error
      : attempt.error;
    setBusy(false);
    if (error) {
      toast("error", error.message);
      return;
    }
    toast(
      "success",
      isMissingColumnError(attempt.error)
        ? "DB chưa có cột nháp — đã lưu thẳng, học sinh thấy ngay."
        : "Đã lưu nháp — học sinh chưa thấy thay đổi này.",
    );
    onSaved();
  }

  async function publish() {
    if (!title.trim()) {
      toast("error", "Mục cần có tiêu đề.");
      return;
    }
    if (item && !neverPublished && !confirm("Đăng nội dung này cho học sinh xem ngay?")) return;
    setBusy(true);
    const supabase = getSupabase();
    const attempt = item
      ? await supabase
          .from("lesson_items")
          .update({
            ...buildLivePayload(),
            published_at: item.published_at ?? new Date().toISOString(),
            draft_payload: null,
            draft_saved_at: null,
          })
          .eq("id", item.id)
      : await supabase
          .from("lesson_items")
          .insert({ ...buildLivePayload(), published_at: new Date().toISOString() });
    const error = isMissingColumnError(attempt.error)
      ? (item
          ? await supabase.from("lesson_items").update(buildLivePayload()).eq("id", item.id)
          : await supabase.from("lesson_items").insert(buildLivePayload())
        ).error
      : attempt.error;
    setBusy(false);
    if (error) {
      toast("error", error.message);
      return;
    }
    toast("success", "Đã đăng chính thức.");
    onSaved();
  }

  async function discardDraft() {
    if (!item || !confirm("Bỏ bản nháp đang sửa, quay về bản đã đăng?")) return;
    setBusy(true);
    const { error } = await getSupabase()
      .from("lesson_items")
      .update({ draft_payload: null, draft_saved_at: null })
      .eq("id", item.id);
    setBusy(false);
    if (error) {
      toast("error", error.message);
      return;
    }
    toast("success", "Đã hủy bản nháp.");
    onSaved();
  }

  return (
    <div className="admin-card admin-card--accent space-y-3">
      {!item && (
        <p className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-2 text-xs text-amber-200">
          🕓 Mục mới — bấm &quot;Lưu nháp&quot; để lưu tạm (học sinh chưa thấy), hoặc &quot;Đăng chính thức&quot; để hiện ngay.
        </p>
      )}
      {item && neverPublished && (
        <p className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-2 text-xs text-amber-200">
          🕓 Mục này chưa từng đăng — học sinh chưa thấy.
        </p>
      )}
      {item && !neverPublished && hasDraft && (
        <p className="rounded-lg border border-blue-500/30 bg-blue-500/5 p-2 text-xs text-blue-200">
          📝 Đang sửa bản nháp (lưu lúc {item.draft_saved_at ? new Date(item.draft_saved_at).toLocaleString("vi-VN") : "?"}) —
          học sinh vẫn thấy bản cũ cho tới khi bấm &quot;Đăng chính thức&quot;.
        </p>
      )}
      <div className="flex flex-wrap items-center gap-3">
        <select
          value={kind}
          onChange={(e) => setKind(e.target.value as LessonItemKind)}
          className={`${inputCls} bg-panel`}
        >
          {SECTION_ORDER.map((k) => (
            <option key={k} value={k}>
              {SECTION_META[k].icon} {SECTION_META[k].label}
            </option>
          ))}
        </select>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Tiêu đề mục, vd Lý thuyết trọng tâm"
          className={`${inputCls} min-w-60 flex-1`}
        />
        <input
          value={subtitle}
          onChange={(e) => setSubtitle(e.target.value)}
          placeholder="Phụ đề (không bắt buộc)"
          className={`${inputCls} min-w-40 flex-1`}
        />
      </div>

      {isVideoKind && (
        <input
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
          placeholder="Link YouTube, vd https://youtu.be/…"
          className={`${inputCls} w-full`}
        />
      )}
      {!examKind && (
        <input
          value={pdfUrl}
          onChange={(e) => setPdfUrl(e.target.value)}
          placeholder="Link PDF (không bắt buộc)"
          className={`${inputCls} w-full`}
        />
      )}
      {kind === "ly_thuyet" && (
        <LaTexEditor
          value={bodyHtml}
          onChange={(html) => setBodyHtml(html)}
          placeholder="Nội dung (viết LaTeX hoặc HTML)"
        />
      )}
      {isHomework && (
        <label className="flex flex-wrap items-center gap-2 text-sm text-slate-300">
          Hạn nộp
          <input
            type="datetime-local"
            value={dueAt}
            onChange={(e) => setDueAt(e.target.value)}
            className={`${inputCls} bg-panel`}
          />
          {dueAt && (
            <button onClick={() => setDueAt("")} className={chipBtn}>
              Bỏ hạn nộp
            </button>
          )}
        </label>
      )}
      {isWorkedKind && (
        <div className="space-y-3">
          <p className="text-xs text-slate-400">
            Dạng bài tự luận (kiểu cũ, chỉ hiện lời giải) — bài tập mẫu có chấm đáp án thì
            gắn đề ở dưới.
          </p>
          {questions.map((q, idx) => (
            <div key={idx} className="space-y-2 rounded-xl border border-white/10 bg-white/5 p-3">
              <div className="flex items-center gap-2">
                <input
                  value={q.label}
                  onChange={(e) => updateQuestion(idx, { label: e.target.value })}
                  placeholder='Nhãn ngắn, vd "TL" hoặc "Dạng cơ bản"'
                  className={`${inputCls} flex-1`}
                />
                <button
                  onClick={() => removeQuestion(idx)}
                  className="admin-chip admin-chip--danger"
                >
                  Xóa
                </button>
              </div>
              <LaTexEditor
                value={q.body_html}
                onChange={(html) => updateQuestion(idx, { body_html: html })}
                placeholder="Đề bài + lời giải mẫu (viết LaTeX hoặc HTML)"
              />
            </div>
          ))}
          <button
            onClick={() => setQuestions((current) => [...current, { label: "", body_html: "" }])}
            className={chipBtn}
          >
            + Thêm dạng bài
          </button>
        </div>
      )}
      {examKind && (
        <div className="space-y-1">
          {isWorkedKind && (
            <p className="text-xs text-slate-400">
              Đề gắn ở đây hiện thành từng bài mẫu: em chọn đáp án, bấm &quot;Kiểm tra&quot;
              mới mở lời giải chi tiết.
            </p>
          )}
          {kind === "luyen_tap" && (
            <p className="text-xs text-slate-400">
              Toàn bộ câu của các đề gắn ở đây gộp thành ngân hàng để bốc ngẫu nhiên.
            </p>
          )}
          <ExamPicker value={examIds} onChange={setExamIds} />
        </div>
      )}
      {kind === "luyen_tap" && item && (
        <PracticeWrongestPanel itemId={item.id} />
      )}

      <div className="flex flex-wrap gap-2">
        <button
          onClick={publish}
          disabled={busy}
          className="admin-btn admin-btn--primary disabled:opacity-50"
        >
          🚀 Đăng chính thức
        </button>
        <button
          onClick={saveDraft}
          disabled={busy}
          className="rounded-full border border-white/15 px-5 py-2 text-sm text-slate-300 hover:border-white/30 disabled:opacity-50"
        >
          💾 Lưu nháp
        </button>
        {hasDraft && (
          <button
            onClick={discardDraft}
            disabled={busy}
            className="admin-chip admin-chip--danger disabled:opacity-50"
          >
            Hủy nháp
          </button>
        )}
        <button
          onClick={onCancel}
          className="rounded-full border border-white/15 px-5 py-2 text-sm text-slate-300 hover:border-white/30"
        >
          Hủy
        </button>
      </div>
    </div>
  );
}

function practiceFormLabel(form: string) {
  return form === "ly_thuyet" || form === "bai_tap"
    ? QUESTION_FORM_LABELS[form]
    : "—";
}

/** Tổng hợp câu học sinh hay sai trong ngân hàng của một mục Luyện tập — gộp mọi lớp đã làm. */
function PracticeWrongestPanel({ itemId }: { itemId: number }) {
  const [rows, setRows] = useState<LessonPracticeWrongQuestion[] | null>(null);
  const [openKey, setOpenKey] = useState<string | null>(null);
  const [questionsByExam, setQuestionsByExam] = useState<Record<number, ExamQuestion[]>>({});

  useEffect(() => {
    setRows(null);
    setOpenKey(null);
    fetchLessonPracticeWrongest(itemId)
      .then(setRows)
      .catch(() => setRows([]));
  }, [itemId]);

  async function toggle(row: LessonPracticeWrongQuestion) {
    const key = `${row.examId}|${row.sourceIndex}`;
    if (openKey === key) {
      setOpenKey(null);
      return;
    }
    setOpenKey(key);
    if (!questionsByExam[row.examId]) {
      const { data } = await getSupabase()
        .from("exams")
        .select("questions")
        .eq("id", row.examId)
        .single();
      setQuestionsByExam((cur) => ({
        ...cur,
        [row.examId]: (data?.questions as ExamQuestion[]) ?? [],
      }));
    }
  }

  return (
    <div className="space-y-2 rounded-xl border border-white/10 bg-white/5 p-3">
      <p className="text-sm font-semibold text-white">Câu học sinh hay sai</p>
      <p className="text-xs text-slate-400">
        Gộp mọi lượt làm của mọi lớp trên các đề gắn ở trên — dùng để biết câu nào trong
        ngân hàng cần xem lại đề bài hoặc dạy lại.
      </p>
      {rows === null ? (
        <p className="text-xs text-slate-500">Đang tải…</p>
      ) : rows.length === 0 ? (
        <p className="text-xs text-slate-500">Chưa có dữ liệu (chưa có học sinh nào làm).</p>
      ) : (
        <div className="space-y-1.5">
          {rows.slice(0, 10).map((row) => {
            const key = `${row.examId}|${row.sourceIndex}`;
            const question = questionsByExam[row.examId]?.[row.sourceIndex];
            return (
              <div key={key} className="rounded-lg border border-white/10 bg-panel">
                <button
                  type="button"
                  onClick={() => toggle(row)}
                  className="flex w-full items-center gap-3 p-3 text-left"
                >
                  <span className="min-w-0 flex-1">
                    <span className="block text-sm text-white">
                      {row.examTitle} · Câu {row.sourceIndex + 1}
                      <span className="ml-2 font-normal text-slate-400">
                        {row.topic} · {practiceFormLabel(row.form)}
                      </span>
                    </span>
                  </span>
                  <span className="shrink-0 text-right">
                    <span
                      className={`font-mono text-sm font-bold ${row.pct >= 60 ? "text-red-300" : row.pct >= 30 ? "text-amber-300" : "text-slate-300"}`}
                    >
                      {row.pct}%
                    </span>
                    <span className="ml-2 text-xs text-slate-500">
                      {row.wrong}/{row.total}
                    </span>
                  </span>
                  <ChevronDown
                    size={14}
                    className={`shrink-0 text-slate-500 transition-transform ${openKey === key ? "rotate-180" : ""}`}
                  />
                </button>
                {openKey === key && question && (
                  <div className="border-t border-white/10 p-3 text-sm text-slate-300">
                    <ContentHtml html={question.question} className="exam-content block" />
                    {question.type === "multiple_choice" && (
                      <ul className="mt-2 space-y-1 text-xs">
                        {(question as { options: string[]; answer: number }).options.map(
                          (opt, oi) => (
                            <li
                              key={oi}
                              className={
                                oi === (question as { answer: number }).answer
                                  ? "text-emerald-300"
                                  : "text-slate-500"
                              }
                            >
                              {"ABCD"[oi]}. <ContentHtml html={opt} />
                            </li>
                          ),
                        )}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ---------- Quản lý mục của 1 bài học ----------
function LessonItemsEditor({ lesson, onBack }: { lesson: Lesson; onBack: () => void }) {
  const toast = useToast();
  const [items, setItems] = useState<LessonItem[]>([]);
  const [editing, setEditing] = useState<LessonItem | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    fetchLessonItems(lesson.id).then(setItems);
  }, [lesson.id]);
  useEffect(reload, [reload]);


  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= items.length) return;
    const a = items[idx];
    const b = items[other];
    const supabase = getSupabase();
    await supabase.from("lesson_items").update({ sort_order: b.sort_order }).eq("id", a.id);
    await supabase.from("lesson_items").update({ sort_order: a.sort_order }).eq("id", b.id);
    reload();
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <button onClick={onBack} className={chipBtn}>
          ← Quay lại
        </button>
        <h3 className="admin-h2">{lesson.title}</h3>
        {!adding && !editing && (
          <button
            onClick={() => setAdding(true)}
            className="ml-auto admin-btn admin-btn--primary"
          >
            + Thêm mục
          </button>
        )}
      </div>

      {(adding || editing) && (
        <ItemForm
          lessonId={lesson.id}
          item={editing}
          nextSort={items.length + 1}
          onSaved={() => {
            setAdding(false);
            setEditing(null);
            reload();
          }}
          onCancel={() => {
            setAdding(false);
            setEditing(null);
          }}
        />
      )}

      <div className="space-y-2">
        {items.map((it, idx) => {
          const meta = SECTION_META[it.kind];
          const neverPublished = it.published_at === null;
          return (
            <div
              key={it.id}
              className={`admin-card admin-card--row ${neverPublished ? "opacity-50" : ""}`}
            >
              <span title={meta.label}>{meta.icon}</span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-medium text-white">
                  {it.title}
                </span>
                <span className="text-xs" style={{ color: meta.color }}>
                  {meta.label}
                  {it.exam_ids.length > 0 && ` · ${it.exam_ids.length} đề`}
                  {it.questions.length > 0 && ` · ${it.questions.length} dạng bài`}
                  {it.video_url && " · video"}
                  {it.pdf_url && " · PDF"}
                  {neverPublished && " · 🕓 chưa đăng"}
                  {!neverPublished && it.draft_payload && " · 📝 có nháp chưa đăng"}
                </span>
              </span>
              <span className="flex items-center gap-1">
                <button onClick={() => move(idx, -1)} title="Lên" className={chipBtn}>
                  ↑
                </button>
                <button onClick={() => move(idx, 1)} title="Xuống" className={chipBtn}>
                  ↓
                </button>
                <button
                  onClick={() => {
                    setAdding(false);
                    setEditing(it);
                  }}
                  className="admin-chip"
                >
                  Sửa
                </button>
                <button
                  onClick={async () => {
                    if (!confirm(`Xóa mục "${it.title}"?`)) return;
                    const { error } = await getSupabase()
                      .from("lesson_items")
                      .delete()
                      .eq("id", it.id);
                    if (error) {
                      toast("error", error.message);
                      return;
                    }
                    toast("success", "Đã xóa mục.");
                    reload();
                  }}
                  className="admin-chip admin-chip--danger"
                >
                  Xóa
                </button>
              </span>
            </div>
          );
        })}
        {items.length === 0 && !adding && (
          <p className="text-sm text-slate-400">
            Chưa có mục nào — bấm “+ Thêm mục” để soạn lý thuyết, video, đề…
          </p>
        )}
      </div>
    </div>
  );
}

// ---------- Mô tả ngắn (yêu cầu cần đạt) của 1 bài học, hiện dưới tên bài ----------
function LessonDescriptionField({ lesson, onSaved }: { lesson: Lesson; onSaved: () => void }) {
  const toast = useToast();
  const [value, setValue] = useState(lesson.description);
  const [busy, setBusy] = useState(false);
  const dirty = value !== lesson.description;

  async function save() {
    setBusy(true);
    const { error } = await getSupabase()
      .from("lessons")
      .update({ description: value.trim() })
      .eq("id", lesson.id);
    setBusy(false);
    if (error) {
      toast("error", error.message);
      return;
    }
    onSaved();
  }

  return (
    <div className="flex items-center gap-2 pl-8">
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Yêu cầu cần đạt (hiện ngắn gọn dưới tên bài)"
        className={`${inputCls} flex-1 text-xs`}
      />
      {dirty && (
        <button onClick={save} disabled={busy} className="admin-chip disabled:opacity-50">
          Lưu
        </button>
      )}
    </div>
  );
}

// ---------- Quản lý bài học của 1 chương ----------
function ChapterLessonsEditor({
  chapter,
  schoolClass,
  onBack,
}: {
  chapter: Chapter;
  schoolClass: SchoolClass | null;
  onBack: () => void;
}) {
  const toast = useToast();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [openLesson, setOpenLesson] = useState<Lesson | null>(null);
  const [title, setTitle] = useState("");
  const [lessonKind, setLessonKind] = useState<LessonKind>("bai_hoc");

  const reload = useCallback(() => {
    fetchLessons(true).then((ls) =>
      setLessons(ls.filter((l) => l.chapter_id === chapter.id)),
    );
  }, [chapter.id]);
  useEffect(reload, [reload]);

  if (openLesson)
    return <LessonItemsEditor lesson={openLesson} onBack={() => setOpenLesson(null)} />;

  async function addLesson(e: React.FormEvent) {
    e.preventDefault();
    const finalTitle =
      title.trim() ||
      (isPeriodicExam(lessonKind) ? LESSON_KIND_META[lessonKind].label : "");
    if (!finalTitle) return;
    const { error } = await getSupabase().from("lessons").insert({
      chapter_id: chapter.id,
      title: finalTitle,
      lesson_kind: lessonKind,
      sort_order: lessons.length + 1,
    });
    if (error) {
      toast("error", error.message);
      return;
    }
    toast("success", "Đã thêm bài học.");
    setTitle("");
    setLessonKind("bai_hoc");
    reload();
  }

  async function setKind(lesson: Lesson, kind: LessonKind) {
    const { error } = await getSupabase()
      .from("lessons")
      .update({ lesson_kind: kind })
      .eq("id", lesson.id);
    if (error) {
      toast("error", error.message);
      return;
    }
    reload();
  }

  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= lessons.length) return;
    const a = lessons[idx];
    const b = lessons[other];
    const supabase = getSupabase();
    await supabase.from("lessons").update({ sort_order: b.sort_order }).eq("id", a.id);
    await supabase.from("lessons").update({ sort_order: a.sort_order }).eq("id", b.id);
    reload();
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <button onClick={onBack} className={chipBtn}>
          ← Chọn chương khác
        </button>
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-[#60A5FA]">
            {schoolClass ? `Lớp ${schoolClass.name}` : "Toàn trường"}
          </p>
          <h3 className="truncate admin-h2">
            {chapter.title}
          </h3>
        </div>
      </div>

      <form onSubmit={addLesson} className="flex flex-wrap gap-3">
        <select
          value={lessonKind}
          onChange={(e) => setLessonKind(e.target.value as LessonKind)}
          className={`${inputCls} bg-panel`}
        >
          {LESSON_KIND_OPTIONS.map((k) => (
            <option key={k} value={k}>
              {LESSON_KIND_META[k].icon} {LESSON_KIND_META[k].label}
            </option>
          ))}
        </select>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder={
            isPeriodicExam(lessonKind)
              ? `Tên bài (bỏ trống = "${LESSON_KIND_META[lessonKind].label}")`
              : "Tên bài học, vd Giá trị lượng giác của góc lượng giác"
          }
          className={`${inputCls} min-w-72 flex-1`}
        />
        <button
          type="submit"
          className="admin-btn admin-btn--primary"
        >
          + Thêm bài
        </button>
      </form>
      {isPeriodicExam(lessonKind) && (
        <p className="-mt-1 text-xs text-slate-500">
          Bài kiểm tra định kỳ: đặt ở cuối chương tương ứng chương trình, chỉ cần
          soạn mục “Kiểm tra” và gắn đề — hệ thống chấm điểm tự động. Riêng kiểm tra
          giữa/cuối học kì sẽ tách khỏi chương, hiện thành mục riêng ngay sau chương
          được gắn (vd gắn vào chương 1 lớp 12 để ra “Kiểm tra giữa học kì 1”).
        </p>
      )}

      <div className="space-y-2">
        {lessons.map((l, idx) => (
          <div
            key={l.id}
            className={`admin-card space-y-2 ${l.published ? "" : "opacity-50"}`}
          >
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => setOpenLesson(l)}
                className="min-w-0 flex-1 text-left"
              >
                <span className="flex items-center gap-2">
                  {isPeriodicExam(l.lesson_kind) && (
                    <span
                      className="shrink-0 rounded-full px-2 py-0.5 text-[10px] font-bold tracking-wide"
                      style={{
                        color: LESSON_KIND_META[l.lesson_kind].color,
                        backgroundColor: `${LESSON_KIND_META[l.lesson_kind].color}22`,
                      }}
                    >
                      {LESSON_KIND_META[l.lesson_kind].badge}
                    </span>
                  )}
                  <span className="truncate font-medium text-white hover:text-primary">
                    {l.title}
                  </span>
                </span>
                <span className="text-xs text-slate-500">{l.itemCount} mục</span>
              </button>
              <span className="flex flex-wrap items-center gap-1">
                <select
                  value={l.lesson_kind}
                  onChange={(e) => setKind(l, e.target.value as LessonKind)}
                  title="Loại bài"
                  className="rounded-lg border border-white/10 bg-panel px-2 py-1 text-xs text-slate-300"
                >
                  {LESSON_KIND_OPTIONS.map((k) => (
                    <option key={k} value={k}>
                      {LESSON_KIND_META[k].icon} {LESSON_KIND_META[k].label}
                    </option>
                  ))}
                </select>
                <button onClick={() => move(idx, -1)} title="Lên" className={chipBtn}>
                  ↑
                </button>
                <button onClick={() => move(idx, 1)} title="Xuống" className={chipBtn}>
                  ↓
                </button>
                <button
                  onClick={async () => {
                    await getSupabase()
                      .from("lessons")
                      .update({ published: !l.published })
                      .eq("id", l.id);
                    reload();
                  }}
                  className="admin-chip"
                >
                  {l.published ? "Ẩn" : "Hiện"}
                </button>
                <button
                  onClick={() => setOpenLesson(l)}
                  className="admin-chip"
                >
                  Soạn mục
                </button>
                <button
                  onClick={async () => {
                    if (!confirm(`Xóa bài "${l.title}" và toàn bộ mục bên trong?`)) return;
                    const { error } = await getSupabase()
                      .from("lessons")
                      .delete()
                      .eq("id", l.id);
                    if (error) {
                      toast("error", error.message);
                      return;
                    }
                    toast("success", "Đã xóa bài học.");
                    reload();
                  }}
                  className="admin-chip admin-chip--danger"
                >
                  Xóa
                </button>
              </span>
            </div>
            <LessonDescriptionField lesson={l} onSaved={reload} />
          </div>
        ))}
        {lessons.length === 0 && (
          <p className="text-sm text-slate-400">Chưa có bài học nào trong chương.</p>
        )}
      </div>
    </div>
  );
}

// ---------- Cấp cao nhất: danh sách chương ----------
export default function LessonsAdmin() {
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [openChapter, setOpenChapter] = useState<Chapter | null>(null);
  const [title, setTitle] = useState("");
  const [selectedClassId, setSelectedClassId] = useState<number | null>(null);
  const [selectedSubjectCode, setSelectedSubjectCode] = useState("vat-ly");

  const reload = useCallback(() => {
    fetchChapters().then(setChapters);
  }, []);
  useEffect(reload, [reload]);

  useEffect(() => {
    fetchClasses().then((items) => {
      setClasses(items);
      setSelectedClassId((current) => current ?? items[0]?.id ?? null);
    });
  }, []);

  const selectedClass =
    classes.find((schoolClass) => schoolClass.id === selectedClassId) ?? null;
  const displayClasses = displayClassesByGrade(classes);
  const visibleClassIds =
    selectedClassId === null ? [] : (expandClassIdsByGrade([selectedClassId], classes) ?? []);
  const classChapters =
    selectedClassId === null
      ? []
      : chapters.filter(
          (chapter) =>
            chapter.classIds.length === 0 ||
            chapter.classIds.some((classId) => visibleClassIds.includes(classId)),
        );
  const subjectChapters = classChapters.filter(
    (chapter) => chapter.subjectCode === selectedSubjectCode,
  );

  if (openChapter)
    return (
      <ChapterLessonsEditor
        chapter={openChapter}
        schoolClass={selectedClass}
        onBack={() => setOpenChapter(null)}
      />
    );

  async function addChapter(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedClassId) {
      toast("error", "Hãy chọn lớp trước khi thêm chương.");
      return;
    }
    if (!title.trim()) return;
    const { data, error } = await getSupabase()
      .from("chapters")
      .insert({
        title: title.trim(),
        subject_code: selectedSubjectCode,
        sort_order: subjectChapters.length + 1,
      })
      .select("id")
      .single();
    if (error || !data) {
      toast("error", error?.message ?? "Không tạo được chương.");
      return;
    }
    await setItemClasses("chapter_classes", "chapter_id", data.id, [selectedClassId]);
    toast("success", "Đã thêm chương.");
    setTitle("");
    reload();
  }

  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= subjectChapters.length) return;
    const a = subjectChapters[idx];
    const b = subjectChapters[other];
    const supabase = getSupabase();
    await supabase.from("chapters").update({ sort_order: b.sort_order }).eq("id", a.id);
    await supabase.from("chapters").update({ sort_order: a.sort_order }).eq("id", b.id);
    reload();
  }

  return (
    <div className="space-y-6">
      <section className="admin-card">
        <p className="mb-3 text-sm font-medium text-slate-300">
          1. Chọn lớp
        </p>
        <div className="flex flex-wrap gap-2">
          {displayClasses.map((schoolClass) => {
            const active = schoolClass.id === selectedClassId;
            return (
              <button
                key={schoolClass.id}
                type="button"
                onClick={() => {
                  setSelectedClassId(schoolClass.id);
                  setSelectedSubjectCode("vat-ly");
                  setOpenChapter(null);
                }}
                style={
                  active
                    ? { backgroundColor: schoolClass.color, borderColor: schoolClass.color }
                    : undefined
                }
                className={`rounded-full border px-4 py-2 text-sm font-semibold transition-colors ${
                  active
                    ? "text-white"
                    : "border-white/10 text-slate-400 hover:border-white/30 hover:text-slate-200"
                }`}
              >
                {schoolClass.icon && `${schoolClass.icon} `}
                {schoolClass.name}
              </button>
            );
          })}
          {displayClasses.length === 0 && (
            <span className="text-sm text-slate-500">
              Chưa có lớp — thêm lớp ở mục Lớp học trước.
            </span>
          )}
        </div>
      </section>

      {selectedClass && (
        <section className="admin-card">
          <p className="mb-3 text-sm font-medium text-slate-300">2. Chọn môn học</p>
          <div className="flex flex-wrap gap-2">
            {subjectsForGrade(classGrade(selectedClass.name) ?? "").map((subject) => (
              <button
                key={subject.code}
                type="button"
                onClick={() => setSelectedSubjectCode(subject.code)}
                className={`rounded-full border px-4 py-2 text-sm font-semibold ${
                  selectedSubjectCode === subject.code
                    ? "border-blue-400 bg-blue-500/15 text-blue-200"
                    : "border-white/10 text-slate-400 hover:border-white/30"
                }`}
              >
                {subject.icon} {subject.label}
              </button>
            ))}
          </div>
        </section>
      )}

      <form
        onSubmit={addChapter}
        className="admin-card space-y-4"
      >
        <div>
          <p className="text-sm font-medium text-slate-300">
            3. Thêm chương {academicSubject(selectedSubjectCode).label} cho {selectedClass ? `lớp ${selectedClass.name}` : "lớp đã chọn"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Chương mới sẽ chỉ hiện trong lớp đang chọn, sau đó admin vào chương để thêm bài học.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Tên chương, vd Chương 1: Hàm số lượng giác…"
            className={`${inputCls} min-w-72 flex-1`}
            disabled={!selectedClassId}
          />
          <button
            type="submit"
            disabled={!selectedClassId}
            className="admin-btn admin-btn--primary"
          >
            + Thêm chương
          </button>
        </div>
      </form>

      <div className="space-y-2">
        <div>
          <p className="text-sm font-medium text-slate-300">
            4. Chọn chương để đăng bài học
          </p>
          {selectedClass && (
            <p className="mt-1 text-xs text-slate-500">
              Đang xem môn {academicSubject(selectedSubjectCode).label}, lớp {selectedClass.name}.
            </p>
          )}
        </div>
        {subjectChapters.map((ch, idx) => (
          <div
            key={ch.id}
            className="admin-card admin-card--row"
          >
            <button
              onClick={() => setOpenChapter(ch)}
              className="min-w-0 flex-1 text-left"
            >
              <span className="block truncate font-medium text-white hover:text-primary">
                {ch.title}
              </span>
              <span className="text-xs text-slate-500">
                {ch.classIds.length === 0
                  ? "Toàn trường — chưa gán lớp"
                  : classes
                      .filter((c) => ch.classIds.includes(c.id))
                      .map((c) => c.name)
                      .join(", ")}
              </span>
            </button>
            <span className="flex items-center gap-1">
              {selectedClassId !== null && (
                <button
                  onClick={async () => {
                    const has = ch.classIds.includes(selectedClassId);
                    const nextIds = has
                      ? ch.classIds.filter((id) => id !== selectedClassId)
                      : [...ch.classIds, selectedClassId];
                    await setItemClasses("chapter_classes", "chapter_id", ch.id, nextIds);
                    reload();
                  }}
                  title={
                    ch.classIds.includes(selectedClassId)
                      ? `Bỏ khỏi lớp ${selectedClass?.name}`
                      : `Gán vào lớp ${selectedClass?.name}`
                  }
                  className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                    ch.classIds.includes(selectedClassId)
                      ? "border-emerald-400/40 bg-emerald-500/10 text-emerald-200"
                      : "border-white/15 text-slate-300 hover:border-white/30"
                  }`}
                >
                  {ch.classIds.includes(selectedClassId)
                    ? `✓ ${selectedClass?.name}`
                    : `+ ${selectedClass?.name}`}
                </button>
              )}
              <button onClick={() => move(idx, -1)} title="Lên" className={chipBtn}>
                ↑
              </button>
              <button onClick={() => move(idx, 1)} title="Xuống" className={chipBtn}>
                ↓
              </button>
              <button
                onClick={() => setOpenChapter(ch)}
                className="admin-chip"
              >
                Soạn bài
              </button>
              <button
                onClick={async () => {
                  if (!confirm(`Xóa chương "${ch.title}" và toàn bộ bài học bên trong?`))
                    return;
                  const { error } = await getSupabase()
                    .from("chapters")
                    .delete()
                    .eq("id", ch.id);
                  if (error) {
                    toast("error", error.message);
                    return;
                  }
                  toast("success", "Đã xóa chương.");
                  reload();
                }}
                className="admin-chip admin-chip--danger"
              >
                Xóa
              </button>
            </span>
          </div>
        ))}
        {selectedClassId && subjectChapters.length === 0 && (
          <p className="text-sm text-slate-400">
            Lớp này chưa có chương nào — thêm chương đầu tiên ở trên.
          </p>
        )}
      </div>
    </div>
  );
}
