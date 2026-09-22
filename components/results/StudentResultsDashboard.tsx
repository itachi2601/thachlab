"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AlertTriangle, ArrowRight, ChevronDown, Target, Trophy } from "lucide-react";
import Html from "@/components/exams/ContentHtml";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import {
  fetchMyAlert,
  fetchMyScoreHistory,
  fetchMyTopicGaps,
  fetchMyWrongQuestions,
  fetchOutcomeGaps,
  fetchPeriodicRank,
  fetchPeriodicRankOf,
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

/**
 * Bảng kết quả học tập của MỘT học sinh. Dùng ở hai chỗ:
 *  - /lop-hoc/ket-qua: chính em xem (viewer = "student", studentId = auth.uid())
 *  - /phu-huynh: phụ huynh xem thay con (viewer = "parent", studentId = id của con;
 *    RLS "parent reads child ..." trong supabase-migration-phu-huynh.sql cho đọc).
 * Cùng một dữ liệu, chỉ khác cách xưng hô và phụ huynh không có nút "Ôn lại bài".
 */
export type ResultsViewer = "student" | "parent";

const COPY: Record<ResultsViewer, {
  subtitle: string;
  noExam: string;
  noGap: string;
  needsIntro: string;
  needsTitle: string;
  missed: string;
  low: string;
}> = {
  student: {
    subtitle: "Điểm kiểm tra và những chủ đề em cần ôn lại.",
    noExam: "Em chưa làm bài kiểm tra nào.",
    noGap: "Chưa có dữ liệu — hoặc em chưa sai câu nào. Giữ phong độ nhé!",
    needsTitle: "Phần em cần phụ đạo",
    needsIntro: "Phần nào thầy và trợ giảng đã dạy lại, phần nào em đã làm đúng trở lại.",
    missed: "Em còn bài kiểm tra chưa làm — hãy hoàn thành sớm.",
    low: "Điểm kiểm tra của em đang thấp. Trợ giảng sẽ liên hệ để sắp lịch phụ đạo. Cố gắng ôn lại các chủ đề dưới đây nhé.",
  },
  parent: {
    subtitle: "Điểm kiểm tra của con và những chủ đề con cần ôn lại.",
    noExam: "Con chưa làm bài kiểm tra nào trên thachlab.",
    noGap: "Chưa có dữ liệu — hoặc con chưa sai câu nào.",
    needsTitle: "Phần con đang được phụ đạo",
    needsIntro: "Phần nào thầy và trợ giảng đã dạy lại, phần nào con đã làm đúng trở lại.",
    missed: "Con còn bài kiểm tra chưa làm — phụ huynh nhắc con hoàn thành sớm.",
    low: "Điểm kiểm tra của con đang thấp. Trợ giảng sẽ liên hệ để sắp lịch phụ đạo.",
  },
};

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

/** Trang chi tiết bài làm dùng ?ph=1 để nút "Về" trỏ lại /phu-huynh thay vì /lop-hoc/ket-qua. */
function detailHref(resultId: number, viewer: ResultsViewer, hash = "") {
  return `/lop-hoc/ket-qua/chi-tiet/?id=${resultId}${viewer === "parent" ? "&ph=1" : ""}${hash}`;
}

function GapRow({
  gap,
  lessonHref,
  studentId,
  viewer,
}: {
  gap: TopicGap;
  lessonHref: (topicName: string, form: string) => string | null;
  studentId: string;
  viewer: ResultsViewer;
}) {
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<
    Awaited<ReturnType<typeof fetchMyWrongQuestions>> | null
  >(null);
  const href = lessonHref(gap.topic, gap.form);

  useEffect(() => {
    if (!open || items) return;
    fetchMyWrongQuestions(studentId, gap.topic, gap.form)
      .then(setItems)
      .catch(() => setItems([]));
  }, [open, items, studentId, gap.topic, gap.form]);

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
                    href={detailHref(it.ref.examResultId, viewer, `#cau-${it.ref.questionIndex + 1}`)}
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

function AttemptRow({ point, viewer }: { point: ScorePoint; viewer: ResultsViewer }) {
  const dateLabel = new Date(point.at).toLocaleDateString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });

  return (
    <Link
      href={detailHref(point.resultId, viewer)}
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

function AlertBanner({ alert, copy }: { alert: StudentAlert; copy: (typeof COPY)[ResultsViewer] }) {
  return (
    <section className="rounded-2xl border border-amber-400/25 bg-gradient-to-r from-amber-500/10 to-transparent p-5">
      <div className="flex items-center gap-2 text-amber-300">
        <AlertTriangle size={18} />
        <h2 className="font-display font-bold text-white">Cần chú ý</h2>
      </div>
      <p className="mt-2 text-sm text-amber-100/80">
        {alert.kind === "missed_assessment" ? copy.missed : copy.low}
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
const NEED_NOTE: Record<ResultsViewer, Record<NeedStatus, string>> = {
  student: {
    open: "Thầy đã ghi nhận, sẽ sắp buổi phụ đạo cho em.",
    assigned: "Đã có trợ giảng nhận kèm em phần này.",
    tutored: "Em đã được dạy lại phần này — làm bài sau để chốt.",
    cleared: "Em đã làm đúng lại phần này. Giỏi!",
    dismissed: "Phần này tạm gác lại.",
  },
  parent: {
    open: "Thầy đã ghi nhận, sẽ sắp buổi phụ đạo cho con.",
    assigned: "Đã có trợ giảng nhận kèm con phần này.",
    tutored: "Con đã được dạy lại phần này — bài kiểm tra sau sẽ cho biết đã vững chưa.",
    cleared: "Con đã làm đúng lại phần này.",
    dismissed: "Phần này tạm gác lại.",
  },
};

function NeedRow({
  need,
  lessonHref,
  outcomes,
  viewer,
}: {
  need: TutoringNeed;
  lessonHref: (topicName: string, form: string) => string | null;
  outcomes: OutcomeGap[];
  viewer: ResultsViewer;
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
      <p className="mt-1 text-xs text-slate-400">{NEED_NOTE[viewer][need.status]}</p>
    </div>
  );
}

export default function StudentResultsDashboard({
  studentId,
  viewer = "student",
  title = "Kết quả học tập",
}: {
  studentId: string;
  viewer?: ResultsViewer;
  /** Tiêu đề — trang phụ huynh truyền tên con. */
  title?: string;
}) {
  const copy = COPY[viewer];
  const [points, setPoints] = useState<ScorePoint[] | null>(null);
  const [gaps, setGaps] = useState<TopicGap[] | null>(null);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [needs, setNeeds] = useState<TutoringNeed[] | null>(null);
  const [lessonByTopic, setLessonByTopic] = useState<Map<string, number | null>>(new Map());
  const [outcomeGaps, setOutcomeGaps] = useState<OutcomeGap[]>([]);
  const [periodicRank, setPeriodicRank] = useState<PeriodicRank | null>(null);

  useEffect(() => {
    const uid = studentId;
    fetchMyScoreHistory(uid).then(setPoints).catch(() => setPoints([]));
    fetchMyTopicGaps(uid).then(setGaps).catch(() => setGaps([]));
    fetchMyAlert(uid).then(setAlert).catch(() => setAlert(null));
    fetchMyNeeds(uid).then(setNeeds).catch(() => setNeeds([]));
    fetchOutcomeGaps(uid).then(setOutcomeGaps).catch(() => setOutcomeGaps([]));
    fetchQuestionTopics()
      .then((topics) => setLessonByTopic(new Map(topics.map((t) => [t.name, t.lessonId]))))
      .catch(() => undefined);
    fetchMyClassIds(uid)
      .then((classIds) =>
        classIds.length > 0
          ? viewer === "student"
            ? fetchPeriodicRank(classIds[0])
            : fetchPeriodicRankOf(uid, classIds[0])
          : null,
      )
      .then(setPeriodicRank)
      .catch(() => setPeriodicRank(null));
  }, [studentId, viewer]);

  const lessonHref = useMemo(
    () => (topicName: string, form: string) => {
      // Phụ huynh không ở trong lớp, không mở được bài học — bỏ nút "Ôn lại".
      if (viewer !== "student") return null;
      const lesson = lessonByTopic.get(topicName);
      if (!lesson) return null;
      const stage = form === "ly_thuyet" ? "ly_thuyet" : "bai_tap_mau";
      return `/lop-hoc/bai/?id=${lesson}#secondary-stage-${stage}`;
    },
    [lessonByTopic, viewer],
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
    <div className="mx-auto w-full max-w-4xl">
      <div className="flex flex-wrap items-center gap-3">
        <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/15 text-blue-300">
          <Target size={20} />
        </span>
        <div>
          <h1 className="font-display text-2xl font-bold text-white">{title}</h1>
          <p className="text-sm text-slate-400">{copy.subtitle}</p>
        </div>
        {periodicRank && (
          <div className="ml-auto">
            <RankSummary rank={periodicRank} />
          </div>
        )}
      </div>

      {alert && (
        <div className="mt-6">
          <AlertBanner alert={alert} copy={copy} />
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
          <p className="text-sm text-slate-500">{copy.noExam}</p>
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
            {copy.noExam}
          </p>
        ) : (
          <div className="space-y-3">
            {attempts.map((p) => (
              <AttemptRow key={p.resultId} point={p} viewer={viewer} />
            ))}
          </div>
        )}
      </section>

      {needs !== null && needs.length > 0 && (
        <section className="mt-6">
          <h2 className="mb-1 font-display font-semibold text-white">{copy.needsTitle}</h2>
          <p className="mb-3 text-sm text-slate-400">{copy.needsIntro}</p>
          <div className="space-y-2">
            {needs.map((need) => (
              <NeedRow
                key={need.id}
                need={need}
                lessonHref={lessonHref}
                outcomes={outcomesByNeed.get(`${need.studentId}|${need.topicId}|${need.form}`) ?? []}
                viewer={viewer}
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
            {copy.noGap}
          </p>
        ) : (
          <div className="space-y-3">
            {priorityGaps.map((gap) => (
              <GapRow key={gap.key} gap={gap} lessonHref={lessonHref} studentId={studentId} viewer={viewer} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
