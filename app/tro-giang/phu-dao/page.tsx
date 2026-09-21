"use client";

import { useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import TaDemoBanner from "@/components/tro-giang/TaDemoBanner";
import PhuDaoList from "@/components/tro-giang/PhuDaoList";
import TutoringSlotsPlanner from "@/components/tro-giang/TutoringSlotsPlanner";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";

const TABS = [
  { id: "needs", label: "Cần phụ đạo" },
  { id: "slots", label: "Lịch tuần" },
] as const;
type Tab = (typeof TABS)[number]["id"];

function PhuDaoLoader() {
  const { assistant, demo } = useAssistantOrDemo();
  const [tab, setTab] = useState<Tab>("needs");

  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null)
    return <NotRegistered note="Liên hệ giáo viên để được thêm vào danh sách trợ giảng." />;

  return (
    <>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Phụ đạo</h1>
        <p className="mt-1 text-sm text-slate-400">
          {tab === "needs"
            ? "Em nào đang hổng phần nào, phần nào đã được dạy lại. Ghi buổi phụ đạo xong nhớ tick đúng phần đã dạy."
            : "Đăng buổi phụ đạo sắp tới để học sinh trong lớp tự đăng ký từ trang chủ của các em."}
        </p>
      </div>

      <div className="mb-4 flex gap-2">
        {TABS.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setTab(item.id)}
            className={`rounded-full border px-4 py-2 text-sm font-semibold ${
              tab === item.id ? "border-blue-400/50 bg-blue-500/15 text-blue-200" : "border-white/10 text-slate-400"
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      {tab === "needs" ? <PhuDaoList assistant={assistant} /> : <TutoringSlotsPlanner assistant={assistant} />}
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
