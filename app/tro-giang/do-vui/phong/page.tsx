"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import RequireAuth from "@/components/auth/RequireAuth";
import QuizHostRoom from "@/components/quiz-live/QuizHostRoom";

function Inner() {
  const id = Number(useSearchParams().get("id"));
  if (!Number.isInteger(id) || id <= 0) return <p className="text-slate-300">Thiếu mã phòng — mở phòng từ danh sách bộ câu.</p>;
  return <QuizHostRoom roomId={id} />;
}

export default function QuizRoomPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full px-5 pt-24 pb-10">
        <RequireAuth>
          <Suspense fallback={<p className="text-slate-400">Đang tải…</p>}>
            <Inner />
          </Suspense>
        </RequireAuth>
      </main>
    </>
  );
}
