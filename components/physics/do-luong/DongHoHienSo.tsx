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

import { useCallback, useEffect, useRef, useState } from "react";
import { ChonCheDo, LuyenDoc, phuBtn, segBtn, useTienDo, type CheDo } from "./chung";
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
};

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
}: BangDongHoHienSoProps) {
  const chuaReset = trangThai === "xong";
  return (
    <div className="rounded-xl border border-line-strong bg-surface-2 p-3">
      <div
        className="flex items-baseline justify-end gap-2 rounded-lg border border-line bg-panel px-3 py-1"
        aria-live="off"
      >
        <span className="font-mono text-4xl font-bold tabular-nums text-ink">
          {(Math.min(ms, 9999) / 1000).toFixed(3)}
        </span>
        <span className="text-base text-muted">s</span>
      </div>
      {noiO && (
        <p className="mt-1 text-sm text-muted">
          {noiO.A && <>ổ A: {noiO.A}</>}
          {noiO.A && noiO.B && " · "}
          {noiO.B && <>ổ B: {noiO.B}</>}
        </p>
      )}
      <div className="mt-2 flex items-center gap-2">
        <span className="shrink-0 text-sm text-muted">MODE</span>
        <div className="flex flex-1 gap-2">
          {cacMode.map((m) => (
            <button
              key={m}
              type="button"
              className={segBtn(m === mode)}
              disabled={trangThai === "chay"}
              onClick={() => onMode(m)}
            >
              {m}
            </button>
          ))}
        </div>
      </div>
      <div className="mt-2 flex gap-2">
        <button type="button" className={`${phuBtn} flex-1`} disabled={trangThai === "chay"} onClick={onReset}>
          RESET
        </button>
        <button
          type="button"
          className="min-h-11 flex-1 rounded-lg bg-primary px-3 text-sm font-semibold text-white disabled:opacity-40"
          disabled={trangThai !== "cho"}
          onClick={onTha}
        >
          {chuaReset ? "RESET trước" : nhanTha}
        </button>
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
  const P0 = { x: 30, y: 48 };
  const P1 = { x: 344, y: 112 };
  const Lpx = Math.hypot(P1.x - P0.x, P1.y - P0.y);
  const ux = (P1.x - P0.x) / Lpx;
  const uy = (P1.y - P0.y) / Lpx;
  const Ltot = X_E + ts.s + 0.12;
  const k = Lpx / Ltot;
  const t = tMs / 1000;
  const pos = Math.min(Ltot - D_BI / 2, (ts.a * t * t) / 2);
  const r = Math.max(5, (D_BI / 2) * k);
  const nx = uy; // pháp tuyến hướng lên khỏi máng
  const ny = -ux;
  const diem = (m: number, h = 0) => ({ x: P0.x + ux * m * k + nx * -h, y: P0.y + uy * m * k + ny * -h });
  const bi = diem(pos, -r);
  const chan = (o: "A" | "B") => lan.some((l) => l.o === o && tMs > l.vao && tMs < l.ra);
  const cong = (m: number, ten: string, o: "A" | "B") => {
    const g0 = diem(m, -r);
    const tren = diem(m, -2 * r - 22);
    const duoi = diem(m, 10);
    const on = chan(o);
    return (
      <g key={ten}>
        <line x1={duoi.x} y1={duoi.y} x2={tren.x} y2={tren.y} stroke="currentColor" strokeWidth={4} />
        <circle cx={g0.x} cy={g0.y} r={4} fill={on ? "var(--color-danger)" : "var(--color-ok)"} />
        <text x={tren.x} y={tren.y - 6} textAnchor="middle" fontSize={16} fontWeight={700} fill="currentColor">
          {ten}
        </text>
      </g>
    );
  };
  return (
    <svg
      viewBox="0 0 360 134"
      className="block w-full select-none text-ink"
      role="img"
      aria-label="Máng nghiêng, viên bi, hai cổng quang E và F"
    >
      <line x1={P0.x} y1={P0.y} x2={P1.x} y2={P1.y} stroke="currentColor" strokeWidth={2.5} />
      <rect
        x={P0.x - 22}
        y={P0.y - 26}
        width={20}
        height={20}
        rx={3}
        fill="var(--color-primary-soft)"
        stroke="var(--color-primary)"
      />
      <text x={P0.x - 12} y={P0.y + 14} textAnchor="middle" fontSize={16} fill="var(--color-muted)">
        NC
      </text>
      {cong(X_E, "E", "A")}
      {cong(X_E + ts.s, "F", "B")}
      <circle cx={bi.x} cy={bi.y} r={r} fill="currentColor" />
      <text
        x={(diem(X_E).x + diem(X_E + ts.s).x) / 2}
        y={(diem(X_E).y + diem(X_E + ts.s).y) / 2 + 22}
        textAnchor="middle"
        fontSize={16}
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
