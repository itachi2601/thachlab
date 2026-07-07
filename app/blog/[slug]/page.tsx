import type { Metadata } from "next";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import BlogCta from "@/components/blog/BlogCta";
import { getPostBySlug, getPostSlugs } from "@/lib/blog";

const SITE = "https://thachlab.id.vn";

export function generateStaticParams() {
  return getPostSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  const url = `${SITE}/blog/${slug}`;
  return {
    // absolute để không bị template "%s | ThachLab" ở layout cộng thêm lần nữa
    title: { absolute: `${post.title} | ThachLab` },
    description: post.description,
    keywords: post.keywords,
    authors: [{ name: post.author ?? "Thầy Thạch" }],
    alternates: { canonical: `/blog/${slug}` },
    openGraph: {
      title: post.title,
      description: post.description,
      url,
      siteName: "ThachLab",
      locale: "vi_VN",
      type: "article",
      publishedTime: post.date,
      authors: [post.author ?? "Thầy Thạch"],
      ...(post.cover ? { images: [{ url: post.cover }] } : {}),
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
      description: post.description,
      ...(post.cover ? { images: [post.cover] } : {}),
    },
  };
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("vi-VN", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  const url = `${SITE}/blog/${slug}`;

  // Structured data: bài viết + breadcrumb — giúp Google hiển thị rich result.
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BlogPosting",
        headline: post.title,
        description: post.description,
        datePublished: post.date,
        dateModified: post.date,
        inLanguage: "vi-VN",
        author: { "@type": "Person", name: post.author ?? "Thầy Thạch" },
        publisher: {
          "@type": "Organization",
          name: "ThachLab",
          logo: { "@type": "ImageObject", url: `${SITE}/images/logo.png` },
        },
        mainEntityOfPage: { "@type": "WebPage", "@id": url },
        ...(post.cover ? { image: `${SITE}${post.cover}` } : {}),
        keywords: (post.keywords ?? []).join(", "),
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Trang chủ", item: SITE },
          { "@type": "ListItem", position: 2, name: "Blog", item: `${SITE}/blog` },
          { "@type": "ListItem", position: 3, name: post.title, item: url },
        ],
      },
    ],
  };

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pt-28 pb-20 lg:px-8">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />

        <nav aria-label="Breadcrumb" className="text-sm text-slate-500">
          <Link href="/blog" className="text-[#3B82F6] hover:underline">
            Blog
          </Link>{" "}
          / <span>Kiến thức Vật lý THPT</span>
        </nav>

        <article className="mt-4">
          <h1 className="font-display text-3xl font-bold leading-tight text-white sm:text-4xl">
            {post.title}
          </h1>
          <p className="mt-4 text-sm text-slate-500">
            <time dateTime={post.date}>{formatDate(post.date)}</time>
            {" · "}
            {post.readingMinutes} phút đọc {" · "}
            {post.author}
          </p>

          <div
            className="blog-prose mt-8"
            dangerouslySetInnerHTML={{ __html: post.contentHtml }}
          />

          <BlogCta />
        </article>

        <div className="mt-10">
          <Link href="/blog" className="text-sm text-[#3B82F6] hover:underline">
            ← Xem tất cả bài viết
          </Link>
        </div>
      </main>
      <Footer />
    </>
  );
}
