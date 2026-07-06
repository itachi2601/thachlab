import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ThachLab — Vật lý không chỉ là công thức",
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
  openGraph: {
    title: "ThachLab — Vật lý không chỉ là công thức",
    description:
      "Living between equation and motion. Học Vật lý cùng thầy Thạch: hiểu bản chất, không học vẹt.",
    url: "https://thachlab.id.vn",
    siteName: "ThachLab",
    locale: "vi_VN",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
