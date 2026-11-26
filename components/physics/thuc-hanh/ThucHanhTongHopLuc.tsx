"use client";

/**
 * components/physics/thuc-hanh/ThucHanhTongHopLuc.tsx — thí nghiệm ảo "Tổng hợp hai lực đồng quy" theo bộ thiết bị SGK
 * (L10 Bài 22, lesson 67; Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Tự dựng, không lấy gì từ trang khác.
 * Ba lực kế buộc chung nút O trên bảng giấy: lực kế 1, 2 móc vào hai chốt, lực kế 3 treo vật.
 *
 * Trình tự: Dự đoán (PredictGate, T2) → chỉnh F1, F2, α, số 0 lực kế 3 (4 điều khiển, N2) → ghi số mỗi lần bố trí, số đọc có
 * nhiễu (T8) → học sinh tự tính cạnh vẽ, F vẽ, δ, Δ của lần 1 rồi kết luận (L1, L4) → các lần sau máy tính sẵn; bật "số 0 lệch"
 * để thấy CHIỀU lệch (T7) → một câu kiểu đề (T9) → "Chưa nói được gì" (T5).
 * UI: H2 (bảng ≤ 5 cột), C1/H4 (chữ trong hình 16 px), D2 (đích chạm 44 px), D6 (inputmode decimal), M1/M7 (token màu),
 * M4 (✓/✗ kèm chữ), L3 (không điểm, không rank). Không gọi Supabase, không lưu gì.
 */

import { useState } from "react";
import { PredictGate } from "@/components/physics/PredictGate";
import { phuBtn, segBtn } from "@/components/physics/do-luong/chung";
import { BangSoLieu, CauKieuDe, ChuaNoiDuoc, ONhapCham, TrucKhoang } from "./BangSoLieu";
import {
  ALPHA,
  DELTA_GOP,
  F_T,
  SO0_LECH_T,
  XICH,
  chamCanh,
  chamDelta,
  chamDeltaGop,
  chamFve,
  docF3T,
  gocHaiBen,
  nhieuNgauNhien,
  tinhHang,
  vnSo,
  type Hang,
} from "./cham-tong-hop-luc";

const SO_HANG_TOI_DA = 5;
const rad = (d: number) => (d * Math.PI) / 180;

/* ---------------- Cảnh: bảng giấy, ba lực kế, nút O ---------------- */

function LucKe({ x1, y1, x2, y2 }: { x1: number; y1: number; x2: number; y2: number }) {
  // Thân lực kế: hình chữ nhật dọc theo dây, ở đoạn giữa.
  const goc = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
  const cx = (x1 + x2) / 2;
  const cy = (y1 + y2) / 2;
  return (
    <g transform={`rotate(${goc} ${cx} ${cy})`}>
      <rect x={cx - 26} y={cy - 7} width={52} height={14} rx={3} fill="var(--color-surface-2)" stroke="currentColor" />
      {Array.from({ length: 6 }, (_, i) => (
        <line key={i} x1={cx - 20 + i * 8} x2={cx - 20 + i * 8} y1={cy - 7} y2={cy - 2} stroke="currentColor" />
      ))}
    </g>
  );
}

function CanhBang({ h, f3T, so0 }: { h: Pick<Hang, "f1T" | "f2T" | "a">; f3T: number; so0: boolean }) {
  const O = { x: 180, y: 128 };
  const L = 118;
  const { t1, t2 } = gocHaiBen(h.f1T, h.f2T, h.a);
  const p1 = { x: O.x - L * Math.sin(rad(t1)), y: O.y - L * Math.cos(rad(t1)) };
  const p2 = { x: O.x + L * Math.sin(rad(t2)), y: O.y - L * Math.cos(rad(t2)) };
  // cung α quanh O, bán kính 26
  const r = 26;
  const c1 = { x: O.x - r * Math.sin(rad(t1)), y: O.y - r * Math.cos(rad(t1)) };
  const c2 = { x: O.x + r * Math.sin(rad(t2)), y: O.y - r * Math.cos(rad(t2)) };
  const lon = h.a > 180 ? 1 : 0;
  // Chữ F3/vật đặt phía dây KHÔNG chúc xuống (dây chúc xuống dưới O khi góc lệch của nó > 90°).
  const ghiBenTrai = t2 > 90;
  const xGhi = ghiBenTrai ? O.x - 34 : O.x + 34;
  const neoGhi = ghiBenTrai ? "end" : "start";
  const chot = (p: { x: number; y: number }) => <circle cx={p.x} cy={Math.max(p.y, 14)} r={5} fill="currentColor" />;
  // Số chỉ ghi ở hai góc trên của bảng: hai chốt gần nhau (α nhỏ) thì ghi cạnh chốt sẽ đè nhau.
  const ghiTrai = { x: 14, y: 28 };
  const ghiPhai = { x: 346, y: 28 };
  return (
    <svg
      viewBox="0 0 360 260"
      className="block w-full select-none text-ink"
      role="img"
      aria-label={`Bảng giấy, nút O nối ba dây: lực kế 1 chỉ ${vnSo(h.f1T / 10, 1)} N, lực kế 2 chỉ ${vnSo(h.f2T / 10, 1)} N, góc giữa hai dây ${h.a} độ, lực kế 3 treo vật chỉ ${vnSo(f3T / 10, 1)} N`}
    >
      <rect
        x={6}
        y={4}
        width={348}
        height={252}
        rx={6}
        fill="var(--color-surface-2)"
        stroke="var(--color-line-strong)"
      />
      {/* dây 1, 2 */}
      <line x1={O.x} y1={O.y} x2={p1.x} y2={Math.max(p1.y, 14)} stroke="currentColor" strokeWidth={1.5} />
      <line x1={O.x} y1={O.y} x2={p2.x} y2={Math.max(p2.y, 14)} stroke="currentColor" strokeWidth={1.5} />
      <LucKe x1={O.x} y1={O.y} x2={p1.x} y2={Math.max(p1.y, 14)} />
      <LucKe x1={O.x} y1={O.y} x2={p2.x} y2={Math.max(p2.y, 14)} />
      {chot(p1)}
      {chot(p2)}
      <text x={ghiTrai.x} y={ghiTrai.y} fontSize={16} fontWeight={700} fill="currentColor" textAnchor="start">
        F1 = {vnSo(h.f1T / 10, 1)} N
      </text>
      <text x={ghiPhai.x} y={ghiPhai.y} fontSize={16} fontWeight={700} fill="currentColor" textAnchor="end">
        F2 = {vnSo(h.f2T / 10, 1)} N
      </text>
      {/* cung α */}
      <path
        d={`M${c1.x},${c1.y} A${r},${r} 0 ${lon} 1 ${c2.x},${c2.y}`}
        fill="none"
        stroke="var(--color-primary)"
        strokeWidth={2}
      />
      <text
        x={t1 > 90 ? O.x + 12 : O.x - 12}
        y={O.y + 24}
        fontSize={16}
        textAnchor={t1 > 90 ? "start" : "end"}
        fill="var(--color-primary)"
      >
        α = {h.a}°
      </text>
      {/* dây 3 + lực kế 3 + vật */}
      <line x1={O.x} y1={O.y} x2={O.x} y2={214} stroke="currentColor" strokeWidth={1.5} />
      <LucKe x1={O.x} y1={150} x2={O.x} y2={204} />
      <rect x={O.x - 18} y={214} width={36} height={30} rx={3} fill="currentColor" />
      <circle cx={O.x} cy={O.y} r={4} fill="var(--color-danger)" />
      <text x={O.x + 10} y={O.y + 5} fontSize={16} fill="currentColor">
        O
      </text>
      <text
        x={xGhi}
        y={186}
        textAnchor={neoGhi}
        fontSize={16}
        fontWeight={700}
        fill={so0 ? "var(--color-warn)" : "currentColor"}
      >
        F3 = {vnSo(f3T / 10, 1)} N
      </text>
      {so0 && (
        <text x={xGhi} y={208} textAnchor={neoGhi} fontSize={15} fill="var(--color-warn)">
          số 0 lệch +{vnSo(SO0_LECH_T / 10, 1)} N
        </text>
      )}
      <text x={ghiBenTrai ? O.x - 26 : O.x + 26} y={236} textAnchor={neoGhi} fontSize={15} fill="var(--color-muted)">
        vật
      </text>
    </svg>
  );
}

/* ---------------- Giấy vẽ: hình bình hành theo tỉ lệ xích + thước ---------------- */

const PX_CM = 24;

function HinhBinhHanh({ h, cheo }: { h: Hang; cheo: number }) {
  const { t1, t2 } = gocHaiBen(h.f1T, h.f2T, h.a);
  const l1 = (h.f1T / 10 / XICH) * PX_CM;
  const l2 = (h.f2T / 10 / XICH) * PX_CM;
  // Toạ độ tương đối với O (y lên trên là âm); cạnh có thể chúc xuống dưới O khi một góc lệch > 90°.
  const a0 = { x: -l1 * Math.sin(rad(t1)), y: -l1 * Math.cos(rad(t1)) };
  const b0 = { x: l2 * Math.sin(rad(t2)), y: -l2 * Math.cos(rad(t2)) };
  const c0 = { x: a0.x + b0.x, y: a0.y + b0.y };
  const tren = Math.min(0, a0.y, b0.y, c0.y);
  const duoi = Math.max(0, a0.y, b0.y);
  const H = Math.max(140, duoi - tren + 70);
  const O = { x: 200, y: H - 26 - duoi };
  const A = { x: O.x + a0.x, y: O.y + a0.y };
  const B = { x: O.x + b0.x, y: O.y + b0.y };
  const C = { x: O.x + c0.x, y: O.y + c0.y };
  const XT = 34; // thước dọc bên trái
  const soCm = Math.ceil(cheo);
  return (
    <figure>
      <svg
        viewBox={`0 0 360 ${H}`}
        className="block w-full text-ink"
        role="img"
        aria-label="Hình bình hành vẽ theo tỉ lệ xích và thước đo đường chéo"
      >
        {/* hai cạnh lực + hai cạnh song song */}
        <line x1={O.x} y1={O.y} x2={A.x} y2={A.y} stroke="currentColor" strokeWidth={2.5} />
        <line x1={O.x} y1={O.y} x2={B.x} y2={B.y} stroke="currentColor" strokeWidth={2.5} />
        <line x1={A.x} y1={A.y} x2={C.x} y2={C.y} stroke="currentColor" strokeDasharray="4 3" />
        <line x1={B.x} y1={B.y} x2={C.x} y2={C.y} stroke="currentColor" strokeDasharray="4 3" />
        {/* đường chéo */}
        <line x1={O.x} y1={O.y} x2={C.x} y2={C.y} stroke="var(--color-primary)" strokeWidth={3} />
        <circle cx={O.x} cy={O.y} r={3.5} fill="currentColor" />
        <text x={O.x + 8} y={O.y + 18} fontSize={16} fill="currentColor">
          O
        </text>
        <text
          x={A.x - 4 < XT + 70 ? A.x + 4 : A.x - 4}
          y={A.y - 6}
          fontSize={16}
          textAnchor={A.x - 4 < XT + 70 ? "start" : "end"}
          fill="currentColor"
        >
          {vnSo(h.f1T / 10 / XICH, 1)} cm
        </text>
        <text
          x={B.x > 300 ? B.x - 4 : B.x + 4}
          y={B.y - 6}
          fontSize={16}
          textAnchor={B.x > 300 ? "end" : "start"}
          fill="currentColor"
        >
          {vnSo(h.f2T / 10 / XICH, 1)} cm
        </text>
        {/* gióng ngang từ O và đỉnh chéo sang thước */}
        <line x1={XT + 12} x2={O.x} y1={O.y} y2={O.y} stroke="var(--color-muted)" strokeDasharray="2 3" />
        <line x1={XT + 12} x2={C.x} y1={C.y} y2={C.y} stroke="var(--color-primary)" strokeDasharray="2 3" />
        {/* thước: 0 ngang O, vạch mm, số mỗi cm */}
        <line x1={XT} x2={XT} y1={O.y} y2={O.y - soCm * PX_CM} stroke="currentColor" strokeWidth={1.5} />
        {Array.from({ length: soCm * 10 + 1 }, (_, i) => {
          const y = O.y - (i / 10) * PX_CM;
          const w = i % 10 === 0 ? 12 : i % 5 === 0 ? 8 : 4;
          return (
            <line
              key={i}
              x1={XT}
              x2={XT + w}
              y1={y}
              y2={y}
              stroke="currentColor"
              strokeWidth={i % 10 === 0 ? 1.5 : 0.8}
            />
          );
        })}
        {Array.from({ length: soCm + 1 }, (_, i) => (
          <text key={i} x={XT - 6} y={O.y - i * PX_CM + 5} fontSize={15} textAnchor="end" fill="var(--color-muted)">
            {i}
          </text>
        ))}
      </svg>
      <figcaption className="mt-1 text-sm text-muted">
        Tỉ lệ xích 1 cm ↔ 0,5 N. Đường chéo qua O (xanh) đo trên thước được{" "}
        <b className="text-ink">{vnSo(cheo, 1)} cm</b>.
      </figcaption>
    </figure>
  );
}

/* ---------------- Nội dung câu hỏi ---------------- */

const DU_DOAN = {
  question:
    "Đổi sang một lực kế 3 chưa chỉnh số 0: chưa móc vật đã chỉ 0,4 N. Làm vài lần với các góc khác nhau, so F3 đọc được với F vẽ từ hình bình hành. Kết quả sẽ thế nào?",
  options: [
    {
      text: "Lần nào F3 cũng lớn hơn F vẽ, chừng 0,4 N.",
      correct: true,
      why: "Lò xo đã dãn sẵn nên mọi số đọc cộng thêm cùng một lượng: lệch về một phía, như nhau ở mọi lần.",
    },
    {
      text: "Lúc F3 lớn hơn, lúc nhỏ hơn F vẽ.",
      why: "Số 0 lệch cộng cùng một lượng vào mọi lần đọc, không lên xuống ngẫu nhiên.",
    },
    {
      text: "F3 nhỏ hơn F vẽ.",
      why: "Chưa treo vật đã chỉ 0,4 N thì treo vật vào sẽ chỉ dư thêm 0,4 N, không thiếu.",
    },
    {
      text: "Không lệch, vì làm nhiều lần rồi lấy trung bình là hết.",
      why: "Lấy trung bình chỉ giảm phần lên xuống ngẫu nhiên; phần dư một phía vẫn còn nguyên.",
    },
  ],
};

const CAU_DE = {
  de: "Trong thí nghiệm tổng hợp hai lực đồng quy, ba lực kế buộc chung nút O; lực kế 1, 2 móc vào hai chốt, lực kế 3 treo vật. Phát biểu nào sau đây sai?",
  cac: [
    {
      text: "Nút O đứng yên nên lực của lực kế 3 cân bằng với hợp lực của F1 và F2.",
      why: "O đứng yên: ba lực tác dụng lên O có tổng bằng 0, nên F3 cùng độ lớn, ngược chiều với hợp lực F.",
    },
    {
      text: "Giữ nguyên F1, F2 mà tăng góc α giữa hai dây thì lực kế 3 chỉ số nhỏ hơn.",
      why: "F² = F1² + F2² + 2F1F2cos α: α tăng thì cos α giảm, F giảm.",
    },
    {
      text: "Vẽ hai cạnh F1, F2 hợp nhau góc 180° − α rồi lấy đường chéo vẫn được đúng hợp lực.",
      dung: true,
      why: "Hai cạnh phải chung gốc O và hợp nhau đúng góc α giữa hai dây; dùng góc bù là ra đường chéo kia, sai độ lớn.",
    },
    {
      text: "Lực kế 3 chưa chỉnh số 0 làm F3 lệch cùng một phía ở mọi lần; làm thêm nhiều lần không khử được.",
      why: "Đó là sai số lệch về một phía; phải chỉnh số 0 đúng tư thế dùng (hoặc trừ số lệch).",
    },
  ],
};

/* ---------------- Thành phần chính ---------------- */

export default function ThucHanhTongHopLuc() {
  const [duDoan, setDuDoan] = useState<number | null>(null);
  const [f1T, setF1T] = useState(F_T.macDinh);
  const [f2T, setF2T] = useState(F_T.macDinh);
  const [a, setA] = useState(ALPHA.macDinh);
  const [so0, setSo0] = useState(false);
  const [nhieu, setNhieu] = useState(() => nhieuNgauNhien());
  const [hang, setHang] = useState<Hang[]>([]);
  const [buocTinh, setBuocTinh] = useState(0);
  const [hsFve, setHsFve] = useState<number | null>(null);
  const [ketLuan, setKetLuan] = useState<boolean | null>(null);

  const f3T = docF3T(f1T, f2T, a, so0, nhieu);
  const cuoi = hang[hang.length - 1];
  const trungLanTruoc = !!cuoi && cuoi.f1T === f1T && cuoi.f2T === f2T && cuoi.a === a && cuoi.so0 === so0;
  const h1 = hang[0];
  const kq1 = h1 ? tinhHang(h1) : null;
  const hsXong = ketLuan !== null;
  const dangChoTinh = !!h1 && !hsXong;

  const doi = (fn: () => void) => {
    fn();
    setNhieu(nhieuNgauNhien());
  };
  const ghi = () => {
    if (dangChoTinh || trungLanTruoc || hang.length >= SO_HANG_TOI_DA) return;
    setHang((hs) => [...hs, { f1T, f2T, a, f3T, so0 }]);
  };

  const coCaHai = hang.some((x) => x.so0) && hang.some((x) => !x.so0);
  const bangKq = hang.map(tinhHang);

  const dieuKhien = (
    nhan: string,
    giaTri: string,
    giam: () => void,
    tang: () => void,
    khoaGiam: boolean,
    khoaTang: boolean,
  ) => (
    <div className="flex items-center gap-2">
      <span className="w-24 shrink-0 text-sm text-muted">{nhan}</span>
      <button type="button" className={phuBtn} aria-label={`Giảm ${nhan}`} disabled={khoaGiam} onClick={giam}>
        −
      </button>
      <span className="min-w-0 flex-1 text-center font-mono text-lg tabular-nums">{giaTri}</span>
      <button type="button" className={phuBtn} aria-label={`Tăng ${nhan}`} disabled={khoaTang} onClick={tang}>
        +
      </button>
    </div>
  );

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Thí nghiệm ảo tổng hợp hai lực đồng quy"
    >
      <h2 className="font-display text-lg font-semibold">Thí nghiệm ảo: tổng hợp hai lực đồng quy</h2>
      <p className="mt-1 text-base text-muted">
        Nhiệm vụ: ghi số lần 1, tự vẽ (theo tỉ lệ xích) và so F vẽ với F3. Rồi đổi bố trí, bật “số 0 lệch” và so tiếp.
      </p>

      <div className="mt-3">
        <PredictGate
          question={DU_DOAN.question}
          options={DU_DOAN.options}
          choice={duDoan}
          onChoose={setDuDoan}
          hint="Kiểm bằng số: tính xong lần 1, ghi thêm vài lần, rồi bật số 0 lệch và ghi tiếp."
        />
      </div>

      {duDoan !== null && (
        <>
          {/* Điều khiển (N2): F1, F2, α, số 0 lực kế 3. */}
          <div className="mt-3 space-y-2">
            {dieuKhien(
              "Lực kế 1",
              `F1 = ${vnSo(f1T / 10, 1)} N`,
              () => doi(() => setF1T(f1T - 1)),
              () => doi(() => setF1T(f1T + 1)),
              dangChoTinh || f1T <= F_T.min,
              dangChoTinh || f1T >= F_T.max,
            )}
            {dieuKhien(
              "Lực kế 2",
              `F2 = ${vnSo(f2T / 10, 1)} N`,
              () => doi(() => setF2T(f2T - 1)),
              () => doi(() => setF2T(f2T + 1)),
              dangChoTinh || f2T <= F_T.min,
              dangChoTinh || f2T >= F_T.max,
            )}
            {dieuKhien(
              "Góc hai dây",
              `α = ${a}°`,
              () => doi(() => setA(a - ALPHA.buoc)),
              () => doi(() => setA(a + ALPHA.buoc)),
              dangChoTinh || a <= ALPHA.min,
              dangChoTinh || a >= ALPHA.max,
            )}
            <div className="flex items-center gap-2">
              <span className="w-24 shrink-0 text-sm text-muted">Số 0 lực kế 3</span>
              <div className="flex flex-1 gap-2">
                <button
                  type="button"
                  className={segBtn(!so0)}
                  disabled={dangChoTinh}
                  onClick={() => so0 && doi(() => setSo0(false))}
                >
                  Đã chỉnh
                </button>
                <button
                  type="button"
                  className={segBtn(so0)}
                  disabled={dangChoTinh || !hsXong}
                  onClick={() => !so0 && doi(() => setSo0(true))}
                >
                  Lệch +{vnSo(SO0_LECH_T / 10, 1)} N
                </button>
              </div>
            </div>
            {dangChoTinh && <p className="text-sm text-muted">Tính xong lần 1 rồi mới đổi bố trí.</p>}
          </div>

          <div className="mt-3">
            <CanhBang h={{ f1T, f2T, a }} f3T={f3T} so0={so0} />
            <p className="text-sm text-muted">
              Chỉnh F1, F2, α là dời hai chốt trên giá. Nút O đứng yên rồi mới đọc. Dây nhẹ, không dãn.
            </p>
          </div>
          <div className="mt-2">
            <button
              type="button"
              className="min-h-11 w-full rounded-lg bg-primary px-4 text-base font-semibold text-white disabled:opacity-50"
              disabled={dangChoTinh || trungLanTruoc || hang.length >= SO_HANG_TOI_DA}
              onClick={ghi}
            >
              Chấm phương, ghi số lần {hang.length + 1}
            </button>
            {trungLanTruoc && !dangChoTinh && (
              <p className="mt-1 text-sm text-muted">Đổi F1, F2, α hoặc số 0 rồi mới ghi lần mới.</p>
            )}
            {hang.length >= SO_HANG_TOI_DA && <p className="mt-1 text-sm text-muted">Đủ {SO_HANG_TOI_DA} lần.</p>}
          </div>

          {/* Bảng số đọc (H2: 5 cột). */}
          {hang.length > 0 && (
            <div className="mt-3">
              <BangSoLieu
                tieuDe="Bảng số đọc"
                cot={[{ nhan: "Lần" }, { nhan: "F1 (N)" }, { nhan: "F2 (N)" }, { nhan: "α (°)" }, { nhan: "F3 (N)" }]}
                hang={hang.map((x, i) => [
                  i + 1,
                  vnSo(x.f1T / 10, 1),
                  vnSo(x.f2T / 10, 1),
                  x.a,
                  <span key="f3" className={x.so0 ? "text-warn" : ""}>
                    {vnSo(x.f3T / 10, 1)}
                    {x.so0 ? "*" : ""}
                  </span>,
                ])}
              />
              {hang.some((x) => x.so0) && <p className="mt-1 text-sm text-warn">* lực kế 3 chưa chỉnh số 0.</p>}
            </div>
          )}

          {/* Học sinh tự xử lí lần 1 (L1, L4). */}
          {h1 && kq1 && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">
                Tự xử lí lần 1 (tỉ lệ xích 1 cm ↔ 0,5 N, mỗi lực kế sai số 0,1 N)
              </p>
              <ONhapCham
                nhan={<>1. Cạnh vẽ cho F1 = {vnSo(h1.f1T / 10, 1)} N dài</>}
                donVi="cm"
                vidu="4,0"
                cham={(r) => chamCanh(r, h1.f1T / 10)}
                onXong={() => setBuocTinh((b) => Math.max(b, 1))}
              />
              {buocTinh >= 1 && <HinhBinhHanh h={h1} cheo={kq1.cheo} />}
              {buocTinh >= 1 && (
                <ONhapCham
                  nhan={<>2. Đổi đường chéo ra lực: F vẽ =</>}
                  donVi="N"
                  vidu="3,45"
                  cham={(r) => chamFve(r, h1, kq1)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHsFve(v);
                    setBuocTinh((b) => Math.max(b, 2));
                  }}
                />
              )}
              {buocTinh >= 2 && (
                <ONhapCham
                  nhan={<>3. Độ lệch δ = |F vẽ − F3| =</>}
                  donVi="N"
                  vidu="0,05"
                  cham={(r) => chamDelta(r, hsFve ?? kq1.fVe, kq1)}
                  onXong={() => setBuocTinh((b) => Math.max(b, 3))}
                />
              )}
              {buocTinh >= 3 && (
                <ONhapCham
                  nhan={<>4. Sai số gộp Δ = ΔF1 + ΔF2 + ΔF3 =</>}
                  donVi="N"
                  vidu="0,3"
                  cham={(r) => chamDeltaGop(r)}
                  onXong={() => setBuocTinh((b) => Math.max(b, 4))}
                />
              )}
              {buocTinh >= 4 && (
                <div className="rounded-xl border border-line bg-surface-2 p-3">
                  <p className="text-base text-ink">
                    5. δ = {vnSo(Math.abs((hsFve ?? kq1.fVe) - kq1.f3), 2)} N, Δ = {vnSo(DELTA_GOP, 1)} N. Kết luận?
                  </p>
                  <div className="mt-2 grid gap-2">
                    {[true, false].map((chon) => {
                      const dung = chon === Math.abs((hsFve ?? kq1.fVe) - kq1.f3) <= DELTA_GOP + 1e-9;
                      const daChon = ketLuan !== null;
                      return (
                        <button
                          key={String(chon)}
                          type="button"
                          disabled={daChon}
                          onClick={() => setKetLuan(chon)}
                          className={`min-h-11 rounded-lg border bg-panel px-3 py-2 text-left text-base text-ink ${
                            !daChon
                              ? "border-line-strong hover:bg-primary-soft"
                              : dung
                                ? "border-ok"
                                : ketLuan === chon
                                  ? "border-danger"
                                  : "border-line opacity-80"
                          }`}
                        >
                          {chon
                            ? "δ ≤ Δ: hợp quy tắc hình bình hành trong phạm vi sai số."
                            : "δ > Δ: chưa khớp, phải tìm nguyên nhân trước khi kết luận."}
                        </button>
                      );
                    })}
                  </div>
                  {ketLuan !== null && (
                    <p className="mt-2 text-base text-ink" aria-live="polite">
                      {ketLuan === Math.abs((hsFve ?? kq1.fVe) - kq1.f3) <= DELTA_GOP + 1e-9 ? (
                        <b className="text-ok">✓ Đúng.</b>
                      ) : (
                        <b className="text-danger">✗ Chưa đúng.</b>
                      )}{" "}
                      So δ với Δ: độ lệch nằm trong sai số đọc của ba lực kế thì chưa có gì trái quy tắc. Giờ đổi bố trí
                      (F1, F2, α), ghi thêm vài lần; rồi bật <b>Lệch +{vnSo(SO0_LECH_T / 10, 1)} N</b> và ghi tiếp.
                    </p>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Máy xử lí các lần + so (T7). */}
          {hsXong && (
            <div className="mt-4 space-y-2">
              <BangSoLieu
                tieuDe="Xử lí (máy tính sẵn)"
                cot={[
                  { nhan: "Lần" },
                  { nhan: "chéo (cm)" },
                  { nhan: "F vẽ (N)" },
                  { nhan: "F3 (N)" },
                  { nhan: "δ (N)" },
                ]}
                hang={bangKq.map((k, i) => [
                  i + 1,
                  vnSo(k.cheo, 1),
                  vnSo(k.fVe, 2),
                  vnSo(k.f3, 1),
                  <span key="d" className={k.khop ? "" : "font-semibold text-danger"}>
                    {vnSo(k.delta, 2)} {k.khop ? "≤ Δ" : "> Δ"}
                  </span>,
                ])}
              />
              <TrucKhoang
                lo={-0.8}
                hi={0.8}
                vach={[-0.6, -0.3, 0, 0.3, 0.6]}
                moc={0}
                ds={bangKq.map((k, i) => ({
                  nhan: `L${i + 1}`,
                  giua: k.f3 - k.fVe,
                  ban: DELTA_GOP,
                  phu: hang[i].so0,
                }))}
                ghiVach={(v) => vnSo(v, 1)}
                aria="Độ lệch F3 trừ F vẽ của từng lần, kèm sai số gộp 0,3 N"
                chuThich="Mỗi đoạn: (F3 − F vẽ) ± Δ của một lần (cam: lực kế 3 chưa chỉnh số 0). Đoạn chạm vạch 0 xanh lá: khớp trong sai số."
              />
              {coCaHai ? (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base leading-relaxed">
                  Các lần số 0 lệch: F3 luôn <b>lớn hơn</b> F vẽ chừng {vnSo(SO0_LECH_T / 10, 1)} N, đoạn cam dồn hẳn
                  sang phải, thường vượt Δ. Đó không phải quy tắc hình bình hành sai: trừ số lệch (hoặc chỉnh số 0 đúng
                  tư thế treo) thì δ lại nhỏ. Vượt sát Δ thì tìm nguyên nhân lệch một phía trước khi kết luận.
                </p>
              ) : (
                <p className="text-base text-muted">
                  {hang.length < 2
                    ? "Đổi F1, F2 hoặc α rồi ghi thêm một lần: máy xử lí sẵn."
                    : "Bật “Lệch +0,4 N” ở Số 0 lực kế 3 rồi ghi thêm lần mới để so."}
                </p>
              )}
            </div>
          )}

          {hsXong && (
            <div className="mt-4 space-y-3">
              <CauKieuDe de={CAU_DE.de} cac={CAU_DE.cac} />
              <ChuaNoiDuoc
                y={[
                  "Chỉ kiểm hai lực đồng quy trong một mặt phẳng; chưa nói gì về hai lực song song hay về tác dụng làm quay.",
                  "Một lần đo δ ≤ Δ chưa đủ để tin quy tắc: phải đúng ở nhiều góc, nhiều cặp lực khác nhau.",
                ]}
              />
            </div>
          )}
        </>
      )}
    </section>
  );
}
