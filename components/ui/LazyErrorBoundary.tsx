"use client";

/**
 * components/ui/LazyErrorBoundary.tsx
 *
 * Bọc quanh một next/dynamic() để lỗi (tải chunk lỗi, hoặc lỗi render sau khi
 * chunk đã tải xong) chỉ làm hỏng đúng phần đó thay vì kéo sập toàn bộ React
 * root — app xuất tĩnh này không có app/error.tsx nên không có gì bắt lại nếu
 * lỗi lọt lên tới đỉnh cây.
 *
 * ĐÃ KIỂM BẰNG THỰC NGHIỆM (không chỉ đọc code — xoá thật 1 file chunk trong
 * `out/`, mở tab mới, quan sát): với component `dynamic(..., { ssr: false })`
 * chỉ mount SAU một tương tác của người dùng (bấm nút, đổi tab, vào trang cần
 * đăng nhập...) — đúng kiểu 7 chỗ được bọc trong đợt này — boundary này BẮT
 * ĐƯỢC ChunkLoadError bình thường: trang vẫn hiện đủ, chỉ đúng phần đó rơi về
 * `fallback`. Test trên `components/home/PhysicsSimulationHero.tsx`
 * (FormulaPanel): xoá chunk thật, tab mới, `ChunkLoadError` lên console nhưng
 * trang KHÔNG trắng — khớp lý thuyết vì dynamic({ssr:false}) không nằm trong
 * lần hydrate đầu, Suspense của nó là Suspense/catch thuần client bình thường.
 *
 * GIỚI HẠN: perf4/RESULT.md §6 (27/9/2026) ghi nhận một trường hợp KHÔNG bắt
 * được — nhưng đó là `RevealMotion` trong `components/ui/Reveal.tsx`, dùng
 * `React.lazy()` (không phải next/dynamic) và render ngay trên trang chủ cho
 * MỌI khách — tức nằm trong lần prerender/hydrate đầu tiên. Nghi vấn: lỗi tải
 * chunk xảy ra đúng lúc hydrate có thể không được Suspense/ErrorBoundary nhận
 * diện đúng cách trong Turbopack (khác hẳn dynamic({ssr:false}) mount sau khi
 * đã hydrate xong). KHÔNG suy luận ngược lại rằng LazyErrorBoundary "vô dụng"
 * cho mọi trường hợp — chỉ tránh dùng cho một dynamic() sẽ render ngay trong
 * lần tải trang đầu tiên của người dùng ẩn danh (như Reveal.tsx) mà chưa kiểm
 * lại thực nghiệm riêng cho trường hợp đó.
 */

import { Component, type ReactNode } from "react";

export class LazyErrorBoundary extends Component<
  { fallback?: ReactNode; children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    return this.state.hasError ? (this.props.fallback ?? null) : this.props.children;
  }
}

// Khung chờ dùng chung cho các panel/tab có nội dung thật (không phải widget phụ
// im lặng trả null) — báo rõ cho người dùng biết phần này lỗi thay vì để trống
// không rõ lý do.
export function LazyPanelFallback({
  message = "Không tải được phần này. Thử tải lại trang.",
  className = "min-h-[24rem]",
}: {
  message?: string;
  className?: string;
}) {
  return (
    <div
      className={`flex items-center justify-center rounded-2xl border border-dashed border-white/10 bg-panel p-6 text-center text-sm text-slate-400 ${className}`}
    >
      {message}
    </div>
  );
}
