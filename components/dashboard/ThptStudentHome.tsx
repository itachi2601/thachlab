"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ChevronRight, Flame, LogOut, QrCode, Trophy } from "lucide-react";
import type { Profile } from "@/components/auth/AuthProvider";
import AvatarUploader from "@/components/account/AvatarUploader";
import type { SchoolClass } from "@/features/exams/types";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { expandClassIdsByGrade } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { useToast } from "@/components/ui/Toast";
import PwaInstallCard from "@/components/pwa/PwaInstallCard";
import TodayCard from "@/components/dashboard/TodayCard";
import TutoringSection, { liveExitWindows } from "@/components/dashboard/TutoringSection";
import { rankNextSteps } from "@/features/learning/next-steps";
import CatchupCard from "@/components/results/CatchupCard";
import QuickPractice, { type QuickPracticeRequest } from "@/components/mastery/QuickPractice";
import {
  fetchMyProgressMarks,
  summarizeLessonProgress,
  type LessonProgressSummary,
  type LessonWithItemRefs,
  type MyProgressMarks,
} from "@/services/lessons";
import { fetchChaptersStatic, fetchClassesStatic, fetchLessonsStatic } from "@/services/static-content";
import { fetchMyAlert, fetchMyScoreHistory, type ScorePoint, type StudentAlert } from "@/services/analytics";
import RankAvatarFrame from "@/components/rank/RankAvatarFrame";
import WornTitle from "@/components/rank/WornTitle";
import StreakWeek from "@/components/rank/StreakWeek";
import type { RankStatus } from "@/features/rank/types";
import { fetchMyRankStatus, fetchMyStreakDays, type StreakDay } from "@/services/rank";
import { fetchMyWeakestTopics, type WeakTopic } from "@/services/mastery";
import WelcomeBackDialog from "@/components/dashboard/WelcomeBackDialog";
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
import { setTodayBadge } from "@/lib/today-badge";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

function HeroStats({
  rank,
  days,
  weekGain,
}: {
  rank: RankStatus | null | undefined;
  days: StreakDay[] | null;
  weekGain: number | null;
}) {
  const daily = rank?.season ? rank.daily : null;
  const next = rank?.next;
  const freezeLeft = daily ? Math.max(0, (daily.freeze_per_week ?? 0) - (daily.freeze_used_week ?? 0)) : 0;
  if (!rank?.season && weekGain === null) return null;
  return (
    <div className="relative mt-4 space-y-3 sm:mt-5">
      {next && rank && (
        <div>
          <div className="flex items-center justify-between gap-3 text-[13px] text-slate-300">
            <span className="flex items-center gap-1.5">
              <Trophy size={14} className="shrink-0 text-amber-300" aria-hidden />
              Còn <b className="text-white">{next.rp_needed} RP</b> nữa là lên {next.name}
            </span>
            <Link href="/lop-hoc/xep-hang" className="-my-3 inline-flex min-h-11 shrink-0 items-center gap-0.5 text-blue-200 hover:text-white">
              Xếp hạng <ChevronRight size={14} />
            </Link>
          </div>
          <div className="mt-1 h-2 overflow-hidden rounded-full bg-white/10">
            <div
              className="h-full rounded-full bg-amber-400"
              style={{ width: `${Math.max(3, Math.min(100, Math.round((100 * rank.rp) / Math.max(1, rank.rp + next.rp_needed))))}%` }}
            />
          </div>
        </div>
      )}
      {daily && (
        <div className="space-y-2 border-t border-white/10 pt-3">
          <p className="flex items-center gap-2 text-sm font-semibold text-white">
            <Flame size={18} className={daily.streak > 0 ? "text-amber-400" : "text-slate-500"} fill={daily.streak > 0 ? "currentColor" : "none"} aria-hidden />
            {daily.streak > 0 ? `Chuỗi ${daily.streak} ngày` : "Bắt đầu chuỗi ngày"}
            {daily.today_done && <span className="text-xs font-normal text-emerald-300">đã giữ hôm nay ✓</span>}
          </p>
          {days && days.length > 0 && <StreakWeek days={days} />}
          {daily.streak > 0 && freezeLeft > 0 && !daily.today_done && (
            <p className="text-[13px] text-sky-300">Tuần này còn {freezeLeft} lượt đóng băng: lỡ một ngày chuỗi vẫn không gãy.</p>
          )}
        </div>
      )}
      {weekGain !== null && (
        <p className="border-t border-white/10 pt-3 text-[13px] text-slate-300">
          Tiến bộ so với tuần trước:{" "}
          <b className="text-emerald-300">{weekGain > 0 ? `+${String(weekGain).replace(".", ",")} điểm` : "giữ vững phong độ"}</b>
        </p>
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
  const [streakDays, setStreakDays] = useState<StreakDay[] | null>(null);
  // undefined = đang tải; [] = không có / RPC chưa chạy. Một lần tải, dùng cho cả thẻ "Hôm nay" lẫn thẻ kỹ năng yếu.
  const [weakTopics, setWeakTopics] = useState<WeakTopic[] | undefined>(undefined);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [scoresLoaded, setScoresLoaded] = useState(false);
  const [lastLessonId, setLastLessonId] = useState(0);
  // Danh mục lớp/chương/bài đã về (kể cả lỗi) — trước đó chưa biết "bài kế" nên chưa vẽ việc hôm nay, tránh chớp "Ôn lại".
  const [catalogLoaded, setCatalogLoaded] = useState(false);

  const [practice, setPractice] = useState<QuickPracticeRequest | null>(null);
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
    fetchMyStreakDays().then(setStreakDays);
    fetchMyWeakestTopics(3).then(setWeakTopics).catch(() => setWeakTopics([]));
  }, [studentId]);

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
  // "Tiến bộ so với tuần trước" (thay Điểm TB, thầy chốt 8/10/2026): điểm TB 7 ngày qua so với 7 ngày trước đó.
  // Chỉ hiện khi tăng hoặc bằng và cả hai tuần đều có bài — điểm giảm thì không khoe số (L4, không so sánh làm nản).
  const weekGain = useMemo(() => {
    const now = nowMs;
    const DAY = 86_400_000;
    const avg = (from: number, to: number) => {
      const xs = scores.filter((p) => {
        const t = new Date(p.at).getTime();
        return t >= from && t < to;
      });
      return xs.length ? { mean: xs.reduce((sum, p) => sum + p.score, 0) / xs.length, n: xs.length } : null;
    };
    const cur = avg(now - 7 * DAY, now + DAY);
    const prev = avg(now - 14 * DAY, now - 7 * DAY);
    if (!cur || !prev) return null;
    const diff = Math.round((cur.mean - prev.mean) * 10) / 10;
    return diff >= 0 ? diff : null;
  }, [scores, nowMs]);
  // Bài đã làm nhưng chưa đạt — gợi ý làm lại khi không còn bài nào tồn đọng.
  const retryExam = useMemo(() => {
    const worst = new Map<number, ScorePoint>();
    for (const point of scores) {
      const cur = worst.get(point.examId);
      if (!cur || point.score > cur.score) worst.set(point.examId, point); // điểm tốt nhất của đề
    }
    return [...worst.values()].filter((p) => p.score < 6.5).sort((a, b) => a.score - b.score)[0] ?? null;
  }, [scores]);

  // Kỹ năng yếu nhất (chỉ khi bài chứa nó có trong lớp để dựng được liên kết) và bài đã học xong gần nhất (để ôn cách quãng).
  const weakList = useMemo(
    () =>
      (weakTopics ?? []).flatMap((t) => {
        const lesson = classLessons?.find((l) => l.id === t.lessonId);
        return lesson
          ? [{ topicId: t.topicId, topicName: t.topicName, lessonId: t.lessonId, lessonTitle: t.lessonTitle, chapterId: lesson.chapter_id, pct: t.pct }]
          : [];
      }),
    [weakTopics, classLessons],
  );
  const reviewLesson = useMemo(() => {
    if (!classLessons) return null;
    const done = classLessons.filter((l) => {
      const summary = progress.get(l.id);
      return summary && summary.total > 0 && summary.completed >= summary.total;
    });
    const last = done[done.length - 1];
    return last ? { id: last.id, chapterId: last.chapter_id, title: last.title } : null;
  }, [classLessons, progress]);

  const nextSteps = useMemo(
    () =>
      rankNextSteps({
        need: needs[0] ? { id: needs[0].id, label: needLabel(needs[0]) } : null,
        needAvailableAt: needs[0] ? nextExitAttemptAt(lastExitAttempt.get(needs[0].id), nowMs) : null,
        retryExam,
        nextLesson: nextLesson
          ? {
              id: nextLesson.id,
              chapterId: nextLesson.chapter_id,
              title: nextLesson.title,
              chapterTitle: nextChapter?.title,
              completed: progress.get(nextLesson.id)?.completed,
              total: progress.get(nextLesson.id)?.total ?? nextLesson.itemCount,
            }
          : null,
        weak: weakList,
        reviewLesson,
      }),
    [needs, lastExitAttempt, nowMs, retryExam, nextLesson, nextChapter, progress, weakList, reviewLesson],
  );

  // Thẻ "Hôm nay em làm gì": chỉ việc thích ứng theo hồ sơ em (rankNextSteps). Việc đầu là nút nổi duy nhất của trang (B2, L5);
  // tối đa 3 lựa chọn khác (N2). Chờ đủ điểm + kỹ năng yếu + danh mục mới vẽ (tránh chớp "Ôn lại").
  const attentionReady = scoresLoaded && catalogLoaded && weakTopics !== undefined;
  const todaySteps = attentionReady ? nextSteps : [];
  const primaryStep = todaySteps[0] ?? null;
  const secondarySteps = todaySteps.slice(1);
  const alertText =
    attentionReady && alert && alert.kind !== "missed_assessment"
      ? alert.kind === "exam_violation"
        ? "Bài kiểm tra gần đây bị ghi nhận rời màn hình nhiều lần — trợ giảng sẽ kiểm tra lại kiến thức của em."
        : "Điểm kiểm tra đang thấp — trợ giảng sẽ liên hệ sắp lịch phụ đạo."
      : null;
  const showToday = attentionReady && (primaryStep !== null || alertText !== null);

  // Chấm đỏ ở nút "Hôm nay" của thanh đáy: chỉ cập nhật khi đã tải đủ dữ liệu (tránh chớp tắt).
  useEffect(() => {
    if (attentionReady) setTodayBadge(studentId, showToday);
  }, [attentionReady, showToday, studentId]);

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
                Chào {profile?.full_name || "bạn"} quay lại
              </h1>
              {rank?.display_title && <WornTitle title={rank.display_title} size="md" className="mt-1 max-w-full" />}
              <p className="mt-1 text-[13px] text-slate-400 sm:text-sm">
                Lớp {className}
                <span className="text-slate-600"> · </span>
                <Link href="/lop-hoc" className="-my-3 inline-flex min-h-11 items-center gap-0.5 text-blue-200 hover:text-white">
                  Chương trình lớp <ChevronRight size={14} />
                </Link>
              </p>
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            {/* Thầy chiếu mã QR của đề lên bảng → em quét là vào đúng đề (app/quet-ma).
                Hạ cấp thành nút viền như "Đăng xuất" để không tranh chỗ nổi bật với thẻ Hôm nay (B2). */}
            <Link
              href="/quet-ma"
              aria-label="Quét mã QR của đề"
              className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-white/10 text-slate-300 hover:border-white/30 hover:text-white sm:h-auto sm:w-auto sm:gap-2 sm:px-4 sm:py-2 sm:text-sm sm:font-bold"
            >
              <QrCode size={16} />
              <span className="hidden sm:inline">Quét mã</span>
            </Link>
            <button
              onClick={onSignOut}
              aria-label="Đăng xuất"
              className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/10 text-slate-300 sm:h-auto sm:w-auto sm:gap-2 sm:px-4 sm:py-2 sm:text-sm sm:font-bold"
            >
              <LogOut size={16} />
              <span className="hidden sm:inline">Đăng xuất</span>
            </button>
          </div>
        </div>
        <HeroStats rank={rank} days={streakDays} weekGain={weekGain} />
      </section>

      {/* Mục 1 — MỘT thẻ việc hôm nay (N4, B2, L5): thay cho NextStepsCard + khối "Việc cần làm" + dòng gợi ý ở thẻ chuỗi ngày (7/10/2026) */}
      {showToday && (
        <TodayCard
          rank={rank}
          primary={primaryStep}
          secondary={secondarySteps}
          alertText={alertText}
          onUnlock={(needId) => setQuizNeed(needs.find((n) => n.id === needId) ?? null)}
          onQuickPractice={(step) => step.practice && setPractice(step.practice)}
        />
      )}

      <WelcomeBackDialog
        userId={studentId}
        name={profile?.full_name}
        rank={rank}
        days={streakDays}
        primary={primaryStep}
        ready={attentionReady}
        onUnlock={(needId) => setQuizNeed(needs.find((n) => n.id === needId) ?? null)}
        onQuickPractice={(step) => step.practice && setPractice(step.practice)}
      />
      <QuickPractice
        request={practice}
        onClose={() => setPractice(null)}
        onFinished={() => fetchMyWeakestTopics(3).then(setWeakTopics).catch(() => undefined)}
        onUnavailable={(req) => {
          setPractice(null);
          const lesson = classLessons?.find((l) => l.id === req.lessonId);
          window.location.assign(`/lop-hoc/bai?id=${req.lessonId}${lesson ? `&chapter=${lesson.chapter_id}` : ""}`);
        }}
      />

      <PwaInstallCard />

      {/* Mục 3 — Luyện thêm: kỹ năng yếu (tự ẩn khi không có), bù bài cho em vào lớp trễ (tự ẩn), rồi MỘT khối phụ đạo */}
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
