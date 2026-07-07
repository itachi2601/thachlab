"use client";

import { useEffect, useMemo, useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchMyClassIds } from "@/services/classes";
import {
  fetchPublishedPosts,
  visibleTo,
  type PostMeta,
} from "@/services/content";
import { supabaseConfigured } from "@/services/supabase";

/** Đổi link YouTube bất kỳ (watch/youtu.be/shorts) thành link nhúng. */
function toYouTubeEmbed(url: string): string | null {
  const m = url.match(
    /(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{11})/,
  );
  return m ? `https://www.youtube.com/embed/${m[1]}` : null;
}

function PostCard({ post }: { post: PostMeta }) {
  const embed = post.video_url ? toYouTubeEmbed(post.video_url) : null;
  return (
    <article
      id={`post-${post.id}`}
      className="rounded-2xl border border-white/10 bg-[#0B1020] p-6"
    >
      <h2 className="font-display text-xl font-semibold text-white">
        {post.title}
      </h2>
      <p className="mt-1 text-xs text-slate-500">
        {new Date(post.created_at).toLocaleDateString("vi-VN")}
      </p>
      {embed && (
        <div className="mt-4 aspect-video overflow-hidden rounded-xl">
          <iframe
            src={embed}
            title={post.title}
            className="h-full w-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
      )}
      {post.video_url && !embed && (
        <a
          href={post.video_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 inline-block text-sm text-[#3B82F6] hover:underline"
        >
          Xem video ↗
        </a>
      )}
      {post.body && (
        <p className="mt-4 whitespace-pre-wrap text-sm leading-relaxed text-slate-300">
          {post.body}
        </p>
      )}
    </article>
  );
}

export default function NewsPage() {
  const { session, profile } = useAuth();
  const [posts, setPosts] = useState<PostMeta[] | null>(null);
  const [myClassIds, setMyClassIds] = useState<number[] | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    if (!supabaseConfigured) return;
    fetchPublishedPosts().then(setPosts);
  }, []);

  const isStudent = Boolean(session) && profile?.role !== "admin";

  useEffect(() => {
    if (!isStudent || !session) return;
    fetchMyClassIds(session.user.id).then(setMyClassIds);
  }, [isStudent, session]);

  // khách/quản trị thấy tất cả; học sinh chỉ thấy lớp mình
  const effectiveClassIds = isStudent ? myClassIds : null;

  const visible = useMemo(
    () =>
      (posts ?? []).filter(
        (p) =>
          visibleTo(p.classIds, effectiveClassIds) &&
          p.title.toLowerCase().includes(search.toLowerCase()),
      ),
    [posts, effectiveClassIds, search],
  );

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Tin <span className="text-gradient">tức</span>
        </h1>
        <p className="mt-3 mb-6 text-slate-400">
          Bài giảng, video và thông báo từ thầy Thạch
          {effectiveClassIds !== null && " — hiển thị theo lớp của em"}.
        </p>
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="🔍 Tìm bài viết…"
          className="mb-8 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none"
        />
        {!supabaseConfigured ? (
          <p className="text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : !posts ? (
          <SkeletonGrid count={2} />
        ) : visible.length === 0 ? (
          <p className="text-slate-400">Không có bài viết nào.</p>
        ) : (
          <div className="space-y-8">
            {visible.map((p) => (
              <PostCard key={p.id} post={p} />
            ))}
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
