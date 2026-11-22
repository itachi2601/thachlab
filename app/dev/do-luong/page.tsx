"use client";

import { DongHoDaNangLazy, DongHoHienSoLazy, PanmeLazy, ThuocKepLazy } from "@/components/physics/SimulationsLazy";

/**
 * XEM THỬ dụng cụ đo tương tác (Gói A, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 3). Mở http://localhost:3000/dev/do-luong
 * Component: components/physics/do-luong/*. Gắn vào bài qua hộp `.tl-mo-phong[data-mo-phong]` (MoPhongPortals).
 */
export default function DoLuongDevPage() {
  return (
    <main className="mx-auto min-h-screen max-w-2xl space-y-6 bg-bg px-4 py-6">
      <h1 className="font-display text-xl font-bold text-ink">Xem thử: dụng cụ đo</h1>
      <ThuocKepLazy />
      <PanmeLazy />
      <DongHoDaNangLazy />
      <DongHoHienSoLazy />
    </main>
  );
}
