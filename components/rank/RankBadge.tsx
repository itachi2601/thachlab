"use client";

import { useId } from "react";
import ParagonBadge from "@/components/rank/ParagonBadge";
import { divisionLabel, tierMeta, type TierCode } from "@/features/rank/types";

/**
 * Huy chương kiểu quân đội theo bậc.
 * Thân huy chương + màu ruy-băng = bậc; kim loại = phân bậc (III đồng · II bạc · I vàng).
 * Thiên Thể / Chí Tôn không có phân bậc → luôn vàng.
 * `paragon` = danh vị Vô Song (trên Chí Tôn) → vẽ huy hiệu độc quyền ParagonBadge thay cho huy chương bậc.
 */

type Metal = "bronze" | "silver" | "gold";

const METALS: Record<Metal, { diag: string[]; vert: string[]; edge: string }> = {
  gold: { diag: ["#fff3cf", "#e2b93b", "#8a6a1e", "#f0d060", "#6b4f12"], vert: ["#fff0bf", "#d4a836", "#7a5a14"], edge: "#5a3f0c" },
  silver: { diag: ["#ffffff", "#d6dbe3", "#6f7784", "#eef1f5", "#4b525e"], vert: ["#ffffff", "#b8bfc9", "#5a6270"], edge: "#4b525e" },
  bronze: { diag: ["#f3d3ae", "#c0803c", "#5c3814", "#e0a060", "#3d2410"], vert: ["#f0c9a0", "#b87333", "#5a3a1a"], edge: "#3d2410" },
};

const PLAT = { diag: ["#ffffff", "#e6e9f0", "#8d95a3", "#f6f7fa", "#5e6572"], vert: ["#ffffff", "#c3c9d4", "#6b7380"], edge: "#4b525e" };

interface Ribbon {
  base: string;
  stripes: [number, number, string][];
}

const RIBBONS: Record<TierCode, Ribbon> = {
  tan_binh: { base: "#1b2a4a", stripes: [[92, 3, "#d8e6ff"], [145, 3, "#d8e6ff"], [112, 16, "#9fc3ff"]] },
  chien_binh: { base: "#2f4a2a", stripes: [[98, 6, "#c9a15a"], [136, 6, "#c9a15a"], [116, 8, "#e8dcc0"]] },
  tinh_anh: { base: "#b8500f", stripes: [[96, 6, "#ffd27a"], [138, 6, "#ffd27a"], [118, 4, "#3a1a05"]] },
  tinh_nhue: { base: "#8b0016", stripes: [[94, 6, "#e8c85a"], [140, 6, "#e8c85a"], [118, 4, "#fff3cf"]] },
  dai_su: { base: "#0f2a7a", stripes: [[100, 6, "#ffffff"], [134, 6, "#ffffff"], [118, 4, "#e8c85a"]] },
  cao_thu: { base: "#3a1275", stripes: [[96, 6, "#26c6da"], [138, 6, "#26c6da"], [117, 6, "#d3b0ff"]] },
  thach_dau: { base: "#111111", stripes: [[88, 7, "#e2b93b"], [145, 7, "#e2b93b"], [111, 18, "#b0001a"], [119, 2, "#e2b93b"]] },
};

const STAR5 = "M0,-6 L1.5,-2 L5.7,-1.9 L2.4,0.8 L3.5,4.9 L0,2.5 L-3.5,4.9 L-2.4,0.8 L-5.7,-1.9 L-1.5,-2 Z";
const RAY_L = "M120,138 L128,172 L112,172 Z";
const RAY_S = "M120,150 L126,172 L114,172 Z";
const PT8_L = "M120,140 L129,198 L120,208 L111,198 Z";
const PT8_S = "M120,160 L126,200 L120,206 L114,200 Z";
const CROSS_ARM = "M120,204 L102,150 L110,142 L120,152 L130,142 L138,150 Z";

const LEAVES: [number, number, number][] = [
  [98, 260, -30], [84, 246, -50], [72, 226, -70], [66, 204, -90], [66, 180, -110], [72, 160, -130],
  [90, 250, 30], [76, 232, 10], [68, 212, -10], [66, 190, -30], [70, 168, -50],
];

function rot(deg: number) {
  return `rotate(${deg} 120 204)`;
}

export default function RankBadge({
  code,
  division,
  size = 64,
  className = "",
  paragon = false,
}: {
  code: string | null | undefined;
  division?: number | null;
  size?: number;
  className?: string;
  paragon?: boolean | null;
}) {
  const meta = tierMeta(code);
  const tier = (code && code in RIBBONS ? code : "tan_binh") as TierCode;
  const uid = useId().replace(/:/g, "");
  if (paragon) return <ParagonBadge size={size} className={className} />;
  const id = (n: string) => `${uid}-${n}`;
  const url = (n: string) => `url(#${id(n)})`;
  const div = divisionLabel(division);
  const metalKey: Metal = division === 3 ? "bronze" : division === 2 ? "silver" : "gold";
  const m = METALS[metalKey];
  const rib = RIBBONS[tier];
  const detailed = size >= 40;
  const fillMetal = url("m-diag");
  const fillMetalV = url("m-vert");
  const fillGold = url("g-diag");
  const fillGoldV = url("g-vert");
  const fillPlat = url("p-diag");
  const fillPlatV = url("p-vert");
  const edge = m.edge;

  const grad = (name: string, stops: string[], vertical: boolean) => (
    <linearGradient id={id(name)} x1="0" y1="0" x2={vertical ? "0" : "1"} y2="1">
      {stops.map((c, i) => (
        <stop key={i} offset={stops.length === 5 ? [0, 0.3, 0.55, 0.75, 1][i] : [0, 0.6, 1][i]} stopColor={c} />
      ))}
    </linearGradient>
  );

  const star = (x: number, y: number, s: number, fill: string, stroke?: string) => (
    <path d={STAR5} fill={fill} stroke={stroke} strokeWidth={stroke ? 0.4 : 0} transform={`translate(${x} ${y}) scale(${s})`} />
  );

  const clasp = (y: number) => (
    <g key={y} transform={`translate(0 ${y})`}>
      <rect x="86" y="-4" width="68" height="8" fill={fillMetal} stroke={edge} strokeWidth="0.8" />
      <path d="M92,-4 V4 M148,-4 V4" stroke={edge} strokeWidth="0.8" />
    </g>
  );

  const rosette = (y: number, color: string) => (
    <g>
      <circle cx="120" cy={y} r="10" fill={color} stroke={fillMetal} strokeWidth="2.5" />
      <circle cx="120" cy={y} r="10" fill="none" stroke="#fff3cf" strokeWidth="1" strokeDasharray="2 2" opacity="0.8" />
      <circle cx="120" cy={y} r="3.5" fill={fillMetal} />
    </g>
  );

  const loop = (
    <g>
      <circle cx="120" cy="113" r="7" fill="none" stroke={fillMetal} strokeWidth="3.5" />
      <circle cx="120" cy="113" r="7" fill="none" stroke={edge} strokeWidth="0.6" />
    </g>
  );

  const crown = (scale = 1) => (
    <g transform={`translate(120 122) scale(${scale})`}>
      <path d="M-18,12 L-18,-8 L-9,1 L0,-14 L9,1 L18,-8 L18,12 Z" fill={fillMetal} stroke={edge} strokeWidth="1" />
      <rect x="-18" y="8" width="36" height="6" fill={m.vert[1]} stroke={edge} strokeWidth="1" />
      <circle cx="-18" cy="-8" r="2.5" fill="#ff5a6e" />
      <circle cx="0" cy="-14" r="3" fill="#ffffff" />
      <circle cx="18" cy="-8" r="2.5" fill="#ff5a6e" />
    </g>
  );

  const wreath = (
    <g>
      {[false, true].map((mirror) => (
        <g key={String(mirror)} transform={mirror ? "matrix(-1 0 0 1 240 0)" : undefined}>
          <path d="M104,266 C62,250 50,204 64,154" fill="none" stroke={fillMetal} strokeWidth="2.5" />
          {LEAVES.map(([x, y, r], i) => (
            <ellipse key={i} rx="3.6" ry="7.5" fill={fillMetal} transform={`translate(${x} ${y}) rotate(${r})`} />
          ))}
        </g>
      ))}
    </g>
  );

  const rays = (count: 16 | 24, fill: string, stroke: string) => {
    const step = 360 / (count / 2);
    return (
      <g fill={fill} stroke={stroke} strokeWidth="0.5">
        {Array.from({ length: count / 2 }, (_, k) => (
          <path key={`l${k}`} d={RAY_L} transform={rot(k * step)} />
        ))}
        {Array.from({ length: count / 2 }, (_, k) => (
          <path key={`s${k}`} d={RAY_S} transform={rot(step / 2 + k * step)} />
        ))}
      </g>
    );
  };

  const points8 = (d: string, offset: number, fill: string, stroke: string, sw: number) => (
    <g fill={fill} stroke={stroke} strokeWidth={sw}>
      {Array.from({ length: 8 }, (_, k) => (
        <path key={k} d={d} transform={rot(offset + k * 45)} />
      ))}
    </g>
  );

  const enamel = (r: number, color: string, ring = true) => (
    <g>
      <circle cx="120" cy="204" r={r + 6} fill={fillMetal} stroke={edge} strokeWidth="1" />
      <circle cx="120" cy="204" r={r} fill={color} />
      <circle cx="120" cy="204" r={r} fill={url("shade")} />
      {ring && <circle cx="120" cy="204" r={r} fill="none" stroke="#fff3cf" strokeWidth="0.8" opacity="0.6" />}
    </g>
  );

  let devices: React.ReactNode = null;
  let suspension: React.ReactNode = loop;
  let body: React.ReactNode = null;

  switch (tier) {
    case "tan_binh":
      body = (
        <g>
          <circle cx="120" cy="204" r="58" fill={fillMetal} stroke={edge} strokeWidth="1.5" />
          <circle cx="120" cy="204" r="50" fill="#2a2418" stroke={m.vert[0]} strokeWidth="1" opacity="0.95" />
          <circle cx="120" cy="204" r="46" fill="none" stroke={fillMetal} strokeWidth="1" strokeDasharray="1 3" />
          {star(120, 204, 6, fillMetalV, edge)}
        </g>
      );
      break;
    case "chien_binh":
      devices = star(120, 58, 1.6, fillMetal, edge);
      body = (
        <g>
          <path d="M120,146 L166,162 V204 C166,236 142,256 120,266 C98,256 74,236 74,204 V162 Z" fill={fillMetal} stroke={edge} strokeWidth="1.5" />
          <path d="M120,158 L156,170 V204 C156,228 138,246 120,254 C102,246 84,228 84,204 V170 Z" fill="#1d2430" stroke={m.vert[0]} strokeWidth="1" />
          <path d="M92,196 L120,220 L148,196" fill="none" stroke={fillMetalV} strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M92,196 L120,220 L148,196" fill="none" stroke={edge} strokeWidth="0.8" strokeLinecap="round" strokeLinejoin="round" opacity="0.6" />
          <path d="M98,222 L120,240 L142,222" fill="none" stroke={fillMetalV} strokeWidth="4" strokeLinecap="round" />
          {star(120, 180, 2.2, fillMetalV)}
        </g>
      );
      break;
    case "tinh_anh":
      devices = (
        <g>
          {star(108, 58, 1.5, fillMetal, edge)}
          {star(132, 58, 1.5, fillMetal, edge)}
        </g>
      );
      body = (
        <g>
          {rays(16, fillMetalV, edge)}
          {enamel(32, "#c96b12")}
          <circle cx="120" cy="204" r="9" fill={fillMetalV} stroke={edge} strokeWidth="0.6" />
        </g>
      );
      break;
    case "tinh_nhue":
      devices = rosette(58, rib.base);
      body = (
        <g>
          {wreath}
          <g fill={fillMetalV} stroke={edge} strokeWidth="1">
            {[0, 90, 180, 270].map((a) => (
              <path key={a} d={CROSS_ARM} transform={rot(a)} />
            ))}
          </g>
          {enamel(17, "#b0001a", false)}
          {star(120, 204, 1.6, "#fff3cf")}
        </g>
      );
      break;
    case "dai_su":
      devices = (
        <g>
          {clasp(40)}
          {clasp(64)}
        </g>
      );
      suspension = crown();
      body = (
        <g>
          {wreath}
          {points8(PT8_S, 22.5, fillPlatV, PLAT.edge, 0.6)}
          {points8(PT8_L, 0, fillMetalV, edge, 0.8)}
          {enamel(20, "#0a2a7a", false)}
          {star(120, 204, 2.2, fillMetalV)}
        </g>
      );
      break;
    case "cao_thu":
      devices = (
        <g>
          {rosette(34, rib.base)}
          {clasp(58)}
          {clasp(80)}
        </g>
      );
      body = (
        <g>
          {wreath}
          <circle cx="120" cy="204" r="64" fill="none" stroke={fillMetal} strokeWidth="1.2" strokeDasharray="1 3" />
          {points8(PT8_L, 22.5, fillPlatV, PLAT.edge, 0.6)}
          {points8(PT8_L, 0, fillMetalV, edge, 0.8)}
          {enamel(21, "#3a1275", false)}
          <ellipse cx="120" cy="204" rx="15" ry="4.5" fill="none" stroke={fillPlat} strokeWidth="2" transform="rotate(-22 120 204)" />
          <circle cx="120" cy="204" r="7" fill={fillPlat} stroke={PLAT.edge} strokeWidth="0.6" />
        </g>
      );
      break;
    case "thach_dau":
      devices = (
        <g>
          {rosette(30, "#b0001a")}
          {clasp(52)}
          {clasp(68)}
          {clasp(84)}
        </g>
      );
      suspension = crown(1.25);
      body = (
        <g>
          <path d="M66,258 L172,150" stroke={url("s-diag")} strokeWidth="6" strokeLinecap="round" />
          <path d="M174,258 L68,150" stroke={url("s-diag")} strokeWidth="6" strokeLinecap="round" />
          <path d="M78,240 L92,254 M162,240 L148,254" stroke={fillGold} strokeWidth="5" strokeLinecap="round" />
          {wreath}
          {rays(24, fillGoldV, "#5a3f0c")}
          {points8(PT8_L, 0, fillPlatV, PLAT.edge, 0.7)}
          {enamel(23, "#b0001a", false)}
          <circle cx="120" cy="204" r="23" fill="none" stroke="#fff3cf" strokeWidth="0.8" strokeDasharray="2 2" opacity="0.7" />
          {detailed && (
            <g filter={url("glow")}>
              <circle cx="120" cy="204" r="13" fill="#ffffff" />
            </g>
          )}
          <circle cx="120" cy="204" r="13" fill={fillPlat} opacity="0.85" />
          <polygon
            points="132,199 127.2,194.2 120,192.2 112.8,194.2 108,199 108,209 112.8,213.8 120,215.8 127.2,213.8 132,209"
            fill="none"
            stroke="#fff"
            strokeWidth="0.8"
            opacity="0.8"
          />
        </g>
      );
      break;
  }

  return (
    <svg
      viewBox="28 0 184 280"
      width={size}
      height={Math.round((size * 280) / 184)}
      className={className}
      role="img"
      aria-label={`Huy chương ${meta.name}${div ? ` ${div}` : ""}`}
    >
      <defs>
        {grad("m-diag", m.diag, false)}
        {grad("m-vert", m.vert, true)}
        {grad("g-diag", METALS.gold.diag, false)}
        {grad("g-vert", METALS.gold.vert, true)}
        {grad("p-diag", PLAT.diag, false)}
        {grad("p-vert", PLAT.vert, true)}
        {grad("s-diag", METALS.silver.diag, false)}
        <linearGradient id={id("shade")} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#fff" stopOpacity="0.18" />
          <stop offset="0.5" stopColor="#000" stopOpacity="0" />
          <stop offset="1" stopColor="#000" stopOpacity="0.35" />
        </linearGradient>
        <linearGradient id={id("ribside")} x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#000" stopOpacity="0.35" />
          <stop offset="0.15" stopColor="#000" stopOpacity="0" />
          <stop offset="0.85" stopColor="#000" stopOpacity="0" />
          <stop offset="1" stopColor="#000" stopOpacity="0.35" />
        </linearGradient>
        {detailed && (
          <>
            <pattern id={id("rib")} width="2" height="3" patternUnits="userSpaceOnUse">
              <rect width="2" height="1" fill="#000" opacity="0.14" />
            </pattern>
            <filter id={id("shadow")} x="-30%" y="-30%" width="160%" height="160%">
              <feDropShadow dx="0" dy="4" stdDeviation="3.5" floodColor="#000" floodOpacity="0.65" />
            </filter>
            <filter id={id("glow")} x="-60%" y="-60%" width="220%" height="220%">
              <feGaussianBlur stdDeviation="3" result="b" />
              <feMerge>
                <feMergeNode in="b" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </>
        )}
      </defs>
      <g filter={detailed ? url("shadow") : undefined}>
        <rect x="88" y="10" width="64" height="98" fill={rib.base} />
        {rib.stripes.map(([x, w, c], i) => (
          <rect key={i} x={x} y="10" width={w} height="98" fill={c} />
        ))}
        {detailed && <rect x="88" y="10" width="64" height="98" fill={url("rib")} />}
        <rect x="88" y="10" width="64" height="98" fill={url("shade")} />
        <rect x="88" y="10" width="64" height="98" fill={url("ribside")} />
        <rect x="82" y="6" width="76" height="9" fill={fillMetal} stroke={edge} strokeWidth="0.8" />
        {devices}
        {suspension}
        {body}
      </g>
    </svg>
  );
}
