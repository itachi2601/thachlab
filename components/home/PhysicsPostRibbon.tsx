"use client";

import { useCallback, useSyncExternalStore } from "react";
import Link from "next/link";
import { PhysicsCuriosityCard } from "@/components/home/PhysicsCuriosityCard";
import type { PhysicsCardData } from "@/lib/physics-card";

export type RibbonPost = PhysicsCardData;

const READ_STORAGE_KEY = "thachlab:read_ribbon_posts";

const EMPTY_READ: ReadonlySet<string> = new Set<string>();

// Bộ nhớ đệm snapshot cho useSyncExternalStore: chỉ đọc localStorage khi giá trị thô thay đổi.
let cachedRaw: string | null = null;
let cachedRead: ReadonlySet<string> = EMPTY_READ;
const readListeners = new Set<() => void>();

function parseReadSlugs(raw: string | null): ReadonlySet<string> {
  if (!raw) return EMPTY_READ;
  try {
    const list: unknown = JSON.parse(raw);
    if (Array.isArray(list)) {
      return new Set(list.filter((item): item is string => typeof item === "string"));
    }
  } catch {
    // Bỏ qua dữ liệu hỏng
  }
  return EMPTY_READ;
}

function getReadSnapshot(): ReadonlySet<string> {
  let raw: string | null = null;
  try {
    raw = localStorage.getItem(READ_STORAGE_KEY);
  } catch {
    // Bỏ qua lỗi truy cập localStorage (chặn cookie, private browsing)
    return EMPTY_READ;
  }
  if (raw === cachedRaw) return cachedRead;
  cachedRaw = raw;
  cachedRead = parseReadSlugs(raw);
  return cachedRead;
}

function getServerReadSnapshot(): ReadonlySet<string> {
  return EMPTY_READ;
}

function subscribeReadSlugs(onStoreChange: () => void) {
  const handleStorage = (event: StorageEvent) => {
    if (event.key === READ_STORAGE_KEY || event.key === null) onStoreChange();
  };
  window.addEventListener("storage", handleStorage);
  readListeners.add(onStoreChange);
  return () => {
    window.removeEventListener("storage", handleStorage);
    readListeners.delete(onStoreChange);
  };
}

function markRibbonPostRead(slug: string) {
  const current = getReadSnapshot();
  if (current.has(slug)) return;
  const next = new Set(current);
  next.add(slug);
  const serialized = JSON.stringify(Array.from(next));
  try {
    localStorage.setItem(READ_STORAGE_KEY, serialized);
  } catch {
    // Bỏ qua lỗi lưu
  }
  cachedRaw = serialized;
  cachedRead = next;
  readListeners.forEach((listener) => listener());
}

/** Dải bài "Vật lý quanh ta": hàng thẻ (ảnh + hook + câu đố) vuốt ngang (không chạy tự động — chữ trôi thì không đọc, không bấm trúng được trên 375px). */
export function PhysicsPostRibbon({ posts, label, total }: { posts: RibbonPost[]; label?: string; total?: number }) {
  const readSlugs = useSyncExternalStore(subscribeReadSlugs, getReadSnapshot, getServerReadSnapshot);

  const handlePostClick = useCallback((slug: string) => {
    markRibbonPostRead(slug);
  }, []);

  if (posts.length === 0) return null;
  return (
    <div>
      <div className="flex items-center justify-between gap-3">
        {label ? <p className="font-mono text-xs uppercase tracking-widest text-muted">{label}</p> : <span />}
        <Link href="/blog/#vat-ly-quanh-ta" className="inline-flex min-h-11 items-center text-sm font-semibold text-primary underline-offset-4 hover:underline">
          Vuốt để xem thêm · Xem tất cả →
        </Link>
      </div>
      {/* Điện thoại: vuốt ngang qua 5 thẻ (thẻ kế lấp ló báo còn nữa). Máy tính: dàn đủ 4 cột, không để trống bên phải. */}
      <ul className="flex snap-x snap-mandatory items-stretch gap-3 overflow-x-auto pb-2 [scrollbar-width:thin] lg:gap-4">
        {posts.map((post) => {
          const isNew = !readSlugs.has(post.slug);
          return (
            <li key={post.slug} className={`w-[82%] shrink-0 snap-start sm:w-80 lg:w-[calc(25%-12px)]`}>
              <PhysicsCuriosityCard card={post} isNew={isNew} compact onOpen={handlePostClick} />
            </li>
          );
        })}
        <li className="flex w-[60%] shrink-0 snap-start sm:w-56 lg:w-56">
          <Link
            href="/blog/#vat-ly-quanh-ta"
            className="flex min-h-44 w-full flex-col items-center justify-center gap-1 rounded-xl border border-dashed border-primary bg-panel p-4 text-center font-semibold text-primary"
          >
            <span className="font-display text-3xl">{total ?? ""}</span>
            <span>Xem tất cả bài →</span>
          </Link>
        </li>
      </ul>
    </div>
  );
}
