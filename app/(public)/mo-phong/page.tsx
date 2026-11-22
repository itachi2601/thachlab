import type { Metadata } from "next";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ThuVienMoPhong from "@/components/mo-phong/ThuVienMoPhong";
import { SITE_URL } from "@/lib/site";

export const metadata: Metadata = {
  title: "Thư viện mô phỏng và thí nghiệm Vật lí",
  description:
    "Mô phỏng tự dựng, clip thí nghiệm và mô phỏng PhET cho Vật lí lớp 9 đến 12. Xem miễn phí, không cần đăng nhập, tìm theo lớp và chủ đề.",
  alternates: { canonical: "/mo-phong" },
  openGraph: {
    title: "Thư viện mô phỏng và thí nghiệm Vật lí — ThachLab",
    description: "Mô phỏng, clip thí nghiệm và PhET cho Vật lí lớp 9–12. Xem miễn phí.",
    url: `${SITE_URL}/mo-phong`,
    type: "website",
  },
};

export default function MoPhongPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-4 pb-24 pt-28 lg:px-8">
        <h1 className="font-display text-3xl font-semibold text-ink">Thư viện mô phỏng và thí nghiệm</h1>
        <p className="mt-3 max-w-3xl text-lg leading-relaxed text-ink">
          Xem miễn phí, không cần đăng nhập. Mỗi thẻ có một câu “Nhìn vào:” để biết cần quan sát điều gì. Mô phỏng chỉ chạy khi bạn bấm.
        </p>
        <div className="mt-6">
          <ThuVienMoPhong />
        </div>

        <section className="mt-12 rounded-2xl border border-line bg-panel p-6" aria-labelledby="moi-dang-ky">
          <h2 id="moi-dang-ky" className="text-xl font-semibold text-ink">
            Muốn học tiếp theo từng bài?
          </h2>
          <p className="mt-2 max-w-2xl text-lg leading-relaxed text-ink">
            Mỗi mô phỏng nằm trong một bài học có dự đoán trước, câu hỏi sau và chấm ngay. Đăng ký tài khoản để làm đủ các bài đó.
          </p>
          <Link
            href="/dang-ky"
            className="mt-4 inline-flex min-h-12 items-center rounded-xl bg-primary px-6 text-base font-semibold text-white hover:bg-primary-dark"
          >
            Đăng ký học
          </Link>
        </section>
      </main>
      <Footer />
    </>
  );
}
