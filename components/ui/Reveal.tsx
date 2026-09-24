"use client";

/**
 * components/ui/Reveal.tsx
 *
 * Bọc nội dung để hiện dần + trượt lên khi cuộn tới (một lần duy nhất).
 * Phần framer-motion nằm ở RevealMotion.tsx và được nạp chậm (React.lazy)
 * để trang chủ không tải framer-motion (~140 KB) trong JS ban đầu.
 *
 * Trong lúc chờ chunk, fallback render đúng trạng thái ban đầu của hiệu ứng
 * (ẩn + dịch xuống 28px) — giống hệt HTML mà motion.div vốn prerender —
 * nên không có nháy nội dung, không nhảy layout; khi chunk về, phần tử đang
 * trong khung nhìn sẽ hiện dần như trước.
 */

import { lazy, Suspense, type ReactNode } from "react";

const RevealMotion = lazy(() => import("@/components/ui/RevealMotion"));

export function Reveal({
  children,
  delay = 0,
  className,
}: {
  children: ReactNode;
  delay?: number;
  className?: string;
}) {
  return (
    <Suspense
      fallback={
        <div className={className} style={{ opacity: 0, transform: "translateY(28px)" }}>
          {children}
        </div>
      }
    >
      <RevealMotion delay={delay} className={className}>
        {children}
      </RevealMotion>
    </Suspense>
  );
}
