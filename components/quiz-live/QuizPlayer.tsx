"use client";

import { useEffect, useRef, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import type { PlayerState } from "@/features/quiz-live/types";
import { quizErrorText } from "@/features/quiz-live/types";
import { getPlayerState, joinQuiz, sendAnswer, type JoinResult } from "@/lib/quiz-live-play";
import { OPTION_STYLE, TimerBar, useCountdown, usePoll } from "./shared";

const KEY = "thachlab-quiz-session";
type Session = Pick<JoinResult, "room_id" | "token" | "nickname">;

function loadSession(): Session | null {
  try {
    const s = sessionStorage.getItem(KEY);
    return s ? (JSON.parse(s) as Session) : null;
  } catch {
    return null;
  }
}
function saveSession(s: Session | null) {
  try {
    if (s) sessionStorage.setItem(KEY, JSON.stringify(s));
    else sessionStorage.removeItem(KEY);
  } catch {
    /* trình duyệt chặn lưu — vẫn chơi được, chỉ không tự vào lại khi tải lại trang */
  }
}

const inputCls =
  "w-full rounded-2xl border border-line-strong bg-surface-2 px-4 py-4 text-center text-xl font-bold text-ink placeholder:text-muted focus:border-primary focus:outline-none";

function JoinForm({ initialPin, onJoined }: { initialPin: string; onJoined: (s: Session) => void }) {
  const [pin, setPin] = useState(initialPin);
  const [nick, setNick] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (busy) return;
    setBusy(true);
    setErr("");
    try {
      const r = await joinQuiz(pin.trim(), nick.trim());
      const s = { room_id: r.room_id, token: r.token, nickname: r.nickname };
      saveSession(s);
      onJoined(s);
    } catch (e2) {
      setErr(quizErrorText(e2));
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="mx-auto flex w-full max-w-sm flex-col gap-4">
      <h1 className="text-center font-display text-3xl font-extrabold text-ink">Đố vui lớp học</h1>
      <label className="block">
        <span className="mb-1 block text-center text-sm text-ink">Mã PIN trên màn hình lớp</span>
        <input
          className={`${inputCls} tracking-[0.3em]`}
          inputMode="numeric"
          autoComplete="off"
          maxLength={6}
          value={pin}
          onChange={(e) => setPin(e.target.value.replace(/\D/g, ""))}
          placeholder="000000"
        />
      </label>
      <label className="block">
        <span className="mb-1 block text-center text-sm text-ink">Biệt danh của em</span>
        <input className={inputCls} maxLength={20} value={nick} onChange={(e) => setNick(e.target.value)} placeholder="Ví dụ: Newton" />
      </label>
      {err && <p role="alert" className="rounded-xl bg-red-500/15 px-4 py-3 text-center text-sm text-danger">{err}</p>}
      <button
        type="submit"
        disabled={busy || pin.length < 6 || !nick.trim()}
        className="min-h-14 rounded-2xl bg-primary px-6 text-lg font-bold text-white disabled:opacity-40"
      >
        {busy ? "Đang vào…" : "Vào phòng"}
      </button>
      <p className="text-center text-xs text-muted">Không cần đăng nhập. Đừng dùng tên thật của bạn khác.</p>
    </form>
  );
}

function Scoreline({ s }: { s: Extract<PlayerState, { score: number }> }) {
  return (
    <div className="flex items-center justify-between rounded-2xl bg-surface-2 px-4 py-3 text-sm text-ink">
      <span className="truncate font-semibold">{s.nickname}</span>
      <span className="font-mono tabular-nums">
        Hạng <b className="text-ink">{s.rank}</b> · <b className="text-ink">{s.score}</b> điểm
      </span>
    </div>
  );
}

function Game({ session, onLeave }: { session: Session; onLeave: () => void }) {
  const [state, setState] = useState<PlayerState | null>(null);
  const [stamp, setStamp] = useState(0);
  const [picked, setPicked] = useState<{ index: number; choice: number } | null>(null);
  const [sendErr, setSendErr] = useState("");
  const sending = useRef(false);

  const { refresh, error } = usePoll(
    () => getPlayerState(session.room_id, session.token),
    (last) => (last && "phase" in last && last.phase === "question" ? 1200 : 2000),
    (d) => {
      setState(d);
      setStamp(Date.now());
    },
  );

  const live = state && "title" in state ? state : null;
  const left = useCountdown(live?.seconds_left ?? 0, stamp, live?.phase === "question");

  useEffect(() => {
    if (state && (state.phase === "kicked" || state.phase === "gone")) saveSession(null);
  }, [state]);

  async function choose(choice: number) {
    if (!live || sending.current || live.phase !== "question") return;
    if (picked?.index === live.index) return;
    sending.current = true;
    setSendErr("");
    setPicked({ index: live.index, choice });
    try {
      await sendAnswer(session.room_id, session.token, choice);
    } catch (e) {
      setSendErr(quizErrorText(e));
      setPicked(null);
    } finally {
      sending.current = false;
      refresh();
    }
  }

  if (!state)
    return <p className="text-center text-ink">{error ? "Đang kết nối lại…" : "Đang vào phòng…"}</p>;
  if (state.phase === "kicked" || state.phase === "gone")
    return (
      <div className="mx-auto max-w-sm space-y-4 text-center">
        <p className="text-lg text-ink">{state.phase === "kicked" ? "Bạn không còn trong phòng này." : "Phòng đã đóng."}</p>
        <button onClick={onLeave} className="min-h-12 rounded-2xl bg-primary px-6 font-bold text-white">Vào phòng khác</button>
      </div>
    );
  const s = state as Extract<PlayerState, { score: number }>;
  const myChoice = s.my_choice ?? (picked && picked.index === s.index ? picked.choice : null);

  return (
    <div className="mx-auto flex w-full max-w-lg flex-col gap-4">
      <Scoreline s={s} />
      {error && <p className="text-center text-xs text-warn">Mạng chập chờn — đang thử lại…</p>}

      {s.phase === "lobby" && (
        <div className="space-y-2 py-10 text-center">
          <p className="text-2xl font-extrabold text-ink">Đã vào phòng!</p>
          <p className="text-ink">{s.title}</p>
          <p className="text-muted">{s.players} bạn đang chờ · chờ thầy/cô bắt đầu…</p>
        </div>
      )}

      {s.phase === "question" && (
        <>
          <p className="text-center text-sm font-semibold text-ink">Câu {s.index + 1}/{s.total}</p>
          <TimerBar left={left} total={s.time_limit} />
          <div className="rounded-2xl bg-surface-2 p-4 text-lg leading-relaxed text-ink">
            <ContentHtml html={s.question ?? ""} />
          </div>
          {myChoice !== null ? (
            <p className="rounded-2xl bg-surface-2 py-4 text-center font-semibold text-ink">
              Đã chọn {OPTION_STYLE[myChoice].letter} — chờ cả lớp…
            </p>
          ) : left <= 0 ? (
            <p className="rounded-2xl bg-surface-2 py-4 text-center font-semibold text-ink">Hết giờ…</p>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {(s.options ?? []).map((o, i) => (
                <button
                  key={i}
                  onClick={() => void choose(i)}
                  className={`flex min-h-28 flex-col items-start gap-1 rounded-2xl p-3 text-left text-white active:scale-[0.98] ${OPTION_STYLE[i].bg}`}
                >
                  <span className="text-sm font-extrabold opacity-90">{OPTION_STYLE[i].letter}</span>
                  <span className="text-base font-semibold leading-snug"><ContentHtml html={o} /></span>
                </button>
              ))}
            </div>
          )}
          {sendErr && <p role="alert" className="text-center text-sm text-danger">{sendErr}</p>}
        </>
      )}

      {s.phase === "reveal" && (
        <>
          <div className={`rounded-2xl py-6 text-center ${myChoice === null ? "bg-surface-2" : s.my_correct ? "bg-emerald-600" : "bg-rose-600"}`}>
            <p className="text-3xl font-extrabold text-ink">
              {myChoice === null ? "Em chưa trả lời" : s.my_correct ? "Chính xác!" : "Chưa đúng"}
            </p>
            {s.my_correct && <p className="mt-1 font-mono text-xl font-bold text-ink">+{s.my_points} điểm</p>}
          </div>
          <div className="space-y-2 rounded-2xl bg-surface-2 p-4 text-sm text-ink">
            <p>
              Đáp án đúng: <b className="text-ink">{OPTION_STYLE[s.answer ?? 0].letter}</b>
              {" — "}
              <ContentHtml html={(s.options ?? [])[s.answer ?? 0] ?? ""} />
            </p>
            {s.explanation ? <div className="text-ink"><ContentHtml html={s.explanation} /></div> : null}
          </div>
          <Top top={s.top ?? []} me={s.nickname} />
          <p className="text-center text-sm text-muted">Chờ thầy/cô sang câu tiếp…</p>
        </>
      )}

      {s.phase === "finished" && (
        <>
          <div className="rounded-2xl bg-primary/20 py-8 text-center">
            <p className="text-sm text-ink">Kết thúc!</p>
            <p className="text-5xl font-extrabold text-ink">Hạng {s.rank}</p>
            <p className="mt-1 font-mono text-lg text-ink">{s.score} điểm</p>
          </div>
          <Top top={s.top ?? []} me={s.nickname} />
          <button onClick={onLeave} className="min-h-12 rounded-2xl bg-surface-2 font-bold text-ink">Chơi phòng khác</button>
        </>
      )}
    </div>
  );
}

function Top({ top, me }: { top: { id: number; nickname: string; score: number }[]; me: string }) {
  if (!top.length) return null;
  return (
    <ol className="space-y-1.5">
      {top.map((t, i) => (
        <li key={t.id} className={`flex items-center justify-between rounded-xl px-4 py-2.5 text-sm ${t.nickname === me ? "bg-primary/30 text-ink" : "bg-surface-2 text-ink"}`}>
          <span className="truncate"><b className="mr-2 font-mono">{i + 1}</b>{t.nickname}</span>
          <span className="font-mono tabular-nums">{t.score}</span>
        </li>
      ))}
    </ol>
  );
}

export default function QuizPlayer({ initialPin }: { initialPin: string }) {
  const [session, setSession] = useState<Session | null | undefined>(undefined);
  useEffect(() => {
    const t = setTimeout(() => setSession(loadSession()), 0);
    return () => clearTimeout(t);
  }, []);
  if (session === undefined) return null;
  return session ? (
    <Game
      session={session}
      onLeave={() => {
        saveSession(null);
        setSession(null);
      }}
    />
  ) : (
    <JoinForm initialPin={initialPin} onJoined={setSession} />
  );
}
