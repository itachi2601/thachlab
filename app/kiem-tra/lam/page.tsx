"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import ExamRunner from "@/components/exams/ExamRunner";
import type { Exam } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

function ExamLoader() {
  const { session } = useAuth();
  const searchParams = useSearchParams();
  const id = Number(searchParams.get("id"));
  const [exam, setExam] = useState<Exam | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!session || !id) return;
    getSupabase()
      .from("exams")
      .select("id, title, duration_minutes, published, questions")
      .eq("id", id)
      .single()
      .then(({ data, error }) => {
        if (error || !data) setError("Không tìm thấy đề này.");
        else setExam(data as Exam);
      });
  }, [session, id]);

  if (!id)
    return <p className="text-center text-slate-400">Thiếu mã đề trong địa chỉ.</p>;
  if (error) return <p className="text-center text-red-400">{error}</p>;
  if (!exam) return <p className="text-center text-slate-400">Đang tải đề…</p>;
  return <ExamRunner exam={exam} />;
}

export default function TakeExamPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <RequireAuth>
          <Suspense
            fallback={<p className="text-center text-slate-400">Đang tải…</p>}
          >
            <ExamLoader />
          </Suspense>
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
