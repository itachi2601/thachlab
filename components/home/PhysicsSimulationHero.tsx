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
 * để tự đọc ra d₂ − d₁ = kλ. Tab 4 — "Sóng âm": hai loa trái/phải của máy phát cùng một
 * âm sin (hai nguồn kết hợp), học sinh bật âm, che một tai và dịch đầu để nghe chỗ to chỗ
 * nhỏ, đối chiếu với bản đồ vân. Tab "Hình chiếu" (ShadowSpringSimulation) đã rời hero
 * 7/10/2026 — code giữ nguyên để nhúng vào bài Dao động lớp 11.
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
 * Câu hỏi và câu dẫn (COPY) đổi theo tab đang chọn, không giữ lời của tab "Ném xiên".
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
      <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-line text-sm text-muted sm:h-[26rem]">
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
      <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-line text-sm text-muted sm:h-[26rem]">
        Đang tải mô phỏng…
      </div>
    ),
  }
);

// Mô hình "Sóng âm": hai loa của máy phát âm đơn sắc + bản đồ vân giao thoa; Web Audio
// chỉ có nghĩa khi học sinh thật sự chọn tab này.
const SoundWavesSimulation = dynamic(
  () => import("@/components/physics/SoundInterferenceSimulation").then((m) => () => <m.SoundInterferenceSimulation compact />),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-72 items-center justify-center rounded-xl border border-dashed border-line text-sm text-muted sm:h-[26rem]">
        Đang tải mô phỏng…
      </div>
    ),
  }
);

const TABS = [
  { key: "projectile", label: "Ném xiên" },
  { key: "rescue", label: "Thả hàng" },
  { key: "interference", label: "Giao thoa" },
  { key: "sound", label: "Sóng âm" },
] as const;

type TabKey = (typeof TABS)[number]["key"];

/** Câu hỏi + câu dẫn đổi theo tab đang chọn. Giữ hai dòng tiêu đề ngắn để mô phỏng
 *  vẫn nằm trong màn hình đầu ở 375px (B1); câu dẫn chỉ nói việc của đúng tab đó (N1, N4). */
const COPY: Record<
  TabKey,
  { line1: string; before: string; accent: string; after: string; body: string }
> = {
  projectile: {
    line1: "Ném ở góc nào",
    before: "thì ",
    accent: "xa nhất",
    after: "?",
    body: "Kéo bệ phóng rồi thả tay — mỗi lần ném là một thí nghiệm em tự làm.",
  },
  rescue: {
    line1: "Thả lúc nào",
    before: "thì ",
    accent: "trúng",
    after: "?",
    body: "Lái máy bay cứu hộ, bấm thả đúng lúc để gói hàng rơi trúng bãi đáp.",
  },
  interference: {
    line1: "Sóng gặp nhau",
    before: "chỗ nào ",
    accent: "sáng",
    after: "?",
    body: "Kéo điểm M trên khay sóng hai nguồn — đọc hiệu đường đi, biết chỗ sáng hay tối.",
  },
  sound: {
    line1: "Hai loa cùng phát",
    before: "sao có chỗ ",
    accent: "im",
    after: "?",
    body: "Bật âm, che một tai rồi dịch đầu sang ngang — nghe tiếng to nhỏ đổi theo chỗ ngồi.",
  },
};

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
  const copy = COPY[tab];

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
    <section id="thpt" className="relative overflow-clip bg-bg px-6 pb-10 pt-24 sm:pb-16 sm:pt-28 lg:px-12">
      <div aria-hidden className="grid-bg absolute inset-0" />

      <div className="relative mx-auto grid max-w-6xl grid-cols-1 gap-6 lg:grid-cols-12 lg:items-center lg:gap-x-10">
        <div className="order-1 lg:order-none lg:col-span-4 lg:col-start-1 lg:row-start-1" aria-live="polite" aria-atomic="true">
          <p className="font-mono text-xs uppercase tracking-widest text-primary">
            Có bao giờ em tự hỏi…
          </p>

          <h1 className="mt-2 font-display text-[2rem] font-bold leading-[1.1] tracking-tight text-ink sm:mt-5 sm:text-5xl lg:text-[2.4rem]">
            {copy.line1}
            <br />
            {copy.before}
            <span className="text-primary">{copy.accent}</span>
            {copy.after}
          </h1>

          <p className="mt-3 hidden max-w-md text-base leading-relaxed text-muted sm:mt-5 sm:block">
            {copy.body}
          </p>
        </div>

        <div className="order-3 lg:order-none lg:col-span-4 lg:col-start-1 lg:row-start-2 lg:self-start">
          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/lop-hoc"
              className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-primary-dark active:scale-[0.98] sm:text-base"
            >
              Vào lớp học
              <ArrowRight size={18} />
            </Link>
            <Link
              href="#learning-path"
              className="inline-flex items-center gap-2 rounded-lg border border-line px-5 py-3 text-sm font-medium text-ink transition hover:bg-surface-2 active:scale-[0.98] sm:text-base"
            >
              Xem lộ trình
            </Link>
          </div>

          <p className="mt-3 max-w-md text-sm leading-relaxed text-muted">
            Học miễn phí trên web, theo đúng nhịp lớp trên trường.
          </p>
        </div>
        <div className="relative rounded-2xl border border-line bg-panel p-2.5 shadow-xl sm:p-5 order-2 lg:order-none lg:col-span-8 lg:col-start-5 lg:row-span-2 lg:row-start-1">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2 sm:mb-3">
            <p className="font-mono text-[13px] uppercase tracking-widest text-muted">
              Thí nghiệm
            </p>
            <div
              role="tablist"
              aria-label="Chọn thí nghiệm"
              onKeyDown={onTablistKeyDown}
              className="flex overflow-hidden rounded-lg border border-line-strong"
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
                      ? "bg-primary-soft text-primary"
                      : "text-muted hover:bg-surface-2"
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
                <SoundWavesSimulation />
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
