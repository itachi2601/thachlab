"use client";

import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import { supabaseConfigured } from "@/services/supabase";

function Notice({ children, wide = false }: { children: React.ReactNode; wide?: boolean }) {
  return (
    <div
      className={`mx-auto mt-10 rounded-2xl border border-white/10 bg-panel p-6 sm:mt-16 sm:p-8 ${
        wide ? "max-w-3xl text-left text-slate-300" : "max-w-xl text-center text-slate-300"
      }`}
    >
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
 * - guestNotice: nội dung thay cho câu mặc định "Em cần đăng nhập…" khi chưa đăng nhập — dùng ở
 *   trang không dành cho học sinh (vd /phu-huynh xưng "em" với phụ huynh là sai).
 * - guestActions: nút phụ nằm cùng hàng với nút Đăng nhập (vd "Nhắn Zalo cho thầy" ở /phu-huynh).
 *   Để riêng khỏi guestNotice vì hàng nút do component này render.
 * - loginHref: đích nút Đăng nhập (mặc định /dang-nhap).
 * - showSignUp: ẩn nút Đăng ký khi form /dang-ky không hợp với người xem (phụ huynh tạo tài khoản qua link mời).
 * - guestWide: khách chưa đăng nhập thấy khung rộng (max-w-3xl) và căn trái — dùng khi nội dung
 *   khách là một trang giới thiệu thật (vd /phu-huynh) chứ không phải 1 câu nhắc đăng nhập.
 * - guestHideAuthRow: trang tự vẽ nút hành động trong guestNotice (để đặt Zalo/gọi lên trước,
 *   Đăng nhập xuống dưới) — component thôi render hàng nút Đăng nhập/Đăng ký mặc định.
 */
export default function RequireAuth({
  children,
  adminOnly = false,
  area,
  restrictToAdmin = false,
  guestNotice,
  guestActions,
  loginHref = "/dang-nhap",
  showSignUp = true,
  guestWide = false,
  guestHideAuthRow = false,
}: {
  children: React.ReactNode;
  adminOnly?: boolean;
  area?: "thpt" | "cttc";
  restrictToAdmin?: boolean;
  guestNotice?: React.ReactNode;
  guestActions?: React.ReactNode;
  loginHref?: string;
  showSignUp?: boolean;
  guestWide?: boolean;
  guestHideAuthRow?: boolean;
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
      <Notice wide={guestWide}>
        {guestNotice ?? <p>Em cần đăng nhập để sử dụng tính năng này.</p>}
        {!guestHideAuthRow && (
          <div className={`mt-5 flex flex-wrap gap-3 ${guestWide ? "" : "justify-center"}`}>
            <Link
              href={loginHref}
              className="rounded-full bg-primary px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark"
            >
              Đăng nhập
            </Link>
            {showSignUp && (
              <Link
                href="/dang-ky"
                className="rounded-full border border-white/15 px-5 py-2.5 text-sm font-semibold text-slate-200 hover:border-white/30"
              >
                Đăng ký
              </Link>
            )}
            {guestActions}
          </div>
        )}
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
