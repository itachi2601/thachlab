"use client";

/**
 * components/physics/GasGraphsSimulation.tsx — C1 (content/thi-nghiem/de-xuat-bo-sung-2026-11-12.md mục C)
 *
 * Khí lí tưởng, lượng khí không đổi. Học sinh chọn quá trình (đẳng nhiệt / đẳng tích / đẳng áp) rồi kéo điểm trạng thái;
 * ba đồ thị p–V, p–T, V–T cùng cập nhật. Công tắc K ↔ °C cho thấy đường kéo dài chỉ qua gốc O khi trục là kelvin.
 * Bẫy cần lộ: nhận nhầm quá trình khi đổi hệ trục (đường qua O trên V–T là đẳng áp, không phải đẳng tích…).
 *
 * Số liệu: chọn nR = 1 J/K (n ≈ 0,12 mol) để p(kPa)·V(L) = T(K); trạng thái đầu (1): 100 kPa, 3 L, 300 K. T = t + 273.
 *
 * Quy tắc UI (docs/QUY-TAC-THIET-KE.md): T2/V7 (hai đồ thị p–T, V–T khoá tới khi đoán), N2 (≤ 3 nút mỗi hàng),
 * D2 (tay cầm kéo 44×44 px, nút ≥ 44 px), D5 (không cần hover), H3/H4 (nhãn trên hình, chữ SVG ≥ 12 đơn vị ở bề rộng 320),
 * M3/M7 (màu theo token nền sáng), B4 (không gì tự chạy), N8 (dòng "Nhìn vào" ngay dưới đồ thị).
 * Kéo trên đồ thị bằng tay cầm HTML có touch-action:none — chạm vào chỗ khác vẫn cuộn trang được.
 */

import { useCallback, useMemo, useRef, useState, type PointerEvent as ReactPointerEvent } from "react";
import { PredictGate, vn, type PredictOption } from "./PredictGate";

type Process = "nhiet" | "tich" | "ap";
type TUnit = "K" | "C";
type GraphKey = "pV" | "pT" | "VT";

interface GasState {
  p: number; // kPa
  V: number; // L
  T: number; // K
}

const NR = 1; // kPa·L/K = J/K
const P0 = 100;
const V0 = 3;
const T0 = 300;
const ZERO_C = 273;

const PROCESS_LABEL: Record<Process, string> = { nhiet: "Đẳng nhiệt", tich: "Đẳng tích", ap: "Đẳng áp" };

/** Tham số tự do của từng quá trình: đẳng nhiệt kéo V, hai quá trình còn lại kéo T. */
const PARAM: Record<Process, { min: number; max: number; step: number; start: number; label: string; unit: string }> = {
  nhiet: { min: 1, max: 6, step: 0.1, start: V0, label: "Thể tích V", unit: "L" },
  tich: { min: 150, max: 600, step: 5, start: T0, label: "Nhiệt độ T", unit: "K" },
  ap: { min: 150, max: 600, step: 5, start: T0, label: "Nhiệt độ T", unit: "K" },
};

function stateOf(proc: Process, s: number): GasState {
  if (proc === "nhiet") return { V: s, T: T0, p: (NR * T0) / s };
  if (proc === "tich") return { T: s, V: V0, p: (NR * s) / V0 };
  return { T: s, p: P0, V: (NR * s) / P0 };
}

/* ---------------- Hình học SVG ---------------- */

const W = 320;
const H = 230;
const PL = 46; // lề trái (nhãn trục tung)
const PR = 16;
const PT = 16;
const PB = 36;

interface Axis {
  min: number;
  max: number;
  ticks: number[];
  label: string;
}

function tAxis(unit: TUnit): Axis {
  return unit === "K"
    ? { min: 0, max: 660, ticks: [200, 400, 600], label: "T (K)" }
    : { min: -300, max: 400, ticks: [100, 300], label: "t (°C)" };
}
const P_AXIS: Axis = { min: 0, max: 330, ticks: [100, 200, 300], label: "p (kPa)" };
const V_AXIS: Axis = { min: 0, max: 7, ticks: [2, 4, 6], label: "V (L)" };

function tVal(T: number, unit: TUnit) {
  return unit === "K" ? T : T - ZERO_C;
}

interface GraphSpec {
  key: GraphKey;
  title: string;
  x: Axis;
  y: Axis;
  xOf: (g: GasState) => number;
  yOf: (g: GasState) => number;
}

function graphSpecs(unit: TUnit): GraphSpec[] {
  const ta = tAxis(unit);
  return [
    { key: "pV", title: "Đồ thị p–V", x: V_AXIS, y: P_AXIS, xOf: (g) => g.V, yOf: (g) => g.p },
    {
      key: "pT",
      title: unit === "K" ? "Đồ thị p–T" : "Đồ thị p–t",
      x: ta,
      y: P_AXIS,
      xOf: (g) => tVal(g.T, unit),
      yOf: (g) => g.p,
    },
    {
      key: "VT",
      title: unit === "K" ? "Đồ thị V–T" : "Đồ thị V–t",
      x: ta,
      y: V_AXIS,
      xOf: (g) => tVal(g.T, unit),
      yOf: (g) => g.V,
    },
  ];
}

function sx(a: Axis, v: number) {
  return PL + ((v - a.min) / (a.max - a.min)) * (W - PL - PR);
}
function sy(a: Axis, v: number) {
  return H - PB - ((v - a.min) / (a.max - a.min)) * (H - PB - PT);
}

/* ---------------- Câu dự đoán (T2) ---------------- */

const OPT = {
  hyper: "Một nhánh hypebol",
  dung: "Đoạn thẳng vuông góc với trục nhiệt độ",
  ngang: "Đoạn thẳng song song với trục nhiệt độ",
  quaO: "Đường thẳng có phần kéo dài đi qua gốc toạ độ O",
};

const PREDICT: Record<Process, { ask: GraphKey; question: string; options: PredictOption[] }> = {
  nhiet: {
    ask: "pT",
    question:
      "Nén khí đẳng nhiệt (kéo điểm trên đồ thị p–V). Trên đồ thị p–T (trục nhiệt độ theo kelvin), quá trình này được biểu diễn bằng",
    options: [
      { text: OPT.hyper, why: "Hypebol là hình của đẳng nhiệt trên p–V (p tỉ lệ nghịch với V), không mang sang p–T." },
      { text: OPT.dung, correct: true, why: "T không đổi nên mọi trạng thái có cùng hoành độ T: một đoạn thẳng đứng." },
      { text: OPT.quaO, why: "Đường qua O trên p–T là đẳng tích (p tỉ lệ thuận với T)." },
      { text: OPT.ngang, why: "Song song trục nhiệt độ nghĩa là p không đổi — đó là đẳng áp." },
    ],
  },
  tich: {
    ask: "VT",
    question: "Đun nóng khí đẳng tích. Trên đồ thị V–T (trục nhiệt độ theo kelvin), quá trình này được biểu diễn bằng",
    options: [
      { text: OPT.quaO, why: "Đường qua O trên V–T là đẳng áp (V tỉ lệ thuận với T) — bẫy khi đổi hệ trục." },
      { text: OPT.ngang, correct: true, why: "V không đổi nên mọi trạng thái có cùng tung độ V: một đoạn nằm ngang." },
      { text: OPT.dung, why: "Vuông góc trục nhiệt độ nghĩa là T không đổi — đó là đẳng nhiệt." },
      { text: OPT.hyper, why: "Trên V–T, cả ba quá trình đều là đường thẳng, không có hypebol." },
    ],
  },
  ap: {
    ask: "pT",
    question: "Đun nóng khí đẳng áp. Trên đồ thị p–T (trục nhiệt độ theo kelvin), quá trình này được biểu diễn bằng",
    options: [
      { text: OPT.quaO, why: "Đường qua O trên p–T là đẳng tích; đẳng áp chỉ qua O trên đồ thị V–T." },
      { text: OPT.hyper, why: "Trên p–T, cả ba quá trình đều là đường thẳng, không có hypebol." },
      { text: OPT.ngang, correct: true, why: "p không đổi nên mọi trạng thái có cùng tung độ p: một đoạn nằm ngang." },
      { text: OPT.dung, why: "Vuông góc trục nhiệt độ nghĩa là T không đổi — đó là đẳng nhiệt." },
    ],
  },
};

const BAY: Record<Process, string> = {
  nhiet: "Đẳng nhiệt chỉ là hypebol trên p–V; trên p–T và V–T nó là đoạn thẳng đứng.",
  tich: "Trên V–T, đẳng tích là đoạn nằm ngang. Đường qua O trên V–T là đẳng áp — đọc tên trục trước khi đọc hình.",
  ap: "Trên p–T, đẳng áp là đoạn nằm ngang. Đường qua O trên p–T là đẳng tích — đọc tên trục trước khi đọc hình.",
};

/* ---------------- Một đồ thị ---------------- */

interface GraphProps {
  spec: GraphSpec;
  proc: Process;
  s: number;
  unit: TUnit;
  onParam: (s: number) => void;
}

const SAMPLES = 160;

function Graph({ spec, proc, s, unit, onParam }: GraphProps) {
  const boxRef = useRef<HTMLDivElement>(null);
  const range = PARAM[proc];
  const { x: ax, y: ay } = spec;

  const pt = (g: GasState) => ({ x: sx(ax, spec.xOf(g)), y: sy(ay, spec.yOf(g)) });

  const samples = useMemo(() => {
    const out: { s: number; x: number; y: number }[] = [];
    for (let i = 0; i <= SAMPLES; i++) {
      const v = range.min + ((range.max - range.min) * i) / SAMPLES;
      const g = stateOf(proc, v);
      out.push({ s: v, x: sx(ax, spec.xOf(g)), y: sy(ay, spec.yOf(g)) });
    }
    return out;
    // spec đổi theo unit; ax/ay là trường của spec
  }, [proc, range.min, range.max, spec, ax, ay]);

  const fullPath = samples.map((q, i) => `${i ? "L" : "M"}${q.x.toFixed(1)},${q.y.toFixed(1)}`).join(" ");
  const lo = Math.min(range.start, s);
  const hi = Math.max(range.start, s);
  const donePath = samples
    .filter((q) => q.s >= lo - 1e-9 && q.s <= hi + 1e-9)
    .map((q, i) => `${i ? "L" : "M"}${q.x.toFixed(1)},${q.y.toFixed(1)}`)
    .join(" ");

  // Đường kéo dài về T = 0 K cho hai đường "tỉ lệ thuận": đẳng tích trên p–T, đẳng áp trên V–T.
  const extrap =
    (proc === "tich" && spec.key === "pT") || (proc === "ap" && spec.key === "VT")
      ? { from: samples[0], to: { x: sx(ax, tVal(0, unit)), y: sy(ay, 0) } }
      : null;

  const a = pt(stateOf(proc, range.start));
  const b = pt(stateOf(proc, s));

  const nearest = useCallback(
    (clientX: number, clientY: number) => {
      const box = boxRef.current;
      if (!box) return;
      const r = box.getBoundingClientRect();
      const vx = ((clientX - r.left) / r.width) * W;
      const vy = ((clientY - r.top) / r.height) * H;
      let best = samples[0];
      let bd = Infinity;
      for (const q of samples) {
        const d = (q.x - vx) ** 2 + (q.y - vy) ** 2;
        if (d < bd) {
          bd = d;
          best = q;
        }
      }
      const snapped = Math.round(best.s / range.step) * range.step;
      onParam(Math.min(range.max, Math.max(range.min, snapped)));
    },
    [samples, range.step, range.min, range.max, onParam],
  );

  const onDown = (e: ReactPointerEvent<HTMLDivElement>) => {
    e.currentTarget.setPointerCapture(e.pointerId);
    nearest(e.clientX, e.clientY);
  };
  const onMove = (e: ReactPointerEvent<HTMLDivElement>) => {
    if (e.currentTarget.hasPointerCapture(e.pointerId)) nearest(e.clientX, e.clientY);
  };

  const yAxisX = sx(ax, Math.max(ax.min, 0));
  const xAxisY = sy(ay, 0);
  const fmtTick = (v: number) => (Number.isInteger(v) ? vn(v, 0) : vn(v, 1));

  return (
    <figure className="min-w-0">
      <figcaption className="mb-1 text-sm font-semibold text-ink">{spec.title}</figcaption>
      <div ref={boxRef} className="relative rounded-lg border border-line bg-panel">
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="block h-auto w-full select-none"
          role="img"
          aria-label={`${spec.title}: quá trình ${PROCESS_LABEL[proc].toLowerCase()}`}
          onClick={(e) => nearest(e.clientX, e.clientY)}
        >
          {/* lưới nhẹ */}
          {ay.ticks.map((t) => (
            <line
              key={`gy${t}`}
              x1={PL}
              x2={W - PR}
              y1={sy(ay, t)}
              y2={sy(ay, t)}
              className="stroke-line"
              strokeWidth={1}
            />
          ))}
          {ax.ticks.map((t) => (
            <line
              key={`gx${t}`}
              x1={sx(ax, t)}
              x2={sx(ax, t)}
              y1={PT}
              y2={H - PB}
              className="stroke-line"
              strokeWidth={1}
            />
          ))}

          {/* trục */}
          <line x1={PL} x2={W - PR + 4} y1={xAxisY} y2={xAxisY} className="stroke-muted" strokeWidth={1.5} />
          <path d={`M${W - PR + 4},${xAxisY} l-7,-4 v8 z`} className="fill-muted" />
          <line x1={yAxisX} x2={yAxisX} y1={H - PB} y2={PT - 6} className="stroke-muted" strokeWidth={1.5} />
          <path d={`M${yAxisX},${PT - 6} l-4,7 h8 z`} className="fill-muted" />
          <text x={yAxisX - 6} y={xAxisY + 15} textAnchor="end" className="fill-ink" fontSize={13} fontWeight={700}>
            O
          </text>

          {ay.ticks.map((t) => (
            <text key={`ty${t}`} x={yAxisX - 6} y={sy(ay, t) + 4} textAnchor="end" className="fill-muted" fontSize={13}>
              {fmtTick(t)}
            </text>
          ))}
          {ax.ticks.map((t) => (
            <text key={`tx${t}`} x={sx(ax, t)} y={H - PB + 16} textAnchor="middle" className="fill-muted" fontSize={13}>
              {fmtTick(t)}
            </text>
          ))}
          <text x={W - PR} y={H - 4} textAnchor="end" className="fill-ink" fontSize={14} fontStyle="italic">
            {ax.label}
          </text>
          <text x={yAxisX + 8} y={PT + 2} className="fill-ink" fontSize={14} fontStyle="italic">
            {ay.label}
          </text>

          {/* đường kéo dài (nét đứt) về 0 K */}
          {extrap && (
            <g>
              <line
                x1={extrap.from.x}
                y1={extrap.from.y}
                x2={extrap.to.x}
                y2={extrap.to.y}
                stroke="var(--color-cyan)"
                strokeWidth={2}
                strokeDasharray="6 5"
              />
              <circle cx={extrap.to.x} cy={extrap.to.y} r={4} fill="var(--color-cyan)" />
              {unit === "C" && (
                <text
                  x={extrap.to.x}
                  y={xAxisY + 16}
                  textAnchor="middle"
                  className="fill-ink"
                  fontSize={13}
                  fontWeight={700}
                >
                  −273
                </text>
              )}
            </g>
          )}

          {/* cả đường của quá trình (nhạt) + đoạn đã đi (đậm) */}
          <path d={fullPath} fill="none" stroke="var(--color-cyan)" strokeOpacity={0.35} strokeWidth={3} />
          {donePath && <path d={donePath} fill="none" stroke="var(--color-cyan)" strokeWidth={3.5} />}

          {/* trạng thái (1) và (2) */}
          <circle cx={a.x} cy={a.y} r={5} className="fill-panel" stroke="var(--color-ink)" strokeWidth={2} />
          <text x={a.x + 8} y={a.y - 8} className="fill-ink" fontSize={13}>
            (1)
          </text>
          <circle cx={b.x} cy={b.y} r={7} fill="var(--color-primary)" stroke="var(--color-panel)" strokeWidth={2} />
          <text x={b.x + 9} y={b.y + 16} className="fill-primary" fontSize={13} fontWeight={700}>
            (2)
          </text>
        </svg>
        {/* tay cầm kéo 44×44 px (D2); chỉ nó chặn cuộn trang */}
        <div
          aria-hidden
          onPointerDown={onDown}
          onPointerMove={onMove}
          className="absolute h-11 w-11 -translate-x-1/2 -translate-y-1/2 cursor-grab touch-none rounded-full ring-2 ring-primary/40 active:cursor-grabbing"
          style={{ left: `${(b.x / W) * 100}%`, top: `${(b.y / H) * 100}%` }}
        />
      </div>
    </figure>
  );
}

/* ---------------- Component chính ---------------- */

const segBtn = (on: boolean) =>
  `min-h-11 flex-1 rounded-lg px-2 text-sm font-medium transition active:scale-[0.98] ${
    on ? "bg-primary text-white" : "border border-line-strong bg-panel text-ink hover:bg-primary-soft"
  }`;

export default function GasGraphsSimulation() {
  const [proc, setProc] = useState<Process>("nhiet");
  const [s, setS] = useState<number>(PARAM.nhiet.start);
  const [unit, setUnit] = useState<TUnit>("K");
  const [guess, setGuess] = useState<Record<Process, number | null>>({ nhiet: null, tich: null, ap: null });

  const g = stateOf(proc, s);
  const g1 = stateOf(proc, PARAM[proc].start);
  const specs = useMemo(() => graphSpecs(unit), [unit]);
  const unlocked = guess[proc] !== null;
  const pv = specs[0];
  const others = specs.slice(1);

  const chooseProc = (p: Process) => {
    setProc(p);
    setS(PARAM[p].start);
  };

  const ratios = [
    { label: "p·V", value: `${vn(g.p * g.V, 0)} J`, fixed: proc === "nhiet" },
    { label: "p/T", value: `${vn((1000 * g.p) / g.T, 0)} Pa/K`, fixed: proc === "tich" },
    { label: "V/T", value: `${vn((1000 * g.V) / g.T, 1)} mL/K`, fixed: proc === "ap" },
  ];

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Mô phỏng ba đồ thị khí lí tưởng"
    >
      <h2 className="font-display text-lg font-semibold">Ba đồ thị của cùng một quá trình khí</h2>
      <p className="mt-1 text-sm leading-relaxed text-muted">
        Lượng khí không đổi. Chọn quá trình rồi kéo điểm (2) trên đồ thị p–V; điểm (1) là trạng thái đầu.
      </p>

      <div className="mt-3 flex gap-2" role="group" aria-label="Chọn quá trình">
        {(Object.keys(PROCESS_LABEL) as Process[]).map((p) => (
          <button
            key={p}
            type="button"
            aria-pressed={proc === p}
            onClick={() => chooseProc(p)}
            className={segBtn(proc === p)}
          >
            {PROCESS_LABEL[p]}
          </button>
        ))}
      </div>

      <div className="mt-3 grid gap-4 lg:grid-cols-3">
        <div className="min-w-0">
          <Graph spec={pv} proc={proc} s={s} unit={unit} onParam={setS} />
          <label className="mt-2 block text-sm">
            <span className="flex justify-between text-muted">
              <span>{PARAM[proc].label}</span>
              <span className="font-mono text-ink">
                {vn(s, proc === "nhiet" ? 1 : 0)} {PARAM[proc].unit}
              </span>
            </span>
            <input
              type="range"
              min={PARAM[proc].min}
              max={PARAM[proc].max}
              step={PARAM[proc].step}
              value={s}
              onChange={(e) => setS(Number(e.target.value))}
              className="mt-1 h-11 w-full cursor-pointer accent-[var(--color-primary)]"
              aria-label={`${PARAM[proc].label} của trạng thái (2)`}
            />
          </label>
          {/* Số đo p, V, T ẩn tới khi đoán: ô của đại lượng không đổi sẽ lộ đáp án (T2) */}
          {unlocked && (
            <dl className="mt-1 grid grid-cols-3 gap-2 text-center text-sm">
              <div className="rounded-lg bg-surface-2 px-1 py-1.5">
                <dt className="text-muted">p</dt>
                <dd className="font-mono font-semibold">{vn(g.p, 0)} kPa</dd>
              </div>
              <div className="rounded-lg bg-surface-2 px-1 py-1.5">
                <dt className="text-muted">V</dt>
                <dd className="font-mono font-semibold">{vn(g.V, 2)} L</dd>
              </div>
              <div className="rounded-lg bg-surface-2 px-1 py-1.5">
                <dt className="text-muted">T</dt>
                <dd className="font-mono font-semibold">
                  {vn(g.T, 0)} K
                  <span className="block text-xs font-normal text-muted">t = {vn(g.T - ZERO_C, 0)} °C</span>
                </dd>
              </div>
            </dl>
          )}
        </div>

        {unlocked ? (
          <div className="min-w-0 lg:col-span-2">
            <div className="flex items-center gap-2" role="group" aria-label="Đơn vị trục nhiệt độ">
              <span className="text-sm text-muted">Trục nhiệt độ:</span>
              <button
                type="button"
                aria-pressed={unit === "K"}
                onClick={() => setUnit("K")}
                className={segBtn(unit === "K")}
              >
                T (K)
              </button>
              <button
                type="button"
                aria-pressed={unit === "C"}
                onClick={() => setUnit("C")}
                className={segBtn(unit === "C")}
              >
                t (°C)
              </button>
            </div>
            <div className="mt-2 grid gap-4 sm:grid-cols-2">
              {others.map((sp) => (
                <Graph key={sp.key} spec={sp} proc={proc} s={s} unit={unit} onParam={setS} />
              ))}
            </div>
          </div>
        ) : (
          <div className="min-w-0 lg:col-span-2">
            <PredictGate
              question={PREDICT[proc].question}
              options={PREDICT[proc].options}
              choice={guess[proc]}
              onChoose={(i) => setGuess((old) => ({ ...old, [proc]: i }))}
            />
            <p className="mt-2 text-sm text-muted">🔒 Đồ thị p–T và V–T mở sau khi em chọn.</p>
          </div>
        )}
      </div>

      {unlocked && (
        <div className="mt-4 space-y-2 text-sm leading-relaxed">
          <PredictGate
            question={PREDICT[proc].question}
            options={PREDICT[proc].options}
            choice={guess[proc]}
            onChoose={() => {}}
            hint="Kéo điểm (2) trên bất kì đồ thị nào để tự kiểm."
          />
          <dl className="grid grid-cols-3 gap-2 text-center">
            {ratios.map((r) => (
              <div key={r.label} className={`rounded-lg px-1 py-1.5 ${r.fixed ? "bg-primary-soft" : "bg-surface-2"}`}>
                <dt className="text-muted">{r.label}</dt>
                <dd className="font-mono font-semibold">{r.value}</dd>
                <dd className={`text-xs ${r.fixed ? "font-semibold text-primary" : "text-muted"}`}>
                  {r.fixed
                    ? "không đổi"
                    : `(1): ${r.label === "p·V" ? vn(g1.p * g1.V, 0) : r.label === "p/T" ? vn((1000 * g1.p) / g1.T, 0) : vn((1000 * g1.V) / g1.T, 1)}`}
                </dd>
              </div>
            ))}
          </dl>
          <p>
            <b>Nhìn vào:</b>{" "}
            {proc === "nhiet"
              ? "cùng một quá trình nhưng mỗi hệ trục vẽ một hình khác nhau."
              : unit === "K"
                ? "đường nét đứt kéo dài tới gốc O. Bấm t (°C) xem nó còn qua O không."
                : "trục °C: đường nét đứt cắt trục ngang tại −273 °C, không qua gốc O — vẫn là cùng một quá trình."}
          </p>
          <p>
            <b>Bẫy đề hay gài:</b> {BAY[proc]}
          </p>
        </div>
      )}
    </section>
  );
}
