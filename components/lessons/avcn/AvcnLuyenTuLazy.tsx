"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/** Bản tải-chậm của mục Luyện từ AVCN — chỉ bài AVCN cần, không nằm trong JS ban đầu của /lop-hoc/bai. */
const Inner = dynamic(() => import("@/components/lessons/avcn/AvcnLuyenTu"), {
  ssr: false,
  loading: () => <p className="avcn-lt-loading text-sm text-muted">Đang tải phần luyện từ…</p>,
});

export default function AvcnLuyenTuLazy(props: ComponentProps<typeof Inner>) {
  return (
    <LazyErrorBoundary fallback={<p className="text-sm text-muted">Không tải được phần luyện từ. Thử tải lại trang.</p>}>
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
