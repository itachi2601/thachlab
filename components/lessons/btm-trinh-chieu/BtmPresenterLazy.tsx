"use client";

import dynamic from "next/dynamic";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

/**
 * Bản tải-chậm của trình chiếu bài tập mẫu — chỉ tải khi thầy bấm "Trình chiếu" ở một dạng (quy tắc AGENTS.md: khối JS
 * mới ở trang học sinh tách bằng next/dynamic({ssr:false}) + LazyErrorBoundary). Học sinh không bao giờ tải chunk này.
 */
const Inner = dynamic(() => import("./BtmPresenterTuDang"), {
  ssr: false,
  loading: () => (
    <div className="lesson-presenter-loading" role="status">
      Đang mở trình chiếu bài tập mẫu…
    </div>
  ),
});

export default function BtmPresenterLazy(props: { questions: LessonWorkedQuestion[]; start: number; title?: string; lessonId?: number; itemId?: number; onClose: () => void }) {
  return (
    <LazyErrorBoundary
      fallback={
        <div className="lesson-presenter-loading is-error" role="alert">
          Không mở được trình chiếu. Thử tải lại trang rồi bấm lại.
        </div>
      }
    >
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
