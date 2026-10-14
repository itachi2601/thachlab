import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import AboutFounder from "@/components/home/AboutFounder";
import Features from "@/components/home/Features";
import ExamSamples from "@/components/home/ExamSamples";
import Testimonials from "@/components/home/Testimonials";
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
export default function GioiThieuPage() {
  return (
    <>
      <Navbar />
      <main className="pt-16">
        <AboutFounder />
        <Features />
        <ExamSamples />
        <Testimonials />
      </main>
      <Footer />
    </>
  );
}
