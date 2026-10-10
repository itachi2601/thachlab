"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import type { PhysicsAroundPost } from "@/lib/blog";
import { rotatePhysicsAround, vietnamDayIndex } from "@/lib/physics-around";

const OTHERS = 3;

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

  const { featured, others } = rotatePhysicsAround(posts, index, OTHERS);
  const diagram = featured.cover?.endsWith(".svg") ?? false;

  return (
    <section id="physics-everywhere" className="border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="flex flex-wrap items-end justify-between gap-4">
          <div className="max-w-xl">
            <p className="font-mono text-xs uppercase tracking-widest text-primary">Vật lý quanh ta</p>
            <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Những câu hỏi từ đời thường
            </h2>
          </div>
          <Link
            href="/blog/#vat-ly-quanh-ta"
            className="inline-flex min-h-11 items-center gap-1.5 text-sm font-medium text-primary transition hover:text-primary-dark"
          >
            Tất cả bài viết <ArrowRight size={16} />
          </Link>
        </Reveal>

        <div className="mt-10 grid gap-10 lg:grid-cols-12 lg:gap-12">
          <Reveal className={others.length > 0 ? "lg:col-span-7" : "lg:col-span-12"}>
            <Link href={featured.href} className="group block">
              {featured.cover ? (
                <div className="aspect-[16/10] overflow-hidden rounded-xl border border-line bg-panel">
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
              {featured.tag ? (
                <p className="mt-5 font-mono text-xs uppercase tracking-widest text-muted">{featured.tag}</p>
              ) : null}
              <h3 className="mt-2 font-display text-2xl font-bold leading-snug text-ink transition-colors group-hover:text-primary">
                {featured.title}
              </h3>
              <p className="mt-2 max-w-xl text-sm leading-relaxed text-muted">{featured.description}</p>
              <span className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-primary">
                Đọc bài <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              </span>
            </Link>
          </Reveal>

          {others.length > 0 ? (
            <Reveal delay={0.1} className="lg:col-span-5">
              <p className="font-mono text-xs uppercase tracking-widest text-muted">Những câu hỏi khác</p>
              <ul className="mt-4 divide-y divide-line border-y border-line">
                {others.map((post) => (
                  <li key={post.slug}>
                    <Link href={post.href} className="group block py-5">
                      {post.tag ? <p className="text-xs text-muted">{post.tag}</p> : null}
                      <p className="mt-1 font-display text-lg font-semibold leading-snug text-ink transition-colors group-hover:text-primary">
                        {post.title}
                      </p>
                    </Link>
                  </li>
                ))}
              </ul>
            </Reveal>
          ) : null}
        </div>
      </div>
    </section>
  );
}
