"use client";

import { useMemo } from "react";
import { makeQrCode, QR_QUIET_ZONE } from "@/lib/qr";

/** Mã QR nền trắng, chữ đen (máy ảnh chỉ đọc chắc trên nền sáng) — dùng chung cho màn hình chiếu của buổi ôn. */
export default function QrBox({ text, label, className = "size-64" }: { text: string; label: string; className?: string }) {
  const { d, count } = useMemo(() => makeQrCode(text), [text]);
  const box = count + QR_QUIET_ZONE * 2;
  return (
    <svg
      viewBox={`${-QR_QUIET_ZONE} ${-QR_QUIET_ZONE} ${box} ${box}`}
      className={`block rounded-2xl border border-line ${className}`}
      shapeRendering="crispEdges"
      role="img"
      aria-label={label}
    >
      <rect x={-QR_QUIET_ZONE} y={-QR_QUIET_ZONE} width={box} height={box} fill="#ffffff" />
      <path d={d} fill="#000000" />
    </svg>
  );
}
