"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { MAU_ONG_THUY_NGAN } from "@/features/lessons/btm-trinh-chieu/mau-ong-thuy-ngan";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

// Như trang bài học: trình chiếu chỉ chạy phía client (đọc localStorage, DOMParser).
const BtmPresenter = dynamic(() => import("@/components/lessons/btm-trinh-chieu/BtmPresenter"), { ssr: false });
const BtmPresenterTuDang = dynamic(() => import("@/components/lessons/btm-trinh-chieu/BtmPresenterTuDang"), { ssr: false });

/**
 * XEM THỬ TRÌNH CHIẾU BÀI TẬP MẪU (17/11/2026) — http://localhost:3000/dev/btm-trinh-chieu
 *   (không tham số)  → mẫu soạn tay: ống thuỷ ngân 157 °C (bảng trạng thái ①②, hình tự vẽ)
 *   ?f=btm           → dựng tự động từ scripts/data/bai-tap-mau/<N>.json qua public/xem-thu/btm.json (chạy
 *                      `npx tsx scripts/publish-bai-tap-mau.mts --lesson N --xem-thu` trước) — đúng như trên trang bài học
 * Phím: → / Space / PageDown tiếp · ← lùi · 1–9 nhảy bước · [ ] đổi dạng · F toàn màn · B nền sáng/tối · Esc thoát.
 */
export default function BtmTrinhChieuDevPage() {
  const [data, setData] = useState<{ questions: LessonWorkedQuestion[]; lesson_title?: string } | null>(null);
  const [f, setF] = useState<string | null>(null);
  useEffect(() => {
    const v = new URLSearchParams(location.search).get("f");
    if (!v || !/^[\w-]+$/.test(v)) return;
    fetch(`/xem-thu/${v}.json`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((j) => {
        setF(v);
        setData(j);
      })
      .catch(() => {
        setF(v);
        setData({ questions: [] });
      });
  }, []);
  if (f) return data ? <BtmPresenterTuDang questions={data.questions} start={0} title={data.lesson_title} onClose={() => history.back()} /> : null;
  return <BtmPresenter bais={[MAU_ONG_THUY_NGAN]} title="Mẫu soạn tay" />;
}
