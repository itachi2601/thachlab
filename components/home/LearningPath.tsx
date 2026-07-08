import Link from "next/link";
import {
  Atom,
  BookOpen,
  CheckCircle2,
  ClipboardCheck,
  Flag,
  Magnet,
  Microscope,
  Rocket,
  Waves,
  Zap,
} from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

const stages = [
  {
    grade: "Lớp 9",
    shortLabel: "KHTN 9",
    articleHref: "/blog/lo-trinh-hoc-khtn-9-phan-vat-ly-thi-chuyen",
    focus: "KHTN - phần Vật lý",
    detail:
      "Đi từng bậc: chắc nền KHTN, mở rộng tư duy rồi luyện HSG hoặc định hướng thi chuyên Vật lý.",
    topics: ["Điện học", "Từ học", "Quang học", "Luyện chuyên"],
    checkpoints: ["Nắm định luật Ohm", "Vẽ được mạch điện", "Hiểu từ trường và thấu kính"],
    scene: "khtn9",
    icon: Microscope,
    ring: "from-emerald-400 to-lime-300",
    image: "/images/learning-path/khtn-9-vat-ly.png",
  },
  {
    grade: "Lớp 10",
    shortLabel: "Vật lý 10",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-10-dung-de-mat-goc",
    focus: "Nhập môn & nền tảng cơ học",
    detail:
      "Làm quen cách học mới: ít toán đố, nhiều thực tế. Trọng tâm là đọc – vẽ đồ thị chuyển động.",
    topics: ["Động học", "Định luật Newton", "Năng lượng", "Chuyển động tròn"],
    checkpoints: ["Đọc được đồ thị chuyển động", "Vẽ lực đúng", "Biết dùng bảo toàn năng lượng"],
    scene: "class10",
    icon: BookOpen,
    ring: "from-blue-500 to-cyan-400",
    image: "/images/learning-path/vat-ly-10.jpg",
  },
  {
    grade: "Lớp 11",
    shortLabel: "Vật lý 11",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-11-nam-de-duoi-nhat",
    focus: "Dao động, sóng & điện",
    detail:
      "Năm bản lề nhiều khái niệm trừu tượng nhất. Học chắc bản chất qua thí nghiệm và mô phỏng.",
    topics: ["Dao động", "Sóng cơ & ánh sáng", "Điện trường", "Dòng điện không đổi"],
    checkpoints: ["Phân tích dao động", "Hiểu sóng và ánh sáng", "Làm chủ điện trường/mạch DC"],
    scene: "class11",
    icon: Rocket,
    ring: "from-violet-500 to-blue-400",
    image: "/images/learning-path/vat-ly-11.jpg",
  },
  {
    grade: "Lớp 12",
    shortLabel: "Vật lý 12",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-12-muon-tang-diem",
    focus: "Nhiệt, khí & vật lý hiện đại",
    detail:
      "Điểm mới của chương trình 2018: Nhiệt học chuyển lên lớp 12, giảm điện xoay chiều phức tạp. Luyện đề chuẩn cấu trúc thi mới.",
    topics: ["Vật lý nhiệt", "Khí lý tưởng", "Từ trường", "Lượng tử & hạt nhân"],
    checkpoints: ["Giải bài nhiệt/khí", "Hiểu từ trường", "Luyện đề theo cấu trúc thi"],
    scene: "class12",
    icon: Flag,
    ring: "from-amber-400 to-orange-500",
    image: "/images/learning-path/vat-ly-12.jpg",
  },
];

function RoadmapScene({ scene }: { scene: string }) {
  if (scene === "khtn9") {
    return (
      <div className="relative h-full overflow-hidden bg-gradient-to-br from-slate-950 via-emerald-950 to-cyan-950">
        <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(34,211,238,0.13)_1px,transparent_1px)] bg-[length:18px_18px]" />
        <div className="absolute left-5 top-7 h-12 w-8 rounded-md border border-yellow-300 bg-yellow-300/20 shadow-[0_0_28px_rgba(250,204,21,0.35)]" />
        <div className="absolute left-[3.25rem] top-12 h-1 w-24 bg-yellow-300 shadow-[0_0_16px_rgba(250,204,21,0.8)]" />
        <div className="absolute right-10 top-7 flex h-14 w-14 items-center justify-center rounded-full border border-yellow-200 bg-yellow-300/10 text-yellow-200 shadow-[0_0_24px_rgba(250,204,21,0.5)]">
          <Zap size={24} />
        </div>
        <div className="absolute bottom-5 left-10 h-10 w-16 rounded-t-full border-[10px] border-b-0 border-cyan-300/80" />
        <Magnet className="absolute bottom-5 right-8 text-red-300 drop-shadow-[0_0_12px_rgba(248,113,113,0.8)]" size={42} />
      </div>
    );
  }

  if (scene === "class10") {
    return (
      <div className="relative h-full overflow-hidden bg-gradient-to-br from-slate-950 via-blue-950 to-cyan-950">
        <div className="absolute inset-x-7 bottom-6 h-px bg-cyan-200/40" />
        <div className="absolute left-8 top-12 h-24 w-40 rounded-[50%] border-t-2 border-dashed border-cyan-300/80" />
        <div className="absolute left-16 top-16 h-4 w-4 rounded-full bg-yellow-300 shadow-[0_0_20px_rgba(250,204,21,0.9)]" />
        <div className="absolute bottom-6 right-12 h-10 w-16 rounded-lg border border-cyan-300/60 bg-cyan-300/10" />
        <div className="absolute bottom-[4.5rem] right-20 h-16 w-1 rotate-[-35deg] rounded-full bg-blue-300" />
        <div className="absolute bottom-28 right-14 border-b-[10px] border-l-[8px] border-r-[8px] border-b-blue-300 border-l-transparent border-r-transparent" />
        <span className="absolute bottom-12 left-10 font-mono text-xs text-cyan-200">F = ma</span>
      </div>
    );
  }

  if (scene === "class11") {
    return (
      <div className="relative h-full overflow-hidden bg-gradient-to-br from-slate-950 via-violet-950 to-blue-950">
        <Waves className="absolute left-5 top-8 text-cyan-200 drop-shadow-[0_0_14px_rgba(34,211,238,0.8)]" size={58} />
        <div className="absolute bottom-6 left-7 right-7 h-12">
          <div className="h-full rounded-[50%] border-t-2 border-cyan-300/80" />
          <div className="-mt-12 h-full rounded-[50%] border-b-2 border-violet-300/70" />
        </div>
        <div className="absolute right-8 top-7 h-20 w-20 rounded-full border border-cyan-200/30">
          <Atom className="absolute left-5 top-5 text-cyan-100" size={38} />
        </div>
        <span className="absolute right-8 bottom-8 rounded-full border border-violet-300/30 bg-violet-300/10 px-3 py-1 font-mono text-xs text-violet-100">
          E
        </span>
      </div>
    );
  }

  return (
    <div className="relative h-full overflow-hidden bg-gradient-to-br from-slate-950 via-amber-950 to-rose-950">
      <div className="absolute left-8 top-6 h-16 w-8 rounded-full border border-orange-200/50 bg-orange-300/10">
        <div className="absolute bottom-1 left-1 right-1 h-9 rounded-full bg-orange-300 shadow-[0_0_22px_rgba(251,146,60,0.75)]" />
      </div>
      <Atom className="absolute right-8 top-6 text-yellow-100 drop-shadow-[0_0_16px_rgba(254,240,138,0.8)]" size={54} />
      <div className="absolute bottom-6 left-8 h-12 w-24 rounded-[50%] border-t-2 border-cyan-300/80" />
      <div className="absolute bottom-7 right-10 h-12 w-12 rounded-full border border-amber-200/40 bg-amber-300/10" />
      <span className="absolute bottom-9 right-14 font-mono text-xs text-amber-100">PV</span>
    </div>
  );
}

export default function LearningPath() {
  return (
    <section id="learning-path" className="relative overflow-hidden py-24 lg:py-32">
      <div
        aria-hidden
        className="glow-blob right-[-10%] top-[10%] h-[380px] w-[380px] bg-violet-700/25"
      />
      <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
        <Reveal className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-cyan-300">
            Lộ trình học
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Học theo lộ trình —{" "}
            <span className="text-gradient">hiểu từ gốc, vững đến đích.</span>
          </h2>
        </Reveal>

        <Reveal delay={0.1}>
          <div
            id="learning-roadmap"
            className="mt-10 scroll-mt-24 rounded-3xl border border-cyan-300/15 bg-cyan-300/[0.04] p-5 shadow-2xl shadow-cyan-950/20 md:p-6"
          >
            <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
              <div className="max-w-2xl">
                <p className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-cyan-200">
                  <CheckCircle2 size={14} />
                  Roadmap tự kiểm tra
                </p>
                <h3 className="mt-3 font-display text-2xl font-bold text-ink">
                  Em đang ở đâu trên hành trình Vật lý?
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">
                  Tick các mốc đã làm được để biết mình nên củng cố KHTN 9, xây nền
                  cơ học lớp 10, vượt phần trừu tượng lớp 11 hay bước vào luyện đề lớp 12.
                </p>
              </div>
              <Link
                href="/kiem-tra"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-cyan-300 px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-200"
              >
                <ClipboardCheck size={18} />
                Kiểm tra đầu vào
              </Link>
            </div>

            <div className="relative mt-8 grid gap-4 lg:grid-cols-4">
              <div
                aria-hidden
                className="absolute left-10 right-10 top-8 hidden h-px bg-gradient-to-r from-emerald-300 via-cyan-300 to-amber-300 lg:block"
              />
              {stages.map((stage, index) => (
                <div key={stage.shortLabel} className="relative">
                  <div
                    className={`relative z-20 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br ${stage.ring} text-white shadow-lg shadow-cyan-950/30`}
                  >
                    <stage.icon size={24} />
                  </div>
                  <div className="mt-4 overflow-hidden rounded-2xl border border-white/10 bg-[#080D1A]/80">
                    <div
                      className="relative h-28"
                      role="img"
                      aria-label={`Scene minh họa chặng ${stage.shortLabel}`}
                    >
                      <RoadmapScene scene={stage.scene} />
                      <div className="absolute inset-0 bg-gradient-to-t from-[#080D1A] via-[#080D1A]/20 to-transparent" />
                      <div className="absolute bottom-3 left-3 flex items-center gap-2">
                        <span className="rounded-full bg-black/40 px-2.5 py-1 text-[11px] font-semibold text-white backdrop-blur">
                          Chặng {index + 1}
                        </span>
                        <span className="rounded-full border border-white/15 bg-white/10 px-2.5 py-1 text-[11px] text-white backdrop-blur">
                          {stage.grade}
                        </span>
                      </div>
                    </div>

                    <div className="p-4">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <p className="font-mono text-[11px] uppercase tracking-widest text-slate-500">
                          Tự check
                        </p>
                        <h4 className="mt-1 font-display text-base font-bold text-white">
                          {stage.shortLabel}
                        </h4>
                      </div>
                      <span className="rounded-full border border-white/10 px-2.5 py-1 text-[11px] text-slate-300">
                        {stage.grade}
                      </span>
                    </div>
                    <ul className="mt-4 space-y-2">
                      {stage.checkpoints.map((item) => (
                        <li key={item} className="flex items-start gap-2 text-sm text-slate-300">
                          <input
                            type="checkbox"
                            aria-label={`${stage.shortLabel}: ${item}`}
                            className="mt-1 h-4 w-4 rounded border-white/20 bg-white/5 accent-cyan-300"
                          />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        <div className="relative mt-16">
          <div className="grid grid-cols-1 gap-12 md:grid-cols-2 md:gap-8 xl:grid-cols-4">
            {stages.map((s, i) => (
              <Reveal key={s.grade} delay={i * 0.12}>
                <div className="glass glass-hover relative flex h-full flex-col items-start overflow-hidden rounded-3xl">
                  <div className="relative h-44 w-full">
                    <img
                      src={s.image}
                      alt={`Sơ đồ tóm tắt chương trình ${s.grade.toLowerCase()}`}
                      className="h-full w-full object-cover object-top"
                      loading="lazy"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#0b0b16] via-transparent to-transparent" />
                    <span
                      className={`absolute bottom-3 left-3 flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br ${s.ring} text-white shadow-lg`}
                    >
                      <s.icon size={22} />
                    </span>
                  </div>
                  <div className="flex flex-1 flex-col items-start p-7 pt-5">
                    <span className="font-mono text-xs uppercase tracking-widest text-muted">
                      {s.grade}
                    </span>
                    <h3 className="mt-1 font-display text-xl font-bold text-ink">
                      {s.focus}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-muted">
                      {s.detail}
                    </p>
                    <ul className="mt-4 flex flex-wrap gap-1.5">
                      {s.topics.map((t) => (
                        <li
                          key={t}
                          className="rounded-full border border-white/10 bg-white/5 px-2.5 py-1 text-xs text-slate-300"
                        >
                          {t}
                        </li>
                      ))}
                    </ul>
                    {"articleHref" in s && s.articleHref && (
                      <Link
                        href={s.articleHref}
                        className="mt-5 inline-flex items-center rounded-full border border-cyan-300/30 px-4 py-2 text-sm font-semibold text-cyan-200 transition hover:border-cyan-300 hover:bg-cyan-300/10"
                      >
                        Đọc lộ trình {s.grade.toLowerCase()} →
                      </Link>
                    )}
                  </div>
                </div>
              </Reveal>
            ))}
          </div>

          {/* Đường quỹ đạo nối các giai đoạn — phát sáng nhẹ */}
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
