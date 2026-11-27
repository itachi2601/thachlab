"use client";

/**
 * GCPT Bài 5 (LBM) — cường độ chùm I = P/(πd²/4) và năng lượng đường E = P/v (cùng công thức, cùng bài toán mẫu trong bài:
 * 3 kW, d = 0,2 mm, v = 3 m/phút → I ≈ 9,5·10⁶ W/cm², E = 60 J/mm). Dải cường độ cho từng việc là mốc tham khảo
 * thường gặp trong tài liệu gia công laser (tôi bề mặt → hàn → cắt → khoan/bốc hơi), chỉ để định hướng.
 */

import { useState } from "react";
import { vn, vnSci } from "../PredictGate";
import { GhiChuMoHinh, KhungMoPhong, O, ThanhMuc, TruotSo, nutPhu } from "./chung";

const DOAN = {
  question: "Laser 3 kW, điểm hội tụ 0,2 mm, đang cắt ở 3 m/phút. Tăng tốc độ cắt lên 6 m/phút, giữ nguyên P và d. Khi đó",
  options: [
    { text: "cường độ I giảm một nửa, năng lượng đường E giữ nguyên.", why: "I = P/(πd²/4) không chứa v; chạy nhanh không làm điểm sáng yếu đi." },
    {
      text: "cường độ I giữ nguyên, năng lượng đường E giảm một nửa.",
      correct: true,
      why: "I chỉ phụ thuộc P và d. E = P/v: v gấp đôi thì mỗi mm đường cắt nhận một nửa năng lượng, HAZ hẹp hơn nhưng có thể không cắt thủng.",
    },
    { text: "cả I và E đều giảm một nửa.", why: "I không phụ thuộc tốc độ cắt." },
    { text: "cả I và E đều không đổi, vì công suất không đổi.", why: "E = P/v có v ở mẫu số: tốc độ đổi thì E đổi." },
  ],
  hint: "Kéo tốc độ cắt và xem ô I, ô E thay đổi thế nào.",
};

/** Dải cường độ (W/cm², tham khảo). */
const DAI = [
  { tu: 3, den: 5, ten: "nung, tôi bề mặt", mau: "var(--color-ok)" },
  { tu: 5, den: 6, ten: "hàn", mau: "var(--color-cyan)" },
  { tu: 6, den: 7.3, ten: "cắt", mau: "var(--color-primary)" },
  { tu: 7.3, den: 9, ten: "khoan, khắc (bốc hơi)", mau: "var(--color-violet)" },
];

export default function LaserCuongDo() {
  const [P, setP] = useState(3000); // W
  const [d, setD] = useState(0.2); // mm
  const [vm, setVm] = useState(3); // m/phút

  const dien = (Math.PI * (d / 10) ** 2) / 4; // cm²
  const I = P / dien;
  const vmms = (vm * 1000) / 60;
  const E = P / vmms; // J/mm
  const logI = Math.log10(I);
  const viec = DAI.find((z) => logI >= z.tu && logI < z.den)?.ten ?? (logI < 3 ? "chỉ hâm nóng" : "bốc hơi mạnh");

  /* ---- Hình chùm hội tụ: điểm vẽ theo tỉ lệ d ---- */
  const W = 200;
  const H = 190;
  const r = 4 + (d / 0.4) * 22;
  const yF = 150;

  /* ---- Thang log I ---- */
  const BW = 320;
  const bx = (l: number) => 10 + ((l - 3) / 6) * (BW - 20);

  return (
    <KhungMoPhong ten="Laser: cường độ chùm và năng lượng đường" doan={DOAN}>
      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-2">
          <svg viewBox={`0 0 ${W} ${H}`} className="mx-auto w-full max-w-[260px]" role="img" aria-label="Chùm laser hội tụ qua thấu kính">
            <rect x={60} y={6} width={80} height={36} fill="var(--color-violet)" opacity={0.25} />
            <text x={100} y={28} textAnchor="middle" fontSize={11} fill="var(--color-ink)">chùm {vn(P / 1000, 1)} kW</text>
            <ellipse cx={100} cy={58} rx={46} ry={8} fill="var(--color-cyan)" opacity={0.45} stroke="var(--color-ink)" />
            <text x={150} y={62} fontSize={10} fill="var(--color-muted)">thấu kính</text>
            <path d={`M60,58 L${100 - r / 6},${yF} L${100 + r / 6},${yF} L140,58 Z`} fill="var(--color-danger)" opacity={0.28} />
            <rect x={20} y={yF} width={160} height={28} fill="var(--color-surface-2)" stroke="var(--color-line-strong)" />
            <ellipse cx={100} cy={yF} rx={r} ry={r * 0.3} fill="var(--color-danger)" opacity={0.9} />
            <text x={100} y={yF + 20} textAnchor="middle" fontSize={11} fill="var(--color-ink)">điểm ø{vn(d, 2)} mm</text>
          </svg>
          <svg viewBox={`0 0 ${BW} 62`} className="w-full" role="img" aria-label="Thang cường độ, vị trí của chùm hiện tại">
            {DAI.map((z) => (
              <g key={z.ten}>
                <rect x={bx(z.tu)} y={14} width={bx(z.den) - bx(z.tu)} height={12} fill={z.mau} opacity={0.35} />
                <text x={(bx(z.tu) + bx(z.den)) / 2} y={42} textAnchor="middle" fontSize={11} fill="var(--color-ink)">
                  {z.ten.split(" (")[0]}
                </text>
              </g>
            ))}
            {[3, 5, 7, 9].map((l) => (
              <text key={l} x={bx(l)} y={58} textAnchor="middle" fontSize={10.5} fill="var(--color-muted)">10{["³", "⁵", "⁷", "⁹"][(l - 3) / 2]}</text>
            ))}
            <path d={`M${bx(Math.min(9, Math.max(3, logI)))},12 l-6,-9 h12 Z`} fill="var(--color-ink)" />
          </svg>
          <p className="text-xs text-muted">Thang cường độ W/cm² (log, mốc tham khảo). Tam giác đen: chùm đang chỉnh.</p>
          <button type="button" className={nutPhu + " w-full"} onClick={() => { setP(3000); setD(0.2); setVm(3); }}>
            Về số của bài toán mẫu (3 kW · 0,2 mm · 3 m/phút)
          </button>
        </div>

        <div className="min-w-0 space-y-3">
          <TruotSo nhan="Công suất P" giaTri={P} hien={`${vn(P / 1000, 1)} kW`} min={500} max={6000} step={100} onChange={setP} />
          <TruotSo nhan="Đường kính điểm hội tụ d" giaTri={d} hien={`${vn(d, 2)} mm`} min={0.05} max={0.4} step={0.01} onChange={setD} />
          <TruotSo nhan="Tốc độ cắt v" giaTri={vm} hien={`${vn(vm, 1)} m/phút`} min={0.5} max={20} step={0.5} onChange={setVm} />
          <dl className="grid grid-cols-2 gap-2">
            <O nhan="Cường độ I = P/(πd²/4)" so={`${vnSci(I, 1)} W/cm²`} phu={`đủ cho: ${viec}`} />
            <O nhan="Năng lượng đường E = P/v" so={`${vn(E, E < 10 ? 1 : 0)} J/mm`} phu={`v = ${vn(vmms, 1)} mm/s`} />
          </dl>
          <ThanhMuc
            nhan="Bề rộng HAZ (xu hướng theo E)"
            muc={Math.log10(E) / Math.log10(800)}
            chu={E < 20 ? "hẹp" : E < 100 ? "vừa" : "rộng"}
            mau="var(--color-warn)"
          />
          <p className="text-sm text-muted">
            Nhỏ điểm → mạnh (I ∝ 1/d²). Chậm tốc độ → nóng (E ∝ 1/v). E quá nhỏ có thể không cắt thủng tấm dày; E quá lớn thì
            HAZ rộng, xỉ bám, cháy cạnh.
          </p>
        </div>
      </div>
      <GhiChuMoHinh>
        I là cường độ trung bình trên điểm hội tụ; dải cường độ cho từng việc và thanh HAZ chỉ là xu hướng tham khảo.
        Tốc độ cắt thật tra theo máy, vật liệu, bề dày và khí trợ.
      </GhiChuMoHinh>
    </KhungMoPhong>
  );
}
