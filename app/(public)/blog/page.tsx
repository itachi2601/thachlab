import type { Metadata } from "next";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getAllPosts, type PostMeta } from "@/lib/blog";
import { SITE_URL } from "@/lib/site";

const PHYSICS = "Vật lý quanh ta";

export const metadata: Metadata = {
  title: "Blog Kiến Thức Vật Lý THPT",
  description:
    "Vật lý quanh ta: những câu hỏi đời thường. Và lộ trình học Vật lý THPT theo chương trình GDPT 2018 từ thầy Thạch.",
  alternates: { canonical: "/blog" },
  openGraph: {
    title: "Blog Kiến Thức Vật Lý THPT — ThachLab",
    description:
      "Hai mục riêng: Vật lý quanh ta, và lộ trình học từng lớp.",
    url: `${SITE_URL}/blog`,
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

function PostList({ posts }: { posts: PostMeta[] }) {
  if (posts.length === 0) return null;
  return (
    <div className="space-y-5">
      {posts.map((post) => (
        <Link
          key={post.slug}
          href={`/blog/${post.slug}`}
          className="group block rounded-2xl border border-line bg-panel p-6 transition-all hover:-translate-y-1 hover:border-primary/50"
        >
          <p className="text-sm text-muted">
            <time dateTime={post.date}>{formatDate(post.date)}</time>
            {" · "}
            {post.readingMinutes} phút đọc
          </p>
          {post.tags?.length ? (
            <div className="mt-3 flex flex-wrap gap-2">
              {post.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full border border-line bg-surface-2 px-3 py-1 text-sm text-ink"
                >
                  {tag}
                </span>
              ))}
            </div>
          ) : null}
          <h3 className="mt-2 font-display text-xl font-bold text-ink group-hover:text-primary">
            {post.title}
          </h3>
          <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-muted">
            {post.description}
          </p>
          <span className="mt-4 inline-block text-sm font-semibold text-primary">
            Đọc tiếp →
          </span>
        </Link>
      ))}
    </div>
  );
}

export default function BlogIndexPage() {
  const posts = getAllPosts();
  const physics = posts.filter((post) => post.category === PHYSICS);
  const paths = posts.filter((post) => post.category !== PHYSICS);

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-6 pt-28 pb-20 lg:px-8">
        <p className="font-mono text-xs font-medium tracking-widest text-primary uppercase">
          Blog kiến thức
        </p>
        <h1 className="mt-3 font-display text-3xl font-bold text-ink sm:text-4xl">
          Bài viết
        </h1>
        <p className="mt-3 max-w-2xl text-muted">
          Hai mục riêng. Câu hỏi đời thường nằm ở Vật lý quanh ta. Lộ trình từng lớp nằm ở mục dưới.
        </p>

        <section id="vat-ly-quanh-ta" className="scroll-mt-24 mt-12">
          <h2 className="font-display text-2xl font-bold text-ink">Vật lý quanh ta</h2>
          <p className="mt-2 mb-6 max-w-2xl text-sm leading-relaxed text-muted">
            Vì sao một việc em vẫn gặp lại xảy ra như vậy. Mỗi bài một câu hỏi.
          </p>
          <PostList posts={physics} />
        </section>

        <section id="lo-trinh" className="scroll-mt-24 mt-16 border-t border-line pt-12">
          <h2 className="font-display text-2xl font-bold text-ink">Lộ trình học</h2>
          <p className="mt-2 mb-6 max-w-2xl text-sm leading-relaxed text-muted">
            Mỗi lớp học gì, và nên đi theo thứ tự nào.
          </p>
          <PostList posts={paths} />
        </section>
      </main>
      <Footer />
    </>
  );
}
