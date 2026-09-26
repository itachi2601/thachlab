"use client";

import Link from "next/link";
import { ChevronRight, Sparkles } from "lucide-react";
import RankBadge from "@/components/rank/RankBadge";
import TierName from "@/components/rank/TierName";
import { formatRp, tierMeta, titleDisplay, type RankStatus } from "@/features/rank/types";

/**
 * Thẻ rank dùng ở nhiều chỗ (trang học sinh, trang kết quả, phụ huynh):
 *   MINH ANH · CAO THỦ
 *   Pháp Sư Điện Trường · Huyền Thoại
 *   2.180 RP · Xem thử thách tiếp theo
 * status = undefined → đang tải; null / không có mùa → trạng thái rõ ràng, không giả số liệu.
 */
export default function RankCard({
  status,
  name,
  href = "/lop-hoc/xep-hang/",
  compact = false,
  className = "",
}: {
  status: RankStatus | null | undefined;
  name?: string;
  /** null = không có link (phụ huynh xem). */
  href?: string | null;
  compact?: boolean;
  className?: string;
}) {
  const paragon = !!status?.tier?.paragon;
  const meta = tierMeta(status?.tier?.code, paragon);
  const inner = (
    <div
      className={`relative overflow-hidden rounded-2xl border p-4 sm:p-5 ${className}`}
      style={{
        borderColor: `${meta.color}55`,
        background: `linear-gradient(135deg, ${meta.color}26 0%, rgba(11,16,32,0) 60%)`,
      }}
    >
      <div className="flex items-center gap-3 sm:gap-4">
        {status === undefined ? (
          <div className="h-16 w-14 animate-pulse rounded-xl bg-white/5" />
        ) : (
          <RankBadge code={status?.tier?.code} division={status?.tier?.division} paragon={paragon} size={compact ? 52 : 64} />
        )}
        <div className="min-w-0 flex-1">
          {status === undefined ? (
            <>
              <div className="h-4 w-40 animate-pulse rounded bg-white/10" />
              <div className="mt-2 h-3 w-28 animate-pulse rounded bg-white/5" />
            </>
          ) : !status?.season ? (
            <>
              <p className="font-display text-base font-bold uppercase tracking-wide text-white">
                {name ? `${name} · ` : ""}Chưa mở mùa
              </p>
              <p className="mt-0.5 text-sm text-slate-400">
                {status?.display_title
                  ? titleDisplay(status.display_title.name, status.display_title.level)
                  : status?.titles_count
                    ? `${status.titles_count} danh hiệu đã sưu tập`
                    : "RP sẽ tính khi giáo viên mở mùa xếp hạng."}
              </p>
            </>
          ) : (
            <>
              {name && <p className="truncate text-xs font-bold uppercase tracking-widest text-slate-400">{name}</p>}
              <TierName code={status.tier?.code} division={status.tier?.division} paragon={paragon} size="md" />
              <p className="mt-0.5 truncate text-sm text-slate-300">
                {status.display_title ? (
                  <>
                    <Sparkles size={13} className="mr-1 inline text-amber-300" />
                    {titleDisplay(status.display_title.name, status.display_title.level)}
                  </>
                ) : (
                  <span className="text-slate-500">Chưa đeo danh hiệu</span>
                )}
              </p>
              {!compact && (
                <p className="mt-1 text-sm text-slate-400">
                  <b className="text-white">{formatRp(status.rp)} RP</b>
                  {paragon && " · Danh vị độc quyền — trên cả Chí Tôn"}
                  {status.next && (
                    <>
                      {" · "}
                      {status.next.rp_needed > 0
                        ? `còn ${formatRp(status.next.rp_needed)} RP tới ${status.next.name}`
                        : status.next.gate && !status.next.gate.passed
                          ? `đủ RP — xem thử thách lên ${status.next.name}`
                          : `sắp lên ${status.next.name}`}
                    </>
                  )}
                </p>
              )}
            </>
          )}
        </div>
        {compact && status?.season && (
          <span className="shrink-0 text-right text-sm text-slate-300">
            <b className="block text-white">{formatRp(status.rp)}</b>RP
          </span>
        )}
        {href && <ChevronRight size={18} className="shrink-0 text-slate-500" />}
      </div>
    </div>
  );

  if (!href) return inner;
  return (
    <Link href={href} className="block transition-transform hover:-translate-y-0.5 motion-reduce:transform-none">
      {inner}
    </Link>
  );
}
