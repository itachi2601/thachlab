"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của StudentResultsDashboard (889 dòng, kéo ContentHtml + RankCard + ParentScoreBars +
 * ParentGoal) — dùng ở /phu-huynh, chỉ render sau RequireAuth + sau khi đã tải danh sách con
 * (docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md việc B1), nên LazyErrorBoundary bắt được lỗi tải chunk.
 *
 * Fallback theo QUY-TAC-THIET-KE-PHU-HUYNH: câu đầy đủ (không chỉ spinner), chữ 18px (text-lg), cùng
 * kiểu khung với `Notice` của trang (nền panel, chữ slate-300), min-height giữ chỗ cho khối kết quả
 * để không nhảy bố cục khi chunk về.
 */
const boxClass =
  "flex min-h-[24rem] items-center justify-center rounded-2xl border border-white/10 bg-panel p-8 text-center text-lg leading-relaxed text-slate-300";

const StudentResultsDashboardLazyInner = dynamic(() => import("@/components/results/StudentResultsDashboard"), {
  ssr: false,
  loading: () => <p className={boxClass}>Đang tải kết quả học tập của con…</p>,
});

export default function StudentResultsDashboardLazy(props: ComponentProps<typeof StudentResultsDashboardLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={<p className={boxClass}>Chưa tải được kết quả học tập của con. Phụ huynh vui lòng tải lại trang.</p>}
    >
      <StudentResultsDashboardLazyInner {...props} />
    </LazyErrorBoundary>
  );
}
