"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/** Bản tải-chậm của EntryDiagnosticQuiz — chỉ mount khi em bấm "Bắt đầu" (cùng mẫu TutoringExitQuizLazy). */
const Inner = dynamic(() => import("@/components/results/EntryDiagnosticQuiz"), {
  ssr: false,
  loading: () => (
    <div role="status" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <p className="rounded-2xl border border-line bg-panel px-5 py-4 text-sm text-ink">Đang tải bài kiểm tra…</p>
    </div>
  ),
});

export default function EntryDiagnosticQuizLazy(props: ComponentProps<typeof Inner>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div role="alertdialog" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="max-w-sm rounded-2xl border border-line bg-panel p-5 text-center text-sm text-ink">
            <p>Không tải được bài kiểm tra (có thể do mạng chập chờn). Thử tải lại trang.</p>
            <button
              type="button"
              onClick={props.onClose}
              className="mt-3 min-h-11 rounded-full border border-line px-4 py-1.5 text-xs font-semibold text-ink hover:border-line-strong"
            >
              Đóng
            </button>
          </div>
        </div>
      }
    >
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
