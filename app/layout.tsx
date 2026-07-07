import type { Metadata } from "next";
import AuthProvider from "@/components/auth/AuthProvider";
import ToastProvider from "@/components/ui/Toast";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://thachlab.id.vn"),
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
    url: "https://thachlab.id.vn",
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
  url: "https://thachlab.id.vn",
  logo: "https://thachlab.id.vn/images/logo.png",
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
    <html lang="vi" className="h-full antialiased">
      <body className="min-h-full flex flex-col">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
        />
        <AuthProvider>
          <ToastProvider>{children}</ToastProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
