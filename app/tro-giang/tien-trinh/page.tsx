"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import TaDemoBanner from "@/components/tro-giang/TaDemoBanner";
import TeachingProgressTree from "@/components/dashboard/TeachingProgressTree";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";

function Loader() {
  const { assistant, demo } = useAssistantOrDemo();
  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null) return <NotRegistered note="Liên hệ giáo viên để được thêm vào danh sách trợ giảng." />;
  return (
    <>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Tiến trình bài dạy</h1>
        <p className="mt-1 text-sm text-slate-400">
          Tick bài lớp đã học trong tuần và ghi chú để cải tiến cho năm sau. Thầy cũng thấy đúng bảng này.
        </p>
      </div>
      <TeachingProgressTree />
      {demo && <TaDemoBanner />}
    </>
  );
}

export default function TienTrinhPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-2xl px-5 pt-28 pb-16">
        <RequireAuth>
          <Loader />
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
