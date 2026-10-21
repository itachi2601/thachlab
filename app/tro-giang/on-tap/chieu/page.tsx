"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import RequireAuth from "@/components/auth/RequireAuth";
import ReviewScreen from "@/components/review/ReviewScreen";

function Inner() {
  const id = Number(useSearchParams().get("id")) || 0;
  return id ? <ReviewScreen sessionId={id} /> : <p className="p-8 text-slate-700">Thiếu mã buổi ôn (?id=…).</p>;
}

// Màn hình chiếu lên tivi — không Navbar/Footer để chừa chỗ cho đồng hồ và mã QR.
export default function OnTapChieuPage() {
  return (
    <RequireAuth>
      <Suspense fallback={null}>
        <Inner />
      </Suspense>
    </RequireAuth>
  );
}
