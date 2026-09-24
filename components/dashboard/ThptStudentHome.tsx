"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import Link from "next/link";
import { AlertTriangle, CalendarClock, ChevronRight, LogOut, Megaphone, Trophy, Users } from "lucide-react";
import type { Profile } from "@/components/auth/AuthProvider";
import AvatarUploader from "@/components/account/AvatarUploader";
import type { SchoolClass } from "@/features/exams/types";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { expandClassIdsByGrade, fetchClasses } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { useToast } from "@/components/ui/Toast";
import CatchupCard from "@/components/results/CatchupCard";
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
  type ClassAssessment,
  type ScorePoint,
  type StudentAlert,
} from "@/services/analytics";
import RankBadge from "@/components/rank/RankBadge";
import RankCard from "@/components/rank/RankCard";
import { tierLabel, type RankStatus } from "@/features/rank/types";
import { fetchMyRankStatus } from "@/services/rank";
import {
  fetchLatestAnnouncements,
  fetchRecentAnnouncements,
  type AnnouncementKind,
  type ClassAnnouncement,
} from "@/services/announcements";
import {
  ACTIVE_NEED_STATUSES,
  NEED_STATUS_LABEL,
  cancelRegistration,
  fetchMyNeeds,
  fetchMyRegistrations,
  fetchUpcomingSlots,
  needLabel,
  registerForSlot,
  type NeedStatus,
  type TutoringNeed,
  type TutoringSlot,
} from "@/services/tutoring";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

const NEED_TONE: Record<NeedStatus, string> = {
  open: "border-red-500/40 bg-red-500/10 text-red-200",
  assigned: "border-amber-500/40 bg-amber-500/10 text-amber-200",
  tutored: "border-blue-500/40 bg-blue-500/10 text-blue-200",
  cleared: "border-emerald-500/40 bg-emerald-500/10 text-emerald-200",
  dismissed: "border-white/15 bg-white/5 text-slate-400",
};

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
      <p className="mt-1.5 text-[11px] text-slate-500">
        {item.createdByName || "Giáo viên"} ·{" "}
        {new Date(item.createdAt).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })}
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
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<Lesson[] | null>(null);
  const [progress, setProgress] = useState<Map<number, LessonProgressSummary>>(new Map());
  const [scores, setScores] = useState<ScorePoint[]>([]);
  const [rank, setRank] = useState<RankStatus | null | undefined>(undefined);
  const [assessments, setAssessments] = useState<ClassAssessment[]>([]);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [lastLessonId, setLastLessonId] = useState(0);

  const [todayNote, setTodayNote] = useState<ClassAnnouncement | null>(null);
  const [homeworkNotes, setHomeworkNotes] = useState<ClassAnnouncement[]>([]);
  const [needs, setNeeds] = useState<TutoringNeed[]>([]);
  const [slots, setSlots] = useState<TutoringSlot[]>([]);
  const [myRegistrations, setMyRegistrations] = useState<Set<number>>(new Set());
  const [busySlotId, setBusySlotId] = useState<number | null>(null);

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
    fetchMyAlert(studentId).then(setAlert).catch(() => setAlert(null));
    fetchMyRankStatus().then(setRank).catch(() => setRank(null));
    fetchClassAssessments(classId).then(setAssessments).catch(() => setAssessments([]));
  }, [studentId, classId]);

  function reloadAnnouncements() {
    fetchLatestAnnouncements(classId)
      .then((byKind) => setTodayNote(byKind.today_task))
      .catch(() => setTodayNote(null));
    fetchRecentAnnouncements(classId, "homework" as AnnouncementKind, 5)
      .then(setHomeworkNotes)
      .catch(() => setHomeworkNotes([]));
  }
  useEffect(reloadAnnouncements, [classId]);

  function reloadTutoring() {
    fetchMyNeeds(studentId)
      .then((rows) => setNeeds(rows.filter((n) => ACTIVE_NEED_STATUSES.includes(n.status))))
      .catch(() => setNeeds([]));
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

  const hasTodayContent = Boolean(todayNote) || Boolean(nextLesson) || todoExams.length > 0;

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
      <section className="relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-[#172c46] via-[#0e1c32] to-[#071426] p-4 sm:rounded-3xl sm:p-8">
        <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="relative flex items-start justify-between gap-3">
          <div className="flex min-w-0 items-start gap-3 sm:gap-4">
            <AvatarUploader studentId={studentId} url={profile?.avatar_url} name={profile?.full_name} size={56} />
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
        <Link
          href="/lop-hoc/xep-hang/"
          className="flex items-center gap-2 rounded-xl border border-blue-500/15 bg-blue-500/5 p-3 sm:rounded-2xl sm:p-5"
        >
          <RankBadge code={rank?.tier?.code} division={rank?.tier?.division} size={30} className="shrink-0 sm:hidden" />
          <RankBadge code={rank?.tier?.code} division={rank?.tier?.division} size={44} className="hidden shrink-0 sm:block" />
          <span className="min-w-0">
            <strong className="block truncate text-sm text-white sm:text-lg">
              {rank?.season ? tierLabel(rank.tier?.code, rank.tier?.division) : "—"}
            </strong>
            <p className="mt-1 truncate text-[9px] font-bold uppercase tracking-wide text-blue-300 sm:text-xs sm:tracking-wider">
              Xếp hạng
            </p>
          </span>
        </Link>
      </section>

      <RankCard status={rank} name={profile?.full_name} />

      {/* Mục 1 — Việc cần làm trong buổi học hiện tại */}
      <Section icon={Megaphone} title="Việc cần làm hôm nay">
        <div className="mt-3 space-y-2.5">
          {todayNote && <AnnouncementNote item={todayNote} />}

          {nextLesson && (
            <Link
              href={`/lop-hoc/bai?id=${nextLesson.id}&chapter=${nextLesson.chapter_id}`}
              className="flex items-center justify-between gap-3 rounded-xl border border-blue-400/20 bg-blue-500/5 p-3 hover:bg-blue-500/10"
            >
              <div className="min-w-0">
                <small className="text-[10px] font-bold uppercase tracking-wider text-blue-300">Học tiếp theo</small>
                <p className="mt-0.5 truncate text-sm font-bold text-white">{nextLesson.title}</p>
                {nextChapter && <p className="truncate text-xs text-slate-400">{nextChapter.title}</p>}
              </div>
              <ChevronRight className="shrink-0 text-blue-300" size={18} />
            </Link>
          )}

          {todoExams.map((item) => (
            <Link
              key={item.id}
              href={`/kiem-tra/lam?id=${item.examId}`}
              className="flex items-center justify-between gap-3 rounded-xl bg-white/[.02] p-3 hover:bg-white/5"
            >
              <span className="flex min-w-0 items-center gap-2">
                <Trophy size={14} className="shrink-0 text-amber-300" />
                <span className="min-w-0">
                  <strong className="block truncate text-sm text-white">{item.examTitle}</strong>
                  <small className="text-xs text-slate-500">Bài kiểm tra chưa làm</small>
                </span>
              </span>
              <ChevronRight size={16} className="shrink-0 text-slate-500" />
            </Link>
          ))}

          {!hasTodayContent && <p className="text-sm text-slate-500">Chưa có việc gì mới — cứ ôn lại bài cũ nhé.</p>}
        </div>
      </Section>

      {/* Mục 2 — Bài tập về nhà */}
      <Section icon={CalendarClock} title="Bài tập về nhà">
        <div className="mt-3 space-y-2">
          {homeworkNotes.length === 0 ? (
            <p className="text-sm text-slate-500">Chưa có bài tập về nhà mới.</p>
          ) : (
            homeworkNotes.map((item) => <AnnouncementNote key={item.id} item={item} />)
          )}
        </div>
      </Section>

      {/* Mục 3 — Chủ đề cần phụ đạo */}
      <CatchupCard studentId={studentId} classId={classId} viewer="student" />

      <Section icon={Users} title="Chủ đề cần phụ đạo">
        <div className="mt-3 space-y-4">
          {needs.length === 0 ? (
            <p className="text-sm text-slate-500">Hiện chưa có chủ đề nào cần phụ đạo — cứ tiếp tục học nhé!</p>
          ) : (
            <div className="flex flex-wrap gap-1.5">
              {needs.map((need) => (
                <span
                  key={need.id}
                  className={`rounded-full border px-3 py-1 text-xs font-semibold ${NEED_TONE[need.status]}`}
                >
                  {needLabel(need)} · {NEED_STATUS_LABEL[need.status]}
                </span>
              ))}
            </div>
          )}

          <div>
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Buổi phụ đạo sắp tới</p>
            {slots.length === 0 ? (
              <p className="text-sm text-slate-500">Chưa có buổi phụ đạo nào được đăng cho lớp em.</p>
            ) : (
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
                        className={`mt-2 w-full rounded-lg py-2 text-xs font-bold disabled:opacity-40 ${
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
          </div>
        </div>
      </Section>

      <Link
        href="/lop-hoc"
        className="flex items-center justify-between gap-3 rounded-2xl border border-white/10 bg-panel p-4 text-sm font-semibold text-slate-200 hover:bg-white/5 sm:p-5"
      >
        Xem toàn bộ chương trình lớp {className}
        <ChevronRight size={16} className="shrink-0 text-slate-500" />
      </Link>
    </div>
  );
}
