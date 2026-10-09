"use client";

import ForYouRow from "@/components/mastery/ForYouRow";
import { useEffect, useMemo, useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useAuth } from "@/components/auth/AuthProvider";
import RequireAuth from "@/components/auth/RequireAuth";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type { Difficulty, SchoolClass } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import type { Chapter } from "@/features/lessons/types";
import { isPeriodicExam } from "@/features/lessons/types";
import { displayClassesByGrade, expandClassIdsByGrade } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { fetchExamsFull, type LessonWithItemRefs } from "@/services/lessons";
import { fetchLearnedLessonIds } from "@/services/progress";
import { fetchChaptersStatic, fetchClassesStatic, fetchLessonsStatic } from "@/services/static-content";
import { supabaseConfigured } from "@/services/supabase";

// Modal luyện: cùng chunk lazy với thẻ mastery ở trang bài học (perf4) — không vào JS ban đầu.
const PracticeModalLazy = dynamic(() => import("@/components/mastery/TopicPracticeModal"), {
  ssr: false,
  loading: () => null,
});

function PracticeModal(props: ComponentProps<typeof PracticeModalLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div role="alertdialog" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="max-w-sm rounded-2xl border border-white/10 bg-panel p-5 text-center text-sm text-slate-300">
            <p>Không tải được phần luyện tập (có thể do mạng chập chờn). Thử tải lại trang.</p>
            <button
              type="button"
              onClick={props.onClose}
              className="mt-3 rounded-full border border-white/15 px-4 py-1.5 text-xs font-semibold text-white hover:border-white/30"
            >
              Đóng
            </button>
          </div>
        </div>
      }
    >
      <PracticeModalLazy {...props} />
    </LazyErrorBoundary>
  );
}

const LEVELS: Difficulty[] = ["de", "trung-binh", "kho"];
const NO_EXAMS: number[] = [];
const REVIEW_COUNTS = [10, 20, 30] as const;
type Mode = "single" | "review";

const lessonExamIds = (l: LessonWithItemRefs) => Array.from(new Set(l.itemRefs.flatMap((r) => r.exam_ids)));

interface PoolStats {
  topics: { name: string; total: number }[];
  /** Đếm câu theo mức, áp dụng bộ lọc YCCĐ đang chọn. */
  byLevel: Record<"de" | "trung-binh" | "kho", number>;
  total: number;
}

const selectCls =
  "w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-white/30 focus:outline-none";

function Content() {
  const { session } = useAuth();
  const [mode, setMode] = useState<Mode>("single");
  const [learned, setLearned] = useState<Set<number> | null>(null);
  // null = em chưa tự chọn gì → dùng mặc định "các bài đã học"; có giá trị = em đã chỉnh tay.
  const [selected, setSelected] = useState<Set<number> | null>(null);
  const [reviewCount, setReviewCount] = useState<(typeof REVIEW_COUNTS)[number]>(20);
  // Ảnh chụp lựa chọn lúc bấm nút: đổi chọn/tải xong dữ liệu khi modal đang mở không làm bốc lại câu.
  const [reviewRun, setReviewRun] = useState<{ byLesson: Record<number, number[]>; count: number } | null>(null);
  const [soloLessonId, setSoloLessonId] = useState<number | null>(null);
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<LessonWithItemRefs[] | null>(null);
  const [classId, setClassId] = useState<number | null>(null);
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [lessonId, setLessonId] = useState<number | null>(null);
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState<Difficulty>("");
  const [pool, setPool] = useState<{ topic: string; difficulty: Difficulty }[] | null>(null);
  const [poolError, setPoolError] = useState(false);
  const [practicing, setPracticing] = useState(false);

  useEffect(() => {
    if (!supabaseConfigured) return;
    fetchClassesStatic(setClasses).then(setClasses);
    fetchChaptersStatic(setChapters).then(setChapters);
    fetchLessonsStatic(setLessons).then(setLessons);
  }, []);

  const displayClasses = useMemo(() => (classes ? displayClassesByGrade(classes) : []), [classes]);
  const activeClassId = classId ?? displayClasses[0]?.id ?? null;

  const classChapters = useMemo(() => {
    if (!classes || !chapters || activeClassId === null) return [];
    const ids = expandClassIdsByGrade([activeClassId], classes);
    return chapters.filter((c) => c.subjectCode === "vat-ly" && visibleTo(c.classIds, ids));
  }, [classes, chapters, activeClassId]);

  const chapterLessons = useMemo(
    () =>
      (lessons ?? []).filter(
        (l) => l.chapter_id === chapterId && l.published && !isPeriodicExam(l.lesson_kind),
      ),
    [lessons, chapterId],
  );

  const lesson = chapterLessons.find((l) => l.id === lessonId) ?? null;
  const examIds = useMemo(
    () => (lesson ? Array.from(new Set(lesson.itemRefs.flatMap((r) => r.exam_ids))) : []),
    [lesson],
  );

  // Nạp câu của bài đã chọn để biết bài có những YCCĐ / mức nào (1 truy vấn `exams`, cùng
  // nguồn với "Luyện 10 câu phần này" ở trang bài học).
  useEffect(() => {
    if (examIds.length === 0) return;
    let cancelled = false;
    fetchExamsFull(examIds)
      .then((metas) => {
        if (cancelled) return;
        const rows: { topic: string; difficulty: Difficulty }[] = [];
        for (const id of examIds) {
          for (const q of metas.get(id)?.questions ?? []) {
            if (q.type === "essay") continue;
            rows.push({ topic: (q.topic ?? "").trim(), difficulty: q.difficulty ?? "" });
          }
        }
        setPool(rows);
      })
      .catch(() => !cancelled && setPoolError(true));
    return () => {
      cancelled = true;
    };
  }, [examIds]);

  // Đổi bài -> xoá lựa chọn cũ ngay trong handler (không setState trong effect).
  function pickLesson(id: number | null) {
    setLessonId(id);
    setTopic("");
    setLevel("");
    setPool(null);
    setPoolError(false);
  }

  const stats = useMemo<PoolStats | null>(() => {
    const rows = examIds.length === 0 ? [] : pool;
    if (!rows) return null;
    const topicCount = new Map<string, number>();
    for (const r of rows) if (r.topic) topicCount.set(r.topic, (topicCount.get(r.topic) ?? 0) + 1);
    const inTopic = rows.filter((r) => !topic || r.topic === topic);
    const byLevel = { de: 0, "trung-binh": 0, kho: 0 };
    for (const r of inTopic) if (r.difficulty in byLevel) byLevel[r.difficulty as keyof typeof byLevel] += 1;
    return {
      topics: [...topicCount].map(([name, total]) => ({ name, total })),
      byLevel,
      total: inTopic.length,
    };
  }, [examIds, pool, topic]);

  const available = !stats ? 0 : level ? stats.byLevel[level as keyof PoolStats["byLevel"]] : stats.total;

  // ---- Ôn tổng hợp: các chương của lớp → bài (bài chưa có đề thì mờ, không chọn được) ----
  const reviewGroups = useMemo(
    () =>
      classChapters
        .map((c) => ({
          chapter: c,
          lessons: (lessons ?? [])
            .filter((l) => l.chapter_id === c.id && l.published && !isPeriodicExam(l.lesson_kind))
            .map((l) => ({ lesson: l, examIds: lessonExamIds(l) })),
        }))
        .filter((g) => g.lessons.length > 0),
    [classChapters, lessons],
  );
  const reviewable = useMemo(
    () => reviewGroups.flatMap((g) => g.lessons).filter((x) => x.examIds.length > 0),
    [reviewGroups],
  );
  const learnedReviewable = useMemo(
    () => reviewable.filter((x) => learned?.has(x.lesson.id)),
    [reviewable, learned],
  );
  const effectiveSelected = useMemo(
    () => selected ?? new Set(learnedReviewable.map((x) => x.lesson.id)),
    [selected, learnedReviewable],
  );
  const pickedLessons = reviewable.filter((x) => effectiveSelected.has(x.lesson.id));
  const lessonTitles = useMemo(
    () => Object.fromEntries((lessons ?? []).map((l) => [l.id, l.title])),
    [lessons],
  );
  const soloExamIds = useMemo(() => {
    const l = (lessons ?? []).find((x) => x.id === soloLessonId);
    return l ? lessonExamIds(l) : [];
  }, [lessons, soloLessonId]);

  function openMode(next: Mode) {
    setMode(next);
    if (next === "review" && learned === null && session) {
      fetchLearnedLessonIds(session.user.id).then(setLearned);
    }
  }
  function toggleLesson(id: number) {
    const next = new Set(effectiveSelected);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelected(next);
  }
  function selectChapter(ids: number[]) {
    setSelected(new Set([...effectiveSelected, ...ids]));
  }
  function selectRecent() {
    // "Gần nhất" theo thứ tự chương trình (chưa có mốc thời gian học trong dữ liệu đã tải).
    setSelected(new Set(learnedReviewable.slice(-3).map((x) => x.lesson.id)));
  }

  return (
    <div className="mx-auto w-full max-w-2xl px-4 pb-20 pt-28 sm:px-6">
      <h1 className="font-display text-2xl font-semibold text-white">Luyện tập theo yêu cầu cần đạt</h1>
      <p className="mt-1 text-sm text-slate-400">
        Chọn bài, yêu cầu cần đạt và mức độ để luyện đúng chỗ còn thiếu danh hiệu. Câu đã giải đúng rồi không
        được tính lại cho danh hiệu — làm câu mới mới tiến thêm.
      </p>

      {session && <ForYouRow />}

      <div role="tablist" aria-label="Kiểu luyện tập" className="mt-5 grid grid-cols-2 gap-2">
        {(
          [
            ["single", "Theo yêu cầu"],
            ["review", "Ôn tổng hợp"],
          ] as [Mode, string][]
        ).map(([m, text]) => (
          <button
            key={m}
            type="button"
            role="tab"
            aria-selected={mode === m}
            onClick={() => openMode(m)}
            className={`min-h-11 rounded-xl border px-3 text-sm font-semibold ${
              mode === m ? "border-white/60 bg-white/10 text-white" : "border-white/15 text-slate-300 hover:border-white/30"
            }`}
          >
            {text}
          </button>
        ))}
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <label className="text-xs text-slate-400">
          Lớp
          <select
            className={selectCls}
            value={activeClassId ?? ""}
            onChange={(e) => {
              setClassId(Number(e.target.value));
              setChapterId(null);
              setSelected(null);
              pickLesson(null);
            }}
          >
            {displayClasses.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
        <label className={`text-xs text-slate-400 ${mode === "review" ? "hidden" : ""}`}>
          Chương
          <select
            className={selectCls}
            value={chapterId ?? ""}
            onChange={(e) => {
              setChapterId(e.target.value ? Number(e.target.value) : null);
              pickLesson(null);
            }}
          >
            <option value="">— Chọn chương —</option>
            {classChapters.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
        </label>
        <label className={`text-xs text-slate-400 sm:col-span-2 ${mode === "review" ? "hidden" : ""}`}>
          Bài
          <select
            className={selectCls}
            value={lessonId ?? ""}
            disabled={!chapterId}
            onChange={(e) => pickLesson(e.target.value ? Number(e.target.value) : null)}
          >
            <option value="">— Chọn bài —</option>
            {chapterLessons.map((l) => (
              <option key={l.id} value={l.id}>
                {l.title}
              </option>
            ))}
          </select>
        </label>
      </div>

      {mode === "review" && (
        <div className="mt-5 space-y-5">
          {reviewGroups.map((g) => {
            const ready = g.lessons.filter((x) => x.examIds.length > 0).map((x) => x.lesson.id);
            return (
              <section key={g.chapter.id}>
                <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                  <h2 className="text-sm font-semibold text-white">{g.chapter.title}</h2>
                  {ready.length > 0 && (
                    <button
                      type="button"
                      onClick={() => selectChapter(ready)}
                      className="min-h-11 px-2 text-[13px] font-semibold text-slate-300 hover:text-white"
                    >
                      Cả chương
                    </button>
                  )}
                </div>
                <div className="flex flex-wrap gap-2">
                  {g.lessons.map(({ lesson: l, examIds: ids }) => {
                    const empty = ids.length === 0;
                    const on = effectiveSelected.has(l.id) && !empty;
                    return (
                      <button
                        key={l.id}
                        type="button"
                        disabled={empty}
                        aria-pressed={on}
                        onClick={() => toggleLesson(l.id)}
                        className={`min-h-11 rounded-full border px-4 py-2 text-left text-[13px] font-semibold ${
                          on
                            ? "border-white/60 bg-white/10 text-white"
                            : "border-white/15 text-slate-300 hover:border-white/30"
                        } ${empty ? "cursor-not-allowed opacity-40" : ""}`}
                      >
                        {on ? "✓ " : ""}
                        {l.title}
                        {empty && <span className="ml-1.5 font-normal text-slate-400">· chưa có câu</span>}
                      </button>
                    );
                  })}
                </div>
              </section>
            );
          })}
          {lessons && reviewGroups.length === 0 && (
            <p className="text-sm text-slate-400">Lớp này chưa có bài để ôn.</p>
          )}
          {learned !== null && learnedReviewable.length === 0 && selected === null && reviewable.length > 0 && (
            <p className="text-[13px] text-slate-400">Em chưa học bài nào của lớp này — chọn các bài muốn ôn nhé.</p>
          )}

          <div className="space-y-3 rounded-2xl border border-white/10 bg-panel/60 p-4">
            <div className="flex flex-wrap gap-2">
              {learnedReviewable.length > 0 && (
                <button
                  type="button"
                  onClick={selectRecent}
                  className="min-h-11 rounded-full border border-white/15 px-4 text-[13px] font-semibold text-slate-300 hover:border-white/30"
                >
                  3 bài gần nhất
                </button>
              )}
              <button
                type="button"
                onClick={() => setSelected(new Set())}
                className="min-h-11 rounded-full border border-white/15 px-4 text-[13px] font-semibold text-slate-300 hover:border-white/30"
              >
                Bỏ chọn hết
              </button>
            </div>
            <div>
              <p className="mb-1.5 text-[13px] text-slate-400">Số câu</p>
              <div className="flex gap-2">
                {REVIEW_COUNTS.map((n) => (
                  <button
                    key={n}
                    type="button"
                    aria-pressed={reviewCount === n}
                    onClick={() => setReviewCount(n)}
                    className={`min-h-11 flex-1 rounded-full border text-sm font-semibold ${
                      reviewCount === n
                        ? "border-white/60 bg-white/10 text-white"
                        : "border-white/15 text-slate-300 hover:border-white/30"
                    }`}
                  >
                    {n}
                  </button>
                ))}
              </div>
            </div>
            <button
              type="button"
              disabled={pickedLessons.length === 0}
              onClick={() =>
                setReviewRun({
                  byLesson: Object.fromEntries(pickedLessons.map((x) => [x.lesson.id, x.examIds])),
                  count: reviewCount,
                })
              }
              className="min-h-11 w-full rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-40"
            >
              {pickedLessons.length === 0 ? "Chọn ít nhất 1 bài" : `Làm ${reviewCount} câu từ ${pickedLessons.length} bài`}
            </button>
          </div>
        </div>
      )}

      {mode === "single" && lesson && (
        <div className="mt-5 space-y-4 rounded-2xl border border-white/10 bg-panel/60 p-4">
          {poolError && <p className="text-sm text-amber-300">Chưa tải được câu hỏi của bài, thử tải lại trang.</p>}
          {!poolError && !stats && <p className="text-sm text-slate-400">Đang tải câu hỏi của bài…</p>}
          {stats && stats.total === 0 && !topic && (
            <p className="text-sm text-slate-300">Bài này chưa có câu trắc nghiệm để luyện.</p>
          )}
          {stats && (stats.total > 0 || topic) && (
            <>
              <label className="block text-xs text-slate-400">
                Yêu cầu cần đạt
                <select className={selectCls} value={topic} onChange={(e) => setTopic(e.target.value)}>
                  <option value="">Tất cả yêu cầu của bài</option>
                  {stats.topics.map((t) => (
                    <option key={t.name} value={t.name}>
                      {t.name} ({t.total} câu)
                    </option>
                  ))}
                </select>
              </label>
              <div>
                <p className="mb-1.5 text-xs text-slate-400">Mức độ</p>
                <div className="flex flex-wrap gap-2">
                  {(["", ...LEVELS] as Difficulty[]).map((lv) => {
                    const n = lv ? stats.byLevel[lv as keyof PoolStats["byLevel"]] : stats.total;
                    const on = level === lv;
                    return (
                      <button
                        key={lv || "all"}
                        type="button"
                        onClick={() => setLevel(lv)}
                        aria-pressed={on}
                        className={`rounded-full border px-3 py-1.5 text-xs font-semibold ${
                          on ? "border-white/60 bg-white/10 text-white" : "border-white/15 text-slate-300 hover:border-white/30"
                        }`}
                      >
                        {lv ? DIFFICULTY_LABELS[lv] : "Mọi mức"} · {n}
                      </button>
                    );
                  })}
                </div>
              </div>
              <button
                type="button"
                disabled={available === 0}
                onClick={() => setPracticing(true)}
                className="w-full rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-black disabled:cursor-not-allowed disabled:opacity-40"
              >
                {available === 0 ? "Chưa có câu phù hợp" : `Luyện ${Math.min(10, available)} câu`}
              </button>
            </>
          )}
        </div>
      )}

      {reviewRun && (
        <PracticeModal
          lessonId={null}
          examIds={NO_EXAMS}
          topicName=""
          count={reviewRun.count}
          examIdsByLesson={reviewRun.byLesson}
          lessonTitles={lessonTitles}
          onPickLesson={(id) => {
            setReviewRun(null);
            setSoloLessonId(id);
          }}
          onClose={() => setReviewRun(null)}
        />
      )}

      {soloLessonId !== null && (
        <PracticeModal
          lessonId={soloLessonId}
          examIds={soloExamIds}
          topicName=""
          onClose={() => setSoloLessonId(null)}
        />
      )}

      {practicing && mode === "single" && lesson && (
        <PracticeModal
          lessonId={lesson.id}
          examIds={examIds}
          topicName={topic}
          difficulty={level || undefined}
          onClose={() => setPracticing(false)}
        />
      )}
    </div>
  );
}

export default function LuyenTapPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full">
        {!supabaseConfigured ? (
          <p className="pt-28 text-center text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : (
          <RequireAuth>
            <Content />
          </RequireAuth>
        )}
      </main>
      <Footer variant="app" />
    </>
  );
}
