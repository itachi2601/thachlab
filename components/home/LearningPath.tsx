import { BookOpen, Flag, Rocket } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

const stages = [
  {
    grade: "Lớp 10",
    focus: "Xây nền tảng",
    detail: "Nắm vững kiến thức cơ bản",
    icon: BookOpen,
    ring: "from-blue-500 to-cyan-400",
  },
  {
    grade: "Lớp 11",
    focus: "Tăng tốc bứt phá",
    detail: "Hiểu sâu, luyện kỹ năng",
    icon: Rocket,
    ring: "from-violet-500 to-blue-400",
  },
  {
    grade: "Lớp 12",
    focus: "Vượt đích thành công",
    detail: "Ôn luyện, chinh phục mục tiêu",
    icon: Flag,
    ring: "from-amber-400 to-orange-500",
  },
];

export default function LearningPath() {
  return (
    <section id="learning-path" className="relative overflow-hidden py-24 lg:py-32">
      <div
        aria-hidden
        className="glow-blob right-[-10%] top-[10%] h-[380px] w-[380px] bg-violet-700/25"
      />
      <div className="relative mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-cyan-300">
            Lộ trình học
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Học theo lộ trình —{" "}
            <span className="text-gradient">hiểu từ gốc, vững đến đích.</span>
          </h2>
        </Reveal>

        <div className="relative mt-20">
          <div className="grid grid-cols-1 gap-12 md:grid-cols-3 md:gap-8">
            {stages.map((s, i) => (
              <Reveal key={s.grade} delay={i * 0.12}>
                <div className="glass glass-hover relative flex h-full flex-col items-start rounded-3xl p-7">
                  <span
                    className={`flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br ${s.ring} text-white shadow-lg`}
                  >
                    <s.icon size={26} />
                  </span>
                  <span className="mt-5 font-mono text-xs uppercase tracking-widest text-muted">
                    {s.grade}
                  </span>
                  <h3 className="mt-1 font-display text-xl font-bold text-ink">
                    {s.focus}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">
                    {s.detail}
                  </p>
                </div>
              </Reveal>
            ))}
          </div>

          {/* Đường quỹ đạo nối 3 giai đoạn — phát sáng nhẹ */}
          <svg
            viewBox="0 0 1000 60"
            preserveAspectRatio="none"
            className="pointer-events-none absolute inset-x-0 bottom-[-2.5rem] hidden h-14 w-full md:block"
            aria-hidden
          >
            <path
              d="M 60 15 Q 330 55 500 30 Q 670 5 940 45"
              stroke="url(#lp-grad)"
              strokeWidth="2"
              strokeLinecap="round"
              strokeDasharray="1 10"
              fill="none"
            />
            <defs>
              <linearGradient id="lp-grad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#3B82F6" />
                <stop offset="50%" stopColor="#8B5CF6" />
                <stop offset="100%" stopColor="#F59E0B" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>
    </section>
  );
}
