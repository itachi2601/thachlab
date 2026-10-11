import Link from "next/link";

export type RibbonPost = { slug: string; title: string; href: string };

/** Dải bài "Vật lý quanh ta" chạy ngang. Dừng khi rê chuột / focus (globals.css), giảm chuyển động → hàng cuộn tay. */
export function PhysicsPostRibbon({ posts, label }: { posts: RibbonPost[]; label?: string }) {
  if (posts.length === 0) return null;
  return (
    <div>
      {label ? <p className="font-mono text-xs uppercase tracking-widest text-muted">{label}</p> : null}
      <div className="marquee-posts-wrap mt-3 overflow-hidden [mask-image:linear-gradient(90deg,transparent,black_6%,black_94%,transparent)]">
        <ul className="marquee marquee-posts">
          {[0, 1].map((dup) => (
            <li key={dup} className="flex shrink-0 items-center gap-4" aria-hidden={dup === 1 || undefined}>
              {posts.map((post) => (
                <Link
                  key={post.slug}
                  href={post.href}
                  tabIndex={dup === 1 ? -1 : undefined}
                  className="flex min-h-11 items-center rounded-lg border border-line bg-panel px-4 py-2.5 text-sm font-medium text-ink transition hover:border-primary hover:text-primary"
                >
                  <span className="whitespace-nowrap">{post.title}</span>
                </Link>
              ))}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
