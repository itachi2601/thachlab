import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import CncEnrollmentGate from "@/components/lessons/CncEnrollmentGate";

export const metadata: Metadata = {
  title: "Gia công CNC — Không gian học tập",
  description:
    "Hệ thống bài học Gia công CNC theo chuẩn đầu ra, bài giảng, video, kiểm tra và tài liệu.",
};

export default function CncCoursePage() {
  return (
    <>
      <Navbar />
      <main className="cnc-page pt-[76px]">
        <CncEnrollmentGate />
      </main>
      <Footer />
    </>
  );
}
