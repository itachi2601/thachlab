"use client";

/**
 * GCPT Bài 6 (WJM/AWJ) — áp suất → vận tốc tia (Bernoulli, v ≈ √(2p/ρ), như công thức trong bài), lưu lượng qua lỗ phun
 * Q = Cd·(πd²/4)·v (Cd ≈ 0,7, tham khảo), công suất thuỷ lực P = p·Q, lực đẩy ngược F = ρQv.
 * Phần vết cắt (độ côn, vệt trễ) là định tính: tốc độ đầu cắt tính theo phần trăm "tốc độ vừa cắt đứt" của tấm,
 * độ trễ đáy ∝ tỉ số đó mũ 1,5 và độ côn ∝ tỉ số — chỉ để thấy xu hướng "chạy nhanh thì côn, trễ tăng" của bài.
 */

import { useState } from "react";
import { vn } from "../PredictGate";
import { CanhBao, GhiChuMoHinh, KhungMoPhong, O, TruotSo } from "./chung";

const RHO = 1000;
const CD = 0.7;

const DOAN = {
  question: "Tăng áp suất bơm từ 100 MPa lên 400 MPa (gấp 4). Vận tốc tia nước ra khỏi lỗ phun xấp xỉ",
  options: [
    { text: "không đổi, vì lỗ phun không đổi.", why: "Áp suất trước lỗ phun chuyển thành động năng của tia: áp lớn thì tia nhanh hơn." },
    { text: "gấp 4 lần.", why: "v ≈ √(2p/ρ) tỉ lệ với căn bậc hai của p, không tỉ lệ bậc nhất." },
    { text: "gấp 2 lần.", correct: true, why: "v ≈ √(2p/ρ): p gấp 4 thì v gấp √4 = 2 lần (từ ≈ 450 m/s lên ≈ 900 m/s)." },
    { text: "gấp 16 lần.", why: "Động năng ∝ v², nên v chỉ tăng theo √p." },
  ],
  hint: "Kéo áp suất và xem ô vận tốc; rồi thử chạy đầu cắt nhanh dần.",
};

export default function TiaNuoc() {
  const [pMPa, setP] = useState(300);
  const [d, setD] = useState(0.3); // mm, lỗ phun
  const [tocDo, setTocDo] = useState(40); // % tốc độ vừa cắt đứt

  const p = pMPa * 1e6;
  const v = Math.sqrt((2 * p) / RHO);
  const Q = CD * ((Math.PI * (d / 1000) ** 2) / 4) * v; // m³/s
  const Pw = p * Q; // W
  const F = RHO * Q * v; // N

  const k = tocDo / 100;
  const thung = k <= 1;
  const tre = Math.min(1.3, k) ** 1.5; // 0..~1.5
  const con = Math.min(1.3, k);

  /* ---- Mặt cắt dọc theo hướng chạy: tia cong về phía sau ---- */
  const W = 320;
  const H = 170;
  const yTren = 40;
  const day = 110; // chiều dày tấm px
  const xTia = 200;
  const lech = 70 * tre;
  const sauToiDa = thung ? day : day * (1 / k) ** 1.2;
  const yCuoi = yTren + Math.min(day, sauToiDa);
  const dl = xTia - lech * ((yCuoi - yTren) / day) ** 2;

  /* ---- Mặt cắt ngang vết: miệng rộng, đáy hẹp ---- */
  const CW = 140;
  const mieng = 26;
  const dayKe = Math.max(4, mieng - 16 * con);

  return (
    <KhungMoPhong ten="Tia nước: áp suất, vận tốc, độ côn và vệt trễ" doan={DOAN}>
      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-2">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Mặt cắt dọc: tia cắt cong về phía sau khi chạy nhanh">
            <rect x={10} y={yTren} width={W - 20} height={day} fill="var(--color-primary-soft)" stroke="var(--color-line-strong)" />
            {/* rãnh đã cắt phía sau */}
            <path
              d={`M10,${yTren} L${xTia},${yTren} Q${xTia - lech * 0.3},${yTren + day * 0.6} ${dl},${yCuoi} L10,${yCuoi} Z`}
              fill="var(--color-panel)"
              opacity={thung ? 1 : 0.9}
            />
            <rect x={xTia - 14} y={8} width={28} height={26} rx={4} fill="var(--color-slate-500)" />
            <text x={xTia + 20} y={24} fontSize={11} fill="var(--color-ink)">đầu cắt → chạy</text>
            <path d={`M${xTia},34 L${xTia},${yTren} Q${xTia - lech * 0.3},${yTren + day * 0.6} ${dl},${yCuoi}`} fill="none" stroke="var(--color-cyan)" strokeWidth={4} />
            {!thung && <text x={dl - 4} y={yCuoi + 14} fontSize={11} fill="var(--color-danger)" textAnchor="end">chưa cắt thủng</text>}
            {thung && lech > 6 && (
              <>
                <line x1={xTia} y1={yTren + day + 6} x2={dl} y2={yTren + day + 6} stroke="var(--color-danger)" strokeWidth={1.5} />
                <text x={(xTia + dl) / 2} y={yTren + day + 19} textAnchor="middle" fontSize={11} fill="var(--color-danger)">vệt trễ</text>
              </>
            )}
            <text x={14} y={yTren + 14} fontSize={10} fill="var(--color-muted)">đã cắt</text>
          </svg>
          <div className="flex items-start gap-3">
            <svg viewBox={`0 0 ${CW} 100`} className="w-[42%] shrink-0" role="img" aria-label="Mặt cắt ngang vết cắt: miệng rộng, đáy hẹp">
              <rect x={6} y={10} width={CW - 12} height={80} fill="var(--color-primary-soft)" stroke="var(--color-line-strong)" />
              <path
                d={`M${CW / 2 - mieng / 2},10 L${CW / 2 + mieng / 2},10 L${CW / 2 + dayKe / 2},90 L${CW / 2 - dayKe / 2},90 Z`}
                fill={thung ? "var(--color-panel)" : "var(--color-surface-2)"}
              />
            </svg>
            <p className="text-xs text-muted">Mặt cắt ngang vết: miệng rộng, đáy hẹp là độ côn. Chạy càng nhanh, đáy càng hẹp.</p>
          </div>
        </div>

        <div className="min-w-0 space-y-3">
          <TruotSo nhan="Áp suất bơm p" giaTri={pMPa} hien={`${pMPa} MPa`} min={50} max={600} step={10} onChange={setP} />
          <TruotSo nhan="Đường kính lỗ phun d" giaTri={d} hien={`${vn(d, 2)} mm`} min={0.1} max={0.4} step={0.01} onChange={setD} />
          <TruotSo
            nhan="Tốc độ chạy đầu cắt (% tốc độ vừa cắt đứt)"
            giaTri={tocDo}
            hien={`${tocDo}%`}
            min={10}
            max={130}
            step={5}
            onChange={setTocDo}
          />
          <dl className="grid grid-cols-2 gap-2">
            <O nhan="Vận tốc tia v ≈ √(2p/ρ)" so={`≈ ${vn(v, 0)} m/s`} phu={`≈ ${vn(v / 340, 1)} lần vận tốc âm trong không khí`} />
            <O nhan="Lưu lượng Q" so={`${vn(Q * 60000, 2)} L/phút`} phu="Cd ≈ 0,7 (tham khảo)" />
            <O nhan="Công suất tia P = p·Q" so={`${vn(Pw / 1000, 1)} kW`} />
            <O nhan="Lực đẩy ngược F = ρQv" so={`${vn(F, 0)} N`} />
          </dl>
          {!thung ? (
            <CanhBao loai="danger">Quá nhanh: tia không xuyên hết chiều dày, đáy chưa đứt.</CanhBao>
          ) : k > 0.6 ? (
            <CanhBao loai="warn">Đứt nhưng vệt trễ, độ côn lớn: mép xấu, góc bị khuyết. Giảm tốc ở góc hoặc nghiêng đầu bù côn.</CanhBao>
          ) : (
            <CanhBao loai="ok">Chạy chậm: tia gần thẳng, độ côn và vệt trễ nhỏ, đổi lại năng suất thấp.</CanhBao>
          )}
          <p className="text-sm text-danger">⚠ Tia vài trăm MPa cắt được thịt, xương: không đưa tay vào vùng tia.</p>
        </div>
      </div>
      <GhiChuMoHinh>
        v, Q, P, F tính theo công thức lý tưởng (bỏ ma sát trong lỗ phun, Cd ≈ 0,7 tham khảo); với AWJ, vận tốc hạt mài sau buồng
        trộn nhỏ hơn vận tốc nước. Hình vết cắt chỉ định tính.
      </GhiChuMoHinh>
    </KhungMoPhong>
  );
}
