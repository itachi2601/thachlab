import type { Metadata, Viewport } from "next";
import ChunkErrorGuard from "@/components/system/ChunkErrorGuard";
import MobileTabBar from "@/components/layout/MobileTabBar";
import PwaBoot from "@/components/pwa/PwaBoot";
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
  // PWA (GĐ 2.6 M1): manifest do app/manifest.ts sinh ra; iOS cần apple-touch-icon riêng.
  icons: { apple: "/icons/apple-touch-icon.png" },
  appleWebApp: { capable: true, title: "ThachLab", statusBarStyle: "black" },
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

// Khai báo viewport cho điện thoại: viewportFit "cover" là điều kiện để env(safe-area-inset-*)
// khác 0 — thiếu nó thì thanh đáy (MobileTabBar, thanh đáy trang bài) bị tai thỏ và thanh home
// của iPhone che mất. Next 16 đọc export `viewport` này và tự sinh <meta name="viewport">.
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
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
        {/* Bắt tay TCP+TLS với Supabase (Singapore) song song lúc tải trang, thay vì chờ
            tới request đầu tiên — ước tính tiết kiệm ~50-150ms round-trip đầu tiên từ VN. */}
        {SUPABASE_URL && <link rel="preconnect" href={SUPABASE_URL} crossOrigin="anonymous" />}
        {/* Theme: lựa chọn đã lưu > /phu-huynh mặc định SÁNG (phụ huynh lớn tuổi đọc chữ sẫm trên nền
            sáng nhanh hơn — Piepenbrock 2013; chữ xanh nhỏ trên nền đen là tổ hợp tệ nhất cho 45+)
            > theo hệ điều hành. Cùng logic với components/ui/ReadingZone.tsx (defaultTheme). */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem("thachlab-theme");if(t!=="light"&&t!=="dark")t=(location.pathname==="/phu-huynh"||location.pathname.indexOf("/phu-huynh/")===0)?"light":(window.matchMedia("(prefers-color-scheme: light)").matches?"light":"dark");document.documentElement.dataset.theme=t;document.documentElement.style.colorScheme=t}catch(e){}})()`,
          }}
        />
        {/* Lưới an toàn SỚM cho ChunkLoadError: chạy trước hydrate (ChunkErrorGuard chỉ đăng ký
            trong useEffect nên không bắt được lỗi chunk xảy ra trước đó → trang trắng).
            Cùng cờ sessionStorage với ChunkErrorGuard: reload đúng 1 lần mỗi phiên tab. */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){var K="thachlab-chunk-reload",P=["ChunkLoadError","Failed to load chunk","Loading chunk","Failed to fetch dynamically imported module"];function m(x){if(!x)return"";return typeof x==="string"?x:(x.message||"")}function h(s){if(!s)return;for(var i=0;i<P.length;i++){if(s.indexOf(P[i])>-1){try{if(sessionStorage.getItem(K))return;sessionStorage.setItem(K,"1")}catch(e){return}location.reload();return}}}window.addEventListener("error",function(e){h(m(e.error)||e.message)});window.addEventListener("unhandledrejection",function(e){h(m(e.reason))})})()`,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
        />
        <ChunkErrorGuard />
        <ToastProvider>{children}</ToastProvider>
        {/* Thanh đáy kiểu app cho điện thoại (< 1024px) — tự ẩn ở /quan-tri/**, /kiem-tra/lam
            và /lop-hoc/bai (trang bài học đã có thanh đáy riêng). Dùng useAuth nên chỉ chạy
            trong cây có AuthProvider; nhóm trang công khai không có AuthProvider sẽ tự bỏ qua. */}
        <MobileTabBar />
        <PwaBoot />
      </body>
    </html>
  );
}
