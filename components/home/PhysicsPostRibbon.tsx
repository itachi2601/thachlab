"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { PhysicsCuriosityCard } from "@/components/home/PhysicsCuriosityCard";
import type { PhysicsCardData } from "@/lib/physics-card";

export type RibbonPost = PhysicsCardData;

const READ_STORAGE_KEY = "thachlab:read_ribbon_posts";

/** Dải bài "Vật lý quanh ta": hàng thẻ (ảnh + hook + câu đố) vuốt ngang (không chạy tự động — chữ trôi thì không đọc, không bấm trúng được trên 375px). */
export function PhysicsPostRibbon({ posts, label, total }: { posts: RibbonPost[]; label?: string; total?: number }) {
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
      <div className="flex items-center justify-between gap-3">
        {label ? <p className="font-mono text-xs uppercase tracking-widest text-muted">{label}</p> : <span />}
        <Link href="/blog/#vat-ly-quanh-ta" className="inline-flex min-h-11 items-center text-sm font-semibold text-primary underline-offset-4 hover:underline">
          Vuốt để xem thêm · Xem tất cả →
        </Link>
      </div>
      {/* Điện thoại: vuốt ngang qua 5 thẻ (thẻ kế lấp ló báo còn nữa). Máy tính: dàn đủ 4 cột, không để trống bên phải. */}
      <ul className="flex snap-x snap-mandatory items-stretch gap-3 overflow-x-auto pb-2 [scrollbar-width:thin] lg:gap-4">
        {posts.map((post) => {
          const isNew = !readSlugs.has(post.slug);
          return (
            <li key={post.slug} className={`w-[82%] shrink-0 snap-start sm:w-80 lg:w-[calc(25%-12px)]`}>
              <PhysicsCuriosityCard card={post} isNew={isNew} compact onOpen={handlePostClick} />
            </li>
          );
        })}
        <li className="flex w-[60%] shrink-0 snap-start sm:w-56 lg:w-56">
          <Link
            href="/blog/#vat-ly-quanh-ta"
            className="flex min-h-44 w-full flex-col items-center justify-center gap-1 rounded-xl border border-dashed border-primary bg-panel p-4 text-center font-semibold text-primary"
          >
            <span className="font-display text-3xl">{total ?? ""}</span>
            <span>Xem tất cả bài →</span>
          </Link>
        </li>
      </ul>
    </div>
  );
}
