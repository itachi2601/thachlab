"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của LessonPresenter (chế độ trình chiếu bài giảng) — chỉ mount khi thầy bấm
 * "Trình chiếu", nên toàn bộ phần vẽ tay/điều hướng không nằm trong JS ban đầu của
 * `/lop-hoc/bai` (quy tắc tối ưu tốc độ trong AGENTS.md: khối JS nặng thêm mới vào trang học
 * sinh phải tách bằng next/dynamic({ssr:false}) và bọc LazyErrorBoundary).
 *
 * Chunk lỗi (mạng chập chờn ngay lúc bấm chiếu) thì chỉ hiện dòng báo trong lớp phủ, không kéo
 * sập trang bài học đang xem dở.
 */
const LessonPresenterLazyInner = dynamic(() => import("@/components/lessons/LessonPresenter"), {
  ssr: false,
  loading: () => (
    <div className="lesson-presenter-loading" role="status">
      Đang mở chế độ trình chiếu…
    </div>
  ),
});

function LessonPresenterLazy(props: ComponentProps<typeof LessonPresenterLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div className="lesson-presenter-loading is-error" role="alert">
          Không mở được chế độ trình chiếu. Thử tải lại trang rồi bấm lại.
        </div>
      }
    >
      <LessonPresenterLazyInner {...props} />
    </LazyErrorBoundary>
  );
}

export default LessonPresenterLazy;
