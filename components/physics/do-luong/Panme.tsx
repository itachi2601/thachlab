"use client";

/**
 * components/physics/do-luong/Panme.tsx — panme (thước vi kế) độ chia 0,01 mm (Gói A, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3).
 * Gắn vào L10 Bài 3 (lesson 48) qua MoPhongPortals khoá "panme". Tự dựng, không lấy gì từ trang khác.
 *
 * Hình phóng to chỗ đọc: ống cố định có thang mm (trên đường ngang) và thang nửa mm (dưới đường ngang), thước tròn 50 vạch,
 * mỗi vạch 0,01 mm (quay một vòng tiến 0,5 mm). Kéo ngang trên hình hoặc bấm ± để xoay thước tròn.
 * Xem cách đọc (N6): bốn bước, bấm bước nào thì phần đó trong hình được tô (M4, H3). Luyện đọc: số ngẫu nhiên có ca biên
 * (thước tròn gần vạch 0 — dễ nhầm có hay chưa có vạch nửa mm), chấm ngay chỉ đúng chỗ sai (L1, L4), 5 lần liên tiếp (L2, L3).
 * Quy tắc UI: N2, D2 (44 px), C1/H4 (chữ trong hình ≥ 13 px ở 360 px), M1/M7, B4.
 */

import { useRef, useState, type ReactNode } from "react";
import { ChonCheDo, LuyenDoc, phuBtn, soNguyenRaChuoi, useTienDo, type CheDo } from "./chung";
import { chamPanme, ghiPanme, ngauNhienPanme, tachPanme } from "./cham";

const MAX_MM = 24;
const W = 360;
const REF = 104; // đường ngang chuẩn trên ống
const XT = 232; // mép thước tròn (cố định trên hình, ống trượt)
const PPM = 26; // px/mm trên ống
const RC = 70; // bán kính thước tròn trong hình (px)
const TRAI = 12;

type Nhin = "mm" | "nua" | "tron" | null;

function kep(zH: number) {
  return Math.max(0, Math.min(MAX_MM * 100 + 99, Math.round(zH)));
}

function HinhPanme({
  zH,
  nhin,
  hienTrung,
  onKeo,
}: {
  zH: number;
  nhin: Nhin | "all";
  hienTrung: boolean;
  onKeo?: (dz: number) => void;
}) {
  const z = zH / 100;
  const { m, nua, k } = tachPanme(zH);
  const ref = useRef<SVGSVGElement>(null);
  const keo = useRef<{ x: number; tong: number } | null>(null);
  const x = (mm: number) => XT - (z - mm) * PPM;
  const to = (key: Exclude<Nhin, null>) => nhin === "all" || nhin === key;

  const vx = (e: { clientX: number }) => {
    const r = ref.current!.getBoundingClientRect();
    return ((e.clientX - r.left) / r.width) * W;
  };

  const ong: ReactNode[] = [];
  const mm0 = Math.max(0, Math.ceil(z - (XT - TRAI) / PPM));
  for (let j = mm0; j <= Math.floor(z + 1e-9); j++) {
    const px = x(j);
    const hl = to("mm") && j === m;
    ong.push(
      <line
        key={j}
        x1={px}
        x2={px}
        y1={REF}
        y2={REF - (j % 5 === 0 ? 22 : 15)}
        stroke={hl ? "var(--color-primary)" : "currentColor"}
        strokeWidth={hl ? 3 : 1.5}
      />,
    );
    if (j % 5 === 0 && px > TRAI + 8)
      ong.push(
        <text key={`t${j}`} x={px} y={REF - 28} textAnchor="middle" fontSize={16} fontWeight={700} fill="currentColor">
          {j}
        </text>,
      );
  }
  for (let j = mm0; j + 0.5 <= z + 1e-9; j++) {
    const px = x(j + 0.5);
    if (px < TRAI) continue;
    const hl = to("nua") && nua === 1 && j === m;
    ong.push(
      <line
        key={`h${j}`}
        x1={px}
        x2={px}
        y1={REF}
        y2={REF + 15}
        stroke={hl ? "var(--color-primary)" : "currentColor"}
        strokeWidth={hl ? 3 : 1.5}
      />,
    );
  }

  const tron: ReactNode[] = [];
  const goc0 = zH % 50; // vạch đang nằm trên đường ngang
  for (let d = -14; d <= 14; d++) {
    const th = (d * 2 * Math.PI) / 50;
    const y = REF - RC * Math.sin(th);
    const i = (((goc0 + d) % 50) + 50) % 50;
    const hl = hienTrung && d === 0;
    tron.push(
      <line
        key={d}
        x1={XT}
        x2={XT + (i % 5 === 0 ? 24 : 14)}
        y1={y}
        y2={y}
        stroke={hl ? "var(--color-ok)" : "currentColor"}
        strokeWidth={hl ? 3 : 1.4}
        opacity={Math.max(0.35, Math.cos(th))}
      />,
    );
    if (i % 5 === 0 && Math.abs(th) < 0.95)
      tron.push(
        <text
          key={`n${d}`}
          x={XT + 30}
          y={y + 5.5}
          fontSize={16}
          fill={hl ? "var(--color-ok)" : "currentColor"}
          fontWeight={hl ? 700 : 400}
        >
          {i}
        </text>,
      );
  }

  return (
    <svg
      ref={ref}
      viewBox={`0 0 ${W} 200`}
      className="block w-full select-none text-ink"
      style={{ touchAction: "pan-y" }}
      role="img"
      aria-label={
        onKeo ? `Panme đang chỉ ${ghiPanme(zH)} mm. Kéo ngang để xoay thước tròn.` : "Panme: chỗ đọc số phóng to."
      }
      onPointerDown={(e) => {
        if (!onKeo) return;
        keo.current = { x: vx(e), tong: 0 };
        ref.current?.setPointerCapture(e.pointerId);
      }}
      onPointerMove={(e) => {
        if (!keo.current || !onKeo) return;
        const nx = vx(e);
        const dz = Math.trunc((nx - keo.current.x) * 2);
        if (dz !== 0) {
          keo.current.x = nx;
          onKeo(dz);
        }
      }}
      onPointerUp={() => (keo.current = null)}
      onPointerCancel={() => (keo.current = null)}
    >
      {/* ống cố định */}
      <rect
        x={TRAI}
        y={REF - 52}
        width={XT - TRAI}
        height={80}
        fill="var(--color-panel)"
        stroke="currentColor"
        strokeWidth={1.2}
      />
      <line x1={TRAI} x2={XT + 4} y1={REF} y2={REF} stroke="currentColor" strokeWidth={1.4} />
      {ong}
      <text x={TRAI + 6} y={REF + 44} fontSize={16} fill="var(--color-muted)">
        nửa mm ↑
      </text>
      {/* thước tròn */}
      <path
        d={`M${XT},${REF - 92} H${W - 10} V${REF + 92} H${XT} Z`}
        fill="var(--color-primary-soft)"
        stroke="var(--color-primary)"
        strokeWidth={1.5}
      />
      <g>{tron}</g>
      {hienTrung && (
        <text x={XT + 58} y={REF + 6} fontSize={16} fontWeight={700} fill="var(--color-ok)">
          ← {k}
        </text>
      )}
      {onKeo && (
        <text x={XT - 8} y={190} textAnchor="end" fontSize={16} fill="var(--color-primary)">
          ⇆ kéo để xoay
        </text>
      )}
    </svg>
  );
}

export default function Panme() {
  const [cheDo, setCheDo] = useState<CheDo>("xem");
  const [zXem, setZXem] = useState(1286);
  const [zLuyen, setZLuyen] = useState(0);
  const [daCham, setDaCham] = useState(false);
  const [nhin, setNhin] = useState<Nhin>(null);
  const { tienDo, ghi } = useTienDo("thachlab:do-luong:panme:v1");

  const xem = cheDo === "xem";
  const zH = xem ? zXem : zLuyen;
  const { m, nua, k } = tachPanme(zH);
  const kStr = soNguyenRaChuoi(k, 2);

  const cauMoi = () => {
    setZLuyen((cu) => ngauNhienPanme(MAX_MM, cu));
    setDaCham(false);
  };
  const doiCheDo = (v: CheDo) => {
    setCheDo(v);
    setNhin(null);
    if (v === "luyen") cauMoi();
  };
  const doi = (dz: number) => setZXem((zz) => kep(zz + dz));

  const buoc: { key: Exclude<Nhin, null>; text: ReactNode }[] = [
    {
      key: "mm",
      text: (
        <>
          <b>Thang mm</b> (trên đường ngang): vạch cuối cùng lộ ra trước mép thước tròn là <b>{m} mm</b>.
        </>
      ),
    },
    {
      key: "nua",
      text: nua ? (
        <>
          <b>Thang nửa mm</b> (dưới đường ngang): sau vạch {m} mm <b>đã lộ ra</b> một vạch nửa mm → cộng <b>0,50 mm</b>.
        </>
      ) : (
        <>
          <b>Thang nửa mm</b> (dưới đường ngang): sau vạch {m} mm <b>chưa lộ ra</b> vạch nửa mm nào → không cộng.
        </>
      ),
    },
    {
      key: "tron",
      text: (
        <>
          <b>Thước tròn:</b> vạch số <b>{k}</b> nằm đúng đường ngang → {k} × 0,01 = {kStr} mm.
        </>
      ),
    },
  ];

  return (
    <section className="rounded-2xl border border-line bg-panel p-3 text-ink sm:p-5" aria-label="Panme">
      <h2 className="font-display text-lg font-semibold">Panme: đọc số tới 0,01 mm</h2>
      <p className="mt-1 text-sm text-muted">
        Thước tròn có 50 vạch; quay một vòng thì tiến 0,5 mm, nên mỗi vạch là 0,01 mm.
      </p>
      <div className="mt-3">
        <ChonCheDo value={cheDo} onChange={doiCheDo} />
      </div>

      <div className="mt-3">
        <HinhPanme
          zH={zH}
          nhin={xem ? nhin : daCham ? "all" : null}
          hienTrung={xem ? nhin === "tron" || nhin === null : daCham}
          onKeo={xem ? doi : undefined}
        />
      </div>

      {xem ? (
        <div className="mt-2 space-y-2">
          <div className="flex gap-2">
            <button type="button" className={`${phuBtn} flex-1 px-1`} onClick={() => doi(-50)}>
              −0,5
            </button>
            <button type="button" className={`${phuBtn} flex-1 px-1`} onClick={() => doi(-1)}>
              −0,01
            </button>
            <button type="button" className={`${phuBtn} flex-1 px-1`} onClick={() => doi(1)}>
              +0,01
            </button>
            <button type="button" className={`${phuBtn} flex-1 px-1`} onClick={() => doi(50)}>
              +0,5
            </button>
          </div>
          <ol className="space-y-2 text-base leading-relaxed">
            {buoc.map((b, i) => (
              <li key={b.key}>
                <button
                  type="button"
                  onClick={() => setNhin(nhin === b.key ? null : b.key)}
                  className={`w-full rounded-lg px-3 py-2 text-left ${nhin === b.key ? "bg-primary-soft" : "bg-surface-2"}`}
                >
                  {i + 1}. {b.text}
                </button>
              </li>
            ))}
            <li className="rounded-lg border border-line-strong px-3 py-2">
              4. <b>Số đọc:</b> d = {m}
              {nua ? " + 0,50" : ""} + {kStr} = <b>{ghiPanme(zH)} mm</b>.
            </li>
          </ol>
          <p className="text-sm text-muted">
            Bấm từng bước để tô phần cần nhìn. Dễ nhầm nhất khi thước tròn gần vạch 0: bấm −0,01 và +0,01 quanh {m},50
            mm để xem vạch nửa mm hiện ra.
          </p>
        </div>
      ) : (
        <div className="mt-3">
          <LuyenDoc
            cauKey={String(zLuyen)}
            donVi="mm"
            nhan={<>Panme chỉ bao nhiêu?</>}
            cham={(raw) => chamPanme(raw, zLuyen)}
            onDaCham={(kq) => {
              setDaCham(true);
              ghi("0.01", kq.loai === "dung");
            }}
            onCauMoi={cauMoi}
            tienDo={tienDo["0.01"]}
            tenNhiemVu="đọc panme"
          />
        </div>
      )}
    </section>
  );
}
