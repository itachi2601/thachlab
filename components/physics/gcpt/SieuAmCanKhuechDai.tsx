"use client";

/**
 * GCPT Bài 7 (USM) — cần khuếch đại (horn) cộng hưởng và rung đầu dụng cụ.
 * Chiều dài cộng hưởng nửa bước sóng L = c/(2f), c = √(E/ρ) (công thức trong bài; thép E ≈ 200 GPa, ρ ≈ 7850 → L ≈ 126 mm ở 20 kHz).
 * Cần bậc (hai đoạn trụ, chỗ đổi tiết diện ở giữa): tỉ số biên độ ra/vào = (D1/D2)² (tỉ số diện tích; mô hình sóng dọc trong thanh).
 * Đầu dụng cụ dao động điều hoà x = A·sin(2πft): v_max = 2πfA, a_max = (2πf)²A. Hình rung chạy chậm (B4: bấm mới chạy).
 */

import { useEffect, useState } from "react";
import { vn } from "../PredictGate";
import { CanhBao, GhiChuMoHinh, HangNut, KhungMoPhong, O, TruotSo, nutChinh } from "./chung";

const VAT_LIEU = {
  thep: { ten: "Thép", E: 200e9, rho: 7850 },
  titan: { ten: "Titan", E: 110e9, rho: 4500 },
  nhom: { ten: "Nhôm", E: 70e9, rho: 2700 },
} as const;
type VL = keyof typeof VAT_LIEU;

const DOAN = {
  question:
    "Cần khuếch đại bậc: đầu lớn ø40 mm gắn bộ phát, đầu nhỏ ø20 mm gắn dụng cụ. Bộ phát rung biên độ 10 µm. Biên độ ở đầu nhỏ xấp xỉ",
  options: [
    { text: "10 µm, vì cần chỉ truyền rung chứ không đổi biên độ.", why: "Cần thu nhỏ tiết diện chính là để tăng biên độ; nếu không, đầu dụng cụ rung quá yếu." },
    { text: "20 µm, vì đường kính giảm một nửa.", why: "Cái quyết định là diện tích tiết diện, mà diện tích tỉ lệ với D²." },
    {
      text: "40 µm.",
      correct: true,
      why: "Với cần bậc, biên độ tăng theo tỉ số diện tích (D1/D2)² = (40/20)² = 4: 10 µm × 4 = 40 µm.",
    },
    { text: "5 µm, vì đầu nhỏ yếu hơn.", why: "Đầu nhỏ chịu ứng suất lớn hơn nhưng rung mạnh hơn chứ không yếu hơn." },
  ],
  hint: "Kéo tỉ số D1/D2, xem biên độ ra; rồi đổi tần số để thấy chiều dài cần phải đổi theo.",
};

export default function SieuAmCanKhuechDai() {
  const [fk, setF] = useState(20); // kHz
  const [aIn, setAIn] = useState(10); // µm
  const [ti, setTi] = useState(2); // D1/D2
  const [vl, setVl] = useState<VL>("thep");
  const [chay, setChay] = useState(false);
  const [pha, setPha] = useState(0);

  useEffect(() => {
    if (!chay) return;
    let raf = 0;
    const t0 = performance.now();
    const buoc = (now: number) => {
      setPha(((now - t0) / 1000) * 2 * Math.PI * 0.8); // 0,8 Hz hiển thị
      raf = requestAnimationFrame(buoc);
    };
    raf = requestAnimationFrame(buoc);
    return () => cancelAnimationFrame(raf);
  }, [chay]);

  const m = VAT_LIEU[vl];
  const c = Math.sqrt(m.E / m.rho);
  const f = fk * 1000;
  const L = (c / (2 * f)) * 1000; // mm
  const gain = ti * ti;
  const aOut = aIn * gain; // µm
  const w = 2 * Math.PI * f;
  const vMax = w * aOut * 1e-6; // m/s
  const aMax = w * w * aOut * 1e-6; // m/s²

  /* ---- Hình: cần bậc nằm dọc, dài theo tỉ lệ L ---- */
  const W = 200;
  const H = 260;
  const len = Math.min(170, (L / 160) * 170);
  const D1 = 56;
  const D2 = D1 / ti;
  const yDau = 40;
  const yGiua = yDau + len / 2;
  const yCuoi = yDau + len;
  const dich = Math.sin(pha) * (2 + (aOut / 80) * 10); // px, phóng đại
  const yTip = yCuoi + 14 + dich;

  return (
    <KhungMoPhong ten="Siêu âm: cần khuếch đại và biên độ đầu dụng cụ" doan={DOAN}>
      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-2">
          <svg viewBox={`0 0 ${W} ${H}`} className="mx-auto w-full max-w-[260px]" role="img" aria-label="Bộ phát, cần khuếch đại bậc, dụng cụ, bùn hạt mài, phôi">
            <rect x={100 - 34} y={6} width={68} height={30} rx={4} fill="var(--color-slate-500)" />
            <text x={100} y={25} textAnchor="middle" fontSize={11} fill="#fff">bộ phát {fk} kHz</text>
            <rect x={100 - D1 / 2} y={yDau} width={D1} height={len / 2} fill="var(--color-primary-soft)" stroke="var(--color-ink)" />
            <rect x={100 - D2 / 2} y={yGiua} width={D2} height={len / 2 + dich * 0.5} fill="var(--color-primary-soft)" stroke="var(--color-ink)" />
            <rect x={100 - D2 / 2 + 2} y={yCuoi + dich * 0.5} width={D2 - 4} height={14 + dich * 0.5} fill="var(--color-slate-500)" />
            <line x1={170} y1={yDau} x2={170} y2={yCuoi} stroke="var(--color-ink)" />
            <text x={174} y={(yDau + yCuoi) / 2} fontSize={11} fill="var(--color-ink)">L</text>
            <text x={100 + D1 / 2 + 4} y={yDau + 14} fontSize={10} fill="var(--color-muted)">D1</text>
            <text x={100 + D2 / 2 + 4} y={yGiua + 14} fontSize={10} fill="var(--color-muted)">D2</text>
            {/* bùn hạt mài */}
            <rect x={30} y={yTip} width={140} height={Math.max(4, H - 30 - yTip)} fill="var(--color-cyan)" opacity={0.25} />
            {Array.from({ length: 14 }, (_, i) => (
              <circle key={i} cx={40 + i * 9.5} cy={Math.min(H - 34, yTip + 3 + ((i * 7) % 6))} r={2.2} fill="var(--color-ink)" />
            ))}
            <rect x={20} y={H - 30} width={160} height={24} fill="var(--color-surface-2)" stroke="var(--color-line-strong)" />
            <text x={100} y={H - 14} textAnchor="middle" fontSize={11} fill="var(--color-ink)">phôi giòn (gốm, kính)</text>
          </svg>
          <button type="button" className={nutChinh + " w-full"} onClick={() => setChay((x) => !x)}>
            {chay ? "Dừng rung" : "Cho rung (chạy chậm)"}
          </button>
          <p className="text-xs text-muted">Hình rung chậm và phóng đại hàng nghìn lần; thật ra đầu dụng cụ rung {fk} nghìn lần mỗi giây.</p>
        </div>

        <div className="min-w-0 space-y-3">
          <HangNut
            nhan="Vật liệu cần khuếch đại"
            items={(Object.keys(VAT_LIEU) as VL[]).map((k) => ({ value: k, text: VAT_LIEU[k].ten }))}
            value={vl}
            onChange={setVl}
          />
          <TruotSo nhan="Tần số f" giaTri={fk} hien={`${fk} kHz`} min={18} max={40} step={1} onChange={setF} />
          <TruotSo nhan="Biên độ bộ phát A₁" giaTri={aIn} hien={`${aIn} µm`} min={2} max={15} step={1} onChange={setAIn} />
          <TruotSo nhan="Tỉ số đường kính D1/D2" giaTri={ti} hien={vn(ti, 1)} min={1} max={3} step={0.1} onChange={setTi} />
          <dl className="grid grid-cols-2 gap-2">
            <O nhan="Vận tốc âm c = √(E/ρ)" so={`≈ ${vn(c, 0)} m/s`} />
            <O nhan="Chiều dài cộng hưởng L = c/(2f)" so={`≈ ${vn(L, 0)} mm`} />
            <O nhan="Biên độ đầu dụng cụ A₂" so={`≈ ${vn(aOut, 0)} µm`} phu={`hệ số (D1/D2)² = ${vn(gain, 2)}`} />
            <O nhan="Vận tốc đỉnh 2πfA₂" so={`≈ ${vn(vMax, 1)} m/s`} phu={`gia tốc đỉnh ≈ ${vn(aMax / 9.81 / 1000, 0)} nghìn lần g`} />
          </dl>
          {aOut > 60 ? (
            <CanhBao loai="danger">Biên độ quá lớn: ứng suất ở chỗ đổi tiết diện cao, cần dễ nứt mỏi; bùn văng, bề mặt nhám.</CanhBao>
          ) : aOut < 10 ? (
            <CanhBao loai="warn">Biên độ nhỏ: hạt mài đập yếu, bóc rất chậm.</CanhBao>
          ) : (
            <CanhBao loai="ok">Biên độ cỡ vài chục µm: vùng làm việc thường gặp (tham khảo).</CanhBao>
          )}
        </div>
      </div>
      <GhiChuMoHinh>
        Mô hình sóng dọc trong thanh mảnh: L = c/(2f), c = √(E/ρ); cần bậc khuếch đại theo (D1/D2)². Cần thật thường có dạng côn,
        mũ hoặc bậc có góc lượn, hệ số nhỏ hơn và chiều dài phải chỉnh thêm vì có dụng cụ gắn ở đầu.
      </GhiChuMoHinh>
    </KhungMoPhong>
  );
}
