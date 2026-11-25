"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { RotateCcw } from "lucide-react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import { BO_ON_TAP, ON_TAP_THEO_BAI } from "@/content/on-tap";
import type { BoOnTap } from "@/components/lessons/OnNamPhut";
import { flashTheorySection } from "@/app/lop-hoc/bai/_parts/lesson-nav";
import s from "./OnNamPhut.module.css";

// Chunk riêng: chỉ nạp khi HS bấm "Bắt đầu" — không đụng tải ban đầu của /lop-hoc/bai.
const OnNamPhut = dynamic(() => import("@/components/lessons/OnNamPhut"), { ssr: false });

/**
 * "Ôn 5 phút" thu gọn ở cuối mục Lý thuyết, trước Bài tập mẫu (thầy chốt 25/11/2026).
 * Truy xuất ngay sau khi đọc (L1), đúng mạch học — không tab riêng (N2), không huy hiệu/RP (L3, G2),
 * một dòng nhẹ chứ không banner (B2). Bài không có bộ thẻ thì không hiện gì (N3).
 */
export default function OnNamPhutGon({
  lessonId,
  theoryHtml,
  theoryItemId,
}: {
  lessonId: number;
  theoryHtml?: string;
  theoryItemId: number;
}) {
  const info = ON_TAP_THEO_BAI[lessonId];
  const [bo, setBo] = useState<BoOnTap | null>(null);
  const [mo, setMo] = useState(false);
  const [loi, setLoi] = useState(false);
  if (!info || info.so_the === 0) return null;

  const batDau = () => {
    setMo(true);
    setLoi(false);
    BO_ON_TAP[info.slug]?.()
      .then(setBo)
      .catch(() => setLoi(true));
  };

  if (!mo)
    return (
      <div className={s.gon}>
        <RotateCcw size={18} className={s.gonIcon} aria-hidden />
        <span className={s.gonText}>
          <strong>Ôn 5 phút</strong> · {info.so_the} thẻ
        </span>
        <button type="button" className={s.gonBtn} onClick={batDau}>
          Bắt đầu
        </button>
      </div>
    );

  const fallback = (
    <p className={s.gon}>
      Chưa tải được thẻ ôn.{" "}
      <button type="button" className={s.gonBtn} onClick={batDau}>
        Thử lại
      </button>
    </p>
  );
  if (loi) return fallback;
  if (!bo) return <p className={s.gon}>Đang tải thẻ…</p>;
  return (
    <div className={s.gonMo}>
      <LazyErrorBoundary fallback={fallback}>
        <OnNamPhut
          bo={bo}
          vaoNgay
          theoryHtml={theoryHtml}
          theoryItemId={theoryItemId}
          onOnNgay={(id, tieuMuc) => {
            flashTheorySection(id);
            void import("@/components/lessons/OnNamPhut").then((m) => m.cuonToiTieuMuc(id, tieuMuc));
          }}
        />
      </LazyErrorBoundary>
    </div>
  );
}
