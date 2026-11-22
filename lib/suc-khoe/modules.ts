// Mục Sức khỏe (/suc-khoe). MỞ CHO AI: sửa SUC_KHOE_ROLES (một chỗ duy nhất).
// 19/11/2026 thầy mở cho học sinh/sinh viên (THPT và CTTC) để lấy gợi ý bài tập: học sinh dùng chương trình
// không dụng cụ (PROGRAM_HS trong lib/tap-luyen/chuong-trinh.ts), chỉ thấy mô-đun có forStudents: true.
export const SUC_KHOE_ROLES = ["admin", "instructor", "student"] as const;
export const isSucKhoeStaff = (role?: string | null) => role === "admin" || role === "instructor";
export const canUseSucKhoe = (role?: string | null) => !!role && (SUC_KHOE_ROLES as readonly string[]).includes(role);

export type HealthModule = {
  key: string;
  title: string;
  desc: string;
  /** mô tả khi học sinh xem (không nói tới tạ, cân nặng) */
  descHs?: string;
  href?: string;
  status: "dang-dung" | "sap-co";
  /** dành cho học sinh khi thành môn? (số đo cơ thể: KHÔNG — nguy cơ hình ảnh cơ thể tuổi 14–18) */
  forStudents: boolean;
};

export const MODULES: HealthModule[] = [
  { key: "tap-luyen", title: "Tập luyện", desc: "Chương trình A/B/C, ghi từng hiệp, đồng hồ nghỉ, gợi ý tăng tạ.", descHs: "3 buổi tập tại nhà không cần dụng cụ, mỗi buổi khoảng 30 phút, có đồng hồ nghỉ.", href: "/suc-khoe/tap-luyen", status: "dang-dung", forStudents: true },
  { key: "tai-nha", title: "Tập tại nhà — lộ trình 6 bậc", desc: "Từ đi bộ công viên, nghe podcast → tay không → Tabata, HIIT → phòng gym. Cá nhân hoá theo sức em, chỉ lưu trên máy, không gửi máy chủ.", descHs: "Bắt đầu từ đi bộ, lên dần tới Tabata, HIIT rồi phòng gym. Chọn theo sức em; không thu thập dữ liệu — chỉ lưu trên máy em.", href: "/suc-khoe/tai-nha", status: "dang-dung", forStudents: true },
  { key: "so-do", title: "Số đo cơ thể", desc: "Cân nặng, vòng ngực–eo–mông, tỉ lệ dáng người, mục tiêu 4 tuần.", href: "/suc-khoe/tap-luyen?tab=so-do", status: "dang-dung", forStudents: false },
  { key: "tien-bo", title: "Tiến bộ", desc: "Đường sức mạnh từng bài, số hiệp mỗi nhóm cơ trong tuần.", descHs: "Số lần, số giây của em tăng thế nào qua từng buổi.", href: "/suc-khoe/tap-luyen?tab=tien-bo", status: "dang-dung", forStudents: true },
  // Dinh dưỡng bản hiện tại tính theo cân nặng, kcal dư/thiếu cho người lớn → chưa mở cho HS (G2; trang chặn bằng staffOnly)
  { key: "dinh-duong", title: "Dinh dưỡng", desc: "Năng lượng và đạm cần mỗi ngày, ghi món đã ăn, chỉnh theo xu hướng cân.", href: "/suc-khoe/dinh-duong", status: "dang-dung", forStudents: false },
  { key: "ngu-hoi-phuc", title: "Giấc ngủ & hồi phục", desc: "Giờ ngủ, mức mệt sau buổi tập, tuần nhẹ.", status: "sap-co", forStudents: true },
  { key: "bai-hoc", title: "Bài học sức khỏe", desc: "Cơ thể vận động thế nào, khởi động an toàn, ăn uống tuổi lớn — phần sẽ thành môn học.", status: "sap-co", forStudents: true },
];
