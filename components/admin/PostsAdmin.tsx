"use client";

import { useCallback, useEffect, useState } from "react";
import { getSupabase } from "@/services/supabase";

interface Post {
  id: number;
  created_at: string;
  title: string;
  body: string;
  video_url: string;
  published: boolean;
}

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none";

export default function PostsAdmin() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [title, setTitle] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [body, setBody] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const reload = useCallback(() => {
    getSupabase()
      .from("posts")
      .select("*")
      .order("created_at", { ascending: false })
      .then(({ data }) => setPosts((data as Post[]) ?? []));
  }, []);

  useEffect(reload, [reload]);

  async function createPost(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const { error } = await getSupabase().from("posts").insert({
      title: title.trim(),
      video_url: videoUrl.trim(),
      body: body.trim(),
    });
    setBusy(false);
    if (error) {
      setError(error.message);
      return;
    }
    setTitle("");
    setVideoUrl("");
    setBody("");
    reload();
  }

  return (
    <div className="space-y-8">
      <form
        onSubmit={createPost}
        className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6"
      >
        <h2 className="font-display text-lg font-semibold text-white">
          Đăng bài mới
        </h2>
        <input
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Tiêu đề bài học"
          className={inputCls}
        />
        <input
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
          placeholder="Link YouTube (không bắt buộc)"
          className={inputCls}
        />
        <textarea
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Nội dung / mô tả (không bắt buộc)"
          rows={4}
          className={inputCls}
        />
        {error && <p className="text-sm text-red-400">{error}</p>}
        <button
          type="submit"
          disabled={busy}
          className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8] disabled:opacity-50"
        >
          {busy ? "Đang đăng…" : "Đăng bài"}
        </button>
      </form>

      <div className="space-y-3">
        {posts.map((p) => (
          <div
            key={p.id}
            className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-5 py-4"
          >
            <div>
              <p className="font-medium text-white">{p.title}</p>
              <p className="text-xs text-slate-500">
                {new Date(p.created_at).toLocaleString("vi-VN")}
                {p.video_url && " · có video"}
                {!p.published && " · đang ẩn"}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={async () => {
                  await getSupabase()
                    .from("posts")
                    .update({ published: !p.published })
                    .eq("id", p.id);
                  reload();
                }}
                className="rounded-full border border-white/15 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-white/30"
              >
                {p.published ? "Ẩn" : "Hiện"}
              </button>
              <button
                onClick={async () => {
                  if (!confirm(`Xóa bài "${p.title}"?`)) return;
                  await getSupabase().from("posts").delete().eq("id", p.id);
                  reload();
                }}
                className="rounded-full border border-red-500/30 px-3 py-1.5 text-xs font-medium text-red-300 hover:border-red-500/60"
              >
                Xóa
              </button>
            </div>
          </div>
        ))}
        {posts.length === 0 && (
          <p className="text-sm text-slate-400">Chưa có bài đăng nào.</p>
        )}
      </div>
    </div>
  );
}
