"use client";

import { useId } from "react";

/**
 * Huy hiệu độc quyền "Vô Song" (Paragon) — trên cả Chí Tôn, chỉ dành cho học sinh
 * đã đạt trọn bộ danh hiệu và vượt mọi bậc của mùa.
 *
 * Cùng hệ toạ độ với RankBadge (viewBox 240×280, crop 28..212) để dùng chung mọi chỗ.
 * Ngôn ngữ thiết kế: đại huân chương đeo cổ (collar order) — dây chuyền hai bên thay cho
 * ruy-băng đơn, vương miện kín có vòm, đôi cánh vàng, ngôi sao 32 tia bạch kim–vàng,
 * men huyền (obsidian) với biểu tượng nguyên tử — dấu ấn Vật lí của thachlab.
 * Kim loại: bạch kim làm khung, vàng làm điểm nhấn; men trung tâm ánh cực quang (aurora).
 */

const GOLD = { diag: ["#fff3cf", "#e2b93b", "#8a6a1e", "#f0d060", "#6b4f12"], vert: ["#fff0bf", "#d4a836", "#7a5a14"], edge: "#5a3f0c" };
const PLAT = { diag: ["#ffffff", "#e6e9f0", "#8d95a3", "#f6f7fa", "#5e6572"], vert: ["#ffffff", "#c3c9d4", "#6b7380"], edge: "#4b525e" };
const SILVER = ["#ffffff", "#d6dbe3", "#6f7784", "#eef1f5", "#4b525e"];
const AURORA = ["#26c6da", "#7c4dff", "#ff8fd8", "#ffd166"];

const STAR5 = "M0,-6 L1.5,-2 L5.7,-1.9 L2.4,0.8 L3.5,4.9 L0,2.5 L-3.5,4.9 L-2.4,0.8 L-5.7,-1.9 L-1.5,-2 Z";
const RAY_L = "M120,128 L128,172 L112,172 Z";
const RAY_S = "M120,146 L125,172 L115,172 Z";
const SPARK = "M0,-9 C0.8,-2 2,-0.8 9,0 C2,0.8 0.8,2 0,9 C-0.8,2 -2,0.8 -9,0 C-2,-0.8 -0.8,-2 0,-9 Z";

const LEAVES: [number, number, number][] = [
  [98, 260, -30], [84, 246, -50], [72, 226, -70], [66, 204, -90], [66, 180, -110], [72, 160, -130],
  [90, 250, 30], [76, 232, 10], [68, 212, -10], [66, 190, -30], [70, 168, -50],
];

/** Cánh trái: gốc cánh ở (100,196), xoè ra tới x≈42 với ba lớp lông vũ. */
const WING = "M102,188 C88,164 62,156 40,166 C56,172 60,182 48,190 C64,188 72,194 60,204 C76,200 84,206 74,216 C88,212 96,216 102,226 Z";
const WING_LINES = ["M96,196 C82,182 66,176 50,178", "M96,206 C84,196 72,196 58,200", "M98,216 C88,208 80,210 72,214"];

function rot(deg: number) {
  return `rotate(${deg} 120 204)`;
}

/** Điểm trên đường Bézier bậc 3 — dùng rải mắt xích dây chuyền. */
function bez(t: number, p: [number, number][]): [number, number] {
  const u = 1 - t;
  const x = u * u * u * p[0][0] + 3 * u * u * t * p[1][0] + 3 * u * t * t * p[2][0] + t * t * t * p[3][0];
  const y = u * u * u * p[0][1] + 3 * u * u * t * p[1][1] + 3 * u * t * t * p[2][1] + t * t * t * p[3][1];
  return [x, y];
}

const CHAIN_L: [number, number][] = [[84, 16], [66, 48], [70, 96], [104, 118]];

export default function ParagonBadge({
  size = 64,
  className = "",
  animate = true,
}: {
  size?: number;
  className?: string;
  /** Tắt để tôn trọng prefers-reduced-motion hoặc khi render hàng loạt. */
  animate?: boolean;
}) {
  const uid = useId().replace(/:/g, "");
  const id = (n: string) => `${uid}-${n}`;
  const url = (n: string) => `url(#${id(n)})`;
  const detailed = size >= 40;
  const anim = animate && detailed;

  const fillPlat = url("p-diag");
  const fillPlatV = url("p-vert");
  const fillGold = url("g-diag");
  const fillGoldV = url("g-vert");
  const edge = PLAT.edge;

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

  /** Thanh cài cao cấp: bạch kim, đính 3 sao vàng. */
  const clasp = (y: number) => (
    <g key={y} transform={`translate(0 ${y})`}>
      <rect x="86" y="-4" width="68" height="8" fill={fillPlat} stroke={edge} strokeWidth="0.8" />
      <path d="M92,-4 V4 M148,-4 V4" stroke={edge} strokeWidth="0.8" />
      {star(108, 0, 0.55, fillGoldV)}
      {star(120, 0, 0.55, fillGoldV)}
      {star(132, 0, 0.55, fillGoldV)}
    </g>
  );

  /** Hoa hồng men huyền viền bạch kim, tâm kim cương. */
  const rosette = (y: number) => (
    <g>
      <circle cx="120" cy={y} r="11" fill={url("obsidian")} stroke={fillPlat} strokeWidth="2.5" />
      <circle cx="120" cy={y} r="11" fill="none" stroke="#fff3cf" strokeWidth="1" strokeDasharray="2 2" opacity="0.8" />
      <circle cx="120" cy={y} r="4" fill={fillGold} stroke={GOLD.edge} strokeWidth="0.5" />
      <circle cx="120" cy={y} r="1.6" fill="#ffffff" />
    </g>
  );

  /** Vương miện kín (imperial): vòm gặp nhau ở quả cầu, mũ men huyền bên trong. */
  const crown = (
    <g transform="translate(120 122) scale(1.35)">
      <path d="M-18,-8 C-10,-27 10,-27 18,-8 Z" fill={url("obsidian")} />
      <path d="M-18,12 L-18,-8 L-9,1 L0,-14 L9,1 L18,-8 L18,12 Z" fill={fillPlat} stroke={edge} strokeWidth="1" />
      <path d="M-18,-8 C-10,-27 10,-27 18,-8" fill="none" stroke={fillGoldV} strokeWidth="2.6" />
      <path d="M-18,-8 C-10,-27 10,-27 18,-8" fill="none" stroke={GOLD.edge} strokeWidth="0.5" />
      <rect x="-18" y="8" width="36" height="6" fill={PLAT.vert[1]} stroke={edge} strokeWidth="1" />
      <circle cx="-10" cy="11" r="1.6" fill="#7c4dff" />
      <circle cx="0" cy="11" r="1.6" fill="#26c6da" />
      <circle cx="10" cy="11" r="1.6" fill="#7c4dff" />
      <circle cx="-18" cy="-8" r="2.5" fill="#26c6da" />
      <circle cx="0" cy="-14" r="3" fill="#ffffff" />
      <circle cx="18" cy="-8" r="2.5" fill="#26c6da" />
      <circle cx="0" cy="-22" r="3" fill={fillGold} stroke={GOLD.edge} strokeWidth="0.5" />
      {star(0, -29, 0.9, fillGoldV)}
    </g>
  );

  /** Dây chuyền cổ hai bên: mắt xích vàng – bạch kim xen kẽ, ôm lấy ruy-băng. */
  const chain = (mirror: boolean) => {
    const n = 11;
    return (
      <g transform={mirror ? "matrix(-1 0 0 1 240 0)" : undefined}>
        <path d={`M${CHAIN_L[0].join(",")} C${CHAIN_L[1].join(",")} ${CHAIN_L[2].join(",")} ${CHAIN_L[3].join(",")}`} fill="none" stroke={GOLD.vert[1]} strokeWidth="1.6" />
        {Array.from({ length: n }, (_, k) => {
          const [x, y] = bez(k / (n - 1), CHAIN_L);
          const goldLink = k % 2 === 0;
          return (
            <g key={k}>
              <circle cx={x} cy={y} r={goldLink ? 3.2 : 2.6} fill={goldLink ? fillGold : fillPlat} stroke={goldLink ? GOLD.edge : edge} strokeWidth="0.6" />
              {goldLink ? <circle cx={x} cy={y} r="1.3" fill={url("obsidian")} /> : null}
            </g>
          );
        })}
      </g>
    );
  };

  const wreath = (
    <g>
      {[false, true].map((mirror) => (
        <g key={String(mirror)} transform={mirror ? "matrix(-1 0 0 1 240 0)" : undefined}>
          <path d="M104,266 C62,250 50,204 64,154" fill="none" stroke={fillGold} strokeWidth="2.5" />
          {LEAVES.map(([x, y, r], i) => (
            <ellipse key={i} rx="3.6" ry="7.5" fill={fillGold} transform={`translate(${x} ${y}) rotate(${r})`} />
          ))}
        </g>
      ))}
    </g>
  );

  const wings = (
    <g>
      {[false, true].map((mirror) => (
        <g key={String(mirror)} transform={mirror ? "matrix(-1 0 0 1 240 0)" : undefined}>
          <path d={WING} fill={fillGoldV} stroke={GOLD.edge} strokeWidth="1" strokeLinejoin="round" />
          {WING_LINES.map((d, i) => (
            <path key={i} d={d} fill="none" stroke={GOLD.edge} strokeWidth="0.7" opacity="0.7" />
          ))}
        </g>
      ))}
    </g>
  );

  const rays = (
    <g strokeWidth="0.5">
      {Array.from({ length: 16 }, (_, k) => (
        <path key={`l${k}`} d={RAY_L} fill={fillGoldV} stroke={GOLD.edge} transform={rot(k * 22.5)} />
      ))}
      {Array.from({ length: 16 }, (_, k) => (
        <path key={`s${k}`} d={RAY_S} fill={fillPlatV} stroke={edge} transform={rot(11.25 + k * 22.5)} />
      ))}
    </g>
  );

  /** Nguyên tử: ba quỹ đạo bạch kim quanh hạt nhân sáng, ba electron vàng. */
  const atom = (
    <g>
      {[0, 60, 120].map((a) => (
        <ellipse key={a} cx="120" cy="204" rx="20" ry="7" fill="none" stroke={fillPlat} strokeWidth="1.6" transform={rot(a)} />
      ))}
      {[0, 60, 120].map((a, i) => (
        <circle key={a} cx={120 + 20 * Math.cos(((a + 40 + i * 100) * Math.PI) / 180)} cy={204 + 7 * Math.sin(((a + 40 + i * 100) * Math.PI) / 180)} r="2" fill={fillGold} stroke={GOLD.edge} strokeWidth="0.4" transform={rot(a)} />
      ))}
      {detailed && (
        <g filter={url("glow")}>
          <circle cx="120" cy="204" r="6" fill="#ffffff">
            {anim && <animate attributeName="r" values="5.5;7;5.5" dur="3s" repeatCount="indefinite" />}
          </circle>
        </g>
      )}
      <circle cx="120" cy="204" r="5" fill="#ffffff" />
      <path d={SPARK} fill="#ffffff" opacity="0.9" transform="translate(120 204) scale(0.9)">
        {anim && <animateTransform attributeName="transform" type="rotate" from="0 120 204" to="360 120 204" dur="24s" repeatCount="indefinite" additive="sum" />}
      </path>
    </g>
  );

  return (
    <svg
      viewBox="28 0 184 280"
      width={size}
      height={Math.round((size * 280) / 184)}
      className={className}
      role="img"
      aria-label="Huy chương Vô Song"
    >
      <defs>
        {grad("p-diag", PLAT.diag, false)}
        {grad("p-vert", PLAT.vert, true)}
        {grad("g-diag", GOLD.diag, false)}
        {grad("g-vert", GOLD.vert, true)}
        {grad("s-diag", SILVER, false)}
        <radialGradient id={id("obsidian")} cx="0.4" cy="0.35" r="0.8">
          <stop offset="0" stopColor="#2a1d4a" />
          <stop offset="0.6" stopColor="#0e0a1c" />
          <stop offset="1" stopColor="#05030a" />
        </radialGradient>
        <linearGradient id={id("aurora")} x1="0" y1="0" x2="0" y2="1">
          {AURORA.map((c, i) => (
            <stop key={i} offset={i / (AURORA.length - 1)} stopColor={c}>
              {anim && (
                <animate attributeName="stop-color" values={`${c};${AURORA[(i + 1) % AURORA.length]};${AURORA[(i + 2) % AURORA.length]};${c}`} dur="9s" repeatCount="indefinite" />
              )}
            </stop>
          ))}
        </linearGradient>
        <radialGradient id={id("halo")} cx="0.5" cy="0.5" r="0.5">
          <stop offset="0" stopColor="#7c4dff" stopOpacity="0.55" />
          <stop offset="0.6" stopColor="#26c6da" stopOpacity="0.18" />
          <stop offset="1" stopColor="#26c6da" stopOpacity="0" />
        </radialGradient>
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

      {/* Vầng sáng cực quang sau ngôi sao — chỉ ở cỡ lớn */}
      {detailed && <circle cx="120" cy="204" r="82" fill={url("halo")} />}

      <g filter={detailed ? url("shadow") : undefined}>
        {/* Ruy-băng men huyền, sọc cực quang giữa, viền bạch kim – vàng */}
        <rect x="88" y="10" width="64" height="98" fill="#07060d" />
        <rect x="90" y="10" width="2" height="98" fill="#e2b93b" />
        <rect x="148" y="10" width="2" height="98" fill="#e2b93b" />
        <rect x="95" y="10" width="5" height="98" fill="#d6dbe3" />
        <rect x="140" y="10" width="5" height="98" fill="#d6dbe3" />
        <rect x="111" y="10" width="18" height="98" fill={url("aurora")} />
        {detailed && <rect x="88" y="10" width="64" height="98" fill={url("rib")} />}
        <rect x="88" y="10" width="64" height="98" fill={url("shade")} />
        <rect x="88" y="10" width="64" height="98" fill={url("ribside")} />
        <rect x="82" y="6" width="76" height="9" fill={fillPlat} stroke={edge} strokeWidth="0.8" />

        {chain(false)}
        {chain(true)}

        {rosette(30)}
        {clasp(50)}
        {clasp(64)}
        {crown}

        {/* Thân: gươm chéo → nguyệt quế → 32 tia → cánh (đè lên tia, luồn dưới men) → men huyền nguyên tử */}
        <path d="M66,258 L172,150" stroke={url("s-diag")} strokeWidth="6" strokeLinecap="round" />
        <path d="M174,258 L68,150" stroke={url("s-diag")} strokeWidth="6" strokeLinecap="round" />
        <path d="M78,240 L92,254 M162,240 L148,254" stroke={fillGold} strokeWidth="5" strokeLinecap="round" />
        {wreath}
        <circle cx="120" cy="204" r="70" fill="none" stroke={fillPlat} strokeWidth="1.2" strokeDasharray="1 3" />
        {rays}
        {wings}
        <circle cx="120" cy="204" r="34" fill={fillPlat} stroke={edge} strokeWidth="1" />
        <circle cx="120" cy="204" r="30" fill={fillGoldV} stroke={GOLD.edge} strokeWidth="0.6" />
        {Array.from({ length: 12 }, (_, k) => {
          const a = (k * 30 * Math.PI) / 180;
          return <rect key={k} x={120 + 32 * Math.cos(a) - 1.4} y={204 + 32 * Math.sin(a) - 1.4} width="2.8" height="2.8" fill="#ffffff" transform={`rotate(45 ${120 + 32 * Math.cos(a)} ${204 + 32 * Math.sin(a)})`} />;
        })}
        <circle cx="120" cy="204" r="27" fill={url("obsidian")} />
        <circle cx="120" cy="204" r="27" fill={url("shade")} />
        <circle cx="120" cy="204" r="27" fill="none" stroke="#fff3cf" strokeWidth="0.8" strokeDasharray="2 2" opacity="0.7" />
        {atom}
      </g>
    </svg>
  );
}
