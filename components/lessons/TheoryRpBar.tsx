"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { getSupabase } from "@/services/supabase";

/**
 * RP cho bài lý thuyết. Hai lượt, cùng cách bắt đáp án:
 *  - lượt đầu : rank_theory_open khi mở bài → rank_theory_submit
 *  - lượt ôn  : rank_theory_review_open (chỉ khi đã đạt lượt đầu, đủ cách ngày, còn lượt) → rank_theory_review_submit
 * Các câu tự chấm `.tl-quiz` là radio thuần CSS, nên đáp án được nghe qua sự kiện change trên `rootRef`
 * (chỉ lần chọn ĐẦU mỗi câu). Khoá câu = `name` của radio; đáp án = chữ A–F theo thứ tự lựa chọn.
 * Máy chủ chấm, chặn trả lời quá nhanh, giới hạn trần ngày/tuần/mùa. Mức RP chỉnh trong rank_seasons.config,
 * nên giao diện KHÔNG ghi số RP cố định trước khi nộp — số thật hiện ở kết quả.
 */
const LETTERS = ["A", "B", "C", "D", "E", "F"];

type Mode = "loading" | "first" | "review" | "wait" | "maxed" | "off";
type Result = { ok?: boolean; reason?: string; awarded?: number; correct?: number; total?: number; pct?: number };

const REASON_TEXT: Record<string, string> = {
  below_pass: "Chưa đủ 70% câu đúng ở lượt này nên chưa có RP. Em đọc lại phần giải thích rồi học tiếp nhé.",
  too_fast: "Em trả lời nhanh hơn thời gian đọc bài, nên lần này chưa tính RP.",
  capped: "Hôm nay hoặc tuần này em đã đạt trần RP bài lý thuyết.",
  no_season: "Chưa có mùa xếp hạng đang mở nên chưa cộng RP.",
  already: "Em đã nộp bài này rồi, lượt đầu mới tính RP.",
};

function fmtDay(iso: string): string {
  const d = new Date(iso);
  return `${d.getDate()}/${d.getMonth() + 1}`;
}

export function useTheoryRp(itemId: number, bodyHtml: string, rootRef: React.RefObject<HTMLElement | null>) {
  const total = useMemo(() => (bodyHtml.match(/class="[^"]*\btl-quiz\b/g) ?? []).length, [bodyHtml]);
  const answers = useRef<Record<string, string>>({});
  const [fetched, setFetched] = useState<Mode>("loading");
  const [lastTotal, setLastTotal] = useState(total);
  // Mở/đóng mục đổi `total` (0 khi đóng): đặt lại trạng thái ngay trong lúc render, không qua effect.
  if (lastTotal !== total) {
    setLastTotal(total);
    setFetched("loading");
  }
  const mode: Mode = total === 0 ? "off" : fetched;
  const setMode = setFetched;
  const [availableAt, setAvailableAt] = useState<string | null>(null);
  const [count, setCount] = useState(0);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Result | null>(null);

  useEffect(() => {
    if (total === 0) return;
    let alive = true;
    (async () => {
      const sb = getSupabase();
      const { data, error } = await sb.rpc("rank_theory_review_open", { p_item: itemId });
      if (!alive) return;
      const r = (error ? null : data) as { ok?: boolean; reason?: string; available_at?: string } | null;
      if (!r) return setMode("off");
      if (r.ok) return setMode("review");
      if (r.reason === "too_soon") {
        setAvailableAt(r.available_at ?? null);
        return setMode("wait");
      }
      if (r.reason === "max_rounds") return setMode("maxed");
      if (r.reason === "no_first_pass") {
        void sb.rpc("rank_theory_open", { p_item: itemId }).then(() => {}, () => {});
        return setMode("first");
      }
      setMode("off"); // no_key · not_student · no_season
    })().catch(() => alive && setMode("off"));
    return () => { alive = false; };
  }, [itemId, total]);

  const listening = mode === "first" || mode === "review";
  useEffect(() => {
    const root = rootRef.current;
    if (!root || !listening) return;
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
  }, [rootRef, listening]);

  async function submit() {
    setBusy(true);
    try {
      const fn = mode === "review" ? "rank_theory_review_submit" : "rank_theory_submit";
      const { data, error } = await getSupabase().rpc(fn, { p_item: itemId, p_answers: answers.current });
      const r = (error ? null : data) as Result | null;
      if (!r || r.reason === "no_key" || r.reason === "not_student") setMode("off");
      else setResult(r);
    } finally {
      setBusy(false);
    }
  }

  return { mode, total, count, busy, result, availableAt, submit };
}

type RpState = ReturnType<typeof useTheoryRp>;

/** Một dòng đầu bài: em biết luật trước khi học (N1) — không huy hiệu, không số RP cố định. */
export function TheoryRpHint({ rp }: { rp: RpState }) {
  const { mode, availableAt } = rp;
  let text = "";
  if (mode === "first") text = "Làm đúng từ 70% các câu tự kiểm tra trong bài để nhận RP. Mỗi bài tính một lần.";
  else if (mode === "review") text = "Em đang học lại bài này: làm đúng từ 70% các câu tự kiểm tra để nhận RP ôn lại.";
  else if (mode === "wait") text = `Học lại bài này từ ngày ${availableAt ? fmtDay(availableAt) : "sau"} sẽ nhận thêm RP ôn lại.`;
  else if (mode === "maxed") text = "Em đã nhận đủ RP ôn lại của bài này trong mùa.";
  if (!text) return null;
  return <p className="mb-3 text-sm text-muted">{text}</p>;
}

export default function TheoryRpBar({ rp }: { rp: RpState }) {
  const { mode, total, count, busy, result, submit } = rp;
  if ((mode !== "first" && mode !== "review") || count === 0) return null;
  return (
    <div className="theory-rp-bar" role="status" aria-live="polite">
      {!result ? (
        <>
          <span>
            Đã trả lời {count}/{total} câu
          </span>
          <button type="button" className="lesson-done" onClick={submit} disabled={busy || count < total}>
            {busy ? "Đang chấm…" : mode === "review" ? "Nộp để nhận RP ôn lại" : "Nộp để nhận RP"}
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
