"use client";

// Mục "Luyện từ" bài Anh văn chuyên ngành Cơ khí — lượt ngắn, mỗi màn một câu, báo đúng/sai ngay, câu sai quay lại
// cuối lượt. Logic ở features/lessons/avcn-luyen-tu.ts. Quy tắc: N1, N5, L1, L2, L3 (không tim/XP), L4, D2, D3, E1, E4.
import { useCallback, useEffect, useRef, useState } from "react";
import { Volume2, X } from "lucide-react";
import { playSpeech } from "@/lib/play-speech";
import {
  buildRound,
  luyenTuUrl,
  readStats,
  recordResult,
  requeue,
  writeStats,
  type LtData,
  type LtItem,
  type LtWord,
  type LtStats,
} from "@/features/lessons/avcn-luyen-tu";

const LETTERS = ["A", "B", "C", "D"] as const;

type Phase = "start" | "run" | "done";
type Feedback = { ok: boolean; item: LtItem } | null;

const say = (w: LtWord) => playSpeech(w.term, w.audio ?? "");

export default function AvcnLuyenTu({
  chapter,
  onActiveChange,
}: {
  chapter: number;
  /** Đang trong lượt → trang hỏi trước khi đổi tab (mất lượt). */
  onActiveChange?: (active: boolean) => void;
}) {
  const [data, setData] = useState<LtData | null>(null);
  const [loadError, setLoadError] = useState(false);
  const [phase, setPhase] = useState<Phase>("start");
  const [queue, setQueue] = useState<LtItem[]>([]);
  const [base, setBase] = useState(0);
  const [cleared, setCleared] = useState(0);
  const [firstTry, setFirstTry] = useState(0);
  const [missed, setMissed] = useState<LtWord[]>([]);
  const [picked, setPicked] = useState<number | null>(null);
  const [feedback, setFeedback] = useState<Feedback>(null);
  const statsRef = useRef<LtStats>({});
  const nextRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    let alive = true;
    fetch(luyenTuUrl(chapter))
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((d: LtData) => alive && setData(d))
      .catch(() => alive && setLoadError(true));
    return () => {
      alive = false;
    };
  }, [chapter]);

  // Báo trang chỉ khi đổi pha (callback cha tạo mới mỗi lần render — không để nó làm chạy lại effect).
  const activeCbRef = useRef(onActiveChange);
  useEffect(() => {
    activeCbRef.current = onActiveChange;
  }, [onActiveChange]);
  useEffect(() => {
    activeCbRef.current?.(phase === "run");
  }, [phase]);
  useEffect(() => () => activeCbRef.current?.(false), []);

  const start = useCallback(() => {
    if (!data) return;
    statsRef.current = readStats(chapter);
    const items = buildRound(data, statsRef.current);
    setQueue(items);
    setBase(items.length);
    setCleared(0);
    setFirstTry(0);
    setMissed([]);
    setPicked(null);
    setFeedback(null);
    setPhase("run");
  }, [chapter, data]);

  const current = queue[0];

  // Câu nghe: đọc ngay khi hiện (bấm "Tiếp"/"Bắt đầu" vừa xong là thao tác của người dùng nên trình duyệt cho phát).
  useEffect(() => {
    if (phase === "run" && current?.kind === "nghe" && !feedback) say(current.word);
  }, [phase, current, feedback]);

  useEffect(() => {
    if (feedback) nextRef.current?.focus({ preventScroll: true });
  }, [feedback]);

  const finishItem = useCallback(
    (item: LtItem, ok: boolean, results: { w: LtWord; ok: boolean }[]) => {
      let s = statsRef.current;
      for (const r of results) s = recordResult(s, r.w, r.ok);
      statsRef.current = s;
      writeStats(chapter, s);
      if (ok) {
        setCleared((c) => c + 1);
        if (item.retry === 0) setFirstTry((c) => c + 1);
      } else if (item.kind !== "ghep") {
        setMissed((m) => (m.some((w) => w.term === item.word.term && w.vi === item.word.vi) ? m : [...m, item.word]));
      }
      setFeedback({ ok, item });
    },
    [chapter],
  );

  const choose = (i: number) => {
    if (!current || current.kind === "ghep" || feedback) return;
    setPicked(i);
    const ok = i === current.answer;
    // Nghe lại từ đúng sau khi chọn — gắn âm với chữ và nghĩa (Mayer: đa phương tiện, kênh đôi).
    say(current.word);
    finishItem(current, ok, [{ w: current.word, ok }]);
  };

  const next = () => {
    if (!current || !feedback) return;
    let q = queue.slice(1);
    if (!feedback.ok) q = requeue(q, current);
    // Câu sai hết lượt quay lại (MAX_RETRY) vẫn tính là đã qua để thanh tiến độ về đích.
    if (!feedback.ok && q.length === queue.length - 1) setCleared((c) => c + 1);
    setQueue(q);
    setPicked(null);
    setFeedback(null);
    if (q.length === 0) setPhase("done");
  };

  if (loadError) return <p className="text-sm text-muted">Chưa tải được phần luyện từ. Thử tải lại trang.</p>;
  if (!data) return <p className="avcn-lt-loading text-sm text-muted">Đang tải phần luyện từ…</p>;

  if (phase === "start") {
    return (
      <section className="avcn-lt avcn-lt--start" aria-label="Luyện từ">
        <p className="avcn-lt-title">Luyện từ vựng Chapter {data.chapter}</p>
        <p className="avcn-lt-sub">
          11 câu · khoảng 3 phút. Chọn nghĩa, nghe chọn từ, ghép cặp. Câu sai sẽ quay lại cuối lượt.
        </p>
        <button type="button" className="avcn-lt-btn" onClick={start}>
          Bắt đầu
        </button>
      </section>
    );
  }

  if (phase === "done") {
    return (
      <section className="avcn-lt avcn-lt--done" aria-label="Kết quả lượt luyện từ" aria-live="polite">
        <p className="avcn-lt-title">Xong lượt!</p>
        <p className="avcn-lt-sub">
          Đúng ngay lần đầu <strong>{firstTry}</strong>/{base} câu.
          {missed.length === 0 ? " Không sót từ nào." : " Nghe lại các từ còn nhầm — lượt sau từ hay sai được hỏi trước."}
        </p>
        {missed.length > 0 && (
          <ul className="avcn-lt-missed">
            {missed.map((w) => (
              <li key={`${w.term}|${w.vi}`}>
                <button type="button" className="avcn-lt-say" onClick={() => say(w)} aria-label={`Nghe ${w.term}`}>
                  <Volume2 size={18} aria-hidden />
                </button>
                <span className="avcn-lt-missed-term">{w.term}</span>
                <span className="avcn-lt-missed-vi">{w.vi}</span>
              </li>
            ))}
          </ul>
        )}
        <button type="button" className="avcn-lt-btn" onClick={start}>
          Luyện lượt nữa
        </button>
      </section>
    );
  }

  if (!current) return null;
  const pct = base ? Math.round((cleared / base) * 100) : 0;

  return (
    <section className="avcn-lt avcn-lt--run" aria-label="Đang luyện từ">
      <div className="avcn-lt-top">
        <button
          type="button"
          className="avcn-lt-quit"
          onClick={() => setPhase("start")}
          aria-label="Thoát lượt luyện"
          title="Thoát"
        >
          <X size={20} aria-hidden />
        </button>
        <div
          className="avcn-lt-bar"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={base}
          aria-valuenow={cleared}
          aria-label="Tiến độ lượt"
        >
          <span style={{ width: `${pct}%` }} />
        </div>
      </div>

      <div className="exam-paper avcn-lt-body">
        {current.kind === "ghep" ? (
          <MatchPairs key={current.id} item={current} locked={!!feedback} onDone={finishItem} />
        ) : (
          <>
            <p className="avcn-lt-ask">
              {current.retry > 0 && <span className="avcn-lt-again">Làm lại · </span>}
              {current.kind === "nghia" && "Từ này nghĩa là gì?"}
              {current.kind === "tu" && "Chọn từ tiếng Anh đúng nghĩa"}
              {current.kind === "nghe" && "Nghe rồi chọn từ đúng"}
            </p>
            {current.kind === "nghia" && (
              <div className="avcn-lt-prompt">
                <button type="button" className="avcn-lt-say" onClick={() => say(current.word)} aria-label="Nghe từ">
                  <Volume2 size={20} aria-hidden />
                </button>
                <span lang="en" className="avcn-lt-word">
                  {current.word.term}
                </span>
              </div>
            )}
            {current.kind === "tu" && (
              <div className="avcn-lt-prompt">
                <span className="avcn-lt-word">{current.word.vi}</span>
              </div>
            )}
            {current.kind === "nghe" && (
              <div className="avcn-lt-prompt avcn-lt-prompt--nghe">
                <button
                  type="button"
                  className="avcn-lt-say avcn-lt-say--big"
                  onClick={() => say(current.word)}
                  aria-label="Nghe lại"
                >
                  <Volume2 size={32} aria-hidden />
                </button>
              </div>
            )}
            <ul className="avcn-lt-opts" role="list">
              {current.options.map((opt, i) => {
                const state = !feedback
                  ? ""
                  : i === current.answer
                    ? "is-right"
                    : i === picked
                      ? "is-wrong"
                      : "is-dim";
                return (
                  <li key={opt}>
                    <button
                      type="button"
                      className={`avcn-lt-opt ${state}`}
                      onClick={() => choose(i)}
                      disabled={!!feedback}
                      lang={current.kind === "nghia" ? "vi" : "en"}
                    >
                      <span className="avcn-lt-opt-letter">{LETTERS[i]}.</span>
                      <span>{opt}</span>
                    </button>
                  </li>
                );
              })}
            </ul>
          </>
        )}
      </div>

      {feedback && (
        <div className={`avcn-lt-fb ${feedback.ok ? "is-ok" : "is-no"}`} role="status" aria-live="polite">
          <FeedbackText fb={feedback} />
          <button ref={nextRef} type="button" className="avcn-lt-btn" onClick={next}>
            {queue.length === 1 && (feedback.ok || feedback.item.kind === "ghep" || feedback.item.retry >= 2)
              ? "Xem kết quả"
              : "Tiếp"}
          </button>
        </div>
      )}
    </section>
  );
}

function FeedbackText({ fb }: { fb: NonNullable<Feedback> }) {
  const { item, ok } = fb;
  if (item.kind === "ghep") {
    return <p className="avcn-lt-fb-head">{ok ? "Ghép đúng hết ngay!" : "Ghép xong. Các từ ghép nhầm sẽ được hỏi lại ở lượt sau."}</p>;
  }
  const w = item.word;
  return (
    <div>
      <p className="avcn-lt-fb-head">{ok ? "Đúng!" : item.retry >= 2 ? "Chưa đúng — ghi nhớ từ này nhé:" : "Chưa đúng. Câu này sẽ quay lại cuối lượt."}</p>
      <p className="avcn-lt-fb-word">
        <strong lang="en">{w.term}</strong>
        {w.ipa && <span className="avcn-lt-ipa"> {w.ipa}</span>} = {w.vi}
      </p>
    </div>
  );
}

/** Ghép 5 cặp từ – nghĩa: chạm một từ bên trái rồi một nghĩa bên phải (hoặc ngược lại). Cặp đúng mờ đi; cặp sai
 *  nháy đỏ rồi bỏ chọn. Xong cả 5 cặp mới báo — đúng hết không nhầm lần nào thì tính là đúng. */
function MatchPairs({
  item,
  locked,
  onDone,
}: {
  item: Extract<LtItem, { kind: "ghep" }>;
  locked: boolean;
  onDone: (item: LtItem, ok: boolean, results: { w: LtWord; ok: boolean }[]) => void;
}) {
  const [left, setLeft] = useState<number | null>(null);
  const [right, setRight] = useState<number | null>(null);
  const [matched, setMatched] = useState<Set<number>>(new Set());
  const [wrong, setWrong] = useState<[number, number] | null>(null);
  const missRef = useRef<Set<number>>(new Set());

  const timerRef = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(timerRef.current), []);

  /** Đã chọn đủ một bên trái + một bên phải → chấm cặp (gọi trong xử lý bấm, không qua effect). */
  const tryPair = (l: number | null, r: number | null) => {
    setLeft(l);
    setRight(r);
    if (l === null || r === null) return;
    if (l === r) {
      say(item.pairs[l]);
      const m = new Set(matched).add(l);
      setMatched(m);
      setLeft(null);
      setRight(null);
      if (m.size === item.pairs.length) {
        // Từ ghép nhầm tính sai, còn lại tính đúng; cả lượt ghép "đúng" khi không nhầm lần nào.
        onDone(
          item,
          missRef.current.size === 0,
          item.pairs.map((w, i) => ({ w, ok: !missRef.current.has(i) })),
        );
      }
      return;
    }
    missRef.current.add(l);
    setWrong([l, r]);
    timerRef.current = window.setTimeout(() => {
      setWrong(null);
      setLeft(null);
      setRight(null);
    }, 650);
  };

  const cls = (side: "l" | "r", i: number) => {
    if (matched.has(i)) return "is-matched";
    if (wrong && (side === "l" ? wrong[0] : wrong[1]) === i) return "is-wrong";
    if ((side === "l" ? left : right) === i) return "is-picked";
    return "";
  };
  const busy = locked || wrong !== null;

  return (
    <>
      <p className="avcn-lt-ask">Ghép từ với nghĩa đúng</p>
      <div className="avcn-lt-match">
        <ul role="list">
          {item.pairs.map((w, i) => (
            <li key={`l${i}`}>
              <button
                type="button"
                lang="en"
                className={`avcn-lt-tile ${cls("l", i)}`}
                disabled={busy || matched.has(i)}
                aria-pressed={left === i}
                onClick={() => {
                  say(w);
                  tryPair(i, right);
                }}
              >
                {w.term}
              </button>
            </li>
          ))}
        </ul>
        <ul role="list">
          {item.rightOrder.map((i) => (
            <li key={`r${i}`}>
              <button
                type="button"
                className={`avcn-lt-tile ${cls("r", i)}`}
                disabled={busy || matched.has(i)}
                aria-pressed={right === i}
                onClick={() => tryPair(left, i)}
              >
                {item.pairs[i].vi}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
