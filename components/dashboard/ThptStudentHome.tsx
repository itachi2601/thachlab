"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import Link from "next/link";
import { AlertTriangle, BookOpen, CalendarClock, ChevronRight, LogOut, Megaphone, RotateCcw, Sparkles, Trophy, Users } from "lucide-react";
import type { Profile } from "@/components/auth/AuthProvider";
import AvatarUploader from "@/components/account/AvatarUploader";
import type { SchoolClass } from "@/features/exams/types";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { expandClassIdsByGrade } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { useToast } from "@/components/ui/Toast";
import CatchupCard from "@/components/results/CatchupCard";
import {
  fetchMyProgressMarks,
  summarizeLessonProgress,
  type LessonProgressSummary,
  type LessonWithItemRefs,
  type MyProgressMarks,
} from "@/services/lessons";
import { fetchChaptersStatic, fetchClassesStatic, fetchLessonsStatic } from "@/services/static-content";
import {
  fetchClassAssessments,
  fetchMyAlert,
  fetchMyScoreHistory,
  type ClassAssessment,
  type ScorePoint,
  type StudentAlert,
} from "@/services/analytics";
import RankAvatarFrame from "@/components/rank/RankAvatarFrame";
import RankCard from "@/components/rank/RankCard";
import WornTitle from "@/components/rank/WornTitle";
import TitleShowcase from "@/components/rank/TitleShowcase";
import DailyStreakCard from "@/components/rank/DailyStreakCard";
import ClassRankBoard from "@/components/rank/ClassRankBoard";
import HonorVisibilityPicker from "@/components/rank/HonorVisibilityPicker";
import type { RankStatus, RankTitle } from "@/features/rank/types";
import { fetchMyRankStatus, fetchMyTitles } from "@/services/rank";
import {
  fetchLatestAnnouncements,
  fetchRecentAnnouncements,
  type AnnouncementKind,
  type ClassAnnouncement,
} from "@/services/announcements";
import {
  ACTIVE_NEED_STATUSES,
  formatExitWait,
  nextExitAttemptAt,
  NEED_STATUS_LABEL_STUDENT,
  EXIT_COOLDOWN_HOURS,
  cancelRegistration,
  fetchMyExitAttempts,
  fetchMyOpenExitWindows,
  WINDOW_QUIZ_PASS_PCT,
  WINDOW_QUIZ_QUESTION_COUNT,
  fetchMyNeeds,
  fetchMyRegistrations,
  fetchUpcomingSlots,
  needLabel,
  registerForSlot,
  type ExitWindow,
  type NeedStatus,
  type TutoringNeed,
  type TutoringSlot,
} from "@/services/tutoring";
import TutoringExitQuiz from "@/components/results/TutoringExitQuiz";
import { fetchOpenClassReviewHomework, type ClassReviewHomework } from "@/services/homework";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

const NEED_TONE: Record<NeedStatus, string> = {
  open: "border-sky-500/40 bg-sky-500/10 text-sky-200",
  assigned: "border-indigo-500/40 bg-indigo-500/10 text-indigo-200",
  tutored: "border-blue-500/40 bg-blue-500/10 text-blue-200",
  cleared: "border-emerald-500/40 bg-emerald-500/10 text-emerald-200",
  dismissed: "border-white/15 bg-white/5 text-slate-400",
};

function Section({
  icon: Icon,
  title,
  action,
  children,
}: {
  icon: typeof Megaphone;
  title: string;
  action?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Icon size={18} className="text-blue-300" />
          <h2 className="font-display font-bold text-white">{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

function AnnouncementNote({ item }: { item: ClassAnnouncement }) {
  return (
    <div className="rounded-xl border border-blue-400/20 bg-blue-500/5 p-3">
      <p className="whitespace-pre-wrap text-sm text-blue-100">{item.body}</p>
      <p className="mt-1.5 text-[13px] text-slate-400">
        {item.createdByName || "Giáo viên"} ·{" "}
        {new Date(item.createdAt).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })}
      </p>
      {item.examId && (
        <Link
          href={`/kiem-tra/lam?id=${item.examId}`}
          className="mt-2.5 flex items-center justify-between gap-2 rounded-lg bg-blue-500/15 px-3 py-2 text-sm font-bold text-blue-100 hover:bg-blue-500/25"
        >
          <span className="flex min-w-0 items-center gap-2">
            <Trophy size={14} className="shrink-0 text-amber-300" />
            <span className="truncate">{item.examTitle ?? "Làm bài"}</span>
          </span>
          <ChevronRight size={16} className="shrink-0" />
        </Link>
      )}
    </div>
  );
}

export default function ThptStudentHome({
  profile,
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
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<LessonWithItemRefs[] | null>(null);
  const [progressMarks, setProgressMarks] = useState<MyProgressMarks | null>(null);
  const [scores, setScores] = useState<ScorePoint[]>([]);
  const [rank, setRank] = useState<RankStatus | null | undefined>(undefined);
  const [titles, setTitles] = useState<RankTitle[] | null | undefined>(undefined);
  const [assessments, setAssessments] = useState<ClassAssessment[]>([]);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [scoresLoaded, setScoresLoaded] = useState(false);
  const [assessmentsLoaded, setAssessmentsLoaded] = useState(false);
  const [lastLessonId, setLastLessonId] = useState(0);

  const [todayNote, setTodayNote] = useState<ClassAnnouncement | null>(null);
  const [homeworkNotes, setHomeworkNotes] = useState<ClassAnnouncement[]>([]);
  const [reviewHomework, setReviewHomework] = useState<ClassReviewHomework[]>([]);
  const [needs, setNeeds] = useState<TutoringNeed[]>([]);
  const [slots, setSlots] = useState<TutoringSlot[]>([]);
  const [myRegistrations, setMyRegistrations] = useState<Set<number>>(new Set());
  const [busySlotId, setBusySlotId] = useState<number | null>(null);
  const [lastExitAttempt, setLastExitAttempt] = useState<Map<number, string>>(new Map());
  const [quizNeed, setQuizNeed] = useState<TutoringNeed | null>(null);
  // Bài kiểm tra cuối buổi do trợ giảng mở: cửa sổ còn mở + các lượt em đã làm trong từng cửa sổ.
  const [openWindows, setOpenWindows] = useState<ExitWindow[]>([]);
  const [windowDone, setWindowDone] = useState<Set<string>>(new Set());
  const [quizWindow, setQuizWindow] = useState<ExitWindow | null>(null);
  const [nowMs, setNowMs] = useState(() => Date.now());
  useEffect(() => {
    if (openWindows.length === 0) return;
    const t = window.setInterval(() => setNowMs(Date.now()), 15_000);
    return () => window.clearInterval(t);
  }, [openWindows.length]);

  useEffect(() => {
    // Ưu tiên file tĩnh /data/catalog.json; Supabase đối chiếu ngầm, có khác thì setter được gọi lại.
    Promise.all([fetchClassesStatic(setClasses), fetchChaptersStatic(setChapters), fetchLessonsStatic(setLessons)])
      .then(([cs, chs, ls]) => {
        setLastLessonId(Number(window.localStorage.getItem(LAST_LESSON_KEY)) || 0);
        setClasses(cs);
        setChapters(chs);
        setLessons(ls);
      })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    fetchMyScoreHistory(studentId)
      .then(setScores)
      .catch(() => setScores([]))
      .finally(() => setScoresLoaded(true));
    // dấu "đã học" không phụ thuộc lớp/chương/bài → tải ngay, tiến độ tính ở client khi đủ dữ liệu
    fetchMyProgressMarks(studentId).then(setProgressMarks).catch(() => setProgressMarks(null));
    fetchMyAlert(studentId).then(setAlert).catch(() => setAlert(null));
    fetchMyRankStatus().then(setRank).catch(() => setRank(null));
    fetchMyTitles().then(setTitles).catch(() => setTitles(null));
    fetchClassAssessments(classId)
      .then(setAssessments)
      .catch(() => setAssessments([]))
      .finally(() => setAssessmentsLoaded(true));
  }, [studentId, classId]);

  function reloadAnnouncements() {
    fetchLatestAnnouncements(classId)
      .then((byKind) => setTodayNote(byKind.today_task))
      .catch(() => setTodayNote(null));
    fetchRecentAnnouncements(classId, "homework" as AnnouncementKind, 5)
      .then(setHomeworkNotes)
      .catch(() => setHomeworkNotes([]));
    fetchOpenClassReviewHomework(classId).then(setReviewHomework).catch(() => setReviewHomework([]));
  }
  useEffect(reloadAnnouncements, [classId]);

  function reloadTutoring() {
    fetchMyNeeds(studentId)
      .then((rows) => {
        const active = rows.filter((n) => ACTIVE_NEED_STATUSES.includes(n.status));
        setNeeds(active);
        fetchMyExitAttempts(studentId, active.map((n) => n.id))
          .then((attempts) => {
            const last = new Map<number, string>();
            for (const a of attempts) {
              const prev = last.get(a.tutoringNeedId);
              if (!prev || a.createdAt > prev) last.set(a.tutoringNeedId, a.createdAt);
            }
            setLastExitAttempt(last);
            setWindowDone(
              new Set(attempts.filter((a) => a.windowId).map((a) => `${a.windowId}|${a.tutoringNeedId}`)),
            );
          })
          .catch(() => setLastExitAttempt(new Map()));
      })
      .catch(() => setNeeds([]));
    fetchMyOpenExitWindows().then(setOpenWindows).catch(() => setOpenWindows([]));
    fetchUpcomingSlots(classId).then(setSlots).catch(() => setSlots([]));
    fetchMyRegistrations(studentId).then((ids) => setMyRegistrations(new Set(ids))).catch(() => setMyRegistrations(new Set()));
  }
  useEffect(reloadTutoring, [studentId, classId]);

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

  const progress = useMemo(
    (): Map<number, LessonProgressSummary> =>
      classLessons && progressMarks ? summarizeLessonProgress(classLessons, progressMarks) : new Map(),
    [classLessons, progressMarks],
  );

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

  // L2: tiến độ của bài đang dở (không phải cả lớp); chưa có thì quay về tổng.
  const lessonProgress = useMemo(() => {
    if (!nextLesson) return null;
    const summary = progress.get(nextLesson.id);
    const total = summary?.total ?? nextLesson.itemCount;
    if (!total) return null;
    const completed = summary?.completed ?? 0;
    return { completed, total, pct: Math.round((completed / total) * 100) };
  }, [nextLesson, progress]);
  const shownProgress = lessonProgress ?? totals;

  const nextChapter = classChapters?.find((chapter) => chapter.id === nextLesson?.chapter_id) ?? null;
  const avgScore = scores.length
    ? Math.round((scores.reduce((sum, point) => sum + point.score, 0) / scores.length) * 10) / 10
    : null;
  const doneExamIds = useMemo(() => new Set(scores.map((point) => point.examId)), [scores]);
  const todoExams = assessments.filter((item) => !doneExamIds.has(item.examId)).slice(0, 5);
  const todoReviewHomework = reviewHomework.filter((item) => !doneExamIds.has(item.examId)).slice(0, 3);
  // Bài đã làm nhưng chưa đạt — gợi ý làm lại khi không còn bài nào tồn đọng.
  const retryExam = useMemo(() => {
    const worst = new Map<number, ScorePoint>();
    for (const point of scores) {
      const cur = worst.get(point.examId);
      if (!cur || point.score > cur.score) worst.set(point.examId, point); // điểm tốt nhất của đề
    }
    return [...worst.values()].filter((p) => p.score < 6.5).sort((a, b) => a.score - b.score)[0] ?? null;
  }, [scores]);

  const pendingCount = todoExams.length + todoReviewHomework.length;
  const attentionReady = scoresLoaded && assessmentsLoaded;
  const showSuggestions = attentionReady && pendingCount === 0;

  const todoItems = [
    ...todoExams.map((item) => ({ key: `a-${item.id}`, href: `/kiem-tra/lam?id=${item.examId}`, title: item.examTitle, kind: "Bài kiểm tra" })),
    ...todoReviewHomework.map((item) => ({ key: `r-${item.id}`, href: `/kiem-tra/lam?id=${item.examId}`, title: item.title, kind: "BTVN ôn tập" })),
  ];
  const primaryTodo = attentionReady ? todoItems[0] ?? null : null;
  const otherTodos = primaryTodo ? todoItems.slice(1) : [];
  const hasAlert = attentionReady && Boolean(alert && alert.kind !== "missed_assessment");
  const hasTodayContent =
    Boolean(todayNote) || Boolean(primaryTodo) || hasAlert || (Boolean(nextLesson) && !showSuggestions);

  const nearTier = rank?.next && rank.next.rp_needed > 0 && rank.next.rp_needed <= 50
    ? `Còn ${rank.next.rp_needed} RP là lên ${rank.next.name}`
    : null;
  const dailySuggestion = todoExams.length > 0
    ? `Gợi ý: làm bài kiểm tra "${todoExams[0].examTitle}".${nearTier ? ` ${nearTier}!` : ""}`
    : nextLesson
      ? `Gợi ý: học tiếp "${nextLesson.title}" rồi làm phần luyện tập.${nearTier ? ` ${nearTier}!` : ""}`
      : needs.length > 0
        ? `Gợi ý: luyện thêm chủ đề "${needs[0].topicName}" đang cần phụ đạo.`
        : null;

  async function toggleRegistration(slot: TutoringSlot) {
    setBusySlotId(slot.id);
    try {
      if (myRegistrations.has(slot.id)) {
        await cancelRegistration(slot.id, studentId);
        toast("info", "Đã huỷ đăng ký.");
      } else {
        await registerForSlot(slot.id, studentId);
        toast("success", "Đã đăng ký buổi phụ đạo.");
      }
      reloadTutoring();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa thực hiện được, thử lại nhé.");
    } finally {
      setBusySlotId(null);
    }
  }

  return (
    <div className="space-y-4 sm:space-y-5">
      <section className="relative overflow-hidden rounded-2xl border border-white/10 bg-panel p-4 sm:rounded-3xl sm:p-7">
        <div className="relative flex items-start justify-between gap-3">
          <div className="flex min-w-0 items-center gap-3 sm:gap-4">
            <RankAvatarFrame status={rank} size={56}>
              <AvatarUploader studentId={studentId} url={profile?.avatar_url} name={profile?.full_name} size={56} />
            </RankAvatarFrame>
            <div className="min-w-0">
              <h1 className="font-display text-xl font-bold leading-tight text-white sm:text-3xl">
                Chào {profile?.full_name || "bạn"} 👋
              </h1>
              {rank?.display_title && <WornTitle title={rank.display_title} size="md" className="mt-1 max-w-full" />}
              <p className="mt-1 text-xs text-slate-400 sm:text-sm">Lớp {className}</p>
            </div>
          </div>
          <button
            onClick={onSignOut}
            aria-label="Đăng xuất"
            className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/10 text-slate-300 sm:h-auto sm:w-auto sm:gap-2 sm:px-4 sm:py-2 sm:text-sm sm:font-bold"
          >
            <LogOut size={16} />
            <span className="hidden sm:inline">Đăng xuất</span>
          </button>
        </div>
        <div className="relative mt-4 flex items-end gap-3 sm:mt-5 sm:gap-5">
          <div className="min-w-0 flex-1">
            <div className="mb-1.5 flex items-end justify-between gap-3 text-xs">
              <b className="text-blue-200">{lessonProgress ? "Bài đang học" : "Năng lượng học tập"}</b>
              <span className="whitespace-nowrap font-mono text-[13px] text-slate-400">
                {shownProgress ? `${shownProgress.completed}/${shownProgress.total} mục · ${shownProgress.pct}%` : "…"}
              </span>
            </div>
            <div className="h-3 overflow-hidden rounded-full border border-white/10 bg-[#050914] sm:h-3.5">
              <div
                className="h-full rounded-full bg-primary transition-[width]"
                style={{ width: `${shownProgress?.pct ?? 0}%` }}
              />
            </div>
          </div>
          <div className="shrink-0 rounded-xl border border-white/10 bg-white/[0.04] px-3 py-1.5 text-right">
            <strong className="block font-display text-lg leading-none text-white sm:text-xl">
              {avgScore !== null ? avgScore.toLocaleString("vi-VN") : "—"}
            </strong>
            <span className="text-[13px] font-bold uppercase tracking-wide text-blue-300">Điểm TB</span>
          </div>
        </div>
      </section>

      {showSuggestions && (
        <section className="rounded-2xl border border-emerald-400/25 bg-gradient-to-r from-emerald-500/10 to-transparent p-4 sm:p-5">
          <div className="flex items-center gap-2 text-emerald-300">
            <Sparkles size={18} />
            <h2 className="font-display font-bold text-white">Em đã làm xong bài được giao — việc nên làm tiếp</h2>
          </div>
          <div className="mt-3 space-y-2">
            {needs[0] && (
              <button
                type="button"
                onClick={() => setQuizNeed(needs[0])}
                disabled={nextExitAttemptAt(lastExitAttempt.get(needs[0].id)) !== null}
                className="flex min-h-11 w-full items-center justify-between gap-3 rounded-xl border border-emerald-400/20 bg-black/15 p-3 text-left hover:bg-black/25 disabled:opacity-50"
              >
                <span className="flex min-w-0 items-center gap-2">
                  <Users size={16} className="shrink-0 text-sky-300" />
                  <span className="min-w-0">
                    <strong className="block truncate text-sm text-white">Mở khoá chủ đề: {needLabel(needs[0])}</strong>
                    <small className="text-[13px] text-slate-400">Tự kiểm tra, đạt từ 80% là mở khoá</small>
                  </span>
                </span>
                <ChevronRight size={16} className="shrink-0 text-emerald-300" />
              </button>
            )}
            {retryExam && (
              <Link
                href={`/kiem-tra/lam?id=${retryExam.examId}`}
                className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-emerald-400/20 bg-black/15 p-3 hover:bg-black/25"
              >
                <span className="flex min-w-0 items-center gap-2">
                  <RotateCcw size={16} className="shrink-0 text-rose-300" />
                  <span className="min-w-0">
                    <strong className="block truncate text-sm text-white">Làm lại: {retryExam.examTitle}</strong>
                    <small className="text-[13px] text-slate-400">
                      Lần trước {retryExam.score.toLocaleString("vi-VN")} điểm — làm lại để chốt kiến thức
                    </small>
                  </span>
                </span>
                <ChevronRight size={16} className="shrink-0 text-emerald-300" />
              </Link>
            )}
            {nextLesson && (
              <Link
                href={`/lop-hoc/bai?id=${nextLesson.id}&chapter=${nextLesson.chapter_id}`}
                className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-emerald-400/20 bg-black/15 p-3 hover:bg-black/25"
              >
                <span className="flex min-w-0 items-center gap-2">
                  <BookOpen size={16} className="shrink-0 text-blue-300" />
                  <span className="min-w-0">
                    <strong className="block truncate text-sm text-white">Học tiếp: {nextLesson.title}</strong>
                    {nextChapter && <small className="block truncate text-[13px] text-slate-400">{nextChapter.title}</small>}
                  </span>
                </span>
                <ChevronRight size={16} className="shrink-0 text-emerald-300" />
              </Link>
            )}
            {!needs[0] && !retryExam && !nextLesson && (
              <Link
                href="/lop-hoc"
                className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-emerald-400/20 bg-black/15 p-3 hover:bg-black/25"
              >
                <span className="min-w-0">
                  <strong className="block truncate text-sm text-white">Ôn lại các bài đã học</strong>
                  <small className="text-[13px] text-slate-400">Chọn một bài bất kỳ để luyện thêm</small>
                </span>
                <ChevronRight size={16} className="shrink-0 text-emerald-300" />
              </Link>
            )}
          </div>
        </section>
      )}

      {/* Mục 1 — MỘT thẻ việc cần làm hôm nay: đúng một nút nổi ("Làm bài" hoặc "Học tiếp"), cảnh báo chỉ là một dòng nhỏ (N3, B2) */}
      {hasTodayContent && <Section icon={Megaphone} title="Việc cần làm hôm nay">
        <div className="mt-3 space-y-2.5">
          {todayNote && <AnnouncementNote item={todayNote} />}

          {primaryTodo ? (
            <Link
              href={primaryTodo.href}
              className="flex min-h-12 items-center justify-between gap-3 rounded-xl bg-primary p-3 text-white hover:bg-primary-dark"
            >
              <div className="min-w-0">
                <small className="text-[13px] font-bold uppercase tracking-wider text-blue-100">Làm bài</small>
                <p className="mt-0.5 truncate text-sm font-bold">{primaryTodo.title}</p>
                <p className="text-[13px] text-blue-100">{primaryTodo.kind} · chưa làm</p>
              </div>
              <ChevronRight className="shrink-0" size={18} />
            </Link>
          ) : nextLesson && !showSuggestions ? (
            <Link
              href={`/lop-hoc/bai?id=${nextLesson.id}&chapter=${nextLesson.chapter_id}`}
              className="flex min-h-12 items-center justify-between gap-3 rounded-xl bg-primary p-3 text-white hover:bg-primary-dark"
            >
              <div className="min-w-0">
                <small className="text-[13px] font-bold uppercase tracking-wider text-blue-100">Học tiếp</small>
                <p className="mt-0.5 truncate text-sm font-bold">{nextLesson.title}</p>
                {nextChapter && <p className="truncate text-[13px] text-blue-100">{nextChapter.title}</p>}
              </div>
              <ChevronRight className="shrink-0" size={18} />
            </Link>
          ) : null}

          {otherTodos.length > 0 && (
            <ul className="space-y-0.5">
              {otherTodos.map((item) => (
                <li key={item.key}>
                  <Link href={item.href} className="flex min-h-11 items-center justify-between gap-2 text-sm text-slate-300 hover:text-white">
                    <span className="min-w-0 truncate">{item.title} <span className="text-[13px] text-slate-400">· {item.kind}</span></span>
                    <ChevronRight size={16} className="shrink-0 text-slate-500" />
                  </Link>
                </li>
              ))}
            </ul>
          )}

          {attentionReady && alert && alert.kind !== "missed_assessment" && (
            <p className="flex items-start gap-1.5 text-[13px] text-amber-200/80">
              <AlertTriangle size={14} className="mt-0.5 shrink-0 text-amber-300" />
              {alert.kind === "exam_violation"
                ? "Bài kiểm tra gần đây bị ghi nhận rời màn hình nhiều lần — trợ giảng sẽ kiểm tra lại kiến thức của em."
                : "Điểm kiểm tra đang thấp — trợ giảng sẽ liên hệ sắp lịch phụ đạo."}
            </p>
          )}
        </div>
      </Section>}

      {/* Mục 2 — Bài tập về nhà */}
      {homeworkNotes.length > 0 && (
        <Section icon={CalendarClock} title="Bài tập về nhà">
          <div className="mt-3 space-y-2">
            {homeworkNotes.map((item) => <AnnouncementNote key={item.id} item={item} />)}
          </div>
        </Section>
      )}

      {/* Mục 3 — Chủ đề cần phụ đạo */}
      <CatchupCard studentId={studentId} classId={classId} viewer="student" />

      {openWindows
        .filter((w) => new Date(w.closesAt).getTime() > nowMs)
        .map((w) => {
          const mine = needs.filter((n) => w.topicIds.includes(n.topicId));
          if (mine.length === 0) return null;
          const minutesLeft = Math.max(1, Math.ceil((new Date(w.closesAt).getTime() - nowMs) / 60000));
          return (
            <div key={w.id} className="rounded-2xl border border-sky-400/40 bg-sky-500/10 p-4 sm:p-5">
              <h2 className="font-display font-bold text-white">Bài kiểm tra cuối buổi phụ đạo đã mở</h2>
              <p className="mt-1 text-sm text-sky-100">
                Em tự làm một mình, {WINDOW_QUIZ_QUESTION_COUNT} câu, đạt từ {WINDOW_QUIZ_PASS_PCT}%. Còn khoảng{" "}
                {minutesLeft} phút.
              </p>
              <div className="mt-3 space-y-2">
                {mine.map((need) => {
                  const done = windowDone.has(`${w.id}|${need.id}`);
                  return (
                    <button
                      key={need.id}
                      type="button"
                      disabled={done}
                      onClick={() => {
                        setQuizNeed(need);
                        setQuizWindow(w);
                      }}
                      className="flex min-h-11 w-full items-center justify-between gap-3 rounded-xl border border-sky-400/30 bg-black/20 p-3 text-left text-sm font-semibold text-white hover:bg-black/30 disabled:opacity-50"
                    >
                      <span className="min-w-0 truncate">{needLabel(need)}</span>
                      <span className="shrink-0 text-[13px] text-sky-200">{done ? "Đã làm" : "Bắt đầu"}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}

      {(needs.length > 0 || slots.length > 0) && <Section icon={Users} title="Chủ đề đang mở khoá">
        <div className="mt-3 space-y-4">
          {needs.length > 0 && (
            <>
              <p className="text-sm text-slate-400">
                Mở khoá bằng cách <strong className="text-slate-200">đăng ký phụ đạo</strong> bên dưới, hoặc{" "}
                <strong className="text-slate-200">tự kiểm tra</strong> (đạt từ 80%). Hai lượt cách nhau {EXIT_COOLDOWN_HOURS} giờ.
              </p>
              <div className="space-y-1.5">
                {needs.map((need) => {
                  const wait = nextExitAttemptAt(lastExitAttempt.get(need.id));
                  return (
                    <div key={need.id} className="flex flex-wrap items-center gap-1.5">
                      <span className={`rounded-full border px-3 py-1 text-[13px] font-semibold ${NEED_TONE[need.status]}`}>
                        {needLabel(need)} · {NEED_STATUS_LABEL_STUDENT[need.status]}
                      </span>
                      <button
                        type="button"
                        onClick={() => setQuizNeed(need)}
                        disabled={wait !== null}
                        className="min-h-11 rounded-full border border-white/15 px-4 py-2 text-[13px] font-semibold text-slate-300 hover:border-white/30 disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        {wait ? `Lượt tiếp theo mở lúc ${formatExitWait(wait)}` : "Tự kiểm tra"}
                      </button>
                    </div>
                  );
                })}
              </div>
            </>
          )}

          {slots.length > 0 && <div>
            <p className="mb-2 text-[13px] font-bold uppercase tracking-wide text-slate-400">Buổi phụ đạo sắp tới</p>
            {(
              <div className="space-y-2">
                {slots.map((slot) => {
                  const registered = myRegistrations.has(slot.id);
                  const full = slot.registeredCount >= slot.capacity && !registered;
                  return (
                    <div key={slot.id} className="rounded-xl border border-white/10 bg-white/[.02] p-3">
                      <div className="flex flex-wrap items-center gap-2">
                        <strong className="text-sm text-white">
                          {new Date(`${slot.workDate}T00:00:00`).toLocaleDateString("vi-VN", {
                            weekday: "short",
                            day: "2-digit",
                            month: "2-digit",
                          })}{" "}
                          · {slot.startTime.slice(0, 5)}–{slot.endTime.slice(0, 5)}
                        </strong>
                        <span className="text-xs text-slate-500">{slot.assistantName}</span>
                        <span className="ml-auto text-xs text-slate-500">
                          {slot.registeredCount}/{slot.capacity}
                        </span>
                      </div>
                      {slot.note && <p className="mt-1 text-xs text-slate-400">{slot.note}</p>}
                      <button
                        type="button"
                        onClick={() => toggleRegistration(slot)}
                        disabled={busySlotId === slot.id || full}
                        className={`mt-2 min-h-11 w-full rounded-lg py-2 text-sm font-bold disabled:opacity-40 ${
                          registered
                            ? "border border-white/15 text-slate-300"
                            : "bg-blue-600 text-white"
                        }`}
                      >
                        {registered ? "Huỷ đăng ký" : full ? "Đã đủ số lượng" : "Đăng ký"}
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </div>}
        </div>
      </Section>}

      <Link
        href="/lop-hoc"
        className="flex items-center justify-between gap-3 rounded-2xl border border-white/10 bg-panel p-4 text-sm font-semibold text-slate-200 hover:bg-white/5 sm:p-5"
      >
        Xem toàn bộ chương trình lớp {className}
        <ChevronRight size={16} className="shrink-0 text-slate-500" />
      </Link>

      <div className="grid gap-4 sm:grid-cols-[1.15fr_1fr] sm:items-start">
        <RankCard status={rank} />
        <TitleShowcase titles={titles} displayCode={rank?.display_title?.code ?? null} className="h-full" />
      </div>
      <DailyStreakCard status={rank} suggestion={dailySuggestion} />
      <ClassRankBoard classId={classId} />
      <HonorVisibilityPicker />


      {quizNeed && (
        <TutoringExitQuiz
          need={quizNeed}
          studentId={studentId}
          exitWindow={quizWindow ?? undefined}
          onClose={() => {
            setQuizNeed(null);
            setQuizWindow(null);
            reloadTutoring();
          }}
          onCleared={() => {
            setQuizNeed(null);
            setQuizWindow(null);
            reloadTutoring();
          }}
        />
      )}
    </div>
  );
}
