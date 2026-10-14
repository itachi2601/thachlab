import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";
import { marked } from "marked";
import type { PhotoCredit, PhysicsCardData, PostQuiz } from "@/lib/physics-card";

// Thư mục chứa bài viết Markdown (đọc tại thời điểm build — Server Component).
const BLOG_DIR = join(process.cwd(), "content", "blog");

export interface PostFrontmatter {
  title: string;
  description: string;
  date: string; // ISO yyyy-mm-dd
  keywords?: string[];
  category?: string;
  tags?: string[];
  cover?: string; // đường dẫn ảnh đại diện (dùng cho OG/mạng xã hội)
  // Thẻ "Vật lý quanh ta" (trang chủ + /blog) — xem docs/ANH-VAT-LY-QUANH-TA.md
  hook?: string;
  badge?: string;
  quiz?: PostQuiz;
  photo?: string; // ảnh thẻ 16:9 thật (webp), khác `cover`
  photoAlt?: string;
  photoCredit?: PhotoCredit;
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
    category: fm.category,
    tags: fm.tags ?? [],
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

export interface PhysicsAroundPost extends PhysicsCardData {
  description: string;
  tag: string;
  cover: string | null;
  date: string;
  /** id các bài học liên quan, lấy từ link trong mục "Em đã học ở đâu?" — để gắn bài đọc vào cuối bài học. */
  lessonIds: number[];
}

const GRADE_TAG = /^(Lớp \d+|KHTN \d+)$/u;

function topicTag(tags: string[] | undefined): string {
  return (tags ?? []).find((tag) => !GRADE_TAG.test(tag)) ?? "";
}

function publicFileExists(urlPath: string): boolean {
  return existsSync(join(process.cwd(), "public", urlPath.replace(/^\//, "")));
}

/** Ảnh bìa: ưu tiên webp cùng tên, rồi cover trong frontmatter, rồi hình đầu tiên trong bài. */
function resolveCover(cover: string | undefined, markdown: string): string | null {
  const candidates: string[] = [];
  if (cover) {
    if (/\.(jpe?g|png)$/i.test(cover)) {
      candidates.push(cover.replace(/\.(jpe?g|png)$/i, ".webp"));
    }
    candidates.push(cover);
  }
  const inline = markdown.match(/!\[[^\]]*]\((\/images\/[^)\s]+)\)/);
  if (inline) candidates.push(inline[1]);
  return candidates.find((url) => publicFileExists(url)) ?? null;
}

function validQuiz(quiz: PostQuiz | undefined): PostQuiz | undefined {
  if (!quiz || !quiz.question || !quiz.why || !Array.isArray(quiz.options)) return undefined;
  if (quiz.options.length < 2 || quiz.options.length > 4) return undefined;
  if (!Number.isInteger(quiz.answer) || quiz.answer < 0 || quiz.answer >= quiz.options.length) return undefined;
  return quiz;
}

/** Ảnh thẻ chỉ được dùng khi file có thật VÀ ghi công đủ tác giả, giấy phép, link nguồn (cam kết ở /dieu-khoan). */
function resolvePhoto(fm: PostFrontmatter): string | null {
  const credit = fm.photoCredit;
  if (!fm.photo || !credit?.author || !credit.license || !credit.sourceUrl) return null;
  return publicFileExists(fm.photo) ? fm.photo : null;
}

function buildCard(slug: string, fm: PostFrontmatter, markdown: string): PhysicsCardData {
  const photo = resolvePhoto(fm);
  return {
    slug,
    title: fm.title,
    href: `/blog/${slug}`,
    badge: fm.badge,
    hook: fm.hook,
    quiz: validQuiz(fm.quiz),
    photo,
    photoAlt: photo ? (fm.photoAlt ?? fm.title) : undefined,
    photoCredit: photo ? fm.photoCredit : undefined,
    readingMinutes: readingTime(markdown),
  };
}

/** id bài học trong mục "## Em đã học ở đâu?" (link /lop-hoc/bai?id=N). */
export function relatedLessonIds(markdown: string): number[] {
  const section = markdown.split(/^## /m).find((part) => part.startsWith("Em đã học ở đâu"));
  if (!section) return [];
  const ids = [...section.matchAll(/\/lop-hoc\/bai\?id=(\d+)/g)].map((m) => Number(m[1]));
  return [...new Set(ids)];
}

/** Bài "Vật lý quanh ta" đã viết, theo thứ tự đăng — để trang chủ xoay tua. */
export function getPhysicsAroundPosts(): PhysicsAroundPost[] {
  return getPostSlugs()
    .map((slug) => {
      const raw = readFileSync(join(BLOG_DIR, `${slug}.md`), "utf8");
      const { data, content } = matter(raw);
      const fm = data as PostFrontmatter;
      if (fm.category !== "Vật lý quanh ta") return null;
      const post: PhysicsAroundPost = {
        ...buildCard(slug, fm, content),
        description: fm.description,
        tag: topicTag(fm.tags),
        cover: resolveCover(fm.cover, content),
        date: fm.date,
        lessonIds: relatedLessonIds(content),
      };
      return post;
    })
    .filter((post): post is PhysicsAroundPost => post !== null)
    .sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.slug < b.slug ? -1 : 1));
}
