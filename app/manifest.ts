import type { MetadataRoute } from "next";

// output: "export" bắt buộc route kiểu file-convention phải tĩnh.
export const dynamic = "force-static";

// Màu lấy từ --color-bg (tối) trong app/globals.css. Giữ đồng bộ bằng tay: manifest không đọc được CSS.
const BG = "#05070b";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "ThachLab",
    short_name: "ThachLab",
    description: "Học Vật lý THPT cùng thầy Thạch: hiểu bản chất, không học vẹt.",
    lang: "vi",
    start_url: "/",
    scope: "/",
    display: "standalone",
    background_color: BG,
    theme_color: BG,
    // Nhấn giữ icon app (Android, iOS 16+ qua Safari không hỗ trợ — chỉ Android/desktop) để vào thẳng.
    shortcuts: [
      { name: "Lớp học", short_name: "Lớp học", url: "/lop-hoc/", icons: [{ src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" }] },
      { name: "Luyện tập", short_name: "Luyện tập", url: "/luyen-tap/", icons: [{ src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" }] },
    ],
    icons: [
      { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/icons/icon-maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
}
