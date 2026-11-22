"use client";

/**
 * components/physics/CurrentBalanceSimulation.tsx — mô phỏng tự kéo "cân dòng điện" (việc 5,
 * docs/KE-HOACH-CAI-TIEN-CLIP-2026-11-19.md), đặt sau clip tn-l12-thuchanhtu-04 ở L12 Bài 11 (lesson 12).
 *
 * Nam châm chữ U đặt trên cân, đoạn dây trong khe gá trên giá riêng (không chạm cân). Học sinh chọn I = 0…5 A và chiều
 * dòng; cân đọc phản lực F′ của lực từ lên nam châm: Δm = ±F/g. Số cân lấy NGUYÊN VĂN cột "Δm đo" của
 * content/thi-nghiem/tn-l12-thuchanhtu-04.json (so_lieu_mau, mô hình B = 0,12 T, l = 4,0 cm, g = 9,81 m/s²) để khớp clip
 * và bảng trong bài; F = Δm·g và B = F/(I·l) tính ra từ đó (khớp cột mN và T của kho).
 * Bẫy cần lộ (hien_tuong_hay_sai của kho): "đảo chiều thì cân về 0" (đã hỏi trong clip) và "B suy ra đổi theo I" (câu đoán 2).
 *
 * Quy tắc UI (docs/QUY-TAC-THIET-KE.md): T2/V7 (câu đoán khoá mô phỏng, câu đoán 2 khoá cột B), E1/E4 (A. B. C. D., font đề),
 * L1/L3 (phản hồi có lí do, không điểm), D2 (thanh trượt và nút cao 44 px), N2 (≤ 3 thao tác mỗi hàng),
 * N8 (số cân ngay cạnh hình), H3 (nhãn trên hình), M3/M4 (F, F′ có màu kèm chữ), B4 (không gì tự chạy).
 */

import { useState } from "react";
import { PredictGate, vn, type PredictOption } from "./PredictGate";

const G = 9.81; // m/s²
const L = 0.04; // m
/** Δm đo (g) tại I = 0…5 A, chiều ra khỏi trang — so_lieu_mau.hang[*][1] của tn-l12-thuchanhtu-04. */
const DM = [0, 0.5, 0.97, 1.45, 1.97, 2.44] as const;
/** Độ dốc đồ thị Δm–I (g/A) — ghi chú so_lieu_mau. */
const SLOPE = 0.4885;

const Q_RATIO: { question: string; options: PredictOption[] } = {
  question: "Với I = 1 A, cân chỉ +0,50 g. Giữ nguyên chiều dòng, tăng I lên 4 A. Số chỉ của cân gần bằng",
  options: [
    { text: "+0,50 g.", why: "Lực từ F = B·I·l tỉ lệ với I, nên tăng I thì lực lên nam châm cũng tăng." },
    { text: "+1,00 g.", why: "I tăng 4 lần chứ không phải 2 lần." },
    {
      text: "+2,00 g.",
      correct: true,
      why: "F = B·I·l tỉ lệ thuận với I: I gấp 4 thì F′ lên nam châm gấp 4, cân chỉ ≈ 4 × 0,50 = 2,0 g (đo được 1,97 g).",
    },
    { text: "+8,00 g.", why: "F tỉ lệ bậc nhất với I, không phải với I²: gấp 4 chứ không gấp 16." },
  ],
};

const Q_B: { question: string; options: PredictOption[] } = {
  question: "Tính B = Δm·g/(I·l) từ số đo ở I = 1 A và ở I = 5 A. So với B tính ở 1 A, B tính ở 5 A",
  options: [
    { text: "lớn gấp 5 lần, vì dòng điện lớn gấp 5 lần.", why: "Δm cũng lớn gấp 5 lần nên thương Δm/I không đổi." },
    {
      text: "gần bằng nhau, khoảng 0,12 T.",
      correct: true,
      why: "B là đặc trưng của nam châm, không do dòng điện qua dây tạo ra: Δm tăng đúng theo I nên B = Δm·g/(I·l) luôn quanh 0,12 T.",
    },
    { text: "nhỏ bằng 1/5, vì chia cho I lớn hơn.", why: "Tử số Δm cũng tăng theo I nên không nhỏ đi." },
    { text: "bằng 0, vì dòng lớn làm nam châm mất từ tính.", why: "Dòng vài ampe không làm nam châm vĩnh cửu mất từ." },
  ],
};

/* ---------------- Mũi tên dọc ---------------- */

function VArrow({ x, y, len, color, label }: { x: number; y: number; len: number; color: string; label: string }) {
  if (Math.abs(len) < 1) return null;
  const s = Math.sign(len);
  const tip = y + len;
  return (
    <g>
      <line x1={x} y1={y} x2={x} y2={tip - s * 7} stroke={color} strokeWidth={4} strokeLinecap="round" />
      <path d={`M${x},${tip} L${x - 7},${tip - s * 12} L${x + 7},${tip - s * 12} Z`} fill={color} />
      <text x={x + 10} y={tip + (s > 0 ? -4 : 14)} fill={color} fontSize={17} fontWeight={700} fontStyle="italic">
        {label}
      </text>
    </g>
  );
}

const segBtn = (on: boolean) =>
  `min-h-11 flex-1 rounded-lg px-2 text-sm font-medium transition active:scale-[0.98] ${
    on ? "bg-primary text-white" : "border border-line-strong bg-panel text-ink hover:bg-primary-soft"
  }`;

/* ---------------- Component chính ---------------- */

export default function CurrentBalanceSimulation() {
  const [I, setI] = useState(1);
  const [dir, setDir] = useState<1 | -1>(1); // +1: ra khỏi trang (⊙), −1: vào trong trang (⊗)
  const [q1, setQ1] = useState<number | null>(null);
  const [q2, setQ2] = useState<number | null>(null);
  const [pts, setPts] = useState<Set<string>>(() => new Set(["1:1"]));

  const dm = dir * DM[I]; // g
  const F = Math.abs(dm) * G; // mN (Δm g × 9,81 m/s² = mN)
  const B = I > 0 ? (F * 1e-3) / (I * L) : 0;

  const record = (i: number, d: 1 | -1) => setPts((p) => new Set(p).add(`${i}:${d}`));
  const changeI = (i: number) => {
    setI(i);
    record(i, dir);
  };
  const changeDir = (d: 1 | -1) => {
    setDir(d);
    record(I, d);
  };

  const header = <h2 className="font-display text-lg font-semibold">Cân dòng điện: tự chỉnh I và chiều dòng</h2>;

  if (q1 === null) {
    return (
      <section
        className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
        aria-label="Mô phỏng cân dòng điện"
      >
        {header}
        <div className="mt-3">
          <PredictGate question={Q_RATIO.question} options={Q_RATIO.options} choice={q1} onChoose={setQ1} />
        </div>
        <p className="mt-2 text-sm text-muted">🔒 Mô phỏng mở sau khi em chọn.</p>
      </section>
    );
  }

  /* ----- Hình: nhìn dọc theo dây; N bên trái, S bên phải nên B⃗ hướng sang phải ----- */
  const W = 320;
  const fLen = I === 0 ? 0 : 16 + 11 * I; // F′ cùng độ dài với F (định luật III)
  const wire = { x: 150, y: 92 };
  const magSide = { x: 52, y: 124 }; // F′ vẽ cạnh nam châm cho khỏi che số cân
  const display = `${dm > 0 ? "+" : dm < 0 ? "−" : ""}${vn(Math.abs(dm), 2)} g`;

  /* ----- Đồ thị Δm–I ----- */
  const GX0 = 40;
  const GX1 = 300;
  const GY0 = 18;
  const GY1 = 158;
  const gx = (i: number) => GX0 + ((GX1 - GX0) * i) / 5;
  const gy = (m: number) => (GY0 + GY1) / 2 - (m / 2.5) * ((GY1 - GY0) / 2);
  const recorded = [...pts].map((k) => {
    const [i, d] = k.split(":").map(Number);
    return { i, m: d * DM[i], key: k };
  });
  const posI = new Set(recorded.filter((p) => p.m > 0).map((p) => p.i));
  const negI = new Set(recorded.filter((p) => p.m < 0).map((p) => p.i));

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Mô phỏng cân dòng điện"
    >
      {header}
      <div className="mt-3">
        <PredictGate
          question={Q_RATIO.question}
          options={Q_RATIO.options}
          choice={q1}
          onChoose={() => {}}
          hint="Kéo I từ 1 A lên 4 A rồi đọc số cân."
        />
      </div>

      <div className="mt-3 grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        {/* Sân khấu */}
        <div className="min-w-0">
          <div className="mx-auto max-w-[440px] rounded-lg border border-line bg-surface-2">
            <svg
              viewBox={`0 0 ${W} 270`}
              className="block h-auto w-full select-none"
              role="img"
              aria-label={`Cân dòng điện: I = ${I} A, ${dir > 0 ? "ra khỏi trang" : "vào trong trang"}, cân chỉ ${display}`}
            >
              {/* giá đỡ dây: đế, trụ, tay ngang, thanh treo */}
              <rect x={268} y={238} width={44} height={8} rx={2} className="fill-muted" fillOpacity={0.6} />
              <rect x={286} y={20} width={8} height={220} className="fill-muted" fillOpacity={0.6} />
              <rect x={156} y={20} width={138} height={7} className="fill-muted" fillOpacity={0.6} />
              <rect x={157} y={26} width={6} height={wire.y - 34} className="fill-muted" fillOpacity={0.6} />
              <text x={300} y={16} textAnchor="end" className="fill-muted" fontSize={14}>
                giá riêng
              </text>

              {/* mặt bàn */}
              <line x1={4} y1={246} x2={W - 4} y2={246} className="stroke-muted" strokeWidth={2} />

              {/* cân điện tử */}
              <rect x={60} y={196} width={180} height={50} rx={8} className="fill-panel stroke-ink" strokeWidth={2} />
              <rect x={70} y={188} width={160} height={9} rx={2} className="fill-muted" fillOpacity={0.5} />
              <rect x={92} y={207} width={116} height={30} rx={4} fill="#0f172a" />
              <text
                x={150}
                y={229}
                textAnchor="middle"
                fill="#4ade80"
                fontSize={20}
                fontWeight={700}
                fontFamily="ui-monospace, monospace"
              >
                {display}
              </text>

              {/* nam châm chữ U: hai cánh đứng, gông dưới */}
              <rect x={86} y={170} width={128} height={18} rx={3} className="fill-muted" fillOpacity={0.8} />
              <rect x={86} y={60} width={34} height={120} rx={3} fill="#dc2626" />
              <rect x={180} y={60} width={34} height={120} rx={3} fill="#2563eb" />
              <text x={103} y={82} textAnchor="middle" fill="#fff" fontSize={18} fontWeight={700}>
                N
              </text>
              <text x={197} y={82} textAnchor="middle" fill="#fff" fontSize={18} fontWeight={700}>
                S
              </text>
              {/* đường sức trong khe */}
              {[110, 140].map((y) => (
                <g key={y}>
                  <line
                    x1={124}
                    y1={y}
                    x2={170}
                    y2={y}
                    className="stroke-muted"
                    strokeWidth={1.5}
                    strokeDasharray="4 3"
                  />
                  <path d={`M176,${y} l-7,-4 l0,8 Z`} className="fill-muted" />
                </g>
              ))}
              <text x={150} y={160} textAnchor="middle" className="fill-muted" fontSize={13} fontStyle="italic">
                B
              </text>

              {/* dây dẫn (nhìn dọc theo dây) */}
              <circle cx={wire.x} cy={wire.y} r={11} className="fill-panel stroke-ink" strokeWidth={2.5} />
              {I === 0 ? null : dir > 0 ? (
                <circle cx={wire.x} cy={wire.y} r={3.5} className="fill-ink" />
              ) : (
                <path
                  d={`M${wire.x - 6},${wire.y - 6} l12,12 M${wire.x + 6},${wire.y - 6} l-12,12`}
                  className="stroke-ink"
                  strokeWidth={2.5}
                />
              )}

              {/* lực: F lên dây, F′ lên nam châm — cùng độ dài, ngược chiều */}
              <VArrow x={wire.x} y={wire.y - dir * 12} len={-dir * fLen} color="var(--color-accent)" label="F" />
              <VArrow x={magSide.x} y={magSide.y} len={dir * fLen} color="var(--color-primary)" label="F′" />
            </svg>
          </div>
          <p className="mt-1 text-center text-xs text-muted">
            Mũi tên F, F′ phóng to cho dễ thấy; F′ luôn ngược chiều, cùng độ dài với F.
          </p>
        </div>

        {/* Điều khiển + số đo */}
        <div className="min-w-0 space-y-3 text-sm">
          <label className="block">
            <span className="flex justify-between text-muted">
              <span>Cường độ dòng điện I</span>
              <span className="font-mono text-ink">{I} A</span>
            </span>
            <input
              type="range"
              min={0}
              max={5}
              step={1}
              value={I}
              onChange={(e) => changeI(Number(e.target.value))}
              className="h-11 w-full cursor-pointer accent-[var(--color-primary)]"
              aria-label="Cường độ dòng điện I"
            />
          </label>
          <div className="flex gap-2" role="group" aria-label="Chiều dòng điện">
            <button type="button" aria-pressed={dir > 0} onClick={() => changeDir(1)} className={segBtn(dir > 0)}>
              ⊙ ra khỏi trang
            </button>
            <button type="button" aria-pressed={dir < 0} onClick={() => changeDir(-1)} className={segBtn(dir < 0)}>
              ⊗ vào trong trang
            </button>
          </div>

          <dl className="grid grid-cols-2 gap-2">
            <div className="rounded-lg bg-surface-2 p-2">
              <dt className="text-muted">Cân chỉ Δm</dt>
              <dd className="font-mono font-semibold">{display}</dd>
            </div>
            <div className="rounded-lg bg-surface-2 p-2">
              <dt className="text-muted">Lực từ F = |Δm|·g</dt>
              <dd className="font-mono font-semibold">{I === 0 ? "0" : `${vn(F, 2)} mN`}</dd>
            </div>
            <div className="col-span-2 rounded-lg bg-surface-2 p-2">
              <dt className="text-muted">B = F/(I·l), l = 4,0 cm</dt>
              <dd className="font-mono font-semibold">
                {q2 === null ? "🔒 đoán câu dưới trước" : I === 0 ? "— (I = 0)" : `${vn(B, 3)} T`}
              </dd>
            </div>
          </dl>

          {/* Đồ thị Δm–I tự chấm điểm theo các nấc em đã thử */}
          <div className="rounded-lg border border-line bg-surface-2">
            <svg viewBox="0 0 320 180" className="block h-auto w-full" role="img" aria-label="Đồ thị số cân theo I">
              <line x1={GX0} y1={GY0} x2={GX0} y2={GY1} className="stroke-muted" strokeWidth={1.5} />
              <line x1={GX0} y1={gy(0)} x2={GX1} y2={gy(0)} className="stroke-muted" strokeWidth={1.5} />
              {[1, 2, 3, 4, 5].map((i) => (
                <text key={i} x={gx(i)} y={gy(0) + 15} textAnchor="middle" className="fill-muted" fontSize={14}>
                  {i}
                </text>
              ))}
              {[2, -2].map((m) => (
                <text key={m} x={GX0 - 6} y={gy(m) + 4} textAnchor="end" className="fill-muted" fontSize={14}>
                  {m > 0 ? "+2" : "−2"}
                </text>
              ))}
              <text x={GX0 + 4} y={GY0 + 2} className="fill-muted" fontSize={14}>
                Δm (g)
              </text>
              <text x={GX1} y={gy(0) - 6} textAnchor="end" className="fill-muted" fontSize={14}>
                I (A)
              </text>
              {posI.size >= 3 && (
                <line
                  x1={gx(0)}
                  y1={gy(0)}
                  x2={gx(5)}
                  y2={gy(SLOPE * 5)}
                  stroke="var(--color-cyan)"
                  strokeWidth={1.5}
                  strokeDasharray="5 4"
                />
              )}
              {negI.size >= 3 && (
                <line
                  x1={gx(0)}
                  y1={gy(0)}
                  x2={gx(5)}
                  y2={gy(-SLOPE * 5)}
                  stroke="var(--color-cyan)"
                  strokeWidth={1.5}
                  strokeDasharray="5 4"
                />
              )}
              {recorded.map((p) => (
                <circle key={p.key} cx={gx(p.i)} cy={gy(p.m)} r={4.5} fill="var(--color-cyan)" />
              ))}
              <circle cx={gx(I)} cy={gy(dm)} r={8} fill="none" stroke="var(--color-accent)" strokeWidth={2} />
            </svg>
          </div>
          <p className="text-xs text-muted">
            Mỗi nấc em thử thành một chấm. Thử đủ 3 nấc cùng chiều thì hiện đường thẳng qua gốc toạ độ. Số liệu minh hoạ
            (B = 0,12 T, l = 4,0 cm), khớp bảng trong bài.
          </p>
        </div>
      </div>

      <div className="mt-4 space-y-2 text-sm leading-relaxed">
        <PredictGate
          question={Q_B.question}
          options={Q_B.options}
          choice={q2}
          onChoose={setQ2}
          hint="Kéo I qua 1, 3, 5 A và đọc ô B: số đo dao động quanh 0,12 T do sai số, không tăng theo I."
        />
        <p>
          <b>Nhìn vào:</b> đảo chiều ở cùng I thì F và F′ đổi chiều, số cân đổi dấu, độ lớn giữ nguyên.
        </p>
      </div>
    </section>
  );
}
