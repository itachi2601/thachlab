"use client";
import { useCallback, useEffect, useMemo, useState } from "react";
import { BarChart3, ChevronDown, CloudOff, Dumbbell, History, Lock, Play, Ruler, Trophy } from "lucide-react";
import { exerciseById, programFor, weeklySets, type Program, type Routine } from "@/lib/tap-luyen/chuong-trinh";
import { useAuth } from "@/components/auth/AuthProvider";
import {
  bestCountHistory, bestE1rmHistory, deleteWorkout, e1rm, fetchWorkouts, flushQueue, fmtKg, lastSetsOf, loadDraft, newId, pendingCount,
  isLocalOnly, saveDraft, saveWorkout, setTapLuyenUser, weekPlan, workoutStats, type Draft, type LoggedExercise, type Workout,
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

/** Ba điều học sinh cần biết trước buổi đầu (rút từ RULES_TEXT_HS, bản đầy đủ ở hộp "Tập an toàn" cuối tab). */
const FIRST_SESSION_SAFETY = [
  "Khởi động 5 phút: xoay cổ, vai, hông, gối, cổ chân; đi bộ nhanh tại chỗ.",
  "Động tác bắt đầu sai thì dừng hiệp, không cố thêm lần.",
  "Đau nhói ở khớp, chóng mặt, tức ngực hay khó thở bất thường: dừng ngay và báo người lớn.",
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

/** Kỷ lục cá nhân của buổi vừa xong: bài có tạ so 1RM ước lượng, bài không tạ so số lần / số giây tốt nhất. */
function personalBests(w: Workout, history: Workout[]) {
  const out: string[] = [];
  for (const e of w.exercises) {
    const work = e.sets.filter((s) => s.kind === "n");
    if (work.some((s) => s.kg && s.reps)) {
      const before = bestE1rmHistory(history, e.id).reduce((a, p) => Math.max(a, p.v), 0);
      let best = 0, top = "";
      for (const s of work) if (s.kg && s.reps && e1rm(s.kg, s.reps) > best) { best = e1rm(s.kg, s.reps); top = `${fmtKg(s.kg)} kg × ${s.reps}`; }
      if (best && before && best > before + 0.01) out.push(`${e.name}: ${top}`);
    } else {
      const before = bestCountHistory(history, e.id).reduce((a, p) => Math.max(a, p.v), 0);
      const best = Math.max(0, ...work.map((s) => s.sec ?? s.reps ?? 0));
      const unit = work.some((s) => s.sec != null) ? "giây" : "lần";
      if (best && before && best > before) out.push(`${e.name}: ${best} ${unit}`);
    }
  }
  return out;
}

export default function TapLuyenApp() {
  const { profile } = useAuth();
  const program = programFor(profile?.role);
  // phải chạy trước loadDraft() bên dưới: dữ liệu trên máy tách theo tài khoản
  if (profile?.id) setTapLuyenUser(profile.id, program.kind === "thay");
  const tabs = program.measurements ? TABS : TABS.filter((t) => t.key !== "so-do");
  const [tab, setTab] = useState<Tab>(() => {
    const t = new URLSearchParams(window.location.search).get("tab");
    return tabs.some((x) => x.key === t) ? (t as Tab) : "tap";
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
    return program.routines.some((r) => r.key === b) ? b : null;
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
    const prs = personalBests(w, history);
    const synced = await saveWorkout(w);
    updateDraft(null);
    setSummary({ w, prs, synced });
    window.scrollTo({ top: 0 });
    reload();
  };

  if (draft && tab === "tap")
    return (
      <>
        <TabBar tabs={tabs} tab={tab} setTab={setTab} live />
        <WorkoutLogger draft={draft} history={history} exercises={program.exercises} onChange={updateDraft} onFinish={finish} onDiscard={() => updateDraft(null)} />
      </>
    );

  return (
    <>
      <TabBar tabs={tabs} tab={tab} setTab={setTab} live={!!draft} />
      {isLocalOnly() && (
        <p className="mb-3 flex items-start gap-2 rounded-xl border border-ok/40 px-3 py-2 text-sm text-ink">
          <Lock size={16} className="mt-0.5 shrink-0 text-ok" />
          <span><b>Không thu thập dữ liệu của em.</b> Các buổi tập chỉ lưu trên trình duyệt của máy này, không gửi lên máy chủ, thầy cô không xem được. Đổi máy hoặc xoá dữ liệu trình duyệt thì lịch sử mất.</span>
        </p>
      )}
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
          <StartTab program={program} history={history} loaded={loaded} focus={focus} onStart={start} />
        </>
      )}
      {tab === "lich-su" && <HistoryTab history={history} onDelete={async (id) => { await deleteWorkout(id).catch(() => alert("Chưa xoá được trên máy chủ.")); reload(); }} />}
      {tab === "tien-bo" && <ProgressTab program={program} history={history} />}
      {tab === "so-do" && program.measurements && <SoDo />}
    </>
  );
}

function TabBar({ tabs, tab, setTab, live }: { tabs: typeof TABS; tab: Tab; setTab: (t: Tab) => void; live: boolean }) {
  return (
    <nav className={`mb-4 grid gap-1 rounded-2xl border border-line bg-panel p-1 ${tabs.length === 4 ? "grid-cols-4" : "grid-cols-3"}`} aria-label="Mục ứng dụng tập">
      {tabs.map((t) => (
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

function StartTab({ program, history, loaded, focus, onStart }: { program: Program; history: Workout[]; loaded: boolean; focus: string | null; onStart: (r: Routine | null) => void }) {
  const ROUTINES = program.routines;
  const hs = program.kind === "hoc-sinh";
  const [open, setOpen] = useState<string | null>(focus);
  const { count: weekCount, done: doneKeys, next, lastOf } = weekPlan(history, ROUTINES.map((r) => r.key), focus);

  return (
    <div className="space-y-3">
      {/* Học sinh (mục tự chọn, không tính điểm): không hiện "0/3 buổi" như chỉ tiêu còn thiếu (N3, L3) — chỉ ghi nhận buổi đã tập. */}
      {!hs && (
        <Card>
          <p className="text-sm text-muted">Tuần này</p>
          <p className="text-2xl font-bold text-ink">
            {weekCount}/{ROUTINES.length} buổi <span className="text-base font-semibold text-muted">· {ROUTINES.map((r) => (doneKeys.has(r.key) ? `${r.key} ✓` : r.key)).join("  ")}</span>
          </p>
          {loaded && history.length === 0 && (
            <p className="mt-1 text-sm text-muted">Chưa có buổi nào. Buổi đầu: nhập tạ vừa sức, cột “Lần trước” sẽ tự có từ buổi sau.</p>
          )}
        </Card>
      )}
      {hs && weekCount > 0 && (
        <Card>
          <p className="text-sm text-muted">Tuần này</p>
          <p className="text-2xl font-bold text-ink">Em đã tập {weekCount} buổi</p>
        </Card>
      )}
      {/* Buổi đầu tiên: ba điều an toàn hiện sẵn phía trên nút Bắt đầu (trước đây chỉ nằm trong hộp gập cuối trang). */}
      {hs && loaded && history.length === 0 && (
        <Card>
          <p className="font-bold text-ink">Trước buổi đầu tiên</p>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink">
            {FIRST_SESSION_SAFETY.map((t) => <li key={t}>{t}</li>)}
          </ul>
          <p className="mt-2 text-sm text-muted">Bắt đầu từ buổi 1, làm số lần vừa sức. Cột “Lần trước” sẽ tự có từ buổi sau.</p>
        </Card>
      )}

      {ROUTINES.map((r) => {
        const last = lastOf(r.key);
        const isOpen = open === r.key;
        return (
          <Card key={r.key} className={r.key === next ? "ring-2 ring-primary" : ""}>
            <div className="flex items-start gap-3">
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-primary-soft text-lg font-black text-primary">{r.key}</span>
              <div className="min-w-0 flex-1">
                <p className="font-bold text-ink">{r.name.replace(/^\w+ · /, "")}</p>
                <p className="text-xs text-muted">
                  {r.items.length} bài · {r.items.reduce((a, i) => a + i.sets, 0)} hiệp · {program.minutes} · {last ? `lần trước ${fmtDay(last.started_at)}` : "chưa tập"}
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
        <summary className="min-h-8 cursor-pointer font-bold text-ink">{hs ? "Tập an toàn: bản đầy đủ" : "Nguyên tắc chương trình · số hiệp/tuần"}</summary>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink">
          {program.rules.map((t) => <li key={t}>{t}</li>)}
        </ul>
        {!hs && (
          <>
            <p className="mt-3 text-sm font-semibold text-ink">Hiệp làm việc mỗi tuần (A+B+C)</p>
            <p className="text-sm text-muted">{weeklySets(ROUTINES).map(([g, n]) => `${g} ${n}`).join(" · ")}</p>
          </>
        )}
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
        {st.volume > 0 ? (
          <div className="rounded-xl bg-surface-2 py-2"><dt className="text-xs text-muted">Khối lượng</dt><dd className="font-bold text-ink">{vn(st.volume, 0)} kg</dd></div>
        ) : (
          <div className="rounded-xl bg-surface-2 py-2"><dt className="text-xs text-muted">Bài</dt><dd className="font-bold text-ink">{w.exercises.length}</dd></div>
        )}
        <div className="rounded-xl bg-surface-2 py-2"><dt className="text-xs text-muted">Hiệp</dt><dd className="font-bold text-ink">{st.sets}</dd></div>
      </dl>
      {prs.length > 0 && (
        <div className="mt-3">
          <p className="flex items-center gap-1.5 text-sm font-bold text-accent"><Trophy size={16} /> Tốt hơn chính mình lần trước</p>
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
              <p className="text-xs text-muted">{fmtDur(min)}{st.volume > 0 ? ` · ${vn(st.volume, 0)} kg` : ""} · {st.sets} hiệp</p>
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

function ProgressTab({ program, history }: { program: Program; history: Workout[] }) {
  const hs = program.kind === "hoc-sinh";
  const exIds = useMemo(() => {
    const m = new Map<string, number>();
    for (const w of history) for (const e of w.exercises) if (e.sets.some((s) => (hs ? s.done && (s.reps || s.sec) : s.kg && s.reps))) m.set(e.id, (m.get(e.id) ?? 0) + 1);
    // bài trọng tâm ngực–vai lên trước
    const order = ["chest_press_machine", "incline_db_press", "shoulder_press_machine", "lateral_raise_db", "lat_pulldown"];
    return [...m.keys()].sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99));
  }, [history, hs]);
  const [sel, setSel] = useState<string>("");
  const cur = sel || exIds[0] || "";
  const pts = useMemo(() => (!cur ? [] : hs ? bestCountHistory(history, cur).map((p) => ({ ...p, top: "" })) : bestE1rmHistory(history, cur)), [history, cur, hs]);
  const unit = exerciseById(cur)?.track === "time" ? "giây" : hs ? "lần" : "kg";

  // số hiệp làm việc 7 ngày qua theo nhóm cơ
  const [since] = useState(() => Date.now() - 7 * 864e5);
  const groupSets = new Map<string, number>();
  for (const w of history) if (new Date(w.started_at).getTime() >= since) for (const e of w.exercises) {
    const g = exerciseById(e.id)?.group ?? "Khác";
    groupSets.set(g, (groupSets.get(g) ?? 0) + e.sets.filter((s) => s.kind === "n" && s.done).length);
  }
  const plan = new Map(weeklySets(program.routines));

  return (
    <div className="space-y-3">
      <Card>
        <p className="font-bold text-ink">Hiệp làm việc 7 ngày qua</p>
        <ul className="mt-2 space-y-2">
          {program.groups.map((g) => {
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
        <p className="font-bold text-ink">{hs ? "Tiến bộ từng bài" : "Sức mạnh từng bài"}</p>
        {exIds.length === 0 ? (
          <p className="mt-1 text-sm text-muted">{hs ? "Tập vài buổi sẽ thấy số lần (số giây) của em tăng dần ở đây." : "Tập vài buổi có ghi kg sẽ thấy đường tiến bộ ở đây."}</p>
        ) : (
          <>
            <select value={cur} onChange={(e) => setSel(e.target.value)} className="mt-2 h-11 w-full rounded-xl border border-line bg-surface-2 px-3 text-base text-ink" aria-label="Chọn bài tập">
              {exIds.map((id) => <option key={id} value={id}>{exerciseById(id)?.name ?? id}</option>)}
            </select>
            <p className="mt-2 text-xs text-muted">{hs ? `Hiệp tốt nhất mỗi buổi (${unit})` : "1RM ước lượng (Epley) từ hiệp tốt nhất mỗi buổi"}</p>
            <LineChart points={pts.map((p) => ({ x: p.date, y: p.v }))} unit={unit} />
            <ul className="mt-2 divide-y divide-line text-sm">
              {[...pts].reverse().slice(0, 8).map((p, i) => (
                <li key={i} className="flex justify-between py-1.5"><span className="text-muted">{fmtDay(p.date)}</span><span className="tabular-nums text-ink">{hs ? `${p.v} ${unit}` : `${p.top} · ≈${vn(p.v)} kg`}</span></li>
              ))}
            </ul>
          </>
        )}
      </Card>
    </div>
  );
}
