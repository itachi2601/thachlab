"use client";

import { Sparkles } from "lucide-react";
import TitleBadge from "@/components/rank/TitleBadge";
import { levelThemedColor } from "@/features/rank/badge-assets";
import { LEVEL_LABELS, type TitleLevel } from "@/features/rank/types";

/**
 * Danh hiệu đang đeo, hiện dưới tên học sinh: logo nhỏ + tên + mức, màu chữ theo mức.
 * Dùng chung cho khung chào trang HS, thẻ rank, trang xếp hạng, chip bạn cùng lớp, top tuần.
 * Không có `code` (RPC cũ chỉ trả tên) → icon Sparkles thay logo. title null → không render gì.
 */
export default function WornTitle({
  title,
  size = "sm",
  className = "",
}: {
  title: { code?: string | null; name: string; level: TitleLevel | string | null } | null | undefined;
  size?: "sm" | "md";
  className?: string;
}) {
  if (!title) return null;
  const lv = (title.level ?? null) as TitleLevel | null;
  const lvLabel = lv ? LEVEL_LABELS[lv] : "";
  const color = levelThemedColor(lv);
  const icon = size === "md" ? 20 : 14;
  return (
    <span
      className={`inline-flex min-w-0 max-w-full items-center gap-1 font-semibold ${size === "md" ? "text-sm" : "text-[12px]"} ${className}`}
      style={{ color }}
    >
      {title.code ? <TitleBadge code={title.code} level={lv} size={icon} /> : <Sparkles size={icon - 2} className="shrink-0 opacity-80" />}
      <span className="truncate">
        {title.name}
        {lvLabel && <span className="font-medium opacity-75"> · {lvLabel}</span>}
      </span>
    </span>
  );
}
