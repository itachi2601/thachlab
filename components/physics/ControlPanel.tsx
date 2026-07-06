/**
 * components/physics/ControlPanel.tsx
 *
 * Bảng điều khiển: biên độ A, tần số f, nút Phát/Tạm dừng/Reset và nút
 * bật/tắt panel công thức.
 */

import { ChevronDown, ChevronUp, Pause, Play, RotateCcw } from "lucide-react";
import { AMPLITUDE_RANGE, FREQUENCY_RANGE, formatNumber } from "@/lib/physics";

export interface ControlPanelProps {
  amplitude: number;
  frequency: number;
  isPlaying: boolean;
  formulaOpen: boolean;
  onAmplitudeChange: (value: number) => void;
  onFrequencyChange: (value: number) => void;
  onToggle: () => void;
  onReset: () => void;
  onToggleFormula: () => void;
}

const sliderClass =
  "h-1.5 w-full cursor-pointer appearance-none rounded-full bg-white/10 accent-[#2563EB] " +
  "[&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none " +
  "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-[#2563EB] " +
  "[&::-webkit-slider-thumb]:shadow-[0_0_0_3px_rgba(37,99,235,0.25)] " +
  "[&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:rounded-full " +
  "[&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-[#2563EB]";

export function ControlPanel({
  amplitude,
  frequency,
  isPlaying,
  formulaOpen,
  onAmplitudeChange,
  onFrequencyChange,
  onToggle,
  onReset,
  onToggleFormula,
}: ControlPanelProps) {
  return (
    <div className="mt-4 space-y-4">
      {/* Slider Biên độ */}
      <div>
        <div className="mb-1.5 flex items-center justify-between text-xs text-slate-400">
          <label htmlFor="amplitude-slider">Biên độ A</label>
          <span className="font-mono text-slate-200">{formatNumber(amplitude, 3)} m</span>
        </div>
        <input
          id="amplitude-slider"
          type="range"
          min={AMPLITUDE_RANGE.min}
          max={AMPLITUDE_RANGE.max}
          step={AMPLITUDE_RANGE.step}
          value={amplitude}
          onChange={(e) => onAmplitudeChange(parseFloat(e.target.value))}
          className={sliderClass}
          aria-label="Biên độ dao động"
        />
      </div>

      {/* Slider Tần số */}
      <div>
        <div className="mb-1.5 flex items-center justify-between text-xs text-slate-400">
          <label htmlFor="frequency-slider">Tần số f</label>
          <span className="font-mono text-slate-200">{formatNumber(frequency, 2)} Hz</span>
        </div>
        <input
          id="frequency-slider"
          type="range"
          min={FREQUENCY_RANGE.min}
          max={FREQUENCY_RANGE.max}
          step={FREQUENCY_RANGE.step}
          value={frequency}
          onChange={(e) => onFrequencyChange(parseFloat(e.target.value))}
          className={sliderClass}
          aria-label="Tần số dao động"
        />
      </div>

      {/* Nút điều khiển */}
      <div className="flex items-center gap-2">
        <button
          onClick={onToggle}
          className="flex flex-1 items-center justify-center gap-1.5 rounded-lg bg-[#2563EB] px-3 py-2 text-sm font-medium text-white transition hover:bg-[#1D4ED8] active:scale-[0.98]"
        >
          {isPlaying ? <Pause size={15} /> : <Play size={15} />}
          {isPlaying ? "Tạm dừng" : "Phát"}
        </button>
        <button
          onClick={onReset}
          className="flex items-center justify-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.04] px-3 py-2 text-sm text-slate-200 transition hover:bg-white/[0.08] active:scale-[0.98]"
          aria-label="Đặt lại"
        >
          <RotateCcw size={15} />
        </button>
        <button
          onClick={onToggleFormula}
          aria-pressed={formulaOpen}
          className={`flex items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-sm transition active:scale-[0.98] ${
            formulaOpen
              ? "bg-[#FACC15] text-[#1E1300]"
              : "border border-white/10 bg-white/[0.04] text-slate-200 hover:bg-white/[0.08]"
          }`}
        >
          {formulaOpen ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
          {formulaOpen ? "Ẩn công thức" : "Hiện công thức"}
        </button>
      </div>
    </div>
  );
}
