"use client";

/**
 * GCPT Bài 9 (CHM/PCM) — ăn lẹm (undercut) dưới mép mặt nạ. Ăn sâu e thì ăn ngang u = e/Fe (Fe: hệ số ăn mòn;
 * đẳng hướng Fe ≈ 1 như trong bài). Biên vết ăn quanh mỗi mép mặt nạ xem là một phần tư elip (bán trục u ngang, e dọc).
 * Một mặt: thủng khi e ≥ T; hai mặt: mỗi mặt chỉ cần e = T/2. Lỗ mặt trên = w + 2u; chỗ hẹp nhất = w + 2u·√(1 − (s/e)²)
 * với s = T (một mặt) hoặc T/2 (hai mặt). Khớp ví dụ trong bài: T = 0,2 mm, w = 0,3 mm, ăn một mặt, Fe = 1 → mặt trên ≈ 0,7 mm.
 */

import { useState } from "react";
import { vn } from "../PredictGate";
import { CanhBao, GhiChuMoHinh, HangNut, KhungMoPhong, O, TruotSo } from "./chung";

type Mat = 1 | 2;

const DOAN = {
  question:
    "Tấm inox dày 0,2 mm, cửa sổ mặt nạ rộng 0,3 mm, ăn mòn đẳng hướng. Nếu ăn từ CẢ HAI mặt (hai cửa sổ thẳng hàng) cho tới khi vừa thủng, lỗ ở mặt trên rộng khoảng",
  options: [
    { text: "0,7 mm, giống như ăn một mặt.", why: "Ăn một mặt phải ăn sâu 0,2 mm nên lẹm 0,2 mm mỗi bên; hai mặt chỉ cần ăn sâu 0,1 mm mỗi mặt." },
    {
      text: "0,5 mm.",
      correct: true,
      why: "Mỗi mặt chỉ ăn sâu T/2 = 0,1 mm là gặp nhau, nên lẹm mỗi bên ≈ 0,1 mm: 0,3 + 2 × 0,1 = 0,5 mm.",
    },
    { text: "0,3 mm, vì ăn hai mặt thì không còn lẹm.", why: "Vẫn có lẹm: dung dịch ăn ngang ở cả hai mặt, chỉ là ít hơn." },
    { text: "0,9 mm, vì ăn hai lần.", why: "Hai mặt ăn đồng thời, mỗi mặt ăn nửa chiều dày, nên lẹm giảm chứ không tăng." },
  ],
  hint: "Chọn 'Hai mặt', kéo thời gian ăn tới lúc vừa thủng rồi đọc ô lỗ mặt trên.",
};

export default function AnMonAnLem() {
  const [T, setT] = useState(0.2); // mm
  const [w, setW] = useState(0.3); // mm
  const [mat, setMat] = useState<Mat>(1);
  const [Fe, setFe] = useState(1);
  const [phan, setPhan] = useState(60); // % thời gian so với lúc vừa thủng

  const s = mat === 1 ? T : T / 2; // độ sâu cần để thủng
  const e = (phan / 100) * s;
  const u = e / Fe;
  const thung = e >= s - 1e-9;
  const lTren = w + 2 * u;
  const lHep = thung ? w + 2 * u * Math.sqrt(Math.max(0, 1 - (s / e) ** 2)) : 0;
  const lemTong = u;

  /* ---- Hình mặt cắt ---- */
  const W = 320;
  const H = 170;
  const rongMax = w + 2 * (s * 1.5) / Fe;
  const k = Math.min((W - 30) / Math.max(rongMax + 0.2, 0.6), 110 / T);
  const cx = W / 2;
  const y0 = 30;
  const X = (mm: number) => cx + mm * k;
  const Y = (mm: number) => y0 + mm * k;
  const xL = -w / 2;
  const xR = w / 2;
  const ve = (yMat: number, huong: 1 | -1) => {
    // vết ăn từ mặt yMat, đi theo hướng huong (+1 xuống, −1 lên)
    if (e <= 0) return "";
    const yE = yMat + huong * e;
    const sweep = huong === 1 ? 1 : 0;
    return [
      `M${X(xL - u)},${Y(yMat)}`,
      `L${X(xR + u)},${Y(yMat)}`,
      u > 0 ? `A${u * k},${e * k} 0 0 ${sweep} ${X(xR)},${Y(yE)}` : `L${X(xR)},${Y(yE)}`,
      `L${X(xL)},${Y(yE)}`,
      u > 0 ? `A${u * k},${e * k} 0 0 ${sweep} ${X(xL - u)},${Y(yMat)}` : `L${X(xL - u)},${Y(yMat)}`,
      "Z",
    ].join(" ");
  };
  const matNa = (yMat: number, len: 1 | -1) => (
    <g>
      <rect x={6} y={len === 1 ? Y(yMat) - 6 : Y(yMat)} width={X(xL) - 6} height={6} fill="var(--color-ink)" />
      <rect x={X(xR)} y={len === 1 ? Y(yMat) - 6 : Y(yMat)} width={W - 6 - X(xR)} height={6} fill="var(--color-ink)" />
    </g>
  );

  return (
    <KhungMoPhong ten="Ăn mòn hoá học: ăn lẹm dưới mặt nạ" doan={DOAN}>
      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-2">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Mặt cắt tấm, mặt nạ và vết ăn mòn">
            <rect x={6} y={Y(0)} width={W - 12} height={T * k} fill="var(--color-primary)" fillOpacity={0.28} stroke="var(--color-line-strong)" />
            <path d={ve(0, 1)} fill="var(--color-panel)" />
            {mat === 2 && <path d={ve(T, -1)} fill="var(--color-panel)" />}
            {/* vẽ lại viền tấm ngoài vùng ăn để không lộ phần elip tràn ra ngoài tấm */}
            <rect x={0} y={Y(T)} width={W} height={H - Y(T)} fill="var(--color-panel)" />
            <rect x={0} y={0} width={W} height={Y(0)} fill="var(--color-panel)" />
            {matNa(0, 1)}
            {mat === 2 ? matNa(T, -1) : <rect x={6} y={Y(T)} width={W - 12} height={6} fill="var(--color-ink)" />}
            <line x1={X(xL)} y1={8} x2={X(xL)} y2={Y(0)} stroke="var(--color-danger)" strokeDasharray="3 3" />
            <line x1={X(xR)} y1={8} x2={X(xR)} y2={Y(0)} stroke="var(--color-danger)" strokeDasharray="3 3" />
            <text x={cx} y={14} textAnchor="middle" fontSize={11} fill="var(--color-danger)">cửa sổ w = {vn(w, 2)} mm</text>
            {u > 0.005 && (
              <>
                <line x1={X(xR)} y1={Y(0) + 4} x2={X(xR + u)} y2={Y(0) + 4} stroke="var(--color-warn)" strokeWidth={2} />
                <text x={X(xR + u) + 3} y={Y(0) + 14} fontSize={11} fill="var(--color-warn)">lẹm u</text>
              </>
            )}
            <text x={8} y={H - 6} fontSize={11} fill="var(--color-muted)">
              Mặt nạ: dải đen. {mat === 1 ? "Mặt dưới che kín." : "Hai cửa sổ thẳng hàng."}
            </text>
          </svg>
          <TruotSo
            nhan="Thời gian ăn (so với lúc vừa thủng)"
            giaTri={phan}
            hien={`${phan}%`}
            min={0}
            max={150}
            step={5}
            onChange={setPhan}
          />
        </div>

        <div className="min-w-0 space-y-3">
          <HangNut
            nhan="Ăn từ"
            items={[
              { value: 1 as Mat, text: "Một mặt" },
              { value: 2 as Mat, text: "Hai mặt" },
            ]}
            value={mat}
            onChange={setMat}
          />
          <HangNut
            nhan="Hệ số ăn mòn Fe = sâu / lẹm"
            items={[1, 2, 3].map((v) => ({ value: v, text: v === 1 ? "1 (đẳng hướng)" : String(v) }))}
            value={Fe}
            onChange={setFe}
          />
          <TruotSo nhan="Chiều dày tấm T" giaTri={T} hien={`${vn(T, 2)} mm`} min={0.05} max={1} step={0.05} onChange={setT} />
          <TruotSo nhan="Cửa sổ mặt nạ w" giaTri={w} hien={`${vn(w, 2)} mm`} min={0.1} max={1} step={0.05} onChange={setW} />
          <dl className="grid grid-cols-2 gap-2">
            <O nhan="Đã ăn sâu e (mỗi mặt)" so={`${vn(e, 3)} mm`} phu={`cần ${vn(s, 3)} mm để thủng`} />
            <O nhan="Lẹm mỗi bên u = e/Fe" so={`${vn(lemTong, 3)} mm`} />
            <O nhan="Lỗ ở mặt trên" so={`${vn(lTren, 2)} mm`} />
            <O nhan="Chỗ hẹp nhất" so={thung ? `${vn(lHep, 2)} mm` : "chưa thủng"} />
          </dl>
          {!thung ? (
            <CanhBao loai="warn">Chưa thủng: tiếp tục ăn. Lẹm vẫn đang lớn dần theo độ sâu.</CanhBao>
          ) : phan > 110 ? (
            <CanhBao loai="danger">Ăn quá giờ: lỗ tiếp tục rộng ra ở mọi chiều, kích thước vượt dung sai.</CanhBao>
          ) : (
            <CanhBao loai="ok">Vừa thủng. Muốn lỗ mặt trên đúng kích thước: thu nhỏ cửa sổ trên phim bớt 2u.</CanhBao>
          )}
        </div>
      </div>
      <GhiChuMoHinh>
        Mô hình hình học: biên vết ăn quanh mép mặt nạ là phần tư elip; Fe = 1 là ăn đẳng hướng (nhúng), phun có áp cho Fe lớn hơn
        (tham khảo). Bỏ qua mặt nạ bong mép và nồng độ dung dịch đổi theo thời gian.
      </GhiChuMoHinh>
    </KhungMoPhong>
  );
}
