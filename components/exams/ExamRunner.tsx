"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import QuestionCard from "@/components/exams/QuestionCard";
import type { Exam, QuestionResponse } from "@/features/exams/types";
import {
  buildQuestionResults,
  emptyResponses,
  gradeExam,
  gradeQuestion,
  isAnswered,
  QUESTION_FORM_LABELS,
  questionTopicIds,
} from "@/features/exams/types";
import { fetchQuestionTopics } from "@/services/analytics";
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

  // Nhãn chủ đề + link ôn lại cho phần "Xem lại bài làm"
  const [topicMap, setTopicMap] = useState<
    Map<number, { name: string; lessonId: number | null }>
  >(new Map());
  useEffect(() => {
    if (phase !== "done") return;
    const ids = questionTopicIds(exam.questions);
    if (ids.length === 0) return;
    fetchQuestionTopics()
      .then((topics) =>
        setTopicMap(
          new Map(
            topics
              .filter((t) => ids.includes(t.id))
              .map((t) => [t.id, { name: t.name, lessonId: t.lessonId }]),
          ),
        ),
      )
      .catch(() => undefined);
  }, [phase, exam.questions]);

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
    const studentId = session.user.id;

    void (async () => {
      const supabase = getSupabase();
      const { data, error } = await supabase
        .from("exam_results")
        .insert({
          student_id: studentId,
          exam_id: exam.id,
          score: summary.score10,
          duration_seconds: Math.round((Date.now() - startedAt.current) / 1000),
          detail: {
            responses: finalResponses,
            correctCount: summary.correctCount,
          },
        })
        .select("id")
        .single();
      if (error || !data) {
        setSaveState("failed");
        return;
      }
      setSaveState("saved");
      // Chốt đúng/sai + nhãn từng câu để phân tích chủ đề. Không chặn — lỗi ở
      // đây chỉ mất dữ liệu phân tích, điểm vẫn được lưu ở trên.
      try {
        const topicIds = questionTopicIds(exam.questions);
        const names = new Map<number, string>();
        if (topicIds.length) {
          const { data: topics } = await supabase
            .from("question_topics")
            .select("id, name")
            .in("id", topicIds);
          for (const t of topics ?? []) names.set(t.id as number, t.name as string);
        }
        const rows = buildQuestionResults(exam.questions, finalResponses, names).map(
          (r) => ({ ...r, exam_result_id: data.id, student_id: studentId, exam_id: exam.id }),
        );
        await supabase.from("exam_question_results").insert(rows);
      } catch {
        /* bảng phân tích chưa có / lỗi mạng — bỏ qua */
      }
    })();
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
          className="mt-6 w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white transition-transform hover:-translate-y-0.5 hover:bg-primary-dark"
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
              secondsLeft <= 60 ? "text-red-400" : "text-cyan"
            }`}
          >
            {formatClock(secondsLeft)}
          </span>
          <button
            onClick={confirmSubmit}
            className="rounded-full bg-[#2563EB] px-4 py-1.5 text-sm font-semibold text-white hover:bg-primary-dark"
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
          className="mt-8 w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white hover:bg-primary-dark"
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
          href="/lop-hoc"
          className="mt-4 inline-block text-sm text-primary hover:underline"
        >
          ← Về danh sách đề
        </Link>
      </div>

      <h2 className="mt-10 mb-4 font-display text-xl font-semibold text-white">
        Xem lại bài làm
      </h2>
      <ol className="space-y-6">
        {exam.questions.map((q, qi) => {
          const g = q.type !== "essay" ? gradeQuestion(q, responses[qi]) : null;
          const wrong = g ? g.earned < g.max : false;
          const topicId = typeof q.topic_id === "number" ? q.topic_id : null;
          const topic = topicId ? topicMap.get(topicId) : undefined;
          const formLabel =
            q.form === "ly_thuyet" || q.form === "bai_tap"
              ? QUESTION_FORM_LABELS[q.form]
              : "";
          const stage = q.form === "ly_thuyet" ? "ly_thuyet" : "bai_tap_mau";
          return (
            <li key={qi}>
              {wrong && (topic?.name || formLabel) && (
                <div className="mb-2 flex flex-wrap items-center gap-2 text-xs">
                  {topic?.name && (
                    <span className="rounded-full bg-amber-500/15 px-2.5 py-1 font-semibold text-amber-300">
                      {topic.name}
                    </span>
                  )}
                  {formLabel && (
                    <span className="rounded-full border border-white/15 px-2.5 py-1 text-slate-400">
                      {formLabel}
                    </span>
                  )}
                  {topic?.lessonId && (
                    <Link
                      href={`/lop-hoc/bai/?id=${topic.lessonId}#secondary-stage-${stage}`}
                      className="font-semibold text-primary hover:underline"
                    >
                      Ôn ngay →
                    </Link>
                  )}
                </div>
              )}
              <QuestionCard
                index={qi + 1}
                question={q}
                response={responses[qi]}
                review
              />
            </li>
          );
        })}
      </ol>
    </div>
  );
}
