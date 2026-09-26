import AuthedShell from "@/components/auth/AuthedShell";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* ThptStudentHome (render trong page.tsx của /tai-khoan) đọc /data/catalog.json
          (xem services/static-content.ts) — preload song song với tải trang. */}
      <link rel="preload" as="fetch" href="/data/catalog.json" crossOrigin="anonymous" />
      <AuthedShell>{children}</AuthedShell>
    </>
  );
}
