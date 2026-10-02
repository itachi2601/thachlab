"use client";

import { useEffect, useMemo, useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type { Difficulty, SchoolClass } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import type { Chapter } from "@/features/lessons/types";
import { isPeriodicExam } from "@/features/lessons/types";
import { displayClassesByGrade, expandClassIdsByGrade } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { fetchExamsFull, type LessonWithItemRefs } from "@/services/lessons";
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

interface PoolStats {
  topics: { name: string; total: number }[];
  /** Đếm câu theo mức, áp dụng bộ lọc YCCĐ đang chọn. */
  byLevel: Record<"de" | "trung-binh" | "kho", number>;
  total: number;
}

const selectCls =
  "w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-white/30 focus:outline-none";

function Content() {
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

  return (
    <div className="mx-auto w-full max-w-2xl px-4 pb-20 pt-28 sm:px-6">
      <Link href="/tai-khoan/" className="mb-5 inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-white">
        <ChevronLeft size={16} /> Về trang của em
      </Link>
      <h1 className="font-display text-2xl font-semibold text-white">Luyện tập theo yêu cầu cần đạt</h1>
      <p className="mt-1 text-sm text-slate-400">
        Chọn bài, yêu cầu cần đạt và mức độ để luyện đúng chỗ còn thiếu danh hiệu. Câu đã giải đúng rồi không
        được tính lại cho danh hiệu — làm câu mới mới tiến thêm.
      </p>

      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        <label className="text-xs text-slate-400">
          Lớp
          <select
            className={selectCls}
            value={activeClassId ?? ""}
            onChange={(e) => {
              setClassId(Number(e.target.value));
              setChapterId(null);
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
        <label className="text-xs text-slate-400">
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
        <label className="text-xs text-slate-400 sm:col-span-2">
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

      {lesson && (
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

      {practicing && lesson && (
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
      <Footer />
    </>
  );
}
