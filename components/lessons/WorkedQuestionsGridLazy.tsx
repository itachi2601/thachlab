"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của WorkedQuestionsGrid (tab "Bài mẫu" của /lop-hoc/bai) — kéo theo GiaiCungHinh,
 * StepwiseSolution, VariantPractice, SimilarBankPractice; tab chỉ mount khi học sinh bấm mở (tab mặc định là
 * Lý thuyết) nên tách khỏi JS ban đầu của trang không đổi trải nghiệm chính. KaTeX vẫn nạp đồng bộ qua
 * ContentHtml ở trang (không nằm trong chunk này). Rà soát website 18/11/2026, đợt 3.
 */
const WorkedQuestionsGridLazyInner = dynamic(() => import("@/components/lessons/WorkedQuestionsGrid"), {
  ssr: false,
  loading: () => <p className="text-sm text-muted">Đang tải bài tập mẫu…</p>,
});

// Chunk lỗi (mạng chập chờn, vừa deploy bản mới) chỉ làm hỏng đúng mục này, không kéo sập trang bài đang xem dở.
function WorkedQuestionsGridLazy(props: ComponentProps<typeof WorkedQuestionsGridLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={<p className="text-sm text-muted">Không tải được bài tập mẫu. Thử tải lại trang.</p>}
    >
      <WorkedQuestionsGridLazyInner {...props} />
    </LazyErrorBoundary>
  );
}

export default WorkedQuestionsGridLazy;
