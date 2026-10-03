"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AlertTriangle, ArrowRight, BookOpen, ChevronDown, RotateCcw, Sparkles, Target, Trophy } from "lucide-react";
import Html from "@/components/exams/ContentHtml";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import {
  fetchClassAssessments,
  fetchMyAlert,
  fetchMyScoreHistory,
  fetchMyTopicGaps,
  fetchMyWrongQuestions,
  fetchOutcomeGaps,
  fetchQuestionTopics,
  outcomeGapsByNeed,
  type ClassAssessment,
  type OutcomeGap,
  type ScorePoint,
  type StudentAlert,
  type TopicGap,
} from "@/services/analytics";
import {
  NEED_STATUS_LABEL_STUDENT,
  fetchMyNeeds,
  needLabel,
  type NeedStatus,
  type TutoringNeed,
} from "@/services/tutoring";
import { fetchMyClassIds } from "@/services/classes";
import RankCard from "@/components/rank/RankCard";
import type { RankStatus } from "@/features/rank/types";
import { fetchMyRankStatus, fetchRankStatusOf } from "@/services/rank";
import { CONTACT } from "@/lib/contact";

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
  violation: string;
}> = {
  student: {
    subtitle: "Điểm kiểm tra và những chủ đề em cần ôn lại.",
    noExam: "Em chưa làm bài kiểm tra nào.",
    noGap: "Chưa có dữ liệu — hoặc em chưa sai câu nào. Giữ phong độ nhé!",
    needsTitle: "Phần em đang mở khoá",
    needsIntro: "Phần nào thầy và trợ giảng đã dạy lại, phần nào em đã làm đúng trở lại.",
    missed: "Em còn một bài kiểm tra chưa làm — làm ngay khi có thời gian nhé.",
    low: "Trợ giảng sẽ liên hệ để sắp lịch phụ đạo. Trong lúc chờ, ôn lại chủ đề đầu tiên bên dưới rồi thử làm lại câu sai nhé.",
    violation: "Bài kiểm tra gần đây của em bị ghi nhận nhiều lần rời màn hình/thoát toàn màn hình. Trợ giảng sẽ kiểm tra lại kiến thức thực tế của em.",
  },
  parent: {
    subtitle: "Điểm các bài con đã làm trên web, phần con còn sai và phần thầy đang phụ đạo.",
    noExam:
      "Con chưa làm bài nào trên web. Khi con làm bài đầu tiên, điểm sẽ hiện ở đây — anh chị không phải làm gì thêm.",
    noGap: "Chưa thấy phần nào con sai nhiều. Nếu con mới vào lớp, cần vài bài mới có dữ liệu.",
    // P8: phụ huynh không biết chữ "mở khoá" của hệ thống — nói thẳng là phụ đạo.
    needsTitle: "Phần con đang được phụ đạo",
    needsIntro: "Phần nào thầy và trợ giảng đã dạy lại, phần nào con đã làm đúng trở lại.",
    missed: "Con còn bài kiểm tra chưa làm. Anh chị nhắc con vào làm cho kịp.",
    // P8/P18: không phán xét ("đang thấp", "yếu") — nói theo NGƯỠNG đạt (6,5) + việc làm tiếp.
    low: "Điểm bài kiểm tra gần đây của con dưới mức đạt (6,5). Thầy sẽ sắp lịch phụ đạo cho con — anh chị nhắc con ôn lại các phần ở dưới.",
    violation:
      "Bài kiểm tra gần đây của con bị ghi nhận nhiều lần rời màn hình. Thầy sẽ kiểm tra lại kiến thức thực tế của con — anh chị hỏi thăm con xem có việc gì không.",
  },
};

const PASS = 6.5;

function ScoreTrend({ points }: { points: ScorePoint[] }) {
  if (points.length === 0) return null;
  const W = 640;
  const H = 260;
  const padL = 44;
  const padB = 20;
  const padT = 22;
  const innerW = W - padL - 12;
  const innerH = H - padT - padB;
  const x = (i: number) =>
    padL + (points.length === 1 ? innerW / 2 : (i / (points.length - 1)) * innerW);
  const y = (score: number) => padT + innerH - (score / 10) * innerH;
  const passY = y(PASS);
  const line = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(i)},${y(p.score)}`).join(" ");

  return (
    <div>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full"
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
            <text x={padL - 8} y={y(g) + 8} textAnchor="end" fontSize="24" fill="currentColor" fillOpacity="0.5">
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
        <text x={W - 12} y={passY - 8} textAnchor="end" fontSize="24" fill="#f59e0b">
          đạt 6,5
        </text>
        <path d={line} fill="none" stroke="#60A5FA" strokeWidth="2" />
        {points.map((p, i) => (
          <g key={p.resultId}>
            <circle
              cx={x(i)}
              cy={y(p.score)}
              r="7"
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

const UNTAGGED_TOPIC = "Chưa gắn chủ đề";
const MAX_GAPS_SHOWN = 5;

function formLabel(form: string) {
  return form === "ly_thuyet" || form === "bai_tap"
    ? QUESTION_FORM_LABELS[form]
    : form === "" ? "Nhiều loại" : "Chưa phân loại";
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
          <span className="mt-0.5 block text-[13px] text-slate-400">
            {formLabel(gap.form)} · sai {gap.wrong}/{gap.total} câu
          </span>
        </span>
        {/* P8/P19: một mình "60%" không nói là 60% cái gì — phụ huynh phải đọc được nghĩa con số. */}
        <span className="shrink-0 text-right">
          <span
            className={`block font-mono text-lg font-bold ${
              gap.pct >= 60 ? "text-red-300" : gap.pct >= 30 ? "text-amber-300" : "text-slate-300"
            }`}
          >
            {gap.pct}%
          </span>
          {viewer === "parent" && <span className="block text-[13px] text-slate-400">tỉ lệ sai</span>}
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
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
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
                    className="flex items-start gap-3 rounded-xl bg-white/5 px-4 py-3 hover:bg-white/10"
                  >
                    <span className="min-w-0 flex-1">
                      <span className="block text-[13px] font-bold text-slate-400">
                        {it.ref.examTitle} · Câu {it.ref.questionIndex + 1}
                      </span>
                      <span className="mt-1 line-clamp-2 block text-sm text-slate-200">
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

function AttemptRow({
  point,
  viewer,
  prev,
}: {
  point: ScorePoint;
  viewer: ResultsViewer;
  /** Bài liền trước (cũ hơn) — chỉ dùng để hiện chênh lệch cho phụ huynh. */
  prev?: ScorePoint;
}) {
  const dateLabel = new Date(point.at).toLocaleDateString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
  const delta = prev ? Math.round((point.score - prev.score) * 100) / 100 : null;

  return (
    <Link
      href={detailHref(point.resultId, viewer)}
      className="flex items-center gap-4 rounded-2xl border border-white/10 p-4 hover:border-white/25"
    >
      <span className="min-w-0 flex-1">
        <span className="block font-display font-semibold text-white">{point.examTitle}</span>
        <span className="mt-0.5 block text-[13px] text-slate-400">
          {viewer === "parent" ? longDate(point.at) : dateLabel}
          {point.periodic ? ` · ${point.kindLabel}` : ""}
        </span>
        {viewer === "parent" && delta !== null && (
          <span className={`mt-1 block text-[13px] font-semibold ${deltaShort(delta).cls}`}>
            {deltaShort(delta).text}
          </span>
        )}
      </span>
      <span
        className={`shrink-0 font-mono text-lg font-bold ${
          point.score >= PASS ? "text-emerald-300" : "text-red-300"
        }`}
      >
        {point.score.toLocaleString("vi-VN")}
        <span className="block text-right font-sans text-[13px] font-semibold">
          {point.score >= PASS ? "Đạt" : "Chưa đạt"}
        </span>
      </span>
      <ArrowRight size={18} className="shrink-0 text-slate-500" />
    </Link>
  );
}

function AlertBanner({
  alert,
  copy,
  hideMissed,
}: {
  alert: StudentAlert;
  copy: (typeof COPY)[ResultsViewer];
  hideMissed?: boolean;
}) {
  if (hideMissed && alert.kind === "missed_assessment") return null;
  return (
    <section className="rounded-2xl border border-amber-400/25 bg-amber-500/[.07] p-5">
      <div className="flex items-center gap-2 text-amber-300">
        <AlertTriangle size={18} />
        <h2 className="font-display font-bold text-white">Cần chú ý</h2>
      </div>
      <p className="mt-2 text-sm text-amber-100/80">
        {alert.kind === "missed_assessment"
          ? copy.missed
          : alert.kind === "exam_violation"
            ? copy.violation
            : copy.low}
      </p>
      {alert.handledNote && (
        <p className="mt-1 text-[13px] text-slate-400">Ghi chú: {alert.handledNote}</p>
      )}
    </section>
  );
}

const NEED_TONE: Record<NeedStatus, string> = {
  open: "border-sky-500/30 bg-sky-500/[.06] text-sky-200",
  assigned: "border-indigo-500/30 bg-indigo-500/[.06] text-indigo-200",
  tutored: "border-blue-500/30 bg-blue-500/[.06] text-blue-200",
  cleared: "border-emerald-500/30 bg-emerald-500/[.06] text-emerald-200",
  dismissed: "border-white/10 bg-white/[.03] text-slate-400",
};

/** Cách nói với chính học sinh — không dùng chữ "cảnh báo" cho em. */
const NEED_NOTE: Record<ResultsViewer, Record<NeedStatus, string>> = {
  student: {
    open: "Phần này đang chờ em mở khoá — ôn lại rồi tự kiểm tra, hoặc thầy sẽ sắp buổi kèm.",
    assigned: "Đã có trợ giảng nhận kèm em phần này.",
    tutored: "Em đã được dạy lại phần này — làm bài sau để chốt.",
    cleared: "Em đã phục hồi phần này. Giỏi!",
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
        <span className="rounded-full border border-current px-2.5 py-0.5 text-[13px] font-bold">
          {NEED_STATUS_LABEL_STUDENT[need.status]}
        </span>
        {href && (
          <Link
            href={href}
            className="ml-auto inline-flex min-h-11 items-center text-sm font-semibold text-blue-300 underline-offset-2 hover:underline"
          >
            Ôn lại bài
          </Link>
        )}
      </div>
      {outcomes.length > 0 && (
        <ul className="mt-2 space-y-0.5 text-[13px] text-slate-300">
          {outcomes.map((o) => (
            <li key={o.topicId}>
              · {o.topicName} — sai {o.wrong}/{o.total} câu
            </li>
          ))}
        </ul>
      )}
      <p className="mt-1 text-[13px] text-slate-400">{NEED_NOTE[viewer][need.status]}</p>
    </div>
  );
}

/* ============================================================
   Khối riêng cho PHỤ HUYNH (45–60 tuổi) — docs/QUY-TAC-THIET-KE-PHU-HUYNH.md
   Không đụng nhánh học sinh: mọi thứ dưới đây chỉ render khi viewer === "parent".
   ============================================================ */

/** P11: ngày kèm thứ — "Thứ Ba, 30/09/2026" định vị được, "30/09/2026" thì phải tính. */
function longDate(iso: string) {
  const d = new Date(iso);
  const weekday = ["Chủ nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"][d.getDay()];
  return `${weekday}, ${d.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" })}`;
}

function scoreText(score: number) {
  return score.toLocaleString("vi-VN", { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}

/** P12: chênh lệch điểm phải có cả màu LẪN chữ (mù màu đỏ–lục ~8% nam giới). */
function deltaText(delta: number) {
  if (delta === 0) return { cls: "text-slate-400", text: "không đổi so với bài trước" };
  return delta > 0
    ? { cls: "text-emerald-300", text: `tăng ${scoreText(Math.abs(delta))} điểm so với bài trước` }
    : { cls: "text-red-300", text: `giảm ${scoreText(Math.abs(delta))} điểm so với bài trước` };
}

/** Bản ngắn của deltaText, dùng trong danh sách bài đã làm (một dòng). */
function deltaShort(delta: number) {
  if (delta === 0) return { cls: "text-slate-400", text: "= không đổi so với bài trước" };
  return delta > 0
    ? { cls: "text-emerald-300", text: `↑ tăng ${scoreText(delta)} so với bài trước` }
    : { cls: "text-red-300", text: `↓ giảm ${scoreText(Math.abs(delta))} so với bài trước` };
}

/** Một mục "nhãn → số to → câu giải thích", xếp dọc trong một cột đọc (P6, P17: bảng hai cột
 *  nhãn–số bắt mắt lia trái–phải; số to, chữ số tabular nên các hàng vẫn thẳng cột nhau). */
function Fact({ label, value, sub }: { label: string; value: React.ReactNode; sub?: React.ReactNode }) {
  return (
    <div className="border-b border-white/10 py-3 first:pt-0 last:border-b-0 last:pb-0">
      <p className="text-slate-400">{label}</p>
      <p className="parent-num mt-0.5 font-display text-2xl font-bold text-white">{value}</p>
      {sub && <p className="parent-copy mt-0.5 text-slate-400">{sub}</p>}
    </div>
  );
}

/**
 * Tóm tắt cho phụ huynh: trả lời "con học thế nào" trong một màn hình, bằng số to + câu chữ,
 * từ dữ liệu dashboard đã tải (không gọi thêm Supabase lần nào).
 * Cố ý KHÔNG vẽ biểu đồ ở đây: biểu đồ đường với nhãn trục nhỏ khó đọc với tuổi 45–60 và lặp lại
 * đúng dữ liệu của danh sách bài bên dưới (P6, P17, N4).
 */
function ParentSummaryPanel({
  points,
  gaps,
  needs,
  avg,
}: {
  points: ScorePoint[];
  gaps: TopicGap[];
  needs: TutoringNeed[] | null;
  avg: number | null;
}) {
  const latest = points[points.length - 1];
  const prev = points.length > 1 ? points[points.length - 2] : null;
  const delta = prev ? Math.round((latest.score - prev.score) * 100) / 100 : null;
  // "Sai nhiều nhất" xếp theo SỐ CÂU SAI, không theo % — một chủ đề chỉ có 1 câu mà sai cũng ra
  // 100%, đứng đầu bảng sẽ doạ phụ huynh bằng con số vô nghĩa. Ưu tiên chủ đề có ≥3 câu.
  const ranked = [...gaps].filter((g) => g.wrong > 0).sort((a, b) => b.wrong - a.wrong || b.pct - a.pct || b.total - a.total);
  const worst = ranked.find((g) => g.total >= 3) ?? ranked[0];
  const openNeed = (needs ?? []).find((n) => n.status === "open" || n.status === "assigned");
  const lastThree = points.slice(-3).map((p) => scoreText(p.score)).join(" → ");

  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-panel p-5">
      <h2 className="font-display text-lg font-bold text-white">Tóm tắt cho anh chị</h2>
      <p className="mt-1 text-slate-400">Số liệu lấy từ các bài con làm trên web.</p>

      <div className="mt-3">
        <Fact
          label="Bài gần nhất"
          value={`${scoreText(latest.score)}/10`}
          sub={
            <>
              {longDate(latest.at)} · {latest.examTitle}
              {latest.periodic ? ` (${latest.kindLabel})` : ""}
            </>
          }
        />
        <Fact
          label="Điểm trung bình"
          value={avg === null ? "—" : scoreText(avg)}
          sub={`${points.length} bài đã làm`}
        />
        <Fact
          label={prev ? "So với bài trước" : "Ghi chú"}
          value={delta === null ? "Bài đầu tiên" : `${delta > 0 ? "+" : ""}${scoreText(delta)}`}
          sub={delta === null ? "Chưa có bài nào trước đó để so sánh." : <span className={deltaText(delta).cls}>{deltaText(delta).text}</span>}
        />
      </div>

      {points.length >= 3 && (
        <p className="mt-3 text-slate-400">
          Ba bài gần nhất: <b className="parent-num text-white">{lastThree}</b>
        </p>
      )}

      {worst && (
        <p className="parent-copy mt-3 text-slate-300">
          Còn sai nhiều nhất: <b className="text-white">{worst.topic}</b> — sai {worst.wrong}/{worst.total} câu (
          {worst.pct}%).
        </p>
      )}

      <p className="parent-copy mt-2 text-slate-300">
        {openNeed
          ? `Thầy đã ghi nhận và đang sắp phụ đạo phần ${needLabel(openNeed)}.`
          : "Hiện chưa có phần nào con cần phụ đạo thêm."}
      </p>
      <p className="parent-copy mt-2 text-slate-300">
        Việc anh chị làm được hôm nay: nhắc con làm bài tập thầy giao và ôn lại phần con còn sai.
        {worst && CONTACT.zalo && (
          <>
            {" "}
            <a
              href={CONTACT.zalo}
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold text-cyan-300 underline-offset-2 hover:underline"
            >
              Nhờ thầy kèm thêm phần này
            </a>
            .
          </>
        )}
      </p>
    </section>
  );
}

export default function StudentResultsDashboard({
  studentId,
  viewer = "student",
  title = "Kết quả học tập",
  afterSummary,
}: {
  studentId: string;
  viewer?: ResultsViewer;
  /** Tiêu đề — trang phụ huynh truyền tên con. */
  title?: string;
  /**
   * Chỉ dùng ở /phu-huynh: khối chèn ngay sau "Tóm tắt cho anh chị" (bài tập về nhà, bù bài) —
   * đó là việc phụ huynh phải làm tiếp, không nên nằm dưới cùng trang.
   */
  afterSummary?: React.ReactNode;
}) {
  const copy = COPY[viewer];
  const [points, setPoints] = useState<ScorePoint[] | null>(null);
  const [gaps, setGaps] = useState<TopicGap[] | null>(null);
  const [alert, setAlert] = useState<StudentAlert | null>(null);
  const [needs, setNeeds] = useState<TutoringNeed[] | null>(null);
  const [lessonByTopic, setLessonByTopic] = useState<Map<string, number | null>>(new Map());
  const [outcomeGaps, setOutcomeGaps] = useState<OutcomeGap[]>([]);
  const [rankStatus, setRankStatus] = useState<RankStatus | null | undefined>(undefined);
  const [assessments, setAssessments] = useState<ClassAssessment[] | null>(null);

  useEffect(() => {
    const uid = studentId;
    if (viewer === "student") {
      fetchMyClassIds(uid)
        .then((ids) => Promise.all(ids.map((id) => fetchClassAssessments(id))))
        .then((lists) => setAssessments(lists.flat()))
        .catch(() => setAssessments([]));
    }
    fetchMyScoreHistory(uid).then(setPoints).catch(() => setPoints([]));
    fetchMyTopicGaps(uid).then(setGaps).catch(() => setGaps([]));
    fetchMyAlert(uid).then(setAlert).catch(() => setAlert(null));
    fetchMyNeeds(uid).then(setNeeds).catch(() => setNeeds([]));
    fetchOutcomeGaps(uid).then(setOutcomeGaps).catch(() => setOutcomeGaps([]));
    fetchQuestionTopics()
      .then((topics) => setLessonByTopic(new Map(topics.map((t) => [t.name, t.lessonId]))))
      .catch(() => undefined);
    (viewer === "student" ? fetchMyRankStatus() : fetchRankStatusOf(uid))
      .then(setRankStatus)
      .catch(() => setRankStatus(null));
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

  // Các dòng "Chưa gắn chủ đề" (mỗi loại một dòng) gộp thành một; danh sách chỉ hiện 5 chủ đề đầu (N3).
  const priorityGaps = useMemo(() => {
    const wrongOnly = (gaps ?? []).filter((g) => g.wrong > 0);
    const untagged = wrongOnly.filter((g) => g.topic === UNTAGGED_TOPIC);
    if (untagged.length === 0) return wrongOnly;
    const total = untagged.reduce((a, g) => a + g.total, 0);
    const wrong = untagged.reduce((a, g) => a + g.wrong, 0);
    const merged: TopicGap = {
      key: `${UNTAGGED_TOPIC}|`, topicId: null, topic: UNTAGGED_TOPIC, form: "", total, wrong,
      pct: total ? Math.round((wrong / total) * 100) : 0,
    };
    return [...wrongOnly.filter((g) => g.topic !== UNTAGGED_TOPIC), merged]
      .sort((a, b) => b.wrong - a.wrong || b.pct - a.pct);
  }, [gaps]);
  const shownGaps = priorityGaps.slice(0, MAX_GAPS_SHOWN);
  const loading = points === null || gaps === null;
  const isEmpty = !loading && points.length === 0 && priorityGaps.length === 0;
  const attempts = useMemo(() => (points ? [...points].reverse() : null), [points]);

  // Bài được giao mà chưa làm → bấm vào làm ngay; hết bài thì gợi ý việc tiếp theo (chỉ học sinh).
  const todoExams = useMemo(() => {
    if (viewer !== "student" || !assessments || !points) return [];
    const done = new Set(points.map((p) => p.examId));
    const seen = new Set<number>();
    return assessments.filter((a) => {
      if (done.has(a.examId) || seen.has(a.examId)) return false;
      seen.add(a.examId);
      return true;
    }).slice(0, 5);
  }, [viewer, assessments, points]);
  const retryExam = useMemo(() => {
    if (!points) return null;
    const best = new Map<number, ScorePoint>();
    for (const p of points) {
      const cur = best.get(p.examId);
      if (!cur || p.score > cur.score) best.set(p.examId, p);
    }
    return [...best.values()].filter((p) => p.score < PASS).sort((a, b) => a.score - b.score)[0] ?? null;
  }, [points]);
  const firstReviewGap = priorityGaps.find((g) => lessonHref(g.topic, g.form));
  const studentReady = viewer === "student" && assessments !== null && points !== null;
  const showSuggestions = studentReady && todoExams.length === 0;

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
      </div>

      {alert && (viewer !== "student" || alert.kind !== "missed_assessment" || todoExams.length === 0) && (
        <div className="mt-6">
          <AlertBanner alert={alert} copy={copy} hideMissed={viewer === "student"} />
        </div>
      )}

      {studentReady && todoExams.length > 0 && (
        <section className="mt-6 rounded-2xl border border-amber-400/25 bg-amber-500/[.07] p-4 sm:p-5">
          <div className="flex items-center gap-2 text-amber-300">
            <AlertTriangle size={18} />
            <h2 className="font-display font-bold text-white">Cần chú ý</h2>
          </div>
          <p className="mt-2 text-sm text-amber-100/80">
            Em còn <strong className="text-white">{todoExams.length} bài chưa làm</strong> — bấm vào để làm ngay:
          </p>
          <div className="mt-3 space-y-2">
            {todoExams.map((item) => (
              <Link
                key={item.id}
                href={`/kiem-tra/lam?id=${item.examId}`}
                className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-amber-400/20 bg-black/15 p-3 hover:bg-black/25"
              >
                <span className="flex min-w-0 items-center gap-2">
                  <Trophy size={16} className="shrink-0 text-amber-300" />
                  <span className="min-w-0">
                    <strong className="block truncate text-sm text-white">{item.examTitle}</strong>
                    <small className="text-[13px] text-slate-400">Bài kiểm tra · chưa làm</small>
                  </span>
                </span>
                <span className="flex shrink-0 items-center gap-1 text-sm font-bold text-amber-200">
                  Làm bài <ArrowRight size={16} />
                </span>
              </Link>
            ))}
          </div>
        </section>
      )}

      {showSuggestions && (
        <section className="mt-6 rounded-2xl border border-emerald-400/25 bg-emerald-500/[.07] p-4 sm:p-5">
          <div className="flex items-center gap-2 text-emerald-300">
            <Sparkles size={18} />
            <h2 className="font-display font-bold text-white">Em đã làm xong bài được giao — việc nên làm tiếp</h2>
          </div>
          <div className="mt-3 space-y-2">
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
                <ArrowRight size={16} className="shrink-0 text-emerald-300" />
              </Link>
            )}
            {firstReviewGap && (
              <Link
                href={lessonHref(firstReviewGap.topic, firstReviewGap.form) as string}
                className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-emerald-400/20 bg-black/15 p-3 hover:bg-black/25"
              >
                <span className="flex min-w-0 items-center gap-2">
                  <BookOpen size={16} className="shrink-0 text-blue-300" />
                  <span className="min-w-0">
                    <strong className="block truncate text-sm text-white">Ôn lại: {firstReviewGap.topic}</strong>
                    <small className="text-[13px] text-slate-400">Chủ đề em còn sai nhiều nhất</small>
                  </span>
                </span>
                <ArrowRight size={16} className="shrink-0 text-emerald-300" />
              </Link>
            )}
            <Link
              href="/tai-khoan"
              className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-emerald-400/20 bg-black/15 p-3 hover:bg-black/25"
            >
              <span className="min-w-0">
                <strong className="block truncate text-sm text-white">Học tiếp bài đang dở</strong>
                <small className="text-[13px] text-slate-400">Về trang cá nhân để vào bài tiếp theo</small>
              </span>
              <ArrowRight size={16} className="shrink-0 text-emerald-300" />
            </Link>
          </div>
        </section>
      )}

      {/* P7: với phụ huynh, "con học thế nào" phải xong trong một màn hình — tóm tắt đứng ngay
          sau cảnh báo, trước mọi danh sách chi tiết. */}
      {viewer === "parent" && points !== null && points.length > 0 && (
        <ParentSummaryPanel points={points} gaps={priorityGaps} needs={needs} avg={avg} />
      )}

      {viewer === "parent" && afterSummary && <div className="mt-6">{afterSummary}</div>}

      {!loading && isEmpty && (
        <p className="mt-6 text-sm text-slate-400">{copy.noExam}</p>
      )}

      {priorityGaps.length > 0 && (
        <section className="mt-6">
          <h2 className="mb-3 font-display font-semibold text-white">
            {viewer === "parent" ? "Phần con còn sai" : "Chủ đề cần ôn"}
          </h2>
          <div className="space-y-3">
            {shownGaps.map((gap) => (
              <GapRow key={gap.key} gap={gap} lessonHref={lessonHref} studentId={studentId} viewer={viewer} />
            ))}
          </div>
        </section>
      )}

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

      {attempts !== null && attempts.length > 0 && (
        <section className="mt-6">
          <h2 className="mb-3 font-display font-semibold text-white">
            {viewer === "parent" ? "Các bài con đã làm" : "Bài đã làm"}
          </h2>
          <div className="space-y-3">
            {attempts.map((p, i) => (
              // attempts mới nhất trước → bài liền trước (cũ hơn) là phần tử kế tiếp.
              <AttemptRow key={p.resultId} point={p} viewer={viewer} prev={attempts[i + 1]} />
            ))}
          </div>
        </section>
      )}

      {/* P6/P17/N4: phụ huynh 45–60 tuổi nhận số to + câu chữ nhanh hơn biểu đồ đường có nhãn trục
          nhỏ, và biểu đồ lặp đúng dữ liệu của danh sách trên → chỉ học sinh xem biểu đồ. */}
      {viewer === "student" && points !== null && points.length > 0 && (
        <section className="mt-6 rounded-2xl border border-white/10 bg-panel p-5">
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="font-display font-semibold text-white">Điểm theo thời gian</h2>
            {avg !== null && (
              <span className="text-sm text-slate-400">
                trung bình <b className="text-white">{avg.toLocaleString("vi-VN")}</b>
              </span>
            )}
          </div>
          <div className="text-slate-300">
            <ScoreTrend points={points} />
          </div>
        </section>
      )}

      {/* L3: phần thưởng ngoài (hạng) chỉ ở cuối, sau việc cần làm. */}
      {viewer === "parent" && (
        <h2 className="mt-8 font-display font-semibold text-white">Thành tích trong lớp</h2>
      )}
      {viewer === "parent" && (
        // P19: RP/danh hiệu là hệ thống điểm thưởng của web, không phải điểm học tập — nói rõ,
        // nếu không phụ huynh sẽ đọc "CAO THỦ · 2.180 RP" như một nhận xét học lực.
        <p className="parent-copy mt-1 text-slate-400">
          Điểm thưởng và danh hiệu con nhận khi làm bài trên web. Đây không phải điểm học tập — điểm
          học tập nằm ở phần trên.
        </p>
      )}
      <div className={viewer === "parent" ? "mt-3" : "mt-8"}>
        <RankCard status={rankStatus} href={viewer === "student" ? "/lop-hoc/xep-hang/" : null} />
      </div>
    </div>
  );
}
