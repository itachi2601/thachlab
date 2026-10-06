"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của StudentAttendancePanel — chỉ render sau RequireAuth + sau fetch vai/ghi danh ở app/tai-khoan/page.tsx
 * (đã hydrate xong), nên LazyErrorBoundary bắt được lỗi tải chunk. Tách theo vai để mỗi vai chỉ tải
 * đúng bảng của mình (docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md việc A). Fallback giữ min-height xấp xỉ
 * bảng thật để không nhảy bố cục (QUY-TAC-THIET-KE).
 */
const Inner = dynamic(() => import("@/components/attendance/StudentAttendancePanel"), {
  ssr: false,
  loading: () => (
    <p className="rounded-2xl border border-white/10 bg-panel p-6 text-slate-400 min-h-[30vh]">Đang tải điểm danh…</p>
  ),
});

export default function StudentAttendancePanelLazy(props: ComponentProps<typeof Inner>) {
  return (
    <LazyErrorBoundary
      fallback={
        <p className="rounded-2xl border border-white/10 bg-panel p-6 text-slate-400 min-h-[30vh]">
          Không tải được điểm danh. Thử tải lại trang.
        </p>
      }
    >
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
