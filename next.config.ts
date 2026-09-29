import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Next tự đoán workspace root bằng cách dò lockfile ở các thư mục cha — máy này có
  // /Users/MAC/package-lock.json (không liên quan) nên Next đoán nhầm root, in cảnh báo.
  // Khai rõ root = thư mục chạy lệnh build/dev (repo hoặc worktree hiện tại) để tắt cảnh báo.
  turbopack: {
    root: process.cwd(),
  },
  // Xuất tĩnh để deploy lên shared hosting LiteSpeed (thachlab.id.vn) —
  // không có Node.js server ở đó, mọi tương tác đều là client component.
  output: "export",
  // Mỗi trang thành thư-mục/index.html — bắt buộc với Apache/LiteSpeed:
  // có route con (vd /lop-hoc/bai) sẽ tạo thư mục trùng tên trang cha,
  // không có index.html thì server trả 403.
  trailingSlash: true,
  // Disable Image Optimization vì export mode không support server-side optimization
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
