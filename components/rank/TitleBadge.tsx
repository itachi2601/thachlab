"use client";

import Image from "next/image";
import { titleBadgeDisplaySrc } from "@/features/rank/badge-assets";
import type { TitleLevel } from "@/features/rank/types";

/**
 * Logo một danh hiệu (huy hiệu lục giác). Có ảnh → webp 512px trong public/images/rank; chưa có ảnh (bộ sưu tập,
 * thành tích chưa vẽ) → ô lục giác vàng có sao. `locked` làm mờ + xám (dùng ở bộ sưu tập đầy đủ).
 */
export default function TitleBadge({
  code,
  level,
  size = 32,
  locked = false,
  className = "",
  title,
}: {
  code: string;
  level: TitleLevel | string | null | undefined;
  size?: number;
  locked?: boolean;
  className?: string;
  title?: string;
}) {
  const src = titleBadgeDisplaySrc(code, level);
  const lockCls = locked ? "opacity-30 grayscale" : "";
  if (src) {
    return (
      <Image
        src={src}
        alt=""
        title={title}
        width={size}
        height={size}
        draggable={false}
        className={`inline-block shrink-0 select-none ${lockCls} ${className}`}
        style={{ width: size, height: size }}
      />
    );
  }
  return (
    <span
      title={title}
      aria-hidden
      className={`inline-grid shrink-0 select-none place-items-center font-bold text-[#2a1f05] ${lockCls} ${className}`}
      style={{
        width: size,
        height: size,
        fontSize: Math.round(size * 0.42),
        clipPath: "polygon(50% 0, 93% 25%, 93% 75%, 50% 100%, 7% 75%, 7% 25%)",
        background: "linear-gradient(160deg, #fff3cf, #b58a17)",
      }}
    >
      ★
    </span>
  );
}
