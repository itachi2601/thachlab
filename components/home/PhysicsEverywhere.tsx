import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

const featured = {
  tag: "Gym & Thể thao",
  title: "Vì sao cơ bắp co lại khi nâng tạ?",
  desc: "Tín hiệu thần kinh, sợi actin – myosin, lực kéo của cơ, xương làm đòn bẩy và khớp làm điểm xoay — một buổi tập là một bài cơ học.",
  href: "/blog/vi-sao-co-bap-co-lai-khi-nang-ta",
  cover: "/images/blog/co-bap-co-lai-khi-nang-ta-cover.webp",
};

const others = [
  { tag: "Trượt băng nghệ thuật", title: "Vì sao vận động viên xoay nhanh hơn khi thu tay lại?" },
  { tag: "Xe điện & Năng lượng", title: "Vì sao phanh tái sinh giúp xe điện sạc lại pin?" },
  { tag: "Kiến trúc & Cầu đường", title: "Vì sao Taipei 101 treo một con lắc khổng lồ giữa toà nhà?" },
];

export default function PhysicsEverywhere() {
  return (
    <section id="physics-everywhere" className="border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="flex flex-wrap items-end justify-between gap-4">
          <div className="max-w-xl">
            <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Vật lý quanh ta</p>
            <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Những câu hỏi từ đời thường
            </h2>
          </div>
          <Link
            href="/blog"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-cyan-300 transition hover:text-cyan-200"
          >
            Tất cả bài viết <ArrowRight size={16} />
          </Link>
        </Reveal>

        <div className="mt-10 grid gap-10 lg:grid-cols-12 lg:gap-12">
          <Reveal className="lg:col-span-7">
            <Link href={featured.href} className="group block">
              <div className="aspect-[16/10] overflow-hidden rounded-xl border border-line">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={featured.cover}
                  alt=""
                  loading="lazy"
                  decoding="async"
                  className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.02]"
                />
              </div>
              <p className="mt-5 font-mono text-xs uppercase tracking-widest text-muted">{featured.tag}</p>
              <h3 className="mt-2 font-display text-2xl font-bold leading-snug text-ink transition-colors group-hover:text-cyan-200">
                {featured.title}
              </h3>
              <p className="mt-2 max-w-xl text-sm leading-relaxed text-muted">{featured.desc}</p>
              <span className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-cyan-300">
                Đọc bài <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              </span>
            </Link>
          </Reveal>

          <Reveal delay={0.1} className="lg:col-span-5">
            <p className="font-mono text-xs uppercase tracking-widest text-muted">Những câu hỏi khác</p>
            <ul className="mt-4 divide-y divide-line border-y border-line">
              {others.map((q) => (
                <li key={q.title} className="py-5">
                  <p className="text-xs text-muted">{q.tag}</p>
                  <p className="mt-1 font-display text-lg font-semibold leading-snug text-ink">{q.title}</p>
                </li>
              ))}
            </ul>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
