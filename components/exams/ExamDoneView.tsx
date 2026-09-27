"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import ExamResultSummary, { type ResultBadge } from "@/components/exams/ExamResultSummary";
import ExamReviewPager from "@/components/exams/ExamReviewPager";
import Button from "@/components/ui/Button";
import type { Exam, QuestionResponse } from "@/features/exams/types";
import {
  gradeExam,
  gradeQuestion,
  QUESTION_FORM_LABELS,
  questionTopicNames,
} from "@/features/exams/types";
import { deriveTheoryStatus, STATUS_LABELS } from "@/features/progress/types";
import { saveTheoryReviewContext, type TheoryReviewContext } from "@/features/lessons/theory-sections";
import { fetchQuestionTopics } from "@/services/analytics";

function formatClock(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

/**
 * Màn hình sau khi nộp bài (điểm + xem lại từng câu) — tách khỏi ExamRunner.tsx và tải qua
 * `next/dynamic({ ssr: false })` (xem components/exams/ExamRunner.tsx) vì học sinh KHÔNG thấy
 * màn này ngay khi vào trang (chỉ hiện sau khi bấm "Nộp bài"): kéo theo ExamResultSummary +
 * ExamReviewPager (bảng thống kê, xem lại bài làm) — phần "không phải câu hỏi đang hiển thị
 * ngay" theo đúng mục tiêu đợt tối ưu tốc độ lần 4 (perf4/RESULT.md). KHÔNG đổi logic chấm
 * điểm/nộp bài — mọi tính toán ở đây thuần đọc props, không ghi Supabase (việc ghi điểm vẫn nằm
 * trong ExamRunner.save()).
 */
export default function ExamDoneView({
  exam,
  responses,
  itemId,
  minCorrect,
  theoryLessonId,
  usedSeconds,
  saveState,
  onRetry,
}: {
  exam: Exam;
  responses: QuestionResponse[];
  itemId: number | null;
  minCorrect: number | null;
  theoryLessonId: number | null;
  usedSeconds: number;
  saveState: "idle" | "saving" | "saved" | "failed";
  onRetry: () => void;
}) {
  const { profile } = useAuth();

  // Chủ đề -> bài học để làm nút "Ôn ngay" ở phần "Xem lại bài làm".
  const [lessonByTopic, setLessonByTopic] = useState<Map<string, number | null>>(new Map());
  useEffect(() => {
    const names = questionTopicNames(exam.questions);
    if (names.length === 0) return;
    fetchQuestionTopics()
      .then((topics) => setLessonByTopic(new Map(topics.map((t) => [t.name, t.lessonId]))))
      .catch(() => undefined);
  }, [exam.questions]);

  const finalSummary = gradeExam(exam.questions, responses);
  const hasEssay = exam.questions.some((q) => q.type === "essay");
  let badge: ResultBadge | null = null;
  if (hasEssay) {
    badge = { label: STATUS_LABELS.pending_grading, tone: "pending" };
  } else if (minCorrect !== null) {
    const t = deriveTheoryStatus({
      confirmedRead: true,
      quizAttempts: [{ createdAt: new Date().toISOString(), correctCount: finalSummary.correctCount }],
      minCorrect,
    });
    badge =
      t.status === "passed"
        ? { label: STATUS_LABELS.passed, tone: "pass" }
        : { label: STATUS_LABELS.completed_not_passed, tone: "fail" };
  } else if (exam.pass_score != null) {
    badge =
      finalSummary.score10 >= exam.pass_score
        ? { label: STATUS_LABELS.passed, tone: "pass" }
        : { label: STATUS_LABELS.completed_not_passed, tone: "fail" };
  }

  return (
    <div className="mx-auto max-w-3xl">
      <ExamResultSummary
        questions={exam.questions}
        responses={responses}
        detailAnchor="xem-lai-bai-lam"
        badge={badge}
        meta={
          <>
            {profile?.full_name}
            {profile?.class_name && ` · Lớp ${profile.class_name}`}
            {` · ${exam.title} · ${formatClock(usedSeconds)}`}
          </>
        }
      />
      {hasEssay && (
        <p className="mt-3 text-center text-xs text-violet-300">
          Đề có {exam.questions.filter((q) => q.type === "essay").length} câu tự luận — thầy/cô chấm xong,
          điểm sẽ được cập nhật.
        </p>
      )}

      <div className="mt-4 flex flex-col items-center gap-2 text-center text-xs text-slate-500">
        {saveState === "saving" && <span>Đang lưu điểm…</span>}
        {saveState === "saved" && <span>✓ Đã ghi nhận</span>}
        {saveState === "failed" && (
          <>
            <span className="text-red-300">Chưa lưu được điểm — kiểm tra mạng rồi thử lại, đừng tắt trang này.</span>
            <Button variant="outline" size="sm" onClick={onRetry}>
              Thử lại
            </Button>
          </>
        )}
      </div>
      <p className="mt-2 text-center">
        <Link href="/lop-hoc" className="text-sm text-primary hover:underline">
          ← Về danh sách đề
        </Link>
      </p>

      <h2
        id="xem-lai-bai-lam"
        className="mt-10 mb-4 scroll-mt-24 font-display text-xl font-semibold text-white"
      >
        Xem lại bài làm
      </h2>
      <p className="mb-4 text-sm text-slate-500">
        Bấm số câu ở bảng bên dưới để xem nhanh — bảng luôn ghim trên đầu khi em cuộn trang.
      </p>
      {(() => {
        // Gom TẤT CẢ câu sai có gắn theorySection trong lượt này — bấm "Ôn ngay" ở BẤT KỲ câu
        // nào cũng mang theo đủ cả bộ, để trang bài học tô đúng MỌI đoạn liên quan cùng lúc
        // thay vì chỉ đoạn của câu vừa bấm (sai nhiều câu ở nhiều đoạn khác nhau thì đoạn cũ
        // sẽ mất dấu nếu chỉ mang theo 1 câu).
        const allTheoryReviewContexts: TheoryReviewContext[] =
          itemId && theoryLessonId
            ? exam.questions
                .map((q, qi): TheoryReviewContext | null => {
                  if (q.theorySection === undefined) return null;
                  const g = q.type !== "essay" ? gradeQuestion(q, responses[qi]) : null;
                  if (!g || g.earned >= g.max) return null;
                  return {
                    itemId,
                    sectionIndex: q.theorySection,
                    questionIndex: qi + 1,
                    questionHtml: q.question,
                    pickedHtml: q.type === "multiple_choice" && typeof responses[qi] === "number" ? q.options[responses[qi] as number] : null,
                    correctHtml: q.type === "multiple_choice" ? q.options[q.answer] : null,
                  };
                })
                .filter((c): c is TheoryReviewContext => c !== null)
            : [];
        return (
          <ExamReviewPager
            questions={exam.questions}
            responses={responses}
            renderAbove={(qi) => {
              const q = exam.questions[qi];
              const g = q.type !== "essay" ? gradeQuestion(q, responses[qi]) : null;
              const wrong = g ? g.earned < g.max : false;
              const topicName = (q.topic ?? "").trim();
              const formLabel =
                q.form === "ly_thuyet" || q.form === "bai_tap"
                  ? QUESTION_FORM_LABELS[q.form]
                  : "";
              const stage = q.form === "ly_thuyet" ? "ly_thuyet" : "bai_tap_mau";
              // Câu có gắn theorySection VÀ đây đúng là quiz kiểm tra nhanh của chính bài đó (có
              // theoryLessonId + itemId) → nhảy thẳng + tô màu đúng đoạn lý thuyết liên quan, chính
              // xác hơn hẳn so với tra theo tên chủ đề (chỉ đưa được tới đầu cả mục lý thuyết).
              const preciseHref =
                q.theorySection !== undefined && theoryLessonId && itemId
                  ? `/lop-hoc/bai/?id=${theoryLessonId}&item=${itemId}#theory-sec-${itemId}-${q.theorySection}`
                  : null;
              const lessonId = topicName ? lessonByTopic.get(topicName) : undefined;
              const reviewHref = preciseHref ?? (lessonId ? `/lop-hoc/bai/?id=${lessonId}#secondary-stage-${stage}` : null);
              if (!wrong || (!topicName && !formLabel)) return null;
              return (
                <div className="mb-2 flex flex-wrap items-center gap-2 text-xs">
                  {topicName && (
                    <span className="rounded-full bg-amber-500/15 px-2.5 py-1 font-semibold text-amber-300">
                      {topicName}
                    </span>
                  )}
                  {formLabel && (
                    <span className="rounded-full border border-white/15 px-2.5 py-1 text-slate-400">
                      {formLabel}
                    </span>
                  )}
                  {reviewHref && (
                    <Link
                      href={reviewHref}
                      onClick={() => preciseHref && allTheoryReviewContexts.length > 0 && saveTheoryReviewContext(allTheoryReviewContexts)}
                      className="font-semibold text-primary hover:underline"
                    >
                      Ôn ngay →
                    </Link>
                  )}
                </div>
              );
            }}
          />
        );
      })()}
    </div>
  );
}
