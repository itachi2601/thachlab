"use client";

import dynamic from "next/dynamic";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type { ComponentProps } from "react";

/**
 * Bản tải-chậm của ContentHtml cho khu quản trị / giáo viên / tin tức — nơi
 * công thức chỉ *có thể* xuất hiện. KaTeX (~290 KB JS + CSS) không nằm trong
 * JS ban đầu của trang; chỗ hiển thị chờ bằng một vệt skeleton nhỏ tới khi
 * chunk về (thường trước cả khi dữ liệu Supabase tải xong).
 *
 * Trang bài học / làm đề / kết quả của học sinh vẫn dùng ContentHtml đồng bộ
 * để công thức hiện ngay cùng nội dung, không nhảy layout.
 */
const ContentHtmlLazyInner = dynamic(() => import("@/components/exams/ContentHtml"), {
  ssr: false,
  loading: () => (
    <span
      className="inline-block h-4 w-32 max-w-full animate-pulse rounded bg-surface-2 align-middle"
      aria-hidden
    />
  ),
});

// Nội dung này chỉ là MỘT đoạn trong bài viết/câu hỏi lớn hơn — lỗi render thì
// ẩn đúng đoạn đó (fallback null), không kéo sập cả bài viết/trang admin đang mở.
function ContentHtmlLazy(props: ComponentProps<typeof ContentHtmlLazyInner>) {
  return (
    <LazyErrorBoundary>
      <ContentHtmlLazyInner {...props} />
    </LazyErrorBoundary>
  );
}

export default ContentHtmlLazy;
