"use client";

import { useId } from "react";
import { divisionLabel, tierMeta } from "@/features/rank/types";

/** Huy hiệu khiên theo bậc — màu theo bậc, số La Mã là phân bậc (III → I); Cao Thủ/Thách Đấu có ngôi sao. */
export default function RankBadge({
  code,
  division,
  size = 64,
  className = "",
}: {
  code: string | null | undefined;
  division?: number | null;
  size?: number;
  className?: string;
}) {
  const meta = tierMeta(code);
  const gid = useId();
  const div = divisionLabel(division);
  const elite = code === "cao_thu" || code === "thach_dau";

  return (
    <svg
      viewBox="0 0 100 112"
      width={size}
      height={Math.round(size * 1.12)}
      className={className}
      role="img"
      aria-label={`Huy hiệu ${meta.name}${div ? ` ${div}` : ""}`}
    >
      <defs>
        <linearGradient id={`${gid}-g`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor={meta.light} />
          <stop offset="1" stopColor={meta.color} />
        </linearGradient>
        <linearGradient id={`${gid}-s`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="rgba(255,255,255,0.35)" />
          <stop offset="1" stopColor="rgba(255,255,255,0)" />
        </linearGradient>
      </defs>
      <path
        d="M50 4 L93 20 V58 C93 82 73 101 50 108 C27 101 7 82 7 58 V20 Z"
        fill={`url(#${gid}-g)`}
        stroke="rgba(255,255,255,0.28)"
        strokeWidth="2"
      />
      <path
        d="M50 14 L83 26 V58 C83 76 68 91 50 97 C32 91 17 76 17 58 V26 Z"
        fill="rgba(5,7,15,0.35)"
        stroke="rgba(255,255,255,0.12)"
        strokeWidth="1"
      />
      <path d="M50 4 L93 20 V40 C70 46 30 46 7 40 V20 Z" fill={`url(#${gid}-s)`} opacity="0.5" />
      {elite ? (
        <path
          d="M50 34 L56.5 49 L73 50.5 L60.5 61.5 L64.5 78 L50 69.5 L35.5 78 L39.5 61.5 L27 50.5 L43.5 49 Z"
          fill="#fff"
          opacity="0.95"
        />
      ) : (
        <text
          x="50"
          y="70"
          textAnchor="middle"
          fontSize={div.length > 2 ? 30 : 36}
          fontWeight="800"
          fill="#fff"
          fontFamily="var(--font-display), ui-sans-serif, system-ui"
        >
          {div || meta.name.charAt(0)}
        </text>
      )}
    </svg>
  );
}
