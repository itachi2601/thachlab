import {
  BookOpen,
  Bug,
  ClipboardList,
  Database,
  FileUp,
  Gauge,
  GraduationCap,
  LayoutDashboard,
  Megaphone,
  MessageSquare,
  School,
  SquarePen,
  Tags,
  Trophy,
  UserCheck,
  UserCog,
  Users,
  Video,
  type LucideIcon,
} from "lucide-react";

export type AdminArea = "thpt" | "cttc";

export const AREA_LABEL: Record<AdminArea, string> = { thpt: "THPT – THCS", cttc: "CTTC" };
export const AREA_ENTRY: Record<AdminArea, string> = {
  thpt: "/quan-tri/bai-hoc",
  cttc: "/quan-tri/cnc-bai-hoc",
};

export interface AdminNavItem {
  href: string;
  label: string;
  /** Mô tả ngắn, dùng ở thẻ hành động nhanh trên trang Tổng quan. */
  desc?: string;
  icon: LucideIcon;
  /** Link rời khỏi khu quản trị (ví dụ /dashboard). */
  external?: boolean;
}

export const AREA_ITEMS: Record<AdminArea, AdminNavItem[]> = {
  thpt: [
    { href: "/quan-tri/bai-hoc", label: "Bài học", desc: "Chương, bài và các mục trong bài", icon: BookOpen },
    { href: "/quan-tri/dang-de", label: "Đăng đề kiểm tra", desc: "Dán đề kiểu Azota rồi đăng thẳng vào bài", icon: SquarePen },
    { href: "/quan-tri/nhap-bai", label: "Nhập bài (LaTeX)", desc: "Đăng trọn bài học từ gói JSON", icon: FileUp },
    { href: "/quan-tri/ngan-hang-cau-hoi", label: "Ngân hàng câu hỏi", desc: "Tra cứu và tái sử dụng câu hỏi", icon: Database },
    { href: "/quan-tri/chu-de", label: "Chủ đề câu hỏi", desc: "Yêu cầu cần đạt và nhãn phân loại", icon: Tags },
    { href: "/quan-tri/xep-hang", label: "Xếp hạng & danh hiệu", desc: "Mùa RP, ngưỡng bậc, bài tính RP, danh hiệu", icon: Trophy },
    { href: "/quan-tri/lop-hoc", label: "Lớp học", desc: "Mở lớp, duyệt yêu cầu vào lớp", icon: School },
    { href: "/quan-tri/hoc-sinh", label: "Học sinh", desc: "Tài khoản học sinh và lớp đang theo", icon: GraduationCap },
    { href: "/quan-tri/bang-diem", label: "Bảng điểm", desc: "Kết quả bài kiểm tra đã nộp", icon: ClipboardList },
  ],
  cttc: [
    { href: "/quan-tri/cnc-bai-hoc", label: "Bài học", desc: "Nội dung, tài nguyên và điều kiện mở bài", icon: BookOpen },
    { href: "/quan-tri/cnc-video", label: "Video bài giảng", desc: "Đăng video YouTube cho từng bài", icon: Video },
    { href: "/quan-tri/cnc-dang-de", label: "Đăng đề kiểm tra", desc: "Dán đề kiểu Azota rồi đăng vào ngân hàng CNC", icon: SquarePen },
    // Mở lớp học phần mới + nhập danh sách sinh viên nằm ở tab "Danh sách lớp" của dashboard.
    { href: "/dashboard", label: "Lớp học phần & sinh viên", desc: "Mở lớp, nhập danh sách sinh viên", icon: Users, external: true },
    { href: "/quan-tri/tinh-trang-may", label: "Tình trạng máy", desc: "Máy hư, người sửa, thời gian chờ", icon: Gauge },
  ],
};

export const SHARED_ITEMS: AdminNavItem[] = [
  { href: "/quan-tri/tro-giang", label: "Trợ giảng", desc: "Chấm điểm tháng và hệ số lương", icon: UserCheck },
  { href: "/quan-tri/phan-cong-giang-vien", label: "Phân công giảng viên", desc: "Gán khu vực quản trị cho giảng viên", icon: UserCog },
  { href: "/quan-tri/tin-nhan", label: "Tin nhắn", desc: "Gửi và đọc tin nhắn với học sinh", icon: MessageSquare },
  { href: "/quan-tri/bai-dang", label: "Thông báo / học liệu", desc: "Bài đăng hiển thị cho học sinh", icon: Megaphone },
  { href: "/quan-tri/bao-loi", label: "Báo lỗi & góp ý", desc: "Lỗi và đề xuất tính năng gửi từ nút nổi trên web", icon: Bug },
];

export const OVERVIEW_ITEM: AdminNavItem = {
  href: "/quan-tri",
  label: "Tổng quan",
  icon: LayoutDashboard,
};

const ALL_ITEMS = [OVERVIEW_ITEM, ...AREA_ITEMS.thpt, ...AREA_ITEMS.cttc, ...SHARED_ITEMS];

/** Khu vực mà một đường dẫn thuộc về — quyết định tông màu của shell. */
export function areaOfPath(pathname: string): AdminArea | null {
  if (AREA_ITEMS.thpt.some((item) => pathname.startsWith(item.href) && item.href !== "/dashboard")) return "thpt";
  if (pathname.startsWith("/quan-tri/cnc-") || pathname.startsWith("/quan-tri/tinh-trang-may")) return "cttc";
  return null;
}

/** Tiêu đề hiện ở thanh trên — lấy mục khớp dài nhất để route con vẫn có tên. */
export function titleOfPath(pathname: string): string {
  const match = ALL_ITEMS.filter((item) => pathname === item.href || pathname.startsWith(`${item.href}/`)).sort(
    (a, b) => b.href.length - a.href.length,
  )[0];
  return match?.label ?? "Quản trị";
}
