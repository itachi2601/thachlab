"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { getSupabase } from "@/services/supabase";

/**
 * RP cho bài lý thuyết: mở bài → rank_theory_open; các câu tự chấm `.tl-quiz` (radio, không JS)
 * được nghe qua sự kiện change trên `rootRef`; nộp → rank_theory_submit. Máy chủ chấm, chặn trả lời
 * quá nhanh, chỉ cộng lượt đầu. Khoá câu = thuộc tính `name` của radio; đáp án = chữ A–D theo thứ tự lựa chọn.
 * Bài chưa có dòng theory_quiz_keys → máy chủ trả no_key → thanh tự ẩn.
 */
const LETTERS = ["A", "B", "C", "D", "E", "F"];

type Result = { ok?: boolean; reason?: string; awarded?: number; correct?: number; total?: number; pct?: number };

const REASON_TEXT: Record<string, string> = {
  below_pass: "Chưa đủ 70% câu đúng ở lượt đầu nên chưa có RP. Em đọc lại phần giải thích rồi học tiếp nhé.",
  too_fast: "Em trả lời nhanh hơn thời gian đọc bài, nên lần này chưa tính RP.",
  capped: "Hôm nay hoặc tuần này em đã đạt trần RP bài lý thuyết.",
  no_season: "Chưa có mùa xếp hạng đang mở nên chưa cộng RP.",
  already: "Em đã nộp bài này rồi, lượt đầu mới tính RP.",
};

export default function TheoryRpBar({
  itemId,
  bodyHtml,
  rootRef,
}: {
  itemId: number;
  bodyHtml: string;
  rootRef: React.RefObject<HTMLElement | null>;
}) {
  const total = useMemo(() => (bodyHtml.match(/class="[^"]*\btl-quiz\b/g) ?? []).length, [bodyHtml]);
  const answers = useRef<Record<string, string>>({});
  const [count, setCount] = useState(0);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    if (total === 0) return;
    void getSupabase().rpc("rank_theory_open", { p_item: itemId }).then(() => {}, () => {});
  }, [itemId, total]);

  useEffect(() => {
    const root = rootRef.current;
    if (!root || total === 0) return;
    function onChange(e: Event) {
      const input = e.target as HTMLInputElement | null;
      if (!input || input.type !== "radio" || !input.name) return;
      const quiz = input.closest(".tl-quiz");
      if (!quiz || answers.current[input.name]) return; // chỉ tính lần chọn ĐẦU
      const radios = Array.from(quiz.querySelectorAll<HTMLInputElement>('input[type="radio"]'));
      const letter = LETTERS[radios.indexOf(input)];
      if (!letter) return;
      answers.current[input.name] = letter;
      setCount(Object.keys(answers.current).length);
    }
    root.addEventListener("change", onChange);
    return () => root.removeEventListener("change", onChange);
  }, [rootRef, total]);

  if (total === 0 || hidden || count === 0) return null;

  async function submit() {
    setBusy(true);
    try {
      const { data, error } = await getSupabase().rpc("rank_theory_submit", {
        p_item: itemId,
        p_answers: answers.current,
      });
      const r = (error ? null : data) as Result | null;
      if (!r || r.reason === "no_key" || r.reason === "not_student") setHidden(true);
      else setResult(r);
    } finally {
      setBusy(false);
    }
  }

  const done = result !== null;
  return (
    <div className="theory-rp-bar" role="status" aria-live="polite">
      {!done ? (
        <>
          <span>
            Đã trả lời {count}/{total} câu
          </span>
          <button type="button" className="lesson-done" onClick={submit} disabled={busy || count < total}>
            {busy ? "Đang chấm…" : "Nộp để nhận RP"}
          </button>
        </>
      ) : (
        <span>
          {result.reason === "ok" && (result.awarded ?? 0) > 0
            ? `+${result.awarded} RP · đúng ${result.correct}/${result.total} câu`
            : `Đúng ${result.correct ?? 0}/${result.total ?? total} câu. ${REASON_TEXT[result.reason ?? ""] ?? ""}`}
        </span>
      )}
    </div>
  );
}
