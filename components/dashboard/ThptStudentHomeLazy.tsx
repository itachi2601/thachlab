"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của ThptStudentHome — chỉ render sau RequireAuth + sau fetch vai/ghi danh ở app/tai-khoan/page.tsx
 * (đã hydrate xong), nên LazyErrorBoundary bắt được lỗi tải chunk. Tách theo vai để mỗi vai chỉ tải
 * đúng bảng của mình (docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md việc A). Fallback giữ min-height xấp xỉ
 * bảng thật để không nhảy bố cục (QUY-TAC-THIET-KE).
 */
const Inner = dynamic(() => import("@/components/dashboard/ThptStudentHome"), {
  ssr: false,
  loading: () => (
    <p className="rounded-2xl border border-line bg-panel p-6 text-muted min-h-[60vh]">Đang tải bảng học tập…</p>
  ),
});

export default function ThptStudentHomeLazy(props: ComponentProps<typeof Inner>) {
  return (
    <LazyErrorBoundary
      fallback={
        <p className="rounded-2xl border border-line bg-panel p-6 text-muted min-h-[60vh]">
          Không tải được bảng học tập. Thử tải lại trang.
        </p>
      }
    >
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
