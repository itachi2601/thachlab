"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/components/auth/AuthProvider";
import { CHANGE_PASSWORD_PATH, mustChangePassword } from "@/lib/mat-khau-mac-dinh";

/**
 * Đăng nhập bằng mật khẩu mặc định (= mã số HS) thì mọi trang cần đăng nhập chuyển sang trang đổi mật khẩu
 * cho tới khi đổi xong (cờ ở lib/mat-khau-mac-dinh.ts). Không thêm truy vấn nào.
 */
export default function DefaultPasswordGate() {
  const { session } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const uid = session?.user.id ?? null;

  useEffect(() => {
    if (!uid || !pathname) return;
    if (pathname.startsWith(CHANGE_PASSWORD_PATH) || pathname.startsWith("/dang-nhap")) return;
    if (!mustChangePassword(uid)) return;
    const here = `${pathname}${window.location.search}`;
    router.replace(`${CHANGE_PASSWORD_PATH}/?next=${encodeURIComponent(here)}`);
  }, [uid, pathname, router]);

  return null;
}
