"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import TaDemoBanner from "@/components/tro-giang/TaDemoBanner";
import TaClassAnnouncements from "@/components/tro-giang/TaClassAnnouncements";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";

function ThongBaoLoader() {
  const { assistant, demo } = useAssistantOrDemo();

  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null)
    return <NotRegistered note="Liên hệ giáo viên để được thêm vào danh sách trợ giảng." />;

  return (
    <>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Thông báo lớp</h1>
        <p className="mt-1 text-sm text-slate-400">
          Đăng việc cần làm hôm nay và bài tập về nhà — học sinh thấy ngay ở trang chủ của mình.
        </p>
      </div>
      <TaClassAnnouncements assistant={assistant} />
      {demo && <TaDemoBanner raised />}
    </>
  );
}

export default function ThongBaoPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-lg px-5 pt-28 pb-16">
        <RequireAuth>
          <ThongBaoLoader />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
