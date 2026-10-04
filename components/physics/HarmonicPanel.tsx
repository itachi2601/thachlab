"use client";

/**
 * components/physics/HarmonicPanel.tsx
 *
 * Panel "Dao động": con lắc lò xo + đồ thị x–t + bảng điều khiển.
 *
 * ĐÃ RỜI HERO 5/10/2026 (hero đổi tab 2 thành "Thả hàng cứu hộ"). Code giữ nguyên,
 * cố ý: đây là mô phỏng tương tác duy nhất của chương Dao động lớp 11 — Giai đoạn 3
 * trong docs/ROADMAP.md chờ nhúng nó vào bài Dao động kèm bộ câu hỏi.
 * Hiện chưa file nào import, nên nó không nằm trong bundle.
 *
 * Khi nhúng lại: nạp bằng next/dynamic({ ssr: false }) — SVG + đồ thị + framer-motion
 * của bảng công thức không nên vào gói JS tải đầu tiên của trang.
 *
 * Không tự chạy khi mới mở (autoPlay: false): mô phỏng chỉ chuyển động khi học
 * sinh bấm "Phát" (quy tắc B4 — hoạt hình để giải thích, do HS bấm chạy).
 */

import { useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import { useHarmonicMotion } from "@/hooks/useHarmonicMotion";
import { ControlPanel } from "@/components/physics/ControlPanel";
import { DisplacementChart } from "@/components/physics/DisplacementChart";
import { SpringSimulation } from "@/components/physics/SpringSimulation";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

// Bảng công thức dùng framer-motion (~140 KB) và chỉ hiện khi bấm nút — tải chậm, lúc đóng vốn không render gì.
const FormulaPanelLazy = dynamic(
  () => import("@/components/physics/FormulaPanel").then((m) => m.FormulaPanel),
  { ssr: false, loading: () => null }
);
// Panel phụ, vốn đã trả null khi đóng — lỗi render thì cũng chỉ ẩn đi, không cần thông báo.
function FormulaPanel(props: ComponentProps<typeof FormulaPanelLazy>) {
  return (
    <LazyErrorBoundary>
      <FormulaPanelLazy {...props} />
    </LazyErrorBoundary>
  );
}

export function HarmonicPanel() {
  const motion = useHarmonicMotion({ initialAmplitude: 0.1, initialFrequency: 1, autoPlay: false });
  const [formulaOpen, setFormulaOpen] = useState(false);

  return (
    <div>
      <div className="grid grid-cols-2 gap-2 sm:gap-3">
        <div className="h-36 rounded-xl border border-white/5 bg-black/20 sm:h-64">
          <SpringSimulation x={motion.x} v={motion.v} a={motion.a} amplitude={motion.amplitude} />
        </div>
        <div className="h-36 rounded-xl border border-white/5 bg-black/20 p-2 sm:h-64">
          <DisplacementChart t={motion.t} amplitude={motion.amplitude} frequency={motion.frequency} />
        </div>
      </div>

      <ControlPanel
        amplitude={motion.amplitude}
        frequency={motion.frequency}
        isPlaying={motion.isPlaying}
        formulaOpen={formulaOpen}
        onAmplitudeChange={motion.setAmplitude}
        onFrequencyChange={motion.setFrequency}
        onToggle={motion.toggle}
        onReset={motion.reset}
        onToggleFormula={() => setFormulaOpen((open) => !open)}
      />

      <FormulaPanel open={formulaOpen} period={motion.period} omega={motion.omega} />
    </div>
  );
}
