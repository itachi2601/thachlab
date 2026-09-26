// Tách khỏi services/bug-reports.ts: types + nhãn tiếng Việt thuần, không đụng
// supabase — để components/BugReportWidget.tsx (render ở MỌI trang kể cả trang công
// khai) dùng BUG_CATEGORY_LABELS lúc render (đồng bộ, cho <select>) mà không phải tải
// cả @supabase/supabase-js chỉ vì nằm chung file với các hàm gọi DB.
export type BugCategory = "hien_thi" | "diem" | "dang_nhap" | "de_xuat" | "khac";
export type BugStatus = "moi" | "dang_xu_ly" | "da_xu_ly";

export const BUG_CATEGORY_LABELS: Record<BugCategory, string> = {
  hien_thi: "Lỗi hiển thị / giao diện",
  diem: "Lỗi điểm / bài kiểm tra",
  dang_nhap: "Lỗi đăng nhập / tài khoản",
  de_xuat: "Đề xuất tính năng mới",
  khac: "Khác",
};

export const BUG_STATUS_LABELS: Record<BugStatus, string> = {
  moi: "Mới",
  dang_xu_ly: "Đang xử lý",
  da_xu_ly: "Đã xử lý",
};
