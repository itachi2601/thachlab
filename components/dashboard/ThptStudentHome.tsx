"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AlertTriangle, ChevronRight, LogOut, Target, Trophy } from "lucide-react";
import type { Profile } from "@/components/auth/AuthProvider";
import type { SchoolClass } from "@/features/exams/types";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { expandClassIdsByGrade, fetchClasses } from "@/services/classes";
import { visibleTo } from "@/services/content";
import {
  fetchChapters,
  fetchLessonProgressSummaries,
  fetchLessons,
  type LessonProgressSummary,
} from "@/services/lessons";
import {
  fetchClassAssessments,
  fetchMyAlert,
  fetchMyScoreHistory,
  fetchMyTopicGaps,
  fetchPeriodicRank,
  type ClassAssessment,
  type PeriodicRank,
  type ScorePoint,
  type StudentAlert,
  type TopicGap,
} from "@/services/analytics";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-xl border border-blue-500/15 bg-blue-500/5 p-3 sm:rounded-2xl sm:p-5">
      <strong className="text-xl text-white sm:text-3xl">{value}</strong>
      <p className="mt-1 truncate text-[9px] font-bold uppercase tracking-wide text-blue-300 sm:text-xs sm:tracking-wider">
        {label}
      </p>
    </div>
  );
}

export default function ThptStudentHome({
  profile,
  email,
  studentId,
  classId,
  className,
  onSignOut,
}: {
  profile: Profile | null;
  email?: string;
  studentId: string;
  classId: number;
  className: string;
  onSignOut: () => void;
}) {
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<Lesson[] | null>(null);
  const [progress, setProgress] = useState<Map<number, LessonProgressSummary>>(new Map());
  const [scores, setScores] = useState<ScorePoint[]>([]);
  const [rank, setRank] = useState<PeriodicRank | null>(null);
  const [assessments, setAssessments] = useState<ClassAssessment[]>([]);
  const [gaps, setGaps] = useState<TopicGap[]>([]);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [lastLessonId, setLastLessonId] = useState(0);

  useEffect(() => {
    Promise.all([fetchClasses(), fetchChapters(), fetchLessons()])
      .then(([cs, chs, ls]) => {
        setLastLessonId(Number(window.localStorage.getItem(LAST_LESSON_KEY)) || 0);
        setClasses(cs);
        setChapters(chs);
        setLessons(ls);
      })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    fetchMyScoreHistory(studentId).then(setScores).catch(() => setScores([]));
    fetchMyTopicGaps(studentId).then(setGaps).catch(() => setGaps([]));
    fetchMyAlert(studentId).then(setAlert).catch(() => setAlert(null));
    fetchPeriodicRank(classId).then(setRank).catch(() => setRank(null));
    fetchClassAssessments(classId).then(setAssessments).catch(() => setAssessments([]));
  }, [studentId, classId]);

  const classChapters = useMemo(() => {
    if (!classes || !chapters) return null;
    const visibleClassIds = expandClassIdsByGrade([classId], classes);
    return chapters.filter((chapter) => visibleTo(chapter.classIds, visibleClassIds));
  }, [classes, chapters, classId]);

  const classLessons = useMemo(() => {
    if (!classChapters || !lessons) return null;
    const order = new Map(classChapters.map((chapter, index) => [chapter.id, index]));
    return lessons
      .filter((lesson) => order.has(lesson.chapter_id))
      .sort(
        (a, b) =>
          (order.get(a.chapter_id) ?? 0) - (order.get(b.chapter_id) ?? 0) ||
          a.sort_order - b.sort_order,
      );
  }, [classChapters, lessons]);

  useEffect(() => {
    if (!classLessons) return;
    fetchLessonProgressSummaries(studentId, classLessons.map((lesson) => lesson.id))
      .then(setProgress)
      .catch(() => setProgress(new Map()));
  }, [classLessons, studentId]);

  const totals = useMemo(() => {
    if (!classLessons) return null;
    let completed = 0;
    let total = 0;
    for (const lesson of classLessons) {
      const summary = progress.get(lesson.id);
      completed += summary?.completed ?? 0;
      total += summary?.total ?? lesson.itemCount;
    }
    return { completed, total, pct: total > 0 ? Math.round((completed / total) * 100) : 0 };
  }, [classLessons, progress]);

  const nextLesson = useMemo(() => {
    if (!classLessons?.length) return null;
    const unfinished = (lesson: Lesson) => {
      const summary = progress.get(lesson.id);
      const total = summary?.total ?? lesson.itemCount;
      return total === 0 || (summary?.completed ?? 0) < total;
    };
    return (
      classLessons.find((lesson) => lesson.id === lastLessonId && unfinished(lesson)) ??
      classLessons.find(unfinished) ??
      null
    );
  }, [classLessons, progress, lastLessonId]);

  const nextChapter = classChapters?.find((chapter) => chapter.id === nextLesson?.chapter_id) ?? null;
  const avgScore = scores.length
    ? Math.round((scores.reduce((sum, point) => sum + point.score, 0) / scores.length) * 10) / 10
    : null;
  const doneExamIds = useMemo(() => new Set(scores.map((point) => point.examId)), [scores]);
  const todoExams = assessments.filter((item) => !doneExamIds.has(item.examId)).slice(0, 3);
  const topGaps = gaps.filter((gap) => gap.wrong > 0).slice(0, 3);

  return (
    <div className="space-y-4 sm:space-y-5">
      <section className="relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-[#172c46] via-[#0e1c32] to-[#071426] p-4 sm:rounded-3xl sm:p-8">
        <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="relative flex items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="text-[10px] font-bold uppercase tracking-[.14em] text-blue-300 sm:text-xs sm:tracking-[.16em]">
              Không gian học tập của tôi
            </p>
            <h1 className="mt-1.5 truncate font-display text-2xl font-bold text-white sm:mt-2 sm:text-3xl">
              Chào {profile?.full_name || "bạn"} 👋
            </h1>
            <p className="mt-1.5 text-xs text-slate-400 sm:mt-2 sm:text-sm">Lớp {className}</p>
            {email && <p className="mt-1 hidden text-xs text-slate-600 sm:block">{email}</p>}
          </div>
          <button
            onClick={onSignOut}
            aria-label="Đăng xuất"
            className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-white/10 text-slate-300 sm:h-auto sm:w-auto sm:gap-2 sm:px-4 sm:py-2 sm:text-sm sm:font-bold"
          >
            <LogOut size={16} />
            <span className="hidden sm:inline">Đăng xuất</span>
          </button>
        </div>
        <div className="relative mt-5 sm:mt-6">
          <div className="mb-2 flex items-end justify-between gap-3 text-xs">
            <b className="text-blue-200">Năng lượng học tập</b>
            <span className="whitespace-nowrap font-mono text-[11px] text-slate-400 sm:text-xs">
              {totals ? `${totals.completed}/${totals.total} mục · ${totals.pct}%` : "…"}
            </span>
          </div>
          <div className="h-3.5 overflow-hidden rounded-full border border-white/10 bg-[#050914] sm:h-4">
            <div
              className="h-full rounded-full bg-gradient-to-r from-blue-600 via-cyan-400 to-sky-300 shadow-[0_0_18px_rgba(56,189,248,.45)] transition-[width]"
              style={{ width: `${totals?.pct ?? 0}%` }}
            />
          </div>
        </div>
      </section>

      {alert && (
        <section className="rounded-2xl border border-amber-400/25 bg-gradient-to-r from-amber-500/10 to-transparent p-4 sm:p-5">
          <div className="flex items-center gap-2 text-amber-300">
            <AlertTriangle size={18} />
            <h2 className="font-display font-bold text-white">Cần chú ý</h2>
          </div>
          <p className="mt-2 text-sm text-amber-100/80">
            {alert.kind === "missed_assessment"
              ? "Em còn bài kiểm tra chưa làm — hãy hoàn thành sớm."
              : "Điểm kiểm tra của em đang thấp. Trợ giảng sẽ liên hệ để sắp lịch phụ đạo."}
          </p>
        </section>
      )}

      <section className="grid grid-cols-3 gap-2 sm:gap-3">
        <Stat value={totals ? `${totals.pct}%` : "—"} label="Tiến độ" />
        <Stat value={avgScore !== null ? avgScore.toLocaleString("vi-VN") : "—"} label="Điểm TB" />
        <Stat value={rank ? `${rank.rank}/${rank.total}` : "—"} label="Hạng lớp" />
      </section>

      {nextLesson && (
        <Link
          href={`/lop-hoc/bai?id=${nextLesson.id}&chapter=${nextLesson.chapter_id}`}
          className="flex items-center justify-between gap-3 rounded-2xl border border-blue-400/20 bg-gradient-to-r from-blue-500/10 to-transparent p-4 sm:p-5"
        >
          <div className="min-w-0">
            <small className="text-[10px] font-bold uppercase tracking-wider text-blue-300 sm:text-xs">
              Học tiếp theo
            </small>
            <h2 className="mt-1 truncate font-display text-lg font-bold text-white sm:text-xl">
              {nextLesson.title}
            </h2>
            {nextChapter && <p className="mt-1 truncate text-xs text-slate-400 sm:text-sm">{nextChapter.title}</p>}
          </div>
          <ChevronRight className="shrink-0 text-blue-300" />
        </Link>
      )}

      {todoExams.length > 0 && (
        <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-4 sm:p-5">
          <div className="flex items-center gap-2">
            <Trophy size={18} className="text-amber-300" />
            <h2 className="font-display font-bold text-white">Bài kiểm tra cần làm</h2>
          </div>
          <div className="mt-3 space-y-2">
            {todoExams.map((item) => (
              <Link
                key={item.id}
                href={`/kiem-tra/lam?id=${item.examId}`}
                className="flex items-center justify-between gap-3 rounded-xl bg-white/[.02] p-3 hover:bg-white/5"
              >
                <span className="min-w-0">
                  <strong className="block truncate text-sm text-white">{item.examTitle}</strong>
                  <small className="text-xs text-slate-500">Chưa làm</small>
                </span>
                <ChevronRight size={16} className="shrink-0 text-slate-500" />
              </Link>
            ))}
          </div>
        </section>
      )}

      {topGaps.length > 0 && (
        <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-4 sm:p-5">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Target size={18} className="text-blue-300" />
              <h2 className="font-display font-bold text-white">Chủ đề cần ôn</h2>
            </div>
            <Link href="/lop-hoc/ket-qua" className="text-xs font-semibold text-[#60A5FA] hover:underline">
              Xem tất cả →
            </Link>
          </div>
          <div className="mt-3 space-y-2">
            {topGaps.map((gap) => (
              <div key={gap.key} className="flex items-center justify-between gap-3 rounded-xl bg-white/[.02] p-3">
                <span className="min-w-0 truncate text-sm text-slate-200">{gap.topic}</span>
                <span
                  className={`shrink-0 font-mono text-sm font-bold ${
                    gap.pct >= 60 ? "text-red-300" : gap.pct >= 30 ? "text-amber-300" : "text-slate-400"
                  }`}
                >
                  sai {gap.pct}%
                </span>
              </div>
            ))}
          </div>
        </section>
      )}

      <Link
        href="/lop-hoc"
        className="flex items-center justify-between gap-3 rounded-2xl border border-white/10 bg-[#0B1020] p-4 text-sm font-semibold text-slate-200 hover:bg-white/5 sm:p-5"
      >
        Xem toàn bộ chương trình lớp {className}
        <ChevronRight size={16} className="shrink-0 text-slate-500" />
      </Link>
    </div>
  );
}
