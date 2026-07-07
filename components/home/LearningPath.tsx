import Link from "next/link";
import { BookOpen, Flag, Rocket } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

const stages = [
  {
    grade: "Lớp 10",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-10-dung-de-mat-goc",
    focus: "Nhập môn & nền tảng cơ học",
    detail:
      "Làm quen cách học mới: ít toán đố, nhiều thực tế. Trọng tâm là đọc – vẽ đồ thị chuyển động.",
    topics: ["Động học", "Định luật Newton", "Năng lượng", "Chuyển động tròn"],
    icon: BookOpen,
    ring: "from-blue-500 to-cyan-400",
  },
  {
    grade: "Lớp 11",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-11-nam-de-duoi-nhat",
    focus: "Dao động, sóng & điện",
    detail:
      "Năm bản lề nhiều khái niệm trừu tượng nhất. Học chắc bản chất qua thí nghiệm và mô phỏng.",
    topics: ["Dao động", "Sóng cơ & ánh sáng", "Điện trường", "Dòng điện không đổi"],
    icon: Rocket,
    ring: "from-violet-500 to-blue-400",
  },
  {
    grade: "Lớp 12",
    focus: "Nhiệt, khí & vật lý hiện đại",
    detail:
      "Điểm mới của chương trình 2018: Nhiệt học chuyển lên lớp 12, giảm điện xoay chiều phức tạp. Luyện đề chuẩn cấu trúc thi mới.",
    topics: ["Vật lý nhiệt", "Khí lý tưởng", "Từ trường", "Lượng tử & hạt nhân"],
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
