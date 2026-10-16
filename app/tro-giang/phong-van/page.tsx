"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import PhongVanForm from "@/components/tro-giang/PhongVanForm";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";

function PhongVanLoader() {
  const { assistant } = useAssistantOrDemo();

  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null) return <NotRegistered note="Liên hệ giáo viên để được thêm vào danh sách trợ giảng." />;

  return (
    <>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Phỏng vấn học sinh</h1>
        <p className="mt-1 text-sm text-slate-400">
          Chào {assistant.short_name} — hỏi trực tiếp từng em về bài tự kiểm tra để thoát &quot;đang mở khoá&quot;, rồi ghi lại tại đây.
        </p>
      </div>
      <PhongVanForm />
    </>
  );
}

export default function PhongVanPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-lg px-5 pt-28 pb-10">
        <RequireAuth>
          <PhongVanLoader />
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
