"use client";
import Link from "next/link";
import { ArrowLeft, HeartPulse } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { canUseSucKhoe } from "@/lib/suc-khoe/modules";

/** Khung chung các trang /suc-khoe: đăng nhập + chỉ vai trò được mở (lib/suc-khoe/modules.ts). */
export default function SucKhoeShell({ title, back, children }: { title: string; back?: { href: string; label: string }; children: React.ReactNode }) {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-xl px-4 pt-24 pb-16 lg:max-w-3xl">
        <RequireAuth>
          <Gate title={title} back={back}>{children}</Gate>
        </RequireAuth>
      </main>
    </>
  );
}

function Gate({ title, back, children }: { title: string; back?: { href: string; label: string }; children: React.ReactNode }) {
  const { profile, loading } = useAuth();
  if (loading || !profile) return <p className="h-24 animate-pulse rounded-2xl bg-surface-2" aria-label="Đang tải" />;
  if (!canUseSucKhoe(profile.role))
    return (
      <section className="rounded-2xl border border-line bg-panel p-6 text-center">
        <HeartPulse className="mx-auto text-primary" size={32} />
        <h1 className="mt-2 text-xl font-bold text-ink">Mục Sức khỏe đang thử nghiệm</h1>
        <p className="mt-1 text-sm text-muted">Mục này sẽ mở cho học sinh khi soạn xong phần bài học.</p>
        <Link href="/tai-khoan" className="mt-4 inline-flex min-h-11 items-center rounded-xl bg-primary px-5 text-sm font-bold text-white">Về trang của em</Link>
      </section>
    );
  return (
    <>
      <div className="mb-3 flex items-center gap-2">
        {back && (
          <Link href={back.href} aria-label={back.label} className="grid h-11 w-11 place-items-center rounded-xl text-muted hover:bg-surface-2">
            <ArrowLeft size={20} />
          </Link>
        )}
        <h1 className="font-display text-xl font-bold text-ink">{title}</h1>
        {!back && <span className="rounded-full bg-primary-soft px-2.5 py-0.5 text-xs font-bold text-primary">Bản thử · chỉ giáo viên thấy</span>}
      </div>
      {children}
    </>
  );
}
