import type { Metadata } from "next";
import ToastProvider from "@/components/ui/Toast";
import { SITE_URL } from "@/lib/site";
import { SUPABASE_URL } from "@/lib/supabase-env";
import { fontClassName } from "./fonts";
import "./globals.css";

// AuthProvider (kéo theo @supabase/supabase-js + GoTrue, ~211KB) không còn bọc ở đây
// nữa — trước đây layout gốc này áp dụng cho MỌI trang, kể cả trang công khai chưa đăng
// nhập (/, /blog, /khoa-hoc), buộc các trang đó tải cả GoTrue dù không cần. Giờ mỗi
// nhóm route tự quyết: nhóm cần đăng nhập dùng components/auth/AuthedShell.tsx (có
// AuthProvider) trong layout.tsx riêng của nó; nhóm công khai dùng
// components/auth/PublicShell.tsx (không có AuthProvider) trong app/(public)/layout.tsx.
// ToastProvider ở lại đây vì dùng chung cả 2 phía và không phụ thuộc supabase-js.

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "ThachLab — Vật lý không chỉ là công thức",
    template: "%s | ThachLab",
  },
  description:
    "Nền tảng học Vật lý THPT của thầy Thạch — sống giữa phương trình và chuyển động. Hiểu bản chất, sống khỏe mạnh, có đam mê và không ngừng học hỏi.",
  keywords: [
    "vật lý",
    "vật lý THPT",
    "thầy Thạch",
    "ThachLab",
    "học vật lý",
    "GDPT 2018",
  ],
  alternates: { canonical: "/" },
  openGraph: {
    title: "ThachLab — Vật lý không chỉ là công thức",
    description:
      "Living between equation and motion. Học Vật lý cùng thầy Thạch: hiểu bản chất, không học vẹt.",
    url: SITE_URL,
    siteName: "ThachLab",
    locale: "vi_VN",
    type: "website",
    images: [
      {
        url: "/images/og-lo-trinh-vat-ly.png",
        width: 1200,
        height: 630,
        alt: "ThachLab — Học Vật lý THPT theo chương trình mới 2018",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "ThachLab — Vật lý không chỉ là công thức",
    description: "Học Vật lý THPT cùng thầy Thạch: hiểu bản chất, không học vẹt.",
    images: ["/images/og-lo-trinh-vat-ly.png"],
  },
  // Xác minh quyền sở hữu site cho Google Search Console (phương thức Thẻ HTML).
  verification: {
    google: "0qVSXLYLOif58yDOQmLBCWgDb3zu9CERcFem76Gy-oo",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large" },
  },
};

// Structured data toàn site — giúp Google nhận diện thương hiệu.
const orgJsonLd = {
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  name: "ThachLab",
  alternateName: "Trung tâm Vật lý thầy Thạch",
  url: SITE_URL,
  logo: `${SITE_URL}/images/logo.png`,
  description:
    "Trung tâm luyện thi Vật lý THPT theo chương trình GDPT 2018 — học offline kết hợp hệ thống luyện đề online.",
  sameAs: ["https://www.facebook.com/thachlab"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi" className={`h-full antialiased ${fontClassName}`} data-theme="dark" suppressHydrationWarning>
      <head>
        {/* Bắt tay TCP+TLS với Supabase (Sydney) song song lúc tải trang, thay vì chờ
            tới request đầu tiên — ước tính tiết kiệm ~50-150ms round-trip đầu tiên từ VN. */}
        {SUPABASE_URL && <link rel="preconnect" href={SUPABASE_URL} crossOrigin="anonymous" />}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem("thachlab-theme");if(t!=="light"&&t!=="dark")t=window.matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.dataset.theme=t;document.documentElement.style.colorScheme=t}catch(e){}})()`,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
        />
        <ToastProvider>{children}</ToastProvider>
      </body>
    </html>
  );
}
