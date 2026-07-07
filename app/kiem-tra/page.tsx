"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { getSupabase } from "@/services/supabase";

interface ExamMeta {
  id: number;
  title: string;
  duration_minutes: number;
  question_count: number;
}

function ExamList() {
  const { session } = useAuth();
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!session) return;
    getSupabase()
      .from("exams")
      .select("id, title, duration_minutes, question_count")
      .eq("published", true)
      .order("created_at", { ascending: false })
      .then(({ data, error }) => {
        if (error) setError(error.message);
        else setExams(data as ExamMeta[]);
      });
  }, [session]);

  if (error)
    return <p className="text-red-400">Không tải được danh sách đề: {error}</p>;
  if (!exams) return <p className="text-slate-400">Đang tải danh sách đề…</p>;
  if (exams.length === 0)
    return <p className="text-slate-400">Chưa có đề nào được đăng.</p>;

  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {exams.map((exam) => (
        <Link
          key={exam.id}
          href={`/kiem-tra/lam?id=${exam.id}`}
          className="group rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/50"
        >
          <h2 className="font-display text-lg font-semibold text-white group-hover:text-[#3B82F6]">
            {exam.title}
          </h2>
          <p className="mt-3 text-sm text-slate-400">
            {exam.question_count} câu · {exam.duration_minutes} phút
          </p>
          <span className="mt-5 inline-block rounded-full bg-[#2563EB]/15 px-4 py-1.5 text-sm font-semibold text-[#3B82F6]">
            Vào làm bài →
          </span>
        </Link>
      ))}
    </div>
  );
}

export default function ExamListPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          Bài <span className="text-gradient">kiểm tra</span>
        </h1>
        <p className="mt-3 mb-10 max-w-2xl text-slate-400">
          Làm bài trắc nghiệm ngay trên web — nộp bài là có điểm liền, kèm lời
          giải chi tiết từng câu.
        </p>
        <RequireAuth>
          <ExamList />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
