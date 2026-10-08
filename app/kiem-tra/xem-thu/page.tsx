"use client";

import { Suspense } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ExamSamplePreview from "@/components/exams/ExamSamplePreview";

export default function ExamSamplePage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <Suspense fallback={<p className="text-center text-base text-slate-400">Đang tải câu 1…</p>}>
          <ExamSamplePreview />
        </Suspense>
      </main>
      <Footer />
    </>
  );
}
