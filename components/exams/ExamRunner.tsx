"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import QuestionCard from "@/components/exams/QuestionCard";
import type { Exam, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeExam, isAnswered } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

type Phase = "intro" | "running" | "done";

function formatClock(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export default function ExamRunner({ exam }: { exam: Exam }) {
  const { session, profile } = useAuth();
  const [phase, setPhase] = useState<Phase>("intro");
  const [responses, setResponses] = useState<QuestionResponse[]>(() =>
    emptyResponses(exam.questions),
  );
  const [secondsLeft, setSecondsLeft] = useState(exam.duration_minutes * 60);
  const [saveState, setSaveState] = useState<
    "idle" | "saving" | "saved" | "failed"
  >("idle");
  const [usedSeconds, setUsedSeconds] = useState(0);
  const startedAt = useRef(0);
  const submittedRef = useRef(false);
  const responsesRef = useRef(responses);

  const answeredCount = exam.questions.filter((q, i) =>
    isAnswered(q, responses[i]),
  ).length;

  // submit được gọi từ nút bấm và từ interval hết giờ — chấm và lưu ngay tại đây
  const submit = useCallback(() => {
    if (submittedRef.current) return;
    submittedRef.current = true;
    setUsedSeconds(Math.round((Date.now() - startedAt.current) / 1000));
    setPhase("done");
    if (!session) return;
    setSaveState("saving");
    const finalResponses = responsesRef.current;
    const summary = gradeExam(exam.questions, finalResponses);
    getSupabase()
      .from("exam_results")
      .insert({
        student_id: session.user.id,
        exam_id: exam.id,
        score: summary.score10,
        duration_seconds: Math.round((Date.now() - startedAt.current) / 1000),
        detail: {
          responses: finalResponses,
          correctCount: summary.correctCount,
        },
      })
      .then(({ error }) => setSaveState(error ? "failed" : "saved"));
  }, [exam, session]);

  const confirmSubmit = () => {
    if (
      answeredCount === exam.questions.length ||
      confirm(
        `Còn ${exam.questions.length - answeredCount} câu chưa làm. Nộp bài luôn?`,
      )
    )
      submit();
  };

  useEffect(() => {
    if (phase !== "running") return;
    const timer = setInterval(() => {
      setSecondsLeft((s) => {
        if (s <= 1) {
          submit();
          return 0;
        }
        return s - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [phase, submit]);

  if (phase === "intro") {
    return (
      <div className="mx-auto max-w-xl rounded-2xl border border-white/10 bg-[#0B1020] p-8">
        <h1 className="font-display text-2xl font-bold text-white">
          {exam.title}
        </h1>
        <p className="mt-3 text-sm text-slate-400">
          {exam.questions.length} câu · {exam.duration_minutes} phút · nộp bài
          là có điểm ngay kèm lời giải
        </p>
        <p className="mt-2 text-sm text-slate-400">
          Học sinh:{" "}
          <span className="font-semibold text-white">
            {profile?.full_name}
          </span>
          {profile?.class_name && ` · Lớp ${profile.class_name}`}
        </p>
        <button
          onClick={() => {
            startedAt.current = Date.now();
            setPhase("running");
          }}
          className="mt-6 w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white transition-transform hover:-translate-y-0.5 hover:bg-[#1D4ED8]"
        >
          Bắt đầu làm bài
        </button>
      </div>
    );
  }

  if (phase === "running") {
    return (
      <div className="mx-auto max-w-3xl">
        <div className="sticky top-16 z-40 mb-6 flex items-center justify-between rounded-2xl border border-white/10 bg-[#0B1020]/95 px-5 py-3 backdrop-blur-md">
          <span className="text-sm text-slate-400">
            Đã làm{" "}
            <span className="font-semibold text-white">
              {answeredCount}/{exam.questions.length}
            </span>{" "}
            câu
          </span>
          <span
            className={`font-mono text-lg font-semibold ${
              secondsLeft <= 60 ? "text-red-400" : "text-[#22D3EE]"
            }`}
          >
            {formatClock(secondsLeft)}
          </span>
          <button
            onClick={confirmSubmit}
            className="rounded-full bg-[#2563EB] px-4 py-1.5 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
          >
            Nộp bài
          </button>
        </div>

        <ol className="space-y-6">
          {exam.questions.map((q, qi) => (
            <li key={qi}>
              <QuestionCard
                index={qi + 1}
                question={q}
                response={responses[qi]}
                onChange={(r) => {
                  const next = [...responsesRef.current];
                  next[qi] = r;
                  responsesRef.current = next;
                  setResponses(next);
                }}
              />
            </li>
          ))}
        </ol>

        <button
          onClick={confirmSubmit}
          className="mt-8 w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
        >
          Nộp bài
        </button>
      </div>
    );
  }

  const summary = gradeExam(exam.questions, responses);
  return (
    <div className="mx-auto max-w-3xl">
      <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-8 text-center">
        <p className="text-sm text-slate-400">
          {profile?.full_name}
          {profile?.class_name && ` · Lớp ${profile.class_name}`}
        </p>
        <p className="mt-2 font-display text-5xl font-bold text-gradient">
          {summary.score10.toLocaleString("vi-VN")}
        </p>
        <p className="mt-2 text-slate-300">
          Đúng trọn vẹn {summary.correctCount}/{exam.questions.length} câu ·{" "}
          {formatClock(usedSeconds)}
        </p>
        <p className="mt-3 text-xs text-slate-500">
          {saveState === "saving" && "Đang lưu điểm…"}
          {saveState === "saved" && "✓ Điểm đã được lưu"}
          {saveState === "failed" &&
            "Không lưu được điểm — hãy chụp màn hình kết quả gửi thầy"}
        </p>
        <Link
          href="/kiem-tra"
          className="mt-4 inline-block text-sm text-[#3B82F6] hover:underline"
        >
          ← Về danh sách đề
        </Link>
      </div>

      <h2 className="mt-10 mb-4 font-display text-xl font-semibold text-white">
        Xem lại bài làm
      </h2>
      <ol className="space-y-6">
        {exam.questions.map((q, qi) => (
          <li key={qi}>
            <QuestionCard
              index={qi + 1}
              question={q}
              response={responses[qi]}
              review
            />
          </li>
        ))}
      </ol>
    </div>
  );
}
