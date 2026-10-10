"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { X } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import { useToast } from "@/components/ui/Toast";
import type { HostState } from "@/features/quiz-live/types";
import { quizErrorText } from "@/features/quiz-live/types";
import { advanceRoom, endRoom, getHostState, kickPlayer } from "@/services/quiz-live";
import { OPTION_STYLE, TimerBar, useCountdown, usePoll } from "./shared";

/** Màn hình điều khiển + chiếu lên lớp: PIN lớn, câu hỏi, đếm người trả lời, đáp án + bảng xếp hạng. */
export default function QuizHostRoom({ roomId }: { roomId: number }) {
  const toast = useToast();
  const [st, setSt] = useState<HostState | null>(null);
  const [stamp, setStamp] = useState(0);
  const [busy, setBusy] = useState(false);
  const [fatal, setFatal] = useState("");
  const [joinUrl, setJoinUrl] = useState("");

  useEffect(() => {
    const t = setTimeout(() => setJoinUrl(`${window.location.host}/choi`), 0);
    return () => clearTimeout(t);
  }, []);

  const { refresh, error } = usePoll(
    () => getHostState(roomId),
    (last) => (last?.phase === "question" ? 1000 : 2000),
    (d) => {
      setSt(d);
      setStamp(Date.now());
    },
    !fatal,
  );
  useEffect(() => {
    if (error && /forbidden|room_not_found/.test(error)) setTimeout(() => setFatal(quizErrorText(error)), 0);
  }, [error]);

  const left = useCountdown(st?.seconds_left ?? 0, stamp, st?.phase === "question");

  const next = useCallback(async () => {
    if (busy) return;
    setBusy(true);
    try {
      await advanceRoom(roomId);
      refresh();
    } catch (e) {
      toast("error", quizErrorText(e));
    } finally {
      setBusy(false);
    }
  }, [busy, roomId, refresh, toast]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "BUTTON") return;
      if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        void next();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [next]);

  async function kick(id: number) {
    try {
      await kickPlayer(roomId, id);
      refresh();
    } catch (e) {
      toast("error", quizErrorText(e));
    }
  }
  async function end() {
    if (!confirm("Kết thúc phòng này? Học sinh sẽ thấy bảng xếp hạng cuối.")) return;
    try {
      await endRoom(roomId);
      refresh();
    } catch (e) {
      toast("error", quizErrorText(e));
    }
  }

  if (fatal)
    return (
      <div className="space-y-4 text-center">
        <p className="text-ink">{fatal}</p>
        <Link href="/tro-giang/do-vui" className="text-primary underline">Về danh sách bộ câu</Link>
      </div>
    );
  if (!st) return <p className="text-ink">Đang mở phòng…</p>;

  const answered = st.players.filter((p) => p.answered).length;
  const last = st.index + 1 >= st.total;
  const nextLabel =
    st.phase === "lobby" ? "Bắt đầu" : st.phase === "question" ? "Chốt đáp án" : last ? "Xem kết quả cuối" : "Câu tiếp theo";

  return (
    <div className="mx-auto w-full max-w-5xl space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3 text-sm text-ink">
        <span className="font-semibold text-ink">{st.title}</span>
        <span>
          Vào chơi: <b className="text-ink">{joinUrl}</b> · PIN <b className="font-mono text-ink">{st.pin}</b>
        </span>
        <span>{st.players.length} người chơi{error ? " · mất kết nối, đang thử lại…" : ""}</span>
      </div>

      {st.phase === "lobby" && (
        <div className="space-y-6 rounded-3xl border border-line bg-panel p-6 text-center sm:p-10">
          <p className="text-ink">Mở <b className="text-ink">{joinUrl}</b> trên điện thoại và nhập mã</p>
          <p className="font-mono text-7xl font-extrabold tracking-[0.2em] text-ink sm:text-8xl">{st.pin}</p>
          <div className="flex min-h-12 flex-wrap justify-center gap-2">
            {st.players.length === 0 && <span className="text-muted">Chưa có ai vào…</span>}
            {st.players.map((p) => (
              <span key={p.id} className="inline-flex items-center gap-1 rounded-full bg-surface-2 py-1.5 pl-4 pr-2 text-sm font-semibold text-ink">
                {p.nickname}
                <button onClick={() => void kick(p.id)} aria-label={`Mời ${p.nickname} ra`} className="grid size-7 place-items-center rounded-full text-ink hover:bg-surface-2">
                  <X size={14} />
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      {(st.phase === "question" || st.phase === "reveal") && (
        <>
          <div className="flex items-center justify-between text-sm text-ink">
            <span className="font-semibold">Câu {st.index + 1}/{st.total}</span>
            <span>{answered}/{st.players.length} đã trả lời</span>
          </div>
          {st.phase === "question" && <TimerBar left={left} total={st.time_limit} />}
          <div className="rounded-3xl border border-line-strong bg-panel p-6 text-2xl leading-relaxed text-ink sm:p-8 sm:text-3xl">
            <ContentHtml html={st.question ?? ""} />
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {(st.options ?? []).map((o, i) => {
              const reveal = st.phase === "reveal";
              const isRight = reveal && st.answer === i;
              const max = Math.max(1, ...(st.counts ?? [0]));
              return (
                <div key={i} className={`relative overflow-hidden rounded-2xl p-4 text-white ${OPTION_STYLE[i].bg} ${reveal && !isRight ? "opacity-40" : ""} ${isRight ? `ring-4 ${OPTION_STYLE[i].ring}` : ""}`}>
                  <div className="flex items-start gap-3">
                    <span className="text-xl font-extrabold">{OPTION_STYLE[i].letter}</span>
                    <span className="flex-1 text-xl font-semibold leading-snug"><ContentHtml html={o} /></span>
                    {isRight && <span className="text-2xl font-extrabold" aria-label="đáp án đúng">✓</span>}
                  </div>
                  {reveal && (
                    <div className="mt-3 flex items-center gap-2 text-sm font-bold">
                      <div className="h-2 flex-1 rounded-full bg-black/25">
                        <div className="h-2 rounded-full bg-white/80" style={{ width: `${((st.counts?.[i] ?? 0) / max) * 100}%` }} />
                      </div>
                      <span className="w-6 text-right tabular-nums">{st.counts?.[i] ?? 0}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          {st.phase === "reveal" && st.explanation && (
            <div className="rounded-2xl border border-line bg-surface-2 p-4 text-ink"><ContentHtml html={st.explanation} /></div>
          )}
          {st.phase === "reveal" && <Board top={st.top ?? []} />}
        </>
      )}

      {st.phase === "finished" && (
        <div className="space-y-4 rounded-3xl border border-line bg-panel p-6 text-center sm:p-10">
          <p className="text-3xl font-extrabold text-ink">Kết thúc — bảng xếp hạng</p>
          <Board top={st.top ?? []} podium />
          <Link href="/tro-giang/do-vui" className="inline-block rounded-2xl bg-primary px-6 py-3 font-bold text-white">Về danh sách bộ câu</Link>
        </div>
      )}

      {st.phase !== "finished" && (
        <div className="flex flex-wrap items-center justify-between gap-3">
          <button onClick={() => void end()} className="min-h-11 rounded-xl border border-line px-4 text-sm text-ink hover:bg-surface-2">Kết thúc phòng</button>
          <button onClick={() => void next()} disabled={busy || (st.phase === "lobby" && st.players.length === 0)} className="min-h-14 rounded-2xl bg-primary px-8 text-lg font-bold text-white disabled:opacity-40">
            {nextLabel} <span className="ml-1 text-xs font-normal opacity-70">(phím cách)</span>
          </button>
        </div>
      )}
    </div>
  );
}

function Board({ top, podium = false }: { top: { id: number; nickname: string; score: number }[]; podium?: boolean }) {
  if (!top.length) return null;
  const medals = ["🥇", "🥈", "🥉"];
  return (
    <ol className="mx-auto max-w-xl space-y-2 text-left">
      {top.slice(0, podium ? 10 : 5).map((t, i) => (
        <li key={t.id} className="flex items-center justify-between rounded-xl bg-surface-2 px-5 py-3 text-lg text-ink">
          <span className="truncate"><span className="mr-3 inline-block w-8 font-mono">{medals[i] ?? i + 1}</span>{t.nickname}</span>
          <span className="font-mono font-bold tabular-nums">{t.score}</span>
        </li>
      ))}
    </ol>
  );
}
