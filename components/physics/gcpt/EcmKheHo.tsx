"use client";

/**
 * GCPT Bài 4 (ECM) — khe hở tự cân bằng. Định luật Faraday: tốc độ hoà tan mặt phôi v_d = ηA·J/(zFρ);
 * mật độ dòng qua khe J = κ(U − ΔU)/h (định luật Ohm cho lớp dung dịch dày h). Dụng cụ tiến đều với tốc độ f:
 *   dh/dt = v_d − f = C·κ(U − ΔU)/h − f,  C = ηA/(zFρ)
 * → khe cân bằng h_e = C·κ(U − ΔU)/f (khe hẹp thì dòng đậm, tan nhanh, khe tự nới; khe rộng thì ngược lại).
 * Thép xem như sắt (A = 55,85; z = 2; ρ = 7,86; η = 0,9) khớp bài toán mẫu trong bài: J = 100 A/cm² → v ≈ 2,0 mm/phút.
 * κ = 0,15 S/cm (dung dịch NaCl, tham khảo), ΔU = 3 V (sụt áp ở điện cực, tham khảo).
 */

import { useEffect, useRef, useState } from "react";
import { vn } from "../PredictGate";
import { CanhBao, GhiChuMoHinh, KhungMoPhong, O, TruotSo, nutChinh, nutPhu } from "./chung";

const C = (0.9 * 55.85) / (2 * 96485 * 7.86); // cm³/C
const KAPPA = 0.15; // S/cm
const DU = 3; // V
const H0 = 0.8; // mm khe ban đầu
const T_MAX = 180; // s mô phỏng hiển thị trên đồ thị
const TANG_TOC = 30; // 1 s thật = 30 s mô phỏng
const S = 2; // cm² diện tích hốc (bài toán mẫu)

const DOAN = {
  question:
    "Máy ECM đang chạy ổn định với khe hở khoảng 0,3 mm. Giữ nguyên điện áp, tăng tốc độ tiến dụng cụ lên gấp đôi. Sau một lúc, khe hở sẽ",
  options: [
    { text: "giảm dần về 0 rồi đoản mạch, vì dụng cụ tiến nhanh hơn tốc độ hoà tan.", why: "Khe hẹp lại thì điện trở lớp dung dịch giảm, dòng tăng, phôi tan nhanh hơn: khe không tiếp tục co mãi." },
    {
      text: "giảm còn khoảng một nửa rồi ổn định ở đó.",
      correct: true,
      why: "Khe cân bằng khi tốc độ hoà tan bằng tốc độ tiến. Tốc độ hoà tan tỉ lệ 1/h, nên f gấp đôi thì h cân bằng còn một nửa (≈ 0,15 mm).",
    },
    { text: "không đổi, vì khe hở do điện áp quyết định.", why: "Điện áp không đổi nhưng tốc độ tiến đổi thì điểm cân bằng phải đổi theo." },
    { text: "tăng lên gấp đôi.", why: "Dụng cụ tiến nhanh hơn thì nó lấn về phía phôi, khe hẹp lại chứ không rộng ra." },
  ],
  hint: "Bấm Chạy, đợi khe ổn định, rồi kéo tốc độ tiến lên gấp đôi trong lúc đang chạy.",
};

function vanTocHoaTan(U: number, hmm: number) {
  // mm/phút
  const J = (KAPPA * (U - DU)) / (hmm / 10); // A/cm²
  return { J, v: C * J * 10 * 60 };
}

export default function EcmKheHo() {
  const [U, setU] = useState(15);
  const [f, setF] = useState(1); // mm/phút
  const [chay, setChay] = useState(false);
  const [h, setH] = useState(H0);
  const [t, setT] = useState(0);
  const [lichSu, setLichSu] = useState<{ t: number; h: number }[]>([{ t: 0, h: H0 }]);

  const ref = useRef({ U, f, h, t });
  useEffect(() => {
    ref.current.U = U;
    ref.current.f = f;
  }, [U, f]);

  useEffect(() => {
    if (!chay) return;
    let raf = 0;
    let last = performance.now();
    const buoc = (now: number) => {
      const dtThat = Math.min(0.05, (now - last) / 1000);
      last = now;
      let { h: hh, t: tt } = ref.current;
      const dt = dtThat * TANG_TOC; // s mô phỏng
      const n = 20;
      for (let i = 0; i < n; i++) {
        const { v } = vanTocHoaTan(ref.current.U, hh);
        hh += ((v - ref.current.f) / 60) * (dt / n); // mm
        hh = Math.max(0.01, hh);
      }
      tt += dt;
      ref.current.h = hh;
      ref.current.t = tt;
      setH(hh);
      setT(tt);
      setLichSu((ls) => {
        const next = [...ls, { t: tt, h: hh }];
        return next.length > 400 ? next.filter((_, i) => i % 2 === 0) : next;
      });
      if (tt >= T_MAX) {
        setChay(false);
        return;
      }
      raf = requestAnimationFrame(buoc);
    };
    raf = requestAnimationFrame(buoc);
    return () => cancelAnimationFrame(raf);
  }, [chay]);

  const datLai = () => {
    setChay(false);
    ref.current.h = H0;
    ref.current.t = 0;
    setH(H0);
    setT(0);
    setLichSu([{ t: 0, h: H0 }]);
  };

  // v (mm/phút) = C[cm³/C]·κ(U−ΔU)/(h/10 cm)·10·60 = 6000·C·κ(U−ΔU)/h  →  h_e = 6000·C·κ(U−ΔU)/f
  const hE = (6000 * C * KAPPA * (U - DU)) / f;
  const { J, v } = vanTocHoaTan(U, h);
  const Je = (KAPPA * (U - DU)) / (hE / 10);

  /* ---- Hình khe ---- */
  const SW = 150;
  const SH = 190;
  const kpx = 90; // px / mm
  const yPhoi = 120;
  const yDc = yPhoi - h * kpx;

  /* ---- Đồ thị h(t) ---- */
  const GW = 200;
  const GH = 190;
  const gx = (tt: number) => 30 + (tt / T_MAX) * (GW - 40);
  const gy = (hh: number) => GH - 25 - (Math.min(hh, 1) / 1) * (GH - 45);
  const duong = lichSu.map((p, i) => `${i ? "L" : "M"}${gx(p.t).toFixed(1)},${gy(p.h).toFixed(1)}`).join(" ");

  return (
    <KhungMoPhong ten="ECM: khe hở tự cân bằng" doan={DOAN}>
      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="min-w-0">
          <div className="flex gap-2">
            <svg viewBox={`0 0 ${SW} ${SH}`} className="w-[43%] shrink-0" role="img" aria-label="Dụng cụ, khe dung dịch và phôi">
              <rect x={30} y={Math.max(0, yDc - 90)} width={90} height={Math.min(90, yDc)} fill="var(--color-slate-500)" />
              <text x={75} y={Math.max(14, yDc - 8)} textAnchor="middle" fontSize={11} fill="#fff">dụng cụ (−)</text>
              <rect x={10} y={yDc} width={130} height={yPhoi - yDc} fill="var(--color-cyan)" opacity={0.35} />
              <rect x={10} y={yPhoi} width={130} height={SH - yPhoi - 4} fill="var(--color-primary)" fillOpacity={0.28} stroke="var(--color-line-strong)" />
              <text x={75} y={yPhoi + 24} textAnchor="middle" fontSize={11} fill="var(--color-ink)">phôi (+)</text>
              <text x={75} y={SH - 12} textAnchor="middle" fontSize={11} fill="var(--color-muted)">phôi tan dần</text>
              <line x1={144} y1={yDc} x2={144} y2={yPhoi} stroke="var(--color-ink)" />
              <text x={140} y={(yDc + yPhoi) / 2 + 4} textAnchor="end" fontSize={11} fill="var(--color-ink)">h</text>
            </svg>
            <svg viewBox={`0 0 ${GW} ${GH}`} className="min-w-0 flex-1" role="img" aria-label="Đồ thị khe hở theo thời gian">
              <line x1={30} y1={GH - 25} x2={GW - 6} y2={GH - 25} stroke="var(--color-ink)" />
              <line x1={30} y1={GH - 25} x2={30} y2={14} stroke="var(--color-ink)" />
              {[0.25, 0.5, 0.75, 1].map((m) => (
                <g key={m}>
                  <line x1={27} y1={gy(m)} x2={GW - 6} y2={gy(m)} stroke="var(--color-line)" strokeDasharray="2 3" />
                  <text x={25} y={gy(m) + 4} textAnchor="end" fontSize={10} fill="var(--color-muted)">{vn(m, 2)}</text>
                </g>
              ))}
              {hE <= 1 && <line x1={30} y1={gy(hE)} x2={GW - 6} y2={gy(hE)} stroke="var(--color-ok)" strokeWidth={1.5} strokeDasharray="6 3" />}
              <path d={duong} fill="none" stroke="var(--color-primary)" strokeWidth={2.2} />
              <text x={34} y={12} fontSize={10} fill="var(--color-muted)">h (mm)</text>
              <text x={GW - 6} y={GH - 10} textAnchor="end" fontSize={10} fill="var(--color-muted)">t = {Math.round(t)} s</text>
              <text x={GW - 8} y={hE <= 1 ? gy(hE) - 4 : 24} textAnchor="end" fontSize={10} fill="var(--color-ok)">cân bằng</text>
            </svg>
          </div>
          <div className="mt-2 flex gap-2">
            <button type="button" className={nutChinh + " flex-1"} onClick={() => setChay((c) => !c)} disabled={t >= T_MAX}>
              {chay ? "Tạm dừng" : t > 0 ? "Chạy tiếp" : "Chạy"}
            </button>
            <button type="button" className={nutPhu + " flex-1"} onClick={datLai}>
              Làm lại (h = 0,8 mm)
            </button>
          </div>
        </div>

        <div className="min-w-0 space-y-3">
          <TruotSo nhan="Điện áp U" giaTri={U} hien={`${U} V`} min={8} max={24} step={1} onChange={setU} />
          <TruotSo nhan="Tốc độ tiến dụng cụ f" giaTri={f} hien={`${vn(f, 1)} mm/phút`} min={0.5} max={5} step={0.1} onChange={setF} />
          <dl className="grid grid-cols-2 gap-2">
            <O nhan="Khe hở lúc này" so={`${vn(h, 3)} mm`} />
            <O nhan="Mật độ dòng J lúc này" so={`${vn(J, 0)} A/cm²`} phu={`I = J·S = ${vn(J * S, 0)} A (S = 2 cm²)`} />
            <O nhan="Tốc độ hoà tan" so={`${vn(v, 2)} mm/phút`} phu={v > f + 0.01 ? "> f: khe nới ra" : v < f - 0.01 ? "< f: khe hẹp lại" : "= f: cân bằng"} />
            <O nhan="Khe cân bằng h_e" so={`${vn(hE, 3)} mm`} phu={`J_e ≈ ${vn(Je, 0)} A/cm²`} />
          </dl>
          {hE < 0.1 ? (
            <CanhBao loai="danger">Khe cân bằng quá hẹp: dung dịch khó lưu thông, dễ sôi, đoản mạch. Giảm f hoặc tăng U.</CanhBao>
          ) : hE > 0.5 ? (
            <CanhBao loai="warn">Khe cân bằng rộng: dòng toả rộng, phôi sao chép hình dụng cụ kém chính xác.</CanhBao>
          ) : (
            <CanhBao loai="ok">Khe cân bằng trong khoảng làm việc 0,1 – 0,5 mm (tham khảo).</CanhBao>
          )}
        </div>
      </div>
      <GhiChuMoHinh>
        Mô hình: v_hoà tan = ηA·J/(zFρ), J = κ(U − ΔU)/h; thép xem như sắt, η = 0,9, κ = 0,15 S/cm, ΔU = 3 V (tham khảo).
        Khe cân bằng h_e = ηA·κ(U − ΔU)/(zFρ·f). Bỏ qua nhiệt, bọt khí làm κ đổi dọc khe. Thời gian chạy nhanh gấp 30 lần.
      </GhiChuMoHinh>
    </KhungMoPhong>
  );
}
