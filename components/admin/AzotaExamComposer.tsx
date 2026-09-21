"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import ExamSection, { compressRasterInputs, type TopicGroup } from "@/components/admin/ExamSection";
import { useToast } from "@/components/ui/Toast";
import { canonicalizeQuestionTopics, type SchoolClass } from "@/features/exams/types";
import {
  LESSON_KIND_META,
  SECTION_META,
  SECTION_ORDER,
  isPeriodicExam,
  type Chapter,
  type Lesson,
  type LessonItem,
  type LessonItemKind,
} from "@/features/lessons/types";
import { subjectsForGrade } from "@/services/academic-subjects";
import { fetchQuestionTopics, lessonTopics, outcomesOf, type QuestionTopic } from "@/services/analytics";
import { classGrade, displayClassesByGrade, expandClassIdsByGrade, fetchClasses, setItemClasses } from "@/services/classes";
import { applyMediaToBundle, bundleToRows, typeCountSubtitle, validateBundle, type LessonBundle } from "@/services/lesson-import";
import { removeLessonMedia, uploadLessonMedia } from "@/services/lesson-media";
import { fetchChapters, fetchLessonItems, fetchLessons } from "@/services/lessons";
import { getSupabase } from "@/services/supabase";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const selectCls = `${inputCls} bg-[#0B1020]`;

type TargetKind = Extract<LessonItemKind, "kiem_tra" | "luyen_tap" | "bai_tap_ve_nha" | "bai_tap_mau">;
const TARGET_KINDS: TargetKind[] = ["bai_tap_mau", "kiem_tra", "luyen_tap", "bai_tap_ve_nha"];
const TARGET_HINT: Record<TargetKind, string> = {
  bai_tap_mau: "Ghi đáp án, bấm Kiểm tra để biết đúng/sai, rồi mới xem lời giải — không vào điểm.",
  kiem_tra: "Tính giờ, nộp bài một lần, điểm vào bảng điểm.",
  luyen_tap: "Học sinh tự làm, xem đáp án ngay, không vào điểm.",
  bai_tap_ve_nha: "Có hạn nộp, điểm vào bảng điểm.",
};

function toLocalInput(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default function AzotaExamComposer() {
  const toast = useToast();

  const [subjectCode, setSubjectCode] = useState("vat-ly");
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [allLessons, setAllLessons] = useState<Lesson[]>([]);
  const [classId, setClassId] = useState<number | null>(null);
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [lessonId, setLessonId] = useState<number | null>(null);
  const [kind, setKind] = useState<TargetKind>("kiem_tra");
  const [dueAtInput, setDueAtInput] = useState<string | null>(null);
  const [examMode, setExamMode] = useState<"keep" | "replace">("keep");
  const [itemsCache, setItemsCache] = useState<{ lessonId: number; list: LessonItem[] } | null>(null);
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  // Ngân hàng câu hỏi handoff báo trước khối, qua ref (không qua state) vì chỉ cần
  // đọc một lần khi danh sách lớp tải xong — tránh set-state chéo giữa 2 effect.
  const handoffGradeRef = useRef<string | null>(null);

  // ----- Nội dung đề: nhận từ ExamSection dùng chung với phần Đề của trang Đăng bài học -----
  const [examBundle, setExamBundle] = useState<LessonBundle | null>(null);

  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const [doneLink, setDoneLink] = useState<string | null>(null);

  useEffect(() => {
    fetchClasses().then((items) => {
      setClasses(items);
      setClassId((c) => {
        if (c !== null) return c;
        const byGrade = handoffGradeRef.current
          ? items.find((it) => classGrade(it.name) === handoffGradeRef.current)
          : null;
        return byGrade?.id ?? items[0]?.id ?? null;
      });
    });
    fetchChapters().then(setChapters);
    fetchLessons(true).then(setAllLessons);
  }, []);

  const selectedClass = classes.find((c) => c.id === classId) ?? null;
  const grade = selectedClass ? classGrade(selectedClass.name) : null;
  useEffect(() => {
    if (!grade) return;
    fetchQuestionTopics(grade)
      .then(setTopics)
      .catch(() => setTopics([]));
  }, [grade]);
  const catalogNames = useMemo(
    () => topics.filter((t) => t.grade === grade).map((t) => t.name),
    [topics, grade],
  );
  /** Yêu cầu cần đạt xếp theo bài; bài đang chọn (mục 3) đứng đầu. */
  const topicGroups = useMemo<TopicGroup[]>(() => {
    const parents = lessonTopics(topics.filter((t) => t.grade === grade));
    const groups = parents
      .sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi"))
      .map((p) => ({ parent: p, names: outcomesOf(topics, p.id).map((o) => o.name) }))
      .filter((g) => g.names.length > 0 || g.parent.lessonId === lessonId);
    const mine = groups.filter((g) => g.parent.lessonId === lessonId);
    const rest = groups.filter((g) => g.parent.lessonId !== lessonId);
    return [...mine, ...rest];
  }, [topics, grade, lessonId]);

  const displayClasses = displayClassesByGrade(classes);
  const visibleClassIds = useMemo(
    () => (classId === null ? [] : expandClassIdsByGrade([classId], classes) ?? []),
    [classId, classes],
  );
  const chapterOptions = useMemo(
    () =>
      chapters.filter(
        (ch) =>
          ch.subjectCode === subjectCode &&
          (ch.classIds.length === 0 || ch.classIds.some((id) => visibleClassIds.includes(id))),
      ),
    [chapters, subjectCode, visibleClassIds],
  );
  const selectedChapter = chapters.find((c) => c.id === chapterId) ?? null;
  const lessons = useMemo(
    () => (chapterId === null ? [] : allLessons.filter((l) => l.chapter_id === chapterId)),
    [allLessons, chapterId],
  );
  const selectedLesson = lessons.find((l) => l.id === lessonId) ?? null;

  const reloadExisting = useCallback(() => {
    if (lessonId !== null) fetchLessonItems(lessonId).then((list) => setItemsCache({ lessonId, list }));
  }, [lessonId]);
  useEffect(reloadExisting, [reloadExisting]);
  const existingItems = itemsCache?.lessonId === lessonId ? itemsCache.list : null;
  const existingItem = existingItems?.find((it) => it.kind === kind) ?? null;
  const dueAt = dueAtInput ?? toLocalInput(existingItem?.due_at ?? null);

  const targetClassIds = useMemo(() => {
    const base =
      selectedChapter && selectedChapter.classIds.length > 0
        ? selectedChapter.classIds
        : classId !== null
          ? [classId]
          : [];
    return expandClassIdsByGrade(base, classes) ?? base;
  }, [selectedChapter, classId, classes]);

  const questions = examBundle?.exam.questions ?? [];
  const check = examBundle ? validateBundle(examBundle) : null;
  const canPublish =
    !!examBundle && !!check?.ok && questions.length > 0 && lessonId !== null && !busy && !!examBundle.exam.title.trim();

  // ----- Đăng -----
  async function publish() {
    if (!examBundle || lessonId === null) return;
    setBusy(true);
    setDoneLink(null);
    const steps: string[] = [];
    const push = (s: string) => {
      steps.push(s);
      setLog([...steps]);
    };
    const supabase = getSupabase();
    let uploadedPaths: string[] = [];
    let createdExamId: number | null = null;
    try {
      let resolved = examBundle;
      const rasters = examBundle.raster_images ?? [];
      if (rasters.length) {
        push(`Nén & tải ${rasters.length} ảnh…`);
        const media = await uploadLessonMedia(supabase, lessonId, await compressRasterInputs(rasters));
        uploadedPaths = media.map((m) => m.storagePath);
        resolved = applyMediaToBundle(examBundle, media);
        push(`  ✓ đã tải ${media.length} ảnh`);
      }
      resolved = {
        ...resolved,
        exam: { ...resolved.exam, questions: canonicalizeQuestionTopics(resolved.exam.questions, catalogNames) },
      };
      const rows = bundleToRows(resolved, lessonId);

      push(`Tạo đề "${rows.exam.title}" (${rows.exam.questions.length} câu, ${rows.exam.duration_minutes} phút)…`);
      const { data: examRow, error: examErr } = await supabase
        .from("exams")
        .insert(rows.exam)
        .select("id")
        .single();
      if (examErr || !examRow) throw new Error(`Tạo đề lỗi: ${examErr?.message}`);
      const examId = examRow.id as number;
      createdExamId = examId;
      push(`  ✓ đề số ${examId}`);

      if (targetClassIds.length) {
        await setItemClasses("exam_classes", "exam_id", examId, targetClassIds);
        push(`  ✓ gán cho ${targetClassIds.length} lớp`);
      }

      const cur = existingItem;
      const hadExam = (cur?.exam_ids ?? []).length > 0;
      const nextIds = hadExam && examMode === "keep" ? [...cur!.exam_ids, examId] : [examId];
      const payload = {
        lesson_id: lessonId,
        kind,
        title: cur?.title || SECTION_META[kind].label,
        subtitle: typeCountSubtitle(rows.exam.questions, rows.exam.duration_minutes),
        body_html: "",
        video_url: "",
        pdf_url: "",
        questions: cur?.questions ?? [],
        exam_ids: nextIds,
        sort_order: cur?.sort_order ?? SECTION_ORDER.indexOf(kind) + 1,
        ...(kind === "bai_tap_ve_nha" ? { due_at: dueAt ? new Date(dueAt).toISOString() : null } : {}),
      };
      const r = cur
        ? await supabase.from("lesson_items").update(payload).eq("id", cur.id)
        : await supabase.from("lesson_items").insert(payload);
      if (r.error) throw new Error(`Mục ${SECTION_META[kind].label} lỗi: ${r.error.message}`);
      push(`${SECTION_META[kind].label}: ${cur ? "đã cập nhật" : "đã thêm"} (gắn đề ${examId}).`);

      push("Xong.");
      createdExamId = null;
      setDoneLink(`/lop-hoc/bai/?id=${lessonId}`);
      toast("success", "Đã đăng đề.");
      reloadExisting();
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      push(`✕ ${msg}`);
      if (createdExamId !== null) {
        const { error } = await supabase.from("exams").delete().eq("id", createdExamId);
        push(error ? `! Không xóa được đề ${createdExamId} vừa tạo (${error.message}).` : `Đã xóa đề ${createdExamId} vừa tạo.`);
      }
      if (uploadedPaths.length) {
        await removeLessonMedia(supabase, uploadedPaths).catch(() => {});
        push("Đã gỡ ảnh vừa tải lên.");
      }
      toast("error", msg);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <p className="admin-lead" style={{ marginTop: 0 }}>
          Dán đề từ Word hoặc thả file .docx — trang tách câu và đáp án ngay khi gõ, y như Azota. Xem trước bên phải,
          chọn lớp – bài rồi bấm Đăng.
        </p>
      </header>

      <ExamSection
        subjectCode={subjectCode}
        topicGroups={topicGroups}
        catalogNames={catalogNames}
        lessonPicked={lessonId !== null}
        onChange={setExamBundle}
        enableQuestionBankHandoff
        onHandoffGrade={(g) => {
          handoffGradeRef.current = g;
        }}
      />

      {/* ===== 3. Cấu hình & đăng ===== */}
      <section className="space-y-4 rounded-2xl border border-white/10 bg-white/5 p-4">
        <div className="flex items-center gap-2">
          <span className="admin-badge admin-badge--accent">3</span>
          <span className="text-sm font-semibold text-white">Cấu hình & đăng</span>
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <label className="text-xs font-semibold text-slate-400">
            Môn
            <select
              value={subjectCode}
              onChange={(e) => {
                setSubjectCode(e.target.value);
                setChapterId(null);
                setLessonId(null);
              }}
              className={`${selectCls} mt-1`}
            >
              {subjectsForGrade(grade ?? "").map((s) => (
                <option key={s.code} value={s.code}>
                  {s.icon} {s.label}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="grid gap-3 sm:grid-cols-3">
          <label className="text-xs font-semibold text-slate-400">
            Lớp
            <select
              value={classId ?? ""}
              onChange={(e) => {
                setClassId(e.target.value ? Number(e.target.value) : null);
                setChapterId(null);
                setLessonId(null);
              }}
              className={`${selectCls} mt-1`}
            >
              {displayClasses.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>
          <label className="text-xs font-semibold text-slate-400">
            Chương
            <select
              value={chapterId ?? ""}
              onChange={(e) => {
                setChapterId(e.target.value ? Number(e.target.value) : null);
                setLessonId(null);
              }}
              className={`${selectCls} mt-1`}
            >
              <option value="">— chọn chương —</option>
              {chapterOptions.map((ch) => (
                <option key={ch.id} value={ch.id}>
                  {ch.title}
                </option>
              ))}
            </select>
          </label>
          <label className="text-xs font-semibold text-slate-400">
            Bài
            <select
              value={lessonId ?? ""}
              onChange={(e) => setLessonId(e.target.value ? Number(e.target.value) : null)}
              disabled={chapterId === null}
              className={`${selectCls} mt-1 disabled:opacity-50`}
            >
              <option value="">— chọn bài —</option>
              {lessons.map((l) => (
                <option key={l.id} value={l.id}>
                  {isPeriodicExam(l.lesson_kind) ? `${LESSON_KIND_META[l.lesson_kind].icon} ` : ""}
                  {l.title}
                  {l.published ? "" : " (ẩn)"}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {TARGET_KINDS.map((k) => {
            const meta = SECTION_META[k];
            const active = kind === k;
            return (
              <button
                key={k}
                type="button"
                onClick={() => setKind(k)}
                className={`rounded-xl border p-3 text-left transition ${
                  active ? "border-primary bg-primary/10" : "border-white/10 bg-black/20 hover:border-white/30"
                }`}
              >
                <div className="text-sm font-semibold text-white">
                  {meta.icon} {meta.label}
                </div>
                <div className="mt-1 text-xs text-slate-400">{TARGET_HINT[k]}</div>
              </button>
            );
          })}
        </div>

        {kind === "bai_tap_ve_nha" && (
          <label className="block text-xs font-semibold text-slate-400 sm:max-w-xs">
            Hạn nộp (để trống = không đặt hạn)
            <input type="datetime-local" value={dueAt} onChange={(e) => setDueAtInput(e.target.value)} className={`${inputCls} mt-1`} />
          </label>
        )}

        {existingItem && existingItem.exam_ids.length > 0 && (
          <div className="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 bg-black/20 p-3 text-xs text-slate-300">
            <span>
              Mục <b>{SECTION_META[kind].label}</b> của bài này đã có {existingItem.exam_ids.length} đề.
            </span>
            {(
              [
                ["keep", "Giữ + thêm đề mới"],
                ["replace", "Thay bằng đề mới"],
              ] as const
            ).map(([v, label]) => (
              <label key={v} className="inline-flex items-center gap-1">
                <input type="radio" checked={examMode === v} onChange={() => setExamMode(v)} /> {label}
              </label>
            ))}
          </div>
        )}

        {selectedLesson && (
          <p className="text-xs text-slate-400">
            Đăng vào: {selectedClass?.name} → {selectedChapter?.title} → <b className="text-slate-200">{selectedLesson.title}</b>
            {targetClassIds.length > 1 && ` · gán cho ${targetClassIds.length} lớp cùng khối`}
          </p>
        )}

        {check && !check.ok && (
          <ul className="space-y-1 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-200">
            {check.errors.map((e, i) => (
              <li key={i}>• {e}</li>
            ))}
          </ul>
        )}

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={publish}
            disabled={!canPublish}
            className="rounded-xl bg-primary px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-primary/20 hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {busy ? "Đang đăng…" : "Đăng đề"}
          </button>
          {doneLink && (
            <Link href={doneLink} target="_blank" className="text-sm font-semibold text-emerald-300 underline">
              Mở bài học để kiểm tra →
            </Link>
          )}
        </div>

        {log.length > 0 && (
          <pre className="max-h-48 overflow-auto whitespace-pre-wrap rounded-xl bg-black/40 p-3 text-xs text-slate-300">
            {log.join("\n")}
          </pre>
        )}
      </section>
    </div>
  );
}
