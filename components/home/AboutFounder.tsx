import { Reveal } from "@/components/ui/Reveal";

const traits = [
  { label: "Giảng dạy", value: "KHTN 9 & Vật lý THPT" },
  { label: "Đam mê", value: "Cơ khí chế tạo" },
  { label: "Thể thao", value: "Trượt băng nghệ thuật" },
  { label: "Rèn luyện", value: "Gym mỗi ngày" },
];

const socials = [
  { label: "Facebook", href: "https://www.facebook.com/ngodieuthach" },
  { label: "Instagram", href: "https://www.instagram.com/ngo_dieu_thach" },
  { label: "TikTok", href: "https://www.tiktok.com/@ngo_dieu_thach" },
];

export default function AboutFounder() {
  return (
    <section id="about" className="relative overflow-hidden py-24 lg:py-32">
      <div
        aria-hidden
        className="glow-blob left-[-8%] bottom-[0%] h-[360px] w-[360px] bg-blue-700/25"
      />
      <div className="relative mx-auto max-w-6xl px-6 lg:px-8">
        <div className="grid grid-cols-1 items-start gap-16 lg:grid-cols-[0.9fr_1.1fr]">
          <Reveal>
            <p className="font-mono text-xs font-medium uppercase tracking-widest text-cyan-300">
              Người sáng lập
            </p>
            <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Sống giữa <span className="text-gradient">phương trình</span> và{" "}
              <span className="text-gradient">chuyển động.</span>
            </h2>
            <p className="mt-3 font-mono text-sm text-muted">
              Living between equation and motion.
            </p>
            <p className="mt-6 text-base leading-relaxed text-muted">
              ThachLab được sáng lập bởi thầy Thạch — giáo viên trực tiếp giảng
              dạy KHTN 9 và Vật lý THPT. Với niềm yêu thích cơ khí chế tạo,
              những giờ trên sân trượt băng nghệ thuật và phòng gym, thầy tin
              rằng dạy học và sống đẹp là một: sống khỏe mạnh, có đam mê, và
              không ngừng học hỏi. Mỗi bài giảng đều bắt nguồn từ một điều đơn
              giản — mỗi bài học nên bắt đầu bằng một câu hỏi.
            </p>

            <blockquote className="mt-8 border-l-2 border-accent pl-6">
              <p className="font-display text-xl italic leading-snug text-ink">
                &ldquo;Hiểu bản chất, không học thuộc công thức.&rdquo;
              </p>
            </blockquote>

            <div className="mt-8 flex flex-wrap items-center gap-3">
              {socials.map((s) => (
                <a
                  key={s.label}
                  href={s.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="glass glass-hover rounded-full px-5 py-2 text-sm font-medium text-ink"
                >
                  {s.label}
                </a>
              ))}
              <span className="text-sm text-muted">
                3.300+ người theo dõi trên Facebook
              </span>
            </div>
          </Reveal>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {traits.map((t, i) => (
              <Reveal key={t.label} delay={i * 0.08}>
                <div className="glass glass-hover h-full rounded-3xl p-6">
                  <p className="font-mono text-xs uppercase tracking-widest text-muted">
                    {t.label}
                  </p>
                  <p className="mt-2 font-display text-lg font-semibold text-ink">
                    {t.value}
                  </p>
                </div>
              </Reveal>
            ))}

            <Reveal delay={0.3} className="col-span-full">
              <div className="rounded-3xl bg-gradient-to-r from-blue-600 via-violet-600 to-blue-600 p-[1px]">
                <div className="rounded-3xl bg-[#0B1020] p-6">
                  <p className="font-mono text-xs uppercase tracking-widest text-white/60">
                    Triết lý giảng dạy
                  </p>
                  <p className="mt-2 font-display text-lg font-semibold text-white">
                    Passionate teaching can inspire students — dạy bằng đam mê
                    để truyền cảm hứng.
                  </p>
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
