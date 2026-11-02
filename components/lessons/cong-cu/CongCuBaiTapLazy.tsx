"use client";

import dynamic from "next/dynamic";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type { WorkedTool } from "@/features/lessons/types";

/**
 * 🧪 Công cụ giải tương tác dưới đề bài tập mẫu (thử 2/11/2026). Tải chậm (canvas + vòng lặp hình) — chỉ dạng nào có
 * `cong_cu` mới kéo chunk này; lỗi chunk chỉ mất công cụ, đề và lời giải vẫn đủ.
 */
const GiaoThoaHaiNguon = dynamic(() => import("@/components/lessons/cong-cu/GiaoThoaHaiNguon"), {
  ssr: false,
  loading: () => <p className="text-xs text-muted">Đang tải mô phỏng…</p>,
});

export default function CongCuBaiTapLazy({
  tool,
  opened,
  color,
  steps,
}: {
  tool: WorkedTool;
  opened: number | null;
  color: string;
  steps?: string[];
}) {
  if (tool.loai !== "giao_thoa_2_nguon") return null;
  return (
    <LazyErrorBoundary fallback={null}>
      <GiaoThoaHaiNguon {...tool} opened={opened} color={color} steps={steps} />
    </LazyErrorBoundary>
  );
}
