"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của VideoThiNghiemKhung (quy tắc tối ưu tốc độ trong AGENTS.md: khối JS mới ở trang học sinh
 * tách bằng next/dynamic({ssr:false}) + LazyErrorBoundary). Chunk chỉ được tải khi bài có hộp `data-khung`.
 * Tải lỗi thì không hiện gì: hộp video tĩnh trong HTML bài vẫn còn nguyên (khung chỉ ẩn nó SAU khi mount xong).
 */
const Inner = dynamic(() => import("@/components/lessons/VideoThiNghiemKhung"), { ssr: false });

export default function VideoKhungLazy(props: ComponentProps<typeof Inner>) {
  return (
    <LazyErrorBoundary fallback={null}>
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
