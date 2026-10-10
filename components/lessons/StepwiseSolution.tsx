"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import type { LessonWorkedQuestion, WorkedChoice, WorkedFading, WorkedStep } from "@/features/lessons/types";

/**
 * Lời giải "tự giải từng bước" của một dạng bài tập mẫu (skill soan-bai-tap-mau, thầy chốt 9/10/2026).
 * Tách solution_html (do `sol()` trong dung.py dựng) thành: khung Kiến thức → từng `.bt-step` → Đáp số;
 * bước bị giấu theo `fading` (N6 ví dụ mờ dần) chỉ mở khi em trả lời đúng câu hỏi của bước (L1 phản hồi tức thì,
 * giải thích vì sao sai), sai 2 lần mới được "Xem bước này". Bước ≥ 2 bị giấu hỏi thêm "Bước tiếp theo là gì?".
 * `jump` (từ bài tương tự làm sai, mục gỡ rối) mở đúng bước đó và cuộn tới.
 */

/** Bước nào bị giấu (bước không có câu hỏi, như Kiểm tra, không giấu). Giữ khớp với hiddenSteps trong skill scripts/lib.ts. */
export function hiddenSteps(fading: WorkedFading | undefined, steps: WorkedStep[]): boolean[] {
  const last = steps.map((s) => !!s.hoi).lastIndexOf(true);
  return steps.map((s, i) =>
    !s.hoi ? false : fading === "giau_het" ? true : fading === "giau_tu_buoc_2" ? i >= 1 : fading === "giau_buoc_cuoi" ? i === last : false,
  );
}

const STEP = '<div class="bt-step">', FINAL = '<div class="bt-final">';

export function splitSolution(html: string): { head: string; steps: string[]; tail: string } | null {
  const inner = html.replace(/^\s*<div class="bt-sol">/, "").replace(/<\/div>\s*$/, "");
  const a = inner.indexOf(STEP), b = inner.indexOf(FINAL);
  if (a < 0 || b < a) return null;
  const steps = inner.slice(a, b).split(STEP).filter((s) => s.trim()).map((s) => STEP + s);
  return { head: inner.slice(0, a), steps, tail: inner.slice(b) };
}

/** Lấy số đầu tiên em gõ: "10,5 m" → 10.5 (D6: bàn phím số, dấu phẩy thập phân). */
function parseNumber(s: string): number | null {
  const m = s.replace(/\s+/g, "").match(/-?\d+(?:[.,]\d+)?/);
  return m ? Number(m[0].replace(",", ".")) : null;
}

/** Đảo thứ tự lựa chọn ổn định theo nội dung (không để đáp án đúng luôn ở đầu, nhưng không nhảy mỗi lần render). */
function stableShuffle(cs: WorkedChoice[]): WorkedChoice[] {
  const key = (c: WorkedChoice) => [...c.text].reduce((h, ch) => (h * 31 + ch.charCodeAt(0)) % 9973, 7);
  return [...cs].sort((x, y) => key(x) - key(y));
}

function Choices({
  choices,
  onPick,
  picked,
  color,
}: {
  choices: WorkedChoice[];
  onPick: (c: WorkedChoice) => void;
  picked: WorkedChoice | null;
  color: string;
}) {
  const list = useMemo(() => stableShuffle(choices), [choices]);
  return (
    <div className="grid gap-2">
      {list.map((c) => {
        const isPicked = picked === c;
        return (
          <button
            key={c.text}
            type="button"
            onClick={() => onPick(c)}
            className="bt-choice"
            style={isPicked ? { borderColor: c.dung ? "var(--color-ok)" : "var(--color-danger)" } : undefined}
            aria-pressed={isPicked}
          >
            <ContentHtml html={c.text} className="inline" />
          </button>
        );
      })}
      {picked && !picked.dung && picked.vi_sao && (
        <p className="bt-feedback bt-feedback--wrong" role="status">
          <ContentHtml html={picked.vi_sao} className="inline" />
        </p>
      )}
      {picked?.dung && (
        <p className="bt-feedback bt-feedback--ok" role="status" style={{ color }}>
          Đúng. Làm tiếp bước này.
        </p>
      )}
    </div>
  );
}

function StepAsk({
  step,
  index,
  color,
  onDone,
}: {
  step: WorkedStep;
  index: number;
  color: string;
  onDone: () => void;
}) {
  const needNext = !!step.chon_buoc_ke && index > 0;
  const [nextPick, setNextPick] = useState<WorkedChoice | null>(null);
  const [val, setVal] = useState("");
  const [pick, setPick] = useState<WorkedChoice | null>(null);
  const [wrong, setWrong] = useState(0);
  const [lastWrong, setLastWrong] = useState(false);
  const nextOk = !needNext || !!nextPick?.dung;

  function checkNumber() {
    const x = parseNumber(val);
    if (x === null) return;
    const ok = Math.abs(x - (step.dap_so ?? NaN)) <= (step.sai_so ?? 0) + 1e-9;
    if (ok) onDone();
    else {
      setWrong((n) => n + 1);
      setLastWrong(true);
    }
  }

  function pickChoice(c: WorkedChoice) {
    setPick(c);
    if (c.dung) onDone();
    else {
      setWrong((n) => n + 1);
      setLastWrong(true);
    }
  }

  return (
    <div className="bt-step bt-step--ask">
      <p className="bt-step-title">
        <span className="bt-step-n" style={{ borderColor: color, color }}>{index + 1}</span>
        <span>
          <ContentHtml html={step.tieu_de} className="inline" />
        </span>
      </p>
      {needNext && (
        <div className="bt-ask">
          <p className="bt-ask-q">Bước tiếp theo làm gì?</p>
          <Choices choices={step.chon_buoc_ke!} onPick={setNextPick} picked={nextPick} color={color} />
        </div>
      )}
      {nextOk && (
        <div className="bt-ask">
          <p className="bt-ask-q">
            <ContentHtml html={step.hoi ?? ""} className="inline" />
          </p>
          {step.lua_chon ? (
            <Choices choices={step.lua_chon} onPick={pickChoice} picked={pick} color={color} />
          ) : (
            <form
              className="bt-ask-row"
              onSubmit={(e) => {
                e.preventDefault();
                checkNumber();
              }}
            >
              <input
                className="bt-ask-input"
                inputMode="decimal"
                autoComplete="off"
                placeholder="Đáp số"
                aria-label={`Đáp số bước ${index + 1}`}
                value={val}
                onChange={(e) => {
                  setVal(e.target.value);
                  setLastWrong(false);
                }}
              />
              {step.don_vi && <span className="bt-ask-unit">{step.don_vi}</span>}
              <button type="submit" className="lesson-btn-ghost" disabled={parseNumber(val) === null}>
                Kiểm tra
              </button>
            </form>
          )}
          {lastWrong && !step.lua_chon && (
            <p className="bt-feedback bt-feedback--wrong" role="status">
              Chưa đúng. {step.loi_hay_gap && <ContentHtml html={step.loi_hay_gap} className="inline" />}
              {wrong < 2 && " Thử lại một lần."}
            </p>
          )}
          {lastWrong && step.lua_chon && step.loi_hay_gap && wrong >= 2 && (
            <p className="bt-feedback bt-feedback--wrong" role="status">
              <ContentHtml html={step.loi_hay_gap} className="inline" />
            </p>
          )}
          {wrong >= 2 && (
            <button type="button" className="lesson-btn-ghost" onClick={onDone}>
              Xem bước này
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default function StepwiseSolution({
  q,
  color,
  jump,
  onAllOpen,
}: {
  q: LessonWorkedQuestion;
  color: string;
  /** {idx, n}: n đổi → mở bước idx và cuộn tới (gỡ rối từ bài tương tự). */
  jump?: { idx: number; n: number } | null;
  /** Gọi một lần khi mọi bước đã mở — cha mới hiện "Làm bài tương tự" (ví dụ mẫu đi trước, retrieval đi sau). */
  onAllOpen?: () => void;
}) {
  const parts = useMemo(() => splitSolution(q.solution_html ?? ""), [q.solution_html]);
  const steps = useMemo(() => q.buoc ?? [], [q.buoc]);
  const usable = !!parts && parts.steps.length === steps.length && steps.length > 0;
  const hidden = useMemo(() => hiddenSteps(q.fading, steps), [q.fading, steps]);
  const [revealed, setRevealed] = useState<boolean[]>(() => hidden.map((h) => !h));
  const [flash, setFlash] = useState<number | null>(null);
  const refs = useRef<(HTMLDivElement | null)[]>([]);

  // Gỡ rối: prop `jump` đổi → mở tới bước đó (điều chỉnh state ngay lúc render, không setState trong effect) rồi cuộn + nháy khung.
  const [seenJump, setSeenJump] = useState(jump);
  if (jump !== seenJump) {
    setSeenJump(jump);
    if (jump && steps.length) {
      const idx = Math.min(Math.max(jump.idx, 0), steps.length - 1);
      setRevealed((r) => r.map((v, i) => v || i <= idx));
      setFlash(idx);
    }
  }
  useEffect(() => {
    if (flash === null) return;
    const t = setTimeout(() => refs.current[flash]?.scrollIntoView({ behavior: "smooth", block: "center" }), 50);
    const t2 = setTimeout(() => setFlash(null), 2500);
    return () => {
      clearTimeout(t);
      clearTimeout(t2);
    };
  }, [flash]);

  const current = revealed.findIndex((v) => !v); // bước đầu tiên chưa mở
  const allOpen = !usable || current < 0;
  useEffect(() => {
    if (allOpen) onAllOpen?.();
  }, [allOpen, onAllOpen]);

  if (!usable) return <ContentHtml html={q.solution_html ?? ""} className="block leading-relaxed" />;

  const reveal = (i: number) => setRevealed((r) => r.map((v, k) => v || k === i));

  return (
    <div className="exam-content block leading-relaxed">
     <div className="bt-sol">
      <ContentHtml html={parts!.head} className="block" />
      {steps.map((s, i) => (
        <div key={i} ref={(el) => { refs.current[i] = el; }} className={flash === i ? "bt-flash" : undefined}>
          {revealed[i] ? (
            <ContentHtml html={parts!.steps[i]} className="block" />
          ) : i === current ? (
            <StepAsk step={s} index={i} color={color} onDone={() => reveal(i)} />
          ) : (
            <p className="bt-step-title bt-step--locked">
              <span className="bt-step-n">{i + 1}</span>
              <span>
                <ContentHtml html={s.tieu_de} className="inline" />
              </span>
            </p>
          )}
        </div>
      ))}
      {allOpen ? (
        <ContentHtml html={parts!.tail} className="block" />
      ) : (
        <button type="button" className="bt-show-all" onClick={() => setRevealed(steps.map(() => true))}>
          Xem cả lời giải
        </button>
      )}
     </div>
    </div>
  );
}
