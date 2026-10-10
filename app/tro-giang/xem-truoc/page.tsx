"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ClipboardCheck } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import NotRegistered from "@/components/tro-giang/NotRegistered";
import TaPreviewRunner from "@/components/tro-giang/TaPreviewRunner";
import { useAssistantOrDemo } from "@/lib/tro-giang/useAssistant";
import { fetchMyTaPreviews, fetchPreviewExam, taPreviewPath, type TaPreviewRow } from "@/services/exam-ta-preview";
import type { ExamQuestion } from "@/features/exams/types";

function List() {
  const [rows, setRows] = useState<TaPreviewRow[] | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    fetchMyTaPreviews().then(setRows).catch(() => setError("Không tải được danh sách đề."));
  }, []);
  if (error) return <p className="text-red-400">{error}</p>;
  if (!rows) return <p className="text-slate-400">Đang tải…</p>;
  return (
    <div className="space-y-5">
      <Link href="/tro-giang" className="text-sm text-blue-300 underline">← Trang trợ giảng</Link>
      <h1 className="text-xl font-bold text-white">Đề thầy gửi xem trước</h1>
      <p className="text-sm text-slate-400">Làm thử từng câu, đáp án hiện ngay sau mỗi câu. Làm xong sẽ sang phân tích tình hình lớp.</p>
      {rows.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">Thầy chưa gửi đề nào.</p>
      ) : (
        <ul className="space-y-2">
          {rows.map((r) => (
            <li key={`${r.exam_id}-${r.class_id}`}>
              <Link
                href={taPreviewPath(r.exam_id, r.class_id)}
                className="flex min-h-12 items-center gap-3 rounded-2xl border border-white/10 bg-panel px-4 py-3 text-white"
              >
                <ClipboardCheck size={18} className="shrink-0 text-blue-300" />
                <span className="flex-1">
                  {r.exams?.title ?? `Đề #${r.exam_id}`}
                  <span className="block text-xs text-slate-400">
                    {r.classes?.name} · {r.exams?.questions?.length ?? 0} câu
                  </span>
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Preview({ examId, classParam }: { examId: number; classParam: number }) {
  const [state, setState] = useState<{ title: string; questions: ExamQuestion[]; classId: number } | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchPreviewExam(examId), classParam ? Promise.resolve(null) : fetchMyTaPreviews()])
      .then(([exam, previews]) => {
        if (cancelled) return;
        const classId = classParam || previews?.find((p) => p.exam_id === examId)?.class_id || 0;
        if (!classId) return setError("Thầy chưa gửi đề này cho lớp nào.");
        const questions = (exam.questions as ExamQuestion[]) ?? [];
        if (!questions.length) return setError("Đề này chưa có câu hỏi.");
        setState({ title: exam.title as string, questions, classId });
      })
      .catch(() => !cancelled && setError("Không mở được đề — thầy chưa gửi đề này cho trợ giảng."));
    return () => {
      cancelled = true;
    };
  }, [examId, classParam]);
  if (error) return <p className="text-red-400">{error}</p>;
  if (!state) return <p className="text-slate-400">Đang tải đề…</p>;
  return <TaPreviewRunner title={state.title} examId={examId} classId={state.classId} questions={state.questions} />;
}

function Loader() {
  const { assistant } = useAssistantOrDemo();
  const params = useSearchParams();
  const examId = Number(params.get("exam")) || 0;
  const classId = Number(params.get("class")) || 0;
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-2xl px-5 pt-28 pb-16">
        {assistant === undefined ? (
          <p className="text-slate-400">Đang tải…</p>
        ) : assistant === null ? (
          <NotRegistered />
        ) : examId ? (
          <Preview examId={examId} classParam={classId} />
        ) : (
          <List />
        )}
      </main>
      <Footer variant="app" />
    </>
  );
}

export default function TroGiangXemTruocPage() {
  return (
    <RequireAuth>
      <Suspense fallback={<p className="p-10 text-center text-slate-400">Đang tải…</p>}>
        <Loader />
      </Suspense>
    </RequireAuth>
  );
}
