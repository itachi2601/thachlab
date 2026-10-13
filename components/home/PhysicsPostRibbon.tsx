"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export type RibbonPost = { slug: string; title: string; href: string };

const READ_STORAGE_KEY = "thachlab:read_ribbon_posts";

/** Dải bài "Vật lý quanh ta": hàng thẻ TĨNH vuốt ngang (không chạy tự động — chữ trôi thì không đọc, không bấm trúng được trên 375px). */
export function PhysicsPostRibbon({ posts, label }: { posts: RibbonPost[]; label?: string }) {
  const [readSlugs, setReadSlugs] = useState<Set<string>>(() => new Set());

  useEffect(() => {
    try {
      const raw = localStorage.getItem(READ_STORAGE_KEY);
      if (raw) {
        const list = JSON.parse(raw);
        if (Array.isArray(list)) {
          setReadSlugs(new Set(list));
        }
      }
    } catch {
      // Bỏ qua lỗi truy cập localStorage (chặn cookie, private browsing)
    }
  }, []);

  const handlePostClick = (slug: string) => {
    setReadSlugs((prev) => {
      if (prev.has(slug)) return prev;
      const next = new Set(prev);
      next.add(slug);
      try {
        localStorage.setItem(READ_STORAGE_KEY, JSON.stringify(Array.from(next)));
      } catch {
        // Bỏ qua lỗi lưu
      }
      return next;
    });
  };

  if (posts.length === 0) return null;
  return (
    <div>
      {label ? <p className="font-mono text-xs uppercase tracking-widest text-muted">{label}</p> : null}
      <ul className="mt-2 flex snap-x snap-mandatory gap-3 overflow-x-auto pb-2 [scrollbar-width:thin]">
        {posts.map((post) => {
          const isNew = !readSlugs.has(post.slug);
          return (
            <li key={post.slug} className="w-[82%] shrink-0 snap-start sm:w-72">
              <Link
                href={post.href}
                onClick={() => handlePostClick(post.slug)}
                className="flex min-h-14 items-center gap-2 rounded-xl border border-line bg-panel px-4 py-3 text-[15px] font-semibold leading-snug text-ink transition hover:border-primary hover:text-primary"
              >
                <span className="line-clamp-2 flex-1">{post.title}</span>
                {isNew && (
                  <span className="inline-flex shrink-0 items-center rounded border border-primary/25 bg-primary/10 px-1.5 py-0.5 font-mono text-xs font-bold uppercase tracking-wider text-primary">
                    mới
                  </span>
                )}
              </Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
