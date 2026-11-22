"use client";

import { ThucHanhRoiTuDoLazy } from "@/components/physics/SimulationsLazy";

/**
 * XEM THỬ thí nghiệm ảo theo bộ thiết bị SGK (Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5).
 * Mở http://localhost:3000/dev/thuc-hanh. Component: components/physics/thuc-hanh/*. Chưa gắn vào bài (chờ thầy duyệt).
 */
export default function ThucHanhDevPage() {
  return (
    <main className="mx-auto min-h-screen max-w-2xl space-y-6 bg-bg px-4 py-6">
      <h1 className="font-display text-xl font-bold text-ink">Xem thử: thí nghiệm ảo (L10 Bài 11)</h1>
      <ThucHanhRoiTuDoLazy />
    </main>
  );
}
