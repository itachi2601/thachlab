"use client";

import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import { supabaseConfigured } from "@/services/supabase";

function Notice({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-xl rounded-2xl border border-white/10 bg-[#0B1020] p-8 text-center text-slate-300">
      {children}
    </div>
  );
}

/** Chỉ hiển thị nội dung khi đã đăng nhập (adminOnly: chỉ quản trị viên). */
export default function RequireAuth({
  children,
  adminOnly = false,
}: {
  children: React.ReactNode;
  adminOnly?: boolean;
}) {
  const { session, profile, loading } = useAuth();

  if (!supabaseConfigured) {
    return (
      <Notice>
        Hệ thống đang được cấu hình, vui lòng quay lại sau.
        <span className="mt-2 block text-xs text-slate-500">
          (Chưa thiết lập kết nối Supabase — xem .env.local.example)
        </span>
      </Notice>
    );
  }

  if (loading) {
    return <Notice>Đang tải…</Notice>;
  }

  if (!session) {
    return (
      <Notice>
        <p>Em cần đăng nhập để sử dụng tính năng này.</p>
        <div className="mt-5 flex justify-center gap-3">
          <Link
            href="/dang-nhap"
            className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
          >
            Đăng nhập
          </Link>
          <Link
            href="/dang-ky"
            className="rounded-full border border-white/15 px-5 py-2.5 text-sm font-semibold text-slate-200 hover:border-white/30"
          >
            Đăng ký
          </Link>
        </div>
      </Notice>
    );
  }

  if (adminOnly && profile?.role !== "admin") {
    return <Notice>Khu vực này chỉ dành cho quản trị viên.</Notice>;
  }

  return <>{children}</>;
}
