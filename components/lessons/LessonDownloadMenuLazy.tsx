"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Menu "Tải bài học" kéo theo bộ dựng .docx/.tex (docx-writer, latex-to-omml…) — chỉ cần khi
 * học sinh/giáo viên thật sự bấm tải, nên tách khỏi bundle ban đầu của /lop-hoc/bai (quy tắc
 * perf: khối JS nặng thêm vào trang bài = dynamic ssr:false + LazyErrorBoundary).
 */
const Inner = dynamic(() => import("@/components/lessons/LessonDownloadMenu"), { ssr: false, loading: () => null });

export default function LessonDownloadMenuLazy(props: ComponentProps<typeof Inner>) {
  return (
    <LazyErrorBoundary fallback={null}>
      <Inner {...props} />
    </LazyErrorBoundary>
  );
}
