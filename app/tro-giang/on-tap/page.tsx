"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import ReviewHome from "@/components/review/ReviewHome";
import ReviewConsole from "@/components/review/ReviewConsole";

function Inner() {
  const id = Number(useSearchParams().get("id")) || 0;
  return id ? <ReviewConsole key={id} sessionId={id} /> : <ReviewHome />;
}

// Ôn tập theo chặng — dùng chung cho thầy và trợ giảng (RPC review_* chỉ cho is_staff).
// Không có ?id= → danh sách + tạo buổi; có ?id= → bảng điều phối của buổi đó.
export default function OnTapPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-5 pt-28 pb-16">
        <RequireAuth>
          <Suspense fallback={<p className="text-muted">Đang tải…</p>}>
            <Inner />
          </Suspense>
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
