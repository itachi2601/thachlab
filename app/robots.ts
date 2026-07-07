import type { MetadataRoute } from "next";

// Bắt buộc với output: export — route sinh file tĩnh lúc build.
export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      // Trang cá nhân/thao tác không cần Google index
      disallow: ["/tai-khoan/", "/tin-nhan/", "/quan-tri/", "/dang-nhap/"],
    },
    sitemap: "https://thachlab.id.vn/sitemap.xml",
    host: "https://thachlab.id.vn",
  };
}
