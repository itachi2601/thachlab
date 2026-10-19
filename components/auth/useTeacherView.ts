"use client";

import { useAuth } from "@/components/auth/auth-context";

const STAFF_ROLES = new Set(["admin", "instructor", "tro_giang"]);

/**
 * Chế độ giáo viên trên các trang học: vai thật là quản trị, giảng viên hoặc trợ giảng,
 * và không bật "Xem như học sinh".
 *
 * "Xem như trợ giảng" chỉ là cờ giả lập (lib/tro-giang/demo.ts), không đổi vai thật
 * và không bật previewAsStudent — tài khoản đó vẫn là giáo viên.
 *
 * Hồ sơ chưa về thì cờ này là false. Nơi ghi tiến độ phải chờ `loading` của useAuth
 * xong rồi mới ghi, không ghi chỉ vì cờ đang false trong lúc chờ.
 */
export function useTeacherView() {
  const { realProfile, previewAsStudent } = useAuth();
  const role = realProfile?.role;
  const isTeacherView = !!role && STAFF_ROLES.has(role) && !previewAsStudent;
  return { isTeacherView };
}
