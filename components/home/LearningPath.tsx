const stages = [
  {
    grade: "Lớp 10",
    focus: "Cơ học & Năng lượng",
    detail: "Động học, động lực học Newton, công – công suất, động lượng, chuyển động tròn.",
  },
  {
    grade: "Lớp 11",
    focus: "Dao động, Sóng & Điện",
    detail: "Dao động điều hoà, sóng cơ – sóng âm, điện trường, dòng điện không đổi.",
  },
  {
    grade: "Lớp 12",
    focus: "Nhiệt học & Hạt nhân",
    detail: "Vật lý nhiệt, khí lý tưởng, từ trường – điện xoay chiều, vật lý hạt nhân.",
  },
];

export default function LearningPath() {
  return (
    <section id="learning-path" className="bg-white py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-primary">
            Lộ trình học
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Một quỹ đạo xuyên suốt ba năm THPT.
          </h2>
        </div>

        <div className="relative mt-20">
          {/* Spine: the same parabolic language as the Hero, now stretched
              flat to represent a journey travelled over time rather than
              a single throw — 3 điểm dừng, một quỹ đạo liên tục. */}
          <svg
            viewBox="0 0 1000 120"
            preserveAspectRatio="none"
            className="absolute left-0 top-10 hidden h-[2px] w-full md:block"
            aria-hidden
          >
            <path
              d="M 40 60 Q 500 -40 960 60"
              stroke="#0B3D91"
              strokeWidth="2"
              strokeLinecap="round"
              className="trajectory-path"
              fill="none"
            />
          </svg>

          <div className="grid grid-cols-1 gap-10 md:grid-cols-3 md:gap-8">
            {stages.map((s, i) => (
              <div key={s.grade} className="relative flex flex-col">
                <div className="flex items-center gap-3">
                  <span
                    className="flex h-3 w-3 shrink-0 rounded-full bg-accent ring-4 ring-accent/15"
                    aria-hidden
                  />
                  <span className="font-mono text-xs uppercase tracking-widest text-muted">
                    Giai đoạn {i + 1}
                  </span>
                </div>
                <h3 className="mt-4 font-display text-2xl font-bold text-ink">
                  {s.grade}
                </h3>
                <p className="mt-1 text-sm font-semibold text-primary">
                  {s.focus}
                </p>
                <p className="mt-3 text-sm leading-relaxed text-muted">
                  {s.detail}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
