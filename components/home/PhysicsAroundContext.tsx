"use client";

import { createContext, useContext } from "react";

export type AroundPostLite = { slug: string; title: string; href: string; tag: string; cover: string | null; readingMinutes: number; lessonIds?: number[] };

const Ctx = createContext<AroundPostLite[]>([]);

/** Layout (server) đọc bài "Vật lý quanh ta" lúc build rồi truyền xuống — trang HS không thêm request nào. */
export function PhysicsAroundProvider({ posts, children }: { posts: AroundPostLite[]; children: React.ReactNode }) {
  return <Ctx.Provider value={posts}>{children}</Ctx.Provider>;
}

export function usePhysicsAroundPosts() {
  return useContext(Ctx);
}
