"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import Link from "next/link";
import { CalendarClock, ChevronRight, LogOut, Megaphone } from "lucide-react";
import type { Profile } from "@/components/auth/AuthProvider";
import AvatarUploader from "@/components/account/AvatarUploader";
import type { SchoolClass } from "@/features/exams/types";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { expandClassIdsByGrade } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { useToast } from "@/components/ui/Toast";
import TodayCard, { AnnouncementNote } from "@/components/dashboard/TodayCard";
import TutoringSection, { liveExitWindows } from "@/components/dashboard/TutoringSection";
import { rankNextSteps, type NextStep } from "@/features/learning/next-steps";
import CatchupCard from "@/components/results/CatchupCard";
import WeakestSkillsCard from "@/components/mastery/WeakestSkillsCard";
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
import DailyStreakCard from "@/components/rank/DailyStreakCard";
import type { RankStatus } from "@/features/rank/types";
import { fetchMyRankStatus } from "@/services/rank";
import {
  fetchLatestAnnouncements,
  fetchRecentAnnouncements,
  type AnnouncementKind,
  type ClassAnnouncement,
} from "@/services/announcements";
import {
  ACTIVE_NEED_STATUSES,
  nextExitAttemptAt,
  cancelRegistration,
  fetchMyExitAttempts,
  fetchMyOpenExitWindows,
  fetchMyNeeds,
  fetchMyRegistrations,
  fetchMyWaitlist,
  joinWaitlist,
  leaveWaitlist,
  type WaitlistPosition,
  fetchUpcomingSlots,
  needLabel,
  registerForSlot,
  type ExitWindow,
  type TutoringNeed,
  type TutoringSlot,
} from "@/services/tutoring";
import TutoringExitQuiz from "@/components/results/TutoringExitQuizLazy";
import { fetchOpenClassReviewHomework, type ClassReviewHomework } from "@/services/homework";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

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
  const [assessments, setAssessments] = useState<ClassAssessment[]>([]);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [scoresLoaded, setScoresLoaded] = useState(false);
  const [assessmentsLoaded, setAssessmentsLoaded] = useState(false);
  const [lastLessonId, setLastLessonId] = useState(0);
  // Danh mục lớp/chương/bài đã về (kể cả lỗi) — trước đó chưa biết "bài kế" nên chưa vẽ việc hôm nay, tránh chớp "Ôn lại".
  const [catalogLoaded, setCatalogLoaded] = useState(false);

  const [todayNote, setTodayNote] = useState<ClassAnnouncement | null>(null);
  const [homeworkNotes, setHomeworkNotes] = useState<ClassAnnouncement[]>([]);
  const [reviewHomework, setReviewHomework] = useState<ClassReviewHomework[]>([]);
  const [needs, setNeeds] = useState<TutoringNeed[]>([]);
  const [slots, setSlots] = useState<TutoringSlot[]>([]);
  const [myRegistrations, setMyRegistrations] = useState<Set<number>>(new Set());
  const [myWaitlist, setMyWaitlist] = useState<Map<number, WaitlistPosition>>(new Map());
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
      .catch(() => undefined)
      .finally(() => setCatalogLoaded(true));
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
    fetchMyWaitlist(studentId)
      .then((rows) => setMyWaitlist(new Map(rows.map((r) => [r.slotId, r]))))
      .catch(() => setMyWaitlist(new Map()));
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

  const nextSteps = useMemo(
    () =>
      rankNextSteps({
        need: needs[0] ? { id: needs[0].id, label: needLabel(needs[0]) } : null,
        needAvailableAt: needs[0] ? nextExitAttemptAt(lastExitAttempt.get(needs[0].id), nowMs) : null,
        retryExam,
        nextLesson: nextLesson
          ? { id: nextLesson.id, chapterId: nextLesson.chapter_id, title: nextLesson.title, chapterTitle: nextChapter?.title }
          : null,
      }),
    [needs, lastExitAttempt, nowMs, retryExam, nextLesson, nextChapter],
  );

  // Thẻ "Hôm nay em làm gì": bài kiểm tra được giao → BTVN ôn tập → rankNextSteps (mở khoá → làm lại → học tiếp → ôn lại).
  // Việc đầu là nút nổi duy nhất của trang (B2, L5); tối đa 3 việc phụ (N2). Chờ đủ điểm + bài giao + danh mục mới vẽ.
  const attentionReady = scoresLoaded && assessmentsLoaded && catalogLoaded;
  const assignedSteps: NextStep[] = [
    ...todoExams.map((item) => ({
      kind: "assigned" as const,
      key: `a-${item.id}`,
      action: "Làm bài",
      title: item.examTitle,
      hint: "Bài kiểm tra · chưa làm",
      href: `/kiem-tra/lam?id=${item.examId}`,
    })),
    ...todoReviewHomework.map((item) => ({
      kind: "assigned" as const,
      key: `r-${item.id}`,
      action: "Làm bài",
      title: item.title,
      hint: "BTVN ôn tập · chưa làm",
      href: `/kiem-tra/lam?id=${item.examId}`,
    })),
  ];
  const todaySteps = attentionReady ? [...assignedSteps, ...nextSteps].slice(0, 4) : [];
  const primaryStep = todaySteps[0] ?? null;
  const secondarySteps = todaySteps.slice(1);
  const alertText =
    attentionReady && alert && alert.kind !== "missed_assessment"
      ? alert.kind === "exam_violation"
        ? "Bài kiểm tra gần đây bị ghi nhận rời màn hình nhiều lần — trợ giảng sẽ kiểm tra lại kiến thức của em."
        : "Điểm kiểm tra đang thấp — trợ giảng sẽ liên hệ sắp lịch phụ đạo."
      : null;
  const showToday = Boolean(todayNote) || primaryStep !== null || alertText !== null;

  const liveWindows = liveExitWindows(openWindows, needs, nowMs);
  const showTutoring = needs.length > 0 || slots.length > 0 || liveWindows.length > 0;

  async function toggleRegistration(slot: TutoringSlot) {
    setBusySlotId(slot.id);
    try {
      if (myRegistrations.has(slot.id)) {
        await cancelRegistration(slot.id, studentId);
        toast("info", "Đã huỷ đăng ký.");
      } else if (myWaitlist.has(slot.id)) {
        await leaveWaitlist(slot.id, studentId);
        toast("info", "Đã rời hàng chờ.");
      } else if (slot.registeredCount >= slot.capacity) {
        await joinWaitlist(slot.id, studentId);
        toast("success", "Đã vào hàng chờ — có bạn huỷ hoặc trợ giảng mở lượt tiếp, em sẽ được xếp vào.");
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
              <p className="mt-1 text-[13px] text-slate-400 sm:text-sm">
                Lớp {className}
                <span className="text-slate-600"> · </span>
                <Link href="/lop-hoc" className="inline-flex min-h-11 items-center gap-0.5 text-blue-200 hover:text-white">
                  Chương trình lớp <ChevronRight size={14} />
                </Link>
              </p>
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

      {/* Mục 1 — MỘT thẻ việc hôm nay (N4, B2, L5): thay cho NextStepsCard + khối "Việc cần làm" + dòng gợi ý ở thẻ chuỗi ngày (7/10/2026) */}
      {showToday && (
        <TodayCard
          note={todayNote}
          primary={primaryStep}
          secondary={secondarySteps}
          alertText={alertText}
          onUnlock={(needId) => setQuizNeed(needs.find((n) => n.id === needId) ?? null)}
        />
      )}

      {/* Mục 2 — Bài tập về nhà (ghi chú của GV) */}
      {homeworkNotes.length > 0 && (
        <Section icon={CalendarClock} title="Bài tập về nhà">
          <div className="mt-3 space-y-2">
            {homeworkNotes.map((item) => <AnnouncementNote key={item.id} item={item} />)}
          </div>
        </Section>
      )}

      {/* Mục 3 — Luyện thêm: kỹ năng yếu (tự ẩn khi không có), bù bài cho em vào lớp trễ (tự ẩn), rồi MỘT khối phụ đạo */}
      <WeakestSkillsCard />
      <CatchupCard studentId={studentId} classId={classId} viewer="student" showSlots={false} />
      {showTutoring && (
        <TutoringSection
          needs={needs}
          slots={slots}
          windows={liveWindows}
          windowDone={windowDone}
          nowMs={nowMs}
          lastExitAttempt={lastExitAttempt}
          myRegistrations={myRegistrations}
          myWaitlist={myWaitlist}
          busySlotId={busySlotId}
          onQuiz={(need, w) => {
            setQuizNeed(need);
            setQuizWindow(w ?? null);
          }}
          onToggleSlot={toggleRegistration}
        />
      )}

      {/* Mục 4 — Rank gọn: bậc + RP còn thiếu (link sang /lop-hoc/xep-hang) và chuỗi ngày. Bộ sưu tập, bảng tuần
          của lớp, chọn hiển thị vinh danh đã chuyển sang trang Rank (L3, N1 — thầy chốt 7/10/2026). */}
      <div className="grid gap-4 sm:grid-cols-2 sm:items-stretch">
        <RankCard status={rank} className="h-full" />
        <DailyStreakCard status={rank} className="h-full" />
      </div>

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
