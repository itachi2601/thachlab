"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowRight, Lightbulb } from "lucide-react";
import { usePhysicsAroundPosts } from "@/components/home/PhysicsAroundContext";
import { vietnamDayIndex } from "@/lib/physics-around";

/** Thẻ "Góc tò mò": MỘT bài Vật lý quanh ta mỗi ngày, đặt sau việc cần làm hôm nay (N1, C2, M5). */
export default function CuriosityCard() {
  const posts = usePhysicsAroundPosts();
  // Chỉ render sau khi tải chậm ở trình duyệt (ThptStudentHome ssr:false) nên đọc ngày thẳng, không lệch hydrate.
  const [day] = useState(() => vietnamDayIndex());
  if (posts.length === 0) return null;
  const post = posts[day % posts.length];
  return (
    <Link
      href={post.href}
      className="group flex min-h-20 items-center gap-3 rounded-2xl border border-line bg-panel p-3 transition hover:border-primary sm:p-4"
    >
      {post.cover ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={post.cover} alt="" loading="lazy" decoding="async" className="h-16 w-16 shrink-0 rounded-xl border border-line bg-surface-2 object-cover sm:h-20 sm:w-20" />
      ) : (
        <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary sm:h-20 sm:w-20">
          <Lightbulb size={26} aria-hidden />
        </span>
      )}
      <div className="min-w-0 flex-1">
        <p className="font-mono text-xs uppercase tracking-widest text-primary">Góc tò mò · Vật lý quanh ta</p>
        <p className="mt-1 line-clamp-2 text-[15px] font-semibold leading-snug text-ink group-hover:text-primary">{post.title}</p>
        <p className="mt-1 text-[13px] text-muted">{post.readingMinutes} phút đọc</p>
      </div>
      <ArrowRight size={18} className="shrink-0 text-muted group-hover:text-primary" aria-hidden />
    </Link>
  );
}
