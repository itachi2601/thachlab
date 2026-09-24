"use client";

import { useState } from "react";

/** Ảnh đại diện tròn — rơi về chữ cái đầu tên (giống các badge chữ cái sẵn có) khi chưa có/lỗi ảnh. */
export default function Avatar({
  url,
  name,
  size = 40,
  className = "",
}: {
  url?: string | null;
  name?: string | null;
  size?: number;
  className?: string;
}) {
  const [failed, setFailed] = useState(false);
  const initial = (name ?? "?").trim().charAt(0).toUpperCase() || "?";

  if (url && !failed) {
    return (
      // eslint-disable-next-line @next/next/no-img-element -- ảnh do người dùng upload, không thuộc bộ ảnh tĩnh next/image tối ưu được
      <img
        src={url}
        alt={name ?? "Ảnh đại diện"}
        onError={() => setFailed(true)}
        className={`shrink-0 rounded-full object-cover ${className}`}
        style={{ width: size, height: size }}
      />
    );
  }

  return (
    <span
      className={`flex shrink-0 items-center justify-center rounded-full bg-primary/15 font-bold text-[#3B82F6] ${className}`}
      style={{ width: size, height: size, fontSize: size * 0.42 }}
    >
      {initial}
    </span>
  );
}
