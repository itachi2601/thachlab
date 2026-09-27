"use client";

/**
 * components/exams/QuestionSlide.tsx
 *
 * Bọc hiệu ứng chuyển câu (trượt + đổi mờ) khi làm đề — phần framer-motion
 * nằm ở QuestionSlideMotion.tsx và được nạp chậm (React.lazy) để trang làm
 * đề (/kiem-tra/lam) không tải framer-motion (~140 KB) trong JS ban đầu.
 *
 * Trong lúc chờ chunk, fallback render thẳng children không hiệu ứng (giống
 * <Reveal>) — câu hỏi vẫn hiện ngay, không skeleton/khoảng trắng, không nhảy
 * layout; chunk về thì các lần đổi câu tiếp theo mới có hiệu ứng trượt.
 *
 * LazyErrorBoundary (dùng chung — xem components/ui/LazyErrorBoundary.tsx): nếu
 * chunk tải lỗi (mất mạng, 404…) thì trước đây lỗi thoát thẳng lên error boundary
 * toàn trang — crash trắng GIỮA LÚC học sinh đang làm bài, mất câu trả lời chưa
 * lưu. Bắt lỗi tại chỗ, hiện thẳng children không hiệu ứng (giống lúc đang chờ).
 */

import { lazy, Suspense, type ReactNode } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

const QuestionSlideMotion = lazy(() => import("@/components/exams/QuestionSlideMotion"));

export default function QuestionSlide({
  children,
  slideKey,
}: {
  children: ReactNode;
  slideKey: number | string;
}) {
  const plain = <div>{children}</div>;
  return (
    <LazyErrorBoundary fallback={plain}>
      <Suspense fallback={plain}>
        <QuestionSlideMotion slideKey={slideKey}>{children}</QuestionSlideMotion>
      </Suspense>
    </LazyErrorBoundary>
  );
}
