"use client";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import QuizHostHome from "@/components/quiz-live/QuizHostHome";

export default function DoVuiPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-5 pt-28 pb-16">
        <RequireAuth>
          <QuizHostHome />
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
