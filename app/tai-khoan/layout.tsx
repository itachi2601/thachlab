import AuthedShell from "@/components/auth/AuthedShell";
import { PhysicsAroundProvider } from "@/components/home/PhysicsAroundContext";
import { getPhysicsAroundLite } from "@/lib/physics-around-lite";

export default function Layout({ children }: { children: React.ReactNode }) {
  const posts = getPhysicsAroundLite();
  return (
    <>
      {/* ThptStudentHome (render trong page.tsx của /tai-khoan) đọc /data/catalog.json
          (xem services/static-content.ts) — preload song song với tải trang. */}
      <link rel="preload" as="fetch" href="/data/catalog.json" crossOrigin="anonymous" />
      <PhysicsAroundProvider posts={posts}>
        <AuthedShell>{children}</AuthedShell>
      </PhysicsAroundProvider>
    </>
  );
}
