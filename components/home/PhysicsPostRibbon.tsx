"use client";

import { useEffect, useState } from "react";
import { PhysicsCuriosityCard } from "@/components/home/PhysicsCuriosityCard";
import type { PhysicsCardData } from "@/lib/physics-card";

export type RibbonPost = PhysicsCardData;

const READ_STORAGE_KEY = "thachlab:read_ribbon_posts";

/** Dải bài "Vật lý quanh ta": hàng thẻ (ảnh + hook + câu đố) vuốt ngang (không chạy tự động — chữ trôi thì không đọc, không bấm trúng được trên 375px). */
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
      <ul className="mt-2 flex snap-x snap-mandatory items-stretch gap-3 overflow-x-auto pb-2 [scrollbar-width:thin]">
        {posts.map((post) => {
          const isNew = !readSlugs.has(post.slug);
          return (
            <li key={post.slug} className="w-[88%] shrink-0 snap-start sm:w-80">
              <PhysicsCuriosityCard card={post} isNew={isNew} compact onOpen={handlePostClick} />
            </li>
          );
        })}
      </ul>
    </div>
  );
}
