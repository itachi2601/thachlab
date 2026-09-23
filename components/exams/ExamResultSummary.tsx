"use client";

import { Eye } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";
import {
  gradeExam,
  statsByType,
  type ExamQuestion,
  type QuestionResponse,
} from "@/features/exams/types";
import ResultSticker, { resultTier } from "@/components/exams/ResultSticker";

const num = (v: number) => v.toLocaleString("vi-VN", { maximumFractionDigits: 2 });

/** Màu + lời động viên theo phần trăm điểm — giống bảng thống kê của app luyện đề. */
function tone(pct: number) {
  if (pct >= 90)
    return {
      stroke: "#10B981",
      text: "text-emerald-300",
      soft: "bg-emerald-500/10",
      message: "🏆 Xuất sắc! Em nắm rất chắc phần này.",
    };
  if (pct >= 70)
    return {
      stroke: "#06B6D4",
      text: "text-cyan-300",
      soft: "bg-cyan-500/10",
      message: "🔥 Khá tốt rồi — xem lại vài câu sai là chắc kiến thức.",
    };
  if (pct >= 50)
    return {
      stroke: "#F59E0B",
      text: "text-amber-300",
      soft: "bg-amber-500/10",
      message: "💪 Em đã qua nửa đường, ôn lại các câu sai nhé!",
    };
  return {
    stroke: "#F43F5E",
    text: "text-red-300",
    soft: "bg-red-500/10",
    message: "🌱 Em đang bắt đầu, luyện thêm sẽ tiến bộ rất nhanh!",
  };
}

function Ring({ pct, color }: { pct: number; color: string }) {
  const r = 52;
  const c = 2 * Math.PI * r;
  return (
    <svg viewBox="0 0 120 120" className="h-32 w-32 shrink-0" role="img" aria-label={`Đạt ${pct}%`}>
      <circle
        cx="60"
        cy="60"
        r={r}
        fill="none"
        stroke="currentColor"
        strokeOpacity="0.12"
        strokeWidth="12"
        className="text-slate-400"
      />
      <circle
        cx="60"
        cy="60"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="12"
        strokeLinecap="round"
        strokeDasharray={c}
        strokeDashoffset={c * (1 - Math.min(Math.max(pct, 0), 100) / 100)}
        transform="rotate(-90 60 60)"
      />
      <text
        x="60"
        y="60"
        textAnchor="middle"
        dominantBaseline="central"
        fontSize="24"
        fontWeight="700"
        fill={color}
      >
        {pct}%
      </text>
    </svg>
  );
}

export interface ResultBadge {
  label: string;
  tone: "pass" | "fail" | "pending";
}

const BADGE_CLS: Record<ResultBadge["tone"], string> = {
  pass: "bg-emerald-500/15 text-emerald-300 border-emerald-500/40",
  fail: "bg-red-500/15 text-red-300 border-red-500/40",
  pending: "bg-violet-500/15 text-violet-300 border-violet-500/40",
};

interface Props {
  questions: ExamQuestion[];
  responses: QuestionResponse[];
  /** Dòng phụ dưới lời động viên: tên học sinh, thời gian làm bài, hạng… */
  meta?: React.ReactNode;
  /** Neo của khối "Xem lại bài làm" — có thì hiện nút CTA. */
  detailAnchor?: string;
  /** Đạt/Chưa đạt/Chờ chấm — chỉ hiện khi giáo viên đã cấu hình ngưỡng cho đề này. */
  badge?: ResultBadge | null;
}

export default function ExamResultSummary({
  questions,
  responses,
  meta,
  detailAnchor,
  badge,
}: Props) {
  const summary = gradeExam(questions, responses);
  const pct = Math.round(summary.max > 0 ? (summary.earned / summary.max) * 100 : 0);
  const t = tone(pct);
  const stats = statsByType(questions, responses);
  const reduceMotion = useReducedMotion();

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 bg-panel p-5 sm:p-6">
        <div className="flex flex-wrap items-center gap-4">
          <motion.div
            initial={{ scale: reduceMotion ? 1 : 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: reduceMotion ? 0 : 0.4, ease: "backOut" }}
          >
            <ResultSticker tier={resultTier(pct)} />
          </motion.div>
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-3">
              <h2 className="font-display text-xl font-bold leading-snug text-white">{t.message}</h2>
              {badge && (
                <span className={`shrink-0 rounded-full border px-3 py-1 text-xs font-bold ${BADGE_CLS[badge.tone]}`}>
                  {badge.label}
                </span>
              )}
            </div>
            {meta && <p className="mt-1 text-sm text-slate-400">{meta}</p>}
          </div>
        </div>

        <div className="mt-5 flex flex-wrap items-center gap-6">
          <Ring pct={pct} color={t.stroke} />
          <dl className="min-w-[200px] flex-1 space-y-2 text-sm">
            <div className="flex items-center justify-between gap-3">
              <dt className="text-slate-400">Tổng điểm</dt>
              <dd className={`rounded-lg px-3 py-1 font-mono text-lg font-bold ${t.soft} ${t.text}`}>
                {num(summary.score10)}
                <span className="text-slate-400"> / 10</span>
              </dd>
            </div>
            <div className="flex items-center justify-between gap-3">
              <dt className="text-slate-400">Số câu đúng trọn vẹn</dt>
              <dd className="font-mono font-semibold text-white">
                {summary.correctCount}/{questions.length}
              </dd>
            </div>
            <div className="flex items-center justify-between gap-3">
              <dt className="text-slate-400">Điểm đã đạt</dt>
              <dd className="font-mono font-semibold text-white">
                {num(summary.earned)}/{num(summary.max)}
              </dd>
            </div>
          </dl>
        </div>

        {detailAnchor && (
          <a
            href={`#${detailAnchor}`}
            className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-sm font-semibold text-white hover:bg-primary-dark"
          >
            <Eye size={18} /> Xem bài làm chi tiết
          </a>
        )}
      </section>

      <section>
        <h3 className="mb-3 font-display font-semibold text-white">Bảng thống kê</h3>
        <div className="space-y-3">
          {stats.map((s) => (
            <div
              key={s.type}
              className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/10 bg-panel p-4"
            >
              <div className="min-w-[180px] flex-1">
                <p className="font-semibold text-white">
                  {s.label}{" "}
                  <span className="text-sm font-normal text-slate-400">({s.total} câu)</span>
                </p>
                <ul className="mt-1 space-y-0.5 text-sm text-slate-400">
                  <li>
                    Số câu đúng: <b className="text-emerald-300">{s.correct}/{s.total}</b>
                  </li>
                  {s.partial > 0 && (
                    <li>
                      Đúng một phần: <b className="text-amber-300">{s.partial}/{s.total}</b>
                    </li>
                  )}
                  <li>
                    Số câu sai: <b className="text-red-300">{s.wrong}/{s.total}</b>
                  </li>
                  <li>
                    Số câu bỏ qua: <b className="text-slate-300">{s.skipped}/{s.total}</b>
                  </li>
                </ul>
              </div>
              {s.max > 0 ? (
                <div className="rounded-xl bg-white/5 px-4 py-2 text-center">
                  <p className="text-xs text-slate-400">Điểm</p>
                  <p className="font-mono font-bold text-white">
                    {num(s.earned)}
                    <span className="text-slate-400"> / {num(s.max)}</span>
                  </p>
                </div>
              ) : (
                <p className="rounded-xl bg-violet-500/10 px-4 py-2 text-xs text-violet-300">
                  Thầy chấm tay
                </p>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
