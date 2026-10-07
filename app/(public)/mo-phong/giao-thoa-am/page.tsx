import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SoundInterferenceSimulation } from "@/components/physics/SoundInterferenceSimulation";

export const metadata: Metadata = {
  title: "Giao thoa sóng âm bằng loa MacBook",
  description:
    "Phát âm đơn sắc ra hai loa trái/phải của máy, xem bản đồ vân giao thoa và tự nghe chỗ to chỗ nhỏ trước màn hình.",
};

export default function GiaoThoaAmPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-4 pb-24 pt-28 lg:px-8">
        <h1 className="font-display text-2xl font-semibold text-white sm:text-3xl">Giao thoa sóng âm bằng hai loa của máy</h1>
        <p className="mt-2 text-sm leading-relaxed text-slate-300">
          Hai loa trái/phải phát cùng một âm sin nên luôn đồng pha: đó là hai nguồn kết hợp. Bản đồ dưới đây nhìn từ trên xuống,
          màn hình nằm ở đáy. Bật âm, che một tai rồi chậm rãi dịch đầu sang ngang để nghe chỗ to, chỗ nhỏ.
        </p>
        <SoundInterferenceSimulation />
      </main>
      <Footer />
    </>
  );
}
