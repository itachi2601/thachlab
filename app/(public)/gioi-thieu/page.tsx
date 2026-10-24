import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import AboutFounder from "@/components/home/AboutFounder";
import Features from "@/components/home/Features";
import ExamSamples from "@/components/home/ExamSamples";
import Testimonials from "@/components/home/Testimonials";
import TrialSignup from "@/components/home/TrialSignup";
import { SITE_URL } from "@/lib/site";

export const metadata: Metadata = {
  title: "Giới thiệu ThachLab",
  description: "Thầy Thạch là ai, cách học trên ThachLab, đề xem thử và lời nhắn từ các học trò cũ.",
  alternates: { canonical: "/gioi-thieu" },
  openGraph: {
    title: "Giới thiệu — ThachLab",
    description: "Thầy Thạch, cách học trên ThachLab và lời nhắn từ học trò.",
    url: `${SITE_URL}/gioi-thieu`,
    type: "website",
  },
};

// Các khối giới thiệu tách khỏi trang chủ (K1, 14/10/2026): trang chủ chỉ giữ việc HS/phụ huynh cần làm ngay (N2, B2).
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Course",
  name: "Vật lí lớp 10–12 — thầy Thạch",
  description: "Học thêm Vật lí THPT theo chương trình 2018, có trợ giảng theo dõi từng em trên ThachLab.",
  provider: { "@type": "Person", name: "Ngô Diệu Thạch", url: `${SITE_URL}/gioi-thieu` },
  areaServed: "TP.HCM",
  inLanguage: "vi",
};

export default function GioiThieuPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <Navbar />
      <main className="pt-16">
        <AboutFounder />
        <Features />
        <ExamSamples />
        <Testimonials />
        <TrialSignup />
      </main>
      <Footer />
    </>
  );
}
