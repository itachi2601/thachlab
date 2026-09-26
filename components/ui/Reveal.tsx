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
 *
 * ErrorBoundary: nếu việc tải chunk RevealMotion lỗi (mất mạng, chunk 404…),
 * KHÔNG được kẹt ở fallback opacity:0 vĩnh viễn — học sinh sẽ tưởng nhầm
 * trang trắng/thiếu nội dung. Bắt lỗi rồi hiện thẳng nội dung ở trạng thái
 * cuối (opacity:1, không dịch), bỏ qua hiệu ứng, còn hơn ẩn mất nội dung.
 */

import { Component, lazy, Suspense, type ReactNode } from "react";

const RevealMotion = lazy(() => import("@/components/ui/RevealMotion"));

class RevealErrorBoundary extends Component<
  { fallback: ReactNode; children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch() {
    // Chunk tải lỗi (mất mạng, 404…) — không cần log gì thêm, fallback đã lo hiện nội dung.
  }

  render() {
    return this.state.hasError ? this.props.fallback : this.props.children;
  }
}

export function Reveal({
  children,
  delay = 0,
  className,
}: {
  children: ReactNode;
  delay?: number;
  className?: string;
}) {
  // Hiện đúng trạng thái CUỐI (đã hiện hẳn) khi tải chunk lỗi — không phải trạng thái
  // đầu ẩn/opacity:0 như lúc đang chờ, tránh học sinh tưởng trang trắng/mất nội dung.
  const shownFallback = <div className={className}>{children}</div>;

  return (
    <RevealErrorBoundary fallback={shownFallback}>
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
    </RevealErrorBoundary>
  );
}
