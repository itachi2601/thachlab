"use client";

/**
 * components/home/PhysicsSimulationHero.tsx
 *
 * Hero mới của ThachLab: bên trái là thông điệp, bên phải là một "phòng thí
 * nghiệm" thu nhỏ — con lắc lò xo dao động điều hòa đồng bộ với đồ thị x–t,
 * điều khiển được bằng hai slider. Giữ nguyên navbar/màu thương hiệu/font/
 * layout tổng thể của trang — component này chỉ thay thế nội dung Hero.
 */

import { useState } from "react";
import { ArrowRight, PlayCircle, FileVideo, ClipboardCheck, BookOpen } from "lucide-react";
import { useHarmonicMotion } from "@/hooks/useHarmonicMotion";
import { SpringSimulation } from "@/components/physics/SpringSimulation";
import { DisplacementChart } from "@/components/physics/DisplacementChart";
import { ControlPanel } from "@/components/physics/ControlPanel";
import { FormulaPanel } from "@/components/physics/FormulaPanel";

const AVATAR_COLORS = ["#2563EB", "#7C3AED", "#0EA5E9", "#F59E0B"];

const stats = [
  {
    icon: FileVideo,
    tint: "bg-blue-500/15 text-blue-400",
    value: "500+",
    label: "Video bài giảng",
    detail: "Dễ hiểu, trực quan, sinh động",
  },
  {
    icon: ClipboardCheck,
    tint: "bg-emerald-500/15 text-emerald-400",
    value: "3.000+",
    label: "Bài tập thực hành",
    detail: "Từ cơ bản đến nâng cao",
  },
  {
    icon: BookOpen,
    tint: "bg-amber-500/15 text-amber-400",
    value: "100%",
    label: "Bám sát chương trình",
    detail: "GDPT 2018 mới nhất",
  },
];

export function PhysicsSimulationHero() {
  const motion = useHarmonicMotion({ initialAmplitude: 0.1, initialFrequency: 1 });
  const [formulaOpen, setFormulaOpen] = useState(true);

  return (
    <section className="relative overflow-hidden bg-[#05070B] px-6 pt-32 pb-16 sm:pt-36 sm:pb-20 lg:px-12">
      <div className="mx-auto grid max-w-6xl grid-cols-1 items-center gap-14 lg:grid-cols-2 lg:gap-10">
        {/* ---------------- CỘT TRÁI ---------------- */}
        <div>
          <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3.5 py-1.5 text-sm text-slate-300">
            💡 Có bao giờ em tự hỏi...
          </span>

          <h1 className="mt-6 text-4xl font-semibold leading-[1.1] tracking-tight text-white sm:text-5xl lg:text-[3.4rem]">
            Tại sao mọi thứ
            <br />
            lại <span className="text-[#2563EB]">dao động?</span>
          </h1>

          <p className="mt-6 max-w-md text-base leading-relaxed text-slate-400 sm:text-lg">
            Từ con lắc lò xo đến trái tim con người,
            <br className="hidden sm:block" />
            Vật lý giúp chúng ta hiểu nhịp điệu của thế giới.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <button className="flex items-center gap-2 rounded-xl bg-[#2563EB] px-6 py-3 text-sm font-medium text-white shadow-lg shadow-blue-900/30 transition hover:bg-[#1D4ED8] active:scale-[0.98] sm:text-base">
              Bắt đầu hành trình
              <ArrowRight size={18} />
            </button>
            <button className="flex items-center gap-2 rounded-xl border border-white/15 px-6 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5 active:scale-[0.98] sm:text-base">
              <PlayCircle size={18} />
              Xem khóa học
            </button>
          </div>

          <p className="mt-5 flex items-center gap-2 text-sm text-slate-500">
            <span className="text-emerald-400">✔</span> Hoàn toàn miễn phí
          </p>

          <div className="mt-4 flex items-center gap-3">
            <div className="flex -space-x-3">
              {AVATAR_COLORS.map((color, i) => (
                <span
                  key={i}
                  style={{ backgroundColor: color }}
                  className="h-8 w-8 rounded-full border-2 border-[#05070B]"
                />
              ))}
            </div>
            <p className="text-sm leading-tight text-slate-400">
              Hơn 3.000+ học sinh
              <br />
              đang học cùng ThachLab
            </p>
          </div>
        </div>

        {/* ---------------- CỘT PHẢI ---------------- */}
        <div className="relative rounded-3xl border border-white/10 bg-[#0F172A]/80 p-5 shadow-2xl shadow-black/50 backdrop-blur-xl sm:p-6">
          <p className="mb-3 font-mono text-[11px] uppercase tracking-widest text-slate-400">
            Mô phỏng: Dao động con lắc lò xo
          </p>

          {/* PHẦN 1 + PHẦN 2 */}
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div className="h-56 rounded-2xl border border-white/5 bg-black/20 sm:h-64">
              <SpringSimulation
                x={motion.x}
                v={motion.v}
                a={motion.a}
                amplitude={motion.amplitude}
              />
            </div>
            <div className="h-56 rounded-2xl border border-white/5 bg-black/20 p-2 sm:h-64">
              <DisplacementChart
                t={motion.t}
                amplitude={motion.amplitude}
                frequency={motion.frequency}
              />
            </div>
          </div>

          {/* CONTROL PANEL */}
          <ControlPanel
            amplitude={motion.amplitude}
            frequency={motion.frequency}
            isPlaying={motion.isPlaying}
            formulaOpen={formulaOpen}
            onAmplitudeChange={motion.setAmplitude}
            onFrequencyChange={motion.setFrequency}
            onToggle={motion.toggle}
            onReset={motion.reset}
            onToggleFormula={() => setFormulaOpen((o) => !o)}
          />

          {/* CÔNG THỨC */}
          <FormulaPanel open={formulaOpen} period={motion.period} omega={motion.omega} />
        </div>
      </div>

      {/* ---------------- STATS BAR ---------------- */}
      <div className="mx-auto mt-16 grid max-w-6xl grid-cols-1 gap-4 border-t border-white/10 pt-10 sm:grid-cols-3">
        {stats.map((s) => (
          <div key={s.label} className="flex items-center gap-4">
            <span className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl ${s.tint}`}>
              <s.icon size={22} />
            </span>
            <div>
              <p className="text-lg font-semibold text-white">
                {s.value} <span className="text-base font-medium text-slate-300">{s.label}</span>
              </p>
              <p className="text-sm text-slate-500">{s.detail}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
