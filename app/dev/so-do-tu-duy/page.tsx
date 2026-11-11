"use client";

import SoDoTuDuy from "@/components/lessons/so-do/SoDoTuDuy";
import { L12_CHUONG_3 } from "@/features/lessons/so-do-tu-duy/l12-chuong-3";

/**
 * XEM THỬ SƠ ĐỒ TƯ DUY CHƯƠNG — mẫu đầu: Vật lí 12, Chương 3 (11/11/2026). Mở http://localhost:3000/dev/so-do-tu-duy
 * Dữ liệu: features/lessons/so-do-tu-duy/l12-chuong-3.ts · Component: components/lessons/so-do/SoDoTuDuy.tsx
 * Chưa gắn vào trang lớp học; thầy duyệt mẫu rồi mới quyết chỗ đặt.
 */
export default function SoDoTuDuyDevPage() {
  return (
    <main className="min-h-screen bg-bg">
      <SoDoTuDuy data={L12_CHUONG_3} />
    </main>
  );
}
