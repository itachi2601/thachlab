import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

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
    sitemap: `${SITE_URL}/sitemap.xml`,
    host: SITE_URL,
  };
}
