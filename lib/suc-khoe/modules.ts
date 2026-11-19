// Mục Sức khỏe (/suc-khoe) — bản thử cho thầy, sau thành môn cho học sinh.
// MỞ CHO AI: sửa SUC_KHOE_ROLES (một chỗ duy nhất). Học sinh chỉ được thêm vào khi đã làm phần
// "Bài học" và rà theo docs/QUY-TAC-THIET-KE.md (xem ghi chú mỗi mô-đun bên dưới).
export const SUC_KHOE_ROLES = ["admin", "instructor"] as const;
export const canUseSucKhoe = (role?: string | null) => !!role && (SUC_KHOE_ROLES as readonly string[]).includes(role);

export type HealthModule = {
  key: string;
  title: string;
  desc: string;
  href?: string;
  status: "dang-dung" | "sap-co";
  /** dành cho học sinh khi thành môn? (số đo cơ thể: KHÔNG — nguy cơ hình ảnh cơ thể tuổi 14–18) */
  forStudents: boolean;
};

export const MODULES: HealthModule[] = [
  { key: "tap-luyen", title: "Tập luyện", desc: "Chương trình A/B/C, ghi từng hiệp, đồng hồ nghỉ, gợi ý tăng tạ.", href: "/suc-khoe/tap-luyen", status: "dang-dung", forStudents: true },
  { key: "so-do", title: "Số đo cơ thể", desc: "Cân nặng, vòng ngực–eo–mông, tỉ lệ dáng người, mục tiêu 4 tuần.", href: "/suc-khoe/tap-luyen?tab=so-do", status: "dang-dung", forStudents: false },
  { key: "tien-bo", title: "Tiến bộ", desc: "Đường sức mạnh từng bài, số hiệp mỗi nhóm cơ trong tuần.", href: "/suc-khoe/tap-luyen?tab=tien-bo", status: "dang-dung", forStudents: true },
  { key: "dinh-duong", title: "Dinh dưỡng", desc: "Năng lượng và đạm cần mỗi ngày, ghi món đã ăn, chỉnh theo xu hướng cân.", href: "/suc-khoe/dinh-duong", status: "dang-dung", forStudents: true },
  { key: "ngu-hoi-phuc", title: "Giấc ngủ & hồi phục", desc: "Giờ ngủ, mức mệt sau buổi tập, tuần nhẹ.", status: "sap-co", forStudents: true },
  { key: "bai-hoc", title: "Bài học sức khỏe", desc: "Cơ thể vận động thế nào, khởi động an toàn, ăn uống tuổi lớn — phần sẽ thành môn học.", status: "sap-co", forStudents: true },
];
