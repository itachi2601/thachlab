"use client";

/**
 * GCPT Bài 3 (WEDM) — mô phỏng lượng bù dây. Khe cắt W = d + 2g; tâm dây phải lệch khỏi biên một lượng s = d/2 + g.
 * Cắt chày (giữ phần trong): kích thước = L + 2(o − s). Cắt cối (giữ lỗ): kích thước lỗ = L + 2(o + s);
 * o là độ lệch tâm dây so với biên (+ ra ngoài biên). Đúng khi o = +s cho chày, o = −s cho cối. Hình học thuần, không mô hình hoá thêm.
 */

import { useState } from "react";
import { vn } from "../PredictGate";
import { CanhBao, GhiChuMoHinh, HangNut, KhungMoPhong, O, TruotSo } from "./chung";

const L = 20; // mm, kích thước danh nghĩa
type Loai = "chay" | "coi";
type Bu = "khong" | "ngoai" | "trong";

const DOAN = {
  question:
    "Cắt chày vuông cạnh 20 mm bằng dây ø0,25 mm, khe phóng điện 0,03 mm mỗi bên. Lập trình cho tâm dây chạy đúng đường biên 20 mm (không bù). Cạnh chày đo được khoảng",
  options: [
    { text: "20,00 mm.", why: "Dây có bề dày và tia lửa còn ăn thêm một khe: vết cắt lấn vào chày nửa khe cắt ở mỗi cạnh." },
    {
      text: "19,69 mm.",
      correct: true,
      why: "Mỗi cạnh mất s = d/2 + g = 0,125 + 0,03 = 0,155 mm; hai cạnh đối nhau mất 0,31 mm: 20 − 0,31 = 19,69 mm.",
    },
    { text: "19,94 mm.", why: "Mới trừ khe phóng điện 2 × 0,03 mm; còn thiếu bán kính dây 0,125 mm mỗi bên." },
    { text: "20,31 mm.", why: "Vết cắt ăn vào chày chứ không đắp thêm; chày phải nhỏ đi." },
  ],
  hint: "Chọn 'Không bù' rồi đổi sang bù đúng phía để thấy kích thước về 20,00 mm.",
};

export default function WedmBuDay() {
  const [loai, setLoai] = useState<Loai>("chay");
  const [d, setD] = useState(0.25);
  const [g, setG] = useState(0.03);
  const [bu, setBu] = useState<Bu>("khong");

  const s = d / 2 + g;
  const W = d + 2 * g;
  const o = bu === "khong" ? 0 : bu === "ngoai" ? s : -s;
  const kichThuoc = loai === "chay" ? L + 2 * (o - s) : L + 2 * (o + s);
  const sai = kichThuoc - L;
  const dung = Math.abs(sai) < 1e-9;

  /* ---- Hình phóng to quanh một cạnh: trục x tính bằng mm, biên danh nghĩa ở x = 0 (bên trái là phía trong chi tiết) ---- */
  const SW = 320;
  const SH = 190;
  const k = 300; // px / mm
  const x0 = SW / 2;
  const X = (mm: number) => x0 + mm * k;
  const traiKerf = X(o - s);
  const phaiKerf = X(o + s);
  const yDay = 100;

  return (
    <KhungMoPhong ten="Cắt dây: bù đường kính dây và khe phóng điện" doan={DOAN}>
      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="min-w-0">
          <svg viewBox={`0 0 ${SW} ${SH}`} className="w-full" role="img" aria-label="Phóng to một cạnh: dây, khe cắt và biên cần đạt">
            {/* vật liệu giữ lại */}
            {loai === "chay" ? (
              <rect x={0} y={20} width={Math.max(0, traiKerf)} height={150} fill="var(--color-primary)" fillOpacity={0.3} />
            ) : (
              <rect x={phaiKerf} y={20} width={Math.max(0, SW - phaiKerf)} height={150} fill="var(--color-primary)" fillOpacity={0.3} />
            )}
            {/* phần bỏ đi */}
            {loai === "chay" ? (
              <rect x={phaiKerf} y={20} width={Math.max(0, SW - phaiKerf)} height={150} fill="var(--color-surface-2)" />
            ) : (
              <rect x={0} y={20} width={Math.max(0, traiKerf)} height={150} fill="var(--color-surface-2)" />
            )}
            {/* khe cắt */}
            <rect x={traiKerf} y={20} width={phaiKerf - traiKerf} height={150} fill="var(--color-panel)" stroke="var(--color-line-strong)" strokeDasharray="3 3" />
            {/* đường dây đã đi */}
            <line x1={X(o)} y1={20} x2={X(o)} y2={yDay} stroke="var(--color-violet)" strokeWidth={1.5} strokeDasharray="5 4" />
            {/* dây + khe phóng */}
            <circle cx={X(o)} cy={yDay} r={s * k} fill="none" stroke="var(--color-accent)" strokeWidth={1.5} strokeDasharray="2 3" />
            <circle cx={X(o)} cy={yDay} r={(d / 2) * k} fill="var(--color-accent)" opacity={0.85} />
            {/* biên danh nghĩa */}
            <line x1={X(0)} y1={12} x2={X(0)} y2={178} stroke="var(--color-danger)" strokeWidth={2} />
            <text x={X(0) + 4} y={14} fontSize={11} fill="var(--color-danger)">biên cần đạt</text>
            <text x={6} y={186} fontSize={11} fill="var(--color-muted)">
              {loai === "chay" ? "← chày (giữ lại)" : "← lỗ cối (bỏ đi)"}
            </text>
            <text x={SW - 6} y={186} textAnchor="end" fontSize={11} fill="var(--color-muted)">
              {loai === "chay" ? "phế liệu →" : "tấm cối (giữ lại) →"}
            </text>
            <text x={X(o)} y={yDay + s * k + 14} textAnchor="middle" fontSize={11} fill="var(--color-ink)">dây ø{vn(d, 2)}</text>
          </svg>
          <p className="mt-1 text-xs text-muted">Hình phóng to một cạnh (1 mm ≈ 300 px). Vòng nét đứt quanh dây là khe phóng điện g.</p>
        </div>

        <div className="min-w-0 space-y-3">
          <HangNut
            nhan="Cần lấy"
            items={[
              { value: "chay" as Loai, text: "Chày (phần trong)" },
              { value: "coi" as Loai, text: "Lỗ cối" },
            ]}
            value={loai}
            onChange={setLoai}
          />
          <HangNut
            nhan="Đường kính dây d"
            items={[0.1, 0.2, 0.25, 0.3].map((v) => ({ value: v, text: vn(v, 2) }))}
            value={d}
            onChange={setD}
          />
          <TruotSo nhan="Khe phóng điện g mỗi bên" giaTri={g} hien={`${vn(g, 3)} mm`} min={0.01} max={0.05} step={0.005} onChange={setG} />
          <HangNut
            nhan="Tâm dây so với biên"
            items={[
              { value: "khong" as Bu, text: "Không bù" },
              { value: "ngoai" as Bu, text: "Lệch ra ngoài" },
              { value: "trong" as Bu, text: "Lệch vào trong" },
            ]}
            value={bu}
            onChange={setBu}
          />
          <dl className="grid grid-cols-2 gap-2">
            <O nhan="Khe cắt W = d + 2g" so={`${vn(W, 3)} mm`} />
            <O nhan="Lượng bù s = d/2 + g" so={`${vn(s, 3)} mm`} />
            <O nhan={loai === "chay" ? "Cạnh chày đo được" : "Cạnh lỗ cối đo được"} so={`${vn(kichThuoc, 2)} mm`} phu={`danh nghĩa ${L} mm`} />
            <O nhan="Sai lệch" so={`${sai > 0 ? "+" : sai < 0 ? "−" : ""}${vn(Math.abs(sai), 2)} mm`} />
          </dl>
          {dung ? (
            <CanhBao loai="ok">Đúng kích thước: tâm dây lệch {vn(s, 3)} mm về phía phế liệu.</CanhBao>
          ) : (
            <CanhBao loai="danger">
              Sai {vn(Math.abs(sai), 2)} mm. Tâm dây phải lệch về phía {loai === "chay" ? "phế liệu (ra ngoài chày)" : "phần bỏ đi (vào trong lỗ)"}.
            </CanhBao>
          )}
        </div>
      </div>
      <GhiChuMoHinh>
        Hình học thuần: khe cắt W = d + 2g, tâm dây lệch s = d/2 + g. Máy tự tính khi khai báo bù trái/phải (G41/G42);
        khe phóng điện g đổi theo chế độ cắt thô/tinh nên lượng bù mỗi lượt khác nhau. Đổi lượng bù là cách tạo khe hở chày – cối.
      </GhiChuMoHinh>
    </KhungMoPhong>
  );
}
