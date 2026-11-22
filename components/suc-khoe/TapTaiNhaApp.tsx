"use client";
// Lộ trình tập tại nhà — dữ liệu + quy tắc ở lib/suc-khoe/tai-nha.ts.
// CAM KẾT: không gọi Supabase, không fetch, không gửi gì đi. Mọi thứ chỉ ở localStorage của máy này.
// Quy tắc UI: D1 (375px trước), D2 (nút ≥44px), D4 (3 tab), N3 (mỗi màn một việc chính), L3/G2 (không huy hiệu,
// không chuỗi ngày, không xếp hạng), B4 (đồng hồ chỉ chạy khi em bấm Bắt đầu), L4 (phản hồi hướng vào việc tiếp theo).
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Check, ChevronDown, Footprints, Lock, Pause, Play, SkipForward, Trash2, X, Zap, Dumbbell, Activity } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { fmtClock, mondayOf, pad } from "@/components/tap-luyen/ui";
import {
  DEFAULT_PROFILE, EMPTY_STATE, GOALS, HEALTH_FLAGS, STAGES, clearLocal, loadLocal, maxStageFor, phasesOf, progressHint, saveLocal,
  scaleSession, stageByN, suggestStage, totalMin, type LocalState, type Phase, type Profile, type Session, type SessionType,
} from "@/lib/suc-khoe/tai-nha";

const weekId = (d = new Date()) => {
  const m = mondayOf(d);
  return `${m.getFullYear()}-${pad(m.getMonth() + 1)}-${pad(m.getDate())}`;
};
const TYPE_ICON: Record<SessionType, React.ReactNode> = {
  "di-bo": <Footprints size={18} />,
  "suc-manh": <Activity size={18} />,
  hiit: <Zap size={18} />,
  gym: <Dumbbell size={18} />,
};
const TYPE_LABEL: Record<SessionType, string> = { "di-bo": "Đi bộ / chạy", "suc-manh": "Sức mạnh", hiit: "Ngắt quãng", gym: "Phòng gym" };

export default function TapTaiNhaApp() {
  const { profile: acc } = useAuth();
  const uid = acc?.id ?? "";
  // SucKhoeShell chỉ render khi đã có tài khoản → đọc máy ngay lần đầu (trang ssr:false nên có localStorage)
  const [st, setSt] = useState<LocalState | null>(() => loadLocal(uid));
  const [tab, setTab] = useState<"tuan" | "lo-trinh" | "ho-so">("tuan");
  const [playing, setPlaying] = useState<Session | null>(null);

  const update = useCallback(
    (fn: (s: LocalState) => LocalState) =>
      setSt((s) => {
        const n = fn(s ?? EMPTY_STATE);
        saveLocal(uid, n);
        return n;
      }),
    [uid],
  );

  if (!st) return <p className="h-24 animate-pulse rounded-2xl bg-surface-2" aria-label="Đang tải" />;

  if (!st.profile)
    return (
      <div className="space-y-4">
        <PrivacyNote />
        <ProfileForm
          initial={DEFAULT_PROFILE}
          submitLabel="Xem lộ trình của em"
          onSave={(p) => update((s) => ({ ...s, profile: p, stage: suggestStage(p).n, stageSince: weekId() }))}
        />
      </div>
    );

  const p = st.profile;
  return (
    <div className="space-y-4">
      <PrivacyNote compact />
      <div role="tablist" className="grid grid-cols-3 gap-1 rounded-2xl bg-surface-2 p-1">
        {([["tuan", "Tuần này"], ["lo-trinh", "Lộ trình"], ["ho-so", "Hồ sơ"]] as const).map(([k, l]) => (
          <button key={k} role="tab" aria-selected={tab === k} onClick={() => setTab(k)}
            className={`min-h-11 rounded-xl text-sm font-bold ${tab === k ? "bg-panel text-ink shadow-sm" : "text-muted"}`}>{l}</button>
        ))}
      </div>
      {tab === "tuan" && <Week st={st} update={update} onPlay={setPlaying} />}
      {tab === "lo-trinh" && <Roadmap st={st} update={update} />}
      {tab === "ho-so" && (
        <div className="space-y-4">
          <ProfileForm
            initial={p}
            submitLabel="Lưu hồ sơ"
            onSave={(np) => update((s) => ({ ...s, profile: np, stage: Math.min(s.stage, maxStageFor(np)) }))}
          />
          <DataSection uid={uid} onCleared={() => { setSt(EMPTY_STATE); setTab("tuan"); }} />
        </div>
      )}
      {playing && (
        <Player
          session={playing}
          quiet={p.quiet}
          onClose={() => setPlaying(null)}
          onDone={() => {
            const w = weekId();
            update((s) => {
              const weeks = s.weeks.some((x) => x.week === w) ? s.weeks : [...s.weeks, { week: w, done: [] }];
              return { ...s, weeks: weeks.map((x) => (x.week === w ? { ...x, done: [...x.done, playing.key] } : x)) };
            });
            setPlaying(null);
          }}
        />
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------------------------
function PrivacyNote({ compact }: { compact?: boolean }) {
  return (
    <section className="rounded-2xl border border-ok/40 bg-panel p-3">
      <p className="flex items-center gap-2 text-sm font-bold text-ink"><Lock size={16} className="text-ok" /> Không thu thập dữ liệu của em</p>
      {compact ? (
        <p className="mt-1 text-sm text-muted">Câu trả lời và các buổi đã tập chỉ lưu trên máy này. Xem chi tiết ở tab Hồ sơ.</p>
      ) : (
        <ul className="mt-1.5 list-disc space-y-1 pl-5 text-sm text-ink">
          <li>Mọi câu trả lời dưới đây, các buổi em đã tập và cảm nhận của em <b>chỉ lưu trên trình duyệt của máy này</b>.</li>
          <li>Không gửi lên máy chủ thachlab, không ai xem được — kể cả thầy cô, bạn bè, phụ huynh.</li>
          <li>Em xoá được bất cứ lúc nào ở tab Hồ sơ. Đổi máy hoặc xoá dữ liệu trình duyệt thì phải trả lời lại.</li>
        </ul>
      )}
    </section>
  );
}

function DataSection({ uid, onCleared }: { uid: string; onCleared: () => void }) {
  const [ask, setAsk] = useState(false);
  return (
    <section className="rounded-2xl border border-line bg-panel p-4">
      <h2 className="flex items-center gap-2 font-bold text-ink"><Lock size={16} className="text-ok" /> Dữ liệu của em ở đâu?</h2>
      <ul className="mt-2 list-disc space-y-1.5 pl-5 text-sm text-ink">
        <li>Hồ sơ, bậc đang tập, các buổi đã tick và cảm nhận mỗi tuần nằm trong bộ nhớ trình duyệt (localStorage) của máy này.</li>
        <li>Trang này <b>không gửi</b> những thông tin đó lên máy chủ, không có trong bảng điểm, báo cáo hay trang phụ huynh. Thầy cô không xem được.</li>
        <li>Em đăng nhập chỉ để vào được mục Sức khỏe. Máy dùng chung: mỗi tài khoản có phần lưu riêng, nhưng người dùng chung máy có thể mở trình duyệt để xem — nên xoá khi dùng máy công cộng.</li>
        <li>Không có cân nặng, vòng đo hay ảnh cơ thể nào được hỏi ở đây.</li>
      </ul>
      {ask ? (
        <div className="mt-3 grid grid-cols-2 gap-2">
          <button onClick={() => setAsk(false)} className="min-h-11 rounded-xl border border-line text-sm font-bold text-ink">Giữ lại</button>
          <button onClick={() => { clearLocal(uid); onCleared(); }} className="min-h-11 rounded-xl bg-danger text-sm font-bold text-white">Xoá hết</button>
        </div>
      ) : (
        <button onClick={() => setAsk(true)} className="mt-3 flex min-h-11 items-center gap-2 rounded-xl border border-line px-4 text-sm font-bold text-danger">
          <Trash2 size={16} /> Xoá dữ liệu trên máy này
        </button>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------------------------
function Choice<T extends string | number>({ label, value, options, onChange, cols = 2 }: { label: string; value: T; options: [T, string][]; onChange: (v: T) => void; cols?: number }) {
  return (
    <fieldset>
      <legend className="mb-1.5 text-sm font-bold text-ink">{label}</legend>
      <div className={`grid gap-2 ${cols === 4 ? "grid-cols-4" : cols === 3 ? "grid-cols-3" : "grid-cols-1 sm:grid-cols-2"}`}>
        {options.map(([v, l]) => (
          <button type="button" key={String(v)} aria-pressed={value === v} onClick={() => onChange(v)}
            className={`min-h-11 rounded-xl border px-3 py-2 text-left text-sm ${value === v ? "border-primary bg-primary-soft font-bold text-ink" : "border-line text-ink"}`}>{l}</button>
        ))}
      </div>
    </fieldset>
  );
}
function Toggle({ checked, onChange, children }: { checked: boolean; onChange: (v: boolean) => void; children: React.ReactNode }) {
  return (
    <label className="flex min-h-11 cursor-pointer items-start gap-3 rounded-xl border border-line px-3 py-2.5 text-sm text-ink">
      <input type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} className="mt-0.5 h-5 w-5 shrink-0 accent-[var(--color-primary)]" />
      <span>{children}</span>
    </label>
  );
}

function ProfileForm({ initial, submitLabel, onSave }: { initial: Profile; submitLabel: string; onSave: (p: Profile) => void }) {
  const [p, setP] = useState<Profile>(initial);
  const set = <K extends keyof Profile>(k: K, v: Profile[K]) => setP((x) => ({ ...x, [k]: v }));
  const toggleIn = (k: "goals" | "health", v: string) => setP((x) => ({ ...x, [k]: x[k].includes(v) ? x[k].filter((y) => y !== v) : [...x[k], v] }));
  const sug = suggestStage(p);
  return (
    <form className="space-y-5 rounded-2xl border border-line bg-panel p-4" onSubmit={(e) => { e.preventDefault(); onSave(p); }}>
      <div>
        <h2 className="text-lg font-bold text-ink">Vài câu để chọn bậc bắt đầu</h2>
        <p className="text-sm text-muted">Trả lời thật với sức mình — bắt đầu thấp rồi lên nhanh tốt hơn bắt đầu cao rồi bỏ.</p>
      </div>
      <Choice label="Em đang học" value={p.grade} cols={4} onChange={(v) => set("grade", v)} options={[["10", "Lớp 10"], ["11", "Lớp 11"], ["12", "Lớp 12"], ["sv", "SV"]]} />
      <Choice label="Hiện em vận động thế nào?" value={p.activity} onChange={(v) => set("activity", v)}
        options={[[0, "Hầu như chỉ ngồi"], [1, "Đi bộ / đạp xe đi học"], [2, "Chơi thể thao 1–2 buổi/tuần"], [3, "Tập đều từ 3 buổi/tuần"]]} />
      <Choice label="Em đi bộ nhanh liền được bao lâu mà không phải dừng?" value={p.walk} onChange={(v) => set("walk", v)}
        options={[[0, "Dưới 10 phút"], [1, "10–20 phút"], [2, "20–30 phút"], [3, "Hơn 30 phút"]]} />
      <Choice label="Hít đất của em" value={p.push} onChange={(v) => set("push", v)}
        options={[[0, "Chưa làm được"], [1, "Chống tay lên bàn / chống gối"], [2, "Hít đất thường 1–9 cái"], [3, "Hít đất thường từ 10 cái"]]} />
      <Choice label="Mỗi buổi em có khoảng" value={p.minutes} cols={3} onChange={(v) => set("minutes", v)} options={[[20, "20 phút"], [30, "30 phút"], [45, "45 phút"]]} />
      <Choice label="Mỗi tuần em tập được mấy ngày?" value={p.days} cols={4} onChange={(v) => set("days", v)} options={[[2, "2"], [3, "3"], [4, "4"], [5, "5"]]} />
      <fieldset className="space-y-2">
        <legend className="mb-1.5 text-sm font-bold text-ink">Hoàn cảnh và sở thích</legend>
        <Toggle checked={p.quiet} onChange={(v) => set("quiet", v)}>Tập không bật nhảy <span className="text-muted">(nhà tầng, sợ ồn, gối hay đau)</span></Toggle>
        <Toggle checked={p.podcast} onChange={(v) => set("podcast", v)}>Thích nghe podcast / nhạc khi đi bộ</Toggle>
        <Toggle checked={p.withFriend} onChange={(v) => set("withFriend", v)}>Muốn rủ bạn hoặc người nhà tập cùng</Toggle>
      </fieldset>
      <fieldset className="space-y-2">
        <legend className="mb-1.5 text-sm font-bold text-ink">Em muốn gì từ việc tập? <span className="font-normal text-muted">(chọn bao nhiêu cũng được)</span></legend>
        {GOALS.map((g) => <Toggle key={g.key} checked={p.goals.includes(g.key)} onChange={() => toggleIn("goals", g.key)}>{g.label}</Toggle>)}
      </fieldset>
      <fieldset className="space-y-2">
        <legend className="mb-1.5 text-sm font-bold text-ink">Sức khoẻ — có mục nào đúng với em không?</legend>
        <p className="text-xs text-muted">Chỉ để chọn mức an toàn. Không lưu ngoài máy này.</p>
        {HEALTH_FLAGS.map((h) => <Toggle key={h.key} checked={p.health.includes(h.key)} onChange={() => toggleIn("health", h.key)}>{h.label}</Toggle>)}
        {p.health.length > 0 && (
          <div className="rounded-xl border border-warn/50 p-3 text-sm text-ink">
            <p>Em nên <b>nói với bố mẹ và hỏi bác sĩ</b> trước khi tập mạnh hơn đi bộ. Trong lúc chờ, em vẫn đi bộ nhẹ được.</p>
            <div className="mt-2"><Toggle checked={p.doctorOk} onChange={(v) => set("doctorOk", v)}>Bác sĩ đã đồng ý cho em tập</Toggle></div>
          </div>
        )}
      </fieldset>
      <div className="rounded-xl bg-surface-2 p-3 text-sm">
        <p className="font-bold text-ink">Gợi ý: {stageByN(Math.min(sug.n, maxStageFor(p))).name}</p>
        <p className="text-muted">{sug.why}</p>
      </div>
      <button type="submit" className="min-h-12 w-full rounded-xl bg-primary text-sm font-bold text-white">{submitLabel}</button>
    </form>
  );
}

// ---------------------------------------------------------------------------------------------
function Week({ st, update, onPlay }: { st: LocalState; update: (fn: (s: LocalState) => LocalState) => void; onPlay: (s: Session) => void }) {
  const p = st.profile!;
  const stage = stageByN(st.stage);
  const w = weekId();
  const log = st.weeks.find((x) => x.week === w) ?? { week: w, done: [] as string[] };
  const plan = useMemo(
    () => stage.order.slice(0, p.days).map((k, i) => ({ i, s: scaleSession(stage.sessions.find((x) => x.key === k)!, p.minutes) })),
    [stage, p.days, p.minutes],
  );
  // buổi i đã tập khi số lần tập buổi đó ≥ thứ tự xuất hiện của nó trong kế hoạch
  const doneIdx = new Set<number>();
  const counts = new Map<string, number>();
  for (const k of log.done) counts.set(k, (counts.get(k) ?? 0) + 1);
  const seen = new Map<string, number>();
  for (const { i, s } of plan) {
    const n = (seen.get(s.key) ?? 0) + 1;
    seen.set(s.key, n);
    if ((counts.get(s.key) ?? 0) >= n) doneIdx.add(i);
  }
  const hint = progressHint(st, p.days, w);
  const weeksIn = new Set(st.weeks.filter((x) => x.week >= st.stageSince && x.done.length).map((x) => x.week)).size;
  const setLog = (fn: (l: typeof log) => typeof log) =>
    update((s) => {
      const has = s.weeks.some((x) => x.week === w);
      const weeks = has ? s.weeks : [...s.weeks, log];
      return { ...s, weeks: weeks.map((x) => (x.week === w ? fn(x) : x)) };
    });
  const toggleDone = (key: string, done: boolean) =>
    setLog((l) => {
      if (!done) return { ...l, done: [...l.done, key] };
      const j = l.done.lastIndexOf(key);
      return { ...l, done: l.done.filter((_, k) => k !== j) };
    });
  const maxN = maxStageFor(p);

  return (
    <div className="space-y-4">
      <section className="rounded-2xl border border-line bg-panel p-4">
        <p className="text-xs font-bold uppercase tracking-wide text-muted">Em đang ở</p>
        <p className="text-lg font-bold text-ink">{stage.name}</p>
        <p className="text-sm text-ink">{stage.goal}</p>
        <p className="mt-1 text-sm text-muted">
          Tuần thứ {Math.max(1, weeksIn + (log.done.length ? 0 : 1))} ở bậc này · nên ở ít nhất {stage.minWeeks} tuần · tuần này {doneIdx.size}/{plan.length} buổi
        </p>
      </section>

      {hint === "len" && st.stage < Math.min(6, maxN) && (
        <section className="rounded-2xl border border-primary/50 bg-primary-soft p-4">
          <p className="font-bold text-ink">Hai tuần qua em tập đều. Thử tự kiểm để lên {stageByN(st.stage + 1).short}?</p>
          <LevelUpCheck stageN={st.stage} onPass={() => update((s) => ({ ...s, stage: s.stage + 1, stageSince: w }))} />
        </section>
      )}
      {hint === "nhe-lai" && (
        <section className="rounded-2xl border border-warn/50 bg-panel p-4 text-sm text-ink">
          <p className="font-bold">Hai tuần liền em thấy mệt quá.</p>
          <p className="mt-1">Thử bớt một ngày tập hoặc chọn 20 phút/buổi ở tab Hồ sơ. Ngủ đủ 8 tiếng trước khi tăng lại.{st.stage > 1 && " Hoặc lùi về bậc trước vài tuần — không sao cả."}</p>
          {st.stage > 1 && (
            <button onClick={() => update((s) => ({ ...s, stage: s.stage - 1, stageSince: w }))} className="mt-2 min-h-11 rounded-xl border border-line px-4 font-bold">Về {stageByN(st.stage - 1).short}</button>
          )}
        </section>
      )}

      <section aria-labelledby="tn-buoi">
        <h2 id="tn-buoi" className="mb-2 text-sm font-bold uppercase tracking-wide text-muted">Các buổi tuần này</h2>
        <ul className="space-y-2">
          {plan.map(({ i, s }) => (
            <SessionCard key={i} n={i + 1} s={s} quiet={p.quiet} podcast={p.podcast} done={doneIdx.has(i)} onPlay={() => onPlay(s)} onToggle={() => toggleDone(s.key, doneIdx.has(i))} />
          ))}
        </ul>
        <p className="mt-2 text-xs text-muted">Thứ tự tự chọn theo lịch học của em; xen ngày nghỉ, không làm hai buổi ngắt quãng (⚡) hai ngày liền.{p.withFriend && " Rủ bạn cùng đi bộ hay cùng bấm đồng hồ — dễ giữ nhịp hơn."}</p>
      </section>

      <section className="rounded-2xl border border-line bg-panel p-4">
        <p className="font-bold text-ink">Tuần này em thấy thế nào?</p>
        <p className="text-xs text-muted">Dùng để gợi ý lên bậc hay nhẹ lại. Chỉ lưu trên máy này.</p>
        <div className="mt-2 grid grid-cols-3 gap-2">
          {([["nhe", "Nhẹ nhàng"], ["vua", "Vừa sức"], ["met", "Mệt quá"]] as const).map(([k, l]) => (
            <button key={k} aria-pressed={log.feel === k} onClick={() => setLog((x) => ({ ...x, feel: x.feel === k ? undefined : k }))}
              className={`min-h-11 rounded-xl border text-sm ${log.feel === k ? "border-primary bg-primary-soft font-bold text-ink" : "border-line text-ink"}`}>{l}</button>
          ))}
        </div>
      </section>

      <details className="rounded-2xl border border-line bg-panel p-4">
        <summary className="cursor-pointer font-bold text-ink">Mẹo ở bậc này</summary>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink">{stage.tips.map((t) => <li key={t}>{t}</li>)}</ul>
      </details>
      <details className="rounded-2xl border border-line bg-panel p-4">
        <summary className="cursor-pointer font-bold text-ink">Khi nào lên bậc tiếp?</summary>
        <LevelUpCheck stageN={st.stage} disabled={st.stage >= Math.min(6, maxN)} onPass={() => update((s) => ({ ...s, stage: s.stage + 1, stageSince: w }))} />
      </details>
      <SafetyNote />
    </div>
  );
}

function SessionCard({ n, s, quiet, podcast, done, onPlay, onToggle }: { n: number; s: Session; quiet: boolean; podcast: boolean; done: boolean; onPlay: () => void; onToggle: () => void }) {
  const [open, setOpen] = useState(false);
  const ph = useMemo(() => phasesOf(s, quiet), [s, quiet]);
  const walkOnly = s.type === "di-bo" || (s.type === "gym" && s.blocks[0]?.items[0] === "may_di_bo");
  return (
    <li className={`rounded-2xl border bg-panel p-3 ${done ? "border-ok/50" : "border-line"}`}>
      <div className="flex items-start gap-3">
        <span className={`grid h-10 w-10 shrink-0 place-items-center rounded-xl ${done ? "bg-ok/15 text-ok" : "bg-primary-soft text-primary"}`}>{done ? <Check size={18} /> : TYPE_ICON[s.type]}</span>
        <div className="min-w-0 flex-1">
          <p className="font-bold text-ink">Buổi {n} · {s.title}</p>
          <p className="text-sm text-muted">{TYPE_LABEL[s.type]} · khoảng {totalMin(ph)} phút</p>
        </div>
      </div>
      <p className="mt-2 text-sm text-ink">{s.why}</p>
      {walkOnly && podcast && <p className="mt-1 text-sm text-muted">🎧 Gợi ý: một tập podcast em thích, hoặc bài nghe tiếng Anh — vừa đi vừa học.</p>}
      <button onClick={() => setOpen((o) => !o)} aria-expanded={open} className="mt-1 flex min-h-11 items-center gap-1 text-sm font-semibold text-primary">
        <ChevronDown size={16} className={open ? "rotate-180" : ""} /> {open ? "Ẩn bài tập" : "Xem bài tập"}
      </button>
      {open && <SessionDetail s={s} quiet={quiet} />}
      <div className="mt-2 grid grid-cols-2 gap-2">
        <button onClick={onToggle} className={`min-h-11 rounded-xl border text-sm font-bold ${done ? "border-ok/50 text-ok" : "border-line text-ink"}`}>{done ? "Đã tập ✓" : "Đánh dấu đã tập"}</button>
        <button onClick={onPlay} className="flex min-h-11 items-center justify-center gap-1.5 rounded-xl bg-primary text-sm font-bold text-white"><Play size={16} /> Bắt đầu</button>
      </div>
    </li>
  );
}

function SessionDetail({ s, quiet }: { s: Session; quiet: boolean }) {
  const ph = phasesOf(s, quiet);
  const groups: { block: string; items: { name: string; cue: string; sec: number }[] }[] = [];
  for (const p of ph) {
    if (p.kind !== "work" || !p.move) continue;
    const b = p.block.replace(/ · vòng .*/, "");
    let g = groups.find((x) => x.block === b);
    if (!g) groups.push((g = { block: b, items: [] }));
    if (!g.items.some((x) => x.name === p.move!.name)) g.items.push({ name: p.move.name, cue: p.move.cue, sec: p.sec });
  }
  return (
    <div className="mt-1 space-y-3 border-t border-line pt-2">
      {groups.map((g) => {
        const blk = s.blocks.find((b) => g.block === b.label);
        return (
          <div key={g.block}>
            <p className="text-sm font-bold text-ink">
              {g.block}
              {blk && blk.items.length > 1 && <span className="font-normal text-muted"> · {blk.rounds} vòng · {blk.work}″ làm / {blk.rest}″ nghỉ</span>}
            </p>
            {blk?.note && <p className="text-xs text-muted">{blk.note}</p>}
            <ul className="mt-1 space-y-1.5">
              {g.items.map((it) => (
                <li key={it.name} className="text-sm leading-snug">
                  <span className="font-semibold text-ink">{it.name}</span>
                  {it.sec >= 120 && <span className="text-muted"> · {Math.round(it.sec / 60)} phút</span>}
                  <br />
                  <span className="text-muted">{it.cue}</span>
                </li>
              ))}
            </ul>
          </div>
        );
      })}
    </div>
  );
}

function LevelUpCheck({ stageN, onPass, disabled }: { stageN: number; onPass: () => void; disabled?: boolean }) {
  const stage = stageByN(stageN);
  const [ok, setOk] = useState<boolean[]>(() => stage.levelUp.map(() => false));
  if (stageN >= 6) return <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink">{stage.levelUp.map((t) => <li key={t}>{t}</li>)}</ul>;
  const all = ok.every(Boolean);
  return (
    <div className="mt-2 space-y-2">
      {stage.levelUp.map((t, i) => (
        <Toggle key={t} checked={ok[i]} onChange={(v) => setOk((o) => o.map((x, j) => (j === i ? v : x)))}>{t}</Toggle>
      ))}
      {disabled ? (
        <p className="text-sm text-muted">Với mục sức khoẻ em đã chọn, hãy hỏi bác sĩ trước khi lên bậc tiếp.</p>
      ) : (
        <button disabled={!all} onClick={onPass} className="min-h-11 w-full rounded-xl bg-primary text-sm font-bold text-white disabled:opacity-40">
          {all ? `Lên ${stageByN(stageN + 1).name}` : "Đạt đủ các mục thì lên bậc"}
        </button>
      )}
    </div>
  );
}

function SafetyNote() {
  return (
    <section className="rounded-2xl border border-line bg-panel p-4 text-sm text-ink">
      <p className="font-bold">Dừng ngay và báo người lớn khi</p>
      <p className="mt-1">đau tức ngực, chóng mặt, khó thở bất thường, tim đập loạn, đau nhói ở khớp. Mỏi cơ 1–2 ngày sau buổi tập là bình thường.</p>
      <p className="mt-2 text-muted">Ngoài các buổi này, tuổi các em nên vận động vừa đến mạnh khoảng 60 phút mỗi ngày (WHO 2020), ngủ 8–10 tiếng, ăn đủ ba bữa, không ăn kiêng.</p>
    </section>
  );
}

// ---------------------------------------------------------------------------------------------
function Roadmap({ st, update }: { st: LocalState; update: (fn: (s: LocalState) => LocalState) => void }) {
  const p = st.profile!;
  const maxN = maxStageFor(p);
  const [confirm, setConfirm] = useState<number | null>(null);
  return (
    <div className="space-y-3">
      <p className="text-sm text-ink">
        Lộ trình đi theo con đường thầy Thạch đã đi: <b>đi bộ công viên, nghe podcast</b> → <b>bài tay không</b> → <b>Tabata, HIIT</b> → <b>máy đi bộ, máy tạ nhẹ ở phòng gym</b>. Mỗi bậc vài tuần; lên bậc khi đạt tiêu chí, không cần vội.
      </p>
      <ol className="space-y-2">
        {STAGES.map((s) => {
          const cur = s.n === st.stage;
          const locked = s.n > maxN;
          return (
            <li key={s.n} className={`rounded-2xl border bg-panel p-3 ${cur ? "border-primary" : "border-line"}`}>
              <details open={cur}>
                <summary className="flex min-h-11 cursor-pointer list-none items-center gap-3">
                  <span className={`grid h-9 w-9 shrink-0 place-items-center rounded-full text-sm font-bold ${s.n < st.stage ? "bg-ok/15 text-ok" : cur ? "bg-primary text-white" : "bg-surface-2 text-muted"}`}>{s.n < st.stage ? <Check size={16} /> : s.n}</span>
                  <span className="min-w-0 flex-1">
                    <span className="block font-bold text-ink">{s.name}</span>
                    <span className="block text-xs text-muted">ít nhất {s.minWeeks} tuần{cur && " · em đang ở đây"}</span>
                  </span>
                  <ChevronDown size={16} className="shrink-0 text-muted" />
                </summary>
                <p className="mt-2 text-sm text-ink">{s.goal}</p>
                <p className="mt-2 text-sm font-bold text-ink">Các buổi</p>
                <ul className="list-disc pl-5 text-sm text-ink">{s.sessions.map((x) => <li key={x.key}>{x.title} <span className="text-muted">· {TYPE_LABEL[x.type]}</span></li>)}</ul>
                <p className="mt-2 text-sm font-bold text-ink">Lên bậc tiếp khi</p>
                <ul className="list-disc pl-5 text-sm text-ink">{s.levelUp.map((x) => <li key={x}>{x}</li>)}</ul>
                {!cur && (locked ? (
                  <p className="mt-2 text-sm text-muted">Với mục sức khoẻ em đã chọn, hỏi bác sĩ trước khi tập bậc này.</p>
                ) : confirm === s.n ? (
                  <div className="mt-2 grid grid-cols-2 gap-2">
                    <button onClick={() => setConfirm(null)} className="min-h-11 rounded-xl border border-line text-sm font-bold text-ink">Thôi</button>
                    <button onClick={() => { update((x) => ({ ...x, stage: s.n, stageSince: weekId() })); setConfirm(null); }} className="min-h-11 rounded-xl bg-primary text-sm font-bold text-white">Chuyển</button>
                  </div>
                ) : (
                  <button onClick={() => setConfirm(s.n)} className="mt-2 min-h-11 rounded-xl border border-line px-4 text-sm font-bold text-ink">
                    {s.n < st.stage ? "Lùi về bậc này" : "Chuyển sang bậc này"}
                  </button>
                ))}
              </details>
            </li>
          );
        })}
      </ol>
      <p className="text-xs text-muted">
        Cơ sở: Khuyến nghị vận động WHO 2020 cho 5–17 tuổi; Học viện Nhi khoa Hoa Kỳ (AAP 2020) về tập sức mạnh tuổi vị thành niên; bộ câu hỏi sàng lọc PAR-Q+; “talk test” đo mức gắng sức. Tabata ở đây là bản nhẹ cho người mới, không phải bản gốc dành cho vận động viên.
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------------------------
function tone(kind: "work" | "rest" | "end") {
  try {
    navigator.vibrate?.(kind === "work" ? [200] : kind === "end" ? [300, 100, 300] : [120, 80, 120]);
    const Ctx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ctx = new Ctx();
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.value = kind === "work" ? 988 : 660;
    g.gain.setValueAtTime(0.25, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
    o.connect(g).connect(ctx.destination);
    o.start();
    o.stop(ctx.currentTime + 0.4);
  } catch {
    /* trình duyệt chặn âm thanh */
  }
}

function Player({ session, quiet, onClose, onDone }: { session: Session; quiet: boolean; onClose: () => void; onDone: () => void }) {
  const phases = useMemo<Phase[]>(() => phasesOf(session, quiet), [session, quiet]);
  const [idx, setIdx] = useState(0);
  const [left, setLeft] = useState(phases[0]?.sec ?? 0);
  const [run, setRun] = useState(false);
  const [finished, setFinished] = useState(false);
  const endAt = useRef(0);
  const wake = useRef<{ release: () => Promise<void> } | null>(null);

  const go = useCallback((i: number) => {
    if (i >= phases.length) {
      setFinished(true);
      setRun(false);
      tone("end");
      return;
    }
    setIdx(i);
    setLeft(phases[i].sec);
    endAt.current = Date.now() + phases[i].sec * 1000;
    tone(phases[i].kind);
  }, [phases]);

  useEffect(() => {
    if (!run) return;
    endAt.current = Date.now() + left * 1000;
    const t = setInterval(() => {
      const l = Math.ceil((endAt.current - Date.now()) / 1000);
      if (l <= 0) go(idx + 1);
      else setLeft(l);
    }, 250);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [run, idx]);

  // giữ màn hình sáng trong lúc tập (nếu trình duyệt hỗ trợ)
  useEffect(() => {
    const nav = navigator as Navigator & { wakeLock?: { request: (t: "screen") => Promise<{ release: () => Promise<void> }> } };
    if (run && nav.wakeLock) nav.wakeLock.request("screen").then((w) => (wake.current = w)).catch(() => {});
    return () => { wake.current?.release().catch(() => {}); wake.current = null; };
  }, [run]);

  const ph = phases[idx];
  const doneSec = phases.slice(0, idx).reduce((a, p) => a + p.sec, 0) + (ph ? ph.sec - left : 0);
  const total = phases.reduce((a, p) => a + p.sec, 0);

  return (
    <div role="dialog" aria-modal="true" aria-label={session.title} className="fixed inset-0 z-50 flex flex-col bg-bg">
      <div className="mx-auto flex w-full max-w-xl items-center gap-2 px-4 pt-4">
        <p className="min-w-0 flex-1 truncate font-bold text-ink">{session.title}</p>
        <button onClick={onClose} aria-label="Đóng" className="grid h-11 w-11 place-items-center rounded-xl text-muted hover:bg-surface-2"><X size={20} /></button>
      </div>
      <div className="mx-auto mt-2 h-1.5 w-[calc(100%-2rem)] max-w-xl overflow-hidden rounded-full bg-surface-2">
        <div className="h-full bg-primary" style={{ width: `${Math.min(100, (doneSec / Math.max(1, total)) * 100)}%` }} />
      </div>
      {finished ? (
        <div className="mx-auto flex w-full max-w-xl flex-1 flex-col items-center justify-center px-4 text-center">
          <Check size={40} className="text-ok" />
          <p className="mt-2 text-2xl font-bold text-ink">Xong buổi tập</p>
          <p className="mt-1 text-sm text-muted">Uống nước, giãn cơ thêm nếu còn mỏi. Bấm lưu để đánh dấu buổi này (chỉ lưu trên máy em).</p>
          <button onClick={onDone} className="mt-5 min-h-12 w-full rounded-xl bg-primary text-sm font-bold text-white">Lưu là đã tập</button>
          <button onClick={onClose} className="mt-2 min-h-11 w-full rounded-xl text-sm font-bold text-muted">Không lưu</button>
        </div>
      ) : ph ? (
        <>
          <div className="mx-auto flex w-full max-w-xl flex-1 flex-col items-center justify-center px-4 text-center">
            <p className="text-sm text-muted">{ph.block}</p>
            <p className={`mt-1 text-sm font-bold uppercase tracking-wide ${ph.kind === "work" ? "text-primary" : "text-ok"}`}>{ph.kind === "work" ? "Làm" : "Nghỉ"}</p>
            <p className="font-display text-7xl font-bold tabular-nums text-ink">{fmtClock(left)}</p>
            <p className="mt-3 text-xl font-bold text-ink">{ph.label}</p>
            {ph.move?.cue && ph.kind === "work" && <p className="mt-1 max-w-sm text-sm text-muted">{ph.move.cue}</p>}
            {ph.next && <p className="mt-4 text-sm text-muted">Tiếp theo: <span className="font-semibold text-ink">{ph.next}</span></p>}
          </div>
          <div className="mx-auto grid w-full max-w-xl grid-cols-[1fr_2fr] gap-2 px-4 pb-8">
            <button onClick={() => go(idx + 1)} className="flex min-h-14 items-center justify-center gap-1.5 rounded-xl border border-line text-sm font-bold text-ink"><SkipForward size={18} /> Bỏ qua</button>
            <button onClick={() => { if (!run && idx === 0 && left === phases[0].sec) tone(phases[0].kind); setRun((r) => !r); }}
              className="flex min-h-14 items-center justify-center gap-2 rounded-xl bg-primary text-base font-bold text-white">
              {run ? <><Pause size={20} /> Tạm dừng</> : <><Play size={20} /> {idx === 0 && left === phases[0].sec ? "Bắt đầu" : "Tiếp tục"}</>}
            </button>
          </div>
        </>
      ) : null}
    </div>
  );
}
