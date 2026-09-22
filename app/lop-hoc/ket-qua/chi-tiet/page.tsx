"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ChevronDown, ChevronLeft, Trophy } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import QuestionCard from "@/components/exams/QuestionCard";
import ExamResultSummary from "@/components/exams/ExamResultSummary";
import {
  QUESTION_STATUS_LABELS,
  questionStatus,
  type QuestionStatus,
} from "@/features/exams/types";
import {
  fetchExamRank,
  fetchMyExamResultDetail,
  type ExamRank,
  type MyExamAttemptDetail,
} from "@/services/analytics";
import { supabaseConfigured } from "@/services/supabase";

const STATUS_PILL: Record<QuestionStatus, string> = {
  correct: "bg-emerald-500/15 text-emerald-300",
  partial: "bg-amber-500/15 text-amber-300",
  wrong: "bg-red-500/15 text-red-300",
  skipped: "bg-slate-500/20 text-slate-400",
  manual: "bg-violet-500/15 text-violet-300",
};

function AttemptDetail({ resultId }: { resultId: number }) {
  const [detail, setDetail] = useState<MyExamAttemptDetail | null | undefined>(undefined);
  const [rank, setRank] = useState<ExamRank | null>(null);

  useEffect(() => {
    fetchMyExamResultDetail(resultId).then(setDetail).catch(() => setDetail(null));
  }, [resultId]);

  useEffect(() => {
    if (!detail) return;
    fetchExamRank(detail.examId).then(setRank).catch(() => setRank(null));
  }, [detail]);

  if (detail === undefined) {
    return <p className="mt-10 text-center text-sm text-slate-400">Đang tải bài làm…</p>;
  }
  if (detail === null) {
    return (
      <p className="mt-10 text-center text-sm text-slate-500">
        Không tải được bài làm này.
      </p>
    );
  }

  const dateLabel = new Date(detail.createdAt).toLocaleDateString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });

  return (
    <>
      <div className="mb-4">
        <h1 className="font-display text-2xl font-bold text-white">{detail.examTitle}</h1>
        <p className="mt-1 text-sm text-slate-400">Làm ngày {dateLabel}</p>
      </div>

      <ExamResultSummary
        questions={detail.questions}
        responses={detail.responses}
        anchorPrefix="cau"
        detailAnchor="xem-lai-tung-cau"
        meta={
          rank ? (
            <span className="inline-flex items-center gap-1.5">
              <Trophy size={14} className="text-amber-300" />
              Hạng <b className="text-white">{rank.rank}</b>/{rank.total} trong lớp ở đề này
            </span>
          ) : undefined
        }
      />

      <h2
        id="xem-lai-tung-cau"
        className="mt-10 mb-4 scroll-mt-24 font-display text-xl font-semibold text-white"
      >
        Xem lại từng câu
      </h2>
      <p className="mb-4 text-sm text-slate-500">
        Bấm vào số câu ở bảng phía trên để nhảy nhanh tới câu đó. Câu sai/làm dở tự mở sẵn.
      </p>
      <ol className="space-y-3">
        {detail.questions.map((q, i) => {
          const status = questionStatus(q, detail.responses[i]);
          return (
            <li key={i}>
              <details id={`cau-${i + 1}`} open={status !== "correct"} className="scroll-mt-24 group">
                <summary className="flex cursor-pointer list-none items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-5 py-3.5 hover:border-white/25">
                  <span className="font-display font-semibold text-white">Câu {i + 1}</span>
                  <span
                    className={`ml-auto rounded-lg px-2.5 py-1 text-xs font-semibold ${STATUS_PILL[status]}`}
                  >
                    {QUESTION_STATUS_LABELS[status]}
                  </span>
                  <ChevronDown
                    size={18}
                    className="shrink-0 text-slate-500 transition-transform group-open:rotate-180"
                  />
                </summary>
                <div className="mt-3">
                  <QuestionCard index={i + 1} question={q} response={detail.responses[i]} review />
                </div>
              </details>
            </li>
          );
        })}
      </ol>
    </>
  );
}

function DetailLoader() {
  const searchParams = useSearchParams();
  const resultId = Number(searchParams.get("id"));
  // Phụ huynh mở từ /phu-huynh (link mang ?ph=1) — quay về đúng chỗ.
  const fromParent = searchParams.get("ph") === "1";

  if (!resultId || Number.isNaN(resultId)) {
    return (
      <p className="mt-10 text-center text-sm text-slate-500">
        Không tìm thấy bài làm — thiếu mã bài làm trên đường dẫn.
      </p>
    );
  }

  return (
    <>
      <Link
        href={fromParent ? "/phu-huynh/" : "/lop-hoc/ket-qua/"}
        className="mb-6 inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-white"
      >
        <ChevronLeft size={16} /> {fromParent ? "Về Kết quả của con" : "Về Kết quả học tập"}
      </Link>
      <RequireAuth>
        <AttemptDetail key={resultId} resultId={resultId} />
      </RequireAuth>
    </>
  );
}

export default function KetQuaChiTietPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full">
        <div className="mx-auto w-full max-w-3xl px-6 pb-20 pt-28">
          {!supabaseConfigured ? (
            <p className="text-center text-slate-400">Hệ thống đang được cấu hình.</p>
          ) : (
            <Suspense
              fallback={<p className="text-center text-sm text-slate-400">Đang tải…</p>}
            >
              <DetailLoader />
            </Suspense>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
