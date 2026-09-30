import AuthedShell from "@/components/auth/AuthedShell";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* /luyen-tap đọc /data/catalog.json (lớp → chương → bài) như /lop-hoc — preload song song. */}
      <link rel="preload" as="fetch" href="/data/catalog.json" crossOrigin="anonymous" />
      <AuthedShell>{children}</AuthedShell>
    </>
  );
}
