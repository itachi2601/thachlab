import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import CncSessionSheet from "@/components/lessons/CncSessionSheet";

export const metadata: Metadata = {
  title: "Gia công CNC — Phiếu buổi học",
  description: "Phiếu 12 buổi lớp đảo ngược Gia công CNC: mục tiêu, việc tối trước, nhịp 300 phút, sản phẩm nộp, cổng năng lực.",
};

// /lop-hoc/cnc/buoi/?so=N — phiếu buổi N (cnc_lessons id flip-N). Không qua cổng ghi danh: phiếu chỉ là lịch +
// link vào mục bài; nội dung bài vẫn ở /lop-hoc/cnc (có cổng).
export default function CncSessionSheetPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full pt-[76px]">
        <CncSessionSheet />
      </main>
      <Footer />
    </>
  );
}
