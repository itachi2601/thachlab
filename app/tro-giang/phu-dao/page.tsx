"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import TaDemoBanner from "@/components/tro-giang/TaDemoBanner";
import PhuDaoList from "@/components/tro-giang/PhuDaoList";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";

function PhuDaoLoader() {
  const { assistant, demo } = useAssistantOrDemo();

  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null)
    return <NotRegistered note="Liên hệ giáo viên để được thêm vào danh sách trợ giảng." />;

  return (
    <>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Cần phụ đạo</h1>
        <p className="mt-1 text-sm text-slate-400">
          Em nào đang hổng phần nào, phần nào đã được dạy lại. Ghi buổi phụ đạo xong nhớ tick
          đúng phần đã dạy.
        </p>
      </div>
      <PhuDaoList assistant={assistant} />
      {demo && <TaDemoBanner raised />}
    </>
  );
}

export default function PhuDaoPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-lg px-5 pt-28 pb-16">
        <RequireAuth>
          <PhuDaoLoader />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
