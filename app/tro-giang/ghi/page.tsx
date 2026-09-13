"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import GhiBuoiForm from "@/components/tro-giang/GhiBuoiForm";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import TaDemoBanner from "@/components/tro-giang/TaDemoBanner";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";

function GhiLoader() {
  const searchParams = useSearchParams();
  const topic = searchParams.get("topic");
  const { assistant, demo } = useAssistantOrDemo();

  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null)
    return (
      <NotRegistered note="Liên hệ giáo viên để được thêm vào danh sách trợ giảng trước khi ghi buổi làm việc." />
    );

  return (
    <>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Ghi buổi hôm nay</h1>
        <p className="mt-1 text-sm text-slate-400">Chào {assistant.short_name} — chọn loại buổi rồi điền nhanh.</p>
      </div>
      <GhiBuoiForm assistant={assistant} initialTopicId={topic} />
      {demo && <TaDemoBanner raised />}
    </>
  );
}

export default function GhiBuoiPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-lg px-5 pt-28 pb-10">
        <RequireAuth>
          <Suspense fallback={<p className="text-slate-400">Đang tải…</p>}>
            <GhiLoader />
          </Suspense>
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
