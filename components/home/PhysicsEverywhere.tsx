import { ArrowRight, Building2, Cog, Dumbbell, Snowflake } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

const scenes = [
  {
    tag: "Trượt băng tốc độ",
    title: "Vì sao người trượt băng cúi người để tăng tốc?",
    icon: Snowflake,
    tint: "from-sky-500/40 to-blue-900/20 text-sky-300",
    glow: "group-hover:shadow-sky-500/30",
  },
  {
    tag: "Gym & Thể thao",
    title: "Vì sao cơ bắp co lại khi nâng tạ?",
    icon: Dumbbell,
    tint: "from-orange-500/40 to-rose-900/20 text-orange-300",
    glow: "group-hover:shadow-orange-500/30",
  },
  {
    tag: "Cơ khí chế tạo",
    title: "Vì sao các bánh răng ăn khớp hoàn hảo?",
    icon: Cog,
    tint: "from-slate-400/40 to-slate-900/20 text-slate-300",
    glow: "group-hover:shadow-slate-400/30",
  },
  {
    tag: "Kiến trúc & Cầu đường",
    title: "Vì sao cầu treo có thể nâng đỡ khối lượng lớn?",
    icon: Building2,
    tint: "from-violet-500/40 to-indigo-900/20 text-violet-300",
    glow: "group-hover:shadow-violet-500/30",
  },
];

export default function PhysicsEverywhere() {
  return (
    <section id="physics-everywhere" className="relative overflow-hidden py-24 lg:py-32">
      <div
        aria-hidden
        className="glow-blob left-[-12%] top-[20%] h-[360px] w-[360px] bg-blue-700/25"
      />
      <div className="relative mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-cyan-300">
            Vật lý quanh ta
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Vật lý hiện diện trong{" "}
            <span className="text-gradient">mọi khoảnh khắc.</span>
          </h2>
        </Reveal>

        <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {scenes.map((s, i) => (
            <Reveal key={s.title} delay={i * 0.08}>
              <a
                href="#"
                className={`glass glass-hover group flex h-full flex-col overflow-hidden rounded-2xl transition-shadow ${s.glow}`}
              >
                <div
                  className={`flex h-40 items-center justify-center bg-gradient-to-br ${s.tint} transition-transform duration-500 group-hover:scale-[1.03]`}
                >
                  <s.icon
                    size={44}
                    strokeWidth={1.5}
                    className="transition-transform duration-500 group-hover:rotate-6 group-hover:scale-110"
                  />
                </div>
                <div className="flex flex-1 flex-col gap-2 p-5">
                  <span className="text-xs font-medium text-muted">{s.tag}</span>
                  <h3 className="font-display text-base font-semibold leading-snug text-ink">
                    {s.title}
                  </h3>
                  <span className="mt-auto flex items-center gap-1 pt-2 text-sm font-medium text-cyan-300 transition-transform group-hover:translate-x-1">
                    Tìm hiểu <ArrowRight size={16} />
                  </span>
                </div>
              </a>
            </Reveal>
          ))}
        </div>

        <div className="mt-10 flex justify-center">
          <button className="glass glass-hover rounded-full px-6 py-3 text-sm font-medium text-ink">
            Khám phá thêm
          </button>
        </div>
      </div>
    </section>
  );
}
