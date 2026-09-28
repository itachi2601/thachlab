"use client";

import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

// Mục Vinh danh tuần: gọi 1 RPC anon + kéo theo RankBadge/RankAvatarFrame — chỉ tải khi người xem
// cuộn tới gần (không thêm JS/round-trip vào lần tải đầu của trang chủ, giữ Lighthouse đợt perf 9/2026).
const HonorBoardPanel = dynamic(() => import("@/components/home/HonorBoardPanel"), { ssr: false, loading: () => null });

export default function HonorBoard() {
  const ref = useRef<HTMLDivElement>(null);
  const [near, setNear] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el || near) return;
    // Trình duyệt quá cũ không có IntersectionObserver → tải ngay ở tick kế tiếp.
    if (typeof IntersectionObserver === "undefined") {
      const t = setTimeout(() => setNear(true), 0);
      return () => clearTimeout(t);
    }
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setNear(true);
          io.disconnect();
        }
      },
      { rootMargin: "600px 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [near]);

  return (
    <div ref={ref} data-honor-board>
      {near && (
        <LazyErrorBoundary>
          <HonorBoardPanel />
        </LazyErrorBoundary>
      )}
    </div>
  );
}
