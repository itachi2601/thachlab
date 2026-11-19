"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { ArrowDown, ArrowUp, Check, MoreVertical, Plus, Repeat2, Timer, Trash2, TrendingUp, X } from "lucide-react";
import { exerciseById, type Exercise } from "@/lib/tap-luyen/chuong-trinh";
import { lastSetsOf, workoutStats, fmtKg, type Draft, type LoggedExercise, type LoggedSet, type Workout } from "@/lib/tap-luyen/store";
import { NumInput, fmtClock, vn } from "./ui";

type Props = {
  draft: Draft;
  history: Workout[];
  /** danh sách bài cho "Thêm bài" (theo chương trình của người dùng) */
  exercises: Exercise[];
  onChange: (d: Draft) => void;
  onFinish: (d: Draft) => void;
  onDiscard: () => void;
};

const blankSet = (kind: LoggedSet["kind"] = "n", from?: LoggedSet): LoggedSet => ({ kind, kg: from?.kg ?? null, reps: null, sec: null, done: false });

function beep() {
  try {
    navigator.vibrate?.([250, 120, 250]);
    const Ctx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ctx = new Ctx();
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.value = 880;
    g.gain.setValueAtTime(0.25, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
    o.connect(g).connect(ctx.destination);
    o.start();
    o.stop(ctx.currentTime + 0.5);
  } catch {
    /* trình duyệt chặn âm thanh */
  }
}

export default function WorkoutLogger({ draft, history, exercises, onChange, onFinish, onDiscard }: Props) {
  const [now, setNow] = useState(() => Date.now());
  const [rest, setRest] = useState<{ endsAt: number; total: number } | null>(null);
  const [picker, setPicker] = useState<{ mode: "add" } | { mode: "replace"; idx: number } | null>(null);
  const [menu, setMenu] = useState<number | null>(null);
  const beeped = useRef(false);

  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);
  const restLeft = rest ? (rest.endsAt - now) / 1000 : 0;
  useEffect(() => {
    if (rest && restLeft <= 0 && !beeped.current) {
      beeped.current = true;
      beep();
      const t = setTimeout(() => setRest(null), 2500);
      return () => clearTimeout(t);
    }
  }, [rest, restLeft]);

  const elapsed = (now - new Date(draft.started_at).getTime()) / 1000;
  const stats = workoutStats(draft);
  const totalSets = draft.exercises.reduce((a, e) => a + e.sets.filter((s) => s.kind === "n").length, 0);

  const setEx = (i: number, e: LoggedExercise | null) => {
    const ex = [...draft.exercises];
    if (e) ex[i] = e;
    else ex.splice(i, 1);
    onChange({ ...draft, exercises: ex });
  };
  const move = (i: number, d: -1 | 1) => {
    const j = i + d;
    if (j < 0 || j >= draft.exercises.length) return;
    const ex = [...draft.exercises];
    [ex[i], ex[j]] = [ex[j], ex[i]];
    onChange({ ...draft, exercises: ex });
  };

  const tick = (i: number, si: number) => {
    const e = draft.exercises[i];
    const meta = exerciseById(e.id);
    const s = e.sets[si];
    const prev = prevFor(history, e, si, draft.started_at);
    const nextDone = !s.done;
    const filled: LoggedSet = { ...s, done: nextDone };
    if (nextDone) {
      if (meta?.track === "time") filled.sec = s.sec ?? prev?.sec ?? e.lo ?? null;
      else {
        filled.reps = s.reps ?? prev?.reps ?? e.lo ?? null;
        if (meta?.track !== "reps") filled.kg = s.kg ?? prev?.kg ?? null;
      }
    }
    const sets = [...e.sets];
    sets[si] = filled;
    // tạ của hiệp sau chưa nhập → lấy theo hiệp vừa xong
    if (nextDone && filled.kg != null) for (let k = si + 1; k < sets.length; k++) if (sets[k].kind === filled.kind && sets[k].kg == null && !sets[k].done) sets[k] = { ...sets[k], kg: filled.kg };
    setEx(i, { ...e, sets });
    if (nextDone) {
      const secs = s.kind === "w" ? 45 : e.rest;
      beeped.current = false;
      setRest({ endsAt: now + secs * 1000, total: secs }); // `now` (đồng hồ 1 giây) cùng gốc với ô đếm ngược
    }
  };

  const finish = () => {
    const undone = draft.exercises.reduce((a, e) => a + e.sets.filter((s) => !s.done).length, 0);
    if (stats.sets === 0) {
      if (confirm("Chưa tick hiệp nào. Bỏ buổi tập này?")) onDiscard();
      return;
    }
    if (undone && !confirm(`Còn ${undone} hiệp chưa tick — các hiệp đó sẽ bị bỏ. Kết thúc buổi?`)) return;
    onFinish(draft);
  };

  return (
    <div className="pb-28">
      {/* thanh trên cố định */}
      <div className="sticky top-[68px] lg:top-[76px] z-20 -mx-4 mb-3 border-b border-line bg-panel-deep/95 px-4 py-2 backdrop-blur">
        <div className="flex items-center gap-2">
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-bold text-ink">{draft.title}</p>
            <p className="text-xs tabular-nums text-muted">
              {fmtClock(elapsed)}{stats.volume > 0 ? ` · ${vn(stats.volume, 0)} kg` : ""} · {stats.sets}/{totalSets} hiệp
            </p>
          </div>
          <button type="button" onClick={finish} className="min-h-11 rounded-xl bg-ok px-4 text-sm font-bold text-white">
            Kết thúc
          </button>
        </div>
      </div>

      <ol className="space-y-3">
        {draft.exercises.map((e, i) => (
          <ExerciseCard
            key={`${e.id}-${i}`}
            e={e}
            history={history}
            startedAt={draft.started_at}
            menuOpen={menu === i}
            onMenu={() => setMenu(menu === i ? null : i)}
            onChange={(ne) => setEx(i, ne)}
            onTick={(si) => tick(i, si)}
            onRemove={() => { setMenu(null); if (confirm(`Bỏ bài "${e.name}"?`)) setEx(i, null); }}
            onReplace={() => { setMenu(null); setPicker({ mode: "replace", idx: i }); }}
            onUp={() => { setMenu(null); move(i, -1); }}
            onDown={() => { setMenu(null); move(i, 1); }}
          />
        ))}
      </ol>

      <button type="button" onClick={() => setPicker({ mode: "add" })} className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl border border-dashed border-line-strong text-sm font-bold text-primary">
        <Plus size={18} /> Thêm bài tập
      </button>
      <button type="button" onClick={() => confirm("Huỷ buổi tập? Mọi hiệp đã ghi trong buổi này sẽ mất.") && onDiscard()} className="mt-2 min-h-11 w-full rounded-xl text-sm font-semibold text-danger">
        Huỷ buổi tập
      </button>

      {rest && (
        <div className="fixed inset-x-0 bottom-0 z-50 border-t border-line bg-panel-deep px-4 pb-[max(env(safe-area-inset-bottom),12px)] pt-2 shadow-[0_-4px_20px_rgba(0,0,0,.12)]">
          <div className="mx-auto max-w-xl">
            <div className="mb-2 h-1.5 overflow-hidden rounded-full bg-surface-2">
              <div className="h-full bg-primary transition-[width] duration-1000 ease-linear" style={{ width: `${Math.max(0, (restLeft / rest.total) * 100)}%` }} />
            </div>
            <div className="flex items-center gap-2">
              <Timer size={18} className="text-primary" />
              <span className={`flex-1 text-2xl font-bold tabular-nums ${restLeft <= 0 ? "text-ok" : "text-ink"}`}>{restLeft <= 0 ? "Hết nghỉ!" : fmtClock(restLeft)}</span>
              <button type="button" onClick={() => setRest({ ...rest, endsAt: rest.endsAt - 15000 })} className="min-h-11 rounded-lg bg-surface-2 px-3 text-sm font-semibold text-ink">−15</button>
              <button type="button" onClick={() => setRest({ ...rest, endsAt: rest.endsAt + 15000, total: rest.total + 15 })} className="min-h-11 rounded-lg bg-surface-2 px-3 text-sm font-semibold text-ink">+15</button>
              <button type="button" onClick={() => setRest(null)} className="min-h-11 rounded-lg bg-primary px-3 text-sm font-bold text-white">Bỏ qua</button>
            </div>
          </div>
        </div>
      )}

      {picker && (
        <ExercisePicker
          exercises={exercises}
          onClose={() => setPicker(null)}
          onPick={(x) => {
            const prev = lastSetsOf(history, x.id).filter((s) => s.kind === "n");
            const le: LoggedExercise = { id: x.id, name: x.name, rest: 90, lo: x.track === "time" ? 20 : 8, hi: x.track === "time" ? 30 : 12, sets: [0, 1, 2].map((k) => blankSet("n", prev[k])) };
            if (picker.mode === "add") onChange({ ...draft, exercises: [...draft.exercises, le] });
            else {
              const old = draft.exercises[picker.idx];
              setEx(picker.idx, { ...le, rest: old.rest, lo: old.lo, hi: old.hi, sets: old.sets.map((s, k) => ({ ...blankSet(s.kind, s.kind === "n" ? prev[k] : undefined) })) });
            }
            setPicker(null);
          }}
        />
      )}
    </div>
  );
}

function prevFor(history: Workout[], e: LoggedExercise, si: number, before: string) {
  const s = e.sets[si];
  const idx = e.sets.slice(0, si).filter((x) => x.kind === s.kind).length;
  return lastSetsOf(history, e.id, before).filter((x) => x.kind === s.kind)[idx];
}

function ExerciseCard({
  e, history, startedAt, menuOpen, onMenu, onChange, onTick, onRemove, onReplace, onUp, onDown,
}: {
  e: LoggedExercise; history: Workout[]; startedAt: string; menuOpen: boolean;
  onMenu: () => void; onChange: (e: LoggedExercise) => void; onTick: (si: number) => void;
  onRemove: () => void; onReplace: () => void; onUp: () => void; onDown: () => void;
}) {
  const meta = exerciseById(e.id);
  const track = meta?.track ?? "kg_reps";
  const prevWork = useMemo(() => lastSetsOf(history, e.id, startedAt).filter((s) => s.kind === "n"), [history, e.id, startedAt]);
  const workCount = e.sets.filter((s) => s.kind === "n").length;
  const hit = e.hi != null && prevWork.length >= workCount && workCount > 0 && prevWork.slice(0, workCount).every((s) => (track === "time" ? (s.sec ?? 0) : (s.reps ?? 0)) >= (e.hi ?? 0));
  const target = e.lo != null ? (e.lo === e.hi ? `${e.lo}` : `${e.lo}–${e.hi}`) + (track === "time" ? " giây" : " lần") : "";
  const setsCopy = (fn: (s: LoggedSet[]) => LoggedSet[]) => onChange({ ...e, sets: fn([...e.sets]) });
  let workIdx = 0;
  const warmIdxRef = { n: 0 };

  return (
    <li className="rounded-2xl border border-line bg-panel p-3">
      <div className="flex items-start gap-2">
        <div className="min-w-0 flex-1">
          <p className="font-bold leading-snug text-primary">{e.name}</p>
          <p className="text-xs text-muted">
            {target && <>Mục tiêu {target} · </>}nghỉ {fmtClock(e.rest)}
          </p>
        </div>
        <div className="relative">
          <button type="button" aria-label="Tuỳ chọn bài tập" onClick={onMenu} className="grid h-11 w-11 place-items-center rounded-lg text-muted hover:bg-surface-2">
            <MoreVertical size={18} />
          </button>
          {menuOpen && (
            <div className="absolute right-0 top-11 z-10 w-48 overflow-hidden rounded-xl border border-line bg-panel shadow-lg">
              <MenuBtn icon={<Repeat2 size={16} />} onClick={onReplace}>Thay bài khác</MenuBtn>
              <MenuBtn icon={<ArrowUp size={16} />} onClick={onUp}>Đưa lên</MenuBtn>
              <MenuBtn icon={<ArrowDown size={16} />} onClick={onDown}>Đưa xuống</MenuBtn>
              <MenuBtn icon={<Trash2 size={16} />} onClick={onRemove} danger>Bỏ bài này</MenuBtn>
            </div>
          )}
        </div>
      </div>
      {meta?.cue && <p className="mt-1 text-xs leading-relaxed text-muted">{meta.cue}</p>}
      {hit && track !== "reps" && (
        <p className="mt-2 flex items-center gap-1.5 rounded-lg bg-primary-soft px-2 py-1.5 text-xs font-semibold text-primary">
          <TrendingUp size={14} />
          {track === "time" ? `Lần trước đủ giây mọi hiệp → ${meta?.harder ?? "giữ lâu hơn 5–10 giây."}` : `Lần trước chạm ${e.hi} lần mọi hiệp → tăng ${fmtKg(meta?.step ?? 2.5)} kg, quay về ${e.lo} lần.`}
        </p>
      )}
      {hit && track === "reps" && <p className="mt-2 rounded-lg bg-primary-soft px-2 py-1.5 text-xs font-semibold text-primary">Lần trước đủ lần mọi hiệp → {meta?.harder ?? "làm khó hơn (bớt hỗ trợ, nhảy cao hơn)."}</p>}

      <input
        value={e.note ?? ""}
        onChange={(ev) => onChange({ ...e, note: ev.target.value })}
        placeholder="Ghi chú (ghế số mấy, cảm giác…)"
        aria-label="Ghi chú bài tập"
        className="mt-2 w-full rounded-lg border border-transparent bg-transparent px-1 py-1 text-sm text-ink placeholder:text-slate-500 focus:border-line focus:outline-none"
      />

      <div className="mt-1 grid grid-cols-[2.25rem_minmax(0,1fr)_minmax(0,4.5rem)_minmax(0,4.5rem)_2.75rem] items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wide text-muted">
        <span className="text-center">Hiệp</span>
        <span>Lần trước</span>
        <span className="text-center">{track === "kg_reps" ? "kg" : ""}</span>
        <span className="text-center">{track === "time" ? "giây" : "lần"}</span>
        <span className="text-center"><Check size={14} className="mx-auto" /></span>
      </div>
      <ul className="mt-1 space-y-1">
        {e.sets.map((s, si) => {
          const label = s.kind === "w" ? "K" : String(++workIdx);
          const kindIdx = s.kind === "w" ? warmIdxRef.n++ : workIdx - 1;
          const prev = lastSetsOf(history, e.id, startedAt).filter((x) => x.kind === s.kind)[kindIdx];
          const prevTxt = prev ? (track === "time" ? `${prev.sec ?? "–"} giây` : track === "reps" ? `${prev.reps ?? "–"} lần` : `${prev.kg != null ? fmtKg(prev.kg) : "–"} × ${prev.reps ?? "–"}`) : "—";
          const upd = (p: Partial<LoggedSet>) => setsCopy((a) => { a[si] = { ...a[si], ...p }; return a; });
          return (
            <li key={si} className={`grid grid-cols-[2.25rem_minmax(0,1fr)_minmax(0,4.5rem)_minmax(0,4.5rem)_2.75rem] items-center gap-1.5 rounded-lg ${s.done ? "bg-ok/10" : ""}`}>
              <button
                type="button"
                title="Bấm để đổi hiệp khởi động / làm việc"
                onClick={() => upd({ kind: s.kind === "w" ? "n" : "w" })}
                className={`h-11 rounded-lg text-sm font-bold ${s.kind === "w" ? "text-warn" : "text-ink"}`}
              >
                {label}
              </button>
              <span className="truncate text-sm tabular-nums text-muted">{prevTxt}</span>
              {track === "kg_reps" ? (
                <NumInput label={`kg hiệp ${label}`} value={s.kg} placeholder={prev?.kg != null ? fmtKg(prev.kg) : "kg"} onChange={(n) => upd({ kg: n })} />
              ) : (
                <span />
              )}
              {track === "time" ? (
                <NumInput label={`giây hiệp ${label}`} value={s.sec} placeholder={String(prev?.sec ?? e.lo ?? "")} onChange={(n) => upd({ sec: n })} />
              ) : (
                <NumInput label={`số lần hiệp ${label}`} value={s.reps} placeholder={String(prev?.reps ?? e.lo ?? "")} onChange={(n) => upd({ reps: n })} />
              )}
              <button
                type="button"
                aria-label={s.done ? `Bỏ tick hiệp ${label}` : `Tick xong hiệp ${label}`}
                aria-pressed={s.done}
                onClick={() => onTick(si)}
                className={`grid h-11 w-11 place-items-center rounded-lg border ${s.done ? "border-ok bg-ok text-white" : "border-line-strong text-muted"}`}
              >
                <Check size={18} />
              </button>
            </li>
          );
        })}
      </ul>
      <div className="mt-2 flex gap-2">
        <button
          type="button"
          onClick={() => setsCopy((a) => { const last = [...a].reverse().find((x) => x.kind === "n"); return [...a, blankSet("n", last)]; })}
          className="min-h-11 flex-1 rounded-lg bg-surface-2 text-sm font-semibold text-ink"
        >
          + Thêm hiệp
        </button>
        {e.sets.length > 0 && (
          <button type="button" aria-label="Xoá hiệp cuối" onClick={() => setsCopy((a) => a.slice(0, -1))} className="grid min-h-11 w-11 place-items-center rounded-lg bg-surface-2 text-muted">
            <X size={16} />
          </button>
        )}
      </div>
    </li>
  );
}

function MenuBtn({ icon, children, onClick, danger }: { icon: React.ReactNode; children: React.ReactNode; onClick: () => void; danger?: boolean }) {
  return (
    <button type="button" onClick={onClick} className={`flex min-h-11 w-full items-center gap-2 px-3 text-left text-sm font-semibold hover:bg-surface-2 ${danger ? "text-danger" : "text-ink"}`}>
      {icon}
      {children}
    </button>
  );
}

function ExercisePicker({ exercises, onPick, onClose }: { exercises: Exercise[]; onPick: (x: Exercise) => void; onClose: () => void }) {
  const [q, setQ] = useState("");
  const groups = useMemo(() => {
    const k = q.trim().toLowerCase();
    const m = new Map<string, Exercise[]>();
    for (const x of exercises) if (!k || x.name.toLowerCase().includes(k) || x.group.toLowerCase().includes(k)) m.set(x.group, [...(m.get(x.group) ?? []), x]);
    return [...m.entries()];
  }, [q, exercises]);
  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-bg" role="dialog" aria-modal="true" aria-label="Chọn bài tập">
      <div className="flex items-center gap-2 border-b border-line bg-panel-deep px-4 py-2">
        <input autoFocus value={q} onChange={(e) => setQ(e.target.value)} placeholder="Tìm bài: ngực, vai, kéo…" className="h-11 flex-1 rounded-xl border border-line bg-surface-2 px-3 text-base text-ink focus:border-primary focus:outline-none" />
        <button type="button" onClick={onClose} className="min-h-11 px-2 text-sm font-semibold text-primary">Đóng</button>
      </div>
      <div className="flex-1 overflow-y-auto px-4 pb-8">
        {groups.map(([g, list]) => (
          <div key={g} className="mt-3">
            <p className="mb-1 text-xs font-bold uppercase tracking-wide text-muted">{g}</p>
            <ul className="overflow-hidden rounded-xl border border-line bg-panel">
              {list.map((x) => (
                <li key={x.id} className="border-b border-line last:border-0">
                  <button type="button" onClick={() => onPick(x)} className="min-h-12 w-full px-3 text-left text-sm font-semibold text-ink hover:bg-surface-2">{x.name}</button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
