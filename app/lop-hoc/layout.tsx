import AuthedShell from "@/components/auth/AuthedShell";
import { PhysicsAroundProvider } from "@/components/home/PhysicsAroundContext";
import { getPhysicsAroundLite } from "@/lib/physics-around-lite";

export default function Layout({ children }: { children: React.ReactNode }) {
  const posts = getPhysicsAroundLite();
  return (
    <>
      {/* /lop-hoc luôn cần /data/catalog.json (danh mục lớp/chương/bài, xem
          services/static-content.ts) — preload để trình duyệt tải song song với trang
          thay vì chờ JS chạy xong mới bắt đầu fetch. React/Next hoist <link> này vào
          <head> dù đang render trong layout con (không phải root layout). */}
      <link rel="preload" as="fetch" href="/data/catalog.json" crossOrigin="anonymous" />
      <PhysicsAroundProvider posts={posts}>
        <AuthedShell>{children}</AuthedShell>
      </PhysicsAroundProvider>
    </>
  );
}
