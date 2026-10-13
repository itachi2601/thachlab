"use client";

import Link from "next/link";
import { ArrowRight, Lightbulb } from "lucide-react";
import { usePhysicsAroundPosts } from "@/components/home/PhysicsAroundContext";

/** Cuối bài học: "Đọc thêm" các bài Vật lý quanh ta gắn với bài này (khớp qua mục "Em đã học ở đâu?" của bài blog). */
export default function AroundReadMore({ lessonId }: { lessonId: number }) {
  const posts = usePhysicsAroundPosts().filter((p) => p.lessonIds?.includes(lessonId)).slice(0, 2);
  if (posts.length === 0) return null;
  return (
    <section aria-label="Đọc thêm" className="mt-6 rounded-2xl border border-line bg-panel p-4">
      <p className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-primary">
        <Lightbulb size={14} aria-hidden /> Đọc thêm · Vật lý quanh ta
      </p>
      <ul className="mt-2 divide-y divide-line">
        {posts.map((post) => (
          <li key={post.slug}>
            <Link href={post.href} className="group flex min-h-14 items-center gap-3 py-2">
              <span className="flex-1 text-[15px] font-semibold leading-snug text-ink group-hover:text-primary">{post.title}</span>
              <span className="shrink-0 text-[13px] text-muted">{post.readingMinutes} phút</span>
              <ArrowRight size={16} className="shrink-0 text-muted group-hover:text-primary" aria-hidden />
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
