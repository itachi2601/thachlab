"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import ExamSection, { type ExamSectionSeed, type TopicGroup, compressRasterInputs } from "@/components/admin/ExamSection";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import { useToast } from "@/components/ui/Toast";
import { auditQuestionTags, canonicalizeQuestionTopics, tagsComplete } from "@/features/exams/types";
import type { SchoolClass, TagAudit } from "@/features/exams/types";
import type { Chapter, Lesson, LessonItem, LessonWorkedQuestion } from "@/features/lessons/types";
import { academicSubject, subjectsForGrade } from "@/services/academic-subjects";
import { createQuestionTopic, fetchQuestionTopics, lessonTopics, outcomesOf, type QuestionTopic } from "@/services/analytics";
import {
  classGrade,
  displayClassesByGrade,
  expandClassIdsByGrade,
  fetchClasses,
  setItemClasses,
} from "@/services/classes";
import {
  BUNDLE_SCHEMA,
  applyMediaToBundle,
  bundleToRows,
  parseLessonTex,
  typeCountSubtitle,
  validateBundle,
  type LessonBundle,
} from "@/services/lesson-import";
import { removeLessonMedia, uploadLessonMedia } from "@/services/lesson-media";
import { fetchChapters, fetchLessonItems, fetchLessons } from "@/services/lessons";
import { getSupabase } from "@/services/supabase";

const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

type SectionMode = "overwrite" | "merge" | "skip";
type ExamMode = "replace" | "keep" | "skip";
type TheoryPart = { theory_html: string; worked_examples: LessonWorkedQuestion[] };

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

  // ----- 2. Lý thuyết & dạng bài: dán .tex, tách lại mỗi lần gõ (giống ô đề bên dưới) -----
  const [tex, setTex] = useState("");
  const [debouncedTex, setDebouncedTex] = useState("");
  const [theoryOverride, setTheoryOverride] = useState<TheoryPart | null>(null);

  // ----- 3. Đề: dùng chung ExamSection với trang Đăng đề -----
  const [examBundle, setExamBundle] = useState<LessonBundle | null>(null);
  const [examSeed, setExamSeed] = useState<ExamSectionSeed | null>(null);

  // ----- Nâng cao: dán gói JSON có sẵn (đường dự phòng cho skill OCR đề PDF/scan) -----
  const [jsonRaw, setJsonRaw] = useState("");
  const [jsonErr, setJsonErr] = useState<string[]>([]);

  const [targets, setTargets] = useState<{ luyen_tap: boolean; kiem_tra: boolean; bai_tap_mau: boolean }>({
    luyen_tap: true,
    kiem_tra: false,
    bai_tap_mau: false,
  });
  const [theoryMode, setTheoryMode] = useState<SectionMode>("overwrite");
  const [workedMode, setWorkedMode] = useState<SectionMode>("overwrite");
  const [examMode, setExamMode] = useState<ExamMode>("keep");
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

  useEffect(() => {
    const t = setTimeout(() => setDebouncedTex(tex), 250);
    return () => clearTimeout(t);
  }, [tex]);

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

  /** Yêu cầu cần đạt xếp theo bài; bài đang chọn đứng đầu — cùng cách dựng với trang Đăng đề. */
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

  const theoryDraft = useMemo(() => (debouncedTex.trim() ? parseLessonTex(debouncedTex) : null), [debouncedTex]);
  const theoryPart: TheoryPart = useMemo(
    () =>
      theoryOverride ?? {
        theory_html: theoryDraft?.theory_html ?? "",
        worked_examples: theoryDraft?.worked_examples ?? [],
      },
    [theoryOverride, theoryDraft],
  );

  const fullBundle: LessonBundle | null = useMemo(() => {
    if (!examBundle) return null;
    return {
      schema: BUNDLE_SCHEMA,
      theory_html: theoryPart.theory_html,
      worked_examples: theoryPart.worked_examples,
      exam: examBundle.exam,
      raster_images: examBundle.raster_images ?? [],
    };
  }, [examBundle, theoryPart]);

  const check = fullBundle ? validateBundle(fullBundle) : null;
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
      fullBundle ? auditQuestionTags(fullBundle.exam?.questions ?? [], catalogNames, coarseNames) : null,
    [fullBundle, catalogNames, coarseNames],
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
    !!fullBundle &&
    !!check?.ok &&
    lessonId !== null &&
    (targets.luyen_tap || targets.kiem_tra || targets.bai_tap_mau) &&
    (tagsReady || tagOverride) &&
    !busy;

  function existing(kind: LessonItem["kind"]) {
    return existingItems?.find((it) => it.kind === kind) ?? null;
  }

  function selectedLessonTitle() {
    return lessons.find((l) => l.id === lessonId)?.title ?? "";
  }

  /** Nạp gói JSON dán sẵn (skill OCR đề PDF/scan) vào cả 2 khối lý thuyết & đề. */
  function applyJsonBundle(b: LessonBundle) {
    setTheoryOverride({ theory_html: b.theory_html ?? "", worked_examples: b.worked_examples ?? [] });
    setTex("");
    setExamSeed({ token: Date.now(), bundle: b });
  }

  function loadJsonBundle() {
    setJsonErr([]);
    let parsed: unknown;
    try {
      parsed = JSON.parse(jsonRaw);
    } catch (e) {
      setJsonErr([`JSON không hợp lệ: ${e instanceof Error ? e.message : e}`]);
      return;
    }
    const v = validateBundle(parsed);
    applyJsonBundle(parsed as LessonBundle);
    if (!v.ok) toast("warning", `Gói có ${v.errors.length} lỗi cần sửa — xem khối Đề/Lý thuyết bên dưới.`);
    else toast("success", "Gói hợp lệ — đã nạp vào Lý thuyết và Đề.");
  }

  function clearTheoryOverride() {
    setTheoryOverride(null);
  }

  async function publish() {
    if (!fullBundle || lessonId === null) return;
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
      let resolved = fullBundle;
      const rasters = fullBundle.raster_images ?? [];
      if (rasters.length) {
        push(`Nén & tải ${rasters.length} ảnh…`);
        const compressed = await compressRasterInputs(rasters);
        const media = await uploadLessonMedia(supabase, lessonId, compressed);
        uploadedPaths = media.map((m) => m.storagePath);
        resolved = applyMediaToBundle(fullBundle, media);
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

      // 5. Bài tập mẫu: các dạng bài (đọc, không chấm) + đề tự chấm (tuỳ chọn, exam_ids)
      const bt = existing("bai_tap_mau");
      const hasWorked = rows.baiTapMau.questions.length > 0;
      // Gói không có dạng bài (vd publish riêng để gắn đề tự chấm) → không bao giờ xoá dạng bài cũ.
      const shouldWriteBt = targets.bai_tap_mau || (hasWorked && workedMode !== "skip");
      if (!shouldWriteBt) {
        push(
          hasWorked
            ? "Các dạng bài tập: bỏ qua."
            : "Bài tập mẫu: gói không có phần này — giữ nguyên nội dung cũ.",
        );
      } else {
        const merged =
          hasWorked && workedMode === "overwrite"
            ? rows.baiTapMau.questions
            : hasWorked && workedMode === "merge"
              ? [...(bt?.questions ?? []), ...rows.baiTapMau.questions]
              : (bt?.questions ?? []);
        const hadBtExam = (bt?.exam_ids ?? []).length > 0;
        let btExamIds = bt?.exam_ids ?? [];
        let examNote = "";
        if (targets.bai_tap_mau) {
          if (hadBtExam && examMode === "skip") {
            examNote = " (giữ đề cũ)";
          } else {
            btExamIds = hadBtExam && examMode === "keep" ? [...btExamIds, examId] : [examId];
            examNote = ` (gắn đề ${examId})`;
          }
        }
        const payload = {
          ...rows.baiTapMau,
          questions: merged,
          exam_ids: btExamIds,
          subtitle: rows.baiTapMau.subtitle || bt?.subtitle || "",
          sort_order: bt?.sort_order ?? 3,
        };
        const r = bt
          ? await supabase.from("lesson_items").update(payload).eq("id", bt.id)
          : await supabase.from("lesson_items").insert(payload);
        if (r.error) throw new Error(`Bài tập mẫu lỗi: ${r.error.message}`);
        const workedNote = hasWorked
          ? `${bt ? (workedMode === "merge" ? "đã gộp thêm" : "đã ghi đè") : "đã thêm"} (${merged.length} dạng)`
          : bt
            ? "đã cập nhật"
            : "đã thêm";
        push(`Bài tập mẫu: ${workedNote}${examNote}.`);
      }

      // 6. luyen_tap / kiem_tra
      const subtitle = typeCountSubtitle(rows.exam.questions, rows.exam.duration_minutes);
      for (const k of ["luyen_tap", "kiem_tra"] as const) {
        if (!targets[k]) continue;
        const cur = existing(k);
        const hadExam = (cur?.exam_ids ?? []).length > 0;
        if (hadExam && examMode === "skip") {
          push(`${k}: bỏ qua (giữ đề cũ).`);
          continue;
        }
        const nextIds = hadExam && examMode === "keep" ? [...cur!.exam_ids, examId] : [examId];
        const payload = {
          lesson_id: lessonId,
          kind: k,
          title: cur?.title || (k === "luyen_tap" ? "Luyện tập" : "Kiểm tra"),
          subtitle,
          body_html: "",
          video_url: "",
          pdf_url: "",
          questions: [],
          exam_ids: nextIds,
          sort_order: cur?.sort_order ?? (k === "luyen_tap" ? 4 : 5),
        };
        const r = cur
          ? await supabase.from("lesson_items").update(payload).eq("id", cur.id)
          : await supabase.from("lesson_items").insert(payload);
        if (r.error) throw new Error(`${k} lỗi: ${r.error.message}`);
        push(`${k}: ${cur ? "đã cập nhật" : "đã thêm"} (gắn đề ${examId}).`);
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

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-display text-2xl font-bold text-white">Đăng bài học</h1>
        <p className="mt-1 text-sm text-slate-400">
          Dán lý thuyết + dạng bài (LaTeX) ở mục 2, dán/thả đề kiểu Azota ở mục 3 — cả hai đều tách lại ngay khi gõ,
          y như trang Đăng đề. Chọn lớp – bài rồi bấm Đăng.
        </p>
      </header>

      <details className="rounded-2xl border border-white/10 bg-[#0B1020] p-4 text-sm text-slate-300">
        <summary className="cursor-pointer font-medium text-slate-200">
          Nâng cao: dán gói JSON có sẵn (dành cho trợ lý AI hoặc đề PDF/ảnh scan)
        </summary>
        <p className="mt-2 text-xs text-slate-500">
          Dùng khi không gõ trực tiếp được — vd trợ lý AI đã dựng sẵn gói <code>thachlab.lesson-bundle/v1</code> từ đề
          PDF/scan. Nạp vào sẽ thay nội dung ở mục 2 và 3 bên dưới; vẫn rà/sửa lại như bình thường trước khi đăng.
        </p>
        <textarea
          value={jsonRaw}
          onChange={(e) => setJsonRaw(e.target.value)}
          rows={6}
          placeholder='{ "schema": "thachlab.lesson-bundle/v1", "theory_html": "…", "worked_examples": [...], "exam": { ... } }'
          className={`${inputCls} mt-2 w-full font-mono text-xs`}
        />
        <button
          onClick={loadJsonBundle}
          disabled={!jsonRaw.trim()}
          className="mt-2 rounded-lg bg-emerald-600/30 px-4 py-2 text-sm font-semibold text-emerald-200 hover:bg-emerald-600/50 disabled:opacity-40"
        >
          Nạp gói
        </button>
        {jsonErr.length > 0 && (
          <ul className="mt-2 rounded-lg border border-amber-500/30 bg-amber-500/5 p-3 text-xs text-amber-200">
            {jsonErr.map((e, i) => (
              <li key={i}>• {e}</li>
            ))}
          </ul>
        )}
      </details>

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

      {/* 2. Lý thuyết & dạng bài */}
      <section className="space-y-3 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <p className="text-sm font-medium text-slate-300">2. Lý thuyết & dạng bài</p>
        {theoryOverride ? (
          <div className="flex flex-wrap items-center gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-3 text-xs text-emerald-200">
            <span>Đang dùng nội dung nạp từ gói JSON (khối “Nâng cao” ở trên).</span>
            <button
              type="button"
              onClick={clearTheoryOverride}
              className="rounded-lg bg-white/10 px-3 py-1.5 font-semibold text-slate-200 hover:bg-white/20"
            >
              Quay lại dán trực tiếp
            </button>
          </div>
        ) : (
          <>
            <textarea
              value={tex}
              onChange={(e) => setTex(e.target.value)}
              rows={10}
              spellCheck={false}
              placeholder={
                "Dán LaTeX bài học vào đây — trang tách lại lý thuyết/dạng bài mỗi khi gõ.\n\n" +
                "\\subsection{LÍ THUYẾT}\n...\n\\subsection{DẠNG 1: ...}\n...\n\n" +
                "(Phần đề/luyện tập KHÔNG dán ở đây — dán ở mục 3 bên dưới, kiểu Azota.)"
              }
              className={`${inputCls} w-full min-h-[30vh] resize-y font-mono text-[13px] leading-relaxed`}
            />
            {theoryDraft && theoryDraft.notes.length > 0 && (
              <ul className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-3 text-xs text-amber-200">
                {theoryDraft.notes.map((n, i) => (
                  <li key={i}>• {n}</li>
                ))}
              </ul>
            )}
          </>
        )}

        {theoryPart.theory_html.trim() && (
          <div className="rounded-xl border border-white/10 bg-black/20 p-4">
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-blue-300">Xem trước Lý thuyết</p>
            <ContentHtml html={theoryPart.theory_html} className="block text-sm text-slate-300" />
          </div>
        )}
        {theoryPart.worked_examples.length > 0 && (
          <div className="rounded-xl border border-white/10 bg-black/20 p-4">
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-violet-300">
              Các dạng bài tập ({theoryPart.worked_examples.length})
            </p>
            <WorkedQuestionsGrid questions={theoryPart.worked_examples} />
          </div>
        )}
      </section>

      {/* 3. Đề luyện tập / kiểm tra */}
      <section className="space-y-3 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <p className="text-sm font-medium text-slate-300">3. Đề luyện tập / kiểm tra</p>
        <ExamSection
          subjectCode={subjectCode}
          topicGroups={topicGroups}
          catalogNames={catalogNames}
          lessonPicked={lessonId !== null}
          onChange={setExamBundle}
          externalSeed={examSeed}
        />
      </section>

      {/* 4. Nhãn chủ đề trước khi đăng */}
      {audit && (
        <section className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <p className="text-sm font-medium text-slate-300">4. Nhãn chủ đề trước khi đăng</p>
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
        </section>
      )}

      {/* 5. Gắn đề & xử lý nội dung cũ */}
      {fullBundle && (
        <section className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <p className="text-sm font-medium text-slate-300">5. Gắn đề & xử lý nội dung đã có</p>

          <div className="flex flex-wrap gap-4 text-sm text-slate-300">
            {(["bai_tap_mau", "luyen_tap", "kiem_tra"] as const).map((k) => (
              <label key={k} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={targets[k]}
                  onChange={(e) => setTargets((t) => ({ ...t, [k]: e.target.checked }))}
                  className="accent-emerald-500"
                />
                {k === "bai_tap_mau"
                  ? "Gắn vào Bài tập mẫu (tự chấm)"
                  : k === "luyen_tap"
                    ? "Gắn vào Luyện tập"
                    : "Gắn vào Kiểm tra"}
                {(existing(k)?.exam_ids.length ?? 0) > 0 && (
                  <span className="text-xs text-amber-300">· đã có {existing(k)!.exam_ids.length} đề</span>
                )}
              </label>
            ))}
          </div>

          <p className="text-xs text-slate-400">
            Giữ + thêm: đăng thêm đề vào bài. Thay liên kết: chỉ gắn đề mới vào mục đã chọn; đề cũ vẫn được giữ trong kho và các bài khác.
          </p>

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
                  (existing("kiem_tra")?.exam_ids.length ?? 0) > 0 ||
                  (existing("bai_tap_mau")?.exam_ids.length ?? 0) > 0
                }
                value={examMode}
                onChange={setExamMode}
                options={[["keep", "Giữ + thêm"], ["replace", "Thay liên kết"], ["skip", "Bỏ qua"]]}
              />
            </div>
          )}
        </section>
      )}

      {/* 6. Đăng */}
      <section className="space-y-3 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        {check && !check.ok && (
          <ul className="rounded-lg border border-red-500/30 bg-red-500/5 p-3 text-xs text-red-200">
            {check.errors.map((e, i) => (
              <li key={i}>✕ {e}</li>
            ))}
          </ul>
        )}
        <button
          onClick={publish}
          disabled={!canPublish}
          className="rounded-full bg-[#2563EB] px-6 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-40"
        >
          {busy ? "Đang đăng…" : "Đăng bài học"}
        </button>
        {!canPublish && fullBundle && (
          <p className="text-xs text-slate-500">
            {check && !check.ok
              ? "Sửa hết lỗi ở khung đỏ trên trước khi đăng."
              : lessonId === null
                ? "Chọn bài học ở mục 1."
                : !targets.luyen_tap && !targets.kiem_tra && !targets.bai_tap_mau
                  ? "Chọn ít nhất một mục để gắn đề ở mục 5."
                  : !tagsReady && !tagOverride
                    ? "Nhãn chủ đề ở mục 4 chưa đủ — sửa nhãn trong đề, hoặc tick ô cho phép đăng."
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
