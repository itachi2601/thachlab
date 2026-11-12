"use client";

/**
 * components/physics/ChargeInFieldSimulation.tsx — C2 (content/thi-nghiem/de-xuat-bo-sung-2026-11-12.md mục C)
 *
 * Hạt mang điện bay vào từ trường đều, vận tốc vuông góc với đường sức (B⃗ hướng vào mặt phẳng hình). Học sinh đổi v, B,
 * dấu và độ lớn q, khối lượng m; thấy quỹ đạo tròn, bán kính r = mv/(|q|B), chu kì T = 2πm/(|q|B), tốc độ không đổi,
 * lực từ luôn vuông góc vận tốc. Bẫy cần lộ: lực từ không sinh công; T không phụ thuộc v; v = 0 thì không có lực.
 *
 * Hằng số theo SGK: e = 1,6·10⁻¹⁹ C; 1 u = 1,66·10⁻²⁷ kg. Bỏ qua trọng lực. Khung hình 50 cm × 50 cm, tâm quỹ đạo
 * luôn ở giữa khung (hạt vào từ phía dưới tâm với q > 0, phía trên với q < 0, vận tốc ban đầu hướng sang phải).
 * Hình chạy chậm 4 triệu lần (1 µs ↔ 4 s) và chỉ chạy khi học sinh bấm, tự dừng sau 3 vòng (B4).
 *
 * Quy tắc UI (docs/QUY-TAC-THIET-KE.md): T2/V7 (hai câu đoán khoá hình và khoá chu kì), N2 (≤ 3 nút mỗi hàng),
 * D2 (nút ≥ 44 px), M3/M4 (v⃗ màu nhấn, F⃗ màu cảnh báo, kèm chữ), H3 (nhãn trên hình), N8 (số đo cạnh hình).
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { PredictGate, vn, vnSci, type PredictOption } from "./PredictGate";

const E = 1.6e-19; // C
const U = 1.66e-27; // kg
const SLOW = 4e6; // 1 µs vật lí ↔ 4 s trên màn
const MAX_LAPS = 3;

const VIEW = 300; // đơn vị viewBox
const PX_PER_M = 600; // 50 cm ↔ 300 đơn vị
const C = VIEW / 2;

const V_MAX = 0.6; // ×10⁶ m/s — cùng B_MIN, m = 4 u, |q| = e cho r lớn nhất 24,9 cm (vừa khung 50 cm)
const B_MIN = 0.1;
const B_MAX = 0.3;
const F_MAX = 2 * E * V_MAX * 1e6 * B_MAX;

/* ---------------- Câu dự đoán ---------------- */

const Q_SPEED: { question: string; options: PredictOption[] } = {
  question:
    "Một hạt mang điện bay vào vùng từ trường đều với vận tốc vuông góc với các đường sức từ. Bỏ qua trọng lực. Trong từ trường, tốc độ của hạt",
  options: [
    { text: "tăng dần vì lực từ kéo hạt.", why: "Lực từ luôn vuông góc với vận tốc nên không kéo hạt nhanh lên." },
    { text: "giảm dần vì lực từ cản hạt.", why: "Lực từ không ngược chiều chuyển động nên không cản hạt." },
    {
      text: "không đổi.",
      correct: true,
      why: "Lực từ luôn vuông góc với vận tốc nên công của nó bằng 0: động năng và tốc độ không đổi, lực chỉ làm đổi hướng vận tốc.",
    },
    {
      text: "lúc tăng lúc giảm theo vị trí trên quỹ đạo.",
      why: "Không có lúc nào lực từ có thành phần dọc theo vận tốc.",
    },
  ],
};

const Q_PERIOD: { question: string; options: PredictOption[] } = {
  question: "Giữ nguyên hạt và cảm ứng từ B, tăng tốc độ v lên gấp đôi. Chu kì quay T của hạt",
  options: [
    { text: "tăng gấp đôi.", why: "Bán kính tăng gấp đôi, nhưng hạt cũng chạy nhanh gấp đôi." },
    { text: "giảm một nửa.", why: "Hạt chạy nhanh hơn nhưng một vòng cũng dài hơn đúng bấy nhiêu." },
    {
      text: "không đổi.",
      correct: true,
      why: "r = mv/(|q|B) tăng gấp đôi nên chu vi 2πr cũng gấp đôi; T = 2πr/v = 2πm/(|q|B) không chứa v.",
    },
    { text: "tăng gấp bốn.", why: "T = 2πm/(|q|B) không chứa v nên không đổi theo v, càng không thể gấp bốn." },
  ],
};

/* ---------------- Định dạng ---------------- */

function fmtLength(m: number) {
  if (m === 0) return "0";
  if (m < 0.01) return `${vn(m * 1000, 1)} mm`;
  return `${vn(m * 100, 1)} cm`;
}

/* ---------------- Mũi tên ---------------- */

function Arrow({
  x,
  y,
  dx,
  dy,
  color,
  label,
}: {
  x: number;
  y: number;
  dx: number;
  dy: number;
  color: string;
  label: string;
}) {
  const len = Math.hypot(dx, dy);
  if (len < 1) return null;
  const ux = dx / len;
  const uy = dy / len;
  const tipX = x + dx;
  const tipY = y + dy;
  const h = 9;
  const w = 5;
  const head = `M${tipX},${tipY} L${tipX - ux * h - uy * w},${tipY - uy * h + ux * w} L${tipX - ux * h + uy * w},${tipY - uy * h - ux * w} Z`;
  return (
    <g>
      <line
        x1={x}
        y1={y}
        x2={tipX - ux * h * 0.8}
        y2={tipY - uy * h * 0.8}
        stroke={color}
        strokeWidth={3}
        strokeLinecap="round"
      />
      <path d={head} fill={color} />
      <text
        x={tipX + ux * 12}
        y={tipY + uy * 12 + 5}
        textAnchor="middle"
        fill={color}
        fontSize={15}
        fontWeight={700}
        fontStyle="italic"
      >
        {label}
      </text>
    </g>
  );
}

/* ---------------- Component chính ---------------- */

const segBtn = (on: boolean) =>
  `min-h-11 flex-1 rounded-lg px-2 text-sm font-medium transition active:scale-[0.98] disabled:opacity-50 ${
    on ? "bg-primary text-white" : "border border-line-strong bg-panel text-ink hover:bg-primary-soft"
  }`;

export default function ChargeInFieldSimulation() {
  const [sign, setSign] = useState<1 | -1>(1);
  const [qMag, setQMag] = useState<1 | 2>(2);
  const [mU, setMU] = useState<1 | 2 | 4>(4);
  const [v6, setV6] = useState(0.5); // ×10⁶ m/s
  const [B, setB] = useState(0.1); // T
  const [ghost, setGhost] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [t, setTState] = useState(0); // s (vật lí)
  const tRef = useRef(0);
  const setT = useCallback((x: number) => {
    tRef.current = x;
    setTState(x);
  }, []);
  const [q1, setQ1] = useState<number | null>(null);
  const [q2, setQ2] = useState<number | null>(null);

  const q = qMag * E;
  const m = mU * U;
  const v = v6 * 1e6;
  const r = (m * v) / (q * B);
  const T = (2 * Math.PI * m) / (q * B);
  const F = q * v * B;
  const Wd = 0.5 * m * v * v;
  const moving = v > 0;
  const laps = moving ? t / T : 0;

  // Đổi tham số → hạt quay lại điểm vào (giữ trạng thái chạy/dừng).
  const restart = useCallback(() => setT(0), [setT]);
  const setParam =
    <X,>(setter: (x: X) => void) =>
    (x: X) => {
      setter(x);
      restart();
    };

  const limit = MAX_LAPS * T;

  useEffect(() => {
    if (!playing || !moving) return;
    let raf = 0;
    let last = performance.now();
    const step = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      const next = tRef.current + dt / SLOW;
      if (next >= limit) {
        setT(limit);
        setPlaying(false);
        return;
      }
      setT(next);
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [playing, moving, limit, setT]);

  // Toạ độ (toán học, y hướng lên) → viewBox.
  const phi0 = sign > 0 ? -Math.PI / 2 : Math.PI / 2;
  const phi = phi0 + (sign * 2 * Math.PI * t) / (moving ? T : 1);
  const rU = r * PX_PER_M;
  const pos = (radius: number, angle: number) => ({ x: C + radius * Math.cos(angle), y: C - radius * Math.sin(angle) });
  const P = pos(rU, phi);
  // tiếp tuyến theo chiều chuyển động, pháp tuyến hướng vào tâm (toạ độ màn hình)
  const tan = { x: -sign * Math.sin(phi), y: -sign * Math.cos(phi) };
  const nor = { x: -Math.cos(phi), y: Math.sin(phi) };
  const vLen = moving ? 22 + 38 * (v6 / V_MAX) : 0;
  const fLen = F > 0 ? 14 + 46 * (F / F_MAX) : 0;

  const trail = (() => {
    if (!moving || rU < 0.5) return "";
    const end = Math.min(laps, 1);
    const n = Math.max(2, Math.ceil(96 * end));
    const pts: string[] = [];
    for (let i = 0; i <= n; i++) {
      const a = phi0 + (sign * 2 * Math.PI * end * i) / n;
      const p = pos(rU, a);
      pts.push(`${i ? "L" : "M"}${p.x.toFixed(1)},${p.y.toFixed(1)}`);
    }
    return pts.join(" ");
  })();

  // Hạt v/2 vào CÙNG điểm, cùng hướng: quỹ đạo bán kính r/2 tiếp xúc trong tại điểm vào, tâm lệch r/2 về phía điểm vào.
  const Pg = { x: C + (rU / 2) * Math.cos(phi), y: C + (sign * rU) / 2 - (rU / 2) * Math.sin(phi) };
  const showGhost = ghost && q2 !== null && moving;

  const crosses: { x: number; y: number }[] = [];
  for (let i = 15; i < VIEW; i += 30) for (let j = 15; j < VIEW - 30; j += 30) crosses.push({ x: i, y: j });

  if (q1 === null) {
    return (
      <section
        className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
        aria-label="Mô phỏng hạt mang điện trong từ trường"
      >
        <h2 className="font-display text-lg font-semibold">Hạt mang điện trong từ trường đều</h2>
        <div className="mt-3">
          <PredictGate question={Q_SPEED.question} options={Q_SPEED.options} choice={q1} onChoose={setQ1} />
        </div>
        <p className="mt-2 text-sm text-muted">🔒 Mô phỏng mở sau khi em chọn.</p>
      </section>
    );
  }

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Mô phỏng hạt mang điện trong từ trường"
    >
      <h2 className="font-display text-lg font-semibold">Hạt mang điện trong từ trường đều</h2>
      <div className="mt-3">
        <PredictGate
          question={Q_SPEED.question}
          options={Q_SPEED.options}
          choice={q1}
          onChoose={() => {}}
          hint="Bấm Chạy và nhìn số đo tốc độ trong lúc hạt quay."
        />
      </div>

      <div className="mt-3 grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        {/* Sân khấu */}
        <div className="min-w-0">
          <div className="mx-auto max-w-[440px] rounded-lg border border-line bg-surface-2">
            <svg
              viewBox={`0 0 ${VIEW} ${VIEW}`}
              className="block h-auto w-full select-none"
              role="img"
              aria-label="Quỹ đạo của hạt trong từ trường"
            >
              {crosses.map((c) => (
                <path
                  key={`${c.x}-${c.y}`}
                  d={`M${c.x - 4},${c.y - 4} l8,8 M${c.x + 4},${c.y - 4} l-8,8`}
                  className="stroke-muted"
                  strokeOpacity={0.45}
                  strokeWidth={1.3}
                />
              ))}
              <text x={8} y={VIEW - 9} className="fill-muted" fontSize={12}>
                × : đường sức từ hướng vào trong · khung 50 cm
              </text>

              {trail && <path d={trail} fill="none" stroke="var(--color-cyan)" strokeWidth={2.5} strokeOpacity={0.8} />}
              {moving && rU >= 0.5 && <circle cx={C} cy={C} r={2.5} className="fill-muted" />}

              {showGhost && (
                <g>
                  <circle
                    cx={C}
                    cy={C + (sign * rU) / 2}
                    r={rU / 2}
                    fill="none"
                    className="stroke-muted"
                    strokeDasharray="4 4"
                    strokeWidth={1.5}
                  />
                  <circle cx={Pg.x} cy={Pg.y} r={6} className="fill-panel stroke-ink" strokeWidth={2} />
                  <text
                    x={Pg.x + nor.x * 16}
                    y={Pg.y + nor.y * 16 + 4}
                    textAnchor="middle"
                    className="fill-ink"
                    fontSize={12}
                  >
                    v/2
                  </text>
                </g>
              )}

              {moving && fLen > 0 && (
                <path
                  d={`M${P.x + tan.x * 9},${P.y + tan.y * 9} l${nor.x * 9},${nor.y * 9} l${-tan.x * 9},${-tan.y * 9}`}
                  fill="none"
                  className="stroke-ink"
                  strokeWidth={1.2}
                />
              )}
              <Arrow x={P.x} y={P.y} dx={tan.x * vLen} dy={tan.y * vLen} color="var(--color-primary)" label="v" />
              <Arrow x={P.x} y={P.y} dx={nor.x * fLen} dy={nor.y * fLen} color="var(--color-accent)" label="F" />
              <circle cx={P.x} cy={P.y} r={9} className="fill-ink" />
              <text x={P.x} y={P.y + 4.5} textAnchor="middle" className="fill-panel" fontSize={14} fontWeight={700}>
                {sign > 0 ? "+" : "−"}
              </text>
            </svg>
          </div>
          <p className="mt-1 text-center text-xs text-muted">
            Hình chạy chậm 4 triệu lần
            {q2 !== null && (
              <>
                {" "}
                · t = {vn(t * 1e6, 2)} µs{moving ? ` · vòng ${vn(Math.min(laps, MAX_LAPS), 2)}` : ""}
              </>
            )}
          </p>
          <div className="mt-2 flex gap-2">
            <button
              type="button"
              onClick={() => {
                if (t >= limit) setT(0);
                setPlaying((p) => !p);
              }}
              disabled={!moving}
              className={segBtn(true)}
            >
              {playing ? "❚❚ Dừng" : t > 0 && t < limit ? "▶ Chạy tiếp" : "▶ Chạy"}
            </button>
            <button
              type="button"
              onClick={() => {
                setPlaying(false);
                setT(0);
              }}
              className={segBtn(false)}
            >
              ↺ Về đầu
            </button>
            <button
              type="button"
              aria-pressed={ghost}
              onClick={() => setGhost((g) => !g)}
              disabled={q2 === null}
              className={segBtn(ghost)}
              title={q2 === null ? "Mở sau câu đoán về chu kì" : undefined}
            >
              Hạt v/2
            </button>
          </div>
        </div>

        {/* Điều khiển + số đo */}
        <div className="min-w-0 space-y-3 text-sm">
          <div className="grid grid-cols-[4.5rem_1fr] items-center gap-2">
            <span className="text-muted">Dấu q</span>
            <div className="flex gap-2">
              <button
                type="button"
                aria-pressed={sign > 0}
                onClick={() => setParam(setSign)(1)}
                className={segBtn(sign > 0)}
              >
                q &gt; 0
              </button>
              <button
                type="button"
                aria-pressed={sign < 0}
                onClick={() => setParam(setSign)(-1)}
                className={segBtn(sign < 0)}
              >
                q &lt; 0
              </button>
            </div>
            <span className="text-muted">|q|</span>
            <div className="flex gap-2">
              {([1, 2] as const).map((k) => (
                <button
                  key={k}
                  type="button"
                  aria-pressed={qMag === k}
                  onClick={() => setParam(setQMag)(k)}
                  className={segBtn(qMag === k)}
                >
                  {k === 1 ? "e" : "2e"}
                </button>
              ))}
            </div>
            <span className="text-muted">m</span>
            <div className="flex gap-2">
              {([1, 2, 4] as const).map((k) => (
                <button
                  key={k}
                  type="button"
                  aria-pressed={mU === k}
                  onClick={() => setParam(setMU)(k)}
                  className={segBtn(mU === k)}
                >
                  {k} u
                </button>
              ))}
            </div>
          </div>

          <label className="block">
            <span className="flex justify-between text-muted">
              <span>Tốc độ vào v</span>
              <span className="font-mono text-ink">{moving ? `${vnSci(v, 2)} m/s` : "0"}</span>
            </span>
            <input
              type="range"
              min={0}
              max={V_MAX}
              step={0.05}
              value={v6}
              onChange={(e) => {
                const x = Number(e.target.value);
                if (x === 0) setPlaying(false);
                setParam(setV6)(x);
              }}
              className="h-11 w-full cursor-pointer accent-[var(--color-primary)]"
              aria-label="Tốc độ vào v"
            />
          </label>
          <label className="block">
            <span className="flex justify-between text-muted">
              <span>Cảm ứng từ B</span>
              <span className="font-mono text-ink">{vn(B, 2)} T</span>
            </span>
            <input
              type="range"
              min={B_MIN}
              max={B_MAX}
              step={0.05}
              value={B}
              onChange={(e) => setParam(setB)(Number(e.target.value))}
              className="h-11 w-full cursor-pointer accent-[var(--color-primary)]"
              aria-label="Cảm ứng từ B"
            />
          </label>

          <dl className="grid grid-cols-2 gap-2">
            <div className="rounded-lg bg-surface-2 p-2">
              <dt className="text-muted">Tốc độ hạt lúc này</dt>
              <dd className="font-mono font-semibold">{moving ? `${vnSci(v, 2)} m/s` : "0"}</dd>
            </div>
            <div className="rounded-lg bg-surface-2 p-2">
              <dt className="text-muted">Lực từ F = |q|vB</dt>
              <dd className="font-mono font-semibold">{F > 0 ? `${vnSci(F, 2)} N` : "0"}</dd>
            </div>
            <div className="rounded-lg bg-surface-2 p-2">
              <dt className="text-muted">Bán kính r = mv/(|q|B)</dt>
              <dd className="font-mono font-semibold">{moving ? fmtLength(r) : "—"}</dd>
            </div>
            <div className="rounded-lg bg-surface-2 p-2">
              <dt className="text-muted">Chu kì T</dt>
              <dd className="font-mono font-semibold">
                {q2 === null ? "🔒 đoán trước" : moving ? `${vn(T * 1e6, 3)} µs` : "— (đứng yên)"}
              </dd>
            </div>
          </dl>
          <p className="rounded-lg bg-surface-2 p-2">
            Động năng W<sub>đ</sub> = ½mv² ={" "}
            <span className="font-mono font-semibold">{Wd > 0 ? `${vnSci(Wd, 2)} J` : "0"}</span>
            {moving && " — không đổi trong suốt chuyển động: lực từ không sinh công."}
          </p>
          {!moving && (
            <p className="rounded-lg border border-line-strong p-2">
              <b>v = 0</b> ⇒ F = |q|·v·B = 0: từ trường không tác dụng lực lên hạt đứng yên, hạt nằm yên.
            </p>
          )}
        </div>
      </div>

      <div className="mt-4 space-y-2 text-sm leading-relaxed">
        <PredictGate
          question={Q_PERIOD.question}
          options={Q_PERIOD.options}
          choice={q2}
          onChoose={setQ2}
          hint="Bấm “Hạt v/2” rồi Chạy: hai hạt quay hết vòng cùng lúc. Chu kì T = 2πm/(|q|B)."
        />
        <p>
          <b>Nhìn vào:</b> mũi tên F luôn chỉ vào tâm và vuông góc mũi tên v; số đo tốc độ không đổi.
        </p>
      </div>
    </section>
  );
}
