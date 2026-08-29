"use client";

import { useEffect, useState } from "react";
import { fetchPublishedPosts, visibleToCourse, type PostMeta } from "@/services/content";

const CONTENT_TYPE_LABELS: Record<string, string> = {
  thong_bao: "Thông báo",
  tai_lieu: "Tài liệu",
  video: "Video",
};

export default function CncCourseAnnouncements({ courseId }: { courseId: number }) {
  const [posts, setPosts] = useState<PostMeta[]>([]);

  useEffect(() => {
    let cancelled = false;
    fetchPublishedPosts()
      .then((all) => {
        if (cancelled) return;
        setPosts(all.filter((p) => visibleToCourse(p.courseIds, p.classIds, courseId)));
      })
      .catch(() => setPosts([]));
    return () => {
      cancelled = true;
    };
  }, [courseId]);

  if (posts.length === 0) return null;

  return (
    <section className="mb-6 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <h2 className="font-display text-base font-semibold text-white">Thông báo</h2>
      <div className="mt-3 space-y-3">
        {posts.slice(0, 5).map((p) => (
          <article key={p.id} className="rounded-xl border border-white/5 bg-white/[.03] p-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-full bg-primary/15 px-2.5 py-0.5 text-[11px] font-semibold text-primary">
                {CONTENT_TYPE_LABELS[p.content_type] ?? p.content_type}
              </span>
              <span className="text-xs text-slate-500">
                {new Date(p.created_at).toLocaleDateString("vi-VN")}
              </span>
            </div>
            <p className="mt-2 font-medium text-white">{p.title}</p>
            {p.body && <p className="mt-1 whitespace-pre-line text-sm text-slate-400">{p.body}</p>}
            {p.video_url && (
              <a
                href={p.video_url}
                target="_blank"
                rel="noreferrer"
                className="mt-2 inline-block text-sm font-medium text-primary hover:underline"
              >
                ▶ Xem video
              </a>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
