"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của HomeroomStudentHome — chỉ render sau RequireAuth + sau fetch vai/ghi danh ở app/tai-khoan/page.tsx
 * (đã hydrate xong), nên LazyErrorBoundary bắt được lỗi tải chunk. Tách theo vai để mỗi vai chỉ tải
 * đúng bảng của mình (docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md việc A). Fallback giữ min-height xấp xỉ
 * bảng thật để không nhảy bố cục (QUY-TAC-THIET-KE).
 */
const Inner = dynamic(() => import("@/components/dashboard/HomeroomStudentHome"), {
  ssr: false,
  loading: () => (
    <p className="rounded-2xl border border-white/10 bg-panel p-6 text-slate-400 min-h-[40vh]">Đang tải lớp chủ nhiệm…</p>
  ),
});

export default function HomeroomStudentHomeLazy(props: ComponentProps<typeof Inner>) {
  return (
    <LazyErrorBoundary
      fallback={
        <p className="rounded-2xl border border-white/10 bg-panel p-6 text-slate-400 min-h-[40vh]">
          Không tải được lớp chủ nhiệm. Thử tải lại trang.
        </p>
      }
    >
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
