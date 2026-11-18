"use client";
import { useCallback, useEffect, useState } from "react";
import { TARGET } from "@/lib/tap-luyen/chuong-trinh";
import { deleteMeasurement, fetchMeasurements, saveMeasurement, type Measurement } from "@/lib/tap-luyen/store";
import { Card, LineChart, NumInput, fmtDay, todayIso, vn } from "./ui";

const FIELDS: { k: keyof Measurement; label: string; unit: string }[] = [
  { k: "weight_kg", label: "Cân nặng", unit: "kg" },
  { k: "chest_cm", label: "Ngực", unit: "cm" },
  { k: "waist_cm", label: "Eo", unit: "cm" },
  { k: "hip_cm", label: "Mông", unit: "cm" },
  { k: "shoulder_cm", label: "Vai (vòng)", unit: "cm" },
  { k: "arm_cm", label: "Bắp tay", unit: "cm" },
  { k: "height_cm", label: "Chiều cao", unit: "cm" },
];
type Rating = "tot" | "vua" | "yeu";
const RATE: Record<Rating, string> = { tot: "text-ok", vua: "text-warn", yeu: "text-danger" };

function ratios(m: Measurement, h: number) {
  const out: { name: string; v: string; note: string; r: Rating }[] = [];
  if (m.weight_kg) {
    const bmi = m.weight_kg / (h / 100) ** 2;
    out.push({ name: "BMI", v: vn(bmi), note: "18,5–23 bình thường (chuẩn châu Á)", r: bmi >= 18.5 && bmi < 23 ? "tot" : "vua" });
  }
  if (m.waist_cm) {
    const r = m.waist_cm / h;
    out.push({ name: "Eo / chiều cao", v: vn(r, 2), note: "dưới 0,5 là an toàn", r: r < 0.5 ? "tot" : "yeu" });
  }
  if (m.waist_cm && m.hip_cm) {
    const r = m.waist_cm / m.hip_cm;
    out.push({ name: "Eo / mông", v: vn(r, 2), note: "nam: dưới 0,9 là tốt", r: r < 0.9 ? "tot" : "vua" });
  }
  if (m.chest_cm && m.waist_cm) {
    const r = m.chest_cm / m.waist_cm;
    out.push({ name: "Ngực / eo", v: vn(r, 2), note: "điểm cần nâng — dáng chữ V rõ từ ~1,2 trở lên", r: r >= 1.2 ? "tot" : r >= 1.15 ? "vua" : "yeu" });
  }
  if (m.chest_cm && m.hip_cm) {
    const d = m.chest_cm - m.hip_cm;
    out.push({ name: "Ngực − mông", v: `${d > 0 ? "+" : d < 0 ? "−" : ""}${vn(Math.abs(d))} cm`, note: "ngực lớn hơn mông thì thân trên mới ra dáng", r: d > 0 ? "tot" : "yeu" });
  }
  return out;
}

const blank = (last?: Measurement): Measurement => ({
  measured_on: todayIso(),
  height_cm: last?.height_cm ?? TARGET.start.height,
  weight_kg: null, chest_cm: null, waist_cm: null, hip_cm: null, shoulder_cm: null, arm_cm: null, note: null,
});

export default function SoDo() {
  const [list, setList] = useState<Measurement[]>([]);
  const [form, setForm] = useState<Measurement | null>(null);
  const [busy, setBusy] = useState(false);
  const [metric, setMetric] = useState<keyof Measurement>("chest_cm");

  const [now] = useState(() => Date.now());
  const reload = useCallback(
    () =>
      fetchMeasurements().then((r) => {
        setList(r.list);
      }),
    [],
  );
  useEffect(() => {
    fetchMeasurements().then((r) => {
      setList(r.list);
    });
  }, []);

  // Mốc xuất phát thầy báo 18/11/2026 dùng khi chưa có số đo nào trong máy chủ
  const start: Measurement = list[0] ?? {
    measured_on: TARGET.start.date, height_cm: TARGET.start.height, weight_kg: TARGET.start.weight,
    chest_cm: TARGET.start.chest, waist_cm: TARGET.start.waist, hip_cm: TARGET.start.hip, shoulder_cm: null, arm_cm: null,
  };
  const latest = list[list.length - 1] ?? start;
  const h = [...list].reverse().find((m) => m.height_cm)?.height_cm ?? TARGET.start.height;
  const daysSince = Math.floor((now - new Date(`${latest.measured_on}T00:00:00`).getTime()) / 864e5);
  const due = daysSince >= TARGET.remeasureDays;

  const save = async () => {
    if (!form) return;
    setBusy(true);
    try {
      await saveMeasurement(form);
      setForm(null);
      await reload();
    } catch (e) {
      alert(`Chưa lưu được: ${e instanceof Error ? e.message : "lỗi"}. Bảng số đo có thể chưa được tạo trên máy chủ.`);
    } finally {
      setBusy(false);
    }
  };

  const series = list.filter((m) => m[metric] != null).map((m) => ({ x: m.measured_on, y: Number(m[metric]) }));
  const chestTarget = (start.chest_cm ?? TARGET.start.chest) + TARGET.chestGainCm[0];
  const d = (k: keyof Measurement) => (latest[k] != null && start[k] != null ? Number(latest[k]) - Number(start[k]) : null);
  const weeks = Math.max(1, (new Date(`${latest.measured_on}T00:00:00`).getTime() - new Date(`${start.measured_on}T00:00:00`).getTime()) / (7 * 864e5));
  const dw = d("weight_kg");
  const perWeek = dw != null && list.length >= 2 ? dw / weeks : null;

  return (
    <div className="space-y-3">

      <Card className={due ? "border-warn/60" : ""}>
        <div className="flex items-start gap-2">
          <div className="min-w-0 flex-1">
            <p className="font-bold text-ink">{list.length ? `Lần đo gần nhất · ${fmtDay(latest.measured_on)}` : "Mốc xuất phát 18/11 (chưa lưu)"}</p>
            <p className={`text-sm ${due ? "font-semibold text-warn" : "text-muted"}`}>
              {due ? `Đã ${daysSince} ngày — tới lúc đo lại.` : `Đo lại sau ${TARGET.remeasureDays - daysSince} ngày nữa · cùng giờ, cùng cách đo.`}
            </p>
          </div>
          <button type="button" onClick={() => setForm(form ? null : blank(latest))} className="min-h-11 shrink-0 rounded-xl bg-primary px-4 text-sm font-bold text-white">
            {form ? "Đóng" : "Ghi số đo"}
          </button>
        </div>

        {form && (
          <div className="mt-3 rounded-xl bg-surface-2 p-3">
            <label className="block text-sm font-semibold text-ink">
              Ngày đo
              <input type="date" value={form.measured_on} onChange={(e) => setForm({ ...form, measured_on: e.target.value })} className="mt-1 h-11 w-full rounded-lg border border-line bg-panel px-3 text-base text-ink" />
            </label>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {FIELDS.map((f) => (
                <label key={f.k} className="text-sm font-semibold text-ink">
                  {f.label} ({f.unit})
                  <NumInput label={f.label} value={form[f.k] as number | null} placeholder={latest[f.k] != null ? String(latest[f.k]).replace(".", ",") : ""} onChange={(n) => setForm({ ...form, [f.k]: n })} className="mt-1 bg-panel" />
                </label>
              ))}
            </div>
            {!list.length && (
              <button type="button" onClick={() => setForm({ ...start, measured_on: TARGET.start.date, note: "Mốc xuất phát" })} className="mt-2 min-h-11 text-sm font-semibold text-primary">
                Điền mốc 18/11 (53 kg · 82–72–85)
              </button>
            )}
            <button type="button" disabled={busy} onClick={save} className="mt-2 min-h-12 w-full rounded-xl bg-primary text-sm font-bold text-white disabled:opacity-60">
              {busy ? "Đang lưu…" : "Lưu số đo"}
            </button>
          </div>
        )}

        <dl className="mt-3 grid grid-cols-3 gap-2 text-center">
          {(["weight_kg", "chest_cm", "waist_cm", "hip_cm", "shoulder_cm", "arm_cm"] as const).map((k) => {
            const f = FIELDS.find((x) => x.k === k)!;
            const delta = d(k);
            if (latest[k] == null) return null;
            const good = k === "waist_cm" ? (delta ?? 0) <= 0.5 : (delta ?? 0) >= 0;
            return (
              <div key={k} className="rounded-xl bg-surface-2 py-2">
                <dt className="text-xs text-muted">{f.label}</dt>
                <dd className="text-lg font-bold tabular-nums text-ink">{vn(Number(latest[k]))}</dd>
                {delta != null && list.length >= 2 && <dd className={`text-xs font-semibold tabular-nums ${good ? "text-ok" : "text-warn"}`}>{delta > 0 ? "+" : ""}{vn(delta)} {f.unit}</dd>}
              </div>
            );
          })}
        </dl>
      </Card>

      <Card>
        <p className="font-bold text-ink">Chỉ số dáng người</p>
        <ul className="mt-2 divide-y divide-line">
          {ratios(latest, h).map((r) => (
            <li key={r.name} className="flex items-baseline gap-2 py-2">
              <span className="min-w-0 flex-1">
                <span className="block text-sm font-semibold text-ink">{r.name}</span>
                <span className="block text-xs text-muted">{r.note}</span>
              </span>
              <span className={`text-lg font-bold tabular-nums ${RATE[r.r]}`}>{r.v}</span>
            </li>
          ))}
        </ul>
      </Card>

      <Card>
        <p className="font-bold text-ink">Mục tiêu 4 tuần</p>
        <ul className="mt-2 space-y-1.5 text-sm text-ink">
          <li>• Ngực +{TARGET.chestGainCm[0]}–{TARGET.chestGainCm[1]} cm → ≥ {vn(chestTarget)} cm {latest.chest_cm != null && <b className={latest.chest_cm >= chestTarget ? "text-ok" : "text-muted"}>(đang {vn(latest.chest_cm)})</b>}</li>
          <li>• Eo giữ ≤ {TARGET.waistMax} cm {latest.waist_cm != null && <b className={latest.waist_cm <= TARGET.waistMax + 0.5 ? "text-ok" : "text-warn"}>(đang {vn(latest.waist_cm)})</b>}</li>
          <li>
            • Cân tăng {vn(TARGET.weightGainPerWeek[0], 2)}–{vn(TARGET.weightGainPerWeek[1], 2)} kg/tuần
            {perWeek != null && <b className={perWeek > 0.4 ? "text-warn" : perWeek < 0.05 ? "text-warn" : "text-ok"}> (đang {vn(perWeek, 2)} kg/tuần{perWeek > 0.4 ? " — nhanh quá, bớt 150–200 kcal" : perWeek < 0.05 ? " — đứng yên, thêm ~150 kcal" : ""})</b>}
          </li>
          <li>• Ăn trên duy trì {TARGET.surplusKcal[0]}–{TARGET.surplusKcal[1]} kcal; đạm {vn(TARGET.proteinGPerKg[0] * (latest.weight_kg ?? 53), 0)}–{vn(TARGET.proteinGPerKg[1] * (latest.weight_kg ?? 53), 0)} g/ngày</li>
        </ul>
      </Card>

      {list.length > 0 && (
        <Card>
          <div className="flex items-center gap-2">
            <p className="flex-1 font-bold text-ink">Biểu đồ</p>
            <select value={metric} onChange={(e) => setMetric(e.target.value as keyof Measurement)} className="h-11 rounded-xl border border-line bg-surface-2 px-2 text-base text-ink" aria-label="Chọn số đo">
              {FIELDS.filter((f) => f.k !== "height_cm").map((f) => <option key={f.k} value={f.k}>{f.label}</option>)}
            </select>
          </div>
          {series.length ? (
            <LineChart
              points={series}
              unit={FIELDS.find((f) => f.k === metric)?.unit ?? ""}
              target={metric === "chest_cm" ? { y: chestTarget, label: `mục tiêu ${vn(chestTarget)}` } : metric === "waist_cm" ? { y: TARGET.waistMax, label: `giữ ≤ ${TARGET.waistMax}` } : undefined}
            />
          ) : (
            <p className="mt-2 text-sm text-muted">Chưa có số liệu mục này.</p>
          )}
          <ul className="mt-2 divide-y divide-line text-sm">
            {[...list].reverse().map((m) => (
              <li key={m.measured_on} className="flex items-center gap-2 py-1.5">
                <span className="w-16 shrink-0 text-muted">{fmtDay(m.measured_on)}</span>
                <span className="min-w-0 flex-1 truncate tabular-nums text-ink">
                  {[m.weight_kg != null && `${vn(m.weight_kg)} kg`, m.chest_cm != null && m.waist_cm != null && m.hip_cm != null && `${vn(m.chest_cm)}–${vn(m.waist_cm)}–${vn(m.hip_cm)}`].filter(Boolean).join(" · ")}
                </span>
                <button type="button" onClick={async () => { if (confirm(`Xoá số đo ngày ${fmtDay(m.measured_on)}?`)) { await deleteMeasurement(m.measured_on).catch(() => alert("Chưa xoá được.")); reload(); } }} className="min-h-11 px-2 text-xs font-semibold text-danger">Xoá</button>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
