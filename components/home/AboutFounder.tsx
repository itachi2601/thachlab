import { Reveal } from "@/components/ui/Reveal";

const facts = [
  { label: "Dạy", value: "KHTN 9 · Vật lý 10–12 · CNC, tiện – phay (CTTC)" },
  { label: "Ngoài giờ", value: "Cơ khí chế tạo · Trượt băng nghệ thuật · Gym mỗi ngày" },
];

const socials = [
  { label: "Facebook", href: "https://www.facebook.com/ngodieuthach" },
  { label: "Instagram", href: "https://www.instagram.com/ngo_dieu_thach" },
  { label: "TikTok", href: "https://www.tiktok.com/@ngo_dieu_thach" },
];

export default function AboutFounder() {
  return (
    <section id="about" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto grid max-w-6xl gap-12 px-6 lg:grid-cols-12 lg:gap-16 lg:px-8">
        <Reveal className="lg:col-span-7">
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Người đứng lớp</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Một chút về thầy Thạch
          </h2>
          <div className="mt-6 space-y-4 text-base leading-relaxed text-muted">
            <p>
              Thầy dạy KHTN 9 và Vật lý THPT, đồng thời dạy sinh viên CTTC về gia công
              CNC, tiện – phay. ThachLab là nơi thầy gom bài giảng, bài tập và đề kiểm
              tra của tất cả các lớp đó vào một chỗ, để em học ở nhà vẫn theo đúng nhịp
              trên lớp.
            </p>
            <p>
              Ngoài giờ dạy, thầy mê cơ khí chế tạo, trượt băng nghệ thuật và đi gym mỗi
              ngày — nên trong bài giảng em sẽ hay gặp ví dụ từ sân băng, phòng tập và
              xưởng máy.
            </p>
          </div>
          <blockquote className="mt-8 border-l-2 border-cyan-300 pl-5">
            <p className="font-display text-xl italic leading-snug text-ink">
              &ldquo;Hiểu bản chất, không học thuộc công thức.&rdquo;
            </p>
          </blockquote>
        </Reveal>

        <Reveal delay={0.1} className="lg:col-span-5">
          <dl className="divide-y divide-line border-y border-line">
            {facts.map((f) => (
              <div key={f.label} className="grid gap-1 py-4 sm:grid-cols-[6.5rem_1fr]">
                <dt className="font-mono text-xs uppercase tracking-widest text-muted">{f.label}</dt>
                <dd className="text-sm text-ink">{f.value}</dd>
              </div>
            ))}
            <div className="grid gap-1 py-4 sm:grid-cols-[6.5rem_1fr]">
              <dt className="font-mono text-xs uppercase tracking-widest text-muted">Theo dõi</dt>
              <dd className="text-sm text-ink">
                <span className="flex flex-wrap gap-x-4 gap-y-1">
                  {socials.map((s) => (
                    <a
                      key={s.label}
                      href={s.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-cyan-300 underline-offset-4 transition hover:text-cyan-200 hover:underline"
                    >
                      {s.label}
                    </a>
                  ))}
                </span>
                <span className="mt-1 block text-muted">3.300+ người theo dõi trên Facebook</span>
              </dd>
            </div>
          </dl>
        </Reveal>
      </div>
    </section>
  );
}
