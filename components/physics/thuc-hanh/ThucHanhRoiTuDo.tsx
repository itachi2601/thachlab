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

import { useId, useMemo, useState, type ReactNode } from "react";
import { PredictGate } from "@/components/physics/PredictGate";
import { BangDongHoHienSo, useDongHoHienSo, type LanChan } from "@/components/physics/do-luong/DongHoHienSo";
import { phuBtn, segBtn, type KetQuaCham } from "@/components/physics/do-luong/chung";
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

/* ---------------- Phần dùng chung (sẽ tách sang BangSoLieu.tsx ở bài mẫu 2) ---------------- */

/** Ô nhập một số + chấm một lần; sai thì hiện cách tính đúng rồi cho đi tiếp. */
function ONhapCham({
  nhan,
  donVi,
  cham,
  onXong,
  vidu,
}: {
  nhan: ReactNode;
  donVi: string;
  cham: (raw: string) => KetQuaCham | null;
  onXong: () => void;
  vidu: string;
}) {
  const [raw, setRaw] = useState("");
  const [kq, setKq] = useState<KetQuaCham | null>(null);
  const [loiNhap, setLoiNhap] = useState(false);
  const id = useId();
  const kiemTra = () => {
    if (kq) return;
    const r = cham(raw);
    if (!r) return setLoiNhap(true);
    setLoiNhap(false);
    setKq(r);
    onXong();
  };
  return (
    <div className="rounded-xl border border-line bg-surface-2 p-3">
      <label className="block text-base text-ink" htmlFor={id}>
        {nhan}
      </label>
      <div className="mt-2 flex gap-2">
        <div className="flex min-w-0 flex-1 items-center rounded-lg border border-line-strong bg-panel pr-3 focus-within:ring-2 focus-within:ring-primary">
          <input
            id={id}
            inputMode="decimal"
            autoComplete="off"
            value={raw}
            disabled={!!kq}
            onChange={(e) => setRaw(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && kiemTra()}
            placeholder={`ví dụ ${vidu}`}
            className="min-h-11 w-full min-w-0 rounded-lg bg-transparent px-3 text-base text-ink outline-none placeholder:text-slate-500"
          />
          <span className="shrink-0 text-base text-muted">{donVi}</span>
        </div>
        {!kq && (
          <button type="button" className="min-h-11 rounded-lg bg-primary px-4 text-sm font-semibold text-white" onClick={kiemTra}>
            Kiểm tra
          </button>
        )}
      </div>
      {loiNhap && <p className="mt-2 text-sm text-warn">Gõ một số, ví dụ {vidu} (dấu phẩy hay dấu chấm đều được).</p>}
      {kq && (
        <p className="mt-2 text-base leading-relaxed text-ink" aria-live="polite">
          <span className={kq.loai === "dung" ? "font-semibold text-ok" : "font-semibold text-danger"}>
            {kq.loai === "dung" ? "✓ Đúng." : "✗ Chưa đúng."}
          </span>{" "}
          {kq.loi}
        </p>
      )}
    </div>
  );
}

/** Câu 4 phương án kiểu đề (T9): chọn một lần, hiện vì sao từng phương án đúng/sai. */
function CauKieuDe({ de, cac }: { de: string; cac: { text: string; dung?: boolean; why: string }[] }) {
  const [chon, setChon] = useState<number | null>(null);
  const L = ["A", "B", "C", "D"];
  return (
    <div className="rounded-xl border border-line-strong bg-panel p-3">
      <p className="text-xs font-semibold uppercase tracking-wide text-primary">Câu hỏi kiểu đề thi</p>
      <div className="exam-paper mt-1">
        <p className="exam-content text-ink">{de}</p>
        <div className="exam-content mt-2 grid gap-2">
          {cac.map((o, i) => {
            const daChon = chon !== null;
            const mau = !daChon
              ? "border-line-strong hover:bg-primary-soft"
              : o.dung
                ? "border-ok"
                : i === chon
                  ? "border-danger"
                  : "border-line opacity-80";
            return (
              <button
                key={i}
                type="button"
                disabled={daChon}
                onClick={() => setChon(i)}
                className={`flex min-h-11 w-full flex-col items-start rounded-lg border bg-panel px-3 py-2 text-left text-ink transition ${mau}`}
              >
                <span>
                  <b>{L[i]}.</b> {o.text}
                </span>
                {daChon && (
                  <span className="mt-1 font-sans text-sm text-muted">
                    <b className={o.dung ? "text-ok" : "text-muted"}>{o.dung ? "✓ Đây là phát biểu sai cần tìm." : "Phát biểu đúng."}</b>{" "}
                    {o.why}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>
      {chon !== null && (
        <p className="mt-2 text-base text-ink" aria-live="polite">
          {cac[chon].dung ? <b className="text-ok">✓ Đúng.</b> : <b className="text-danger">✗ Chưa đúng.</b>} Đáp án{" "}
          {L[cac.findIndex((o) => o.dung)]}.
        </p>
      )}
    </div>
  );
}

/* ---------------- Cảnh: giá đỡ, nam châm, bi, cổng quang, thước ---------------- */

const Y0 = 52; // px: mép dưới bi lúc còn ở nam châm
const K = 200; // px/m
const R = 8; // px, bán kính bi vẽ (không theo tỉ lệ)
const X_BI = 132;

function CanhRoi({ s, tMs, lan, treMs, tuDu, xong }: { s: number; tMs: number; lan: LanChan[]; treMs: number; tuDu: boolean; xong: boolean }) {
  const t = Math.max(0, tMs - treMs) / 1000;
  const yDay = xong ? 282 : Math.min(Y0 + 0.5 * G_THAT * t * t * K, 282); // xong: bi nằm trong hộp hứng
  const yCong = Y0 + s * K;
  const b = lan.find((l) => l.o === "B");
  const chan = !!b && tMs >= b.vao && tMs <= b.ra;
  return (
    <svg viewBox="0 0 360 292" className="block w-full select-none text-ink" role="img" aria-label="Giá đỡ, nam châm điện giữ viên bi, cổng quang cách đáy bi một đoạn s, thước đo">
      {/* giá đỡ */}
      <line x1={40} y1={10} x2={40} y2={284} stroke="currentColor" strokeWidth={4} />
      <line x1={14} y1={284} x2={200} y2={284} stroke="currentColor" strokeWidth={4} />
      <line x1={40} y1={26} x2={112} y2={26} stroke="currentColor" strokeWidth={3} />
      {/* nam châm điện */}
      <rect x={112} y={12} width={40} height={28} rx={4} fill="var(--color-primary-soft)" stroke="var(--color-primary)" strokeWidth={2} />
      <text x={160} y={24} fontSize={16} fill="currentColor">
        Nam châm điện
      </text>
      {tuDu && (
        <text x={160} y={42} fontSize={16} fill="var(--color-warn)">
          còn từ dư
        </text>
      )}
      {/* thước */}
      <line x1={72} y1={Y0} x2={72} y2={Y0 + K} stroke="currentColor" strokeWidth={1.5} />
      {Array.from({ length: 11 }, (_, i) => (
        <line key={i} x1={72} x2={i % 5 === 0 ? 84 : 79} y1={Y0 + i * 0.1 * K} y2={Y0 + i * 0.1 * K} stroke="currentColor" strokeWidth={1.5} />
      ))}
      {[0, 0.5, 1].map((m) => (
        <text key={m} x={66} y={Y0 + m * K + 5} textAnchor="end" fontSize={16} fill="var(--color-muted)">
          {m === 0 ? "0" : vnSo(m, 1)}
        </text>
      ))}
      {/* hộp mềm hứng bi */}
      <rect x={112} y={270} width={40} height={14} rx={2} fill="var(--color-surface-2)" stroke="var(--color-line-strong)" />
      {/* cổng quang */}
      <rect x={100} y={yCong - 9} width={10} height={18} rx={2} fill="currentColor" />
      <rect x={154} y={yCong - 9} width={10} height={18} rx={2} fill="currentColor" />
      <line x1={110} x2={154} y1={yCong} y2={yCong} stroke={chan ? "var(--color-danger)" : "var(--color-ok)"} strokeWidth={2} strokeDasharray="4 3" />
      <text x={170} y={yCong + 5} fontSize={16} fill="currentColor">
        Cổng quang
      </text>
      {/* kích thước s */}
      <line x1={286} x2={286} y1={Y0} y2={yCong} stroke="var(--color-primary)" strokeWidth={1.5} />
      <line x1={278} x2={294} y1={Y0} y2={Y0} stroke="var(--color-primary)" strokeWidth={1.5} />
      <line x1={278} x2={294} y1={yCong} y2={yCong} stroke="var(--color-primary)" strokeWidth={1.5} />
      <line x1={152} x2={278} y1={Y0} y2={Y0} stroke="var(--color-primary)" strokeWidth={1} strokeDasharray="2 3" />
      <text x={282} y={(Y0 + yCong) / 2 + (s < 0.3 ? -22 : 5)} textAnchor="end" fontSize={16} fontWeight={700} fill="var(--color-primary)">
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
  const LO = 9.2;
  const HI = 10.2;
  const x = (g: number) => 24 + ((Math.min(HI, Math.max(LO, g)) - LO) / (HI - LO)) * 312;
  const h = 36 + ds.length * 30;
  return (
    <figure>
      <svg viewBox={`0 0 360 ${h}`} className="block w-full text-ink" role="img" aria-label="Các khoảng g đo được so với 9,8 m/s²">
        <line x1={24} x2={336} y1={h - 20} y2={h - 20} stroke="currentColor" strokeWidth={1.5} />
        {[9.2, 9.6, 9.8, 10.0].map((v) => (
          <g key={v}>
            <line x1={x(v)} x2={x(v)} y1={h - 25} y2={h - 15} stroke="currentColor" />
            <text x={x(v)} y={h - 1} textAnchor="middle" fontSize={16} fill="var(--color-muted)">
              {vnSo(v, 1)}
            </text>
          </g>
        ))}
        <line x1={x(G_THAT)} x2={x(G_THAT)} y1={6} y2={h - 20} stroke="var(--color-ok)" strokeWidth={2} strokeDasharray="4 3" />
        {ds.map((d, i) => {
          const y = 22 + i * 30;
          const mau = d.tuDu ? "var(--color-warn)" : "var(--color-primary)";
          return (
            <g key={i}>
              <line x1={x(d.kq.g - d.kq.dg)} x2={x(d.kq.g + d.kq.dg)} y1={y} y2={y} stroke={mau} strokeWidth={5} strokeLinecap="round" />
              <circle cx={x(d.kq.g)} cy={y} r={5} fill={mau} />
              <text x={Math.min(x(d.kq.g + d.kq.dg) + 6, 326)} y={y + 5} fontSize={16} fill={mau}>
                B{d.so}
              </text>
            </g>
          );
        })}
      </svg>
      <figcaption className="text-sm text-muted">Vạch xanh lá đứt: 9,8 m/s². Mỗi đoạn: ḡ ± Δg của một bảng (cam: có từ dư).</figcaption>
    </figure>
  );
}

/* ---------------- Nội dung câu hỏi ---------------- */

const DU_DOAN = {
  question:
    "Nam châm còn từ dư: ngắt công tắc thì đồng hồ bắt đầu đếm ngay, nhưng bi còn bám lại một chút rồi mới rơi. So với khi không có từ dư (cùng độ cao s), 5 số t đo được sẽ thế nào?",
  options: [
    {
      text: "Cùng lớn hơn, vẫn chụm như cũ.",
      correct: true,
      why: "Lần nào đồng hồ cũng đếm thêm khoảng bi còn bám nam châm, nên cả loạt dịch lên như nhau; độ chụm do nhiễu ngẫu nhiên quyết định.",
    },
    { text: "Cùng nhỏ hơn, vẫn chụm như cũ.", why: "Đồng hồ đếm từ lúc ngắt điện, bi rời muộn thì thời gian đếm dài ra chứ không ngắn đi." },
    { text: "Tản ra nhiều hơn, trung bình không đổi.", why: "Từ dư làm bi rời muộn gần như cùng một khoảng mỗi lần: lệch về một phía, không phải lên xuống ngẫu nhiên." },
    { text: "Không đổi, vì lấy trung bình 5 lần là hết sai số.", why: "Lấy trung bình chỉ giảm phần lên xuống ngẫu nhiên; phần lệch một phía vẫn còn nguyên." },
  ],
};

const CAU_DE = {
  de: "Một nhóm đo g bằng nam châm điện, cổng quang và đồng hồ hiện số (MODE A↔B), thả bi 5 lần từ s = 0,500 m. Nam châm còn từ dư nên bi rời nam châm muộn hơn lúc đồng hồ bắt đầu đếm. Phát biểu nào sau đây sai?",
  cac: [
    { text: "Năm số t lệch nhau vài phần nghìn giây là do sai số ngẫu nhiên.", why: "Các lần lên xuống quanh giá trị trung bình là sai số ngẫu nhiên." },
    { text: "Từ dư làm mọi số t lớn hơn thời gian rơi thật nên ḡ nhỏ hơn g thật.", why: "g = 2s/t²: t lớn hơn thì g tính ra nhỏ hơn." },
    {
      text: "Thả thêm nhiều lần rồi lấy trung bình sẽ khử được sai số do từ dư.",
      dung: true,
      why: "Lần nào bi cũng rời muộn như nhau nên trung bình bao nhiêu lần vẫn lệch. Cách giảm: chỉnh dòng điện nam châm vừa đủ giữ bi để bi rời ngay khi ngắt.",
    },
    { text: "Kết quả có thể chụm (Δg nhỏ) mà khoảng ḡ ± Δg vẫn không chứa giá trị thật.", why: "Δg tính từ độ phân tán và dụng cụ, không phát hiện được phần lệch một phía (xem bảng có từ dư)." },
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
      setLichSu((ls) => [{ so: bangTinh.so, sCm: bangTinh.sCm, tuDu: bangTinh.tuDu, kq: tinhLoat(bangTinh.tMs, bangTinh.sCm / 100) }, ...ls]);
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
    <section className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5" aria-label="Thí nghiệm ảo đo gia tốc rơi tự do">
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
                <button type="button" className={segBtn(!tuDu)} disabled={khoaDieuKien} onClick={() => tuDu && doiDieuKien(sCm, false)}>
                  Không
                </button>
                <button type="button" className={segBtn(tuDu)} disabled={khoaDieuKien} onClick={() => !tuDu && doiDieuKien(sCm, true)}>
                  Có
                </button>
              </div>
            </div>
            {dangChoTinh && <p className="text-sm text-muted">Tính xong bảng 1 rồi mới đổi điều kiện.</p>}
          </div>

          <div className="mt-3">
            <CanhRoi s={s} tMs={may.tMs} lan={lan} treMs={treMs} tuDu={tuDu} xong={may.trangThai === "xong"} />
            <p className="text-sm text-muted">Bi rơi chiếu chậm {CHIEU_CHAM} lần. Coi giá thẳng đứng, tia sáng ngang mép dưới bi.</p>
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
              Bảng {loat.so} · s = {vnSo(loat.sCm / 100, 3)} m ·{" "}
              {loat.tuDu ? "có từ dư" : "không từ dư"}
            </p>
            <table className="mt-1 w-full border-collapse text-base tabular-nums">
              <thead>
                <tr className="text-left text-sm text-muted">
                  <th className="border-b border-line py-1 pr-2 font-medium">Lần</th>
                  <th className="border-b border-line py-1 pr-2 font-medium">t (s)</th>
                  <th className="border-b border-line py-1 font-medium">|t − t̄| (s)</th>
                </tr>
              </thead>
              <tbody>
                {Array.from({ length: SO_LAN }, (_, i) => {
                  const t = i < loat.tMs.length - (chay ? 1 : 0) ? loat.tMs[i] : undefined;
                  const hienLech = dangHienLaBangTinh && buocTinh >= 2 && kqTinh;
                  return (
                    <tr key={i}>
                      <td className="border-b border-line py-1.5 pr-2">{i + 1}</td>
                      <td className="border-b border-line py-1.5 pr-2 font-mono">{t === undefined ? "—" : vnSo(t / 1000, 3)}</td>
                      <td className="border-b border-line py-1.5 font-mono text-muted">{hienLech ? vnSo(kqTinh.lech[i], 4) : ""}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {!bangDay && <p className="mt-1 text-sm text-muted">Bấm Ngắt nam châm, đọc số, RESET, thả lần tiếp. Còn {SO_LAN - loat.tMs.length} lần.</p>}
          </div>

          {/* Học sinh tự tính bảng 1 (L1, L4). */}
          {bangTinh && kqTinh && !(chay && dangHienLaBangTinh) && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">Tự tính từ bảng 1 (s = {vnSo(bangTinh.sCm / 100, 3)} m, Δs = 0,001 m, Δt_dc = {vnSo(DC_T, 3)} s)</p>
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
                  onXong={xongTinh}
                />
              )}
              {buocTinh >= 2 && (
                <ONhapCham nhan={<>3. ḡ = 2s : t̄² =</>} donVi="m/s²" vidu="9,70" cham={(r) => chamG(r, bangTinh.sCm / 100, kqTinh)} onXong={xongTinh} />
              )}
              {buocTinh >= 3 && (
                <ONhapCham
                  nhan={<>4. Δg = (Δs/s + 2Δt/t̄) · ḡ =</>}
                  donVi="m/s²"
                  vidu="0,15"
                  cham={(r) => chamDg(r, bangTinh.sCm / 100, kqTinh)}
                  onXong={xongTinh}
                />
              )}
              {hsXong && (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base">
                  Kết quả bảng 1: <b>g = {vnSo(kqTinh.g, 2)} ± {vnSo(kqTinh.dg, 2)} m/s²</b>, tức từ {vnSo(kqTinh.g - kqTinh.dg, 2)} đến{" "}
                  {vnSo(kqTinh.g + kqTinh.dg, 2)} m/s².
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
                    B{l.so}: s = {vnSo(l.sCm / 100, 3)} m, {l.tuDu ? "có từ dư" : "không từ dư"} → t̄ = {vnSo(l.kq.tbar, 4)} s, g = {vnSo(l.kq.g, 2)} ±{" "}
                    {vnSo(l.kq.dg, 2)} m/s²
                  </li>
                ))}
              </ul>
              {coCaHai ? (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base leading-relaxed">
                  Bảng có từ dư: mọi t lớn hơn chừng {vnSo(TRE_TU_DU_MS / 1000, 3)} s nên ḡ <b>nhỏ hơn</b>, mà Δg vẫn nhỏ như cũ: chụm nhưng lệch. Cách
                  giảm: chỉnh dòng điện nam châm vừa đủ giữ bi; thả thêm nhiều lần không khử được.
                </p>
              ) : (
                <p className="text-base text-muted">
                  {tuDu ? "Bỏ" : "Bật"} “từ dư” ({tuDu ? "Không" : "Có"}) rồi thả 5 lần: máy tính sẵn bảng mới để so với bảng 1.
                </p>
              )}
            </div>
          )}

          {hsXong && (
            <div className="mt-4 space-y-3">
              <CauKieuDe de={CAU_DE.de} cac={CAU_DE.cac} />
              <details className="rounded-xl border border-line bg-surface-2 p-3">
                <summary className="min-h-11 cursor-pointer py-2 text-base font-semibold">Thí nghiệm này chưa nói được gì? Nghĩ một câu rồi mở.</summary>
                <ul className="mt-1 list-disc space-y-1 pl-5 text-base leading-relaxed">
                  <li>Chỉ một bảng ở một độ cao không phát hiện được từ dư: cả 5 số t cùng lớn lên, bảng vẫn chụm đẹp.</li>
                  <li>Không cho biết vật nhẹ, sức cản lớn có rơi với cùng g: mô hình đã bỏ qua sức cản không khí.</li>
                </ul>
              </details>
            </div>
          )}
        </>
      )}
    </section>
  );
}
