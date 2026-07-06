import { BookOpen, Flag, Rocket } from "lucide-react";

const stages = [
  {
    grade: "Lớp 10",
    focus: "Xây nền tảng",
    detail: "Nắm vững kiến thức cơ bản",
    icon: BookOpen,
  },
  {
    grade: "Lớp 11",
    focus: "Tăng tốc bứt phá",
    detail: "Hiểu sâu, luyện kỹ năng",
    icon: Rocket,
  },
  {
    grade: "Lớp 12",
    focus: "Vượt đích thành công",
    detail: "Ôn luyện, chinh phục mục tiêu",
    icon: Flag,
  },
];

export default function LearningPath() {
  return (
    <section id="learning-path" className="bg-white py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-[#2563EB]">
            Lộ trình học
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Học theo lộ trình – Hiểu từ gốc, vững đến đích.
          </h2>
        </div>

        <div className="relative mt-20">
          <div className="grid grid-cols-1 gap-12 md:grid-cols-3 md:gap-8">
            {stages.map((s) => (
              <div key={s.grade} className="relative flex flex-col items-start">
                <span className="flex h-14 w-14 items-center justify-center rounded-full bg-[#2563EB]/10 text-[#2563EB]">
                  <s.icon size={26} />
                </span>
                <span className="mt-4 font-mono text-xs uppercase tracking-widest text-muted">
                  {s.grade}
                </span>
                <h3 className="mt-1 font-display text-xl font-bold text-ink">
                  {s.focus}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">
                  {s.detail}
                </p>
              </div>
            ))}
          </div>

          {/* Đường quỹ đạo nối 3 giai đoạn, cùng ngôn ngữ hình học với Hero. */}
          <svg
            viewBox="0 0 1000 60"
            preserveAspectRatio="none"
            className="pointer-events-none absolute inset-x-0 bottom-[-2.5rem] hidden h-14 w-full md:block"
            aria-hidden
          >
            <path
              d="M 60 15 Q 330 55 500 30 Q 670 5 940 45"
              stroke="#2563EB"
              strokeOpacity="0.25"
              strokeWidth="2"
              strokeLinecap="round"
              strokeDasharray="1 10"
              fill="none"
            />
          </svg>
        </div>
      </div>
    </section>
  );
}
