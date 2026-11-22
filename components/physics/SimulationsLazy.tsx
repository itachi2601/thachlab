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
const CurrentBalance = dynamic(() => import("@/components/physics/CurrentBalanceSimulation"), { ssr: false, loading });

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

export function CurrentBalanceSimulationLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <CurrentBalance />
    </LazyErrorBoundary>
  );
}

/* ---- Dụng cụ đo (Gói A, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3) ---- */
const ThuocKep = dynamic(() => import("@/components/physics/do-luong/ThuocKep"), { ssr: false, loading });

export function ThuocKepLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <ThuocKep />
    </LazyErrorBoundary>
  );
}

const Panme = dynamic(() => import("@/components/physics/do-luong/Panme"), { ssr: false, loading });

export function PanmeLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <Panme />
    </LazyErrorBoundary>
  );
}

const DongHoDaNang = dynamic(() => import("@/components/physics/do-luong/DongHoDaNang"), { ssr: false, loading });

export function DongHoDaNangLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <DongHoDaNang />
    </LazyErrorBoundary>
  );
}

const DongHoHienSo = dynamic(() => import("@/components/physics/do-luong/DongHoHienSo"), { ssr: false, loading });

export function DongHoHienSoLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <DongHoHienSo />
    </LazyErrorBoundary>
  );
}

const ThucHanhRoiTuDo = dynamic(() => import("@/components/physics/thuc-hanh/ThucHanhRoiTuDo"), { ssr: false, loading });

export function ThucHanhRoiTuDoLazy() {
  return (
    <LazyErrorBoundary fallback={failed}>
      <ThucHanhRoiTuDo />
    </LazyErrorBoundary>
  );
}
