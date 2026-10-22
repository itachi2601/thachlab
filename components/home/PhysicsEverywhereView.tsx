"use client";

import { useCallback, useSyncExternalStore } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import type { PhysicsAroundPost } from "@/lib/blog";
import { rotatePhysicsAround, vietnamDayIndex } from "@/lib/physics-around";

// Nguồn ngoài (ngày lịch) chỉ đọc một lần sau khi hydrate, không cần subscribe.
const subscribeNoop = () => () => {};


export default function PhysicsEverywhereView({
  posts,
  initialIndex,
}: {
  posts: PhysicsAroundPost[];
  initialIndex: number;
}) {
  // HTML tĩnh gắn chỉ số lúc build. Sau khi tải, chỉnh theo ngày lịch Việt Nam
  // để bài xoay tua giữa các lần deploy.
  const getSnapshot = useCallback(() => vietnamDayIndex() % posts.length, [posts.length]);
  const getServerSnapshot = useCallback(() => initialIndex, [initialIndex]);
  const index = useSyncExternalStore(subscribeNoop, getSnapshot, getServerSnapshot);

  const { featured, others } = rotatePhysicsAround(posts, index, 2);

  return (
    <section id="physics-everywhere" className="border-t border-line py-14 lg:py-20">
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

        <Reveal className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 lg:gap-6">
          {[featured, ...others].map((post) => (
            <Link
              key={post.slug}
              href={post.href}
              className="group flex flex-col overflow-hidden rounded-xl border border-line bg-panel transition hover:border-primary"
            >
              {post.cover ? (
                <div className="aspect-[16/10] overflow-hidden border-b border-line bg-surface-2">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={post.cover}
                    alt=""
                    loading="lazy"
                    decoding="async"
                    className={
                      post.cover.endsWith(".svg")
                        ? "h-full w-full object-contain"
                        : "h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.02]"
                    }
                  />
                </div>
              ) : null}
              <div className="flex flex-1 flex-col p-4">
                {post.tag ? <p className="font-mono text-xs uppercase tracking-widest text-muted">{post.tag}</p> : null}
                <h3 className="mt-1.5 font-display text-lg font-bold leading-snug text-ink transition-colors group-hover:text-primary">
                  {post.title}
                </h3>
                <span className="mt-auto inline-flex min-h-11 items-center gap-1.5 pt-2 text-sm font-medium text-primary">
                  Đọc bài <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
                </span>
              </div>
            </Link>
          ))}
        </Reveal>

      </div>
    </section>
  );
}
