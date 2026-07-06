import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Xuất tĩnh để deploy lên shared hosting LiteSpeed (thachlab.id.vn) —
  // không có Node.js server ở đó, mọi tương tác đều là client component.
  output: "export",
};

export default nextConfig;
