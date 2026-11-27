"use client";

import {
  GcptAnMonLazy,
  GcptEcmLazy,
  GcptEdmLazy,
  GcptLaserLazy,
  GcptSieuAmLazy,
  GcptTiaNuocLazy,
  GcptWedmLazy,
} from "@/components/physics/SimulationsLazy";

/**
 * XEM THỬ 7 mô phỏng môn Gia công phi truyền thống (lớp CTTC `gcpt`, 27/11/2026). Mở http://localhost:3000/dev/mo-phong-gcpt
 * Component: components/physics/gcpt/*. Đã gắn vào bài bằng hộp `.tl-mo-phong[data-mo-phong="gcpt-…"]`
 * (components/lessons/MoPhongPortals.tsx): Bài 2 EDM, 3 WEDM, 4 ECM, 5 laser, 6 tia nước, 7 siêu âm, 9 hoá học.
 */
export default function MoPhongGcptDevPage() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl space-y-6 bg-bg px-4 py-6">
      <h1 className="font-display text-xl font-bold text-ink">Xem thử: mô phỏng gia công phi truyền thống</h1>
      <GcptEdmLazy />
      <GcptWedmLazy />
      <GcptEcmLazy />
      <GcptLaserLazy />
      <GcptTiaNuocLazy />
      <GcptSieuAmLazy />
      <GcptAnMonLazy />
    </main>
  );
}
