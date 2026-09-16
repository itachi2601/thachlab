"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import DocxExamImport from "@/components/admin/DocxExamImport";
import ExamDraftEditor from "@/components/admin/ExamDraftEditor";
import QuestionCard from "@/components/exams/QuestionCard";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import { useToast } from "@/components/ui/Toast";
import {
  auditQuestionTags,
  canonicalizeQuestionTopics,
  emptyResponses,
  tagsComplete,
} from "@/features/exams/types";
import type { SchoolClass, TagAudit } from "@/features/exams/types";
import type { Chapter, Lesson, LessonItem } from "@/features/lessons/types";
import { academicSubject, subjectsForGrade } from "@/services/academic-subjects";
import {
  createQuestionTopic,
  fetchQuestionTopics,
  type QuestionTopic,
} from "@/services/analytics";
import {
  classGrade,
  displayClassesByGrade,
  expandClassIdsByGrade,
  fetchClasses,
  setItemClasses,
} from "@/services/classes";
import { compressImageFile } from "@/services/image-compress";
import {
  applyMediaToBundle,
  bundleToRows,
  typeCountSubtitle,
  texToBundleDraft,
  validateBundle,
  type LessonBundle,
} from "@/services/lesson-import";
import { removeLessonMedia, uploadLessonMedia, type RasterImageInput } from "@/services/lesson-media";
import { fetchChapters, fetchLessonItems, fetchLessons } from "@/services/lessons";
import { getSupabase } from "@/services/supabase";

const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

type SectionMode = "overwrite" | "merge" | "skip";
type ExamMode = "replace" | "keep" | "skip";

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

export default function LessonImporter() {
  const toast = useToast();

  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [allLessons, setAllLessons] = useState<Lesson[]>([]);
  const [classId, setClassId] = useState<number | null>(null);
  const [subjectCode, setSubjectCode] = useState("vat-ly");
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [lessonId, setLessonId] = useState<number | null>(null);
  const [itemsCache, setItemsCache] = useState<{ lessonId: number; list: LessonItem[] } | null>(null);
  const [topics, setTopics] = useState<QuestionTopic[]>([]);

  const [source, setSource] = useState<"docx" | "json">("docx");
  const [raw, setRaw] = useState("");
  const [tex, setTex] = useState("");
  const [editing, setEditing] = useState(false);
  const [bundle, setBundle] = useState<LessonBundle | null>(null);
  const [parseErr, setParseErr] = useState<string[]>([]);

  const [targets, setTargets] = useState<{ luyen_tap: boolean; kiem_tra: boolean }>({
    luyen_tap: true,
    kiem_tra: false,
  });
  const [theoryMode, setTheoryMode] = useState<SectionMode>("overwrite");
  const [workedMode, setWorkedMode] = useState<SectionMode>("overwrite");
  const [examMode, setExamMode] = useState<ExamMode>("replace");
  const [createMissingTopics, setCreateMissingTopics] = useState(true);
  const [tagOverride, setTagOverride] = useState(false);

  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const [doneLink, setDoneLink] = useState<string | null>(null);

  useEffect(() => {
    fetchClasses().then((items) => {
      setClasses(items);
      setClassId((c) => c ?? items[0]?.id ?? null);
    });
    fetchChapters().then(setChapters);
    fetchLessons(true).then(setAllLessons);
  }, []);

  const selectedClass = classes.find((c) => c.id === classId) ?? null;
  const grade = selectedClass ? classGrade(selectedClass.name) : null;
  // Danh mục chủ đề của khối — để soát nhãn của đề trước khi đăng.
  const loadTopics = useCallback(() => {
    if (!grade) return;
    fetchQuestionTopics(grade)
      .then(setTopics)
      .catch(() => setTopics([]));
  }, [grade]);
  useEffect(loadTopics, [loadTopics]);
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

  const reloadExisting = useCallback(() => {
    if (lessonId !== null) fetchLessonItems(lessonId).then((list) => setItemsCache({ lessonId, list }));
  }, [lessonId]);
  useEffect(reloadExisting, [reloadExisting]);
  const existingItems = itemsCache?.lessonId === lessonId ? itemsCache.list : null;

  const targetClassIds = useMemo(() => {
    const base =
      selectedChapter && selectedChapter.classIds.length > 0
        ? selectedChapter.classIds
        : classId !== null
          ? [classId]
          : [];
    return expandClassIdsByGrade(base, classes) ?? base;
  }, [selectedChapter, classId, classes]);

  const check = bundle ? validateBundle(bundle) : null;
  // Lọc lại theo khối: danh sách trong state có thể là của lớp chọn trước đó.
  const gradeTopics = useMemo(
    () => (grade ? topics.filter((t) => t.grade === grade) : []),
    [topics, grade],
  );
  const catalogNames = useMemo(() => gradeTopics.map((t) => t.name), [gradeTopics]);
  // Chủ đề tầng bài đã tách yêu cầu cần đạt: gắn nhãn ở mức cả bài là còn thô.
  const coarseNames = useMemo(() => {
    const hasChild = new Set(
      gradeTopics.map((t) => t.parentId).filter((id): id is number => id !== null),
    );
    return gradeTopics.filter((t) => t.parentId === null && hasChild.has(t.id)).map((t) => t.name);
  }, [gradeTopics]);
  const audit: TagAudit | null = useMemo(
    () =>
      bundle ? auditQuestionTags(bundle.exam?.questions ?? [], catalogNames, coarseNames) : null,
    [bundle, catalogNames, coarseNames],
  );
  // Đủ nhãn = mọi câu có chủ đề + loại, và mọi chủ đề đã có trong danh mục (hoặc sẽ được tạo).
  const tagsReady =
    !!audit &&
    (tagsComplete(audit) ||
      (audit.missingTopic.length === 0 &&
        audit.missingForm.length === 0 &&
        createMissingTopics &&
        catalogNames.length > 0 &&
        lessonId !== null &&
        !!grade));
  const canPublish =
    !!bundle &&
    !!check?.ok &&
    lessonId !== null &&
    (targets.luyen_tap || targets.kiem_tra) &&
    (tagsReady || tagOverride) &&
    !busy;

  function existing(kind: LessonItem["kind"]) {
    return existingItems?.find((it) => it.kind === kind) ?? null;
  }

  function loadBundle() {
    setParseErr([]);
    setBundle(null);
    let parsed: unknown;
    try {
      parsed = JSON.parse(raw);
    } catch (e) {
      setParseErr([`JSON không hợp lệ: ${e instanceof Error ? e.message : e}`]);
      return;
    }
    const v = validateBundle(parsed);
    setBundle(parsed as LessonBundle);
    if (!v.ok) toast("warning", `Gói có ${v.errors.length} lỗi cần sửa.`);
    else toast("success", "Gói hợp lệ.");
  }

  /** Nhận nháp từ file Word / .tex: giữ JSON và bản đang sửa luôn khớp nhau. */
  function applyDraft(draft: LessonBundle, notes: string[]) {
    setBundle(draft);
    setRaw(JSON.stringify(draft, null, 2));
    setParseErr(notes.map((n) => `Ghi chú: ${n}`));
    setEditing(true);
  }

  function prefillFromTex() {
    if (!tex.trim()) return;
    const title = selectedLessonTitle()
      ? `Luyện tập – ${selectedLessonTitle()}`
      : "Luyện tập";
    const { bundle: draft, notes } = texToBundleDraft(tex, title);
    applyDraft(draft, notes);
    toast("info", "Đã nạp nháp từ .tex — rà lại phần đề trước khi đăng.");
  }

  function selectedLessonTitle() {
    return lessons.find((l) => l.id === lessonId)?.title ?? "";
  }

  async function publish() {
    if (!bundle || lessonId === null) return;
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
      // 1. Ảnh raster
      let resolved = bundle;
      const rasters = bundle.raster_images ?? [];
      if (rasters.length) {
        push(`Nén & tải ${rasters.length} ảnh…`);
        const compressed = await compressRasterInputs(rasters);
        const media = await uploadLessonMedia(supabase, lessonId, compressed);
        uploadedPaths = media.map((m) => m.storagePath);
        resolved = applyMediaToBundle(bundle, media);
        push(`  ✓ đã tải ${media.length} ảnh lên lesson-media`);
      }

      // 1b. Nhãn chủ đề: tạo chủ đề mới cho bài này, rồi chuẩn hoá chính tả tên
      // theo danh mục để ExamRunner tra được topic_id lúc học sinh nộp bài.
      const aud = auditQuestionTags(resolved.exam?.questions ?? [], catalogNames, coarseNames);
      if (aud.unknown.length && createMissingTopics && grade && catalogNames.length > 0) {
        // Bài này đã có chủ đề tầng bài thì chủ đề mới là yêu cầu cần đạt con của nó.
        const parent = gradeTopics.find((t) => t.parentId === null && t.lessonId === lessonId);
        push(
          parent
            ? `Tạo ${aud.unknown.length} yêu cầu cần đạt trong "${parent.name}"…`
            : `Tạo ${aud.unknown.length} chủ đề mới cho bài này…`,
        );
        for (const t of aud.unknown) {
          try {
            await createQuestionTopic({
              grade,
              name: t.name,
              subjectCode,
              chapterId,
              lessonId,
              parentId: parent?.id ?? null,
            });
            push(`  ✓ chủ đề "${t.name}"`);
          } catch (e) {
            const msg = e instanceof Error ? e.message : String(e);
            push(`  ! chưa tạo được chủ đề "${t.name}" (${msg}) — thêm tay ở Quản trị → Chủ đề câu hỏi.`);
          }
        }
        loadTopics();
      }
      resolved = {
        ...resolved,
        exam: {
          ...resolved.exam,
          questions: canonicalizeQuestionTopics(resolved.exam?.questions ?? [], catalogNames),
        },
      };

      const rows = bundleToRows(resolved, lessonId);

      // 2. Đề
      push(`Tạo đề "${rows.exam.title}"…`);
      const { data: examRow, error: examErr } = await supabase
        .from("exams")
        .insert(rows.exam)
        .select("id")
        .single();
      if (examErr || !examRow) throw new Error(`Tạo đề lỗi: ${examErr?.message}`);
      const examId = examRow.id as number;
      createdExamId = examId;
      push(`  ✓ exam id ${examId}`);

      // 3. exam_classes
      if (targetClassIds.length) {
        await setItemClasses("exam_classes", "exam_id", examId, targetClassIds);
        push(`  ✓ gán đề cho ${targetClassIds.length} lớp`);
      }

      // 4. Lý thuyết
      const lt = existing("ly_thuyet");
      if (!rows.lyThuyet.body_html.trim())
        push("Lý thuyết: gói không có phần này — giữ nguyên nội dung cũ.");
      else if (theoryMode === "skip" && lt) push("Lý thuyết: bỏ qua (giữ nội dung cũ).");
      else {
        const payload = { ...rows.lyThuyet, sort_order: lt?.sort_order ?? 1 };
        const r = lt
          ? await supabase.from("lesson_items").update(payload).eq("id", lt.id)
          : await supabase.from("lesson_items").insert(payload);
        if (r.error) throw new Error(`Lý thuyết lỗi: ${r.error.message}`);
        push(`Lý thuyết: ${lt ? "đã ghi đè" : "đã thêm"}.`);
      }

      // 5. Các dạng bài tập
      const bt = existing("bai_tap_mau");
      if (rows.baiTapMau.questions.length === 0)
        push("Các dạng bài tập: gói không có phần này — giữ nguyên nội dung cũ.");
      else if (workedMode === "skip" && bt) push("Các dạng bài tập: bỏ qua.");
      else {
        const merged =
          workedMode === "merge" && bt
            ? [...bt.questions, ...rows.baiTapMau.questions]
            : rows.baiTapMau.questions;
        const payload = {
          ...rows.baiTapMau,
          questions: merged,
          subtitle: rows.baiTapMau.subtitle || bt?.subtitle || "",
          sort_order: bt?.sort_order ?? 3,
        };
        const r = bt
          ? await supabase.from("lesson_items").update(payload).eq("id", bt.id)
          : await supabase.from("lesson_items").insert(payload);
        if (r.error) throw new Error(`Các dạng bài tập lỗi: ${r.error.message}`);
        push(`Các dạng bài tập: ${bt ? (workedMode === "merge" ? "đã gộp thêm" : "đã ghi đè") : "đã thêm"} (${merged.length} dạng).`);
      }

      // 6. luyen_tap / kiem_tra
      const subtitle = typeCountSubtitle(rows.exam.questions, rows.exam.duration_minutes);
      for (const kind of ["luyen_tap", "kiem_tra"] as const) {
        if (!targets[kind]) continue;
        const cur = existing(kind);
        const hadExam = (cur?.exam_ids ?? []).length > 0;
        if (hadExam && examMode === "skip") {
          push(`${kind}: bỏ qua (giữ đề cũ).`);
          continue;
        }
        const nextIds =
          hadExam && examMode === "keep" ? [...cur!.exam_ids, examId] : [examId];
        if (hadExam && examMode === "replace") {
          const stale = cur!.exam_ids.filter((id) => id !== examId);
          if (stale.length) {
            await supabase.from("exams").delete().in("id", stale);
            push(`${kind}: đã xóa ${stale.length} đề cũ.`);
          }
        }
        const payload = {
          lesson_id: lessonId,
          kind,
          title: cur?.title || (kind === "luyen_tap" ? "Luyện tập" : "Kiểm tra"),
          subtitle,
          body_html: "",
          video_url: "",
          pdf_url: "",
          questions: [],
          exam_ids: nextIds,
          sort_order: cur?.sort_order ?? (kind === "luyen_tap" ? 4 : 5),
        };
        const r = cur
          ? await supabase.from("lesson_items").update(payload).eq("id", cur.id)
          : await supabase.from("lesson_items").insert(payload);
        if (r.error) throw new Error(`${kind} lỗi: ${r.error.message}`);
        push(`${kind}: ${cur ? "đã cập nhật" : "đã thêm"} (gắn đề ${examId}).`);
      }

      push("Xong.");
      createdExamId = null; // đã gắn xong, không rollback nữa
      setDoneLink(`/lop-hoc/bai/?id=${lessonId}`);
      toast("success", "Đã đăng bài học.");
      reloadExisting();
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      push(`✕ ${msg}`);
      // Dọn sạch những gì đã tạo để lần thử sau không để lại đề/ảnh mồ côi.
      if (createdExamId !== null) {
        const staleId = createdExamId;
        // Mục nào đã kịp gắn đề thì gỡ ra trước, tránh để lại exam_ids trỏ vào đề đã xóa.
        const { data: touched } = await supabase
          .from("lesson_items")
          .select("id, exam_ids")
          .eq("lesson_id", lessonId)
          .contains("exam_ids", [staleId]);
        for (const it of touched ?? []) {
          await supabase
            .from("lesson_items")
            .update({ exam_ids: ((it.exam_ids as number[]) ?? []).filter((x) => x !== staleId) })
            .eq("id", it.id);
        }
        const { error } = await supabase.from("exams").delete().eq("id", staleId);
        push(
          error
            ? `! Không xóa được đề ${staleId} vừa tạo (${error.message}) — xóa tay trong Quản trị đề.`
            : `Đã xóa đề ${staleId} vừa tạo${touched?.length ? ` và gỡ khỏi ${touched.length} mục` : ""}.`,
        );
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

  const previewResponses = bundle ? emptyResponses(bundle.exam?.questions ?? []) : [];

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-display text-2xl font-bold text-white">Nhập bài học / đề kiểm tra</h1>
        <p className="mt-1 text-sm text-slate-400">
          Thả file đề Word (.docx) là trang tự tách câu và đáp án — sửa lại chỗ nào chưa ưng rồi Đăng.
          Hoặc dán gói bài học JSON như cũ.
        </p>
      </header>

      {/* 1. Chọn đích */}
      <section className="space-y-3 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <p className="text-sm font-medium text-slate-300">1. Chọn Lớp → Môn → Chương → Bài</p>
        <div className="flex flex-wrap gap-2">
          {displayClasses.map((c) => (
            <button
              key={c.id}
              type="button"
              onClick={() => {
                setClassId(c.id);
                setSubjectCode("vat-ly");
                setChapterId(null);
                setLessonId(null);
              }}
              style={c.id === classId ? { backgroundColor: c.color, borderColor: c.color } : undefined}
              className={`rounded-full border px-4 py-2 text-sm font-semibold ${
                c.id === classId ? "text-white" : "border-white/10 text-slate-400 hover:border-white/30"
              }`}
            >
              {c.icon} {c.name}
            </button>
          ))}
        </div>
        {selectedClass && (
          <div className="flex flex-wrap gap-2">
            {subjectsForGrade(classGrade(selectedClass.name) ?? "").map((s) => (
              <button
                key={s.code}
                type="button"
                onClick={() => {
                  setSubjectCode(s.code);
                  setChapterId(null);
                  setLessonId(null);
                }}
                className={`rounded-full border px-3 py-1.5 text-xs font-semibold ${
                  subjectCode === s.code
                    ? "border-blue-400 bg-blue-500/15 text-blue-200"
                    : "border-white/10 text-slate-400 hover:border-white/30"
                }`}
              >
                {s.icon} {s.label}
              </button>
            ))}
          </div>
        )}
        <div className="grid gap-2 sm:grid-cols-2">
          <select
            value={chapterId ?? ""}
            onChange={(e) => {
              setChapterId(e.target.value ? Number(e.target.value) : null);
              setLessonId(null);
            }}
            className={`${inputCls} bg-[#0B1020]`}
          >
            <option value="">— Chọn chương —</option>
            {chapterOptions.map((ch) => (
              <option key={ch.id} value={ch.id}>
                {ch.title}
              </option>
            ))}
          </select>
          <select
            value={lessonId ?? ""}
            onChange={(e) => setLessonId(e.target.value ? Number(e.target.value) : null)}
            className={`${inputCls} bg-[#0B1020]`}
            disabled={chapterId === null}
          >
            <option value="">— Chọn bài học —</option>
            {lessons.map((l) => (
              <option key={l.id} value={l.id}>
                {l.title}
                {l.published ? "" : " (ẩn)"}
              </option>
            ))}
          </select>
        </div>
        {selectedChapter && (
          <p className="text-xs text-slate-500">
            Môn {academicSubject(subjectCode).label} · đề sẽ gán cho lớp:{" "}
            {classes
              .filter((c) => targetClassIds.includes(c.id))
              .map((c) => c.name)
              .join(", ") || "(chưa xác định)"}
          </p>
        )}
      </section>

      {/* 2. Nguồn nội dung */}
      <section className="space-y-3 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex flex-wrap items-center gap-2">
          <p className="text-sm font-medium text-slate-300">2. Nội dung</p>
          {([["docx", "Từ file Word (.docx)"], ["json", "Dán gói JSON"]] as const).map(([key, label]) => (
            <button
              key={key}
              type="button"
              onClick={() => setSource(key)}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold ${
                source === key ? "bg-[#2563EB] text-white" : "bg-white/5 text-slate-400 hover:bg-white/10"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {source === "docx" && (
          <DocxExamImport
            fallbackTitle={selectedLessonTitle() ? `Kiểm tra – ${selectedLessonTitle()}` : ""}
            subjectCode={subjectCode}
            onDraft={applyDraft}
          />
        )}

        {source === "json" && (
        <>
        <textarea
          value={raw}
          onChange={(e) => setRaw(e.target.value)}
          rows={8}
          placeholder='{ "schema": "thachlab.lesson-bundle/v1", "theory_html": "…", "worked_examples": [...], "exam": { ... } }'
          className={`${inputCls} w-full font-mono text-xs`}
        />
        <div className="flex flex-wrap gap-2">
          <button
            onClick={loadBundle}
            disabled={!raw.trim()}
            className="rounded-lg bg-emerald-600/30 px-4 py-2 text-sm font-semibold text-emerald-200 hover:bg-emerald-600/50 disabled:opacity-40"
          >
            Nạp gói
          </button>
        </div>

        <details className="text-xs text-slate-400">
          <summary className="cursor-pointer hover:text-slate-200">Hoặc dán .tex để tạo nháp (rà lại đề)</summary>
          <textarea
            value={tex}
            onChange={(e) => setTex(e.target.value)}
            rows={6}
            placeholder="\section{...} \subsection{LÍ THUYẾT} ... \subsection{PHẦN I. ...}"
            className={`${inputCls} mt-2 w-full font-mono text-xs`}
          />
          <button
            onClick={prefillFromTex}
            disabled={!tex.trim()}
            className="mt-2 rounded-lg bg-white/10 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:bg-white/20 disabled:opacity-40"
          >
            Tạo nháp từ .tex
          </button>
        </details>
        </>
        )}

        {parseErr.length > 0 && (
          <ul className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-3 text-xs text-amber-200">
            {parseErr.map((e, i) => (
              <li key={i}>• {e}</li>
            ))}
          </ul>
        )}
      </section>

      {/* 3. Validate + preview */}
      {bundle && check && (
        <section className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <p className="text-sm font-medium text-slate-300">3. Kiểm tra & xem trước</p>

          {check.errors.length > 0 && (
            <ul className="rounded-lg border border-red-500/30 bg-red-500/5 p-3 text-xs text-red-200">
              {check.errors.map((e, i) => (
                <li key={i}>✕ {e}</li>
              ))}
            </ul>
          )}
          {check.warnings.length > 0 && (
            <ul className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-3 text-xs text-amber-200">
              {check.warnings.map((e, i) => (
                <li key={i}>! {e}</li>
              ))}
            </ul>
          )}
          {check.ok && check.warnings.length === 0 && (
            <p className="text-xs text-emerald-300">✓ Gói hợp lệ, sẵn sàng đăng.</p>
          )}

          {audit && (
            <div
              className={`rounded-xl border p-4 text-xs ${
                tagsReady ? "border-emerald-500/30 bg-emerald-500/5" : "border-amber-500/40 bg-amber-500/5"
              }`}
            >
              <p className="text-sm font-semibold text-slate-200">
                Nhãn chủ đề · đã gắn {audit.tagged}/{audit.total} câu
              </p>
              <p className="mt-0.5 text-[11px] text-slate-500">
                Dùng cho Phân tích chủ đề &amp; cảnh báo phụ đạo. Nhãn được chốt lúc học sinh nộp
                bài — gắn sau sẽ không cứu được các lượt đã nộp.
              </p>

              {!grade ? (
                <p className="mt-2 text-amber-200">Chọn lớp ở mục 1 để soát nhãn theo danh mục khối.</p>
              ) : catalogNames.length === 0 ? (
                <p className="mt-2 text-amber-200">
                  Danh mục chủ đề khối {grade} đang trống — thêm ở Quản trị → Chủ đề câu hỏi.
                </p>
              ) : null}

              {audit.missingTopic.length > 0 && (
                <p className="mt-2 text-amber-200">✕ Thiếu chủ đề ở câu: {audit.missingTopic.join(", ")}.</p>
              )}
              {audit.missingForm.length > 0 && (
                <p className="mt-1 text-amber-200">
                  ✕ Thiếu loại (lý thuyết / bài tập) ở câu: {audit.missingForm.join(", ")}.
                </p>
              )}

              {(audit.known.length > 0 || audit.unknown.length > 0) && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {audit.known.map((t) => (
                    <span
                      key={t.name}
                      className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-emerald-200"
                    >
                      {t.name} · {t.count} câu
                    </span>
                  ))}
                  {audit.unknown.map((t) => (
                    <span
                      key={t.name}
                      className="rounded-full border border-amber-500/40 bg-amber-500/10 px-2 py-0.5 text-amber-200"
                    >
                      {t.name} · {t.count} câu · chưa có trong danh mục
                    </span>
                  ))}
                </div>
              )}

              {audit.coarse.length > 0 && (
                <p className="mt-2 text-amber-200">
                  ⚠ Còn gắn ở mức cả bài:{" "}
                  {audit.coarse.map((t) => `${t.name} (${t.count} câu)`).join(", ")} — các bài này đã
                  tách yêu cầu cần đạt, gắn vào đúng yêu cầu thì mới biết em hổng phần nào. Sửa ở
                  Quản trị → Chủ đề câu hỏi sau khi đăng cũng được, nhưng nhãn chốt lúc nộp bài.
                </p>
              )}

              {audit.unknown.length > 0 && (
                <label className="mt-3 flex items-start gap-2 text-slate-300">
                  <input
                    type="checkbox"
                    checked={createMissingTopics}
                    onChange={(e) => setCreateMissingTopics(e.target.checked)}
                    disabled={lessonId === null || !grade || catalogNames.length === 0}
                    className="mt-0.5 accent-emerald-500"
                  />
                  <span>
                    Tạo {audit.unknown.length} chủ đề mới cho{" "}
                    <b className="text-slate-100">{selectedLessonTitle() || "bài đang chọn"}</b> khi đăng
                    {lessonId === null && <span className="text-amber-300"> — chọn bài học ở mục 1 trước</span>}
                    <span className="block text-[11px] text-slate-500">
                      Chủ đề mới gắn sẵn vào đúng Chương → Bài này, nên nút “Ôn lại” của học sinh nhảy
                      đúng chỗ ngay.
                    </span>
                  </span>
                </label>
              )}

              {!tagsReady && (
                <label className="mt-2 flex items-center gap-2 text-slate-400">
                  <input
                    type="checkbox"
                    checked={tagOverride}
                    onChange={(e) => setTagOverride(e.target.checked)}
                    className="accent-amber-500"
                  />
                  Đăng dù nhãn chưa đủ (câu thiếu nhãn sẽ không vào phân tích)
                </label>
              )}
            </div>
          )}

          <div className="rounded-xl border border-white/10 bg-black/20 p-4">
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-blue-300">Lý thuyết</p>
            <ContentHtml html={bundle.theory_html ?? ""} className="block text-sm text-slate-300" />
          </div>

          {(bundle.worked_examples?.length ?? 0) > 0 && (
            <div className="rounded-xl border border-white/10 bg-black/20 p-4">
              <p className="mb-2 text-xs font-bold uppercase tracking-wide text-violet-300">
                Các dạng bài tập ({bundle.worked_examples.length})
              </p>
              <WorkedQuestionsGrid questions={bundle.worked_examples} />
            </div>
          )}

          <div className="rounded-xl border border-white/10 bg-black/20 p-4">
            <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
              <p className="text-xs font-bold uppercase tracking-wide text-amber-300">
                Đề: {bundle.exam?.title} — {typeCountSubtitle(bundle.exam?.questions ?? [], bundle.exam?.duration_minutes)}
              </p>
              <button
                type="button"
                onClick={() => setEditing((v) => !v)}
                className="rounded-lg bg-white/10 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:bg-white/20"
              >
                {editing ? "Xem như học sinh" : "Sửa từng câu"}
              </button>
            </div>

            {editing && bundle.exam ? (
              <ExamDraftEditor
                bundle={bundle}
                onChange={(next) => {
                  setBundle(next);
                  setRaw(JSON.stringify(next, null, 2));
                }}
              />
            ) : (
            <>
            <div className="space-y-3">
              {(bundle.exam?.questions ?? []).map((q, i) => (
                <QuestionCard key={i} index={i + 1} question={q} response={previewResponses[i]} review selfCheck={false} />
              ))}
            </div>
            </>
            )}
          </div>
        </section>
      )}

      {/* 4. Mục đề + xử lý nội dung cũ */}
      {bundle && (
        <section className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <p className="text-sm font-medium text-slate-300">4. Gắn đề & xử lý nội dung đã có</p>

          <div className="flex flex-wrap gap-4 text-sm text-slate-300">
            {(["luyen_tap", "kiem_tra"] as const).map((k) => (
              <label key={k} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={targets[k]}
                  onChange={(e) => setTargets((t) => ({ ...t, [k]: e.target.checked }))}
                  className="accent-emerald-500"
                />
                {k === "luyen_tap" ? "Gắn vào Luyện tập" : "Gắn vào Kiểm tra"}
                {(existing(k)?.exam_ids.length ?? 0) > 0 && (
                  <span className="text-xs text-amber-300">· đã có {existing(k)!.exam_ids.length} đề</span>
                )}
              </label>
            ))}
          </div>

          {existingItems && (
            <div className="grid gap-3 text-xs sm:grid-cols-3">
              <ModePicker
                label="Lý thuyết"
                has={!!existing("ly_thuyet")?.body_html}
                value={theoryMode}
                onChange={setTheoryMode}
                options={[["overwrite", "Ghi đè"], ["skip", "Bỏ qua"]]}
              />
              <ModePicker
                label="Các dạng bài tập"
                has={(existing("bai_tap_mau")?.questions.length ?? 0) > 0}
                value={workedMode}
                onChange={setWorkedMode}
                options={[["overwrite", "Ghi đè"], ["merge", "Gộp thêm"], ["skip", "Bỏ qua"]]}
              />
              <ModePicker
                label="Đề cũ ở mục đã chọn"
                has={
                  (existing("luyen_tap")?.exam_ids.length ?? 0) > 0 ||
                  (existing("kiem_tra")?.exam_ids.length ?? 0) > 0
                }
                value={examMode}
                onChange={setExamMode}
                options={[["replace", "Thay"], ["keep", "Giữ + thêm"], ["skip", "Bỏ qua"]]}
              />
            </div>
          )}
        </section>
      )}

      {/* 5. Đăng */}
      <section className="space-y-3 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <button
          onClick={publish}
          disabled={!canPublish}
          className="rounded-full bg-[#2563EB] px-6 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-40"
        >
          {busy ? "Đang đăng…" : "Đăng bài học"}
        </button>
        {!canPublish && bundle && (
          <p className="text-xs text-slate-500">
            {check && !check.ok
              ? "Sửa hết lỗi ở mục 3 trước khi đăng."
              : lessonId === null
                ? "Chọn bài học ở mục 1."
                : !targets.luyen_tap && !targets.kiem_tra
                  ? "Chọn ít nhất một mục để gắn đề."
                  : !tagsReady && !tagOverride
                    ? "Nhãn chủ đề ở mục 3 chưa đủ — sửa nhãn trong gói, hoặc tick ô cho phép đăng."
                    : ""}
          </p>
        )}
        {log.length > 0 && (
          <pre className="max-h-64 overflow-y-auto rounded-lg border border-white/10 bg-black/30 p-3 text-xs text-slate-300">
            {log.join("\n")}
          </pre>
        )}
        {doneLink && (
          <a href={doneLink} target="_blank" rel="noreferrer" className="text-sm font-semibold text-[#60A5FA] hover:text-[#93C5FD]">
            → Mở bài học: {doneLink}
          </a>
        )}
      </section>
    </div>
  );
}

function ModePicker<T extends string>({
  label,
  has,
  value,
  onChange,
  options,
}: {
  label: string;
  has: boolean;
  value: T;
  onChange: (v: T) => void;
  options: [T, string][];
}) {
  return (
    <div className={`rounded-lg border p-3 ${has ? "border-amber-500/30 bg-amber-500/5" : "border-white/10"}`}>
      <p className="font-semibold text-slate-200">{label}</p>
      <p className="mt-0.5 text-[11px] text-slate-500">{has ? "Bài đã có nội dung này" : "Chưa có — sẽ thêm mới"}</p>
      {has && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {options.map(([v, l]) => (
            <button
              key={v}
              type="button"
              onClick={() => onChange(v)}
              className={`rounded-md px-2 py-1 text-[11px] font-semibold ${
                value === v ? "bg-[#2563EB] text-white" : "bg-white/5 text-slate-400 hover:bg-white/10"
              }`}
            >
              {l}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
