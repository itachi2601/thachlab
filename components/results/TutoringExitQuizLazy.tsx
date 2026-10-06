"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của TutoringExitQuiz — bài tự kiểm tra thoát phụ đạo, chỉ mount khi học sinh bấm
 * nút mở (ThptStudentHome `{quizNeed && ...}`) và kéo theo framer-motion (~139 KB) vốn nằm trong JS
 * đầu của /tai-khoan (docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md việc A2).
 *
 * Cả `loading` lẫn fallback dùng cùng lớp phủ toàn màn hình của modal thật, để bấm nút xong có phản
 * hồi ngay (không im lặng) và không nhảy bố cục. Fallback có nút "Đóng" (onClose sẵn có) như mẫu
 * TopicPracticeModal trong LessonMasteryCard.
 */
const TutoringExitQuizLazyInner = dynamic(() => import("@/components/results/TutoringExitQuiz"), {
  ssr: false,
  loading: () => (
    <div role="status" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <p className="rounded-2xl border border-white/10 bg-panel px-5 py-4 text-sm text-slate-300">
        Đang tải bài tự kiểm tra…
      </p>
    </div>
  ),
});

export default function TutoringExitQuizLazy(props: ComponentProps<typeof TutoringExitQuizLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div role="alertdialog" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="max-w-sm rounded-2xl border border-white/10 bg-panel p-5 text-center text-sm text-slate-300">
            <p>Không tải được bài tự kiểm tra (có thể do mạng chập chờn). Thử tải lại trang.</p>
            <button
              type="button"
              onClick={props.onClose}
              className="mt-3 rounded-full border border-white/15 px-4 py-1.5 text-xs font-semibold text-white hover:border-white/30"
            >
              Đóng
            </button>
          </div>
        </div>
      }
    >
      <TutoringExitQuizLazyInner {...props} />
    </LazyErrorBoundary>
  );
}
