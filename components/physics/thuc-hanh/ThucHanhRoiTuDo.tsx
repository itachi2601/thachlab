"use client";

/**
 * components/physics/thuc-hanh/ThucHanhRoiTuDo.tsx — thí nghiệm ảo "Đo gia tốc rơi tự do" theo bộ thiết bị SGK
 * (L10 Bài 11, lesson 56; Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Tự dựng, không lấy gì từ trang khác.
 * Nam châm điện nối ổ A (ngắt công tắc → đồng hồ bắt đầu đếm), cổng quang nối ổ B, MODE A↔B; đồng hồ là `BangDongHoHienSo` của Gói A.
 *
 * Trình tự: Dự đoán (PredictGate, T2) → chỉnh độ cao + bật/tắt từ dư (≤ 4 điều khiển, N2) → thả 5 lần, số tự vào bảng (T8)
 * → học sinh tự tính t̄, Δt, ḡ, Δg, được chấm (L1, L4) → đo bảng thứ hai để thấy CHIỀU lệch của từ dư (T7)
 * → một câu kiểu đề (T9) → "Chưa nói được gì" (T5) + "Bỏ qua…" (T6).
 * UI: B4 (bi đứng yên tới khi bấm Thả), H2 (bảng 3 cột xếp dọc ở 375 px), C1/H4 (chữ trong hình ≥ 14 px ở 360 px),
 * D2 (đích chạm 44 px), D6 (inputmode decimal), M1/M7 (token màu, nền sáng/tối), M4 (✓/✗ kèm chữ), L3 (không điểm, không rank).
 * Không gọi Supabase, không lưu gì.
 */

import { useMemo, useState } from "react";
import { PredictGate } from "@/components/physics/PredictGate";
import { BangDongHoHienSo, useDongHoHienSo, type LanChan } from "@/components/physics/do-luong/DongHoHienSo";
import { phuBtn, segBtn } from "@/components/physics/do-luong/chung";
import { BangSoLieu, CauKieuDe, ChuaNoiDuoc, ONhapCham, TrucKhoang } from "./BangSoLieu";
import {
  DC_T,
  G_THAT,
  S_CM,
  TRE_TU_DU_MS,
  chamDg,
  chamDt,
  chamG,
  chamTbar,
  nhieuNgauNhien,
  soChiMs,
  tinhLoat,
  tRoiMs,
  vnSo,
  type KetQuaLoat,
} from "./cham-roi-tu-do";

const SO_LAN = 5;
const CHIEU_CHAM = 4; // chiếu chậm 4 lần để mắt kịp thấy bi rơi 0,3 s
const D_BI = 0.02; // m, đường kính bi (để tính lúc bi ra khỏi tia)

/* ---------------- Cảnh: giá đỡ, nam châm, bi, cổng quang, thước ---------------- */

const Y0 = 52; // px: mép dưới bi lúc còn ở nam châm
const K = 200; // px/m
const R = 8; // px, bán kính bi vẽ (không theo tỉ lệ)
const X_BI = 132;

function CanhRoi({
  s,
  tMs,
  lan,
  treMs,
  tuDu,
  xong,
}: {
  s: number;
  tMs: number;
  lan: LanChan[];
  treMs: number;
  tuDu: boolean;
  xong: boolean;
}) {
  const t = Math.max(0, tMs - treMs) / 1000;
  const yDay = xong ? 282 : Math.min(Y0 + 0.5 * G_THAT * t * t * K, 282); // xong: bi nằm trong hộp hứng
  const yCong = Y0 + s * K;
  const b = lan.find((l) => l.o === "B");
  const chan = !!b && tMs >= b.vao && tMs <= b.ra;
  return (
    <svg
      viewBox="0 0 360 292"
      className="block w-full select-none text-ink"
      role="img"
      aria-label="Giá đỡ, nam châm điện giữ viên bi, cổng quang cách đáy bi một đoạn s, thước đo"
    >
      {/* giá đỡ */}
      <line x1={40} y1={10} x2={40} y2={284} stroke="currentColor" strokeWidth={4} />
      <line x1={14} y1={284} x2={200} y2={284} stroke="currentColor" strokeWidth={4} />
      <line x1={40} y1={26} x2={112} y2={26} stroke="currentColor" strokeWidth={3} />
      {/* nam châm điện */}
      <rect
        x={112}
        y={12}
        width={40}
        height={28}
        rx={4}
        fill="var(--color-surface-2)"
        stroke="currentColor"
        strokeWidth={2}
      />
      <text x={160} y={24} fontSize={16} fill="currentColor">
        Nam châm điện
      </text>
      {tuDu && (
        <text x={160} y={42} fontSize={16} fill="var(--color-warn)">
          còn từ dư
        </text>
      )}
      {/* thước */}
      <line x1={80} y1={Y0} x2={80} y2={Y0 + K} stroke="currentColor" strokeWidth={1.5} />
      {Array.from({ length: 11 }, (_, i) => (
        <line
          key={i}
          x1={80}
          x2={i % 5 === 0 ? 92 : 87}
          y1={Y0 + i * 0.1 * K}
          y2={Y0 + i * 0.1 * K}
          stroke="currentColor"
          strokeWidth={1.5}
        />
      ))}
      {[0, 0.5, 1].map((m) => (
        <text key={m} x={74} y={Y0 + m * K + 5} textAnchor="end" fontSize={16} fill="var(--color-muted)">
          {m === 0 ? "0" : vnSo(m, 1)}
        </text>
      ))}
      {/* hộp mềm hứng bi */}
      <rect
        x={112}
        y={270}
        width={40}
        height={14}
        rx={2}
        fill="var(--color-surface-2)"
        stroke="var(--color-line-strong)"
      />
      {/* cổng quang */}
      <rect x={100} y={yCong - 9} width={10} height={18} rx={2} fill="currentColor" />
      <rect x={154} y={yCong - 9} width={10} height={18} rx={2} fill="currentColor" />
      <line
        x1={110}
        x2={154}
        y1={yCong}
        y2={yCong}
        stroke={chan ? "var(--color-danger)" : "var(--color-ok)"}
        strokeWidth={2}
        strokeDasharray="4 3"
      />
      <text x={170} y={yCong + 5} fontSize={16} fill="currentColor">
        Cổng quang
      </text>
      {/* kích thước s */}
      <line x1={286} x2={286} y1={Y0} y2={yCong} stroke="currentColor" strokeWidth={1.5} />
      <line x1={278} x2={294} y1={Y0} y2={Y0} stroke="currentColor" strokeWidth={1.5} />
      <line x1={278} x2={294} y1={yCong} y2={yCong} stroke="currentColor" strokeWidth={1.5} />
      <line x1={152} x2={278} y1={Y0} y2={Y0} stroke="currentColor" strokeWidth={1} strokeDasharray="2 3" />
      <text
        x={282}
        y={(Y0 + yCong) / 2 + (s < 0.3 ? -22 : 5)}
        textAnchor="end"
        fontSize={16}
        fontWeight={700}
        fill="currentColor"
      >
        s = {vnSo(s, 3)} m
      </text>
      {/* bi */}
      <circle cx={X_BI} cy={yDay - R} r={R} fill="currentColor" />
    </svg>
  );
}

/* ---------------- Số liệu ---------------- */

/** so: số thứ tự bảng (Bảng 1 là bảng học sinh tự tính). */
type Loat = { so: number; sCm: number; tuDu: boolean; tMs: number[] };
type TomTat = { so: number; sCm: number; tuDu: boolean; kq: KetQuaLoat };

/** Trục số: mỗi bảng đã đo là một khoảng ḡ ± Δg, vạch đứng 9,8. */
function TrucKetQua({ ds }: { ds: TomTat[] }) {
  return (
    <TrucKhoang
      lo={9.2}
      hi={10.2}
      vach={[9.2, 9.6, 9.8, 10.0]}
      moc={G_THAT}
      ds={ds.map((d) => ({ nhan: `B${d.so}`, giua: d.kq.g, ban: d.kq.dg, phu: d.tuDu }))}
      ghiVach={(v) => vnSo(v, 1)}
      aria="Các khoảng g đo được so với 9,8 m/s²"
      chuThich="Vạch xanh lá đứt: 9,8 m/s². Mỗi đoạn: ḡ ± Δg của một bảng (cam: có từ dư)."
    />
  );
}

/* ---------------- Nội dung câu hỏi ---------------- */

const DU_DOAN = {
  question:
    "Nam châm còn từ dư: ngắt công tắc thì đồng hồ bắt đầu đếm ngay, nhưng lõi sắt vẫn còn hút nhẹ viên bi. So với khi không có từ dư (cùng độ cao s), 5 số t đo được sẽ thế nào?",
  options: [
    {
      text: "Cùng lớn hơn, vẫn chụm như cũ.",
      correct: true,
      why: "Lần nào đồng hồ cũng đếm thêm khoảng bi còn bám nam châm, nên cả loạt dịch lên như nhau; độ chụm do nhiễu ngẫu nhiên quyết định.",
    },
    {
      text: "Cùng nhỏ hơn, vẫn chụm như cũ.",
      why: "Đồng hồ đếm từ lúc ngắt điện, bi rời muộn thì thời gian đếm dài ra chứ không ngắn đi.",
    },
    {
      text: "Tản ra nhiều hơn, trung bình không đổi.",
      why: "Từ dư làm bi rời muộn gần như cùng một khoảng mỗi lần: lệch về một phía, không phải lên xuống ngẫu nhiên.",
    },
    {
      text: "Không đổi, vì lấy trung bình 5 lần là hết sai số.",
      why: "Lấy trung bình chỉ giảm phần lên xuống ngẫu nhiên; phần lệch một phía vẫn còn nguyên.",
    },
  ],
};

const CAU_DE = {
  de: "Một nhóm đo g bằng nam châm điện, cổng quang và đồng hồ hiện số (MODE A↔B), thả bi 5 lần từ s = 0,500 m. Nam châm còn từ dư nên bi rời nam châm muộn hơn lúc đồng hồ bắt đầu đếm. Phát biểu nào sau đây sai?",
  cac: [
    {
      text: "Năm số t lệch nhau vài phần nghìn giây là do sai số ngẫu nhiên.",
      why: "Các lần lên xuống quanh giá trị trung bình là sai số ngẫu nhiên.",
    },
    {
      text: "Từ dư làm mọi số t lớn hơn thời gian rơi thật nên ḡ nhỏ hơn g thật.",
      why: "g = 2s/t²: t lớn hơn thì g tính ra nhỏ hơn.",
    },
    {
      text: "Đặt cổng quang thấp hơn (s lớn hơn) thì ḡ càng lệch nhiều khỏi g thật.",
      dung: true,
      why: "Độ trễ do từ dư gần như không đổi, nên t càng lớn thì phần trễ càng nhỏ so với t: thả cao hơn ḡ lệch ÍT hơn (có từ dư, s = 0,200 m cho ḡ ≈ 9,3; s = 1,000 m cho ḡ ≈ 9,6 m/s²). Cách giảm thật: chỉnh dòng điện nam châm vừa đủ giữ bi.",
    },
    {
      text: "Kết quả có thể chụm (Δg nhỏ) mà khoảng ḡ ± Δg vẫn không chứa giá trị thật.",
      why: "Δg tính từ độ phân tán và dụng cụ, không phát hiện được phần lệch một phía (xem bảng có từ dư).",
    },
  ],
};

/* ---------------- Thành phần chính ---------------- */

export default function ThucHanhRoiTuDo() {
  const [duDoan, setDuDoan] = useState<number | null>(null);
  const [sCm, setSCm] = useState(S_CM.macDinh);
  const [tuDu, setTuDu] = useState(false);
  const [nhieu, setNhieu] = useState(() => nhieuNgauNhien());
  const [loat, setLoat] = useState<Loat>({ so: 1, sCm: S_CM.macDinh, tuDu: false, tMs: [] });
  const [lichSu, setLichSu] = useState<TomTat[]>([]);
  /** Bảng học sinh tự tính (bảng đầy đủ đầu tiên) và số ô đã chấm (0..4). */
  const [bangTinh, setBangTinh] = useState<Loat | null>(null);
  const [buocTinh, setBuocTinh] = useState(0);
  /** Δt, ḡ học sinh đã nhập ĐÚNG (để chấm Δg theo số của em, không phạt làm tròn hợp lí). */
  const [hsDt, setHsDt] = useState<number | null>(null);
  const [hsG, setHsG] = useState<number | null>(null);

  const s = sCm / 100;
  const treMs = tuDu ? TRE_TU_DU_MS : 0;
  const tSau = soChiMs(s, tuDu, nhieu); // số chỉ của lần thả sắp tới (đã tính trước để đồng hồ chạy theo)
  const lan = useMemo<LanChan[]>(() => {
    const vRoi = (G_THAT * tRoiMs(s)) / 1000;
    return [
      { o: "A", vao: 0, ra: 1 },
      { o: "B", vao: tSau, ra: tSau + Math.max(2, Math.round((1000 * D_BI) / vRoi)) },
    ];
  }, [s, tSau]);
  const may = useDongHoHienSo(lan, { cham: CHIEU_CHAM, keoThem: 150 });

  const hsXong = buocTinh >= 4;
  const dangChoTinh = !!bangTinh && !hsXong;
  const khoaDieuKien = may.trangThai === "chay" || dangChoTinh;

  // Số chỉ đã biết trước lúc thả: ghi ngay trong lúc bấm, nhưng chỉ HIỆN khi bi qua cổng xong (T8: mỗi lần một số khác).
  const tha = () => {
    if (may.trangThai !== "cho" || dangChoTinh) return;
    const bangMoi = loat.tMs.length >= SO_LAN;
    const moi: Loat = { so: bangMoi ? loat.so + 1 : loat.so, sCm, tuDu, tMs: bangMoi ? [tSau] : [...loat.tMs, tSau] };
    setLoat(moi);
    if (moi.tMs.length === SO_LAN) {
      if (!bangTinh) setBangTinh(moi);
      else setLichSu((ls) => [...ls, { so: moi.so, sCm, tuDu, kq: tinhLoat(moi.tMs, sCm / 100) }].slice(-4));
    }
    may.tha();
  };
  const reset = () => {
    may.reset();
    setNhieu(nhieuNgauNhien());
  };
  const doiDieuKien = (sMoi: number, tuDuMoi: boolean) => {
    setSCm(sMoi);
    setTuDu(tuDuMoi);
    setLoat((cu) => ({ so: cu.tMs.length === SO_LAN ? cu.so + 1 : cu.so, sCm: sMoi, tuDu: tuDuMoi, tMs: [] })); // đổi điều kiện → bảng mới
    reset();
  };
  const xongTinh = () => {
    const nb = buocTinh + 1;
    setBuocTinh(nb);
    if (nb === 4 && bangTinh)
      setLichSu((ls) => [
        { so: bangTinh.so, sCm: bangTinh.sCm, tuDu: bangTinh.tuDu, kq: tinhLoat(bangTinh.tMs, bangTinh.sCm / 100) },
        ...ls,
      ]);
  };

  const bangDay = loat.tMs.length === SO_LAN;
  const khoaTha = dangChoTinh;
  const kqTinh = bangTinh ? tinhLoat(bangTinh.tMs, bangTinh.sCm / 100) : null;
  const dangHienLaBangTinh = loat.so === 1;
  const chay = may.trangThai === "chay";
  // Bảng vừa đủ 5 lần: chờ bi qua cổng rồi mới hiện kết quả của nó.
  const lichSuHien = chay && bangDay && loat.so !== 1 ? lichSu.slice(0, -1) : lichSu;
  const coCaHai = lichSuHien.some((l) => l.tuDu) && lichSuHien.some((l) => !l.tuDu);

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Thí nghiệm ảo đo gia tốc rơi tự do"
    >
      <h2 className="font-display text-lg font-semibold">Thí nghiệm ảo: đo gia tốc rơi tự do</h2>
      <p className="mt-1 text-base text-muted">
        Nhiệm vụ: thả bi 5 lần, tự tính g = ḡ ± Δg. Rồi bật “từ dư”, đo thêm một bảng và so.
      </p>

      <div className="mt-3">
        <PredictGate
          question={DU_DOAN.question}
          options={DU_DOAN.options}
          choice={duDoan}
          onChoose={setDuDoan}
          hint="Kiểm bằng số: đo bảng 1 khi chưa có từ dư, rồi bật từ dư, đo bảng 2."
        />
      </div>

      {duDoan !== null && (
        <>
          {/* Điều khiển (N2): độ cao, từ dư; đồng hồ có RESET và Thả. */}
          <div className="mt-3 space-y-2">
            <div className="flex items-center gap-2">
              <span className="w-24 shrink-0 text-sm text-muted">Độ cao s</span>
              <button
                type="button"
                className={phuBtn}
                aria-label="Giảm độ cao"
                disabled={khoaDieuKien || sCm <= S_CM.min}
                onClick={() => doiDieuKien(sCm - S_CM.buoc, tuDu)}
              >
                −
              </button>
              <span className="min-w-0 flex-1 text-center font-mono text-lg tabular-nums">{vnSo(s, 3)} m</span>
              <button
                type="button"
                className={phuBtn}
                aria-label="Tăng độ cao"
                disabled={khoaDieuKien || sCm >= S_CM.max}
                onClick={() => doiDieuKien(sCm + S_CM.buoc, tuDu)}
              >
                +
              </button>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-24 shrink-0 text-sm text-muted">Từ dư nam châm</span>
              <div className="flex flex-1 gap-2">
                <button
                  type="button"
                  className={segBtn(!tuDu)}
                  disabled={khoaDieuKien}
                  onClick={() => tuDu && doiDieuKien(sCm, false)}
                >
                  Không
                </button>
                <button
                  type="button"
                  className={segBtn(tuDu)}
                  disabled={khoaDieuKien}
                  onClick={() => !tuDu && doiDieuKien(sCm, true)}
                >
                  Có
                </button>
              </div>
            </div>
            {dangChoTinh && <p className="text-sm text-muted">Tính xong bảng 1 rồi mới đổi điều kiện.</p>}
          </div>

          <div className="mt-3">
            <CanhRoi s={s} tMs={may.tMs} lan={lan} treMs={treMs} tuDu={tuDu} xong={may.trangThai === "xong"} />
            <p className="text-sm text-muted">
              Bi rơi chiếu chậm {CHIEU_CHAM} lần. Bỏ qua sức cản không khí. Coi giá thẳng đứng, tia sáng ngang mép dưới
              bi.
            </p>
          </div>
          <div className="mt-2">
            <BangDongHoHienSo
              mode="A↔B"
              onMode={() => undefined}
              ms={may.soChi("A↔B")}
              trangThai={may.trangThai}
              onReset={reset}
              onTha={tha}
              nhanTha={bangDay && !khoaTha ? "Thả (bảng mới)" : "Ngắt nam châm"}
              cacMode={["A↔B"]}
              noiO={{ A: "công tắc nam châm", B: "cổng quang" }}
              khoaTha={khoaTha}
            />
          </div>

          {/* Bảng số liệu, 3 cột xếp dọc (H2). */}
          <div className="mt-3">
            <p className="text-base font-semibold">
              Bảng {loat.so} · s = {vnSo(loat.sCm / 100, 3)} m · {loat.tuDu ? "có từ dư" : "không từ dư"}
            </p>
            <BangSoLieu
              cot={[{ nhan: "Lần" }, { nhan: "t (s)" }, { nhan: "|t − t̄| (s)", phu: true }]}
              hang={Array.from({ length: SO_LAN }, (_, i) => {
                const t = i < loat.tMs.length - (chay ? 1 : 0) ? loat.tMs[i] : undefined;
                const hienLech = dangHienLaBangTinh && buocTinh >= 2 && kqTinh;
                return [
                  i + 1,
                  t === undefined ? undefined : vnSo(t / 1000, 3),
                  hienLech ? vnSo(kqTinh.lech[i], 4) : "",
                ];
              })}
            />
            {!bangDay && (
              <p className="mt-1 text-sm text-muted">
                Bấm Ngắt nam châm, đọc số, RESET, thả lần tiếp. Còn {SO_LAN - loat.tMs.length} lần.
              </p>
            )}
          </div>

          {/* Học sinh tự tính bảng 1 (L1, L4). */}
          {bangTinh && kqTinh && !(chay && dangHienLaBangTinh) && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">
                Tự tính từ bảng 1 (s = {vnSo(bangTinh.sCm / 100, 3)} m, Δs = 0,001 m, Δt_dc = {vnSo(DC_T, 3)} s)
              </p>
              <ONhapCham
                nhan={<>1. Thời gian rơi trung bình t̄ =</>}
                donVi="s"
                vidu="0,321"
                cham={(r) => chamTbar(r, bangTinh.tMs, kqTinh)}
                onXong={xongTinh}
              />
              {buocTinh >= 1 && (
                <ONhapCham
                  nhan={<>2. Sai số tuyệt đối Δt = trung bình |t − t̄| + Δt_dc =</>}
                  donVi="s"
                  vidu="0,0022"
                  cham={(r) => chamDt(r, kqTinh)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHsDt(v);
                    xongTinh();
                  }}
                />
              )}
              {buocTinh >= 2 && (
                <ONhapCham
                  nhan={<>3. ḡ = 2s : t̄² =</>}
                  donVi="m/s²"
                  vidu="9,70"
                  cham={(r) => chamG(r, bangTinh.sCm / 100, kqTinh)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHsG(v);
                    xongTinh();
                  }}
                />
              )}
              {buocTinh >= 3 && (
                <ONhapCham
                  nhan={<>4. Δg = (Δs/s + 2Δt/t̄) · ḡ =</>}
                  donVi="m/s²"
                  vidu="0,15"
                  cham={(r) => chamDg(r, bangTinh.sCm / 100, kqTinh, hsDt ?? kqTinh.dt, hsG ?? kqTinh.g)}
                  onXong={xongTinh}
                />
              )}
              {hsXong && (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base">
                  Kết quả bảng 1:{" "}
                  <b>
                    g = {vnSo(kqTinh.g, 2)} ± {vnSo(kqTinh.dg, 2)} m/s²
                  </b>
                  , tức từ {vnSo(kqTinh.g - kqTinh.dg, 2)} đến {vnSo(kqTinh.g + kqTinh.dg, 2)} m/s².
                </p>
              )}
            </div>
          )}

          {/* So các bảng (T7: chiều lệch). */}
          {hsXong && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">So các bảng</p>
              <TrucKetQua ds={lichSuHien} />
              <ul className="space-y-1 text-base tabular-nums">
                {lichSuHien.map((l, i) => (
                  <li key={i}>
                    B{l.so}: s = {vnSo(l.sCm / 100, 3)} m, {l.tuDu ? "có từ dư" : "không từ dư"} → t̄ ={" "}
                    {vnSo(l.kq.tbar, 4)} s, g = {vnSo(l.kq.g, 2)} ± {vnSo(l.kq.dg, 2)} m/s²
                  </li>
                ))}
              </ul>
              {coCaHai ? (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base leading-relaxed">
                  Bảng có từ dư: mọi t lớn hơn chừng {vnSo(TRE_TU_DU_MS / 1000, 3)} s nên ḡ <b>nhỏ hơn</b>, mà Δg vẫn
                  nhỏ như cũ: chụm nhưng lệch. Cách giảm: chỉnh dòng điện nam châm vừa đủ giữ bi; thả thêm nhiều lần
                  không khử được. Thử thêm: s = 1,000 m, có từ dư thì lệch nhiều hay ít hơn?
                </p>
              ) : (
                <p className="text-base text-muted">
                  {tuDu ? "Bỏ" : "Bật"} “từ dư” ({tuDu ? "Không" : "Có"}) rồi thả 5 lần: máy tính sẵn bảng mới để so với
                  bảng 1.
                </p>
              )}
            </div>
          )}

          {hsXong && (
            <div className="mt-4 space-y-3">
              <CauKieuDe de={CAU_DE.de} cac={CAU_DE.cac} />
              <ChuaNoiDuoc
                y={[
                  "Chỉ một bảng ở một độ cao không phát hiện được từ dư: cả 5 số t cùng lớn lên, bảng vẫn chụm đẹp.",
                  "Không cho biết vật nhẹ, sức cản lớn có rơi với cùng g: mô hình đã bỏ qua sức cản không khí.",
                ]}
              />
            </div>
          )}
        </>
      )}
    </section>
  );
}
