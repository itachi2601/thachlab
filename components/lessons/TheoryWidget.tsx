"use client";

/**
 * components/lessons/TheoryWidget.tsx
 *
 * Cầu nối giữa HTML lý thuyết (chuỗi thô trong `lesson_items.body_html`) và widget React
 * thật. Trong HTML, tác giả đặt thẻ rỗng:
 *
 *   <div class="tl-widget" data-tl-widget="dao-dong-dieu-hoa"></div>
 *
 * TheoryContent.tsx cắt chuỗi tại đó rồi render component ở đây.
 *
 * Hai quy tắc bắt buộc (lý do nằm ở components/ui/LazyErrorBoundary.tsx — đã kiểm bằng thực
 * nghiệm, xem `perf4/RESULT.md` §6):
 *  1. Mọi widget phải là next/dynamic({ ssr: false }) — chunk chỉ tải khi cần, không vào JS
 *     ban đầu của trang bài học (AGENTS.md: "Đăng nội dung — luôn tối ưu tốc độ tải").
 *  2. Chỉ mount SAU một tương tác của học sinh (nút "Mở mô phỏng"). dynamic({ssr:false}) mount
 *     ngay lúc hydrate trang đầu có thể làm lỗi ChunkLoadError không bị boundary bắt; mount sau
 *     tương tác thì boundary bắt bình thường. Phụ huynh/HS mạng yếu cũng không mất luôn cả bài.
 *
 * Widget KHÔNG gọi Supabase, không đọc localStorage, không nhận props từ HTML — mọi tham số
 * nằm trong chính component (muốn cấu hình thì thêm prop và đọc `data-*` tại đây).
 */

import dynamic from "next/dynamic";
import { useState, type ComponentType } from "react";
import { Play, Sparkles } from "lucide-react";
import { LazyErrorBoundary, LazyPanelFallback } from "@/components/ui/LazyErrorBoundary";

const HarmonicMotionLab = dynamic(() => import("@/components/physics/HarmonicMotionLab"), {
  ssr: false,
  loading: () => (
    <LazyPanelFallback className="min-h-[18rem]" message="Đang tải mô phỏng…" />
  ),
});

interface WidgetEntry {
  title: string;
  hint: string;
  Component: ComponentType;
}

/** Tên widget (giá trị `data-tl-widget`) → component. Thêm widget mới = thêm 1 dòng ở đây. */
const WIDGETS: Record<string, WidgetEntry> = {
  "dao-dong-dieu-hoa": {
    title: "Con lắc lò xo và chuyển động tròn đều",
    hint: "Kéo biên độ A, tốc độ góc ω và pha ban đầu φ rồi so sánh con lắc với bóng của điểm M quay đều.",
    Component: HarmonicMotionLab,
  },
};

export default function TheoryWidget({ name }: { name: string }) {
  const [open, setOpen] = useState(false);
  const entry = WIDGETS[name];
  if (!entry) return null; // tên lạ: bỏ qua im lặng, không làm hỏng cả mục lý thuyết

  const { title, hint, Component } = entry;

  return (
    <div className="tl-widget-card">
      <div className="tl-widget-head">
        <p className="tl-widget-title">
          <Sparkles size={15} aria-hidden /> {title}
        </p>
        <p className="tl-widget-hint">{hint}</p>
      </div>
      {open ? (
        <LazyErrorBoundary
          fallback={
            <LazyPanelFallback
              className="min-h-[16rem]"
              message="Không tải được mô phỏng. Em thử tải lại trang, hoặc đọc phần chữ bên trên vẫn đủ ý."
            />
          }
        >
          <Component />
        </LazyErrorBoundary>
      ) : (
        <button type="button" className="tl-widget-open" onClick={() => setOpen(true)}>
          <Play size={15} aria-hidden /> Mở mô phỏng
        </button>
      )}
    </div>
  );
}
