"use client";

/**
 * components/physics/do-luong/DongHoHienSo.tsx — đồng hồ đo thời gian hiện số + cổng quang điện (Gói A,
 * docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3). Gắn vào L10 Bài 6 (lesson 51) qua MoPhongPortals khoá "dong-ho-hien-so".
 * Tự dựng, không lấy gì từ trang khác.
 *
 * Phần dùng lại ở Gói C (thí nghiệm ảo rơi tự do, va chạm trên đệm khí) — không dính bài nào:
 *   - `useDongHoHienSo(lan, { cham })`: chạy đồng hồ theo danh sách lần chắn cổng (cham.ts `LanChan`, ms), trả thời điểm mô phỏng
 *     `tMs` để cảnh tự vẽ vật, `trangThai`, `tha()`, `reset()`, `soChi(mode)`.
 *   - `<BangDongHoHienSo>`: mặt đồng hồ (màn 0,001 s, núm MODE, RESET, nút thả); không biết gì về cảnh.
 *   - `<DongThoiGianChan>`: trục thời gian tô các lần chắn và khoảng MODE đang đếm.
 * Mặc định (default export) là bài 6: bi lăn trên máng nghiêng qua cổng E (ổ A), F (ổ B).
 * Quy tắc UI: N2 (MODE 4 nút một hàng), N6, B4 (bi chỉ lăn khi bấm Thả), D2, C1/H4, M1/M7, M4, L1–L4.
 */

import { useCallback, useEffect, useId, useRef, useState, type ReactNode } from "react";
import { ChonCheDo, LuyenDoc, useTienDo, type CheDo } from "./chung";
import { TEN_MODE, chamDongHoHienSo, ghiGiay, lanChanBiLan, soChiDongHo, type LanChan, type ModeDem } from "./cham";

export type { LanChan, ModeDem } from "./cham";
export const CAC_MODE: ModeDem[] = ["A", "B", "A+B", "A↔B"];

/* ---------------- Hook chạy đồng hồ (dùng lại ở Gói C) ---------------- */

export type TrangThaiDongHo = "cho" | "chay" | "xong";

/**
 * Chạy thời gian mô phỏng cho một lần thả. `lan`: các lần vật chắn tia (ms tính từ lúc thả).
 * `cham`: hệ số chiếu chậm (2 = chậm gấp đôi). `keoThem`: ms chạy thêm sau lần chắn cuối (để vật đi hết cảnh).
 */
export function useDongHoHienSo(lan: LanChan[], opts: { cham?: number; keoThem?: number } = {}) {
  const { cham = 1, keoThem = 300 } = opts;
  const [tMs, setTMs] = useState(0);
  const [trangThai, setTrangThai] = useState<TrangThaiDongHo>("cho");
  const raf = useRef<number | null>(null);
  const ketThuc = lan.reduce((m, l) => Math.max(m, l.ra), 0) + keoThem;

  const dung = () => {
    if (raf.current !== null) cancelAnimationFrame(raf.current);
    raf.current = null;
  };
  useEffect(() => dung, []);

  const tha = useCallback(() => {
    if (trangThai !== "cho") return;
    dung();
    setTrangThai("chay");
    const t0 = performance.now();
    const buoc = (now: number) => {
      const t = (now - t0) / cham;
      if (t >= ketThuc) {
        setTMs(ketThuc);
        setTrangThai("xong");
        raf.current = null;
        return;
      }
      setTMs(t);
      raf.current = requestAnimationFrame(buoc);
    };
    raf.current = requestAnimationFrame(buoc);
  }, [trangThai, cham, ketThuc]);

  const reset = useCallback(() => {
    dung();
    setTMs(0);
    setTrangThai("cho");
  }, []);

  const soChi = useCallback(
    (mode: ModeDem) => (trangThai === "cho" ? 0 : soChiDongHo(mode, lan, tMs)),
    [trangThai, lan, tMs],
  );

  return { tMs, trangThai, tha, reset, soChi };
}

/* ---------------- Mặt đồng hồ (dùng lại ở Gói C) ---------------- */

/*
 * Màu thiết bị CỐ ĐỊNH (không theo sáng/tối — đây là "ảnh" máy thật, M5), như ThuocKep.tsx:
 * vỏ kim loại sơn ghi, màn LED đỏ 7 đoạn trên kính tối, núm MODE nhựa đen, ổ cắm A/B.
 */
const MUC = "#1b2026";
const VIEN = "#7b8590";
const LED = "#ff3b2f";
const LED_TAT = "#2e0e0c";
const XANH = "#1d4ed8";
const XAM_CHU = "#3f4852";
/** Chữ MODE đang chọn trên vỏ: đậm hơn nét để ≥ 4,5:1 trên nền sơn ghi. */
const XANH_CHU = "#1e40af";

function MauMay({ id }: { id: string }) {
  return (
    <defs>
      <linearGradient id={`${id}-kinh`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#2a0c0a" />
        <stop offset="0.5" stopColor="#170605" />
        <stop offset="1" stopColor="#220907" />
      </linearGradient>
      <linearGradient id={`${id}-vien`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#3a4048" />
        <stop offset="1" stopColor="#15191d" />
      </linearGradient>
      <radialGradient id={`${id}-num`} cx="0.38" cy="0.32" r="0.75">
        <stop offset="0" stopColor="#5a6169" />
        <stop offset="0.55" stopColor="#23282d" />
        <stop offset="1" stopColor="#0e1114" />
      </radialGradient>
      <radialGradient id={`${id}-o`} cx="0.4" cy="0.35" r="0.7">
        <stop offset="0" stopColor="#f2f4f6" />
        <stop offset="0.6" stopColor="#b9c0c7" />
        <stop offset="1" stopColor="#7b8590" />
      </radialGradient>
      <filter id={`${id}-sang`} x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="1.6" result="b" />
        <feMerge>
          <feMergeNode in="b" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
  );
}

/** Đoạn sáng của từng chữ số 7 đoạn (a b c d e f g). */
const DOAN: Record<string, string> = {
  "0": "abcdef",
  "1": "bc",
  "2": "abged",
  "3": "abgcd",
  "4": "fgbc",
  "5": "afgcd",
  "6": "afgedc",
  "7": "abc",
  "8": "abcdefg",
  "9": "abcdfg",
};

function ChuSo7Doan({ x, y, so, id }: { x: number; y: number; so: string; id: string }) {
  const w = 30;
  const h = 52;
  const t = 6.5;
  const g = 1.2;
  const xL = x + t / 2;
  const xR = x + w - t / 2;
  const yT = y + t / 2;
  const yM = y + h / 2;
  const yB = y + h - t / 2;
  const ngang = (x1: number, x2: number, yc: number) =>
    `${x1},${yc} ${x1 + t / 2},${yc - t / 2} ${x2 - t / 2},${yc - t / 2} ${x2},${yc} ${x2 - t / 2},${yc + t / 2} ${x1 + t / 2},${yc + t / 2}`;
  const doc = (xc: number, y1: number, y2: number) =>
    `${xc},${y1} ${xc + t / 2},${y1 + t / 2} ${xc + t / 2},${y2 - t / 2} ${xc},${y2} ${xc - t / 2},${y2 - t / 2} ${xc - t / 2},${y1 + t / 2}`;
  const hinh: Record<string, string> = {
    a: ngang(xL + g, xR - g, yT),
    g: ngang(xL + g, xR - g, yM),
    d: ngang(xL + g, xR - g, yB),
    f: doc(xL, yT + g, yM - g),
    b: doc(xR, yT + g, yM - g),
    e: doc(xL, yM + g, yB - g),
    c: doc(xR, yM + g, yB - g),
  };
  const sang = DOAN[so] ?? "";
  return (
    <g transform={`translate(${x + w / 2},${y + h / 2}) skewX(-6) translate(${-(x + w / 2)},${-(y + h / 2)})`}>
      {Object.entries(hinh).map(([k, p]) => (sang.includes(k) ? null : <polygon key={k} points={p} fill={LED_TAT} />))}
      <g fill={LED} filter={`url(#${id}-sang)`}>
        {Object.entries(hinh).map(([k, p]) => (sang.includes(k) ? <polygon key={k} points={p} /> : null))}
      </g>
    </g>
  );
}

/** Vị trí núm MODE trên máy thật (T không dùng ở đây). Góc tính từ phương thẳng đứng, chiều kim đồng hồ. */
const NUM_MODE: { m: string; goc: number }[] = [
  { m: "A", goc: -100 },
  { m: "B", goc: -50 },
  { m: "A+B", goc: 0 },
  { m: "A↔B", goc: 50 },
  { m: "T", goc: 100 },
];

function MatMay({
  ms,
  mode,
  cacMode,
  noiO,
}: {
  ms: number;
  mode: ModeDem;
  cacMode: ModeDem[];
  noiO?: { A?: string; B?: string };
}) {
  const id = `dh${useId().replace(/[^a-zA-Z0-9]/g, "")}`;
  const chu = (Math.min(ms, 9999) / 1000).toFixed(3); // "0.000"
  const so = chu.replace(".", "");
  const KX = 292;
  const KY = 60;
  const gocNum = NUM_MODE.find((n) => n.m === mode)?.goc ?? 0;
  const rad = (d: number) => (d * Math.PI) / 180;
  const o = (x: number, y: number, ten: string, noi?: string) => (
    <g>
      <text x={x} y={y - 17} textAnchor="middle" fontSize={15} fontWeight={700} fill={MUC}>
        {ten}
      </text>
      <circle cx={x} cy={y} r={12} fill="#2b3036" stroke={VIEN} strokeWidth={1.5} />
      <circle cx={x} cy={y} r={8.5} fill="#101316" />
      {[0, 72, 144, 216, 288].map((d) => (
        <circle key={d} cx={x + 5 * Math.sin(rad(d))} cy={y - 5 * Math.cos(rad(d))} r={1.3} fill={`url(#${id}-o)`} />
      ))}
      {noi && (
        <text x={x + 18} y={y + 5} fontSize={15} fill={MUC}>
          {noi}
        </text>
      )}
    </g>
  );
  return (
    <svg viewBox="0 0 360 156" className="block w-full select-none" aria-hidden="true">
      <MauMay id={id} />
      {/* ốc bắt vỏ */}
      {[
        [8, 8],
        [352, 8],
        [8, 148],
        [352, 148],
      ].map(([x, y]) => (
        <g key={`${x}-${y}`}>
          <circle cx={x} cy={y} r={3.5} fill={`url(#${id}-o)`} stroke={VIEN} strokeWidth={0.6} />
          <line x1={x - 2.2} x2={x + 2.2} y1={y} y2={y} stroke="#5f6a74" strokeWidth={1} />
        </g>
      ))}
      <text x={18} y={19} fontSize={15} fontWeight={700} fill={MUC} letterSpacing={0.3}>
        ĐỒNG HỒ HIỆN SỐ
      </text>
      {/* màn LED: viền nhựa đen + kính đỏ sẫm */}
      <rect x={14} y={26} width={200} height={76} rx={6} fill={`url(#${id}-vien)`} />
      <rect x={20} y={32} width={188} height={64} rx={3} fill={`url(#${id}-kinh)`} />
      {so.split("").map((c, i) => (
        <ChuSo7Doan key={i} x={32 + i * 38 + (i > 0 ? 10 : 0)} y={38} so={c} id={id} />
      ))}
      <circle cx={68} cy={87} r={3.6} fill={LED} filter={`url(#${id}-sang)`} />
      <text x={190} y={90} fontSize={18} fontWeight={700} fill={LED}>
        s
      </text>
      <rect x={20} y={32} width={188} height={14} rx={3} fill="#ffffff" fillOpacity={0.05} />
      {/* núm MODE */}
      {NUM_MODE.map(({ m, goc }) => {
        const dung = cacMode.includes(m as ModeDem);
        const chon = m === mode;
        const lx = KX + 37 * Math.sin(rad(goc));
        const ly = KY - 37 * Math.cos(rad(goc));
        return (
          <g key={m}>
            <line
              x1={KX + 23 * Math.sin(rad(goc))}
              y1={KY - 23 * Math.cos(rad(goc))}
              x2={KX + 28 * Math.sin(rad(goc))}
              y2={KY - 28 * Math.cos(rad(goc))}
              stroke={chon ? XANH : MUC}
              strokeWidth={chon ? 2.5 : 1.5}
            />
            <text
              x={lx}
              y={ly + 5}
              textAnchor="middle"
              fontSize={15}
              fontWeight={chon ? 700 : 400}
              fill={chon ? XANH_CHU : dung ? MUC : XAM_CHU}
            >
              {m}
            </text>
          </g>
        );
      })}
      <circle cx={KX} cy={KY} r={21} fill="#9aa3ab" />
      <circle cx={KX} cy={KY} r={19} fill={`url(#${id}-num)`} />
      <line
        x1={KX + 4 * Math.sin(rad(gocNum))}
        y1={KY - 4 * Math.cos(rad(gocNum))}
        x2={KX + 17 * Math.sin(rad(gocNum))}
        y2={KY - 17 * Math.cos(rad(gocNum))}
        stroke="#ffffff"
        strokeWidth={3}
        strokeLinecap="round"
      />
      <text x={KX} y={104} textAnchor="middle" fontSize={15} fontWeight={700} fill={MUC}>
        MODE
      </text>
      {/* ổ cắm A, B (giắc 5 chân) */}
      {o(30, 132, "A", noiO?.A)}
      {o(206, 132, "B", noiO?.B)}
      {/* đèn nguồn */}
      <circle cx={334} cy={126} r={3.2} fill="#22c55e" filter={`url(#${id}-sang)`} />
      <text x={334} y={146} textAnchor="middle" fontSize={15} fill={MUC}>
        ON
      </text>
    </svg>
  );
}

export type BangDongHoHienSoProps = {
  mode: ModeDem;
  /** Đổi MODE. Nên gọi kèm reset() — đồng hồ thật đổi MODE thì phải đếm lại. */
  onMode: (m: ModeDem) => void;
  /** Số chỉ hiện tại (ms). */
  ms: number;
  trangThai: TrangThaiDongHo;
  onReset: () => void;
  onTha: () => void;
  /** Chữ trên nút thả, ví dụ "Thả bi", "Ngắt nam châm". */
  nhanTha?: string;
  /** MODE được phép chọn (mặc định cả 4). */
  cacMode?: ModeDem[];
  /** Cổng nào nối ổ nào, hiện dưới màn: { A: "cổng E", B: "cổng F" }. */
  noiO?: { A?: string; B?: string };
  /** Khoá nút thả (Gói C: bảng đã đủ lần đo, chờ học sinh tính). */
  khoaTha?: boolean;
};

const PHIM =
  "min-h-11 rounded-lg px-2 text-sm font-semibold transition active:scale-[0.98] disabled:opacity-40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1d4ed8]";

export function BangDongHoHienSo({
  mode,
  onMode,
  ms,
  trangThai,
  onReset,
  onTha,
  nhanTha = "Thả",
  cacMode = CAC_MODE,
  noiO,
  khoaTha = false,
}: BangDongHoHienSoProps) {
  const chuaReset = trangThai === "xong";
  return (
    <div
      className="overflow-hidden rounded-xl border"
      style={{
        borderColor: "#6b737b",
        background: "linear-gradient(180deg, #e4e7e2 0%, #d3d7d1 55%, #c3c8c2 100%)",
        boxShadow: "inset 0 1px 0 #ffffff99, 0 1px 2px #0003",
      }}
    >
      <MatMay ms={ms} mode={mode} cacMode={cacMode} noiO={noiO} />
      <span className="sr-only" aria-live="off">
        Đồng hồ chỉ {(Math.min(ms, 9999) / 1000).toFixed(3)} giây, MODE {mode}
        {noiO?.A ? `, ổ A nối ${noiO.A}` : ""}
        {noiO?.B ? `, ổ B nối ${noiO.B}` : ""}
      </span>
      <div className="px-3 pb-3">
        <div className="flex items-center gap-2">
          <span className="shrink-0 text-sm font-semibold" style={{ color: MUC }}>
            MODE
          </span>
          <div className="flex flex-1 gap-2">
            {cacMode.map((m) => {
              const chon = m === mode;
              return (
                <button
                  key={m}
                  type="button"
                  aria-pressed={chon}
                  className={`${PHIM} flex-1 border`}
                  style={
                    chon
                      ? { background: XANH, borderColor: "#1e3a8a", color: "#ffffff" }
                      : { background: "#f6f7f4", borderColor: "#6b737b", color: MUC }
                  }
                  disabled={trangThai === "chay"}
                  onClick={() => onMode(m)}
                >
                  {m}
                </button>
              );
            })}
          </div>
        </div>
        <div className="mt-2 flex gap-2">
          <button
            type="button"
            className={`${PHIM} flex-1 border`}
            style={{ background: "#b91c1c", borderColor: "#7f1d1d", color: "#ffffff" }}
            disabled={trangThai === "chay"}
            onClick={onReset}
          >
            RESET
          </button>
          <button
            type="button"
            className={`${PHIM} flex-1 border`}
            style={{ background: "#15803d", borderColor: "#14532d", color: "#ffffff" }}
            disabled={trangThai !== "cho" || khoaTha}
            onClick={onTha}
          >
            {chuaReset ? "RESET trước" : nhanTha}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ---------------- Trục thời gian các lần chắn (dùng lại ở Gói C) ---------------- */

export function DongThoiGianChan({
  lan,
  mode,
  tenO,
}: {
  lan: LanChan[];
  mode: ModeDem;
  tenO?: { A: string; B: string };
}) {
  const het = lan.reduce((m, l) => Math.max(m, l.ra), 0) * 1.08 || 1;
  const X0 = 52;
  const X1 = 348;
  const x = (ms: number) => X0 + (ms / het) * (X1 - X0);
  const a = lan.find((l) => l.o === "A");
  const b = lan.find((l) => l.o === "B");
  const dem: [number, number][] =
    mode === "A" && a
      ? [[a.vao, a.ra]]
      : mode === "B" && b
        ? [[b.vao, b.ra]]
        : mode === "A+B"
          ? ([a && [a.vao, a.ra], b && [b.vao, b.ra]].filter(Boolean) as [number, number][])
          : a && b
            ? [[a.vao, b.vao]]
            : [];
  const hang = (o: "A" | "B", y: number) => (
    <g key={o}>
      <text x={4} y={y + 6} fontSize={16} fill="currentColor">
        {tenO?.[o] ?? o}
      </text>
      <line x1={X0} x2={X1} y1={y} y2={y} stroke="var(--color-line-strong)" strokeWidth={1} />
      {lan
        .filter((l) => l.o === o)
        .map((l, i) => (
          <rect
            key={i}
            x={x(l.vao)}
            y={y - 7}
            width={Math.max(3, x(l.ra) - x(l.vao))}
            height={14}
            fill="var(--color-warn)"
            rx={2}
          />
        ))}
    </g>
  );
  return (
    <figure>
      <svg
        viewBox="0 0 360 84"
        className="block w-full text-ink"
        role="img"
        aria-label={`MODE ${mode} đếm ${TEN_MODE[mode]}`}
      >
        {hang("A", 18)}
        {hang("B", 46)}
        {dem.map(([u, v], i) => (
          <rect
            key={i}
            x={x(u)}
            y={66}
            width={Math.max(3, x(v) - x(u))}
            height={10}
            fill="var(--color-primary)"
            rx={2}
          />
        ))}
        <text x={4} y={77} fontSize={16} fill="var(--color-primary)">
          đếm
        </text>
      </svg>
      <figcaption className="text-sm text-muted">
        Ô cam: vật đang chắn tia. Vạch xanh: khoảng MODE {mode} đếm.
      </figcaption>
    </figure>
  );
}

/* ---------------- Cảnh bài 6: bi lăn qua hai cổng ---------------- */

const D_BI = 0.02; // m
const X_E = 0.1; // m, từ chỗ thả tới cổng E

type ThongSo = { a: number; s: number };

function CanhMang({ ts, tMs, lan }: { ts: ThongSo; tMs: number; lan: LanChan[] }) {
  const id = `mg${useId().replace(/[^a-zA-Z0-9]/g, "")}`;
  const P0 = { x: 46, y: 58 };
  const P1 = { x: 346, y: 116 };
  const BAN = 150; // mặt bàn
  const DAY = 9; // bề dày máng nhôm
  const Lpx = Math.hypot(P1.x - P0.x, P1.y - P0.y);
  const ux = (P1.x - P0.x) / Lpx;
  const uy = (P1.y - P0.y) / Lpx;
  const goc = (Math.atan2(P1.y - P0.y, P1.x - P0.x) * 180) / Math.PI;
  const Ltot = X_E + ts.s + 0.12;
  const k = Lpx / Ltot;
  const t = tMs / 1000;
  const pos = Math.min(Ltot - D_BI / 2, (ts.a * t * t) / 2);
  const r = Math.max(5, (D_BI / 2) * k);
  // Hệ toạ độ máng: u dọc máng (m → px qua k), v vuông góc, v > 0 là phía dưới mặt máng.
  const diem = (u: number, v = 0) => ({ x: P0.x + ux * u - uy * v, y: P0.y + uy * u + ux * v });
  const chan = (o: "A" | "B") => lan.some((l) => l.o === o && tMs > l.vao && tMs < l.ra);
  const uE = X_E * k;
  const uF = (X_E + ts.s) * k;
  const vTren = -(2 * r + 7); // mép dưới cánh trên cổng quang (đèn phát)
  const vDuoi = DAY + 3; // mép trên cánh dưới (đèn thu)

  // Thước dán trên máng: vạch mỗi cm, số mỗi 10 cm (0 ở mặt nam châm).
  const vach: ReactNode[] = [];
  const so: ReactNode[] = [];
  for (let cm = 0; cm / 100 <= Ltot - 0.005; cm++) {
    const u = (cm / 100) * k;
    const h = cm % 10 === 0 ? 6 : cm % 5 === 0 ? 4.5 : 2.6;
    vach.push(<line key={cm} x1={u} x2={u} y1={DAY - 0.5} y2={DAY - 0.5 - h} />);
    // bỏ số nằm dưới cánh cổng quang hoặc chân đuôi máng
    const vuong = [X_E * k, (X_E + ts.s) * k, Lpx - 10].some((g) => Math.abs(u - g) < 16);
    if (cm % 10 === 0 && cm > 0 && !vuong) {
      const p = diem(u, DAY + 16);
      so.push(
        <text key={`s${cm}`} x={p.x} y={p.y} textAnchor="middle" fontSize={15} fill="currentColor">
          {cm}
        </text>,
      );
    }
  }

  // Cổng quang chữ U (nhựa đen): cánh trên có đèn phát, cánh dưới có đèn thu, thân nối phía sau máng.
  const congSau = (u: number) => (
    <path
      d={`M${u + 6},${vTren - 10} h7 V${vDuoi + 10} h-7 Z`}
      fill={`url(#${id}-nhua)`}
      stroke="#000000"
      strokeWidth={0.6}
    />
  );
  const congTruoc = (u: number, on: boolean) => (
    <g>
      <rect
        x={u - 7}
        y={vTren - 10}
        width={20}
        height={10}
        rx={2}
        fill={`url(#${id}-nhua)`}
        stroke="#000"
        strokeWidth={0.6}
      />
      <rect
        x={u - 7}
        y={vDuoi}
        width={20}
        height={10}
        rx={2}
        fill={`url(#${id}-nhua)`}
        stroke="#000"
        strokeWidth={0.6}
      />
      <rect x={u - 2} y={vTren - 1} width={4} height={2.4} rx={1} fill="#9ca3af" />
      <rect x={u - 2} y={vDuoi - 1.4} width={4} height={2.4} rx={1} fill="#9ca3af" />
      {/* đèn báo trên lưng cổng: sáng đỏ khi vật chắn tia */}
      <circle
        cx={u + 9}
        cy={vTren - 5}
        r={2.6}
        fill={on ? "#ff3b2f" : "#4a1d1a"}
        filter={on ? `url(#${id}-sang)` : undefined}
      />
    </g>
  );
  const tia = (u: number, on: boolean) =>
    on ? null : <line x1={u} x2={u} y1={vTren + 1} y2={0} stroke="#ef4444" strokeWidth={1.2} strokeDasharray="2 2" />;
  const nhanCong = (u: number, ten: string, o: "A" | "B") => {
    const p = diem(u + 3, vTren - 16);
    const on = chan(o);
    return (
      <text x={p.x} y={p.y} textAnchor="middle" fontSize={16} fontWeight={700} fill="currentColor">
        {ten}
        {on && (
          <tspan fontSize={15} fontWeight={400} fill="var(--color-danger)">
            {" "}
            chắn
          </tspan>
        )}
      </text>
    );
  };
  const day = (u: number, o: "A" | "B") => {
    const p = diem(u + 10, vDuoi + 10);
    const xd = p.x + 8;
    return (
      <g>
        <path
          d={`M${p.x},${p.y} C${p.x},${p.y + 14} ${xd},${BAN - 18} ${xd},${BAN + 4}`}
          fill="none"
          stroke="currentColor"
          strokeOpacity={0.45}
          strokeWidth={3.6}
          strokeLinecap="round"
        />
        <path
          d={`M${p.x},${p.y} C${p.x},${p.y + 14} ${xd},${BAN - 18} ${xd},${BAN + 4}`}
          fill="none"
          stroke="#1f2328"
          strokeWidth={2}
          strokeLinecap="round"
        />
        <text x={xd} y={BAN + 20} textAnchor="middle" fontSize={15} fill="currentColor">
          → ổ {o}
        </text>
      </g>
    );
  };
  const bi = diem(pos * k, -r);
  const giaDinh = diem(-8, DAY);
  const chanDuoi = diem(Lpx - 10, DAY);
  const mE = diem(uE, DAY + 30);
  const mF = diem(uF, DAY + 30);

  return (
    <svg
      viewBox="0 0 360 176"
      className="block w-full select-none text-ink"
      role="img"
      aria-label="Máng nghiêng nhôm có thước, nam châm điện giữ viên bi thép ở đầu máng, hai cổng quang E và F nối ổ A và ổ B"
    >
      <defs>
        <linearGradient id={`${id}-nhom`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#f4f6f8" />
          <stop offset="0.35" stopColor="#d5dbe0" />
          <stop offset="0.7" stopColor="#b4bcc4" />
          <stop offset="1" stopColor="#dfe4e8" />
        </linearGradient>
        <linearGradient id={`${id}-nhua`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#4a5058" />
          <stop offset="0.5" stopColor="#24292e" />
          <stop offset="1" stopColor="#111417" />
        </linearGradient>
        <linearGradient id={`${id}-dong`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#f0b37a" />
          <stop offset="0.5" stopColor="#b86b2c" />
          <stop offset="1" stopColor="#e39a5c" />
        </linearGradient>
        <pattern id={`${id}-cuon`} width="2.6" height="20" patternUnits="userSpaceOnUse">
          <rect width="2.6" height="20" fill={`url(#${id}-dong)`} />
          <rect width="0.7" height="20" fill="#7a3f12" fillOpacity={0.6} />
        </pattern>
        <linearGradient id={`${id}-thep`} x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#6b737b" />
          <stop offset="0.5" stopColor="#c9d0d6" />
          <stop offset="1" stopColor="#6b737b" />
        </linearGradient>
        <radialGradient id={`${id}-bi`} cx="0.35" cy="0.3" r="0.75">
          <stop offset="0" stopColor="#ffffff" />
          <stop offset="0.25" stopColor="#d7dde2" />
          <stop offset="0.7" stopColor="#6e7780" />
          <stop offset="1" stopColor="#2c3238" />
        </radialGradient>
        <filter id={`${id}-sang`} x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur stdDeviation="1.4" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* mặt bàn */}
      <line x1={0} x2={360} y1={BAN} y2={BAN} stroke="currentColor" strokeOpacity={0.5} strokeWidth={1.5} />
      {/* giá đỡ đầu máng: đế + trụ thép + khớp kẹp */}
      <rect x={giaDinh.x - 16} y={BAN - 6} width={32} height={6} rx={1.5} fill="#2b3036" />
      <rect
        x={giaDinh.x - 2.5}
        y={giaDinh.y - 2}
        width={5}
        height={BAN - 6 - giaDinh.y + 2}
        fill={`url(#${id}-thep)`}
      />
      <rect x={giaDinh.x - 6} y={giaDinh.y - 4} width={12} height={9} rx={1.5} fill="#2b3036" />
      {/* chân đuôi máng */}
      <path
        d={`M${chanDuoi.x - 5},${chanDuoi.y} L${chanDuoi.x + 5},${chanDuoi.y + 2} L${chanDuoi.x + 5},${BAN} L${chanDuoi.x - 5},${BAN} Z`}
        fill="#2b3036"
      />

      <g transform={`translate(${P0.x},${P0.y}) rotate(${goc})`}>
        {congSau(uE)}
        {congSau(uF)}
        {/* máng nhôm + thước dán */}
        <rect
          x={-12}
          y={0}
          width={Lpx + 10}
          height={DAY}
          fill={`url(#${id}-nhom)`}
          stroke="#7b8590"
          strokeWidth={0.8}
        />
        <line x1={-12} x2={Lpx - 2} y1={0.8} y2={0.8} stroke="#ffffff" strokeWidth={0.8} />
        <g stroke="#1b2026" strokeWidth={0.8}>
          {vach}
        </g>
        {/* nam châm điện: cuộn dây đồng quanh lõi thép, mặt lõi chạm bi */}
        <rect
          x={-r - 30}
          y={-r - 9}
          width={26}
          height={18}
          rx={2}
          fill={`url(#${id}-cuon)`}
          stroke="#7a3f12"
          strokeWidth={0.6}
        />
        <rect
          x={-r - 5}
          y={-r - 5}
          width={5}
          height={10}
          fill={`url(#${id}-thep)`}
          stroke="#4b5560"
          strokeWidth={0.5}
        />
        <rect x={-r - 34} y={-r - 6} width={5} height={12} rx={1} fill="#2b3036" />
        {tia(uE, chan("A"))}
        {tia(uF, chan("B"))}
      </g>
      {/* viên bi thép bóng */}
      <circle cx={bi.x} cy={bi.y} r={r} fill={`url(#${id}-bi)`} stroke="#2c3238" strokeWidth={0.5} />
      <g transform={`translate(${P0.x},${P0.y}) rotate(${goc})`}>
        {congTruoc(uE, chan("A"))}
        {congTruoc(uF, chan("B"))}
      </g>
      {day(uE, "A")}
      {day(uF, "B")}
      {so}
      {nhanCong(uE, "E", "A")}
      {nhanCong(uF, "F", "B")}
      <text x={6} y={16} fontSize={15} fill="currentColor">
        nam châm điện
      </text>
      <path
        d={`M${P0.x - 14},20 L${diem(-r - 18, -r - 10).x},${diem(-r - 18, -r - 10).y - 2}`}
        stroke="currentColor"
        strokeWidth={1}
        strokeOpacity={0.7}
      />
      {/* khoảng EF */}
      <g stroke="var(--color-primary)" strokeWidth={1.2}>
        <line x1={mE.x} y1={mE.y} x2={mF.x} y2={mF.y} />
        <line x1={mE.x - uy * 5} y1={mE.y - ux * 5} x2={mE.x + uy * 5} y2={mE.y + ux * 5} />
        <line x1={mF.x - uy * 5} y1={mF.y - ux * 5} x2={mF.x + uy * 5} y2={mF.y + ux * 5} />
      </g>
      <text
        x={(mE.x + mF.x) / 2}
        y={(mE.y + mF.y) / 2 + 18}
        textAnchor="middle"
        fontSize={16}
        fontWeight={600}
        fill="currentColor"
      >
        EF = {ts.s.toFixed(3).replace(".", ",")} m
      </text>
    </svg>
  );
}

const CAU: { can: ModeDem; de: string }[] = [
  { can: "A↔B", de: "Đo thời gian bi đi từ cổng E tới cổng F." },
  { can: "B", de: "Đo thời gian bi chắn cổng F (để tính tốc độ tức thời tại F)." },
  { can: "A", de: "Đo thời gian bi chắn cổng E (để tính tốc độ tức thời tại E)." },
  { can: "A+B", de: "Đo tổng thời gian bi chắn cổng E và chắn cổng F." },
];

function thongSoNgauNhien(): ThongSo {
  return { a: Math.round((0.8 + Math.random() * 0.8) * 100) / 100, s: (6 + Math.floor(Math.random() * 7)) * 0.05 };
}

export default function DongHoHienSo() {
  const [cheDo, setCheDo] = useState<CheDo>("xem");
  const [ts, setTs] = useState<ThongSo>({ a: 1.2, s: 0.5 });
  const [mode, setMode] = useState<ModeDem>("A↔B");
  const [modeLucTha, setModeLucTha] = useState<ModeDem>("A↔B");
  const [iCau, setICau] = useState(0);
  const [luot, setLuot] = useState(0);
  const [daCham, setDaCham] = useState(false);
  const { tienDo, ghi } = useTienDo("thachlab:do-luong:dong-ho-hien-so:v1");

  const lan = lanChanBiLan(ts.a, D_BI, X_E, ts.s);
  const may = useDongHoHienSo(lan);
  const xem = cheDo === "xem";
  const cau = CAU[iCau];

  const doiMode = (m: ModeDem) => {
    setMode(m);
    may.reset();
  };
  const tha = () => {
    setModeLucTha(mode);
    may.tha();
  };
  const cauMoi = () => {
    setTs(thongSoNgauNhien());
    setICau((i) => (i + 1 + Math.floor(Math.random() * (CAU.length - 1))) % CAU.length);
    setLuot((l) => l + 1);
    setDaCham(false);
    may.reset();
  };
  const doiCheDo = (v: CheDo) => {
    setCheDo(v);
    may.reset();
    if (v === "luyen") cauMoi();
    else setTs({ a: 1.2, s: 0.5 });
  };

  return (
    <section
      className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5"
      aria-label="Đồng hồ đo thời gian hiện số"
    >
      <h2 className="font-display text-lg font-semibold">Đồng hồ hiện số và cổng quang: chọn MODE</h2>
      <div className="mt-3">
        <ChonCheDo value={cheDo} onChange={doiCheDo} />
      </div>
      {!xem && <p className="mt-3 rounded-xl border border-line bg-surface-2 p-3 text-base font-medium">{cau.de}</p>}

      <div className="mt-3">
        <CanhMang ts={ts} tMs={may.tMs} lan={lan} />
      </div>
      <div className="mt-2">
        <BangDongHoHienSo
          mode={mode}
          onMode={doiMode}
          ms={may.soChi(mode)}
          trangThai={may.trangThai}
          onReset={may.reset}
          onTha={tha}
          nhanTha="Thả bi"
          noiO={{ A: "cổng E", B: "cổng F" }}
        />
      </div>

      {xem ? (
        <div className="mt-3 space-y-2 text-base leading-relaxed">
          <p className="rounded-lg bg-surface-2 px-3 py-2">
            <b>MODE {mode}</b> đếm {TEN_MODE[mode]}.
          </p>
          {may.trangThai === "xong" && modeLucTha === mode && (
            <>
              <DongThoiGianChan lan={lan} mode={mode} tenO={{ A: "E", B: "F" }} />
              <p>
                Màn hiện <b>{(soChiDongHo(mode, lan) / 1000).toFixed(3)}</b>, ghi{" "}
                <b>t = {ghiGiay(soChiDongHo(mode, lan))} s</b> (máy ghi dấu chấm, mình ghi dấu phẩy).
              </p>
            </>
          )}
          <p className="text-sm text-muted">
            Chọn một MODE, bấm Thả bi, rồi RESET và thử MODE khác: cùng một lần lăn mà bốn MODE cho bốn số khác nhau.
            Đổi MODE thì đồng hồ về 0, phải thả lại.
          </p>
        </div>
      ) : (
        <div className="mt-3 space-y-2">
          {daCham && <DongThoiGianChan lan={lan} mode={cau.can} tenO={{ A: "E", B: "F" }} />}
          <LuyenDoc
            cauKey={`hs-${luot}`}
            donVi="s"
            nhan={<>Đồng hồ chỉ bao nhiêu giây?</>}
            cham={(raw) => chamDongHoHienSo(raw, cau.can, may.trangThai === "cho" ? mode : modeLucTha, lan)}
            onDaCham={(kq) => {
              setDaCham(true);
              ghi("mode", kq.loai === "dung");
            }}
            onCauMoi={cauMoi}
            tienDo={tienDo["mode"]}
            tenNhiemVu="chọn MODE và đọc đồng hồ"
          />
        </div>
      )}
    </section>
  );
}
