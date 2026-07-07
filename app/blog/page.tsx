import type { Metadata } from "next";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getAllPosts } from "@/lib/blog";

export const metadata: Metadata = {
  title: "Blog Kiến Thức Vật Lý THPT",
  description:
    "Bài viết chia sẻ lộ trình học, mẹo ôn thi và kiến thức Vật lý THPT theo chương trình GDPT 2018 từ thầy Thạch.",
  alternates: { canonical: "/blog" },
  openGraph: {
    title: "Blog Kiến Thức Vật Lý THPT — ThachLab",
    description:
      "Lộ trình học, mẹo ôn thi và kiến thức Vật lý THPT theo chương trình mới 2018.",
    url: "https://thachlab.id.vn/blog",
    type: "website",
  },
};

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("vi-VN", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export default function BlogIndexPage() {
  const posts = getAllPosts();

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-6 pt-28 pb-20 lg:px-8">
        <p className="font-mono text-xs font-medium tracking-widest text-cyan-300 uppercase">
          Blog kiến thức
        </p>
        <h1 className="mt-3 font-display text-3xl font-bold text-white sm:text-4xl">
          Kiến thức &amp; lộ trình{" "}
          <span className="text-gradient">Vật lý THPT</span>
        </h1>
        <p className="mt-3 mb-10 max-w-2xl text-slate-400">
          Chia sẻ lộ trình học, mẹo ôn thi và cách hiểu Vật lý theo chương trình
          mới 2018 — viết bởi thầy Thạch.
        </p>

        {posts.length === 0 ? (
          <p className="text-slate-400">Chưa có bài viết nào.</p>
        ) : (
          <div className="space-y-5">
            {posts.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="group block rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/50"
              >
                <p className="text-xs text-slate-500">
                  <time dateTime={post.date}>{formatDate(post.date)}</time> ·{" "}
                  {post.readingMinutes} phút đọc
                </p>
                <h2 className="mt-2 font-display text-xl font-bold text-white group-hover:text-[#3B82F6]">
                  {post.title}
                </h2>
                <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-slate-400">
                  {post.description}
                </p>
                <span className="mt-4 inline-block text-sm font-semibold text-[#3B82F6]">
                  Đọc tiếp →
                </span>
              </Link>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
