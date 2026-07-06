import { ArrowRight, Building2, Cog, Dumbbell, Snowflake } from "lucide-react";

const scenes = [
  {
    tag: "Trượt băng tốc độ",
    title: "Vì sao người trượt băng cúi người để tăng tốc?",
    icon: Snowflake,
    tint: "from-sky-500/30 to-sky-900/10 text-sky-300",
  },
  {
    tag: "Gym & Thể thao",
    title: "Vì sao cơ bắp co lại khi nâng tạ?",
    icon: Dumbbell,
    tint: "from-orange-500/30 to-orange-900/10 text-orange-300",
  },
  {
    tag: "Cơ khí chế tạo",
    title: "Vì sao các bánh răng ăn khớp hoàn hảo?",
    icon: Cog,
    tint: "from-slate-500/30 to-slate-900/10 text-slate-300",
  },
  {
    tag: "Kiến trúc & Cầu đường",
    title: "Vì sao cầu treo có thể nâng đỡ khối lượng lớn?",
    icon: Building2,
    tint: "from-indigo-500/30 to-indigo-900/10 text-indigo-300",
  },
];

export default function PhysicsEverywhere() {
  return (
    <section id="physics-everywhere" className="bg-white py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-[#2563EB]">
            Vật lý quanh ta
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Vật lý hiện diện trong mọi khoảnh khắc.
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {scenes.map((s) => (
            <a
              key={s.title}
              href="#"
              className="group flex flex-col overflow-hidden rounded-2xl border border-line bg-white transition-shadow hover:shadow-xl hover:shadow-black/5"
            >
              {/* Ảnh minh hoạ tạm thời — thay bằng ảnh thật tại
                  public/images/scenes/<ten-file>.jpg khi có. */}
              <div
                className={`flex h-40 items-center justify-center bg-gradient-to-br ${s.tint} bg-ink`}
              >
                <s.icon size={40} strokeWidth={1.5} />
              </div>
              <div className="flex flex-1 flex-col gap-2 p-5">
                <span className="text-xs font-medium text-muted">{s.tag}</span>
                <h3 className="font-display text-base font-semibold leading-snug text-ink">
                  {s.title}
                </h3>
                <span className="mt-auto flex items-center gap-1 pt-2 text-sm font-medium text-[#2563EB] transition-transform group-hover:translate-x-1">
                  Tìm hiểu <ArrowRight size={16} />
                </span>
              </div>
            </a>
          ))}
        </div>

        <div className="mt-10 flex justify-center">
          <button className="rounded-full border border-line px-6 py-3 text-sm font-medium text-ink transition-colors hover:border-[#2563EB]/40 hover:text-[#2563EB]">
            Khám phá thêm
          </button>
        </div>
      </div>
    </section>
  );
}
