"use client";
import { useCallback, useEffect, useMemo, useState } from "react";
import { BarChart3, ChevronDown, CloudOff, Dumbbell, History, Play, Ruler, Trophy } from "lucide-react";
import { ROUTINES, RULES_TEXT, exerciseById, weeklySets, type Routine } from "@/lib/tap-luyen/chuong-trinh";
import {
  bestE1rmHistory, deleteWorkout, e1rm, fetchWorkouts, flushQueue, fmtKg, lastSetsOf, loadDraft, newId, pendingCount,
  saveDraft, saveWorkout, weekPlan, workoutStats, type Draft, type LoggedExercise, type Workout,
} from "@/lib/tap-luyen/store";
import WorkoutLogger from "./WorkoutLogger";
import SoDo from "./SoDo";
import { Card, LineChart, fmtDay, fmtDur, vn } from "./ui";

type Tab = "tap" | "lich-su" | "tien-bo" | "so-do";
const TABS: { key: Tab; label: string; icon: React.ReactNode }[] = [
  { key: "tap", label: "Tập", icon: <Dumbbell size={18} /> },
  { key: "lich-su", label: "Lịch sử", icon: <History size={18} /> },
  { key: "tien-bo", label: "Tiến bộ", icon: <BarChart3 size={18} /> },
  { key: "so-do", label: "Số đo", icon: <Ruler size={18} /> },
];

function buildDraft(r: Routine | null, history: Workout[]): Draft {
  const exercises: LoggedExercise[] = (r?.items ?? []).map((it) => {
    const meta = exerciseById(it.ex)!;
    const prev = lastSetsOf(history, it.ex).filter((s) => s.kind === "n");
    const hit = meta.track === "kg_reps" && prev.length >= it.sets && prev.slice(0, it.sets).every((s) => (s.reps ?? 0) >= it.hi);
    const kgOf = (k: number) => {
      const p = prev[k]?.kg ?? prev[prev.length - 1]?.kg ?? null;
      return p != null && hit ? p + (meta.step ?? 2.5) : p;
    };
    return {
      id: it.ex,
      name: meta.name,
      rest: it.rest,
      lo: it.lo,
      hi: it.hi,
      sets: [
        ...Array.from({ length: it.warmup ?? 0 }, () => ({ kind: "w" as const, kg: null, reps: null, sec: null, done: false })),
        ...Array.from({ length: it.sets }, (_, k) => ({ kind: "n" as const, kg: meta.track === "kg_reps" ? kgOf(k) : null, reps: null, sec: null, done: false })),
      ],
    };
  });
  return { client_id: newId(), routine_key: r?.key ?? null, title: r ? `Buổi ${r.name}` : "Buổi tự do", started_at: new Date().toISOString(), exercises };
}

export default function TapLuyenApp() {
  const [tab, setTab] = useState<Tab>(() => {
    const t = new URLSearchParams(window.location.search).get("tab");
    return TABS.some((x) => x.key === t) ? (t as Tab) : "tap";
  });
  const [draft, setDraft] = useState<Draft | null>(() => loadDraft());
  const [history, setHistory] = useState<Workout[]>([]);
  const [offline, setOffline] = useState(false);
  const [pending, setPending] = useState(0);
  const [loaded, setLoaded] = useState(false);
  const [summary, setSummary] = useState<{ w: Workout; prs: string[]; synced: boolean } | null>(null);
  // ?buoi=A (link "Mở ứng dụng tập" trong Lịch tuần) → mở sẵn buổi đó
  const [focus] = useState<string | null>(() => {
    const b = new URLSearchParams(window.location.search).get("buoi")?.toUpperCase() ?? "";
    return ["A", "B", "C"].includes(b) ? b : null;
  });

  const reload = useCallback(async () => {
    await flushQueue().catch(() => 0);
    const r = await fetchWorkouts();
    setHistory(r.list);
    setOffline(r.offline);
    setPending(pendingCount());
    setLoaded(true);
  }, []);

  useEffect(() => {
    flushQueue()
      .catch(() => 0)
      .then(fetchWorkouts)
      .then((r) => {
        setHistory(r.list);
        setOffline(r.offline);
        setPending(pendingCount());
        setLoaded(true);
      });
  }, []);

  const updateDraft = (d: Draft | null) => {
    setDraft(d);
    saveDraft(d);
  };

  const start = (r: Routine | null) => {
    if (draft && !confirm("Đang có buổi tập dở. Bỏ buổi đó và bắt đầu buổi mới?")) return;
    updateDraft(buildDraft(r, history));
    setSummary(null);
    setTab("tap");
    window.scrollTo({ top: 0 });
  };

  const finish = async (d: Draft) => {
    const w: Workout = {
      ...d,
      ended_at: new Date().toISOString(),
      exercises: d.exercises.map((e) => ({ ...e, sets: e.sets.filter((s) => s.done) })).filter((e) => e.sets.length),
    };
    const prs: string[] = [];
    for (const e of w.exercises) {
      const before = bestE1rmHistory(history, e.id).reduce((a, p) => Math.max(a, p.v), 0);
      let best = 0, top = "";
      for (const s of e.sets) if (s.kind === "n" && s.kg && s.reps && e1rm(s.kg, s.reps) > best) { best = e1rm(s.kg, s.reps); top = `${fmtKg(s.kg)} kg × ${s.reps}`; }
      if (best && before && best > before + 0.01) prs.push(`${e.name}: ${top}`);
    }
    const synced = await saveWorkout(w);
    updateDraft(null);
    setSummary({ w, prs, synced });
    window.scrollTo({ top: 0 });
    reload();
  };

  if (draft && tab === "tap")
    return (
      <>
        <TabBar tab={tab} setTab={setTab} live />
        <WorkoutLogger draft={draft} history={history} onChange={updateDraft} onFinish={finish} onDiscard={() => updateDraft(null)} />
      </>
    );

  return (
    <>
      <TabBar tab={tab} setTab={setTab} live={!!draft} />
      {(offline || pending > 0) && (
        <p className="mb-3 flex items-start gap-2 rounded-xl border border-warn/40 bg-warn/10 px-3 py-2 text-sm text-ink">
          <CloudOff size={16} className="mt-0.5 shrink-0 text-warn" />
          <span>
            {offline ? "Chưa kết nối được máy chủ (mất mạng hoặc bảng dữ liệu chưa tạo) — đang dùng bản lưu trên máy này." : ""}
            {pending > 0 ? ` ${pending} buổi chờ gửi, sẽ tự gửi lại lần mở sau.` : ""}
          </span>
        </p>
      )}
      {tab === "tap" && (
        <>
          {summary && <Summary {...summary} onClose={() => setSummary(null)} />}
          <StartTab history={history} loaded={loaded} focus={focus} onStart={start} />
        </>
      )}
      {tab === "lich-su" && <HistoryTab history={history} onDelete={async (id) => { await deleteWorkout(id).catch(() => alert("Chưa xoá được trên máy chủ.")); reload(); }} />}
      {tab === "tien-bo" && <ProgressTab history={history} />}
      {tab === "so-do" && <SoDo />}
    </>
  );
}

function TabBar({ tab, setTab, live }: { tab: Tab; setTab: (t: Tab) => void; live: boolean }) {
  return (
    <nav className="mb-4 grid grid-cols-4 gap-1 rounded-2xl border border-line bg-panel p-1" aria-label="Mục ứng dụng tập">
      {TABS.map((t) => (
        <button
          key={t.key}
          type="button"
          aria-current={tab === t.key ? "page" : undefined}
          onClick={() => setTab(t.key)}
          className={`relative flex min-h-12 flex-col items-center justify-center gap-0.5 rounded-xl text-xs font-semibold ${tab === t.key ? "bg-primary text-white" : "text-muted hover:bg-surface-2"}`}
        >
          {t.icon}
          {t.label}
          {t.key === "tap" && live && tab !== "tap" && <span className="absolute right-3 top-2 h-2 w-2 rounded-full bg-ok" aria-label="đang có buổi tập" />}
        </button>
      ))}
    </nav>
  );
}

function StartTab({ history, loaded, focus, onStart }: { history: Workout[]; loaded: boolean; focus: string | null; onStart: (r: Routine | null) => void }) {
  const [open, setOpen] = useState<string | null>(focus);
  const { count: weekCount, done: doneKeys, next, lastOf } = weekPlan(history, ROUTINES.map((r) => r.key), focus);

  return (
    <div className="space-y-3">
      <Card>
        <p className="text-sm text-muted">Tuần này</p>
        <p className="text-2xl font-bold text-ink">
          {weekCount}/3 buổi <span className="text-base font-semibold text-muted">· {ROUTINES.map((r) => (doneKeys.has(r.key) ? `${r.key} ✓` : r.key)).join("  ")}</span>
        </p>
        {loaded && history.length === 0 && <p className="mt-1 text-sm text-muted">Chưa có buổi nào. Buổi đầu: nhập tạ vừa sức, cột “Lần trước” sẽ tự có từ buổi sau.</p>}
      </Card>

      {ROUTINES.map((r) => {
        const last = lastOf(r.key);
        const isOpen = open === r.key;
        return (
          <Card key={r.key} className={r.key === next ? "ring-2 ring-primary" : ""}>
            <div className="flex items-start gap-3">
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-primary-soft text-lg font-black text-primary">{r.key}</span>
              <div className="min-w-0 flex-1">
                <p className="font-bold text-ink">{r.name.replace(/^[ABC] · /, "")}</p>
                <p className="text-xs text-muted">
                  {r.items.length} bài · {r.items.reduce((a, i) => a + i.sets, 0)} hiệp · {last ? `lần trước ${fmtDay(last.started_at)}` : "chưa tập"}
                  {r.key === next && <span className="font-semibold text-primary"> · nên tập tiếp</span>}
                </p>
              </div>
            </div>
            <button type="button" onClick={() => setOpen(isOpen ? null : r.key)} className="mt-2 flex min-h-11 items-center gap-1 text-sm font-semibold text-primary" aria-expanded={isOpen}>
              <ChevronDown size={16} className={isOpen ? "rotate-180" : ""} /> {isOpen ? "Ẩn bài tập" : "Xem bài tập"}
            </button>
            {isOpen && (
              <div className="mb-2">
                <p className="text-sm text-ink">{r.focus}</p>
                <p className="mt-1 text-xs text-muted">{r.when}</p>
                <ol className="mt-2 divide-y divide-line rounded-xl bg-surface-2 text-sm">
                  {r.items.map((it) => {
                    const m = exerciseById(it.ex)!;
                    const p = lastSetsOf(history, it.ex).filter((s) => s.kind === "n")[0];
                    return (
                      <li key={it.ex} className="flex items-baseline gap-2 px-3 py-2">
                        <span className="min-w-0 flex-1 text-ink">{m.name}</span>
                        <span className="shrink-0 tabular-nums text-muted">
                          {it.sets}×{it.lo === it.hi ? it.lo : `${it.lo}–${it.hi}`}{m.track === "time" ? "″" : ""}
                          {p?.kg != null && <> · {fmtKg(p.kg)} kg</>}
                        </span>
                      </li>
                    );
                  })}
                </ol>
              </div>
            )}
            <button type="button" onClick={() => onStart(r)} className="flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-bold text-white">
              <Play size={16} /> Bắt đầu buổi {r.key}
            </button>
          </Card>
        );
      })}

      <button type="button" onClick={() => onStart(null)} className="min-h-12 w-full rounded-xl border border-line-strong text-sm font-bold text-ink">
        Buổi tự do (tự chọn bài)
      </button>

      <details className="rounded-2xl border border-line bg-panel p-4">
        <summary className="min-h-8 cursor-pointer font-bold text-ink">Nguyên tắc chương trình · số hiệp/tuần</summary>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink">
          {RULES_TEXT.map((t) => <li key={t}>{t}</li>)}
        </ul>
        <p className="mt-3 text-sm font-semibold text-ink">Hiệp làm việc mỗi tuần (A+B+C)</p>
        <p className="text-sm text-muted">{weeklySets().map(([g, n]) => `${g} ${n}`).join(" · ")}</p>
      </details>
    </div>
  );
}

function Summary({ w, prs, synced, onClose }: { w: Workout; prs: string[]; synced: boolean; onClose: () => void }) {
  const st = workoutStats(w);
  const min = (new Date(w.ended_at).getTime() - new Date(w.started_at).getTime()) / 60000;
  return (
    <Card className="mb-3 border-ok/50">
      <p className="text-lg font-bold text-ink">Xong buổi! 💪</p>
      <p className="text-sm text-muted">{w.title}</p>
      <dl className="mt-2 grid grid-cols-3 gap-2 text-center">
        <div className="rounded-xl bg-surface-2 py-2"><dt className="text-xs text-muted">Thời gian</dt><dd className="font-bold text-ink">{fmtDur(min)}</dd></div>
        <div className="rounded-xl bg-surface-2 py-2"><dt className="text-xs text-muted">Khối lượng</dt><dd className="font-bold text-ink">{vn(st.volume, 0)} kg</dd></div>
        <div className="rounded-xl bg-surface-2 py-2"><dt className="text-xs text-muted">Hiệp</dt><dd className="font-bold text-ink">{st.sets}</dd></div>
      </dl>
      {prs.length > 0 && (
        <div className="mt-3">
          <p className="flex items-center gap-1.5 text-sm font-bold text-accent"><Trophy size={16} /> Kỷ lục mới (1RM ước lượng)</p>
          <ul className="mt-1 text-sm text-ink">{prs.map((p) => <li key={p}>• {p}</li>)}</ul>
        </div>
      )}
      {!synced && <p className="mt-2 text-sm text-warn">Chưa gửi được lên máy chủ — đã lưu trên máy này, sẽ tự gửi lại.</p>}
      <button type="button" onClick={onClose} className="mt-3 min-h-11 w-full rounded-xl bg-surface-2 text-sm font-semibold text-ink">Đóng</button>
    </Card>
  );
}

function HistoryTab({ history, onDelete }: { history: Workout[]; onDelete: (id: string) => void }) {
  const [open, setOpen] = useState<string | null>(null);
  if (!history.length) return <Card><p className="text-sm text-muted">Chưa có buổi tập nào.</p></Card>;
  return (
    <ul className="space-y-2">
      {history.map((w) => {
        const st = workoutStats(w);
        const min = (new Date(w.ended_at).getTime() - new Date(w.started_at).getTime()) / 60000;
        const isOpen = open === w.client_id;
        return (
          <li key={w.client_id} className="rounded-2xl border border-line bg-panel">
            <button type="button" onClick={() => setOpen(isOpen ? null : w.client_id)} className="w-full p-4 text-left" aria-expanded={isOpen}>
              <p className="flex items-baseline gap-2">
                <span className="min-w-0 flex-1 truncate font-bold text-ink">{w.title.replace(/^Buổi /, "")}</span>
                <span className="shrink-0 text-sm text-muted">{fmtDay(w.started_at)}</span>
              </p>
              <p className="text-xs text-muted">{fmtDur(min)} · {vn(st.volume, 0)} kg · {st.sets} hiệp</p>
              {!isOpen && <p className="mt-1 line-clamp-2 text-sm text-ink">{w.exercises.map((e) => `${e.sets.filter((s) => s.kind === "n").length}× ${e.name}`).join(" · ")}</p>}
            </button>
            {isOpen && (
              <div className="border-t border-line px-4 pb-4 pt-2">
                {w.exercises.map((e, i) => (
                  <div key={i} className="py-1.5">
                    <p className="text-sm font-semibold text-primary">{e.name}</p>
                    {e.note && <p className="text-xs italic text-muted">{e.note}</p>}
                    <p className="text-sm tabular-nums text-ink">
                      {e.sets.map((s) => (s.sec != null ? `${s.sec}″` : s.kg != null ? `${fmtKg(s.kg)}×${s.reps ?? "–"}` : `${s.reps ?? "–"} lần`) + (s.kind === "w" ? " (K)" : "")).join(" · ")}
                    </p>
                  </div>
                ))}
                <button type="button" onClick={() => confirm("Xoá hẳn buổi tập này?") && onDelete(w.client_id)} className="mt-2 min-h-11 text-sm font-semibold text-danger">Xoá buổi này</button>
              </div>
            )}
          </li>
        );
      })}
    </ul>
  );
}

function ProgressTab({ history }: { history: Workout[] }) {
  const exIds = useMemo(() => {
    const m = new Map<string, number>();
    for (const w of history) for (const e of w.exercises) if (e.sets.some((s) => s.kg && s.reps)) m.set(e.id, (m.get(e.id) ?? 0) + 1);
    // bài trọng tâm ngực–vai lên trước
    const order = ["chest_press_machine", "incline_db_press", "shoulder_press_machine", "lateral_raise_db", "lat_pulldown"];
    return [...m.keys()].sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99));
  }, [history]);
  const [sel, setSel] = useState<string>("");
  const cur = sel || exIds[0] || "";
  const pts = useMemo(() => (cur ? bestE1rmHistory(history, cur) : []), [history, cur]);

  // số hiệp làm việc 7 ngày qua theo nhóm cơ
  const [since] = useState(() => Date.now() - 7 * 864e5);
  const groupSets = new Map<string, number>();
  for (const w of history) if (new Date(w.started_at).getTime() >= since) for (const e of w.exercises) {
    const g = exerciseById(e.id)?.group ?? "Khác";
    groupSets.set(g, (groupSets.get(g) ?? 0) + e.sets.filter((s) => s.kind === "n" && s.done).length);
  }
  const plan = new Map(weeklySets());

  return (
    <div className="space-y-3">
      <Card>
        <p className="font-bold text-ink">Hiệp làm việc 7 ngày qua</p>
        <ul className="mt-2 space-y-2">
          {["Ngực", "Vai", "Lưng", "Chân", "Mông", "Sức bật", "Core"].map((g) => {
            const done = groupSets.get(g) ?? 0, goal = plan.get(g) ?? 0;
            return (
              <li key={g} className="grid grid-cols-[4.5rem_1fr_3.5rem] items-center gap-2 text-sm">
                <span className="text-ink">{g}</span>
                <span className="h-2.5 overflow-hidden rounded-full bg-surface-2">
                  <span className={`block h-full rounded-full ${g === "Ngực" || g === "Vai" ? "bg-primary" : "bg-slate-500"}`} style={{ width: `${goal ? Math.min(100, (done / goal) * 100) : 0}%` }} />
                </span>
                <span className="text-right tabular-nums text-muted">{done}/{goal}</span>
              </li>
            );
          })}
        </ul>
      </Card>
      <Card>
        <p className="font-bold text-ink">Sức mạnh từng bài</p>
        {exIds.length === 0 ? (
          <p className="mt-1 text-sm text-muted">Tập vài buổi có ghi kg sẽ thấy đường tiến bộ ở đây.</p>
        ) : (
          <>
            <select value={cur} onChange={(e) => setSel(e.target.value)} className="mt-2 h-11 w-full rounded-xl border border-line bg-surface-2 px-3 text-base text-ink" aria-label="Chọn bài tập">
              {exIds.map((id) => <option key={id} value={id}>{exerciseById(id)?.name ?? id}</option>)}
            </select>
            <p className="mt-2 text-xs text-muted">1RM ước lượng (Epley) từ hiệp tốt nhất mỗi buổi</p>
            <LineChart points={pts.map((p) => ({ x: p.date, y: p.v }))} unit="kg" />
            <ul className="mt-2 divide-y divide-line text-sm">
              {[...pts].reverse().slice(0, 8).map((p, i) => (
                <li key={i} className="flex justify-between py-1.5"><span className="text-muted">{fmtDay(p.date)}</span><span className="tabular-nums text-ink">{p.top} · ≈{vn(p.v)} kg</span></li>
              ))}
            </ul>
          </>
        )}
      </Card>
    </div>
  );
}
