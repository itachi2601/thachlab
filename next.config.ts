import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Xuất tĩnh để deploy lên shared hosting LiteSpeed (thachlab.id.vn) —
  // không có Node.js server ở đó, mọi tương tác đều là client component.
  output: "export",
  // Mỗi trang thành thư-mục/index.html — bắt buộc với Apache/LiteSpeed:
  // có route con (vd /lop-hoc/bai) sẽ tạo thư mục trùng tên trang cha,
  // không có index.html thì server trả 403.
  trailingSlash: true,
};

export default nextConfig;
