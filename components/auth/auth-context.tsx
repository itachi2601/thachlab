"use client";

// Phần "nhẹ" của auth: chỉ types + React Context + hook useAuth, KHÔNG import
// @supabase/supabase-js (xem services/supabase.ts) hay bất kỳ thứ gì nặng.
//
// Lý do tách riêng: Navbar, BugReportWidget, PreviewAsStudentToggle, PreviewAsTaToggle
// xuất hiện trên MỌI trang kể cả các trang công khai chưa đăng nhập (/, /blog, /khoa-hoc).
// Nếu các file đó import useAuth từ AuthProvider.tsx (bản đầy đủ, có gọi getSupabase()),
// bundler sẽ phải đóng gói cả supabase-js + GoTrue (~211KB) vào MỌI trang, kể cả trang
// không hề cần đăng nhập. Import từ file này thay vào đó thì không tốn gì thêm.
//
// AuthProvider.tsx (bản đầy đủ) dùng CHÍNH context này (AuthContext), nên useContext ở
// đây vẫn nhận đúng giá trị thật trên các trang có bọc <AuthProvider> — chỉ khi KHÔNG có
// AuthProvider nào ở trên (các trang công khai) thì mới rơi về giá trị mặc định bên dưới.
import { createContext, useContext } from "react";
import type { Session } from "@supabase/supabase-js";

export interface Profile {
  id: string;
  full_name: string;
  class_name: string;
  role: "student" | "admin" | "instructor" | "tro_giang" | "parent";
  // Khu vực quản trị được phân công cho giảng viên (null = chưa được cấp vào /quan-tri).
  // Chỉ áp dụng cho role "instructor" — role "admin" luôn thấy cả 2 khu vực.
  admin_area: "thpt" | "cttc" | null;
  // Hệ học của học sinh/sinh viên — nguồn sự thật duy nhất để chọn giao diện CTTC hay THPT.
  track: "thpt" | "cttc" | null;
  avatar_url: string | null;
}

export type PreviewMode = "student" | "cttc" | null;

export interface AuthState {
  session: Session | null;
  /** Hồ sơ đang hiển thị cho phần còn lại của app — bị ghi đè khi admin bật "Xem như học sinh". */
  profile: Profile | null;
  /** Hồ sơ thật, không bị ghi đè — dùng để hiện nút bật preview (chỉ role thật = admin mới thấy). */
  realProfile: Profile | null;
  loading: boolean;
  signOut: () => Promise<void>;
  previewAsStudent: boolean;
  setPreviewAsStudent: (value: boolean) => void;
  /**
   * Chế độ xem thử đang bật: "student" = học sinh chung (dùng track thật của admin),
   * "cttc" = sinh viên CTTC đã ghi danh 3 môn (track bị ghi đè thành "cttc"), null = tắt.
   */
  previewMode: PreviewMode;
  setPreviewMode: (mode: PreviewMode) => void;
  /** Đọc lại hồ sơ từ DB — dùng sau khi tự sửa avatar/tên để cập nhật ngay khắp app. */
  refreshProfile: () => Promise<void>;
}

// loading: false (không phải true) — giá trị này chỉ áp dụng khi KHÔNG có <AuthProvider>
// nào ở trên (trang công khai). Nếu để true, các nơi gọi useAuth() trên trang công khai
// (Navbar, BugReportWidget...) sẽ kẹt ở trạng thái "đang tải" mãi mãi vì không có Provider
// nào chạy effect để chuyển loading -> false. Khi CÓ <AuthProvider> thật, state nội bộ của
// nó (không phải default này) mới là giá trị được dùng, nên default ở đây không ảnh hưởng
// gì tới hành vi của các trang cần đăng nhập.
const defaultAuthState: AuthState = {
  session: null,
  profile: null,
  realProfile: null,
  loading: false,
  signOut: async () => {},
  previewAsStudent: false,
  setPreviewAsStudent: () => {},
  previewMode: null,
  setPreviewMode: () => {},
  refreshProfile: async () => {},
};

export const AuthContext = createContext<AuthState>(defaultAuthState);

export function useAuth() {
  return useContext(AuthContext);
}
