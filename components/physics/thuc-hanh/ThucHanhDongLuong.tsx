"use client";

/**
 * components/physics/thuc-hanh/ThucHanhDongLuong.tsx — thí nghiệm ảo "Xác định động lượng của vật trước và sau va chạm"
 * theo bộ thiết bị SGK (L10 Bài 30, lesson 75; Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Tự dựng.
 * Băng đệm khí, xe 1 đẩy vào xe 2 đứng yên, dính nhau (va chạm mềm). Hai đồng hồ hiện số MODE A: đồng hồ 1 nối cổng 1
 * (đo t1), đồng hồ 2 nối cổng 2 (đo t1'); mỗi đồng hồ chỉ giữ lần chắn ĐẦU (lần cản quang xe 1 qua cổng 2 sau đó không tính).
 *
 * Trình tự: Dự đoán (PredictGate, T2) → chọn m1, m2, bật/tắt ma sát (3 điều khiển, N2) → đẩy 3 lần, số tự vào bảng (T8)
 * → học sinh tự tính p, p', δ, ε của lần 1 và kết luận, được chấm (L1, L4) → đo bảng thứ hai để thấy CHIỀU lệch của ma sát
 * (T7) → một câu kiểu đề (T9) → "Chưa nói được gì" (T5) + "Bỏ qua…" (T6).
 * UI: B4 (xe đứng yên tới khi bấm Đẩy), H2 (hai bảng ≤ 5 cột chồng dọc ở 375 px), C1/H4 (chữ trong hình 16 px),
 * D2 (đích chạm 44 px), M1/M7 (token màu), M4 (✓/✗ kèm chữ), L3 (không điểm, không rank). Không gọi Supabase.
 */

import { useMemo, useState } from "react";
import { PredictGate } from "@/components/physics/PredictGate";
import { useDongHoHienSo, type LanChan } from "@/components/physics/do-luong/DongHoHienSo";
import { phuBtn, segBtn } from "@/components/physics/do-luong/chung";
import { BangSoLieu, CauKieuDe, ChuaNoiDuoc, ONhapCham, TrucKhoang } from "./BangSoLieu";
import {
  M1_CHON,
  M2_CHON,
  MAT,
  S_CAN,
  chamDelta,
  chamEps,
  chamP,
  chamPp,
  lanDayNgauNhien,
  soChi,
  tinhHang,
  vSau,
  vnSo,
  type Hang,
} from "./cham-dong-luong";

const SO_LAN = 3;
const SO_O = 5; // p, p', δ, ε, kết luận

/* ---------------- Cảnh: băng đệm khí, hai xe, hai cổng ---------------- */

const X0 = 20; // px: đầu trái băng
const K = 320; // px/m (băng 1,00 m)
const L_XE = 0.1; // m
const DAU1 = 0.12; // m: mũi xe 1 lúc đầu
const DUOI2 = 0.52; // m: đuôi xe 2 (đứng yên) = chỗ va chạm
const CONG1 = 0.3;
const CONG2 = 0.8;
const CUOI = 0.97; // m: mũi xe 2 dừng ở đệm cuối băng
/** Tấm cản quang trên xe: từ (mũi − 0,075) đến (mũi − 0,025), rộng S_CAN. Chắn cổng x khi mũi ∈ [x + 0,025; x + 0,075]. */
const MUI_CHAN = 0.025;

type Lan = { v1: number; vp: number; t1Ms: number; t1pMs: number };

/** Thời điểm (ms) các mốc của một lần đẩy, theo tốc độ thật; độ dài chắn lấy đúng số chỉ đồng hồ. */
function mocLan(l: Lan) {
  const vao1 = ((CONG1 + MUI_CHAN - DAU1) / l.v1) * 1000;
  const vaCham = ((DUOI2 - DAU1) / l.v1) * 1000;
  const vao2 = vaCham + ((CONG2 + MUI_CHAN - (DUOI2 + L_XE)) / l.vp) * 1000;
  return { vao1, vaCham, vao2 };
}

function CanhBang({
  l,
  tMs,
  lan,
  coMaSat,
  daChay,
}: {
  l: Lan;
  tMs: number;
  lan: LanChan[];
  coMaSat: boolean;
  daChay: boolean;
}) {
  const { vaCham } = mocLan(l);
  const t = daChay ? tMs : 0;
  const mui1 = t < vaCham ? DAU1 + (l.v1 * t) / 1000 : DUOI2 + (l.vp * (t - vaCham)) / 1000;
  const mui2 = t < vaCham ? DUOI2 + L_XE : Math.min(CUOI, DUOI2 + L_XE + (l.vp * (t - vaCham)) / 1000);
  const mui1Ve = Math.min(mui1, mui2 - L_XE);
  const chan = (o: "A" | "B") => {
    const c = lan.find((x) => x.o === o);
    return daChay && !!c && tMs >= c.vao && tMs <= c.ra;
  };
  const px = (m: number) => X0 + m * K;
  const YB = 112; // mặt băng
  const xe = (mui: number, nhan: string, key: string) => (
    <g key={key}>
      <rect
        x={px(mui - L_XE)}
        y={YB - 20}
        width={L_XE * K}
        height={18}
        rx={3}
        fill="var(--color-surface-2)"
        stroke="currentColor"
        strokeWidth={2}
      />
      {/* tấm cản quang */}
      <rect x={px(mui - 0.075)} y={YB - 40} width={S_CAN * K} height={20} fill="currentColor" />
      <text x={px(mui - L_XE / 2)} y={YB + 26} textAnchor="middle" fontSize={16} fill="currentColor">
        {nhan}
      </text>
    </g>
  );
  const cong = (x: number, nhan: string, on: boolean) => (
    <g>
      <rect x={px(x) - 3} y={YB - 64} width={6} height={20} fill="currentColor" />
      <line
        x1={px(x)}
        x2={px(x)}
        y1={YB - 44}
        y2={YB - 22}
        stroke={on ? "var(--color-danger)" : "var(--color-ok)"}
        strokeWidth={2}
        strokeDasharray="4 3"
      />
      <text x={px(x)} y={YB - 70} textAnchor="middle" fontSize={16} fill="currentColor">
        {nhan}
      </text>
    </g>
  );
  return (
    <svg
      viewBox="0 0 360 150"
      className="block w-full select-none text-ink"
      role="img"
      aria-label="Băng đệm khí nằm ngang, xe 1 bên trái, xe 2 đứng yên giữa hai cổng quang"
    >
      {/* băng + lỗ khí */}
      <rect
        x={X0}
        y={YB}
        width={K}
        height={10}
        rx={2}
        fill="var(--color-surface-2)"
        stroke="currentColor"
        strokeWidth={1.5}
      />
      {Array.from({ length: 16 }, (_, i) => (
        <circle key={i} cx={X0 + 10 + i * 20} cy={YB + 5} r={1.5} fill="var(--color-muted)" />
      ))}
      <line x1={px(CUOI) + 4} x2={px(CUOI) + 4} y1={YB - 18} y2={YB} stroke="currentColor" strokeWidth={3} />
      {cong(CONG1, "Cổng 1", chan("A"))}
      {cong(CONG2, "Cổng 2", chan("B"))}
      {xe(mui1Ve, "Xe 1", "x1")}
      {xe(mui2, "Xe 2", "x2")}
      {t >= vaCham && <circle cx={px(mui2 - L_XE)} cy={YB - 11} r={3} fill="var(--color-warn)" />}
      <text x={X0} y={YB + 46} fontSize={16} fill="var(--color-muted)">
        Đệm khí{coMaSat ? ", còn ma sát khí" : " (bỏ qua ma sát)"}
      </text>
    </svg>
  );
}

/* ---------------- Nội dung câu hỏi ---------------- */

const DU_DOAN = {
  question:
    "Xe 1 (0,205 kg) qua cổng 1 hết khoảng 0,100 s, đâm vào xe 2 nặng gần gấp đôi (0,398 kg) đang đứng yên rồi dính nhau. Đồng hồ cổng 2 chỉ khoảng bao nhiêu?",
  options: [
    {
      text: "0,050 s",
      why: "Hai xe dính nhau thì nặng hơn xe 1 nên đi chậm hơn: tấm cản quang chắn tia lâu hơn chứ không ngắn đi.",
    },
    { text: "0,100 s", why: "Động lượng chia cho khối lượng lớn hơn gần 3 lần, tốc độ không giữ nguyên được." },
    { text: "0,200 s", why: "Khối lượng sau là 0,205 + 0,398 ≈ 0,603 kg, gần gấp 3 xe 1 chứ không gấp đôi." },
    {
      text: "0,300 s",
      correct: true,
      why: "Động lượng giữ nguyên: v' = m1·v1/(m1 + m2) ≈ v1/2,94, nên thời gian chắn tia gấp khoảng 2,9 lần, cỡ 0,30 s.",
    },
  ],
};

const CAU_DE = {
  de: "Một nhóm làm va chạm mềm trên băng đệm khí ba lần với các khối lượng khác nhau. Cả ba lần đều có p' < p, độ lệch δ lần lượt 2,2 %; 1,9 %; 2,6 %. Phát biểu nào sau đây sai?",
  cac: [
    {
      text: "Ma sát khí và sức cản làm hai xe chậm bớt nên p' đo được nhỏ hơn p.",
      why: "Ngoại lực cản luôn ngược chiều chuyển động nên chỉ làm động lượng giảm.",
    },
    {
      text: "Ba lần lệch cùng một phía là dấu hiệu của sai số hệ thống.",
      why: "Sai số ngẫu nhiên lúc làm p' lớn hơn, lúc làm nhỏ hơn; lệch cùng phía là có nguyên nhân chung.",
    },
    {
      text: "Đo thêm thật nhiều lần rồi lấy trung bình thì p' sẽ bằng p.",
      dung: true,
      why: "Lấy trung bình chỉ giảm phần lên xuống ngẫu nhiên; phần lệch cùng phía do ma sát vẫn còn nguyên (xem bảng có ma sát).",
    },
    {
      text: "Nếu cả ba lần có p' > p thì ma sát không giải thích được; nên kiểm băng có nghiêng xuống về phía cổng 2 không.",
      why: "Ma sát chỉ làm p' nhỏ đi. p' > p cùng phía gợi ý xe được tăng tốc, như băng dốc xuống.",
    },
  ],
};

/* ---------------- Số liệu ---------------- */

type Loat = { so: number; coMaSat: boolean; hang: Hang[] };

const ghiS = (ms: number) => vnSo(ms / 1000, 3);

function MatDongHo({ ten, ms }: { ten: string; ms: number }) {
  return (
    <div className="rounded-xl border border-line-strong bg-surface-2 p-2">
      <p className="text-sm text-muted">{ten}</p>
      <div className="mt-1 flex items-baseline justify-end gap-1 rounded-lg border border-line bg-panel px-2 py-1">
        <span className="font-mono text-3xl font-bold tabular-nums text-ink">
          {(Math.min(ms, 9999) / 1000).toFixed(3)}
        </span>
        <span className="text-base text-muted">s</span>
      </div>
    </div>
  );
}

/* ---------------- Thành phần chính ---------------- */

export default function ThucHanhDongLuong() {
  const [duDoan, setDuDoan] = useState<number | null>(null);
  const [i1, setI1] = useState(0);
  const [i2, setI2] = useState(0);
  const [coMaSat, setCoMaSat] = useState(true);
  const [day, setDay] = useState(() => lanDayNgauNhien());
  const [loat, setLoat] = useState<Loat>({ so: 1, coMaSat: true, hang: [] });
  const [lichSu, setLichSu] = useState<Loat[]>([]);
  /** Bảng học sinh tự tính (bảng đầy đủ đầu tiên) và số ô đã xong (0..5). */
  const [bangTinh, setBangTinh] = useState<Loat | null>(null);
  const [buocTinh, setBuocTinh] = useState(0);
  /** p, p', δ, ε học sinh đã nhập ĐÚNG (chấm ô sau theo số của em). */
  const [hs, setHs] = useState<{ p?: number; pp?: number; d?: number; e?: number }>({});
  const [ketLuan, setKetLuan] = useState<number | null>(null);

  const m1 = M1_CHON[i1];
  const m2 = M2_CHON[i2];
  const doc = soChi(m1, m2, day, coMaSat);
  const lanNay: Lan = useMemo(
    () => ({ v1: day.v1, vp: vSau(m1, m2, day.v1, coMaSat), t1Ms: doc.t1Ms, t1pMs: doc.t1pMs }),
    [day.v1, m1, m2, coMaSat, doc.t1Ms, doc.t1pMs],
  );
  const lan = useMemo<LanChan[]>(() => {
    const m = mocLan(lanNay);
    const a = Math.round(m.vao1);
    const b = Math.round(m.vao2);
    return [
      { o: "A", vao: a, ra: a + lanNay.t1Ms },
      { o: "B", vao: b, ra: b + lanNay.t1pMs },
    ];
  }, [lanNay]);
  // chạy thêm tới khi xe 2 chạm đệm cuối băng
  const keoThem = Math.round(((CUOI - (CONG2 + MUI_CHAN + S_CAN)) / lanNay.vp) * 1000) + 200;
  const may = useDongHoHienSo(lan, { keoThem });

  const hsXong = buocTinh >= SO_O;
  const dangChoTinh = !!bangTinh && !hsXong;
  const chay = may.trangThai === "chay";
  const khoaDieuKien = chay || dangChoTinh;
  const bangDay = loat.hang.length === SO_LAN;

  // Số chỉ đã biết lúc bấm: ghi ngay, nhưng chỉ HIỆN khi xe qua cổng 2 xong (T8).
  const day1 = () => {
    if (may.trangThai !== "cho" || dangChoTinh) return;
    const h: Hang = { m1, m2, ...doc };
    const moi: Loat = bangDay ? { so: loat.so + 1, coMaSat, hang: [h] } : { ...loat, hang: [...loat.hang, h] };
    setLoat(moi);
    if (moi.hang.length === SO_LAN) {
      if (!bangTinh) setBangTinh(moi);
      else setLichSu((ls) => [...ls, moi].slice(-3));
    }
    may.tha();
  };
  const reset = () => {
    may.reset();
    setDay(lanDayNgauNhien());
  };
  const doiMaSat = (co: boolean) => {
    if (co === coMaSat) return;
    setCoMaSat(co);
    setLoat((cu) => ({ so: cu.hang.length ? cu.so + 1 : cu.so, coMaSat: co, hang: [] })); // đổi điều kiện → bảng mới
    reset();
  };
  const xongO = () => {
    const nb = buocTinh + 1;
    setBuocTinh(nb);
    if (nb === SO_O && bangTinh) setLichSu((ls) => [bangTinh, ...ls]);
  };

  const h1 = bangTinh?.hang[0];
  const kq1 = h1 ? tinhHang(h1) : null;
  const dangHienBangTinh = loat.so === 1;
  const soHangHien = loat.hang.length - (chay ? 1 : 0);
  const lichSuHien = chay && bangDay && loat.so !== 1 ? lichSu.slice(0, -1) : lichSu;
  const coCaHai = lichSuHien.some((l) => l.coMaSat) && lichSuHien.some((l) => !l.coMaSat);
  // kết luận lần 1 theo δ, ε của học sinh (nếu đã nhập đúng)
  const dHs = hs.d ?? (kq1 ? kq1.delta * 100 : 0);
  const eHs = hs.e ?? (kq1 ? kq1.eps * 100 : 0);
  const kqHien = (l: Loat) => l.hang.map(tinhHang);
  // Mọi lần của mọi bảng bỏ qua ma sát cùng một phía (ngẫu nhiên vẫn xảy ra với 3 lần): không nói "lúc trên lúc dưới".
  const khongMaSat = lichSuHien.filter((l) => !l.coMaSat).flatMap(kqHien);
  const khongMaSatCungPhia =
    khongMaSat.length > 0 && (khongMaSat.every((k) => k.pp < k.p) || khongMaSat.every((k) => k.pp > k.p));

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Thí nghiệm ảo động lượng trước và sau va chạm"
    >
      <h2 className="font-display text-lg font-semibold">Thí nghiệm ảo: động lượng trước và sau va chạm</h2>
      <p className="mt-1 text-base text-muted">
        Nhiệm vụ: đẩy xe 1 ba lần, tự tính p, p′ và so độ lệch δ với sai số ε. Rồi đổi ma sát, đo thêm một bảng và so.
      </p>

      <div className="mt-3">
        <PredictGate
          question={DU_DOAN.question}
          options={DU_DOAN.options}
          choice={duDoan}
          onChoose={setDuDoan}
          hint="Kiểm bằng số: chọn m1 = 0,205 kg, m2 = 0,398 kg rồi đẩy."
        />
      </div>

      {duDoan !== null && (
        <>
          {/* Điều khiển (N2): m1, m2, ma sát. */}
          <div className="mt-3 space-y-2">
            {(
              [
                ["Xe 1: m1", M1_CHON, i1, setI1],
                ["Xe 2: m2", M2_CHON, i2, setI2],
              ] as const
            ).map(([nhan, chon, i, set]) => (
              <div key={nhan} className="flex items-center gap-2">
                <span className="w-24 shrink-0 text-sm text-muted">{nhan}</span>
                <div className="flex flex-1 gap-2">
                  {chon.map((m, k) => (
                    <button
                      key={k}
                      type="button"
                      className={segBtn(i === k)}
                      disabled={khoaDieuKien}
                      onClick={() => {
                        set(k);
                        if (may.trangThai !== "cho") reset();
                      }}
                    >
                      {vnSo(m, 3)} kg
                    </button>
                  ))}
                </div>
              </div>
            ))}
            <div className="flex items-center gap-2">
              <span className="w-24 shrink-0 text-sm text-muted">Ma sát khí, sức cản</span>
              <div className="flex flex-1 gap-2">
                <button
                  type="button"
                  className={segBtn(!coMaSat)}
                  disabled={khoaDieuKien}
                  onClick={() => doiMaSat(false)}
                >
                  Bỏ qua
                </button>
                <button
                  type="button"
                  className={segBtn(coMaSat)}
                  disabled={khoaDieuKien}
                  onClick={() => doiMaSat(true)}
                >
                  Có
                </button>
              </div>
            </div>
            {dangChoTinh && <p className="text-sm text-muted">Tính xong lần 1 của bảng 1 rồi mới đo tiếp.</p>}
          </div>

          <div className="mt-3">
            <CanhBang l={lanNay} tMs={may.tMs} lan={lan} coMaSat={coMaSat} daChay={may.trangThai !== "cho"} />
            <p className="text-sm text-muted">
              Tấm cản quang trên mỗi xe rộng 5,00 cm. Coi băng nằm ngang, xe 2 đứng yên, hai xe dính hẳn vào nhau.
            </p>
          </div>

          {/* Hai đồng hồ MODE A + RESET + Đẩy. */}
          <div className="mt-2 grid grid-cols-2 gap-2">
            <MatDongHo ten="Đồng hồ 1 · cổng 1 · MODE A" ms={may.soChi("A")} />
            <MatDongHo ten="Đồng hồ 2 · cổng 2 · MODE A" ms={may.soChi("B")} />
          </div>
          <div className="mt-2 flex gap-2">
            <button type="button" className={`${phuBtn} flex-1`} disabled={chay} onClick={reset}>
              RESET
            </button>
            <button
              type="button"
              className="min-h-11 flex-1 rounded-lg bg-primary px-3 text-sm font-semibold text-white disabled:opacity-40"
              disabled={may.trangThai !== "cho" || dangChoTinh}
              onClick={day1}
            >
              {may.trangThai === "xong" ? "RESET trước" : bangDay ? "Đẩy xe 1 (bảng mới)" : "Đẩy xe 1"}
            </button>
          </div>

          {/* Bảng đo (H2: ≤ 5 cột). */}
          <div className="mt-3">
            <BangSoLieu
              tieuDe={
                <>
                  Bảng {loat.so} · {loat.coMaSat ? "có ma sát" : "bỏ qua ma sát"} · s = 0,0500 m
                </>
              }
              cot={[{ nhan: "Lần" }, { nhan: "m1 (kg)" }, { nhan: "m2 (kg)" }, { nhan: "t1 (s)" }, { nhan: "t1′ (s)" }]}
              hang={Array.from({ length: SO_LAN }, (_, i) => {
                const h = i < soHangHien ? loat.hang[i] : undefined;
                return [i + 1, h && vnSo(h.m1, 3), h && vnSo(h.m2, 3), h && ghiS(h.t1Ms), h && ghiS(h.t1pMs)];
              })}
            />
            {!bangDay && (
              <p className="mt-1 text-sm text-muted">
                Đẩy, đọc hai đồng hồ, RESET, đẩy lần tiếp (đổi m1, m2 nếu muốn). Còn {SO_LAN - loat.hang.length} lần.
              </p>
            )}
          </div>

          {/* Học sinh tự tính lần 1 của bảng 1 (L1, L4). */}
          {bangTinh && h1 && kq1 && !(chay && dangHienBangTinh) && (
            <div className="mt-4 space-y-2">
              <p className="text-base font-semibold">
                Tự tính lần 1 của bảng 1 (s = 0,0500 m; Δm = 0,001 kg; Δt = 0,001 s)
              </p>
              <ONhapCham
                nhan={<>1. Động lượng trước va chạm p = m1 · s/t1 =</>}
                donVi="kg·m/s"
                vidu="0,1035"
                cham={(r) => chamP(r, h1, kq1)}
                onXong={(r, v) => {
                  if (r.loai === "dung") setHs((x) => ({ ...x, p: v }));
                  xongO();
                }}
              />
              {buocTinh >= 1 && (
                <ONhapCham
                  nhan={<>2. Động lượng sau va chạm p′ =</>}
                  donVi="kg·m/s"
                  vidu="0,1012"
                  cham={(r) => chamPp(r, h1, kq1)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHs((x) => ({ ...x, pp: v }));
                    xongO();
                  }}
                />
              )}
              {buocTinh >= 2 && (
                <ONhapCham
                  nhan={<>3. Độ lệch δ = |p′ − p| : p =</>}
                  donVi="%"
                  vidu="2,2"
                  cham={(r) => chamDelta(r, kq1, hs.p ?? kq1.p, hs.pp ?? kq1.pp)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHs((x) => ({ ...x, d: Math.abs(v) }));
                    xongO();
                  }}
                />
              )}
              {buocTinh >= 3 && (
                <ONhapCham
                  nhan={<>4. Sai số ε = Δm/m1 + Δt/t1 + 2Δm/(m1 + m2) + Δt/t1′ =</>}
                  donVi="%"
                  vidu="2,5"
                  cham={(r) => chamEps(r, h1, kq1)}
                  onXong={(r, v) => {
                    if (r.loai === "dung") setHs((x) => ({ ...x, e: v }));
                    xongO();
                  }}
                />
              )}
              {buocTinh >= 4 && (
                <div className="rounded-xl border border-line bg-surface-2 p-3">
                  <p className="text-base">
                    5. Lần 1: δ ≈ {vnSo(dHs, 1)} %, ε ≈ {vnSo(eHs, 1)} %. Kết luận?
                  </p>
                  <div className="mt-2 grid gap-2">
                    {[
                      "δ ≤ ε: động lượng bảo toàn trong phạm vi sai số.",
                      "δ > ε: chưa kết luận định luật sai; kiểm lại băng, cổng quang rồi đo lại.",
                    ].map((t, k) => {
                      const dung = dHs <= eHs === (k === 0);
                      const mau =
                        ketLuan === null
                          ? "border-line-strong"
                          : dung
                            ? "border-ok"
                            : ketLuan === k
                              ? "border-danger"
                              : "border-line opacity-80";
                      return (
                        <button
                          key={k}
                          type="button"
                          disabled={ketLuan !== null}
                          onClick={() => {
                            setKetLuan(k);
                            xongO();
                          }}
                          className={`min-h-11 rounded-lg border bg-panel px-3 py-2 text-left text-base text-ink ${mau}`}
                        >
                          {t}
                        </button>
                      );
                    })}
                  </div>
                  {ketLuan !== null && (
                    <p className="mt-2 text-base" aria-live="polite">
                      {dHs <= eHs === (ketLuan === 0) ? (
                        <b className="text-ok">✓ Đúng.</b>
                      ) : (
                        <b className="text-danger">✗ Chưa đúng.</b>
                      )}{" "}
                      {dHs <= eHs
                        ? `${vnSo(dHs, 1)} % ≤ ${vnSo(eHs, 1)} %: độ lệch nằm trong sai số.`
                        : `${vnSo(dHs, 1)} % > ${vnSo(eHs, 1)} %: lệch vượt sai số đo; một lần vượt chưa đủ bác bỏ định luật.`}
                    </p>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Kết quả cả bảng + so các bảng (T7: chiều lệch). */}
          {hsXong && (
            <div className="mt-4 space-y-3">
              {lichSuHien.map((l) => {
                const ds = kqHien(l);
                return (
                  <div key={l.so}>
                    <BangSoLieu
                      tieuDe={
                        <>
                          Bảng {l.so} tính sẵn · {l.coMaSat ? "có ma sát" : "bỏ qua ma sát"}
                        </>
                      }
                      cot={[{ nhan: "Lần" }, { nhan: "p" }, { nhan: "p′" }, { nhan: "δ (%)" }, { nhan: "ε (%)" }]}
                      hang={ds.map((k, i) => [
                        i + 1,
                        vnSo(k.p, 4),
                        vnSo(k.pp, 4),
                        `${vnSo(k.delta * 100, 1)}${k.delta <= k.eps ? "" : " >ε"}`,
                        vnSo(k.eps * 100, 1),
                      ])}
                    />
                    <p className="mt-1 text-sm text-muted">
                      p, p′ tính bằng kg·m/s. p′ &lt; p ở {ds.filter((k) => k.pp < k.p).length}/{ds.length} lần; δ &gt;
                      ε ở {ds.filter((k) => k.delta > k.eps).length}/{ds.length} lần.
                    </p>
                  </div>
                );
              })}
              <TrucKhoang
                lo={0.93}
                hi={1.05}
                vach={[0.94, 0.97, 1, 1.03]}
                moc={1}
                ds={lichSuHien.flatMap((l) =>
                  kqHien(l).map((k, i) => ({ nhan: `${l.so}.${i + 1}`, giua: k.pp / k.p, ban: k.eps, phu: l.coMaSat })),
                )}
                ghiVach={(v) => vnSo(v, 2)}
                aria="Tỉ số p′/p từng lần đo kèm khoảng sai số, so với 1"
                chuThich="Vạch xanh lá đứt: p′/p = 1. Mỗi đoạn: p′/p ± ε của một lần (nhãn bảng.lần; cam: có ma sát). Đoạn chạm vạch 1 thì δ ≤ ε."
              />
              {coCaHai ? (
                <p className="rounded-xl border border-line bg-surface-2 p-3 text-base leading-relaxed">
                  Có ma sát: mỗi lần đều mất chừng {vnSo(MAT * 100, 1)} % động lượng nên p′ <b>nhỏ hơn</b> p, các điểm
                  cam dồn về bên trái vạch 1.{" "}
                  {khongMaSatCungPhia
                    ? "Bảng bỏ qua ma sát lần này cũng lệch cùng một phía: với 3 lần đo, chuyện đó xảy ra ngẫu nhiên khá thường (cỡ 1 trong 4 bảng). Đo thêm một bảng bỏ qua ma sát để xem p′/p có lúc trên lúc dưới 1 không."
                    : "Bỏ qua ma sát: p′/p lúc trên lúc dưới 1, chỉ do đọc đồng hồ."}{" "}
                  Lệch cùng phía ở mọi bảng có ma sát là sai số hệ thống; đo thêm nhiều lần không khử được. Cách giảm:
                  bơm khí đủ mạnh, đặt hai cổng gần chỗ va chạm.
                </p>
              ) : (
                <p className="text-base text-muted">
                  Chọn ma sát “{coMaSat ? "Bỏ qua" : "Có"}” rồi đẩy 3 lần: máy tính sẵn bảng mới để so với bảng 1.
                </p>
              )}
            </div>
          )}

          {hsXong && (
            <div className="mt-4 space-y-3">
              <CauKieuDe de={CAU_DE.de} cac={CAU_DE.cac} />
              <ChuaNoiDuoc
                y={[
                  "δ ≤ ε chỉ cho biết số đo không mâu thuẫn với bảo toàn động lượng trong phạm vi sai số, không chứng minh bảo toàn tuyệt đối.",
                  "Chỉ thử va chạm mềm với xe 2 đứng yên: chưa nói gì về va chạm đàn hồi hay khi cả hai xe cùng chạy.",
                  "Không cho biết động năng: va chạm mềm mất động năng dù động lượng gần như giữ nguyên.",
                ]}
              />
            </div>
          )}
        </>
      )}
    </section>
  );
}
