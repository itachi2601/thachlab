"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";

interface Post {
  id: number;
  created_at: string;
  title: string;
  body: string;
  video_url: string;
}

/** Đổi link YouTube bất kỳ (watch/youtu.be/shorts) thành link nhúng. */
export function toYouTubeEmbed(url: string): string | null {
  const m = url.match(
    /(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{11})/,
  );
  return m ? `https://www.youtube.com/embed/${m[1]}` : null;
}

function PostCard({ post }: { post: Post }) {
  const embed = post.video_url ? toYouTubeEmbed(post.video_url) : null;
  return (
    <article className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
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

export default function PostsPage() {
  const [posts, setPosts] = useState<Post[] | null>(null);

  useEffect(() => {
    if (!supabaseConfigured) return;
    getSupabase()
      .from("posts")
      .select("id, created_at, title, body, video_url")
      .eq("published", true)
      .order("created_at", { ascending: false })
      .then(({ data }) => setPosts((data as Post[]) ?? []));
  }, []);

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Bài <span className="text-gradient">học</span>
        </h1>
        <p className="mt-3 mb-10 text-slate-400">
          Video bài giảng và tài liệu từ thầy Thạch.
        </p>
        {!supabaseConfigured ? (
          <p className="text-slate-400">
            Hệ thống đang được cấu hình, vui lòng quay lại sau.
          </p>
        ) : !posts ? (
          <p className="text-slate-400">Đang tải…</p>
        ) : posts.length === 0 ? (
          <p className="text-slate-400">Chưa có bài học nào.</p>
        ) : (
          <div className="space-y-8">
            {posts.map((p) => (
              <PostCard key={p.id} post={p} />
            ))}
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
