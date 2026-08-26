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

/**
 * Chỉ hiển thị nội dung khi đã đăng nhập.
 * - adminOnly: admin, hoặc giảng viên đã được phân công 1 khu vực quản trị (admin_area).
 * - area: thêm điều kiện phải đúng khu vực được phân công (admin luôn qua được).
 * - restrictToAdmin: chỉ role "admin" — giảng viên được phân công khu vực cũng không vào được
 *   (dùng cho các trang dùng chung/nhạy cảm như phân công giảng viên).
 */
export default function RequireAuth({
  children,
  adminOnly = false,
  area,
  restrictToAdmin = false,
}: {
  children: React.ReactNode;
  adminOnly?: boolean;
  area?: "thpt" | "cttc";
  restrictToAdmin?: boolean;
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
            className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark"
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

  const isAdmin = profile?.role === "admin";
  const hasAnyAdminArea = profile?.role === "instructor" && !!profile.admin_area;

  if (adminOnly && !isAdmin && !hasAnyAdminArea) {
    return <Notice>Khu vực này chỉ dành cho quản trị viên.</Notice>;
  }

  if (restrictToAdmin && !isAdmin) {
    return <Notice>Mục này chỉ dành cho quản trị viên, không dành cho giảng viên được phân công.</Notice>;
  }

  if (area && !isAdmin && profile?.admin_area !== area) {
    return (
      <Notice>
        Tài khoản của bạn chưa được phân công vào khu vực này.
        {profile?.admin_area && (
          <span className="mt-2 block text-xs text-slate-500">
            Bạn đang được phân công khu vực {profile.admin_area === "thpt" ? "THPT" : "CTTC"}.
          </span>
        )}
      </Notice>
    );
  }

  return <>{children}</>;
}
