"use client";

import dynamic from "next/dynamic";

/**
 * Bản tải-chậm của ContentHtml cho khu quản trị / giáo viên / tin tức — nơi
 * công thức chỉ *có thể* xuất hiện. KaTeX (~290 KB JS + CSS) không nằm trong
 * JS ban đầu của trang; chỗ hiển thị chờ bằng một vệt skeleton nhỏ tới khi
 * chunk về (thường trước cả khi dữ liệu Supabase tải xong).
 *
 * Trang bài học / làm đề / kết quả của học sinh vẫn dùng ContentHtml đồng bộ
 * để công thức hiện ngay cùng nội dung, không nhảy layout.
 */
const ContentHtmlLazy = dynamic(() => import("@/components/exams/ContentHtml"), {
  ssr: false,
  loading: () => (
    <span
      className="inline-block h-4 w-32 max-w-full animate-pulse rounded bg-white/10 align-middle"
      aria-hidden
    />
  ),
});

export default ContentHtmlLazy;
