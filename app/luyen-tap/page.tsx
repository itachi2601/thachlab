"use client";

import ForYouRow from "@/components/mastery/ForYouRow";
import LateNightNudge from "@/components/rank/LateNightNudge";
import MistakeVaultCard from "@/components/rank/MistakeVaultCard";
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
import { displayClassesByGrade, expandClassIdsByGrade, fetchMyClassIds } from "@/services/classes";
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
          <div className="max-w-sm rounded-2xl border border-line bg-panel p-5 text-center text-sm text-ink">
            <p>Không tải được phần luyện tập (có thể do mạng chập chờn). Thử tải lại trang.</p>
            <button
              type="button"
              onClick={props.onClose}
              className="mt-3 rounded-full border border-line px-4 py-1.5 text-xs font-semibold text-ink hover:border-line-strong"
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
type Mode = "single" | "quiz15" | "term";
const MODES: [Mode, string][] = [
  ["single", "Theo bài"],
  ["quiz15", "Kiểm tra 15'"],
  ["term", "Ôn thi HK"],
];
/** Đề tự tạo cho ôn thi học kì: số câu + thời gian như đề thật (28 câu · 45 phút là cấu trúc đề HK hiện hành). */
const TERM_SIZES = [
  { count: 20, minutes: 30 },
  { count: 28, minutes: 45 },
] as const;
const QUIZ15 = { count: 10, minutes: 15 };
const TERM_KINDS = new Set(["kiem_tra_giua_ki", "kiem_tra_cuoi_ki"]);

const lessonExamIds = (l: LessonWithItemRefs) => Array.from(new Set(l.itemRefs.flatMap((r) => r.exam_ids)));

interface PoolStats {
  topics: { name: string; total: number }[];
  /** Đếm câu theo mức, áp dụng bộ lọc YCCĐ đang chọn. */
  byLevel: Record<"de" | "trung-binh" | "kho", number>;
  total: number;
}

interface Run {
  byLesson: Record<number, number[]>;
  count: number;
  minutes?: number;
  heading: string;
}

const selectCls =
  "w-full rounded-xl border border-line-strong bg-panel px-3 py-2 text-sm text-ink focus:border-primary focus:outline-none";
/** Nút bắt đầu dính đáy (trên thanh tab điện thoại), chừa góc phải cho nút báo lỗi nổi — danh sách bài dài
 *  thì nút vẫn trong vùng ngón cái (D3), không phải cuộn hết các chương mới bấm được. */
const stickyStartCls = "sticky bottom-[calc(64px+env(safe-area-inset-bottom,0px))] z-10 mr-16 lg:bottom-4 lg:mr-0";
const startBtnCls =
  "min-h-11 w-full rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white shadow-lg disabled:cursor-not-allowed disabled:border disabled:border-line disabled:bg-panel disabled:text-muted! disabled:shadow-none";
const chipCls = (on: boolean) =>
  `min-h-11 rounded-full border px-4 py-2 text-left text-[13px] font-semibold ${
    on ? "border-primary bg-primary-soft text-ink" : "border-line text-ink hover:border-line-strong"
  }`;

interface ReviewGroup {
  chapter: Chapter;
  lessons: { lesson: LessonWithItemRefs; examIds: number[] }[];
}

/** Chọn nhiều bài theo chương (dùng chung cho Kiểm tra 15' và Ôn thi HK). Bài chưa có câu thì ẩn. */
function LessonPicker({
  groups,
  selected,
  onToggle,
  onChapter,
}: {
  groups: ReviewGroup[];
  selected: Set<number>;
  onToggle: (id: number) => void;
  onChapter: (ids: number[]) => void;
}) {
  return (
    <div className="space-y-5">
      {groups.map((g) => (
        <section key={g.chapter.id}>
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
            <h3 className="text-sm font-semibold text-ink">{g.chapter.title}</h3>
            <button
              type="button"
              onClick={() => onChapter(g.lessons.map((x) => x.lesson.id))}
              className="min-h-11 px-2 text-[13px] font-semibold text-ink hover:text-primary"
            >
              Cả chương
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {g.lessons.map(({ lesson: l }) => {
              const on = selected.has(l.id);
              return (
                <button
                  key={l.id}
                  type="button"
                  aria-pressed={on}
                  onClick={() => onToggle(l.id)}
                  className={chipCls(on)}
                >
                  {on ? "✓ " : ""}
                  {l.title}
                </button>
              );
            })}
          </div>
        </section>
      ))}
    </div>
  );
}

function Content() {
  const { session, profile } = useAuth();
  const [mode, setMode] = useState<Mode>("single");
  const [learned, setLearned] = useState<Set<number> | null>(null);
  const [myClassIds, setMyClassIds] = useState<number[] | null>(null);
  // null = em chưa tự chọn gì → dùng mặc định; có giá trị = em đã chỉnh tay. Mỗi chế độ giữ lựa chọn riêng.
  const [picked15, setPicked15] = useState<Set<number> | null>(null);
  const [pickedTerm, setPickedTerm] = useState<Set<number> | null>(null);
  const [termSize, setTermSize] = useState<(typeof TERM_SIZES)[number]>(TERM_SIZES[1]);
  const [timed, setTimed] = useState(true);
  // Ảnh chụp lựa chọn lúc bấm nút: đổi chọn/tải xong dữ liệu khi modal đang mở không làm bốc lại câu.
  const [run, setRun] = useState<Run | null>(null);
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

  const userId = session?.user.id ?? null;
  const isStudent = profile?.role === "student";
  useEffect(() => {
    if (!userId) return;
    if (isStudent) fetchMyClassIds(userId).then(setMyClassIds);
    fetchLearnedLessonIds(userId).then(setLearned);
  }, [userId, isStudent]);

  // Học sinh chỉ thấy khối lớp mình đang học (đề gán theo lớp, chọn lớp khác chỉ gặp bài "trống").
  // Giáo viên/trợ giảng, hoặc em chưa vào lớp nào, thấy mọi lớp.
  const displayClasses = useMemo(() => {
    if (!classes) return [];
    const all = displayClassesByGrade(classes);
    if (!isStudent) return all;
    if (myClassIds === null) return []; // đang tải lớp của em: chưa hiện gì, tránh nháy sang khối khác
    if (myClassIds.length === 0) return all;
    const mine = new Set(expandClassIdsByGrade(myClassIds, classes) ?? []);
    const own = all.filter((c) => mine.has(c.id));
    return own.length > 0 ? own : all;
  }, [classes, isStudent, myClassIds]);
  const activeClassId =
    classId !== null && displayClasses.some((c) => c.id === classId) ? classId : (displayClasses[0]?.id ?? null);

  const classChapters = useMemo(() => {
    if (!classes || !chapters || activeClassId === null) return [];
    const ids = expandClassIdsByGrade([activeClassId], classes);
    return chapters.filter((c) => c.subjectCode === "vat-ly" && visibleTo(c.classIds, ids));
  }, [classes, chapters, activeClassId]);

  const chapterLessons = useMemo(
    () => (lessons ?? []).filter((l) => l.chapter_id === chapterId && l.published && !isPeriodicExam(l.lesson_kind)),
    [lessons, chapterId],
  );

  const lesson = chapterLessons.find((l) => l.id === lessonId) ?? null;
  const examIds = useMemo(() => (lesson ? lessonExamIds(lesson) : []), [lesson]);

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
            rows.push({
              topic: (q.topic ?? "").trim(),
              difficulty: q.difficulty ?? "",
            });
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
  // Chỉ hiện bộ lọc khi thật sự có gì để lọc: ≥2 YCCĐ, ≥2 mức có câu (N3 — không hiện lựa chọn rỗng).
  const levelsWithQuestions = stats ? LEVELS.filter((lv) => stats.byLevel[lv as keyof PoolStats["byLevel"]] > 0) : [];
  const showTopics = !!stats && stats.topics.length >= 2;
  const showLevels = levelsWithQuestions.length >= 2;

  // ---- Kiểm tra 15' / Ôn thi HK: các chương của lớp → bài có câu để bốc ----
  const reviewGroups = useMemo<ReviewGroup[]>(
    () =>
      classChapters
        .map((c) => ({
          chapter: c,
          lessons: (lessons ?? [])
            .filter((l) => l.chapter_id === c.id && l.published && !isPeriodicExam(l.lesson_kind))
            .map((l) => ({ lesson: l, examIds: lessonExamIds(l) }))
            .filter((x) => x.examIds.length > 0),
        }))
        .filter((g) => g.lessons.length > 0),
    [classChapters, lessons],
  );
  const reviewable = useMemo(() => reviewGroups.flatMap((g) => g.lessons), [reviewGroups]);
  const learnedReviewable = useMemo(() => reviewable.filter((x) => learned?.has(x.lesson.id)), [reviewable, learned]);
  // Mặc định: kiểm tra 15' thường hỏi 1–2 bài vừa học; ôn thi HK lấy mọi bài đã học.
  const sel15 = useMemo(
    () => picked15 ?? new Set(learnedReviewable.slice(-2).map((x) => x.lesson.id)),
    [picked15, learnedReviewable],
  );
  const selTerm = useMemo(
    () => pickedTerm ?? new Set(learnedReviewable.map((x) => x.lesson.id)),
    [pickedTerm, learnedReviewable],
  );
  const termLessons = useMemo(
    () =>
      classChapters.flatMap((c) =>
        (lessons ?? [])
          .filter((l) => l.chapter_id === c.id && l.published && TERM_KINDS.has(l.lesson_kind))
          .map((l) => ({ lesson: l, count: lessonExamIds(l).length }))
          .filter((x) => x.count > 0),
      ),
    [classChapters, lessons],
  );
  const lessonTitles = useMemo(() => Object.fromEntries((lessons ?? []).map((l) => [l.id, l.title])), [lessons]);
  const soloExamIds = useMemo(() => {
    const l = (lessons ?? []).find((x) => x.id === soloLessonId);
    return l ? lessonExamIds(l) : [];
  }, [lessons, soloLessonId]);

  const toggleIn = (cur: Set<number>, set: (s: Set<number>) => void) => (id: number) => {
    const next = new Set(cur);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    set(next);
  };
  const addAll = (cur: Set<number>, set: (s: Set<number>) => void) => (ids: number[]) => set(new Set([...cur, ...ids]));

  function startRun(sel: Set<number>, count: number, heading: string, minutes?: number) {
    const chosen = reviewable.filter((x) => sel.has(x.lesson.id));
    setRun({
      byLesson: Object.fromEntries(chosen.map((x) => [x.lesson.id, x.examIds])),
      count,
      minutes,
      heading,
    });
  }

  const noLessonsNote = lessons && reviewGroups.length === 0 && (
    <p className="text-sm text-muted">Lớp này chưa có bài có câu hỏi để ôn.</p>
  );
  // Chỉ nhắc khi em chưa tự chọn bài nào (mặc định rỗng vì chưa học bài nào).
  const notLearnedNote = (picked: Set<number> | null) =>
    picked === null &&
    learned !== null &&
    learnedReviewable.length === 0 &&
    reviewable.length > 0 && (
      <p className="text-[13px] text-muted">Em chưa học bài nào của lớp này, hãy chọn các bài muốn ôn.</p>
    );

  return (
    <div className="mx-auto w-full max-w-2xl px-4 pb-28 pt-28 sm:px-6">
      <h1 className="font-display text-2xl font-semibold text-ink">Luyện tập</h1>
      <p className="mt-1 text-sm text-muted">Chỗ ôn tập chính: kỹ năng em yếu nhất, Kho bẫy câu em từng sai, rồi luyện theo bài, bài 15 phút hoặc ôn thi học kì.</p>

      {session && (
        <div className="mt-4 space-y-4">
          <LateNightNudge />
          <ForYouRow />
          <MistakeVaultCard />
        </div>
      )}

      <div role="tablist" aria-label="Kiểu luyện tập" className="mt-5 grid grid-cols-3 gap-2">
        {MODES.map(([m, text]) => (
          <button
            key={m}
            type="button"
            role="tab"
            aria-selected={mode === m}
            onClick={() => setMode(m)}
            className={`min-h-11 rounded-xl border px-2 text-sm font-semibold ${
              mode === m ? "border-primary bg-primary-soft text-ink" : "border-line text-ink hover:border-line-strong"
            }`}
          >
            {text}
          </button>
        ))}
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {displayClasses.length > 1 && (
          <label className="text-xs text-muted">
            Lớp
            <select
              className={selectCls}
              value={activeClassId ?? ""}
              onChange={(e) => {
                setClassId(Number(e.target.value));
                setChapterId(null);
                setPicked15(null);
                setPickedTerm(null);
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
        )}
        {mode === "single" && (
          <>
            <label className="text-xs text-muted">
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
            <label className="text-xs text-muted sm:col-span-2">
              Bài
              <select
                className={selectCls}
                value={lessonId ?? ""}
                disabled={!chapterId}
                onChange={(e) => pickLesson(e.target.value ? Number(e.target.value) : null)}
              >
                <option value="">— Chọn bài —</option>
                {chapterLessons.map((l) => {
                  const empty = lessonExamIds(l).length === 0;
                  return (
                    <option key={l.id} value={l.id} disabled={empty}>
                      {l.title}
                      {empty ? " (chưa có câu)" : ""}
                    </option>
                  );
                })}
              </select>
            </label>
          </>
        )}
      </div>

      {mode === "quiz15" && (
        <div className="mt-5 space-y-5">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm text-ink">
              {QUIZ15.count} câu, {QUIZ15.minutes} phút, bốc từ các bài em chọn. Thường là 1–2 bài vừa học.
            </p>
            {sel15.size > 0 && (
              <button
                type="button"
                onClick={() => setPicked15(new Set())}
                className="min-h-11 px-2 text-[13px] font-semibold text-muted hover:text-ink"
              >
                Bỏ chọn hết
              </button>
            )}
          </div>
          {noLessonsNote}
          {notLearnedNote(picked15)}
          <LessonPicker
            groups={reviewGroups}
            selected={sel15}
            onToggle={toggleIn(sel15, setPicked15)}
            onChapter={addAll(sel15, setPicked15)}
          />
          <div className={stickyStartCls}>
            <button
              type="button"
              disabled={sel15.size === 0}
              onClick={() => startRun(sel15, QUIZ15.count, "Kiểm tra 15 phút", QUIZ15.minutes)}
              className={startBtnCls}
            >
              {sel15.size === 0 ? "Chọn ít nhất 1 bài" : `Bắt đầu: ${QUIZ15.count} câu · ${QUIZ15.minutes} phút`}
            </button>
          </div>
        </div>
      )}

      {mode === "term" && (
        <div className="mt-5 space-y-6">
          {termLessons.length > 0 && (
            <section>
              <h2 className="text-sm font-semibold text-ink">Đề thi thật</h2>
              <p className="mt-0.5 text-[13px] text-muted">Đề giữa kì, cuối kì các trường đã dùng, có bấm giờ.</p>
              <ul className="mt-2 space-y-2">
                {termLessons.map(({ lesson: l, count }) => (
                  <li key={l.id}>
                    <a
                      href={`/lop-hoc/bai?id=${l.id}`}
                      className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-line px-4 py-2.5 text-sm font-semibold text-ink hover:border-line-strong"
                    >
                      <span>{l.title}</span>
                      <span className="shrink-0 text-[13px] font-normal text-muted">{count} đề ›</span>
                    </a>
                  </li>
                ))}
              </ul>
            </section>
          )}

          <section className="space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <h2 className="text-sm font-semibold text-ink">Tự tạo đề từ các bài em chọn</h2>
                <p className="mt-0.5 text-[13px] text-muted">Mặc định là các bài em đã học.</p>
              </div>
              {selTerm.size > 0 && (
                <button
                  type="button"
                  onClick={() => setPickedTerm(new Set())}
                  className="min-h-11 px-2 text-[13px] font-semibold text-muted hover:text-ink"
                >
                  Bỏ chọn hết
                </button>
              )}
            </div>
            <div className="flex gap-2">
              {TERM_SIZES.map((sz) => (
                <button
                  key={sz.count}
                  type="button"
                  aria-pressed={termSize.count === sz.count}
                  onClick={() => setTermSize(sz)}
                  className={`min-h-11 flex-1 rounded-full border text-sm font-semibold ${
                    termSize.count === sz.count
                      ? "border-primary bg-primary-soft text-ink"
                      : "border-line text-ink hover:border-line-strong"
                  }`}
                >
                  {sz.count} câu · {sz.minutes} phút
                </button>
              ))}
            </div>
            <label className="flex min-h-11 items-center gap-2 text-sm text-ink">
              <input
                type="checkbox"
                checked={timed}
                onChange={(e) => setTimed(e.target.checked)}
                className="h-5 w-5 accent-[var(--color-primary)]"
              />
              Bấm giờ như thi thật
            </label>
            {noLessonsNote}
            {notLearnedNote(pickedTerm)}
            <LessonPicker
              groups={reviewGroups}
              selected={selTerm}
              onToggle={toggleIn(selTerm, setPickedTerm)}
              onChapter={addAll(selTerm, setPickedTerm)}
            />
            <div className={stickyStartCls}>
              <button
                type="button"
                disabled={selTerm.size === 0}
                onClick={() => startRun(selTerm, termSize.count, "Ôn thi học kì", timed ? termSize.minutes : undefined)}
                className={startBtnCls}
              >
                {selTerm.size === 0 ? "Chọn ít nhất 1 bài" : `Làm ${termSize.count} câu từ ${selTerm.size} bài`}
              </button>
            </div>
          </section>
        </div>
      )}

      {mode === "single" && lesson && (
        <div className="mt-5 space-y-4 rounded-2xl border border-line bg-panel/60 p-4">
          {poolError && <p className="text-sm text-amber-300">Chưa tải được câu hỏi của bài, thử tải lại trang.</p>}
          {!poolError && !stats && <p className="text-sm text-muted">Đang tải câu hỏi của bài…</p>}
          {stats && stats.total === 0 && !topic && (
            <p className="text-sm text-ink">Bài này chưa có câu trắc nghiệm để luyện.</p>
          )}
          {stats && (stats.total > 0 || topic) && (
            <>
              {showTopics && (
                <label className="block text-xs text-muted">
                  Phần muốn luyện
                  <select className={selectCls} value={topic} onChange={(e) => setTopic(e.target.value)}>
                    <option value="">Cả bài</option>
                    {stats.topics.map((t) => (
                      <option key={t.name} value={t.name}>
                        {t.name} ({t.total} câu)
                      </option>
                    ))}
                  </select>
                </label>
              )}
              {showLevels && (
                <div>
                  <p className="mb-1.5 text-xs text-muted">Mức độ</p>
                  <div className="flex flex-wrap gap-2">
                    {(["", ...levelsWithQuestions] as Difficulty[]).map((lv) => {
                      const n = lv ? stats.byLevel[lv as keyof PoolStats["byLevel"]] : stats.total;
                      const on = level === lv;
                      return (
                        <button
                          key={lv || "all"}
                          type="button"
                          onClick={() => setLevel(lv)}
                          aria-pressed={on}
                          className={`min-h-11 rounded-full border px-4 text-[13px] font-semibold ${
                            on
                              ? "border-primary bg-primary-soft text-ink"
                              : "border-line text-ink hover:border-line-strong"
                          }`}
                        >
                          {lv ? DIFFICULTY_LABELS[lv] : "Mọi mức"} · {n}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}
              <button
                type="button"
                disabled={available === 0}
                onClick={() => setPracticing(true)}
                className="min-h-11 w-full rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40"
              >
                {available === 0 ? "Chưa có câu phù hợp" : `Luyện ${Math.min(10, available)} câu`}
              </button>
            </>
          )}
        </div>
      )}

      {run && (
        <PracticeModal
          lessonId={null}
          examIds={NO_EXAMS}
          topicName=""
          count={run.count}
          heading={run.heading}
          timeLimitMinutes={run.minutes}
          examIdsByLesson={run.byLesson}
          lessonTitles={lessonTitles}
          onPickLesson={(id) => {
            setRun(null);
            setSoloLessonId(id);
          }}
          onClose={() => setRun(null)}
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
          <p className="pt-28 text-center text-muted">Hệ thống đang được cấu hình.</p>
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
