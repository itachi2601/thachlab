"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import ReviewStudent from "@/components/review/ReviewStudent";

// Trang học sinh của buổi ôn tập theo chặng: tự tìm buổi ôn đang diễn ra của lớp em.
export default function OnTapHocSinhPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-xl px-4 pt-24 pb-24 sm:px-5 sm:pt-28">
        <RequireAuth>
          <ReviewStudent />
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
