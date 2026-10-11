import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ExamIndexBrowser from "@/components/de-thi/ExamIndexBrowser";
import { readExamIndex } from "@/components/de-thi/exam-index.server";
import { SITE_URL } from "@/lib/site";

export const metadata: Metadata = {
  title: "Đề thi Vật lý các năm",
  description:
    "Đề giữa kì, cuối kì và thi thử tốt nghiệp THPT môn Vật lý của nhiều trường, sở giáo dục qua các năm. Làm trực tuyến, chấm điểm ngay.",
  alternates: { canonical: "/de-thi" },
  openGraph: {
    title: "Đề thi Vật lý các năm — ThachLab",
    description: "Đề giữa kì, cuối kì, thi thử tốt nghiệp Vật lý. Làm trực tuyến, chấm điểm ngay.",
    url: `${SITE_URL}/de-thi`,
    type: "website",
  },
};

export default function DeThiPage() {
  const exams = readExamIndex();
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pb-20 pt-28 lg:px-8">
        <h1 className="font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">Đề thi Vật lý các năm</h1>
        <p className="mt-3 max-w-2xl text-base leading-relaxed text-ink">
          Chọn lớp và loại đề, hoặc gõ tên trường, tỉnh. Em đăng nhập rồi làm bài, hệ thống chấm điểm ngay.
        </p>
        <div className="mt-8">
          {exams.length > 0 ? (
            <ExamIndexBrowser exams={exams} />
          ) : (
            <p className="text-base text-ink">Danh sách đề đang được cập nhật. Em quay lại sau nhé.</p>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
