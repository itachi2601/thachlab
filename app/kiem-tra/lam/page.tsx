"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import ReadingZone from "@/components/ui/ReadingZone";
import { useAuth } from "@/components/auth/AuthProvider";
import ExamRunner from "@/components/exams/ExamRunner";
import type { Exam } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";
import { fetchMyClassIds } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { joinSampleClassIfUnset } from "@/services/exam-sample-join";

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
  const { session, realProfile } = useAuth();
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
  const [theoryLessonId, setTheoryLessonId] = useState<number | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!session || !id) return;
    void (async () => {
      const supabase = getSupabase();
      const loadExam = () =>
        supabase
          .from("exams")
          .select("id, title, duration_minutes, published, questions, pass_score")
          .eq("id", id)
          .single();
      let res = await loadExam();
      // pass_score là cột mới (docs/supabase-migration-learning-progress.sql) — lùi
      // về danh sách cột cũ khi DB chưa chạy migration.
      if (res.error) {
        res = await supabase
          .from("exams")
          .select("id, title, duration_minutes, published, questions")
          .eq("id", id)
          .single();
      }
      // Đề mẫu: em vừa đăng ký có thể chưa có dòng lớp, RLS chặn đọc đề.
      // Vào đúng lớp của đề rồi đọc lại một lần.
      const isStaffEarly =
        realProfile?.role === "admin" ||
        realProfile?.role === "instructor" ||
        realProfile?.role === "tro_giang";
      if ((res.error || !res.data) && !isStaffEarly) {
        const joined = await joinSampleClassIfUnset(id, session.user.id).catch(() => false);
        if (joined) res = await loadExam();
      }
      if (res.error || !res.data) {
        setError("Không tìm thấy đề này.");
        return;
      }
      if (!res.data.published) {
        setError("Đề này đang ẩn, chưa thể làm bài.");
        return;
      }
      // Chặn học sinh làm đề không thuộc lớp của mình (đoán/chia sẻ id đề) —
      // staff (admin/instructor/tro_giang) không bị chặn, khớp RLS phía DB
      // (migration 20260927150000_exam_class_access.sql).
      const isStaff =
        realProfile?.role === "admin" ||
        realProfile?.role === "instructor" ||
        realProfile?.role === "tro_giang";
      if (!isStaff) {
        const [{ data: examClasses }, myClassIds] = await Promise.all([
          supabase.from("exam_classes").select("class_id").eq("exam_id", id),
          fetchMyClassIds(session.user.id),
        ]);
        const examClassIds = (examClasses ?? []).map((r) => r.class_id as number);
        let allowed = visibleTo(examClassIds, myClassIds);
        if (!allowed) {
          const joined = await joinSampleClassIfUnset(id, session.user.id).catch(() => false);
          if (joined) {
            const again = await fetchMyClassIds(session.user.id);
            allowed = visibleTo(examClassIds, again);
          }
        }
        if (!allowed) {
          setError("Đề này không thuộc lớp của em, không thể làm bài.");
          return;
        }
      }
      setExam(res.data as Exam);
    })();
  }, [session, id, realProfile]);

  useEffect(() => {
    if (!session || !itemId) return;
    getSupabase()
      .from("lesson_items")
      .select("kind, quiz_min_correct, lesson_id")
      .eq("id", itemId)
      .single()
      .then(({ data }) => {
        if (data?.kind === "ly_thuyet") {
          setMinCorrect((data.quiz_min_correct as number | null) ?? null);
          setTheoryLessonId((data.lesson_id as number | null) ?? null);
        }
      });
  }, [session, itemId]);

  if (!id)
    return <p className="text-center text-slate-400">Thiếu mã đề trong địa chỉ.</p>;
  if (error) return <p className="text-center text-red-400">{error}</p>;
  if (!exam) return <p className="text-center text-slate-400">Đang tải đề…</p>;
  return <ExamRunner exam={exam} itemId={itemId} minCorrect={minCorrect} theoryLessonId={theoryLessonId} />;
}

export default function TakeExamPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <RequireAuth>
          <ReadingZone>
            <Suspense
              fallback={<p className="text-center text-slate-400">Đang tải…</p>}
            >
              <ExamLoader />
            </Suspense>
          </ReadingZone>
        </RequireAuth>
      </main>
      <Footer variant="app" />
    </>
  );
}
