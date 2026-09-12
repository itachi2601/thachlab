"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { AlertTriangle } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import GhiBuoiForm from "@/components/tro-giang/GhiBuoiForm";
import { getMyAssistant, type TaAssistant } from "@/lib/tro-giang/queries";

function NotRegistered() {
  return (
    <div className="rounded-3xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center">
      <AlertTriangle className="mx-auto text-amber-300" size={36} />
      <h1 className="mt-4 font-display text-xl font-bold text-white">
        Tài khoản này chưa được đăng ký làm trợ giảng
      </h1>
      <p className="mt-2 text-sm text-slate-400">
        Liên hệ giáo viên để được thêm vào danh sách trợ giảng trước khi ghi buổi làm việc.
      </p>
    </div>
  );
}

function GhiLoader() {
  const { session } = useAuth();
  const searchParams = useSearchParams();
  const topic = searchParams.get("topic");
  const [assistant, setAssistant] = useState<TaAssistant | null | undefined>(undefined);

  useEffect(() => {
    if (!session) return;
    let cancelled = false;
    getMyAssistant(session.user.id)
      .then((a) => !cancelled && setAssistant(a))
      .catch(() => !cancelled && setAssistant(null));
    return () => {
      cancelled = true;
    };
  }, [session]);

  if (assistant === undefined) return <p className="text-slate-400">Đang tải…</p>;
  if (assistant === null) return <NotRegistered />;

  return (
    <>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-white">Ghi buổi hôm nay</h1>
        <p className="mt-1 text-sm text-slate-400">Chào {assistant.short_name} — chọn loại buổi rồi điền nhanh.</p>
      </div>
      <GhiBuoiForm assistant={assistant} initialTopicId={topic} />
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
