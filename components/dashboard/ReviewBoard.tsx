"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Maximize, X } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import { QUESTION_FORM_LABELS, type ExamQuestion } from "@/features/exams/types";
import type { ExamReviewData, ReviewQuestionStat } from "@/services/analytics";

const LETTERS = ["A", "B", "C", "D"];
const TYPE_LABEL: Record<ExamQuestion["type"], string> = {
  multiple_choice: "Trắc nghiệm",
  true_false: "Đúng — Sai",
  short_answer: "Trả lời ngắn",
  essay: "Tự luận",
};

function pctOf(stat: ReviewQuestionStat) {
  return stat.attempted > 0 ? Math.round((stat.correctN / stat.attempted) * 100) : null;
}
function band(p: number | null) {
  if (p === null) return "mid";
  return p >= 75 ? "easy" : p >= 50 ? "mid" : "hard";
}

export default function ReviewBoard({ data }: { data: ExamReviewData }) {
  const router = useRouter();
  const [idx, setIdx] = useState(0);
  const [reveal, setReveal] = useState(0); // 0 none, 1 answer, 2 explanation
  const [onlyHard, setOnlyHard] = useState(false);

  const { questions, stats } = data;
  const q = questions[idx];
  const stat = stats[idx];

  const go = (i: number) => {
    setIdx(Math.max(0, Math.min(questions.length - 1, i)));
    setReveal(0);
  };
  const cycleReveal = () => setReveal((r) => Math.min(2, r + 1));

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "ArrowRight") go(idx + 1);
      else if (e.key === "ArrowLeft") go(idx - 1);
      else if (e.code === "Space") {
        e.preventDefault();
        cycleReveal();
      } else if (e.key === "r" || e.key === "R") setReveal(0);
      else if (e.key === "f" || e.key === "F") toggleFullscreen();
      else if (e.key === "Escape" && !document.fullscreenElement) router.back();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [idx]);

  function toggleFullscreen() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {});
    else document.exitFullscreen();
  }

  const chips = useMemo(
    () =>
      questions.map((_, i) => {
        const p = pctOf(stats[i]);
        return { i, p, b: band(p) };
      }),
    [questions, stats],
  );

  const p = pctOf(stat);
  const b = band(p);

  return (
    <div className={`review-board${reveal >= 1 ? " rb-revealed" : ""}`}>
      <div className="rb-topbar">
        <div>
          <span className="rb-eyebrow">Bảng chữa bài · ThachLab</span>
          <h1>{data.examTitle}</h1>
        </div>
        <div className="rb-spacer" />
        <div className="rb-progress">
          <span>
            Câu <b>{idx + 1}</b>/{questions.length}
          </span>
          <span className="rb-progress-track">
            <span
              className="rb-progress-fill"
              style={{ width: `${Math.round(((idx + 1) / questions.length) * 100)}%` }}
            />
          </span>
        </div>
        <button className="rb-btn" onClick={toggleFullscreen} title="Toàn màn hình (F)">
          <Maximize size={16} /> Toàn màn hình
        </button>
        <button className="rb-btn" onClick={() => router.back()} title="Thoát (Esc)">
          <X size={16} /> Thoát
        </button>
      </div>

      <div className="rb-stage-wrap">
        <div className="rb-stage">
          <div className="rb-qmeta">
            <span className="rb-qnum">Câu {idx + 1}</span>
            <span className="rb-tag">{TYPE_LABEL[q.type]}</span>
            {q.topic && <span className="rb-tag topic">{q.topic}</span>}
            {q.form && (q.form === "ly_thuyet" || q.form === "bai_tap") && (
              <span className="rb-tag">{QUESTION_FORM_LABELS[q.form]}</span>
            )}
            <span className={`rb-result rb-r-${b}${reveal >= 1 ? " show" : ""}`}>
              <i className="dot" />
              {p === null
                ? "Chưa có lượt làm"
                : `${p}% cả lớp làm đúng (${stat.correctN}/${stat.attempted})`}
            </span>
          </div>

          <div className="rb-qtext">
            <ContentHtml html={q.question} />
          </div>

          {q.type === "multiple_choice" && (
            <div className="rb-options">
              {q.options.map((opt, i) => {
                const n = stat.optionCounts?.[i] ?? 0;
                const optPct = stat.attempted > 0 ? Math.round((n / stat.attempted) * 100) : 0;
                const isCorrect = i === q.answer;
                return (
                  <div key={i} className={`rb-opt${isCorrect ? " correct" : ""}`}>
                    <span className="rb-letter">{LETTERS[i]}</span>
                    <span className="rb-body">
                      <ContentHtml html={opt} />
                      <span className="rb-stat">
                        <span>{n} em</span>
                        <span className="rb-bar">
                          <i style={{ width: `${optPct}%` }} />
                        </span>
                        <span>{optPct}%</span>
                      </span>
                    </span>
                    <span className="rb-badge">✓ đáp án đúng</span>
                  </div>
                );
              })}
            </div>
          )}

          {q.type === "true_false" && (
            <div className="rb-tf-list">
              {q.statements.map((s, i) => {
                const n = stat.statementCorrectN?.[i] ?? 0;
                const stPct = stat.attempted > 0 ? Math.round((n / stat.attempted) * 100) : 0;
                return (
                  <div key={i} className={`rb-tf-row ${s.answer ? "t" : "f"}`}>
                    <span className="rb-letter">{String.fromCharCode(97 + i)})</span>
                    <span className="rb-body">
                      <ContentHtml html={s.text} />
                    </span>
                    <span className="rb-pct">{stPct}% đúng</span>
                    <span className="rb-verdict">{s.answer ? "Đúng" : "Sai"}</span>
                  </div>
                );
              })}
            </div>
          )}

          {q.type === "short_answer" && (
            <div className="rb-sa-box">
              <span className="rb-label">Đáp số</span>
              <span className="rb-value">{reveal >= 1 ? q.answer : "?"}</span>
            </div>
          )}

          {q.type === "essay" && (
            <div className="rb-sa-box">
              <span className="rb-label">Đáp án gợi ý</span>
              {reveal >= 1 && <ContentHtml html={q.suggestedAnswer || "(chưa có)"} />}
            </div>
          )}

          {q.explanation && (
            <div className={`rb-explain${reveal >= 2 ? " open" : ""}`}>
              <div className="rb-inner">
                <div className="rb-lbl">💡 Lời giải</div>
                <ContentHtml html={q.explanation} />
              </div>
            </div>
          )}

          <div className="rb-hint">
            <span>
              <kbd>Space</kbd> hiện đáp án → lời giải
            </span>
            <span>
              <kbd>←</kbd> <kbd>→</kbd> chuyển câu
            </span>
            <span>
              <kbd>F</kbd> toàn màn hình
            </span>
            <span>
              <kbd>R</kbd> ẩn lại
            </span>
          </div>
        </div>
      </div>

      <div className="rb-navbar">
        <div className="rb-navtools">
          <label className="rb-filt">
            <input
              type="checkbox"
              checked={onlyHard}
              onChange={(e) => setOnlyHard(e.target.checked)}
            />
            Chỉ hiện câu &lt; 70% đúng
          </label>
          <span style={{ fontSize: ".78rem", color: "var(--rb-muted)" }}>
            {data.totalStudents} lượt nộp gần nhất trong lớp
          </span>
          <div className="rb-legend">
            <span>
              <i style={{ background: "var(--rb-ok)" }} />
              Dễ ≥75%
            </span>
            <span>
              <i style={{ background: "var(--rb-warn)" }} />
              Trung bình
            </span>
            <span>
              <i style={{ background: "var(--rb-bad)" }} />
              Khó &lt;50%
            </span>
          </div>
        </div>
        <div className="rb-strip">
          {chips.map((c) => (
            <button
              key={c.i}
              className={`rb-chip${c.i === idx ? " active" : ""}${
                onlyHard && (c.p ?? 100) >= 70 ? " hidden" : ""
              }`}
              style={
                c.i === idx
                  ? undefined
                  : {
                      borderColor: `var(--rb-${c.b === "easy" ? "ok" : c.b === "mid" ? "warn" : "bad"}-line)`,
                    }
              }
              title={`Câu ${c.i + 1}${c.p !== null ? ` · ${c.p}% đúng` : ""}`}
              onClick={() => go(c.i)}
            >
              <b>{c.i + 1}</b>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
