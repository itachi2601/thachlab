import Image from "next/image";
import { Reveal } from "@/components/ui/Reveal";
import { CONTACT } from "@/lib/contact";

// Sở thích để 1 dòng, xuống cuối khối — giữ vì là chất riêng của thầy, không phải bằng cấp.
const facts = [
  { label: "Ngoài giờ", value: "Cơ khí chế tạo · Trượt băng nghệ thuật · Gym mỗi ngày" },
];

const socials = [
  { label: "Facebook", href: "https://www.facebook.com/ngodieuthach" },
  { label: "Instagram", href: "https://www.instagram.com/ngo_dieu_thach" },
  { label: "TikTok", href: "https://www.tiktok.com/@ngo_dieu_thach" },
];

/**
 * Khối "Người đứng lớp" — sắp theo thứ tự phụ huynh cần khi tìm chỗ học cho con:
 * ảnh thật (bên trái, trên cùng ở mobile) → tên + số năm/trường + đang dạy gì → câu nói về cách dạy
 * → sở thích (1 dòng, cuối) → mạng xã hội. Chỉ dùng dữ kiện có thật trong lib/contact.ts: tuyệt đối
 * không thêm bằng cấp, giải thưởng, thành tích.
 */
export default function AboutFounder() {
  const hasPhoto = Boolean(CONTACT.teacherPhoto);
  const introduction = [
    CONTACT.years ? `${CONTACT.years} năm dạy Vật lý` : "",
    CONTACT.school,
  ].filter(Boolean);

  return (
    <section id="about" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto grid max-w-6xl gap-12 px-6 lg:grid-cols-12 lg:gap-16 lg:px-8">
        {hasPhoto && (
          <Reveal className="lg:col-span-5">
            <Image
              src={CONTACT.teacherPhoto}
              alt="Thầy Thạch chụp cùng học sinh trong lớp học"
              width={800}
              height={600}
              sizes="(min-width: 1024px) 460px, (min-width: 640px) 88vw, 100vw"
              loading="lazy"
              className="h-auto w-full rounded-2xl border border-line"
            />
          </Reveal>
        )}

        <Reveal delay={0.1} className={hasPhoto ? "lg:col-span-7" : "lg:col-span-12"}>
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Người đứng lớp</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Một chút về thầy Thạch
          </h2>
          {introduction.length > 0 && (
            <p className="mt-5 font-display text-lg leading-snug text-ink">{introduction.join(" · ")}</p>
          )}
          <p className="mt-2 text-base leading-relaxed text-muted">
            Dạy KHTN 9 và Vật lý 10–12 theo chương trình 2018, CNC – tiện – phay (CTTC).
          </p>
          <p className="mt-4 text-base leading-relaxed text-muted">
            ThachLab là nơi thầy gom bài giảng, bài tập và đề kiểm tra của tất cả các
            lớp đó vào một chỗ, để em học ở nhà vẫn theo đúng nhịp trên lớp.
          </p>
          <blockquote className="mt-8 border-l-2 border-cyan-300 pl-5">
            <p className="font-display text-xl italic leading-snug text-ink">
              &ldquo;Hiểu bản chất, không học thuộc công thức.&rdquo;
            </p>
          </blockquote>

          <dl className="mt-8 divide-y divide-line border-y border-line">
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
