"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { ChevronLeft, ChevronRight, Minus, Plus, Search, Trash2, X } from "lucide-react";
import {
  ACTIVITY,
  DEFAULT_PROFILE,
  FOODS,
  GOAL_KCAL,
  GOAL_LABEL,
  adjustAdvice,
  fetchDays,
  fetchProfile,
  saveDay,
  saveProfile,
  sumItems,
  targets,
  weeklyWeights,
  type Food,
  type FoodItem,
  type Goal,
  type NutritionDay,
  type NutritionProfile,
} from "@/lib/suc-khoe/dinh-duong";
import { TARGET } from "@/lib/tap-luyen/chuong-trinh";
import { fetchMeasurements, newId, type Measurement } from "@/lib/tap-luyen/store";
import { analyzeBuild } from "@/lib/suc-khoe/build";
import { Card, NumInput, fmtDay, todayIso, vn } from "@/components/tap-luyen/ui";

const shiftDay = (iso: string, n: number) => {
  const d = new Date(`${iso}T00:00:00`);
  d.setDate(d.getDate() + n);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};
const emptyDay = (day: string): NutritionDay => ({ day, items: [], weight_kg: null });

function Bar({ value, max, tone }: { value: number; max: number; tone: string }) {
  const pct = max > 0 ? Math.min(100, (value / max) * 100) : 0;
  return (
    <div className="h-2.5 overflow-hidden rounded-full bg-surface-2" role="progressbar" aria-valuenow={Math.round(value)} aria-valuemax={Math.round(max)}>
      <div className={`h-full rounded-full ${tone}`} style={{ width: `${pct}%` }} />
    </div>
  );
}

function Seg<T extends string | number>({ value, options, onChange }: { value: T; options: { v: T; label: string }[]; onChange: (v: T) => void }) {
  return (
    <div className="flex gap-1 rounded-xl bg-surface-2 p-1">
      {options.map((o) => (
        <button
          key={String(o.v)}
          type="button"
          onClick={() => onChange(o.v)}
          className={`min-h-10 flex-1 rounded-lg px-2 text-sm font-semibold ${o.v === value ? "bg-panel text-ink shadow-sm" : "text-muted"}`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

export default function DinhDuongApp() {
  const [today] = useState(todayIso);
  const [year] = useState(() => new Date().getFullYear());
  const [cur, setCur] = useState(today);
  const [days, setDays] = useState<Record<string, NutritionDay> | null>(null);
  const [offline, setOffline] = useState(false);
  const [prof, setProf] = useState<NutritionProfile | null>(null);
  const [bodyKg, setBodyKg] = useState<number | null>(null);
  const [bodyCm, setBodyCm] = useState<number | null>(null);
  const [bodyLast, setBodyLast] = useState<Measurement | null>(null);
  const [dirtyDay, setDirtyDay] = useState<string | null>(null);
  const [dirtyProf, setDirtyProf] = useState(false);
  const [sync, setSync] = useState<"ok" | "pending" | null>(null);
  const [picker, setPicker] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const ptimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    fetchDays(shiftDay(todayIso(), -60)).then((r) => {
      setDays(Object.fromEntries(r.list.map((d) => [d.day, d])));
      setOffline(r.offline);
    });
    fetchProfile().then(setProf);
    fetchMeasurements().then((r) => {
      const withW = [...r.list].reverse().find((m) => m.weight_kg);
      const withH = [...r.list].reverse().find((m) => m.height_cm);
      setBodyKg(withW?.weight_kg ?? null);
      setBodyCm(withH?.height_cm ?? null);
      setBodyLast(r.list[r.list.length - 1] ?? null);
    });
  }, []);

  // ghi ngày đang sửa sau 0,7 s không bấm thêm
  useEffect(() => {
    if (!dirtyDay || !days) return;
    const d = days[dirtyDay];
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => {
      saveDay(d).then((ok) => {
        setSync(ok ? "ok" : "pending");
        setDirtyDay(null);
      });
    }, 700);
    return () => {
      if (timer.current) clearTimeout(timer.current);
    };
  }, [dirtyDay, days]);

  useEffect(() => {
    if (!dirtyProf || !prof) return;
    if (ptimer.current) clearTimeout(ptimer.current);
    ptimer.current = setTimeout(() => {
      saveProfile(prof)
        .then(() => setSync("ok"))
        .catch(() => setSync("pending"))
        .finally(() => setDirtyProf(false));
    }, 700);
    return () => {
      if (ptimer.current) clearTimeout(ptimer.current);
    };
  }, [dirtyProf, prof]);

  const list = useMemo(() => Object.values(days ?? {}).sort((a, b) => b.day.localeCompare(a.day)), [days]);
  const day = days?.[cur] ?? emptyDay(cur);
  // cân dùng để tính: cân sáng gần nhất trong nhật ký, rồi số đo cơ thể, rồi mốc 18/11
  const lastDayKg = list.find((d) => d.weight_kg != null)?.weight_kg ?? null;
  const kg = lastDayKg ?? bodyKg ?? TARGET.start.weight;
  const cm = bodyCm ?? TARGET.start.height;
  const t = prof ? targets(prof, kg, cm, year) : null;
  const eaten = sumItems(day.items);
  const weeks = weeklyWeights(list);
  const advice = prof ? adjustAdvice(weeks, prof.goal) : null;

  const recents = useMemo(() => {
    const cnt = new Map<string, { item: FoodItem; n: number }>();
    for (const d of list.slice(0, 30)) for (const i of d.items) cnt.set(i.id, { item: i, n: (cnt.get(i.id)?.n ?? 0) + 1 });
    return [...cnt.values()].sort((a, b) => b.n - a.n).slice(0, 8).map((x) => x.item);
  }, [list]);

  const editDay = (fn: (d: NutritionDay) => NutritionDay) => {
    setDays((m) => ({ ...(m ?? {}), [cur]: fn(m?.[cur] ?? emptyDay(cur)) }));
    setDirtyDay(cur);
    setSync(null);
  };
  const editProf = (patch: Partial<NutritionProfile>) => {
    setProf((p) => ({ ...(p ?? DEFAULT_PROFILE), ...patch }));
    setDirtyProf(true);
    setSync(null);
  };
  const addFood = (f: Omit<Food, "group"> & { group?: string }) =>
    editDay((d) => {
      const ex = d.items.find((i) => i.id === f.id);
      if (ex) return { ...d, items: d.items.map((i) => (i.id === f.id ? { ...i, qty: i.qty + 1 } : i)) };
      return { ...d, items: [...d.items, { id: f.id, name: f.name, unit: f.unit, kcal: f.kcal, p: f.p, c: f.c, f: f.f, qty: 1 }] };
    });
  const setQty = (id: string, qty: number) =>
    editDay((d) => ({ ...d, items: qty <= 0 ? d.items.filter((i) => i.id !== id) : d.items.map((i) => (i.id === id ? { ...i, qty } : i)) }));

  if (!days || !prof) return <p className="h-40 animate-pulse rounded-2xl bg-surface-2" aria-label="Đang tải" />;

  return (
    <div className="space-y-4">
      {offline && <p className="rounded-xl bg-warn/10 px-3 py-2 text-sm text-warn">Đang không kết nối được máy chủ — vẫn ghi được, sẽ gửi lại khi có mạng.</p>}

      {/* chọn ngày */}
      <div className="flex items-center justify-between gap-2">
        <button type="button" aria-label="Ngày trước" onClick={() => setCur(shiftDay(cur, -1))} className="grid h-11 w-11 place-items-center rounded-xl border border-line bg-panel">
          <ChevronLeft size={20} />
        </button>
        <div className="text-center">
          <p className="font-bold text-ink">{cur === today ? "Hôm nay" : fmtDay(cur)}</p>
          <p className="text-xs text-muted">{dirtyDay || dirtyProf ? "Đang lưu…" : sync === "pending" ? "Chưa gửi được — sẽ gửi lại" : sync === "ok" ? "Đã lưu" : cur === today ? fmtDay(cur) : ""}</p>
        </div>
        <button
          type="button"
          aria-label="Ngày sau"
          disabled={cur >= today}
          onClick={() => setCur(shiftDay(cur, 1))}
          className="grid h-11 w-11 place-items-center rounded-xl border border-line bg-panel disabled:opacity-40"
        >
          <ChevronRight size={20} />
        </button>
      </div>

      {/* tổng trong ngày */}
      <Card>
        {t ? (
          <>
            <div className="flex items-baseline justify-between gap-2">
              <p className="text-sm font-semibold text-muted">Năng lượng</p>
              <p className="tabular-nums text-ink">
                <b className="text-2xl">{vn(eaten.kcal, 0)}</b> <span className="text-muted">/ {vn(t.kcal, 0)} kcal</span>
              </p>
            </div>
            <Bar value={eaten.kcal} max={t.kcal} tone={eaten.kcal > t.kcal * 1.1 ? "bg-warn" : "bg-primary"} />
            <div className="mt-3 flex items-baseline justify-between gap-2">
              <p className="text-sm font-semibold text-muted">Đạm</p>
              <p className="tabular-nums text-ink">
                <b className="text-xl">{vn(eaten.p, 0)}</b> <span className="text-muted">/ {t.p} g</span>
              </p>
            </div>
            <Bar value={eaten.p} max={t.p} tone={eaten.p >= t.pRange[0] ? "bg-ok" : "bg-primary"} />
            <p className="mt-3 text-sm text-muted">
              Tinh bột {vn(eaten.c, 0)}/{t.c} g · Chất béo {vn(eaten.f, 0)}/{t.f} g
            </p>
            <p className="mt-1 text-sm font-semibold text-ink">
              {eaten.kcal < t.kcal ? `Còn ${vn(t.kcal - eaten.kcal, 0)} kcal` : `Đã đủ năng lượng`}
              {eaten.p < t.pRange[0] && ` · thiếu ${vn(t.pRange[0] - eaten.p, 0)} g đạm`}
            </p>
          </>
        ) : (
          <p className="text-sm text-ink">Điền <b>năm sinh</b> ở mục “Mục tiêu của tôi” bên dưới để tính năng lượng cần mỗi ngày.</p>
        )}
      </Card>

      {/* món đã ăn */}
      <Card>
        <h2 className="mb-2 font-bold text-ink">Đã ăn ({day.items.length} món)</h2>
        {day.items.length === 0 && <p className="text-sm text-muted">Chưa ghi món nào.</p>}
        <ul className="divide-y divide-line">
          {day.items.map((i) => (
            <li key={i.id} className="flex items-center gap-2 py-2">
              <div className="min-w-0 flex-1">
                <p className="truncate font-semibold text-ink">{i.name}</p>
                <p className="text-xs text-muted">
                  {vn(i.qty, 1)} × {i.unit} · {vn(i.kcal * i.qty, 0)} kcal · {vn(i.p * i.qty, 0)} g đạm
                </p>
              </div>
              <button type="button" aria-label={`Bớt ${i.name}`} onClick={() => setQty(i.id, i.qty - 0.5)} className="grid h-10 w-10 place-items-center rounded-lg bg-surface-2">
                {i.qty <= 0.5 ? <Trash2 size={16} /> : <Minus size={16} />}
              </button>
              <button type="button" aria-label={`Thêm ${i.name}`} onClick={() => setQty(i.id, i.qty + 0.5)} className="grid h-10 w-10 place-items-center rounded-lg bg-surface-2">
                <Plus size={16} />
              </button>
            </li>
          ))}
        </ul>
        <button type="button" onClick={() => setPicker(true)} className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-bold text-white">
          <Plus size={18} /> Thêm món
        </button>
        <label className="mt-3 flex items-center justify-between gap-3 text-sm text-ink">
          <span>
            Cân buổi sáng <span className="text-muted">(kg, tuỳ chọn)</span>
          </span>
          <NumInput
            label="Cân buổi sáng (kg)"
            value={day.weight_kg}
            onChange={(n) => editDay((d) => ({ ...d, weight_kg: n }))}
            placeholder={vn(kg, 1)}
            className="w-24 text-right"
          />
        </label>
      </Card>

      {/* xu hướng cân + chỉnh */}
      <Card>
        <h2 className="mb-2 font-bold text-ink">Xu hướng cân theo tuần</h2>
        {weeks.length > 0 && (
          <ul className="mb-2 grid grid-cols-2 gap-2 text-sm sm:grid-cols-4">
            {weeks.slice(0, 4).map((w) => (
              <li key={w.week} className="rounded-xl bg-surface-2 px-2 py-1.5">
                <p className="text-xs text-muted">Tuần {fmtDay(w.week).slice(3)}</p>
                <p className="font-bold tabular-nums text-ink">
                  {vn(w.avg, 1)} kg <span className="text-xs font-normal text-muted">({w.n} lần)</span>
                </p>
              </li>
            ))}
          </ul>
        )}
        {advice && <p className="text-sm text-ink">{advice.text}</p>}
        {advice && advice.delta !== 0 && (
          <button
            type="button"
            onClick={() => editProf({ kcal_adjust: (prof.kcal_adjust ?? 0) + advice.delta })}
            className="mt-2 min-h-11 rounded-xl border border-primary px-4 text-sm font-bold text-primary"
          >
            Áp dụng {advice.delta > 0 ? "+" : ""}
            {advice.delta} kcal
          </button>
        )}
      </Card>

      {/* gợi ý theo kiểu build (từ trang Số đo) */}
      {prof && bodyLast && (() => {
        const b = analyzeBuild(bodyLast, prof.sex ?? "nam");
        if (!b || b.goal === prof.goal) return null;
        return (
          <Card className="border-primary/50">
            <p className="font-bold text-ink">Theo kiểu build của bạn: {b.label}</p>
            <p className="mt-1 text-sm text-ink">Gợi ý đổi mục tiêu sang <b>{GOAL_LABEL[b.goal]}</b> — {b.goalWhy}.</p>
            <button type="button" onClick={() => editProf({ goal: b.goal })} className="mt-2 min-h-11 rounded-xl bg-primary px-4 text-sm font-bold text-white">
              Dùng mục tiêu {GOAL_LABEL[b.goal]}
            </button>
          </Card>
        );
      })()}

      {/* hồ sơ + công thức */}
      <Card>
        <h2 className="mb-3 font-bold text-ink">Mục tiêu của tôi</h2>
        <div className="space-y-3">
          <label className="flex items-center justify-between gap-3 text-sm text-ink">
            Năm sinh
            <NumInput label="Năm sinh" value={prof.birth_year} onChange={(n) => editProf({ birth_year: n && n > 1900 && n < year ? Math.round(n) : null })} placeholder="VD 1990" className="w-28 text-right" />
          </label>
          <Seg value={prof.sex ?? "nam"} options={[{ v: "nam", label: "Nam" }, { v: "nu", label: "Nữ" }]} onChange={(v) => editProf({ sex: v })} />
          <div>
            <p className="mb-1 text-sm text-ink">Mức vận động</p>
            <Seg value={prof.activity} options={ACTIVITY.map((a) => ({ v: a.v, label: a.label }))} onChange={(v) => editProf({ activity: v })} />
            <p className="mt-1 text-xs text-muted">{ACTIVITY.find((a) => a.v === prof.activity)?.hint}</p>
          </div>
          <div>
            <p className="mb-1 text-sm text-ink">Mục tiêu</p>
            <Seg value={prof.goal} options={(Object.keys(GOAL_LABEL) as Goal[]).map((g) => ({ v: g, label: GOAL_LABEL[g] }))} onChange={(v) => editProf({ goal: v })} />
          </div>
        </div>
        {t && (
          <dl className="mt-4 space-y-1 rounded-xl bg-surface-2 p-3 text-sm tabular-nums">
            <div className="flex justify-between">
              <dt className="text-muted">Chuyển hoá cơ bản ({t.age} tuổi, {vn(kg, 1)} kg, {vn(cm, 0)} cm)</dt>
              <dd className="text-ink">{vn(t.bmr, 0)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-muted">× vận động {vn(prof.activity, 3)} = duy trì</dt>
              <dd className="text-ink">{vn(t.tdee, 0)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-muted">{GOAL_LABEL[prof.goal]}</dt>
              <dd className="text-ink">{GOAL_KCAL[prof.goal] >= 0 ? "+" : ""}{GOAL_KCAL[prof.goal]}</dd>
            </div>
            <div className="flex items-center justify-between">
              <dt className="text-muted">Đã chỉnh theo cân</dt>
              <dd className="flex items-center gap-2 text-ink">
                {prof.kcal_adjust >= 0 ? "+" : ""}
                {prof.kcal_adjust}
                {prof.kcal_adjust !== 0 && (
                  <button type="button" aria-label="Bỏ chỉnh" onClick={() => editProf({ kcal_adjust: 0 })} className="text-muted">
                    <X size={14} />
                  </button>
                )}
              </dd>
            </div>
            <div className="flex justify-between border-t border-line pt-1 font-bold">
              <dt className="text-ink">Mục tiêu mỗi ngày</dt>
              <dd className="text-ink">{vn(t.kcal, 0)} kcal</dd>
            </div>
            <p className="pt-1 text-xs text-muted">
              Đạm {t.p} g ({t.pRange[0]}–{t.pRange[1]} g = 1,6–2,2 g/kg) · béo ~27% · còn lại tinh bột. Công thức Mifflin–St Jeor, sai số khoảng ±10% — xu hướng cân mới là số
              quyết định.
            </p>
          </dl>
        )}
      </Card>

      {picker && <FoodPicker recents={recents} onPick={addFood} onClose={() => setPicker(false)} />}
    </div>
  );
}

function FoodPicker({ recents, onPick, onClose }: { recents: FoodItem[]; onPick: (f: Omit<Food, "group">) => void; onClose: () => void }) {
  const [q, setQ] = useState("");
  const [added, setAdded] = useState<string | null>(null);
  const [cName, setCName] = useState("");
  const [cKcal, setCKcal] = useState<number | null>(null);
  const [cP, setCP] = useState<number | null>(null);
  const norm = (s: string) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/gi, "d").toLowerCase();
  const hits = q ? FOODS.filter((f) => norm(f.name).includes(norm(q))) : FOODS;
  const groups = [...new Set(hits.map((f) => f.group))];
  const pick = (f: Omit<Food, "group">) => {
    onPick(f);
    setAdded(f.name);
  };
  const row = (f: Omit<Food, "group">) => (
    <li key={f.id}>
      <button type="button" onClick={() => pick(f)} className="flex min-h-12 w-full items-center gap-3 py-2 text-left">
        <span className="min-w-0 flex-1">
          <span className="block font-semibold text-ink">{f.name}</span>
          <span className="block text-xs text-muted">
            {f.unit} · {f.kcal} kcal · {vn(f.p, 0)} g đạm
          </span>
        </span>
        <Plus size={18} className="shrink-0 text-primary" />
      </button>
    </li>
  );
  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-panel" role="dialog" aria-label="Thêm món">
      <div className="flex items-center gap-2 border-b border-line p-3">
        <label className="flex min-h-11 flex-1 items-center gap-2 rounded-xl bg-surface-2 px-3">
          <Search size={18} className="text-muted" />
          <input autoFocus value={q} onChange={(e) => setQ(e.target.value)} placeholder="Tìm món (vd: com, trung)" className="w-full bg-transparent text-ink outline-none" />
        </label>
        <button type="button" onClick={onClose} className="min-h-11 rounded-xl bg-primary px-4 text-sm font-bold text-white">
          Xong
        </button>
      </div>
      {/* luôn chiếm chỗ để danh sách không nhảy khi bấm liên tiếp */}
      <p className={`h-8 px-4 py-1.5 text-sm ${added ? "bg-ok/10 text-ok" : "text-muted"}`} aria-live="polite">
        {added ? `Đã thêm: ${added}` : "Bấm một món để thêm 1 phần"}
      </p>
      <div className="flex-1 overflow-y-auto px-4 pb-8">
        {!q && recents.length > 0 && (
          <section>
            <h3 className="mt-3 text-xs font-bold uppercase tracking-wide text-muted">Hay ăn</h3>
            <ul className="divide-y divide-line">
              {recents.map((f) => (
                row(f)
              ))}
            </ul>
          </section>
        )}
        {groups.map((g) => (
          <section key={g}>
            <h3 className="mt-3 text-xs font-bold uppercase tracking-wide text-muted">{g}</h3>
            <ul className="divide-y divide-line">
              {hits
                .filter((f) => f.group === g)
                .map((f) => (
                  row(f)
                ))}
            </ul>
          </section>
        ))}
        <section className="mt-4 rounded-xl border border-line p-3">
          <h3 className="text-sm font-bold text-ink">Món khác (tự nhập)</h3>
          <input value={cName} onChange={(e) => setCName(e.target.value)} placeholder="Tên món" aria-label="Tên món" className="mt-2 min-h-11 w-full rounded-lg border border-line bg-panel px-3 text-ink" />
          <div className="mt-2 grid grid-cols-2 gap-2 text-sm text-muted">
            <label>
              kcal / phần
              <NumInput label="kcal một phần" value={cKcal} onChange={setCKcal} className="mt-1 w-full" />
            </label>
            <label>
              Đạm (g)
              <NumInput label="Đạm gam một phần" value={cP} onChange={setCP} className="mt-1 w-full" />
            </label>
          </div>
          <button
            type="button"
            disabled={!cName.trim() || cKcal == null}
            onClick={() => {
              pick({ id: `tu-${newId()}`, name: cName.trim(), unit: "1 phần", kcal: cKcal ?? 0, p: cP ?? 0, c: 0, f: 0 });
              setCName("");
              setCKcal(null);
              setCP(null);
            }}
            className="mt-2 min-h-11 w-full rounded-xl border border-primary text-sm font-bold text-primary disabled:opacity-40"
          >
            Thêm món này
          </button>
        </section>
      </div>
    </div>
  );
}
