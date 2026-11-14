import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import CncGradesSheet from "@/components/lessons/CncGradesSheet";

export const metadata: Metadata = {
  title: "Gia công CNC — Bảng điểm",
  description: "Bảng điểm học phần Gia công CNC của em: điểm Tiện và điểm Phay.",
};

// /lop-hoc/cnc/bang-diem/ — mỗi em chỉ thấy điểm của mình (RLS bảng cnc_grades).
export default function CncGradesPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full pt-[76px]">
        <CncGradesSheet />
      </main>
      <Footer />
    </>
  );
}
