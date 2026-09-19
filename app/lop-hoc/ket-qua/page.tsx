"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AlertTriangle, ArrowRight, ChevronDown, Target, Trophy } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import Html from "@/components/exams/ContentHtml";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import {
  fetchMyAlert,
  fetchMyScoreHistory,
  fetchMyTopicGaps,
  fetchMyWrongQuestions,
  fetchOutcomeGaps,
  fetchPeriodicRank,
  fetchQuestionTopics,
  outcomeGapsByNeed,
  type OutcomeGap,
  type PeriodicRank,
  type ScorePoint,
  type StudentAlert,
  type TopicGap,
} from "@/services/analytics";
import {
  NEED_STATUS_LABEL,
  fetchMyNeeds,
  needLabel,
  type NeedStatus,
  type TutoringNeed,
} from "@/services/tutoring";
import { fetchMyClassIds } from "@/services/classes";
import { supabaseConfigured } from "@/services/supabase";

const PASS = 6.5;

function ScoreTrend({ points }: { points: ScorePoint[] }) {
  if (points.length === 0) return null;
  const W = 640;
  const H = 200;
  const padL = 30;
  const padB = 26;
  const padT = 14;
  const innerW = W - padL - 12;
  const innerH = H - padT - padB;
  const x = (i: number) =>
    padL + (points.length === 1 ? innerW / 2 : (i / (points.length - 1)) * innerW);
  const y = (score: number) => padT + innerH - (score / 10) * innerH;
  const passY = y(PASS);
  const line = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(i)},${y(p.score)}`).join(" ");

  return (
    <div className="overflow-x-auto">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full min-w-[420px]"
        role="img"
        aria-label="Điểm các bài kiểm tra theo thời gian"
      >
        {[0, 2.5, 5, 7.5, 10].map((g) => (
          <g key={g}>
            <line
              x1={padL}
              x2={W - 12}
              y1={y(g)}
              y2={y(g)}
              stroke="currentColor"
              strokeOpacity="0.12"
            />
            <text x={padL - 6} y={y(g) + 4} textAnchor="end" fontSize="10" fill="currentColor" fillOpacity="0.5">
              {g}
            </text>
          </g>
        ))}
        <line
          x1={padL}
          x2={W - 12}
          y1={passY}
          y2={passY}
          stroke="#f59e0b"
          strokeDasharray="4 4"
          strokeOpacity="0.8"
        />
        <text x={W - 12} y={passY - 5} textAnchor="end" fontSize="10" fill="#f59e0b">
          đạt 6,5
        </text>
        <path d={line} fill="none" stroke="#60A5FA" strokeWidth="2" />
        {points.map((p, i) => (
          <g key={p.resultId}>
            <circle
              cx={x(i)}
              cy={y(p.score)}
              r="4"
              fill={p.score >= PASS ? "#34D399" : "#F43F5E"}
              stroke="#0B1020"
              strokeWidth="1.5"
            />
            <title>
              {p.examTitle} — {p.score.toLocaleString("vi-VN")} điểm
              {p.periodic ? ` (${p.kindLabel})` : ""}
            </title>
          </g>
        ))}
      </svg>
    </div>
  );
}

function formLabel(form: string) {
  return form === "ly_thuyet" || form === "bai_tap"
    ? QUESTION_FORM_LABELS[form]
    : "Chưa phân loại";
}

function GapRow({
  gap,
  lessonHref,
}: {
  gap: TopicGap;
  lessonHref: (topicName: string, form: string) => string | null;
}) {
  const { session } = useAuth();
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<
    Awaited<ReturnType<typeof fetchMyWrongQuestions>> | null
  >(null);
  const href = lessonHref(gap.topic, gap.form);

  useEffect(() => {
    if (!open || items || !session) return;
    fetchMyWrongQuestions(session.user.id, gap.topic, gap.form)
      .then(setItems)
      .catch(() => setItems([]));
  }, [open, items, session, gap.topic, gap.form]);

  const tone =
    gap.pct >= 60
      ? "border-red-500/25 bg-red-500/[.05]"
      : gap.pct >= 30
        ? "border-amber-500/25 bg-amber-500/[.05]"
        : "border-white/10";

  return (
    <div className={`rounded-2xl border ${tone}`}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="flex w-full items-center gap-4 p-4 text-left"
      >
        <span className="min-w-0 flex-1">
          <span className="block font-display font-semibold text-white">{gap.topic}</span>
          <span className="mt-0.5 block text-xs text-slate-400">
            {formLabel(gap.form)} · sai {gap.wrong}/{gap.total} câu
          </span>
        </span>
        <span
          className={`shrink-0 font-mono text-lg font-bold ${
            gap.pct >= 60 ? "text-red-300" : gap.pct >= 30 ? "text-amber-300" : "text-slate-300"
          }`}
        >
          {gap.pct}%
        </span>
        <ChevronDown
          size={18}
          className={`shrink-0 text-slate-500 transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open && (
        <div className="space-y-4 border-t border-white/10 p-4">
          {href && (
            <Link
              href={href}
              className="inline-flex items-center gap-2 rounded-xl bg-[#2563EB] px-4 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
            >
              Ôn lại {formLabel(gap.form).toLowerCase()} phần này →
            </Link>
          )}
          {items === null ? (
            <p className="text-sm text-slate-400">Đang tải câu sai…</p>
          ) : items.length === 0 ? (
            <p className="text-sm text-slate-500">Không tìm được chi tiết câu sai.</p>
          ) : (
            <ul className="space-y-2">
              {items.map((it) => (
                <li key={`${it.ref.examResultId}-${it.ref.questionIndex}`}>
                  <Link
                    href={`/lop-hoc/ket-qua/chi-tiet/?id=${it.ref.examResultId}#cau-${it.ref.questionIndex + 1}`}
                    className="flex items-start gap-3 rounded-xl border border-white/10 bg-white/5 px-4 py-3 hover:border-white/25"
                  >
                    <span className="min-w-0 flex-1">
                      <span className="block text-xs font-bold uppercase tracking-wide text-slate-500">
                        {it.ref.examTitle} · Câu {it.ref.questionIndex + 1}
                      </span>
                      <span className="mt-1 line-clamp-2 block text-sm text-slate-300">
                        <Html html={it.question.question} />
                      </span>
                    </span>
                    <ArrowRight size={16} className="mt-1 shrink-0 text-slate-500" />
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

function RankSummary({ rank }: { rank: PeriodicRank }) {
  return (
    <span className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-[#0B1020] px-4 py-2 text-sm text-slate-300">
      <Trophy size={16} className="text-amber-300" />
      Hạng <b className="text-white">{rank.rank}</b>/{rank.total} trong lớp
      <span className="text-slate-500">
        · TB {rank.myAvg.toLocaleString("vi-VN", { maximumFractionDigits: 1 })}
      </span>
    </span>
  );
}

function AttemptRow({ point }: { point: ScorePoint }) {
  const dateLabel = new Date(point.at).toLocaleDateString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });

  return (
    <Link
      href={`/lop-hoc/ket-qua/chi-tiet/?id=${point.resultId}`}
      className="flex items-center gap-4 rounded-2xl border border-white/10 p-4 hover:border-white/25"
    >
      <span className="min-w-0 flex-1">
        <span className="block font-display font-semibold text-white">{point.examTitle}</span>
        <span className="mt-0.5 block text-xs text-slate-400">
          {dateLabel}
          {point.periodic ? ` · ${point.kindLabel}` : ""}
        </span>
      </span>
      <span
        className={`shrink-0 font-mono text-lg font-bold ${
          point.score >= PASS ? "text-emerald-300" : "text-red-300"
        }`}
      >
        {point.score.toLocaleString("vi-VN")}
      </span>
      <ArrowRight size={18} className="shrink-0 text-slate-500" />
    </Link>
  );
}

function AlertBanner({ alert }: { alert: StudentAlert }) {
  return (
    <section className="rounded-2xl border border-amber-400/25 bg-gradient-to-r from-amber-500/10 to-transparent p-5">
      <div className="flex items-center gap-2 text-amber-300">
        <AlertTriangle size={18} />
        <h2 className="font-display font-bold text-white">Cần chú ý</h2>
      </div>
      <p className="mt-2 text-sm text-amber-100/80">
        {alert.kind === "missed_assessment"
          ? "Em còn bài kiểm tra chưa làm — hãy hoàn thành sớm."
          : "Điểm kiểm tra của em đang thấp. Trợ giảng sẽ liên hệ để sắp lịch phụ đạo. Cố gắng ôn lại các chủ đề dưới đây nhé."}
      </p>
      {alert.handledNote && (
        <p className="mt-1 text-xs text-slate-400">Ghi chú: {alert.handledNote}</p>
      )}
    </section>
  );
}

const NEED_TONE: Record<NeedStatus, string> = {
  open: "border-red-500/30 bg-red-500/[.06] text-red-200",
  assigned: "border-amber-500/30 bg-amber-500/[.06] text-amber-200",
  tutored: "border-blue-500/30 bg-blue-500/[.06] text-blue-200",
  cleared: "border-emerald-500/30 bg-emerald-500/[.06] text-emerald-200",
  dismissed: "border-white/10 bg-white/[.03] text-slate-400",
};

/** Cách nói với chính học sinh — không dùng chữ "cảnh báo" cho em. */
const NEED_NOTE: Record<NeedStatus, string> = {
  open: "Thầy đã ghi nhận, sẽ sắp buổi phụ đạo cho em.",
  assigned: "Đã có trợ giảng nhận kèm em phần này.",
  tutored: "Em đã được dạy lại phần này — làm bài sau để chốt.",
  cleared: "Em đã làm đúng lại phần này. Giỏi!",
  dismissed: "Phần này tạm gác lại.",
};

function NeedRow({
  need,
  lessonHref,
  outcomes,
}: {
  need: TutoringNeed;
  lessonHref: (topicName: string, form: string) => string | null;
  outcomes: OutcomeGap[];
}) {
  const href = lessonHref(need.topicName, need.form);
  return (
    <div className={`rounded-2xl border p-4 ${NEED_TONE[need.status]}`}>
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <span className="font-display font-semibold text-white">{needLabel(need)}</span>
        <span className="rounded-full border border-current px-2.5 py-0.5 text-xs font-bold">
          {NEED_STATUS_LABEL[need.status]}
        </span>
        {href && (
          <Link
            href={href}
            className="ml-auto text-xs font-semibold text-blue-300 underline-offset-2 hover:underline"
          >
            Ôn lại bài
          </Link>
        )}
      </div>
      {outcomes.length > 0 && (
        <ul className="mt-2 space-y-0.5 text-xs text-slate-300">
          {outcomes.map((o) => (
            <li key={o.topicId}>
              · {o.topicName} — sai {o.wrong}/{o.total} câu
            </li>
          ))}
        </ul>
      )}
      <p className="mt-1 text-xs text-slate-400">{NEED_NOTE[need.status]}</p>
    </div>
  );
}

function Dashboard() {
  const { session } = useAuth();
  const [points, setPoints] = useState<ScorePoint[] | null>(null);
  const [gaps, setGaps] = useState<TopicGap[] | null>(null);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [needs, setNeeds] = useState<TutoringNeed[] | null>(null);
  const [lessonByTopic, setLessonByTopic] = useState<Map<string, number | null>>(new Map());
  const [outcomeGaps, setOutcomeGaps] = useState<OutcomeGap[]>([]);
  const [periodicRank, setPeriodicRank] = useState<PeriodicRank | null>(null);

  useEffect(() => {
    if (!session) return;
    const uid = session.user.id;
    fetchMyScoreHistory(uid).then(setPoints).catch(() => setPoints([]));
    fetchMyTopicGaps(uid).then(setGaps).catch(() => setGaps([]));
    fetchMyAlert(uid).then(setAlert).catch(() => setAlert(null));
    fetchMyNeeds(uid).then(setNeeds).catch(() => setNeeds([]));
    fetchOutcomeGaps(uid).then(setOutcomeGaps).catch(() => setOutcomeGaps([]));
    fetchQuestionTopics()
      .then((topics) => setLessonByTopic(new Map(topics.map((t) => [t.name, t.lessonId]))))
      .catch(() => undefined);
    fetchMyClassIds(uid)
      .then((classIds) => (classIds.length > 0 ? fetchPeriodicRank(classIds[0]) : null))
      .then(setPeriodicRank)
      .catch(() => setPeriodicRank(null));
  }, [session]);

  const lessonHref = useMemo(
    () => (topicName: string, form: string) => {
      const lesson = lessonByTopic.get(topicName);
      if (!lesson) return null;
      const stage = form === "ly_thuyet" ? "ly_thuyet" : "bai_tap_mau";
      return `/lop-hoc/bai/?id=${lesson}#secondary-stage-${stage}`;
    },
    [lessonByTopic],
  );

  const avg = useMemo(() => {
    if (!points || points.length === 0) return null;
    return Math.round((points.reduce((a, p) => a + p.score, 0) / points.length) * 10) / 10;
  }, [points]);

  // Chi tiết mịn: trong mỗi phần cần phụ đạo, em còn sai đúng yêu cầu cần đạt nào.
  const outcomesByNeed = useMemo(() => outcomeGapsByNeed(outcomeGaps), [outcomeGaps]);

  const priorityGaps = (gaps ?? []).filter((g) => g.wrong > 0);
  const attempts = useMemo(() => (points ? [...points].reverse() : null), [points]);

  return (
    <div className="mx-auto w-full max-w-4xl px-6 pb-20 pt-28">
      <div className="flex flex-wrap items-center gap-3">
        <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/15 text-blue-300">
          <Target size={20} />
        </span>
        <div>
          <h1 className="font-display text-2xl font-bold text-white">Kết quả học tập</h1>
          <p className="text-sm text-slate-400">
            Điểm kiểm tra và những chủ đề em cần ôn lại.
          </p>
        </div>
        {periodicRank && (
          <div className="ml-auto">
            <RankSummary rank={periodicRank} />
          </div>
        )}
      </div>

      {alert && (
        <div className="mt-6">
          <AlertBanner alert={alert} />
        </div>
      )}

      <section className="mt-6 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="font-display font-semibold text-white">Điểm theo thời gian</h2>
          {avg !== null && (
            <span className="text-sm text-slate-400">
              trung bình <b className="text-white">{avg.toLocaleString("vi-VN")}</b>
            </span>
          )}
        </div>
        {points === null ? (
          <p className="text-sm text-slate-400">Đang tải…</p>
        ) : points.length === 0 ? (
          <p className="text-sm text-slate-500">Em chưa làm bài kiểm tra nào.</p>
        ) : (
          <div className="text-slate-300">
            <ScoreTrend points={points} />
          </div>
        )}
      </section>

      <section className="mt-6">
        <h2 className="mb-3 font-display font-semibold text-white">Bài đã làm</h2>
        {attempts === null ? (
          <p className="text-sm text-slate-400">Đang tải…</p>
        ) : attempts.length === 0 ? (
          <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-sm text-slate-500">
            Em chưa làm bài kiểm tra nào.
          </p>
        ) : (
          <div className="space-y-3">
            {attempts.map((p) => (
              <AttemptRow key={p.resultId} point={p} />
            ))}
          </div>
        )}
      </section>

      {needs !== null && needs.length > 0 && (
        <section className="mt-6">
          <h2 className="mb-1 font-display font-semibold text-white">Phần em cần phụ đạo</h2>
          <p className="mb-3 text-sm text-slate-400">
            Phần nào thầy và trợ giảng đã dạy lại, phần nào em đã làm đúng trở lại.
          </p>
          <div className="space-y-2">
            {needs.map((need) => (
              <NeedRow
                key={need.id}
                need={need}
                lessonHref={lessonHref}
                outcomes={outcomesByNeed.get(`${need.studentId}|${need.topicId}|${need.form}`) ?? []}
              />
            ))}
          </div>
        </section>
      )}

      <section className="mt-6">
        <h2 className="mb-3 font-display font-semibold text-white">Chủ đề cần ôn</h2>
        {gaps === null ? (
          <p className="text-sm text-slate-400">Đang tải…</p>
        ) : priorityGaps.length === 0 ? (
          <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-sm text-slate-500">
            Chưa có dữ liệu — hoặc em chưa sai câu nào. Giữ phong độ nhé!
          </p>
        ) : (
          <div className="space-y-3">
            {priorityGaps.map((gap) => (
              <GapRow key={gap.key} gap={gap} lessonHref={lessonHref} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default function KetQuaPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full">
        {!supabaseConfigured ? (
          <p className="pt-28 text-center text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : (
          <RequireAuth>
            <Dashboard />
          </RequireAuth>
        )}
      </main>
      <Footer />
    </>
  );
}
