// Cấu hình liên hệ + ảnh dùng chung cho trang chủ, trang phụ huynh và footer.
//
// Để ở hằng trong repo (KHÔNG dùng biến môi trường) vì các component này chạy ở client —
// env không có NEXT_PUBLIC_ sẽ undefined khi build tĩnh. Sửa một chỗ, mọi nơi đổi theo;
// đừng rải số điện thoại/Zalo vào từng file.
//
// Giá trị rỗng ("") = chưa có → mọi chỗ tự ẩn phần tử đó (không render nút/nếu không có gì thì bỏ cả cột).
export const CONTACT = {
  /** Số điện thoại hiển thị + dùng cho link tel:. */
  phone: "0982702591",
  /** Link Zalo (mở tab mới). */
  zalo: "https://zalo.me/0982702591",
  /** Khu vực dạy — hiện ở footer và dòng giới thiệu. */
  area: "Khu vực trung tâm TP.HCM",
  /** Email liên hệ — hiện ở cột "Liên hệ" của footer (rỗng thì ẩn). */
  email: "thachngo20212022@gmail.com",
  /** Ảnh thật của thầy (public/, .webp ≤ 150 KB). Rỗng thì khối "Người đứng lớp" giữ bố cục chữ. */
  teacherPhoto: "/images/thay-thach.webp",
  /** Số năm dạy Vật lý THPT. */
  years: 15,
  /** Trường đang công tác. */
  school: "Trường Cao đẳng Kỹ thuật Cao Thắng",
} as const;
