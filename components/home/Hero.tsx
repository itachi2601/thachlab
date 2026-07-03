import type { CSSProperties } from "react";

// The path both the stroked curve (visual) and the flying dot (motion)
// follow. Kept in one place so the two always stay in sync.
const TRAJECTORY_D = "M 40 300 Q 330 40 660 260";

export default function Hero() {
  const dotStyle = {
    "--dot-path": `"${TRAJECTORY_D}"`,
  } as CSSProperties;

  return (
    <section className="relative overflow-hidden pt-40 pb-28 lg:pt-48 lg:pb-36">
      {/* Ambient backdrop: a soft radial wash, nothing louder than the copy */}
      <div
        aria-hidden
        className="pointer-events-none absolute -top-40 right-[-10%] h-[520px] w-[520px] rounded-full bg-primary/5 blur-3xl"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute top-20 right-10 h-64 w-64 rounded-full bg-accent/10 blur-3xl"
      />

      <div className="mx-auto grid max-w-6xl grid-cols-1 items-center gap-16 px-6 lg:grid-cols-[1.05fr_0.95fr] lg:px-8">
        <div>
          <p className="fade-up font-mono text-sm font-medium tracking-wide text-primary">
            v = dx/dt · F = ma · E = mc²
          </p>

          <h1 className="fade-up delay-1 mt-6 font-display text-4xl font-bold leading-[1.1] tracking-tight text-ink sm:text-5xl lg:text-6xl">
            Vật lý không chỉ
            <br />
            là công thức.
          </h1>

          <p className="fade-up delay-2 mt-6 max-w-md text-lg leading-relaxed text-muted">
            Đó là cách chúng ta hiểu thế giới.
          </p>

          <div className="fade-up delay-3 mt-10 flex flex-col gap-4 sm:flex-row">
            <a
              href="#hoc-thu"
              className="rounded-full bg-primary px-7 py-3.5 text-center text-sm font-semibold text-white shadow-lg shadow-primary/25 transition-transform hover:-translate-y-0.5 hover:bg-primary-dark"
            >
              Học thử miễn phí
            </a>
            <a
              href="#features"
              className="rounded-full border border-line bg-white px-7 py-3.5 text-center text-sm font-semibold text-ink transition-colors hover:border-primary/40 hover:text-primary"
            >
              Xem khóa học
            </a>
          </div>

          <p className="fade-up delay-4 mt-8 text-xs font-mono uppercase tracking-widest text-muted">
            Lớp 10 · Lớp 11 · Lớp 12 — Bám sát chương trình GDPT mới
          </p>
        </div>

        {/* Signature: a projectile's arc, drawn like chalk on a bảng đen,
            with a small ball flying along it — the equation made visible. */}
        <div className="relative mx-auto aspect-[7/5] w-full max-w-lg">
          <svg
            viewBox="0 0 700 340"
            fill="none"
            className="h-full w-full"
            aria-hidden
          >
            <line
              x1="20" y1="310" x2="680" y2="310"
              stroke="#E2E8F0" strokeWidth="2"
            />
            <path
              d={TRAJECTORY_D}
              stroke="#0B3D91"
              strokeWidth="3"
              strokeLinecap="round"
              className="trajectory-path"
            />
            {[0, 1, 2, 3, 4, 5].map((i) => (
              <circle
                key={i}
                cx={40 + i * 124}
                cy="310"
                r="2.5"
                fill="#94A3B8"
              />
            ))}
          </svg>

          <div
            style={dotStyle}
            className="trajectory-dot absolute left-0 top-0 h-4 w-4 rounded-full bg-accent shadow-md shadow-accent/40"
          />
        </div>
      </div>
    </section>
  );
}
