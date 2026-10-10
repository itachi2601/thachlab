"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của PracticeSession (mục "Luyện tập") — kéo theo QuestionCard + logic bốc câu/chấm/
 * lưu phiên. Mục này chỉ MOUNT khi học sinh bấm mở (app/lop-hoc/bai/page.tsx `{isOpen && (...)}`),
 * nên tách JS ra khỏi bundle ban đầu của trang không đổi trải nghiệm chính, chỉ chớp loading ngắn
 * lần đầu mở mục (đợt tách JS 6/10/2026, docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md việc C).
 *
 * `loading`/fallback giữ min-height xấp xỉ màn chọn số câu của PracticeSession để mục không nhảy
 * bố cục khi chunk về (QUY-TAC-THIET-KE: fallback không được làm nhảy bố cục).
 *
 * LazyErrorBoundary: nếu chunk lỗi (mạng chập chờn, vừa deploy bản mới), chỉ đúng mục Luyện tập
 * báo lỗi, không kéo sập cả trang bài học đang xem dở (không có app/error.tsx bọc route này).
 * `onActiveChange` vẫn truyền thẳng xuống — practiceActiveRef chỉ bật sau khi chunk mount.
 */
const PracticeSessionLazyInner = dynamic(() => import("@/components/lessons/PracticeSession"), {
  ssr: false,
  loading: () => <p className="min-h-[12rem] text-sm text-muted">Đang tải phần luyện tập…</p>,
});

function PracticeSessionLazy(props: ComponentProps<typeof PracticeSessionLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={
        <p className="min-h-[12rem] text-sm text-muted">
          Không tải được phần luyện tập. Thử tải lại trang.
        </p>
      }
    >
      <PracticeSessionLazyInner {...props} />
    </LazyErrorBoundary>
  );
}

export default PracticeSessionLazy;
