"use client";

/**
 * components/physics/thuc-hanh/ThucHanhTocDo.tsx — thí nghiệm ảo "Đo tốc độ của vật chuyển động" theo bộ thiết bị SGK
 * (L10 Bài 6, lesson 51; Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Tự dựng, không lấy gì từ trang khác.
 * Cảnh máng nghiêng `CanhMang` + mặt đồng hồ `BangDongHoHienSo` của Gói A; bảng/ô chấm `BangSoLieu` dùng chung.
 *
 * Trình tự: Dự đoán (PredictGate, T2) → chỉnh EF (≤ 3 điều khiển, N2) → thả 3 lần qua hai cổng (MODE A↔B), số tự vào bảng (T8)
 * → học sinh tự tính t̄, Δt, v̄, Δv, được chấm (L1, L4) → chuyển một cổng F (MODE B), đo d/t với tia ngang tâm rồi lệch tâm
 * để thấy CHIỀU lệch (T7) → một câu kiểu đề (T9) → "Chưa nói được gì" (T5) + "Bỏ qua…" (T6).
 * UI: B4 (bi đứng yên tới khi bấm), H2 (bảng 3 cột xếp dọc ở 375 px), C1/H4 (chữ trong hình 16 px), D2 (đích chạm 44 px),
 * D6 (inputmode decimal), M1/M7 (token màu), M4 (✓/✗ kèm chữ), L3 (không điểm, không rank). Không gọi Supabase, không lưu gì.
 */

import { useMemo, useState } from "react";
import { PredictGate } from "@/components/physics/PredictGate";
import { BangDongHoHienSo, CanhMang, useDongHoHienSo } from "@/components/physics/do-luong/DongHoHienSo";
import { phuBtn, segBtn } from "@/components/physics/do-luong/chung";
import { BangSoLieu, CauKieuDe, ChuaNoiDuoc, ONhapCham, TrucKhoang } from "./BangSoLieu";
import {
  A_MANG,
  DC_T,
  DELTA_D,
  DELTA_S,
  D_BI,
  LECH_MM,
  S_CM,
  chamDt,
  chamDv,
  chamTbar,
  chamV,
  chamVF,
  dayCung,
  lanChan,
  nhieuNgauNhien,
  soChiLan,
  tinhLoat,
  vTaiF,
  vnSo,
  type KetQuaLoat,
} from "./cham-toc-do";

const SO_LAN = 3;

/* ---------------- Nhìn gần cổng F: tia đi ngang tâm hay lệch ---------------- */

function NhinGanCong({ lech }: { lech: boolean }) {
  const R = 40; // px ↔ 10 mm
  const cx = 110;
  const cy = 60;
  const h = lech ? (LECH_MM / 10) * R : 0;
  const nua = Math.sqrt(R * R - h * h);
  return (
    <svg viewBox="0 0 360 124" className="block w-full text-ink" role="img" aria-label="Nhìn gần viên bi chắn tia sáng">
      <circle cx={cx} cy={cy} r={R} fill="var(--color-surface-2)" stroke="currentColor" strokeWidth={2} />
      <circle cx={cx} cy={cy} r={2.5} fill="currentColor" />
      <line
        x1={20}
        x2={200}
        y1={cy + h}
        y2={cy + h}
        stroke="var(--color-danger)"
        strokeWidth={1.5}
        strokeDasharray="4 3"
      />
      <line
        x1={cx - nua}
        x2={cx + nua}
        y1={cy + h}
        y2={cy + h}
        stroke={lech ? "var(--color-warn)" : "var(--color-primary)"}
        strokeWidth={4}
      />
      <text x={214} y={36} fontSize={16} fill="currentColor">
        d = 20,0 mm
      </text>
      <text x={214} y={60} fontSize={16} fill={lech ? "var(--color-warn)" : "var(--color-primary)"}>
        đoạn chắn {vnSo(dayCung(lech ? LECH_MM : 0) * 1000, 0)} mm
      </text>
      <text x={214} y={84} fontSize={16} fill="var(--color-muted)">
        {lech ? `tia lệch ${LECH_MM} mm` : "tia ngang tâm bi"}
      </text>
      <text x={20} y={118} fontSize={15} fill="var(--color-muted)">
        Nhìn gần cổng F (phóng to)
      </text>
    </svg>
  );
}

/* ---------------- Số liệu ---------------- */

type LoatMot = { so: number; lech: boolean; tMs: number[] };
type TomTat = { so: number; nhan: string; lech: boolean; kq: KetQuaLoat };

const DU_DOAN = {
  question:
    "Cổng F bị chỉnh lệch: tia sáng đi thấp hơn tâm viên bi 6 mm. Đo thời gian chắn tia (MODE B) rồi tính d/t với d = 20,0 mm. So với tốc độ thật của bi tại F, ba kết quả sẽ thế nào?",
  options: [
    {
      text: "Cùng lớn hơn tốc độ thật.",
      correct: true,
      why: "Tia lệch tâm chỉ cắt một dây cung ngắn hơn d, nên bi chắn tia trong thời gian ngắn hơn; lấy d chia thời gian ngắn hơn thì ra số lớn hơn, lần nào cũng vậy.",
    },
    {
      text: "Cùng nhỏ hơn tốc độ thật.",
      why: "Đoạn bi thật sự chắn tia ngắn hơn d, thời gian chắn ngắn đi chứ không dài ra; d/t vì thế lớn lên.",
    },
    {
      text: "Lúc lớn lúc nhỏ, trung bình vẫn đúng.",
      why: "Tia lệch thì lần nào dây cung cũng ngắn như nhau: lệch về một phía, lấy trung bình không khử được.",
    },
    {
      text: "Không đổi, vì bi vẫn lăn như cũ.",
      why: "Bi lăn như cũ nhưng đồng hồ chỉ đếm lúc tia bị che; tia lệch tâm thì bị che ngắn hơn.",
    },
  ],
};

const CAU_DE = {
  de: "Một nhóm đo tốc độ viên bi đường kính d = 20,0 mm lăn nhanh dần trên máng nghiêng, dùng hai cổng quang E, F và đồng hồ hiện số. Phát biểu nào sau đây sai?",
  cac: [
    {
      text: "Ở MODE A↔B, s/t là tốc độ trung bình của bi trên đoạn EF.",
      why: "MODE A↔B đếm từ lúc bi chắn E tới lúc chắn F, nên s/t là tốc độ trung bình trên EF.",
    },
    {
      text: "Đo d/t ở MODE B tại cổng F được số lớn hơn s/t trên EF.",
      why: "Bi nhanh dần nên lúc qua F nó nhanh hơn trung bình trên cả đoạn EF.",
    },
    {
      text: "Tia sáng của cổng F đi thấp hơn tâm bi thì d/t nhỏ hơn tốc độ thật của bi tại F.",
      dung: true,
      why: "Ngược lại: tia lệch tâm cắt dây cung ngắn hơn d, thời gian chắn ngắn hơn nên d/t LỚN hơn tốc độ thật.",
    },
    {
      text: "Sai số tỉ đối của d/t lớn hơn của s/t vì thời gian chắn tia chỉ dài vài chục độ chia của đồng hồ.",
      why: "Chắn tia chỉ cỡ 0,024 s: riêng 1 độ chia 0,001 s đã hơn 4 %, còn t trên EF cỡ 0,8 s.",
    },
  ],
};

function TrucKetQua({ ds, vF }: { ds: TomTat[]; vF: number }) {
  return (
    <TrucKhoang
      lo={0.3}
      hi={1.4}
      vach={[0.4, 0.6, 0.8, 1.0, 1.2, 1.4]}
      moc={vF}
      ds={ds.map((d) => ({ nhan: d.nhan, giua: d.kq.v, ban: d.kq.dv, phu: d.lech }))}
      ghiVach={(v) => vnSo(v, 1)}
      aria="Các khoảng tốc độ đo được so với tốc độ thật của bi tại F"
      chuThich={`Vạch xanh lá đứt: tốc độ thật tại F, ${vnSo(vF, 3)} m/s. Mỗi đoạn: v̄ ± Δv của một bảng (cam: tia lệch tâm).`}
    />
  );
}

/* ---------------- Thành phần chính ---------------- */

export default function ThucHanhTocDo() {
  const [duDoan, setDuDoan] = useState<number | null>(null);
  const [sCm, setSCm] = useState(S_CM.macDinh);
  const [motCong, setMotCong] = useState(false);
  const [lech, setLech] = useState(false);
  const [nhieu, setNhieu] = useState(() => nhieuNgauNhien());
  /** Bảng 1 (hai cổng) — học sinh tự tính. */
  const [bang1, setBang1] = useState<number[]>([]);
  const [buocTinh, setBuocTinh] = useState(0);
  const [hsDt, setHsDt] = useState<number | null>(null);
  const [hsV, setHsV] = useState<number | null>(null);
  /** Các bảng một cổng (số thứ tự từ 2). */
  const [loatMot, setLoatMot] = useState<LoatMot>({ so: 2, lech: false, tMs: [] });
  const [lichSuMot, setLichSuMot] = useState<LoatMot[]>([]);
  const [daTinhVF, setDaTinhVF] = useState(false);

  const s = sCm / 100;
  const lan = useMemo(() => lanChan(s, motCong, lech ? LECH_MM : 0, nhieu), [s, motCong, lech, nhieu]);
  const tSau = soChiLan(lan, motCong);
  const may = useDongHoHienSo(lan, { keoThem: 300 });
  const chay = may.trangThai === "chay";

  const bang1Day = bang1.length === SO_LAN;
  const hsXong = buocTinh >= 4;
  const dangChoTinh = bang1Day && !hsXong;
  const vF = vTaiF(s);

  const tha = () => {
    if (may.trangThai !== "cho" || dangChoTinh) return;
    if (!motCong) {
      if (bang1Day) return;
      setBang1((b) => [...b, tSau]);
    } else {
      const bangMoi = loatMot.tMs.length >= SO_LAN;
      const moi: LoatMot = {
        so: bangMoi ? loatMot.so + 1 : loatMot.so,
        lech,
        tMs: bangMoi ? [tSau] : [...loatMot.tMs, tSau],
      };
      setLoatMot(moi);
      if (moi.tMs.length === SO_LAN)
        setLichSuMot((ls) => (ls.length < 4 ? [...ls, moi] : [ls[0], ...ls.slice(-2), moi])); // giữ bảng một cổng đầu (ô v = d : t̄)
    }
    may.tha();
  };
  const reset = () => {
    may.reset();
    setNhieu(nhieuNgauNhien());
  };
  const doiS = (moi: number) => {
    setSCm(moi);
    setBang1([]);
    reset();
  };
  const doiCong = (mot: boolean, lechMoi: boolean) => {
    setMotCong(mot);
    setLech(lechMoi);
    if (mot) setLoatMot((cu) => ({ so: cu.tMs.length === SO_LAN ? cu.so + 1 : cu.so, lech: lechMoi, tMs: [] }));
    reset();
  };

  const kq1 = bang1Day ? tinhLoat(bang1, s, DELTA_S) : null;
  const tomTat: TomTat[] = [];
  if (hsXong && kq1) tomTat.push({ so: 1, nhan: "B1", lech: false, kq: kq1 });
  // Bảng vừa đủ 3 lần: chờ bi qua cổng xong rồi mới hiện kết quả của nó.
  const lichSuHien = chay && motCong && loatMot.tMs.length === SO_LAN ? lichSuMot.slice(0, -1) : lichSuMot;
  for (const l of lichSuHien)
    tomTat.push({ so: l.so, nhan: `B${l.so}`, lech: l.lech, kq: tinhLoat(l.tMs, D_BI, DELTA_D) });
  const motDauTien = lichSuHien[0];
  const kqMotDau = motDauTien ? tinhLoat(motDauTien.tMs, D_BI, DELTA_D) : null;
  const coCaHai = lichSuHien.some((l) => l.lech) && lichSuHien.some((l) => !l.lech);

  const tMsHien = motCong ? loatMot.tMs : bang1;
  const dangHienBang1 = !motCong;

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Thí nghiệm ảo đo tốc độ viên bi"
    >
      <h2 className="font-display text-lg font-semibold">Thí nghiệm ảo: đo tốc độ viên bi</h2>
      <p className="mt-1 text-base text-muted">
        Nhiệm vụ: thả bi 3 lần qua hai cổng, tự tính v = v̄ ± Δv. Rồi dùng một cổng F, đo d/t khi tia ngang tâm và khi
        tia lệch tâm.
      </p>

      <div className="mt-3">
        <PredictGate
          question={DU_DOAN.question}
          options={DU_DOAN.options}
          choice={duDoan}
          onChoose={setDuDoan}
          hint="Kiểm bằng số: làm xong bảng hai cổng, chuyển sang Một cổng F, đo một bảng tia ngang tâm, một bảng tia lệch."
        />
      </div>

      {duDoan !== null && (
        <>
          {/* Điều khiển (N2): EF, phương án, tia sáng. */}
          <div className="mt-3 space-y-2">
            <div className="flex items-center gap-2">
              <span className="w-24 shrink-0 text-sm text-muted">Khoảng EF</span>
              <button
                type="button"
                className={phuBtn}
                aria-label="Giảm khoảng cách hai cổng"
                disabled={chay || bang1Day || motCong || sCm <= S_CM.min}
                onClick={() => doiS(sCm - S_CM.buoc)}
              >
                −
              </button>
              <span className="min-w-0 flex-1 text-center font-mono text-lg tabular-nums">s = {vnSo(s, 3)} m</span>
              <button
                type="button"
                className={phuBtn}
                aria-label="Tăng khoảng cách hai cổng"
                disabled={chay || bang1Day || motCong || sCm >= S_CM.max}
                onClick={() => doiS(sCm + S_CM.buoc)}
              >
                +
              </button>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-24 shrink-0 text-sm text-muted">Phương án</span>
              <div className="flex flex-1 gap-2">
                <button
                  type="button"
                  className={segBtn(!motCong)}
                  disabled={chay}
                  onClick={() => motCong && doiCong(false, false)}
                >
                  Hai cổng
                </button>
                <button
                  type="button"
                  className={segBtn(motCong)}
                  disabled={chay || !hsXong}
                  onClick={() => !motCong && doiCong(true, false)}
                >
                  Một cổng F
                </button>
              </div>
            </div>
            {motCong && (
              <div className="flex items-center gap-2">
                <span className="w-24 shrink-0 text-sm text-muted">Tia sáng</span>
                <div className="flex flex-1 gap-2">
                  <button
                    type="button"
                    className={segBtn(!lech)}
                    disabled={chay}
                    onClick={() => lech && doiCong(true, false)}
                  >
                    Ngang tâm
                  </button>
                  <button
                    type="button"
                    className={segBtn(lech)}
                    disabled={chay}
                    onClick={() => !lech && doiCong(true, true)}
                  >
                    Lệch {LECH_MM} mm
                  </button>
                </div>
              </div>
            )}
            {!hsXong && bang1Day && <p className="text-sm text-muted">Tính xong bảng 1 rồi mới đổi phương án.</p>}
            {!bang1Day && (
              <p className="text-sm text-muted">Đổi s thì bảng 1 làm lại từ đầu; đủ 3 lần thì s được giữ nguyên.</p>
            )}
          </div>

          <div className="mt-3">
            <CanhMang ts={{ a: A_MANG, s }} tMs={may.tMs} lan={lan} />
            {motCong && <NhinGanCong lech={lech} />}
            <p className="text-sm text-muted">
              Bỏ qua ma sát lăn thay đổi giữa các lần; nam châm điện thả bi từ cùng một chỗ, không có tốc độ đầu.
            </p>
          </div>
          <div className="mt-2">
            <BangDongHoHienSo
              mode={motCong ? "B" : "A↔B"}
              onMode={() => undefined}
              ms={may.soChi(motCong ? "B" : "A↔B")}
              trangThai={may.trangThai}
              onReset={reset}
              onTha={tha}
              nhanTha="Ngắt nam châm"
              cacMode={[motCong ? "B" : "A↔B"]}
              noiO={{ A: "cổng E", B: "cổng F" }}
              khoaTha={dangChoTinh || (!motCong && bang1Day)}
            />
          </div>

          {/* Bảng số liệu, 3 cột xếp dọc (H2). */}
          <div className="mt-3">
            <p className="text-base font-semibold">
              {motCong
                ? `Bảng ${loatMot.so} · một cổng F, MODE B · tia ${loatMot.lech ? `lệch ${LECH_MM} mm` : "ngang tâm"}`
                : `Bảng 1 · hai cổng, MODE A↔B · s = ${vnSo(s, 3)} m`}
            </p>
            <BangSoLieu
              cot={[{ nhan: "Lần" }, { nhan: "t (s)" }, { nhan: "|t − t̄| (s)", phu: true }]}
              hang={Array.from({ length: SO_LAN }, (_, i) => {
                const t = i < tMsHien.length - (chay ? 1 : 0) ? tMsHien[i] : undefined;
                const hienLech = dangHienBang1 && buocTinh >= 2 && kq1;
                return [i + 1, t === undefined ? undefined : vnSo(t / 1000, 3), hienLech ? vnSo(kq1.lech[i], 4) : ""];
              })}
            />
            {tMsHien.length < SO_LAN && (
              <p className="mt-1 text-sm text-muted">
                Bấm Ngắt nam châm, đọc số, RESET, thả lần tiếp. Còn {SO_LAN - tMsHien.length} lần.
              </p>
            )}
          </div>

          {/* Học sinh tự tính bảng 1 (L1, L4). */}
          {kq1 && !(chay && !motCong) && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">
                Tự tính từ bảng 1 (s = {vnSo(s, 3)} m, Δs = 0,0005 m, Δt_dc = {vnSo(DC_T, 3)} s)
              </p>
              <ONhapCham
                nhan={<>1. Thời gian trung bình t̄ =</>}
                donVi="s"
                vidu="0,837"
                cham={(r) => chamTbar(r, bang1, kq1)}
                onXong={() => setBuocTinh((b) => Math.max(b, 1))}
              />
              {buocTinh >= 1 && (
                <ONhapCham
                  nhan={<>2. Sai số tuyệt đối Δt = trung bình |t − t̄| + Δt_dc =</>}
                  donVi="s"
                  vidu="0,002"
                  cham={(r) => chamDt(r, kq1)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHsDt(v);
                    setBuocTinh((b) => Math.max(b, 2));
                  }}
                />
              )}
              {buocTinh >= 2 && (
                <ONhapCham
                  nhan={<>3. Tốc độ trung bình v̄ = s : t̄ =</>}
                  donVi="m/s"
                  vidu="0,597"
                  cham={(r) => chamV(r, s, kq1)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHsV(v);
                    setBuocTinh((b) => Math.max(b, 3));
                  }}
                />
              )}
              {buocTinh >= 3 && (
                <ONhapCham
                  nhan={<>4. Δv = (Δs/s + Δt/t̄) · v̄ =</>}
                  donVi="m/s"
                  vidu="0,002"
                  cham={(r) => chamDv(r, s, kq1, hsDt ?? kq1.dt, hsV ?? kq1.v)}
                  onXong={() => setBuocTinh((b) => Math.max(b, 4))}
                />
              )}
              {hsXong && (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base">
                  Kết quả bảng 1:{" "}
                  <b>
                    v = {vnSo(kq1.v, 3)} ± {vnSo(kq1.dv, 3)} m/s
                  </b>
                  : tốc độ trung bình trên EF. Giờ bấm <b>Một cổng F</b> để đo tốc độ lúc bi qua F.
                </p>
              )}
            </div>
          )}

          {/* Bảng một cổng đầu tiên: học sinh tính d/t (L1). */}
          {hsXong && motDauTien && kqMotDau && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">
                Tự tính từ bảng {motDauTien.so} (t̄ ≈ {vnSo(kqMotDau.tbar, 4)} s, d = 20,0 mm)
              </p>
              <ONhapCham
                key={motDauTien.so}
                nhan={<>Tốc độ khi bi qua F: v = d : t̄ =</>}
                donVi="m/s"
                vidu="0,83"
                cham={(r) => chamVF(r, kqMotDau)}
                onXong={() => setDaTinhVF(true)}
              />
            </div>
          )}

          {/* So các bảng (T7: chiều lệch). */}
          {hsXong && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">So các bảng</p>
              <TrucKetQua ds={tomTat} vF={vF} />
              <ul className="space-y-1 text-base tabular-nums">
                {tomTat.map((l) => (
                  <li key={l.so}>
                    {l.nhan}: {l.so === 1 ? "hai cổng, s/t̄" : `một cổng, d/t̄, tia ${l.lech ? "lệch tâm" : "ngang tâm"}`}{" "}
                    → v = {vnSo(l.kq.v, 3)} ± {vnSo(l.kq.dv, 3)} m/s
                  </li>
                ))}
              </ul>
              {coCaHai && daTinhVF ? (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base leading-relaxed">
                  B1 nằm bên trái vạch vì là tốc độ <b>trung bình</b> trên EF: bi nhanh dần, tới F mới nhanh nhất. Bảng
                  tia lệch tâm: mọi lần chắn ngắn hơn, d/t <b>lớn hơn</b> tốc độ thật, lần nào cũng thế: chụm nhưng
                  lệch. Cách sửa: chỉnh cổng cho tia đi ngang tâm bi; thả thêm nhiều lần không khử được.
                </p>
              ) : (
                <p className="text-base text-muted">
                  {lichSuHien.length === 0
                    ? "Bấm Một cổng F, thả 3 lần với tia ngang tâm."
                    : !daTinhVF
                      ? "Tính v = d : t̄ ở ô trên trước."
                      : `Đổi tia sang ${lichSuHien.some((l) => l.lech) ? "Ngang tâm" : `Lệch ${LECH_MM} mm`} rồi thả 3 lần: máy tính sẵn bảng mới để so.`}
                </p>
              )}
            </div>
          )}

          {hsXong && (
            <div className="mt-4 space-y-3">
              <CauKieuDe de={CAU_DE.de} cac={CAU_DE.cac} />
              <ChuaNoiDuoc
                y={[
                  "Hai cổng chỉ cho tốc độ trung bình trên EF: không biết bi nhanh dần đều hay không, cũng không biết tốc độ tại F.",
                  "Một bảng đo với tia lệch tâm vẫn chụm đẹp: chỉ nhìn bảng số không phát hiện được cổng chỉnh lệch.",
                ]}
              />
            </div>
          )}
        </>
      )}
    </section>
  );
}
