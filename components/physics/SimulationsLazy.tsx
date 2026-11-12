"use client";

import dynamic from "next/dynamic";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của các mô phỏng tự kéo (C1, C2 — content/thi-nghiem/de-xuat-bo-sung-2026-11-12.md mục C).
 * Khối JS mô phỏng chỉ tải phía client (AGENTS.md "Đăng nội dung — tối ưu tốc độ": next/dynamic({ssr:false}) + LazyErrorBoundary).
 * Fallback giữ chiều cao gần bằng mô phỏng thật để không nhảy bố cục.
 */
const loading = () => (
  <p className="min-h-[40vh] rounded-2xl border border-line bg-panel p-6 text-muted">Đang tải mô phỏng…</p>
);
const failed = (
  <p className="min-h-[20vh] rounded-2xl border border-line bg-panel p-6 text-muted">
    Không tải được mô phỏng. Thử tải lại trang.
  </p>
);

const Gas = dynamic(() => import("@/components/physics/GasGraphsSimulation"), { ssr: false, loading });
const Charge = dynamic(() => import("@/components/physics/ChargeInFieldSimulation"), { ssr: false, loading });

export function GasGraphsSimulationLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <Gas />
    </LazyErrorBoundary>
  );
}

export function ChargeInFieldSimulationLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <Charge />
    </LazyErrorBoundary>
  );
}
