"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import TitleBadge from "@/components/rank/TitleBadge";
import { levelTextColor } from "@/features/rank/badge-assets";
import { LEVEL_LABELS, levelRank, type RankTitle, type TitleLevel } from "@/features/rank/types";

/**
 * Khung sưu tập huy hiệu cạnh thẻ rank: chỉ danh hiệu ĐÃ MỞ, mỗi cái một ô logo (ảnh của mức cao nhất),
 * danh hiệu đang đeo có vành vàng. Quá `limit` ô thì gộp "+N". Chạm một ô để xem tên + mức (điện thoại
 * không có hover). Chưa mở gì → một dòng gợi ý, không vẽ ô khoá cho khỏi trống trải.
 */
export default function TitleShowcase({
  titles,
  displayCode,
  href = "/lop-hoc/xep-hang/",
  limit = 15,
  size = 36,
  className = "",
}: {
  /** undefined = đang tải. */
  titles: RankTitle[] | null | undefined;
  displayCode: string | null | undefined;
  href?: string | null;
  limit?: number;
  size?: number;
  className?: string;
}) {
  const [picked, setPicked] = useState<string | null>(null);

  const { owned, total } = useMemo(() => {
    const list = titles ?? [];
    const awardedAt = (t: RankTitle) => Math.max(0, ...Object.values(t.levels).map((d) => (d ? new Date(d).getTime() : 0)));
    const o = list
      .filter((t) => t.level)
      .sort((a, b) => {
        const wa = a.code === displayCode ? 1 : 0;
        const wb = b.code === displayCode ? 1 : 0;
        if (wa !== wb) return wb - wa;
        const r = levelRank(b.level) - levelRank(a.level);
        if (r !== 0) return r;
        return awardedAt(b) - awardedAt(a);
      });
    return { owned: o, total: list.filter((t) => t.visible).length };
  }, [titles, displayCode]);

  const pickedTitle = picked ? owned.find((t) => t.code === picked) ?? null : null;
  const shown = owned.length > limit ? owned.slice(0, limit - 1) : owned;
  const extra = owned.length - shown.length;

  return (
    <section className={`rounded-2xl border border-amber-400/25 bg-amber-400/5 p-3 sm:p-4 ${className}`}>
      <div className="mb-2 flex items-baseline justify-between gap-2">
        <h3 className="font-display text-sm font-semibold text-white sm:text-base">Huy hiệu đã sưu tập</h3>
        {titles === undefined ? (
          <span className="h-3 w-16 animate-pulse rounded bg-white/10" />
        ) : (
          <span className="text-xs text-slate-500">
            {owned.length}/{total}
            {href && (
              <>
                {" · "}
                <Link href={href} className="text-cyan-300 hover:underline">
                  xem tất cả →
                </Link>
              </>
            )}
          </span>
        )}
      </div>

      {titles === undefined ? (
        <div className="flex gap-1.5">
          {[0, 1, 2, 3, 4].map((i) => (
            <span key={i} className="animate-pulse rounded-xl bg-white/5" style={{ width: size + 4, height: size + 4 }} />
          ))}
        </div>
      ) : owned.length === 0 ? (
        <p className="text-xs text-slate-400">Chưa có huy hiệu nào — làm bài luyện tập có gắn chủ đề để mở danh hiệu đầu tiên.</p>
      ) : (
        <>
          <ul className="flex flex-wrap gap-1.5">
            {shown.map((t) => {
              const wearing = t.code === displayCode;
              const active = picked === t.code;
              const label = t.level && t.level !== "don" ? `${t.name} · ${LEVEL_LABELS[t.level as TitleLevel]}` : t.name;
              return (
                <li key={t.code} className="relative">
                  <button
                    type="button"
                    aria-label={label}
                    aria-pressed={active}
                    onClick={() => setPicked((p) => (p === t.code ? null : t.code))}
                    className={`grid place-items-center rounded-xl transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-300 ${
                      wearing ? "bg-amber-400/15 ring-2 ring-amber-400 shadow-[0_0_12px_rgba(226,185,59,.5)]" : active ? "bg-white/10" : "bg-white/[0.03] hover:bg-white/[0.07]"
                    }`}
                    style={{ width: size + 4, height: size + 4 }}
                  >
                    <TitleBadge code={t.code} level={t.level} size={size} />
                  </button>
                  {wearing && (
                    <span className="pointer-events-none absolute -bottom-1.5 left-1/2 -translate-x-1/2 rounded-full bg-amber-400 px-1.5 text-[12px] font-bold leading-[13px] text-[#2a1f05]">
                      đeo
                    </span>
                  )}
                </li>
              );
            })}
            {extra > 0 && (
              <li>
                {href ? (
                  <Link
                    href={href}
                    className="grid place-items-center rounded-xl border border-dashed border-white/15 text-xs font-bold text-slate-400 hover:text-white"
                    style={{ width: size + 4, height: size + 4 }}
                  >
                    +{extra}
                  </Link>
                ) : (
                  <span className="grid place-items-center rounded-xl border border-dashed border-white/15 text-xs font-bold text-slate-400" style={{ width: size + 4, height: size + 4 }}>
                    +{extra}
                  </span>
                )}
              </li>
            )}
          </ul>
          <p className="mt-2 min-h-[16px] text-xs" style={{ color: pickedTitle ? levelTextColor(pickedTitle.level) : undefined }}>
            {pickedTitle ? (
              <>
                <b>{pickedTitle.name}</b>
                {pickedTitle.level && pickedTitle.level !== "don" && <> · {LEVEL_LABELS[pickedTitle.level as TitleLevel]}</>}
                {pickedTitle.code === displayCode && <span className="text-slate-500"> · đang đeo</span>}
              </>
            ) : (
              <span className="text-slate-600">Chạm một huy hiệu để xem tên</span>
            )}
          </p>
        </>
      )}
    </section>
  );
}
