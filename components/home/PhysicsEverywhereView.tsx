"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import type { PhysicsAroundPost } from "@/lib/blog";
import { rotatePhysicsAround, vietnamDayIndex } from "@/lib/physics-around";


export default function PhysicsEverywhereView({
  posts,
  initialIndex,
}: {
  posts: PhysicsAroundPost[];
  initialIndex: number;
}) {
  // HTML tĩnh gắn chỉ số lúc build. Sau khi tải, chỉnh theo ngày lịch Việt Nam
  // để bài xoay tua giữa các lần deploy.
  const [index, setIndex] = useState(initialIndex);
  useEffect(() => {
    const today = vietnamDayIndex() % posts.length;
    if (today !== initialIndex) setIndex(today);
  }, [initialIndex, posts.length]);

  const { featured, others: ribbon } = rotatePhysicsAround(posts, index, posts.length - 1);
  const diagram = featured.cover?.endsWith(".svg") ?? false;

  return (
    <section id="physics-everywhere" className="border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="flex flex-wrap items-end justify-between gap-4">
          <div className="max-w-xl">
            <p className="font-mono text-xs uppercase tracking-widest text-primary">Vật lý quanh ta</p>
            <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Giải mã hiện tượng đời sống
            </h2>
          </div>
          <Link
            href="/blog/#vat-ly-quanh-ta"
            className="inline-flex min-h-11 items-center gap-1.5 text-sm font-medium text-primary transition hover:text-primary-dark"
          >
            Tất cả bài viết <ArrowRight size={16} />
          </Link>
        </Reveal>

        <Reveal className="mt-10 grid items-center gap-6 lg:grid-cols-12 lg:gap-10">
          <Link href={featured.href} className="group contents">
            {featured.cover ? (
              <div className="aspect-[16/10] overflow-hidden rounded-xl border border-line bg-panel lg:col-span-6">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={featured.cover}
                  alt=""
                  loading="lazy"
                  decoding="async"
                  className={
                    diagram
                      ? "h-full w-full object-contain"
                      : "h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.02]"
                  }
                />
              </div>
            ) : null}
            <div className={featured.cover ? "lg:col-span-6" : "lg:col-span-12"}>
              {featured.tag ? (
                <p className="font-mono text-xs uppercase tracking-widest text-muted">{featured.tag}</p>
              ) : null}
              <h3 className="mt-2 font-display text-2xl font-bold leading-snug text-ink transition-colors group-hover:text-primary">
                {featured.title}
              </h3>
              <p className="mt-2 max-w-xl text-sm leading-relaxed text-muted">{featured.description}</p>
              <span className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-primary">
                Đọc bài <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              </span>
            </div>
          </Link>
        </Reveal>

        {ribbon.length > 0 ? (
          <div className="mt-10">
            <p className="font-mono text-xs uppercase tracking-widest text-muted">Hiện tượng khác</p>
            <div className="marquee-posts-wrap mt-4 overflow-hidden [mask-image:linear-gradient(90deg,transparent,black_6%,black_94%,transparent)]">
              <ul className="marquee marquee-posts">
                {[0, 1].map((dup) => (
                  <li key={dup} className="flex shrink-0 items-center gap-4" aria-hidden={dup === 1 || undefined}>
                    {ribbon.map((post) => (
                      <Link
                        key={post.slug}
                        href={post.href}
                        tabIndex={dup === 1 ? -1 : undefined}
                        className="group flex min-h-11 items-center rounded-lg border border-line bg-panel px-4 py-2.5 text-sm font-medium text-ink transition hover:border-primary hover:text-primary"
                      >
                        <span className="whitespace-nowrap">{post.title}</span>
                      </Link>
                    ))}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : null}
      </div>
    </section>
  );
}
