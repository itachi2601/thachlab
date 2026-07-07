import type { MetadataRoute } from "next";
import { getAllPosts } from "@/lib/blog";

// Bắt buộc với output: export — route sinh file tĩnh lúc build.
export const dynamic = "force-static";

const SITE = "https://thachlab.id.vn";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes: MetadataRoute.Sitemap = [
    { url: `${SITE}/`, changeFrequency: "weekly", priority: 1 },
    { url: `${SITE}/lop-hoc/`, changeFrequency: "weekly", priority: 0.9 },
    { url: `${SITE}/blog/`, changeFrequency: "weekly", priority: 0.8 },
    { url: `${SITE}/kiem-tra/`, changeFrequency: "monthly", priority: 0.7 },
    { url: `${SITE}/tin-tuc/`, changeFrequency: "weekly", priority: 0.6 },
    { url: `${SITE}/dang-ky/`, changeFrequency: "yearly", priority: 0.6 },
  ];

  const posts: MetadataRoute.Sitemap = getAllPosts().map((post) => ({
    url: `${SITE}/blog/${post.slug}/`,
    lastModified: post.date,
    changeFrequency: "monthly",
    priority: 0.8,
  }));

  return [...staticRoutes, ...posts];
}
