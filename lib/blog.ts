import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";
import { marked } from "marked";

// Thư mục chứa bài viết Markdown (đọc tại thời điểm build — Server Component).
const BLOG_DIR = join(process.cwd(), "content", "blog");

export interface PostFrontmatter {
  title: string;
  description: string;
  date: string; // ISO yyyy-mm-dd
  keywords?: string[];
  cover?: string; // đường dẫn ảnh đại diện (dùng cho OG/mạng xã hội)
  author?: string;
}

export interface PostMeta extends PostFrontmatter {
  slug: string;
  readingMinutes: number;
}

export interface Post extends PostMeta {
  contentHtml: string;
}

marked.setOptions({ gfm: true, breaks: false });

function readingTime(markdown: string): number {
  const words = markdown.trim().split(/\s+/).length;
  return Math.max(1, Math.round(words / 200)); // ~200 từ/phút
}

/** Danh sách slug (tên file .md không đuôi) — dùng cho generateStaticParams. */
export function getPostSlugs(): string[] {
  return readdirSync(BLOG_DIR)
    .filter((f) => f.endsWith(".md"))
    .map((f) => f.replace(/\.md$/, ""));
}

export function getPostBySlug(slug: string): Post {
  const raw = readFileSync(join(BLOG_DIR, `${slug}.md`), "utf8");
  const { data, content } = matter(raw);
  const fm = data as PostFrontmatter;
  return {
    slug,
    title: fm.title,
    description: fm.description,
    date: fm.date,
    keywords: fm.keywords ?? [],
    cover: fm.cover,
    author: fm.author ?? "Thầy Thạch",
    readingMinutes: readingTime(content),
    contentHtml: marked.parse(content) as string,
  };
}

/** Tất cả bài, mới nhất trước — cho trang danh sách và sitemap. */
export function getAllPosts(): PostMeta[] {
  return getPostSlugs()
    .map((slug) => {
      const { contentHtml: _omit, ...meta } = getPostBySlug(slug);
      return meta;
    })
    .sort((a, b) => (a.date < b.date ? 1 : -1));
}
