"use client";

/**
 * Trình chiếu phân tích bài làm cho CẢ LỚP xem (sau khi nộp, trước/trong buổi chữa).
 * Khác ReviewPrep (bản cho thầy): chỉ số liệu gộp, không tên học sinh, không "cách chữa" của giáo viên; lời AI
 * dùng trường viết cho học sinh (classMessage/studentTip/studentWhy/studentAvoid), bản phân tích cũ thiếu thì
 * rơi về số liệu máy tính + misconception.
 *
 * Nhịp slide (N5 chia nhỏ, G1 ≤ 4 khối mỗi màn):
 *   1. Kết quả cả lớp — 2 con số + 1–2 câu nhận xét mở bằng điểm làm tốt (L4).
 *   2..k. Mỗi câu khó một slide "Bẫy ở Câu X": đề (font đề thi, E1/E4), % chọn từng phương án, phương án bẫy
 *         đánh dấu; Space mới hiện đáp án đúng; khối "Vì sao dễ nhầm" + "Mẹo tránh".
 *   cuối. "Ôn lại trước buổi sau" — tối đa 3 chủ đề, mỗi chủ đề 1 việc cụ thể (L4, N2).
 * Nền sáng mặc định (M1/M7: máy chiếu phòng sáng đọc chữ tối trên nền sáng rõ hơn), phím T đổi nền tối.
 * Không gì tự chuyển động (B4); đúng/sai luôn kèm chữ, không chỉ màu (M4).
 */
import { useEffect, useMemo, useRef, useState, useSyncExternalStore, type CSSProperties, type TouchEvent } from "react";
import { ChevronLeft, ChevronRight, Contrast, Eye, Maximize, X } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import type { ExamQuestion } from "@/features/exams/types";
import type { ExamReviewData } from "@/services/analytics";
import type { AiExamAnalysis } from "@/services/ai-exam-analysis";
import { computeReviewInsights, NO_TOPIC } from "@/lib/review-analysis";
import s from "./ReviewSlides.module.css";

const LETTERS = ["A", "B", "C", "D"];
const MAX_TRAP_SLIDES = 5;
const TRAP_BELOW = 60; // câu < 60% đúng mới lên slide bẫy
const ZOOM_MIN = 0.7;
const ZOOM_MAX = 1.6;

const noopSubscribe = () => () => {};
const esc = (t: string) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
function Txt({ text }: { text: string }) {
  return <ContentHtml html={esc(text)} />;
}

type Slide = { kind: "overview" } | { kind: "trap"; index: number } | { kind: "topics" };

export default function ReviewSlides({
  data,
  ai,
  onJump,
  onClose,
}: {
  data: ExamReviewData;
  ai: AiExamAnalysis | null;
  /** Mở câu đó trên bảng chữa bài (thoát trình chiếu). */
  onJump: (questionIndex: number) => void;
  onClose: () => void;
}) {
  const insights = useMemo(() => computeReviewInsights(data), [data]);
  const [pos, setPos] = useState(0);
  const [reveal, setReveal] = useState(false);
  const [dark, setDark] = useState(false);
  const [zoom, setZoom] = useState(1);
  const rootRef = useRef<HTMLDivElement>(null);

  const traps = useMemo(() => {
    const order = ai?.reviewOrder.length ? ai.reviewOrder : insights.reviewOrder;
    return order
      .filter((i) => {
        const p = insights.questions[i]?.pct;
        return p !== null && p !== undefined && p < TRAP_BELOW;
      })
      .slice(0, MAX_TRAP_SLIDES);
  }, [ai, insights]);

  const slides: Slide[] = useMemo(
    () => [{ kind: "overview" }, ...traps.map((index) => ({ kind: "trap" as const, index })), { kind: "topics" }],
    [traps],
  );
  const slide = slides[Math.min(pos, slides.length - 1)];

  const go = (n: number) => {
    setPos(Math.max(0, Math.min(slides.length - 1, n)));
    setReveal(false);
  };
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) rootRef.current?.requestFullscreen?.().catch(() => {});
    else document.exitFullscreen();
  };
  const zoomBy = (d: number) => setZoom((z) => Math.round(Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, z + d)) * 10) / 10);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      e.stopImmediatePropagation();
      if (e.key === "ArrowRight" || e.key === "PageDown") go(pos + 1);
      else if (e.key === "ArrowLeft" || e.key === "PageUp") go(pos - 1);
      else if (e.code === "Space") {
        e.preventDefault();
        if (slide.kind === "trap") setReveal((r) => !r);
        else go(pos + 1);
      } else if (e.key === "f" || e.key === "F") toggleFullscreen();
      else if (e.key === "t" || e.key === "T") setDark((d) => !d);
      else if (e.key === "+" || e.key === "=") zoomBy(0.1);
      else if (e.key === "-" || e.key === "_") zoomBy(-0.1);
      else if (e.key === "0") setZoom(1);
      else if (e.key === "Enter" && slide.kind === "trap") onJump(slide.index);
      else if (e.key === "Escape" && !document.fullscreenElement) onClose();
    }
    // capture: chặn phím của bảng chữa bài nằm dưới.
    window.addEventListener("keydown", onKey, true);
    return () => window.removeEventListener("keydown", onKey, true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pos, slide]);

  const touchX = useRef<number | null>(null);
  const onTouchStart = (e: TouchEvent) => {
    touchX.current = e.touches.length === 1 ? e.touches[0].clientX : null;
  };
  const onTouchEnd = (e: TouchEvent) => {
    const x0 = touchX.current;
    touchX.current = null;
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 70) go(pos + (dx < 0 ? 1 : -1));
  };

  // Đọc sau khi gắn (tránh lệch SSR/hydrate); iPhone Safari không có Fullscreen API → ẩn nút.
  const canFullscreen = useSyncExternalStore(
    noopSubscribe,
    () => !!document.documentElement.requestFullscreen,
    () => false,
  );

  return (
    <div
      ref={rootRef}
      className={`${s.root}${dark ? ` ${s.dark}` : ""}`}
      style={{ "--zoom": zoom } as CSSProperties}
      role="dialog"
      aria-modal="true"
      aria-label="Trình chiếu phân tích bài làm"
      onTouchStart={onTouchStart}
      onTouchEnd={onTouchEnd}
    >
      <header className={s.top}>
        <span className={s.title}>{data.examTitle}</span>
        <span className={s.count}>
          {pos + 1}/{slides.length}
        </span>
        <div className={s.tools}>
          <button type="button" onClick={() => setDark((d) => !d)} title="Đổi nền sáng/tối (T)" aria-label="Đổi nền">
            <Contrast size={18} />
          </button>
          {canFullscreen && (
            <button type="button" onClick={toggleFullscreen} title="Toàn màn hình (F)" aria-label="Toàn màn hình">
              <Maximize size={18} />
            </button>
          )}
          <button type="button" onClick={onClose} title="Thoát trình chiếu (Esc)" aria-label="Thoát trình chiếu">
            <X size={18} />
          </button>
        </div>
      </header>

      <main className={s.stage}>
        {slide.kind === "overview" && <OverviewSlide insights={insights} ai={ai} trapCount={traps.length} />}
        {slide.kind === "trap" && (
          <TrapSlide
            q={data.questions[slide.index]}
            index={slide.index}
            stat={data.stats[slide.index]}
            pct={insights.questions[slide.index]?.pct ?? null}
            commonWrong={insights.questions[slide.index]?.commonWrong ?? ""}
            note={ai?.questions.find((n) => n.index === slide.index) ?? null}
            reveal={reveal}
          />
        )}
        {slide.kind === "topics" && <TopicsSlide insights={insights} ai={ai} />}
      </main>

      <footer className={s.nav}>
        <button type="button" className={s.navBtn} onClick={() => go(pos - 1)} disabled={pos === 0} aria-label="Trang trước">
          <ChevronLeft size={24} />
        </button>
        {slide.kind === "trap" ? (
          <>
            <button type="button" className={`${s.navBtn} ${s.navMain}`} onClick={() => setReveal((r) => !r)}>
              <Eye size={20} /> {reveal ? "Ẩn đáp án" : "Hiện đáp án"}
            </button>
            <button type="button" className={s.navBtn} onClick={() => onJump(slide.index)} title="Mở câu này trên bảng chữa bài (Enter)">
              Chữa câu này
            </button>
          </>
        ) : (
          <span className={s.dots} aria-hidden>
            {slides.map((_, k) => (
              <i key={k} className={k === pos ? s.dotOn : undefined} />
            ))}
          </span>
        )}
        <button
          type="button"
          className={s.navBtn}
          onClick={() => go(pos + 1)}
          disabled={pos === slides.length - 1}
          aria-label="Trang sau"
        >
          <ChevronRight size={24} />
        </button>
      </footer>
    </div>
  );
}

// ---------- Slide 1: kết quả cả lớp ----------

function OverviewSlide({
  insights,
  ai,
  trapCount,
}: {
  insights: ReturnType<typeof computeReviewInsights>;
  ai: AiExamAnalysis | null;
  trapCount: number;
}) {
  const named = insights.topics.filter((t) => t.topic !== NO_TOPIC && t.pct !== null);
  const best = [...named].sort((a, b) => (b.pct ?? 0) - (a.pct ?? 0))[0];
  const worst = named[0];
  const machine =
    best && worst && best.topic !== worst.topic
      ? `Cả lớp làm chắc nhất phần "${best.topic}" (${best.pct}% đúng). Phần cần cùng xem lại: "${worst.topic}" (${worst.pct}%).`
      : "";
  const message = ai?.classMessage?.trim() || machine;
  return (
    <section className={s.slide}>
      <p className={s.eyebrow}>Kết quả cả lớp</p>
      <div className={s.kpis}>
        <div>
          <b>{insights.avgPct === null ? "—" : `${insights.avgPct}%`}</b>
          <span>câu làm đúng, trung bình</span>
        </div>
        <div>
          <b>{insights.attempts}</b>
          <span>bài đã nộp</span>
        </div>
        {trapCount > 0 && (
          <div>
            <b>{trapCount}</b>
            <span>câu có bẫy cần cùng xem</span>
          </div>
        )}
      </div>
      {message && (
        <div className={s.message}>
          <Txt text={message} />
        </div>
      )}
    </section>
  );
}

// ---------- Slide bẫy từng câu ----------

function TrapSlide({
  q,
  index,
  stat,
  pct,
  commonWrong,
  note,
  reveal,
}: {
  q: ExamQuestion;
  index: number;
  stat: ExamReviewData["stats"][number];
  pct: number | null;
  commonWrong: string;
  note: AiExamAnalysis["questions"][number] | null;
  reveal: boolean;
}) {
  const n = Math.max(1, stat.attempted);
  const why = note?.studentWhy?.trim() || note?.misconception?.trim() || "";
  const avoid = note?.studentAvoid?.trim() || "";

  // Phương án/ý bị chọn sai nhiều nhất = "bẫy".
  let trapOpt = -1;
  if (q.type === "multiple_choice" && stat.optionCounts) {
    stat.optionCounts.forEach((c, i) => {
      if (i !== q.answer && c > 0 && (trapOpt < 0 || c > stat.optionCounts![trapOpt])) trapOpt = i;
    });
  }
  let trapSt = -1;
  if (q.type === "true_false" && stat.statementCorrectN) {
    trapSt = 0;
    stat.statementCorrectN.forEach((c, i) => {
      if (c < stat.statementCorrectN![trapSt]) trapSt = i;
    });
  }

  return (
    <section className={`${s.slide} ${s.trap}`}>
      <p className={s.eyebrow}>
        Bẫy ở Câu {index + 1}
        {pct !== null && <span className={s.pctTag}>{pct}% cả lớp làm đúng</span>}
      </p>
      <div className={s.trapGrid}>
        <div className={`${s.question} exam-paper`}>
          <ContentHtml html={q.question} />
          {q.type === "multiple_choice" && (
            <ul className={s.opts}>
              {q.options.map((opt, i) => {
                const p = Math.round(((stat.optionCounts?.[i] ?? 0) / n) * 100);
                const right = reveal && i === q.answer;
                return (
                  <li key={i} className={`${right ? s.right : ""} ${i === trapOpt ? s.trapped : ""}`}>
                    <span className={s.letter}>{LETTERS[i]}.</span>
                    <span className={s.optBody}>
                      <ContentHtml html={opt} />
                    </span>
                    <span className={s.optPct}>
                      <span className={s.bar}>
                        <i style={{ width: `${p}%` }} />
                      </span>
                      {p}%
                    </span>
                    {right && <span className={s.flag}>✓ Đúng</span>}
                    {!right && i === trapOpt && <span className={`${s.flag} ${s.flagTrap}`}>Bẫy</span>}
                  </li>
                );
              })}
            </ul>
          )}
          {q.type === "true_false" && (
            <ul className={s.opts}>
              {q.statements.map((st, i) => {
                const p = Math.round(((stat.statementCorrectN?.[i] ?? 0) / n) * 100);
                return (
                  <li key={i} className={i === trapSt ? s.trapped : ""}>
                    <span className={s.letter}>{String.fromCharCode(97 + i)})</span>
                    <span className={s.optBody}>
                      <ContentHtml html={st.text} />
                    </span>
                    <span className={s.optPct}>{p}% chọn đúng</span>
                    {reveal ? (
                      <span className={`${s.flag} ${st.answer ? "" : s.flagFalse}`}>{st.answer ? "Đúng" : "Sai"}</span>
                    ) : (
                      i === trapSt && <span className={`${s.flag} ${s.flagTrap}`}>Bẫy</span>
                    )}
                  </li>
                );
              })}
            </ul>
          )}
          {q.type === "short_answer" && (
            <div className={s.saRow}>
              <span>Đáp số:</span> <b>{reveal ? q.answer : "?"}</b>
            </div>
          )}
        </div>

        <aside className={s.why}>
          {commonWrong && (
            <div className={s.whyStat}>
              <b>Nhiều bạn:</b> {commonWrong}
            </div>
          )}
          {why && (
            <div className={s.whyBlock}>
              <h3>Vì sao dễ nhầm</h3>
              <Txt text={why} />
            </div>
          )}
          {avoid && (
            <div className={s.whyBlock}>
              <h3>Mẹo tránh bẫy</h3>
              <Txt text={avoid} />
            </div>
          )}
          {!why && !avoid && <p className={s.muted}>Cả lớp thử nói: bẫy nằm ở đâu?</p>}
        </aside>
      </div>
    </section>
  );
}

// ---------- Slide cuối: ôn lại ----------

function TopicsSlide({ insights, ai }: { insights: ReturnType<typeof computeReviewInsights>; ai: AiExamAnalysis | null }) {
  const items: { topic: string; tip: string; qs: number[] }[] = ai?.topics.length
    ? ai.topics.slice(0, 3).map((t) => ({
        topic: t.topic,
        tip: t.studentTip?.trim() || t.reviewTip,
        qs: t.questionIndexes,
      }))
    : insights.topics
        .filter((t) => t.topic !== NO_TOPIC && t.level !== "thap")
        .slice(0, 3)
        .map((t) => ({
          topic: t.topic,
          tip: `Làm lại các câu ${t.questionIndexes.map((i) => i + 1).join(", ")} rồi đối chiếu lời giải.`,
          qs: t.questionIndexes,
        }));
  return (
    <section className={s.slide}>
      <p className={s.eyebrow}>Ôn lại trước buổi sau</p>
      {items.length === 0 ? (
        <p className={s.message}>Không có chủ đề nào dưới 70% — cả lớp giữ nhịp này nhé.</p>
      ) : (
        <ol className={s.topics}>
          {items.map((t, k) => (
            <li key={k}>
              <span className={s.num}>{k + 1}</span>
              <div>
                <h3>{t.topic}</h3>
                {t.tip && <Txt text={t.tip} />}
                {t.qs.length > 0 && (
                  <p className={s.qs}>Câu {t.qs.map((i) => i + 1).join(" · ")}</p>
                )}
              </div>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
