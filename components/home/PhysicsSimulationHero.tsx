"use client";

/**
 * components/home/PhysicsSimulationHero.tsx
 *
 * Hero trang chủ: một thí nghiệm tương tác ngay màn hình đầu.
 *
 * Tab 1 (mặc định) — "Ném xiên": học sinh tự tay kéo bệ phóng, tự tìm ra góc ném
 * cho tầm xa lớn nhất. Tab 2 — "Thả hàng": máy bay cứu hộ bay ngang ở độ cao h,
 * bấm thả đúng lúc để gói hàng rơi trúng bãi đáp (chuyển động ném ngang, Vật lí 10
 * Bài 12). Tab 3 — "Giao thoa": khay sóng hai nguồn (Bài 12, Vật lí 11), kéo điểm M
 * để tự đọc ra d₂ − d₁ = kλ. Tab 4 — "Hình chiếu": bóng của điểm M quay đều và một
 * con lắc lò xo nằm ngang trên cùng một trục x (Bài 1. Dao động điều hoà, Vật lí 11)
 * — học sinh tự khớp ω để giữ nhịp rồi tự thử xem biên độ có đổi nhịp không.
 *
 * Con lắc lò xo (HarmonicPanel) đã rời hero 5/10/2026 — code giữ nguyên để nhúng
 * vào bài Dao động lớp 11 khi Giai đoạn 3 làm (xem docs/ROADMAP.md).
 *
 * Ba tab sau nạp chậm, chỉ mount khi được chọn. Hàng tab có 4 mục — đúng trần D4 —
 * nên nhãn phải 1 dòng ở 360px: chữ nhỏ hơn và đệm hẹp hơn ở mobile, và mỗi nhãn
 * đều whitespace-nowrap để không bị bẻ thành 2 dòng.
 *
 * Thứ tự DOM = thứ tự đọc trên điện thoại: câu hỏi → thí nghiệm → nút vào lớp
 * (B8) — nhờ vậy phần tương tác nằm trong màn hình đầu ở 375px (B1), còn trên
 * desktop thì thí nghiệm đứng cột phải, cao bằng cả hai hàng chữ.
 */

import { useState, type KeyboardEvent } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";
import { ArrowRight } from "lucide-react";
import { ProjectileSimulation } from "@/components/physics/ProjectileSimulation";
import { LazyErrorBoundary, LazyPanelFallback } from "@/components/ui/LazyErrorBoundary";

// Máy bay + quỹ đạo gói hàng chỉ cần khi học sinh bấm sang tab 2 → để ngoài gói JS
// tải đầu tiên (xem AGENTS.md mục "Đăng nội dung — luôn tối ưu tốc độ tải").
const RescueDropSimulation = dynamic(
  () => import("@/components/physics/RescueDropSimulation").then((m) => m.RescueDropSimulation),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-white/10 text-sm text-slate-400 sm:h-[26rem]">
        Đang tải mô phỏng…
      </div>
    ),
  }
);

// Khay sóng giao thoa cũng nạp chậm: canvas + bản đồ vân chỉ có nghĩa khi học
// sinh thật sự chọn tab này.
const InterferenceSimulation = dynamic(
  () => import("@/components/physics/InterferenceSimulation").then((m) => m.InterferenceSimulation),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-white/10 text-sm text-slate-400 sm:h-[26rem]">
        Đang tải mô phỏng…
      </div>
    ),
  }
);

// Mô hình "Hình chiếu": canvas 2 làn + toán hình chiếu, cũng chỉ có nghĩa khi học
// sinh thật sự chọn tab này.
const ShadowSpringSimulation = dynamic(
  () => import("@/components/physics/ShadowSpringSimulation").then((m) => m.ShadowSpringSimulation),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-white/10 text-sm text-slate-400 sm:h-[26rem]">
        Đang tải mô phỏng…
      </div>
    ),
  }
);

const TABS = [
  { key: "projectile", label: "Ném xiên" },
  { key: "rescue", label: "Thả hàng" },
  { key: "interference", label: "Giao thoa" },
  { key: "projection", label: "Hình chiếu" },
] as const;

type TabKey = (typeof TABS)[number]["key"];

const FORMULAS = [
  "R = v₀²·sin2α/g",
  "x = A·cos(ωt + φ)",
  "F = ma",
  "t = √(2h/g)",
  "E = mc²",
  "L = v₀·t",
  "v = dx/dt",
  "T = 2π√(l/g)",
  "P = F·v",
  "λ = v/f",
  "W = ∫F·ds",
  "p = mv",
  "a = -ω²x",
];

export function PhysicsSimulationHero() {
  const [tab, setTab] = useState<TabKey>("projectile");

  // Một khung báo lỗi dùng chung cho cả 4 tab (chỉ một tab được mount ở mỗi thời điểm).
  const panelFallback = (
    <LazyPanelFallback className="min-h-72" message="Không tải được mô phỏng. Thử tải lại trang." />
  );

  // Điều hướng tab bằng phím trái/phải (chuẩn ARIA cho tablist).
  const onTablistKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
    event.preventDefault();
    const index = TABS.findIndex((item) => item.key === tab);
    const next = event.key === "ArrowRight" ? (index + 1) % TABS.length : (index - 1 + TABS.length) % TABS.length;
    setTab(TABS[next].key);
  };

  return (
    <section id="thpt" className="relative overflow-hidden bg-[#05070B] px-6 pb-10 pt-24 sm:pb-16 sm:pt-28 lg:px-12">
      <div aria-hidden className="grid-bg absolute inset-0" />
      <div
        aria-hidden
        className="pointer-events-none absolute left-1/2 top-[-20%] h-[480px] w-[720px] -translate-x-1/2 rounded-full bg-cyan-500/[0.08] blur-[120px]"
      />

      <div className="relative mx-auto grid max-w-6xl grid-cols-1 gap-6 lg:grid-cols-12 lg:items-center lg:gap-x-10">
        <div className="lg:col-span-5 lg:col-start-1 lg:row-start-1">
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">
            Có bao giờ em tự hỏi…
          </p>

          <h1 className="mt-2 font-display text-[2rem] font-bold leading-[1.1] tracking-tight text-ink sm:mt-5 sm:text-5xl lg:text-[2.9rem]">
            Ném ở góc nào
            <br />
            thì <span className="text-cyan-300">xa nhất</span>?
          </h1>

          <p className="mt-3 max-w-md text-base leading-relaxed text-muted sm:mt-6 sm:text-lg">
            Kéo bệ phóng rồi thả tay, hoặc lái máy bay cứu hộ thả hàng đúng lúc — mỗi lần thử là
            một thí nghiệm em tự làm.
          </p>
        </div>

        <div className="lg:col-span-5 lg:col-start-1 lg:row-start-2 lg:self-start">
          <div className="flex flex-wrap items-center gap-3">
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
              Xem lộ trình
            </Link>
          </div>

          <p className="mt-3 max-w-md text-sm leading-relaxed text-muted">
            Học miễn phí trên web, theo đúng nhịp lớp trên trường.
          </p>
        </div>
        <div className="relative rounded-2xl border border-line bg-panel p-2.5 shadow-xl shadow-black/30 sm:p-5 lg:col-span-7 lg:col-start-6 lg:row-span-2 lg:row-start-1">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2 sm:mb-3">
            <p className="font-mono text-[13px] uppercase tracking-widest text-muted">
              Thí nghiệm
            </p>
            <div
              role="tablist"
              aria-label="Chọn thí nghiệm"
              onKeyDown={onTablistKeyDown}
              className="flex overflow-hidden rounded-lg border border-white/10"
            >
              {TABS.map((item) => (
                <button
                  key={item.key}
                  type="button"
                  role="tab"
                  id={`hero-tab-${item.key}`}
                  aria-selected={tab === item.key}
                  aria-controls={`hero-panel-${item.key}`}
                  tabIndex={tab === item.key ? 0 : -1}
                  onClick={() => setTab(item.key)}
                  className={`inline-flex min-h-11 items-center whitespace-nowrap rounded-none px-2 text-[13px] font-medium transition active:scale-[0.98] sm:px-3 sm:text-sm ${
                    tab === item.key
                      ? "bg-cyan-300/[0.14] text-cyan-300"
                      : "text-slate-400 hover:bg-white/[0.06]"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          <div
            role="tabpanel"
            id={`hero-panel-${tab}`}
            aria-labelledby={`hero-tab-${tab}`}
          >
            {tab === "projectile" ? (
              <LazyErrorBoundary fallback={panelFallback}>
                <ProjectileSimulation />
              </LazyErrorBoundary>
            ) : tab === "rescue" ? (
              <LazyErrorBoundary fallback={panelFallback}>
                <RescueDropSimulation />
              </LazyErrorBoundary>
            ) : tab === "interference" ? (
              <LazyErrorBoundary fallback={panelFallback}>
                <InterferenceSimulation />
              </LazyErrorBoundary>
            ) : (
              <LazyErrorBoundary fallback={panelFallback}>
                <ShadowSpringSimulation />
              </LazyErrorBoundary>
            )}
          </div>
        </div>

      </div>

      <div className="relative mx-auto mt-12 max-w-6xl overflow-hidden [mask-image:linear-gradient(90deg,transparent,black_12%,black_88%,transparent)]">
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
