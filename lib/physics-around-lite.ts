import { getPhysicsAroundPosts, getPostBySlug } from "@/lib/blog";
import type { AroundPostLite } from "@/components/home/PhysicsAroundContext";

/** Danh sách gọn cho layout (server) truyền xuống client: /tai-khoan và /lop-hoc. */
export function getPhysicsAroundLite(): AroundPostLite[] {
  return getPhysicsAroundPosts().map((p) => ({
    slug: p.slug,
    title: p.title,
    href: p.href,
    tag: p.tag,
    cover: p.cover,
    readingMinutes: getPostBySlug(p.slug).readingMinutes,
    lessonIds: p.lessonIds,
  }));
}
