"use client";

import Link from "next/link";
import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";
import { BarChart3, Bug, ChevronRight, KeyRound, LogOut, QrCode } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import AvatarUploader from "@/components/account/AvatarUploader";
import ProfileEditCard from "@/components/account/ProfileEditCard";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

const DailyReminderCard = dynamic(() => import("@/components/pwa/DailyReminderCard"), { ssr: false });

const LINKS = [
  { href: "/lop-hoc/ket-qua", label: "Kết quả học tập chi tiết", Icon: BarChart3 },
  { href: "/quet-ma", label: "Quét mã QR vào hoạt động lớp", Icon: QrCode },
  { href: "/tai-khoan/doi-mat-khau", label: "Đổi mật khẩu", Icon: KeyRound },
  { href: "/bao-loi-cua-toi", label: "Báo lỗi và góp ý", Icon: Bug },
];

/**
 * Tab "Thêm" của học sinh: nơi DUY NHẤT cho thông tin tài khoản (ảnh, họ tên, email, mật khẩu, nhắc học, đăng xuất).
 * Trước đây các thẻ này nằm cuối trang Hôm nay làm trang dài và lặp (N1, C2). Học sinh ít vào đây nên để ngoài trang chính.
 */
function Content() {
  const router = useRouter();
  const { session, profile, signOut } = useAuth();
  if (!session) return null;
  return (
    <div className="mx-auto max-w-xl space-y-4">
      <h1 className="font-display text-2xl font-bold text-ink">Thêm</h1>
      <section className="flex items-center gap-4 rounded-2xl border border-line bg-panel p-4">
        <AvatarUploader studentId={session.user.id} url={profile?.avatar_url} name={profile?.full_name} size={64} />
        <div className="min-w-0">
          <p className="truncate font-display text-lg font-bold text-ink">{profile?.full_name ?? "Học sinh"}</p>
          <p className="truncate text-sm text-muted">{session.user.email}</p>
          <p className="text-[13px] text-muted">Bấm vào ảnh để đổi ảnh đại diện.</p>
        </div>
      </section>

      <ProfileEditCard />

      <LazyErrorBoundary>
        <DailyReminderCard />
      </LazyErrorBoundary>

      <nav aria-label="Mục khác" className="overflow-hidden rounded-2xl border border-line bg-panel">
        {LINKS.map(({ href, label, Icon }) => (
          <Link key={href} href={href} className="flex min-h-14 items-center gap-3 border-b border-line px-4 text-ink last:border-0 hover:bg-surface-2">
            <Icon size={18} className="shrink-0 text-muted" aria-hidden />
            <span className="flex-1 text-sm font-semibold">{label}</span>
            <ChevronRight size={16} className="text-muted" aria-hidden />
          </Link>
        ))}
      </nav>

      <button
        type="button"
        onClick={async () => {
          await signOut();
          router.push("/");
        }}
        className="flex min-h-11 w-full items-center justify-center gap-2 rounded-xl border border-line px-4 text-sm font-semibold text-muted hover:border-line-strong hover:text-danger"
      >
        <LogOut size={16} aria-hidden /> Đăng xuất
      </button>
    </div>
  );
}

export default function ThemPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full px-4 pb-24 pt-28 sm:px-6">
        <RequireAuth>
          <Content />
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
