"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import QuizPlayer from "@/components/quiz-live/QuizPlayer";

function Inner() {
  const pin = (useSearchParams().get("pin") ?? "").replace(/\D/g, "").slice(0, 6);
  return <QuizPlayer initialPin={pin} />;
}

// Trang cho học sinh vào chơi "Đố vui lớp học" bằng mã PIN — không đăng nhập, không Navbar để màn hình điện thoại gọn.
export default function ChoiPage() {
  return (
    <main className="min-h-screen px-4 pt-8 pb-28">
      <Suspense fallback={null}>
        <Inner />
      </Suspense>
    </main>
  );
}
