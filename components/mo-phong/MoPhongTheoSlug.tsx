"use client";

import dynamic from "next/dynamic";
import type { ComponentType } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Nạp lười mô phỏng cho trang /mo-phong/<slug> (Gói B). Riêng file này, KHÔNG sửa SimulationsLazy.tsx.
 * Thêm dụng cụ đo của Gói A: thêm một dòng vào MAP bên dưới (khoá = slug trong lib/mo-phong-trang.ts).
 */
const loading = () => <p className="min-h-[40vh] rounded-2xl border border-line bg-panel p-6 text-muted">Đang tải mô phỏng…</p>;
const failed = (
  <p className="min-h-[20vh] rounded-2xl border border-line bg-panel p-6 text-muted">Không tải được mô phỏng. Thử tải lại trang.</p>
);

const MAP: Record<string, ComponentType> = {
  "khi-ly-tuong": dynamic(() => import("@/components/physics/GasGraphsSimulation"), { ssr: false, loading }),
  "hat-trong-tu-truong": dynamic(() => import("@/components/physics/ChargeInFieldSimulation"), { ssr: false, loading }),
  "can-dong-dien": dynamic(() => import("@/components/physics/CurrentBalanceSimulation"), { ssr: false, loading }),
  "nem-xien": dynamic(() => import("@/components/physics/ProjectileSimulation").then((m) => m.ProjectileSimulation), { ssr: false, loading }),
  "giao-thoa-song": dynamic(() => import("@/components/physics/InterferenceSimulation").then((m) => m.InterferenceSimulation), { ssr: false, loading }),
  "thuoc-kep": dynamic(() => import("@/components/physics/do-luong/ThuocKep"), { ssr: false, loading }),
  panme: dynamic(() => import("@/components/physics/do-luong/Panme"), { ssr: false, loading }),
  "dong-ho-da-nang": dynamic(() => import("@/components/physics/do-luong/DongHoDaNang"), { ssr: false, loading }),
  "dong-ho-hien-so": dynamic(() => import("@/components/physics/do-luong/DongHoHienSo"), { ssr: false, loading }),
};

export default function MoPhongTheoSlug({ slug }: { slug: string }) {
  const C = MAP[slug];
  if (!C) return null;
  return (
    <LazyErrorBoundary fallback={failed}>
      <C />
    </LazyErrorBoundary>
  );
}
