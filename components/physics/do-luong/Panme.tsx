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

import { useId, useRef, useState, type ReactNode } from "react";
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

/* ---------------- Màu thép (cố định, không đổi theo sáng/tối: đây là "ảnh" dụng cụ thật — M5) ---------------- */

/** Mực khắc vạch; màu tô bước đang đọc — cố định vì nằm trên nền thép sáng ở cả hai chế độ (như ThuocKep). */
const MUC = "#1b2026";
const XANH = "#1d4ed8";
const LUC = "#15803d";
/** Chữ đậm hơn nét để đạt ≥ 4,5:1 trên thép. */
const LUC_CHU = "#166534";
const XANH_CHU = "#1e40af";
const VIEN = "#5f6a74";

function MauThep({ id }: { id: string }) {
  return (
    <defs>
      {/* ống cố định: hình trụ trục ngang, sáng ở giữa, tối dần về hai mép */}
      <linearGradient id={`${id}-ong`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#aeb7bf" />
        <stop offset="0.22" stopColor="#e9edf0" />
        <stop offset="0.5" stopColor="#f7f9fa" />
        <stop offset="0.8" stopColor="#d6dce1" />
        <stop offset="1" stopColor="#a2acb5" />
      </linearGradient>
      {/* thước tròn: trụ to hơn, bóng đổ mạnh hơn ở hai mép */}
      <linearGradient id={`${id}-tron`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#808a93" />
        <stop offset="0.17" stopColor="#c6cdd3" />
        <stop offset="0.36" stopColor="#eef1f4" />
        <stop offset="0.5" stopColor="#fafbfc" />
        <stop offset="0.64" stopColor="#eceff2" />
        <stop offset="0.83" stopColor="#c0c8ce" />
        <stop offset="1" stopColor="#7a848d" />
      </linearGradient>
      {/* mép vát của thước tròn (sáng hơn thân) */}
      <linearGradient id={`${id}-vat`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#9aa4ad" />
        <stop offset="0.5" stopColor="#ffffff" />
        <stop offset="1" stopColor="#959fa8" />
      </linearGradient>
      {/* bóng phủ lên phần khía để giữ khối trụ */}
      <linearGradient id={`${id}-bong`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#000" stopOpacity={0.5} />
        <stop offset="0.45" stopColor="#000" stopOpacity={0} />
        <stop offset="0.55" stopColor="#000" stopOpacity={0} />
        <stop offset="1" stopColor="#000" stopOpacity={0.5} />
      </linearGradient>
      {/* khung chữ U sơn xanh lá đậm */}
      <linearGradient id={`${id}-khung`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#6b8a7a" />
        <stop offset="0.5" stopColor="#4c6a5a" />
        <stop offset="1" stopColor="#36503f" />
      </linearGradient>
      {/* khía thẳng song song trục (núm cóc, đuôi thước tròn, đai ốc hãm) */}
      <pattern id={`${id}-khia`} width="4" height="3" patternUnits="userSpaceOnUse">
        <rect width="4" height="3" fill="#b3bcc4" />
        <rect width="4" height="1.3" fill="#56616b" />
      </pattern>
      <radialGradient id={`${id}-toi`} cx="0.5" cy="0.5" r="0.75">
        <stop offset="0.6" stopColor="#000" stopOpacity={0} />
        <stop offset="1" stopColor="#000" stopOpacity={0.18} />
      </radialGradient>
    </defs>
  );
}

const dungId = (pre: string, raw: string) => `${pre}${raw.replace(/[^a-zA-Z0-9]/g, "")}`;

/* ---------------- Hình toàn cảnh (nhỏ): khung chữ U, đe, trục đo, đai ốc hãm, ống, thước tròn, núm cóc ---------------- */

const AY = 44; // trục đo
const S0 = 166; // vạch 0 trên ống (toàn cảnh)
const PX = 2.4; // px/mm (toàn cảnh)

function HinhToanCanh({ zH }: { zH: number }) {
  const id = dungId("pt", useId());
  const z = zH / 100;
  const te = S0 + PX * z; // mép thước tròn
  const mat = 52 + PX * z; // mặt trục đo
  const ticks: ReactNode[] = [];
  for (let j = 0; j <= Math.floor(z + 1e-9); j++) {
    const px = S0 + PX * j;
    ticks.push(<line key={j} x1={px} x2={px} y1={AY} y2={AY - (j % 5 === 0 ? 5 : 3)} />);
    if (j + 0.5 <= z + 1e-9) ticks.push(<line key={`h${j}`} x1={px + PX / 2} x2={px + PX / 2} y1={AY} y2={AY + 3} />);
  }
  const t = `url(#${id}-tron)`;
  return (
    <svg
      viewBox={`0 0 ${W} 100`}
      className="block w-full select-none"
      role="img"
      aria-label="Toàn cảnh panme: khung chữ U, đe, trục đo, ống cố định, thước tròn, núm cóc. Khung nét đứt là chỗ phóng to bên dưới."
    >
      <MauThep id={id} />
      <rect x={1} y={1} width={W - 2} height={98} rx={10} fill="#eef1f4" stroke="#c3cad1" />
      {/* đe + trục đo (vẽ trước khung để hai đầu chui vào khung) */}
      <rect x={40} y={AY - 5} width={12} height={10} fill={`url(#${id}-ong)`} stroke={VIEN} strokeWidth={0.8} />
      <rect x={mat} y={AY - 5} width={140 - mat} height={10} fill={`url(#${id}-ong)`} stroke={VIEN} strokeWidth={0.8} />
      {/* khung chữ U + tấm cách nhiệt */}
      <path
        d="M20,30 H44 V56 Q44,68 58,68 H122 Q136,68 136,56 V30 H160 V62 Q160,94 128,94 H52 Q20,94 20,62 Z"
        fill={`url(#${id}-khung)`}
        stroke="#26362c"
        strokeWidth={1}
      />
      <rect x={54} y={71} width={76} height={20} rx={4} fill="#262b2f" />
      <text x={92} y={86} textAnchor="middle" fontSize={15} fill="#f1f5f9">
        0–25 mm
      </text>
      {/* đai ốc hãm */}
      <rect x={141} y={19} width={14} height={11} rx={2} fill={`url(#${id}-khia)`} stroke={VIEN} strokeWidth={0.8} />
      {/* ống cố định có vạch */}
      <rect x={160} y={AY - 7} width={te - 156} height={14} fill={`url(#${id}-ong)`} stroke={VIEN} strokeWidth={0.8} />
      <g stroke={MUC} strokeWidth={0.6}>
        <line x1={160} x2={te} y1={AY} y2={AY} />
        {ticks}
      </g>
      {/* thước tròn: mép vát + thân + đuôi khía; núm cóc */}
      <path
        d={`M${te},${AY - 8} L${te + 5},${AY - 12} H${te + 56} V${AY + 12} H${te + 5} L${te},${AY + 8} Z`}
        fill={t}
        stroke={VIEN}
        strokeWidth={0.8}
      />
      <rect x={te + 42} y={AY - 12} width={14} height={24} fill={`url(#${id}-khia)`} />
      <rect x={te + 42} y={AY - 12} width={14} height={24} fill={`url(#${id}-bong)`} stroke={VIEN} strokeWidth={0.8} />
      <rect x={te + 57} y={AY - 8} width={17} height={16} fill={`url(#${id}-khia)`} />
      <rect x={te + 57} y={AY - 8} width={17} height={16} fill={`url(#${id}-bong)`} stroke={VIEN} strokeWidth={0.8} />
      <rect x={te + 74} y={AY - 6} width={5} height={12} rx={2} fill={t} stroke={VIEN} strokeWidth={0.8} />
      {/* chỗ phóng to */}
      <rect
        x={te - 24}
        y={AY - 17}
        width={36}
        height={34}
        rx={3}
        fill="none"
        stroke={XANH}
        strokeWidth={1.8}
        strokeDasharray="4 2.5"
      />
      {/* tên bộ phận */}
      <g fontSize={15} fill={MUC}>
        <text x={46} y={18} textAnchor="middle">
          đe
        </text>
        <text x={(mat + 136) / 2} y={18} textAnchor="middle">
          trục đo
        </text>
        <text x={te + 30} y={18} textAnchor="middle">
          thước tròn
        </text>
        <line x1={170} x2={170} y1={AY + 8} y2={AY + 33} stroke={MUC} strokeWidth={0.8} />
        <text x={164} y={90}>
          ống cố định
        </text>
        <text x={te + 66} y={72} textAnchor="middle">
          núm cóc
        </text>
      </g>
    </svg>
  );
}

/* ---------------- Hình phóng to chỗ đọc ---------------- */

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
  const id = dungId("pz", useId());
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
        stroke={hl ? XANH : MUC}
        strokeWidth={hl ? 3 : 1.5}
      />,
    );
    if (j % 5 === 0 && px > TRAI + 8)
      ong.push(
        <text key={`t${j}`} x={px} y={REF - 28} textAnchor="middle" fontSize={16} fontWeight={700} fill={MUC}>
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
        stroke={hl ? XANH : MUC}
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
        stroke={hl ? LUC : MUC}
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
          fill={hl ? LUC_CHU : MUC}
          fontWeight={hl ? 700 : 400}
        >
          {i}
        </text>,
      );
  }

  // Thước tròn: y 12–196, mép vát XT…XT+8, thân tới 334, đuôi khía 334–348, núm cóc 350+.
  const T0 = REF - 92;
  const T1 = REF + 92;
  return (
    <svg
      ref={ref}
      viewBox={`0 0 ${W} 200`}
      className="block w-full select-none"
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
      <MauThep id={id} />
      <defs>
        <clipPath id={`${id}-o`}>
          <rect x={2} y={2} width={W - 4} height={196} rx={10} />
        </clipPath>
      </defs>
      <g clipPath={`url(#${id}-o)`}>
        {/* nền phía sau dụng cụ */}
        <rect x={0} y={0} width={W} height={200} fill="#7d878f" />
        {/* ống cố định (hình trụ) */}
        <rect x={0} y={REF - 52} width={XT + 8} height={102} fill={`url(#${id}-ong)`} />
        <line x1={0} x2={XT + 8} y1={REF - 52} y2={REF - 52} stroke={VIEN} />
        <line x1={0} x2={XT + 8} y1={REF + 50} y2={REF + 50} stroke={VIEN} />
        <line x1={TRAI} x2={XT + 4} y1={REF} y2={REF} stroke={MUC} strokeWidth={1.4} />
        {ong}
        <text x={TRAI + 6} y={REF + 42} fontSize={15} fill={MUC}>
          nửa mm ↑
        </text>
        {/* thước tròn: thân + mép vát có 50 vạch */}
        <path
          d={`M${XT},${T0 + 8} L${XT + 8},${T0} H${W} V${T1} H${XT + 8} L${XT},${T1 - 8} Z`}
          fill={`url(#${id}-tron)`}
        />
        <path d={`M${XT},${T0 + 8} L${XT + 8},${T0} V${T1} L${XT},${T1 - 8} Z`} fill={`url(#${id}-vat)`} />
        <line x1={XT} x2={XT} y1={T0 + 8} y2={T1 - 8} stroke="#3f4852" strokeWidth={1.2} />
        <line x1={XT + 8} x2={XT + 8} y1={T0} y2={T1} stroke={VIEN} strokeOpacity={0.45} />
        {/* đuôi thước tròn khía + núm cóc */}
        <rect x={334} y={T0} width={14} height={T1 - T0} fill={`url(#${id}-khia)`} />
        <rect x={334} y={T0} width={14} height={T1 - T0} fill={`url(#${id}-bong)`} />
        <line x1={334} x2={334} y1={T0} y2={T1} stroke={VIEN} />
        <rect x={350} y={REF - 46} width={W - 350} height={92} fill={`url(#${id}-khia)`} />
        <rect x={350} y={REF - 46} width={W - 350} height={92} fill={`url(#${id}-bong)`} stroke={VIEN} />
        <g>{tron}</g>
        {hienTrung && (
          <text x={XT + 50} y={REF + 6} fontSize={16} fontWeight={700} fill={LUC_CHU}>
            ← {k}
          </text>
        )}
        {onKeo && (
          <g>
            <rect x={XT - 132} y={171} width={124} height={24} rx={12} fill="#f8fafc" />
            <text x={XT - 70} y={188} textAnchor="middle" fontSize={15} fill={XANH_CHU}>
              ⇆ kéo để xoay
            </text>
          </g>
        )}
        <rect x={0} y={0} width={W} height={200} fill={`url(#${id}-toi)`} pointerEvents="none" />
      </g>
      <rect x={2} y={2} width={W - 4} height={196} rx={10} fill="none" stroke="#3f4852" strokeWidth={3} />
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

      <div className="mt-3 space-y-2">
        <HinhToanCanh zH={zH} />
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
