"use client";

import {
  ThucHanhDongLuongLazy,
  ThucHanhRoiTuDoLazy,
  ThucHanhTocDoLazy,
  ThucHanhTongHopLucLazy,
} from "@/components/physics/SimulationsLazy";

/**
 * XEM THỬ thí nghiệm ảo theo bộ thiết bị SGK (Gói C, docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5).
 * Mở http://localhost:3000/dev/thuc-hanh. Component: components/physics/thuc-hanh/*. Đã gắn vào bài 51, 56, 67, 75 qua MoPhongPortals.
 */
export default function ThucHanhDevPage() {
  return (
    <main className="mx-auto min-h-screen max-w-2xl space-y-6 bg-bg px-4 py-6">
      <h1 className="font-display text-xl font-bold text-ink">Xem thử: thí nghiệm ảo (L10 Bài 6, 11, 22, 30)</h1>
      <ThucHanhTocDoLazy />
      <ThucHanhRoiTuDoLazy />
      <ThucHanhTongHopLucLazy />
      <ThucHanhDongLuongLazy />
    </main>
  );
}
