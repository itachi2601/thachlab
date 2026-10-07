import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import InstallGuide from "@/components/pwa/InstallGuide";
import { SITE_URL } from "@/lib/site";

export const metadata: Metadata = {
  title: "Cài ThachLab thành ứng dụng",
  description: "Thêm ThachLab vào màn hình chính điện thoại hoặc máy tính để mở bài luyện chỉ với một lần chạm.",
  alternates: { canonical: "/cai-app" },
};

export default function CaiAppPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-xl px-4 pt-28 pb-20">
        <h1 className="font-display text-3xl font-bold text-white">Cài ThachLab thành ứng dụng</h1>
        <p className="mt-3 mb-8 text-base leading-relaxed text-slate-300">
          Mở bài luyện chỉ với một lần chạm, không cần vào cửa hàng ứng dụng.
        </p>
        <InstallGuide />

        <section className="mt-10 rounded-3xl border border-white/10 bg-panel p-6 text-center">
          <h2 className="font-display text-lg font-bold text-white">Quét mã để mở trang này trên điện thoại</h2>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/icons/qr-cai-app.svg"
            alt={`Mã QR dẫn tới ${SITE_URL}/cai-app`}
            width={224}
            height={224}
            className="mx-auto mt-4 h-56 w-56 rounded-xl"
          />
          <p className="mt-3 text-sm text-slate-400">{SITE_URL.replace("https://", "")}/cai-app</p>
        </section>
      </main>
      <Footer />
    </>
  );
}
