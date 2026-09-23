"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useHarmonicMotion } from "@/hooks/useHarmonicMotion";
import { SpringSimulation } from "@/components/physics/SpringSimulation";
import { DisplacementChart } from "@/components/physics/DisplacementChart";
import { ControlPanel } from "@/components/physics/ControlPanel";
import { FormulaPanel } from "@/components/physics/FormulaPanel";

const FORMULAS = [
  "x = A·cos(ωt + φ)",
  "F = ma",
  "E = mc²",
  "v = dx/dt",
  "T = 2π√(l/g)",
  "P = F·v",
  "λ = v/f",
  "W = ∫F·ds",
  "p = mv",
  "a = -ω²x",
];

export function PhysicsSimulationHero() {
  const motion = useHarmonicMotion({ initialAmplitude: 0.1, initialFrequency: 1 });
  const [formulaOpen, setFormulaOpen] = useState(true);

  return (
    <section id="thpt" className="relative overflow-hidden bg-[#05070B] px-6 pt-14 pb-16 sm:pt-20 sm:pb-20 lg:px-12">
      <div aria-hidden className="grid-bg absolute inset-0" />
      <div
        aria-hidden
        className="pointer-events-none absolute left-1/2 top-[-20%] h-[480px] w-[720px] -translate-x-1/2 rounded-full bg-cyan-500/[0.08] blur-[120px]"
      />

      <div className="relative mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 lg:grid-cols-2 lg:gap-10">
        <div>
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">
            Có bao giờ em tự hỏi…
          </p>

          <h1 className="mt-5 font-display text-4xl font-bold leading-[1.1] tracking-tight text-ink sm:text-5xl lg:text-[3.4rem]">
            Tại sao mọi thứ
            <br />
            lại{" "}
            <span className="bg-gradient-to-r from-cyan-300 to-sky-400 bg-clip-text text-transparent">
              dao động?
            </span>
          </h1>

          <p className="mt-6 max-w-md text-base leading-relaxed text-muted sm:text-lg">
            Từ con lắc lò xo đến nhịp đập của trái tim — Vật lý giúp em hiểu nhịp
            điệu của thế giới quanh mình.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link
              href="/lop-hoc"
              className="inline-flex items-center gap-2 rounded-lg bg-cyan-300 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-200 active:scale-[0.98] sm:text-base"
            >
              Vào lớp học
              <ArrowRight size={18} />
            </Link>
            <Link
              href="#learning-path"
              className="inline-flex items-center gap-2 rounded-lg border border-line px-5 py-3 text-sm font-medium text-ink transition hover:bg-white/5 active:scale-[0.98] sm:text-base"
            >
              Xem lộ trình lớp 9–12
            </Link>
          </div>

          <p className="mt-6 max-w-md text-sm leading-relaxed text-muted">
            Hoàn toàn miễn phí. Thử kéo thanh <span className="text-ink">Biên độ</span> hay{" "}
            <span className="text-ink">Tần số</span> trong mô phỏng — con lắc và đồ thị x–t đổi
            theo ngay.
          </p>
        </div>

        <div className="relative rounded-2xl border border-line bg-panel p-5 shadow-xl shadow-black/30 sm:p-6">
          <p className="mb-3 font-mono text-[11px] uppercase tracking-widest text-muted">
            Mô phỏng: Dao động con lắc lò xo
          </p>

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div className="h-56 rounded-xl border border-white/5 bg-black/20 sm:h-64">
              <SpringSimulation
                x={motion.x}
                v={motion.v}
                a={motion.a}
                amplitude={motion.amplitude}
              />
            </div>
            <div className="h-56 rounded-xl border border-white/5 bg-black/20 p-2 sm:h-64">
              <DisplacementChart
                t={motion.t}
                amplitude={motion.amplitude}
                frequency={motion.frequency}
              />
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
            onToggleFormula={() => setFormulaOpen((o) => !o)}
          />

          <FormulaPanel open={formulaOpen} period={motion.period} omega={motion.omega} />
        </div>
      </div>

      <div className="relative mx-auto mt-14 max-w-6xl overflow-hidden [mask-image:linear-gradient(90deg,transparent,black_12%,black_88%,transparent)]">
        <div className="marquee font-mono text-sm text-slate-500">
          {[0, 1].map((dup) => (
            <span key={dup} className="flex shrink-0 items-center gap-12">
              {FORMULAS.map((f) => (
                <span key={f} className="whitespace-nowrap">
                  {f} <span className="mx-3 text-slate-700">·</span>
                </span>
              ))}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
