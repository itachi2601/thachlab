"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export type RibbonPost = { slug: string; title: string; href: string };

const READ_STORAGE_KEY = "thachlab:read_ribbon_posts";

/** Dải bài "Vật lý quanh ta" chạy ngang. Dừng khi rê chuột / focus (globals.css), giảm chuyển động → hàng cuộn tay. */
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
      <div className="marquee-posts-wrap mt-2 overflow-hidden [mask-image:linear-gradient(90deg,transparent,black_6%,black_94%,transparent)]">
        <ul className="marquee marquee-posts">
          {[0, 1].map((dup) => (
            <li key={dup} className="flex shrink-0 items-center gap-4" aria-hidden={dup === 1 || undefined}>
              {posts.map((post) => {
                const isNew = !readSlugs.has(post.slug);
                return (
                  <Link
                    key={post.slug}
                    href={post.href}
                    onClick={() => handlePostClick(post.slug)}
                    tabIndex={dup === 1 ? -1 : undefined}
                    className="flex min-h-11 items-center gap-2 rounded-lg border border-line bg-panel px-4 py-2 text-sm font-medium text-ink transition hover:border-primary hover:text-primary"
                  >
                    <span className="whitespace-nowrap">{post.title}</span>
                    {isNew && (
                      <span className="inline-flex items-center rounded border border-primary/25 bg-primary/10 px-1.5 py-0.5 font-mono text-[10px] font-bold uppercase tracking-wider text-primary">
                        new
                      </span>
                    )}
                  </Link>
                );
              })}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
