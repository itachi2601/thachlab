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

// Một số iOS/Safari đời cũ không cập nhật useSearchParams() đúng lúc khi trang
// được phục hồi từ bfcache (nút Back) hoặc mở thẳng từ link ngoài (Zalo/Messenger) —
// khi đó searchParams rỗng dù địa chỉ thật sự có "?id=...". Đọc thẳng
// window.location.search làm phương án dự phòng để không báo nhầm "thiếu mã đề".
function readIdFromLocation(): number | null {
  if (typeof window === "undefined") return null;
  const raw = new URLSearchParams(window.location.search).get("id");
  return raw ? Number(raw) : null;
}

function ExamLoader() {
  const { session } = useAuth();
  const searchParams = useSearchParams();
  const [fallbackId, setFallbackId] = useState<number | null>(() => readIdFromLocation());

  useEffect(() => {
    const sync = () => setFallbackId(readIdFromLocation());
    window.addEventListener("pageshow", sync);
    return () => window.removeEventListener("pageshow", sync);
  }, []);

  const id = Number(searchParams.get("id")) || fallbackId || 0;
  const itemIdParam = searchParams.get("item");
  const itemId = itemIdParam ? Number(itemIdParam) : null;
  const [exam, setExam] = useState<Exam | null>(null);
  const [minCorrect, setMinCorrect] = useState<number | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!session || !id) return;
    void (async () => {
      const supabase = getSupabase();
      let res = await supabase
        .from("exams")
        .select("id, title, duration_minutes, published, questions, pass_score")
        .eq("id", id)
        .single();
      // pass_score là cột mới (docs/supabase-migration-learning-progress.sql) — lùi
      // về danh sách cột cũ khi DB chưa chạy migration.
      if (res.error) {
        res = await supabase
          .from("exams")
          .select("id, title, duration_minutes, published, questions")
          .eq("id", id)
          .single();
      }
      if (res.error || !res.data) setError("Không tìm thấy đề này.");
      else setExam(res.data as Exam);
    })();
  }, [session, id]);

  useEffect(() => {
    if (!session || !itemId) return;
    getSupabase()
      .from("lesson_items")
      .select("kind, quiz_min_correct")
      .eq("id", itemId)
      .single()
      .then(({ data }) => {
        if (data?.kind === "ly_thuyet") setMinCorrect((data.quiz_min_correct as number | null) ?? null);
      });
  }, [session, itemId]);

  if (!id)
    return <p className="text-center text-slate-400">Thiếu mã đề trong địa chỉ.</p>;
  if (error) return <p className="text-center text-red-400">{error}</p>;
  if (!exam) return <p className="text-center text-slate-400">Đang tải đề…</p>;
  return <ExamRunner exam={exam} itemId={itemId} minCorrect={minCorrect} />;
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
