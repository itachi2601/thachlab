"use client";

import {
  ChargeInFieldSimulationLazy,
  CurrentBalanceSimulationLazy,
  GasGraphsSimulationLazy,
} from "@/components/physics/SimulationsLazy";

/**
 * XEM THỬ hai mô phỏng tự kéo C1, C2 (12/11/2026). Mở http://localhost:3000/dev/mo-phong-tu-keo
 * Đề xuất: content/thi-nghiem/de-xuat-bo-sung-2026-11-12.md mục C.
 * Component: components/physics/GasGraphsSimulation.tsx (L12 bài 6–7), ChargeInFieldSimulation.tsx (L12 bài 10).
 * Đã gắn vào bài (14/11/2026): hộp `.tl-mo-phong[data-mo-phong]` → components/lessons/MoPhongPortals.tsx —
 * Thêm 19/11/2026 (việc 5, docs/KE-HOACH-CAI-TIEN-CLIP-2026-11-19.md): can-dong-dien — CurrentBalanceSimulation.tsx, sau clip
 * thuchanhtu4 ở L12 Bài 11 (lesson 12), chờ thầy duyệt rồi mới đăng.
 * do-thi-khi ở Bẫy 3 bài Boyle–Charles (lesson 7) và PT trạng thái (lesson 8); dien-tich-tu-truong sau clip luctu5 bài Lực từ (lesson 11).
 */
export default function MoPhongTuKeoDevPage() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl space-y-6 bg-bg px-4 py-6">
      <h1 className="font-display text-xl font-bold text-ink">Xem thử: mô phỏng tự kéo</h1>
      <CurrentBalanceSimulationLazy />
      <GasGraphsSimulationLazy />
      <ChargeInFieldSimulationLazy />
    </main>
  );
}
