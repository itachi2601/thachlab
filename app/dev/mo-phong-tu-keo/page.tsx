"use client";

import { ChargeInFieldSimulationLazy, GasGraphsSimulationLazy } from "@/components/physics/SimulationsLazy";

/**
 * XEM THỬ hai mô phỏng tự kéo C1, C2 (12/11/2026). Mở http://localhost:3000/dev/mo-phong-tu-keo
 * Đề xuất: content/thi-nghiem/de-xuat-bo-sung-2026-11-12.md mục C.
 * Component: components/physics/GasGraphsSimulation.tsx (L12 bài 6–7), ChargeInFieldSimulation.tsx (L12 bài 10).
 * Chưa gắn vào bài học thật; thầy duyệt rồi mới quyết chỗ đặt.
 */
export default function MoPhongTuKeoDevPage() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl space-y-6 bg-bg px-4 py-6">
      <h1 className="font-display text-xl font-bold text-ink">Xem thử: mô phỏng tự kéo C1, C2</h1>
      <GasGraphsSimulationLazy />
      <ChargeInFieldSimulationLazy />
    </main>
  );
}
