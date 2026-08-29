"use client";

import { useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import Link from "next/link";
import { Check, ChevronDown, FileText, Play } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import PracticeQuestionsGrid from "@/components/lessons/PracticeQuestionsGrid";
import {
  SECTION_META,
  SECTION_ORDER,
  formatTypeCounts,
  youTubeEmbed,
  type Lesson,
  type LessonItem,
} from "@/features/lessons/types";
import {
  fetchExamMetas,
  fetchLessonItems,
  fetchMyExamScores,
  fetchMyProgress,
  markItemDone,
  type LessonExamMeta,
} from "@/services/lessons";
import { heartbeatLearningPresence } from "@/services/learning-presence";

const lessonItemsCache = new Map<number, LessonItem[]>();

export interface InlineLessonProgress {
  completed: number;
  total: number;
}

export default function InlineLessonAccordion({
  lesson,
  open,
  onToggle,
  onProgress,
  progress,
  onItemCompleted,
}: {
  lesson: Lesson;
  open: boolean;
  onToggle: () => void;
  onProgress?: (lessonId: number, progress: InlineLessonProgress) => void;
  progress?: InlineLessonProgress;
  onItemCompleted?: () => void;
}) {
  const { session } = useAuth();
  const articleRef = useRef<HTMLElement>(null);
  const presenceOpenedAt = useRef("");
  const [items, setItems] = useState<LessonItem[] | null>(() => lessonItemsCache.get(lesson.id) ?? null);
  const [examMetas, setExamMetas] = useState<Map<number, LessonExamMeta>>(new Map());
  const [scores, setScores] = useState<Map<number, number>>(new Map());
  const [done, setDone] = useState<Set<number>>(new Set());
  const [userProgressLoaded, setUserProgressLoaded] = useState(false);

  useEffect(() => {
    if (!open || items) return;
    fetchLessonItems(lesson.id).then((rows) => {
      lessonItemsCache.set(lesson.id, rows);
      setItems(rows);
    });
  }, [open, items, lesson.id]);

  useEffect(() => {
    if (!open) return;
    const timer = window.setTimeout(() => articleRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 120);
    return () => window.clearTimeout(timer);
  }, [open]);

  useEffect(() => {
    if (!open || !session) return;
    presenceOpenedAt.current = new Date().toISOString();
    const beat = () => {
      if (document.visibilityState !== "visible") return;
      void heartbeatLearningPresence({
        studentId: session.user.id,
        lessonId: lesson.id,
        openedAt: presenceOpenedAt.current,
      }).catch(() => undefined);
    };
    beat();
    const timer = window.setInterval(beat, 60_000);
    document.addEventListener("visibilitychange", beat);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", beat);
    };
  }, [open, session, lesson.id]);

  useEffect(() => {
    if (!open || !session || !items) return;
    const examIds = items
      .filter((item) => item.kind === "kiem_tra")
      .flatMap((item) => item.exam_ids);
    Promise.all([
      fetchExamMetas(examIds),
      fetchMyExamScores(session.user.id),
      fetchMyProgress(session.user.id),
    ]).then(([metas, nextScores, nextDone]) => {
      setExamMetas(metas);
      setScores(nextScores);
      setDone(nextDone);
      setUserProgressLoaded(true);
    });
  }, [open, session, items]);

  const sections = useMemo(
    () => SECTION_ORDER.map((kind) => ({ kind, items: (items ?? []).filter((item) => item.kind === kind) }))
      .filter((section) => section.items.length > 0),
    [items],
  );

  function isItemDone(item: LessonItem) {
    if (item.kind === "kiem_tra")
      return item.exam_ids.length > 0 && item.exam_ids.every((id) => scores.has(id));
    return done.has(item.id);
  }

  const completedCount = items?.filter(isItemDone).length ?? progress?.completed ?? 0;
  const totalCount = items?.length ?? progress?.total ?? lesson.itemCount;
  const percent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;
  const nextIncompleteItem = items?.find((item) => !isItemDone(item)) ?? null;

  useEffect(() => {
    if (!items || (session && !userProgressLoaded)) return;
    onProgress?.(lesson.id, { completed: completedCount, total: items.length });
  }, [completedCount, items, lesson.id, onProgress, session, userProgressLoaded]);

  function complete(item: LessonItem) {
    if (!session || done.has(item.id)) return;
    setDone((current) => new Set(current).add(item.id));
    onItemCompleted?.();
    void markItemDone(session.user.id, item.id);
  }

  return (
    <article ref={articleRef} style={{ scrollMarginTop: "104px" }} className={`overflow-hidden rounded-xl border transition-colors duration-200 ${open ? "border-blue-400/40 bg-[#0B1324]" : "border-white/10 bg-[#0B1020]"}`}>
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        aria-controls={`inline-lesson-${lesson.id}`}
        className="group flex w-full items-center gap-4 px-4 py-4 text-left hover:bg-white/5"
      >
        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#1D3461] text-lg">📖</span>
        <span className="min-w-0 flex-1">
          <span className="block font-display text-sm font-bold tracking-wide text-white uppercase group-hover:text-primary">{lesson.title}</span>
          <span className="mt-1 flex items-center gap-2 text-xs font-semibold text-slate-400">
            <span>{completedCount === 0 ? "Chưa học" : percent === 100 ? "Đã hoàn thành" : "Đang học"}</span>
            <span>·</span><span>{completedCount}/{totalCount} mục</span>
          </span>
          <span className="mt-2 block h-1.5 max-w-56 overflow-hidden rounded-full bg-white/10">
            <span className="block h-full rounded-full bg-blue-500 transition-[width]" style={{ width: `${percent}%` }} />
          </span>
        </span>
        <span className="inline-flex items-center gap-2 text-sm font-semibold text-slate-400">
          {open ? "Thu gọn" : "Mở bài"}
          <ChevronDown size={18} className={`transition-transform ${open ? "rotate-180" : ""}`} />
        </span>
      </button>

      {open && (
        <div id={`inline-lesson-${lesson.id}`} className="border-t border-white/10 p-4 sm:p-5">
          {!items ? (
            <p className="text-sm text-slate-400">Đang tải nội dung bài học…</p>
          ) : items.length === 0 ? (
            <p className="text-sm text-slate-400">Bài học đang được cập nhật.</p>
          ) : (
            <div className="space-y-6">
              {sections.map((section) => {
                const meta = SECTION_META[section.kind];
                return (
                  <section key={section.kind} style={{ "--lesson-color": meta.color } as CSSProperties}>
                    <h4 className="mb-3 flex items-center gap-2 text-sm font-bold uppercase tracking-wide" style={{ color: meta.color }}>
                      <span>{meta.icon}</span>{meta.label}
                    </h4>
                    <div className="space-y-3">
                      {section.items.map((item) => {
                        const embed = item.kind === "video" ? youTubeEmbed(item.video_url) : null;
                        const finished = isItemDone(item);
                        return (
                          <div key={item.id} id={`lesson-item-${item.id}`} style={{ scrollMarginTop: "112px" }} className="rounded-xl border border-white/10 bg-[#080D1A] p-4">
                            <div className="flex flex-wrap items-center gap-3">
                              <div className="min-w-0 flex-1">
                                <h5 className="font-semibold text-white">{item.title}</h5>
                                {item.subtitle && <p className="mt-1 text-sm text-slate-400">{item.subtitle}</p>}
                              </div>
                              {finished && <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-300"><Check size={14} /> Đã hoàn thành</span>}
                            </div>

                            {item.body_html && (
                              <div className="mt-3">
                                <ContentHtml html={item.body_html} className="block leading-relaxed text-slate-200" />
                                {session && !finished && (
                                  <button type="button" onClick={() => complete(item)} className="mt-3 rounded-lg border border-white/15 px-3 py-2 text-xs font-semibold text-slate-300 hover:border-emerald-400/40 hover:text-emerald-300">
                                    Đánh dấu đã đọc
                                  </button>
                                )}
                              </div>
                            )}
                            {embed && (
                              <div className="mt-4 aspect-video overflow-hidden rounded-xl">
                                <iframe src={embed} title={item.title} allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen className="h-full w-full" />
                              </div>
                            )}
                            {item.kind === "bai_tap_mau" && (
                              <div className="mt-3">
                                <WorkedQuestionsGrid questions={item.questions} color={meta.color} />
                              </div>
                            )}
                            {item.kind === "luyen_tap" && (
                              <div className="mt-3">
                                <PracticeQuestionsGrid examIds={item.exam_ids} color={meta.color} />
                              </div>
                            )}
                            {item.kind === "kiem_tra" && (
                              <div className="mt-3 space-y-2">
                                {item.exam_ids.length === 0 ? (
                                  <p className="text-sm text-slate-500">Chưa gắn đề</p>
                                ) : (
                                  item.exam_ids.map((examId) => {
                                    const exam = examMetas.get(examId);
                                    const score = scores.get(examId);
                                    return (
                                      <div key={examId} className="flex flex-wrap items-center gap-2">
                                        <Link href={session ? `/kiem-tra/lam?id=${examId}` : "/dang-nhap"} className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white">
                                          <Play size={15} /> {session ? (score === undefined ? "Làm bài" : `Làm lại · ${score} điểm`) : "Đăng nhập để làm"}
                                        </Link>
                                        {exam && <span className="self-center text-xs text-slate-400">{exam.title} · {exam.duration_minutes} phút · {formatTypeCounts(exam.type_counts) || `${exam.question_count} câu`}</span>}
                                      </div>
                                    );
                                  })
                                )}
                              </div>
                            )}
                            <div className="mt-3 flex flex-wrap gap-2">
                              {embed && session && !finished && (
                                <button type="button" onClick={() => complete(item)} className="rounded-lg border border-white/15 px-3 py-2 text-xs font-semibold text-slate-300 hover:border-emerald-400/40 hover:text-emerald-300">
                                  Đánh dấu đã xem
                                </button>
                              )}
                              {(item.kind === "bai_tap_mau" || item.kind === "luyen_tap") && session && !finished && (
                                <button type="button" onClick={() => complete(item)} className="rounded-lg border border-white/15 px-3 py-2 text-xs font-semibold text-slate-300 hover:border-emerald-400/40 hover:text-emerald-300">
                                  Đánh dấu đã làm
                                </button>
                              )}
                              {item.pdf_url && <a href={item.pdf_url} target="_blank" rel="noreferrer" onClick={() => complete(item)} className="inline-flex items-center gap-2 rounded-lg border border-white/15 px-3 py-2 text-sm font-semibold text-slate-200"><FileText size={15} /> Xem PDF</a>}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </section>
                );
              })}
              {percent === 100 ? (
                <div className="rounded-xl border border-emerald-400/20 bg-emerald-500/10 p-4 text-sm text-emerald-200">
                  <strong className="flex items-center gap-2"><Check size={17} /> Đã hoàn thành bài học</strong>
                  <p className="mt-1 text-emerald-200/70">Em có thể thu gọn bài và chuyển sang bài tiếp theo.</p>
                </div>
              ) : nextIncompleteItem ? (
                <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-blue-400/20 bg-blue-500/5 p-4">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-wide text-blue-300">Tiếp theo</p>
                    <p className="mt-1 text-sm font-semibold text-white">{nextIncompleteItem.title}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => document.getElementById(`lesson-item-${nextIncompleteItem.id}`)?.scrollIntoView({ behavior: "smooth", block: "start" })}
                    className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-bold text-white hover:bg-blue-500"
                  >
                    Học phần tiếp theo
                  </button>
                </div>
              ) : null}
            </div>
          )}
        </div>
      )}
    </article>
  );
}
