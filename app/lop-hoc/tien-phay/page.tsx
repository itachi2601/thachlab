import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import TienPhayEnrollmentGate from "@/components/lessons/TienPhayEnrollmentGate";

export const metadata: Metadata = {
  title: "Tiện – Phay truyền thống — Không gian học tập",
  description:
    "Điểm danh, chọn máy và theo dõi 5S cho buổi thực hành Tiện – Phay truyền thống tại Xưởng C1.1.",
};

export default function TienPhayCoursePage() {
  return (
    <>
      <Navbar />
      <main className="pt-[76px]">
        <TienPhayEnrollmentGate />
      </main>
      <Footer />
    </>
  );
}
