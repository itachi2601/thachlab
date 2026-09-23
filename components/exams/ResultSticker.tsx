type Tier = "excellent" | "good" | "half" | "starting";

const GRADIENT: Record<Tier, [string, string]> = {
  excellent: ["#34d399", "#059669"],
  good: ["#22d3ee", "#0891b2"],
  half: ["#fbbf24", "#d97706"],
  starting: ["#fb7185", "#e11d48"],
};

export function resultTier(pct: number): Tier {
  if (pct >= 90) return "excellent";
  if (pct >= 70) return "good";
  if (pct >= 50) return "half";
  return "starting";
}

/** Sticker minh hoạ nhỏ cho màn hình kết quả — thay emoji trần bằng icon vẽ tay khớp theme. */
export default function ResultSticker({ tier }: { tier: Tier }) {
  const [from, to] = GRADIENT[tier];
  const gid = `result-sticker-${tier}`;

  return (
    <svg viewBox="0 0 88 88" className="h-16 w-16 shrink-0 sm:h-20 sm:w-20" role="presentation" aria-hidden="true">
      <defs>
        <linearGradient id={gid} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor={from} />
          <stop offset="1" stopColor={to} />
        </linearGradient>
      </defs>
      <circle cx="44" cy="44" r="40" fill={`url(#${gid})`} opacity="0.16" />
      <circle cx="44" cy="44" r="32" fill={`url(#${gid})`} opacity="0.22" />

      <g stroke={`url(#${gid})`} strokeWidth="3.2" fill="none" strokeLinecap="round" strokeLinejoin="round">
        {tier === "excellent" && (
          <>
            <path d="M30 28h28v8a14 14 0 0 1-28 0z" />
            <path d="M30 30h-6a6 6 0 0 0 6 10" />
            <path d="M58 30h6a6 6 0 0 1-6 10" />
            <path d="M44 50v8" />
            <path d="M34 64h20" />
            <path d="M38 58h12l2 6H36z" />
          </>
        )}
        {tier === "good" && (
          <path d="M44 20c8 8 12 15 12 22a12 12 0 0 1-24 0c0-4 2-7 5-10 0 4 2 6 4 6-1-6 1-12 3-18z" />
        )}
        {tier === "half" && (
          <>
            <path d="M44 20v8" />
            <path d="M44 60v8" />
            <path d="M26 44h-6" />
            <path d="M68 44h-6" />
            <path d="M31 31l-4-4" />
            <path d="M61 61l-4-4" />
            <path d="M61 31l4-4" />
            <path d="M31 61l-4 4" />
            <circle cx="44" cy="44" r="10" />
          </>
        )}
        {tier === "starting" && (
          <>
            <path d="M44 64V40" />
            <path d="M44 40c0-8-6-14-14-14 0 8 6 14 14 14z" />
            <path d="M44 46c0-7 6-13 13-13 0 7-6 13-13 13z" />
            <path d="M34 64h20" />
          </>
        )}
      </g>
    </svg>
  );
}
