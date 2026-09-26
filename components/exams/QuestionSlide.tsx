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
 */

import { lazy, Suspense, type ReactNode } from "react";

const QuestionSlideMotion = lazy(() => import("@/components/exams/QuestionSlideMotion"));

export default function QuestionSlide({
  children,
  slideKey,
}: {
  children: ReactNode;
  slideKey: number | string;
}) {
  return (
    <Suspense fallback={<div>{children}</div>}>
      <QuestionSlideMotion slideKey={slideKey}>{children}</QuestionSlideMotion>
    </Suspense>
  );
}
