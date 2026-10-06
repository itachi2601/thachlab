"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của ParentChildCards (lịch sắp tới, điểm danh, ghi chú bài tập, học bù, xếp hạng) —
 * chỉ render bên trong StudentResultsDashboard (đã lazy, sau RequireAuth + sau khi tải danh sách con)
 * nên LazyErrorBoundary bắt được lỗi tải chunk (docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md việc B2).
 * Fallback theo QUY-TAC-THIET-KE-PHU-HUYNH: câu đầy đủ, chữ 18px, min-height giữ chỗ.
 */
const boxClass =
  "flex min-h-[12rem] items-center justify-center rounded-2xl border border-white/10 bg-panel p-8 text-center text-lg leading-relaxed text-slate-300";

const ParentChildCardsLazyInner = dynamic(() => import("@/components/parent/ParentChildCards"), {
  ssr: false,
  loading: () => <p className={boxClass}>Đang tải lịch học và điểm danh của con…</p>,
});

export default function ParentChildCardsLazy(props: ComponentProps<typeof ParentChildCardsLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={<p className={boxClass}>Chưa tải được lịch học và điểm danh của con. Phụ huynh vui lòng tải lại trang.</p>}
    >
      <ParentChildCardsLazyInner {...props} />
    </LazyErrorBoundary>
  );
}
