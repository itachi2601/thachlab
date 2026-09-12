"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import RequireAuth from "@/components/auth/RequireAuth";
import ReviewBoard from "@/components/dashboard/ReviewBoard";
import { fetchClassStudents } from "@/services/classes";
import { fetchExamReviewData, type ExamReviewData } from "@/services/analytics";

function ReviewLoader() {
  const searchParams = useSearchParams();
  const examId = Number(searchParams.get("exam"));
  const classId = Number(searchParams.get("class"));
  const [data, setData] = useState<ExamReviewData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!examId || !classId) return;
    let cancelled = false;
    fetchClassStudents(classId)
      .then((students) => fetchExamReviewData(examId, students.map((s) => s.id)))
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((err: unknown) => {
        if (!cancelled)
          setError(err instanceof Error ? err.message : "Không tải được dữ liệu chữa bài.");
      });
    return () => {
      cancelled = true;
    };
  }, [examId, classId]);

  if (!examId || !classId)
    return (
      <p className="p-10 text-center text-slate-400">
        Thiếu mã đề hoặc mã lớp trong địa chỉ — mở màn hình này từ tab Phân tích.
      </p>
    );
  if (error) return <p className="p-10 text-center text-red-400">{error}</p>;
  if (!data) return <p className="p-10 text-center text-slate-400">Đang tải đề…</p>;
  if (data.questions.length === 0)
    return <p className="p-10 text-center text-slate-400">Đề này chưa có câu hỏi.</p>;

  return <ReviewBoard data={data} />;
}

export default function ChuaBaiPage() {
  return (
    <RequireAuth area="thpt">
      <Suspense fallback={<p className="p-10 text-center text-slate-400">Đang tải…</p>}>
        <ReviewLoader />
      </Suspense>
    </RequireAuth>
  );
}
