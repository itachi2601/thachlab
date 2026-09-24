"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Flag } from "lucide-react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { useAuth } from "@/components/auth/AuthProvider";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import ExamResultSummary, { type ResultBadge } from "@/components/exams/ExamResultSummary";
import ExamReviewPager from "@/components/exams/ExamReviewPager";
import type { Exam, ExamQuestion, QuestionResponse } from "@/features/exams/types";
import {
  buildQuestionResults,
  emptyResponses,
  gradeExam,
  gradeQuestion,
  isAnswered,
  QUESTION_FORM_LABELS,
  questionTopicNames,
} from "@/features/exams/types";
import { deriveTheoryStatus, STATUS_LABELS } from "@/features/progress/types";
import { fetchQuestionTopics } from "@/services/analytics";
import {
  finishExamAttempt,
  findExistingExamResultId,
  findOpenExamAttempt,
  saveExamAttemptProgress,
  startExamAttempt,
  type OpenExamAttempt,
} from "@/services/progress";
import { getSupabase } from "@/services/supabase";

type Phase = "intro" | "running" | "done";

type ViolationType = "tab_switch" | "fullscreen_exit";
type Violation = { type: ViolationType; at: string; away_ms: number };

// Trạng thái một câu trên bảng câu hỏi. Câu đúng/sai có 4 ý nên còn nấc "làm dở":
// em bấm được vài ý rồi bỏ qua, nhìn bảng phải thấy ngay chỗ còn thiếu.
type AnswerState = "done" | "partial" | "empty";

function answerState(q: ExamQuestion, r: QuestionResponse): AnswerState {
  if (q.type === "true_false") {
    const picks = Array.isArray(r) ? r : [];
    const filled = q.statements.filter((_, i) => picks[i] != null).length;
    if (filled === 0) return "empty";
    return filled === q.statements.length ? "done" : "partial";
  }
  return isAnswered(q, r) ? "done" : "empty";
}

function formatClock(totalSeconds: number) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export default function ExamRunner({
  exam,
  itemId = null,
  minCorrect = null,
}: {
  exam: Exam;
  /** Mục bài học đang gắn đề này (nếu có) — dùng để ghi nhận exam_attempts. */
  itemId?: number | null;
  /** Chỉ có khi đây là quiz kiểm tra nhanh cuối lý thuyết: số câu đúng tối thiểu để đạt. */
  minCorrect?: number | null;
}) {
  const { session, profile } = useAuth();
  const reduceMotion = useReducedMotion();
  const [phase, setPhase] = useState<Phase>("intro");
  const [responses, setResponses] = useState<QuestionResponse[]>(() =>
    emptyResponses(exam.questions),
  );
  const [secondsLeft, setSecondsLeft] = useState(exam.duration_minutes * 60);
  const [saveState, setSaveState] = useState<
    "idle" | "saving" | "saved" | "failed"
  >("idle");
  const [usedSeconds, setUsedSeconds] = useState(0);
  const [cur, setCur] = useState(0);
  const [flags, setFlags] = useState<Set<number>>(new Set());
  const [paletteOpen, setPaletteOpen] = useState(true);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [violationBanner, setViolationBanner] = useState<{
    type: ViolationType;
    text: string;
  } | null>(null);
  const topRef = useRef<HTMLDivElement>(null);
  const startedAt = useRef(0);
  const submittedRef = useRef(false); // chặn nộp 2 lần (nút + hết giờ), KHÔNG chặn thử lưu lại
  const responsesRef = useRef(responses);
  const violationsRef = useRef<Violation[]>([]);
  const hiddenAtRef = useRef<number | null>(null);
  const everFullscreenRef = useRef(false);
  // Sinh 1 lần/lượt làm, giữ nguyên khi bấm "Thử lại" — chống lưu trùng nếu mạng lỗi giữa chừng.
  // Nếu khôi phục bài đang làm dở thì thay bằng client_token của lượt cũ (xem beginExam).
  const clientTokenRef = useRef<string>(crypto.randomUUID());
  const savedResultIdRef = useRef<number | null>(null);
  const secondsLeftRef = useRef(secondsLeft);

  // Bài đang làm dở của học sinh này cho đúng đề này (nếu có) — dò 1 lần khi vào
  // màn hình giới thiệu, undefined = đang dò, null = không có.
  const [resumable, setResumable] = useState<OpenExamAttempt | null | undefined>(undefined);
  useEffect(() => {
    if (!session || phase !== "intro") return;
    let cancelled = false;
    findOpenExamAttempt(session.user.id, exam.id).then((a) => {
      if (!cancelled) setResumable(a);
    });
    return () => {
      cancelled = true;
    };
  }, [session, exam.id, phase]);

  const answeredCount = exam.questions.filter((q, i) =>
    isAnswered(q, responses[i]),
  ).length;
  const lastIndex = exam.questions.length - 1;

  // Đổi câu thì kéo về đầu câu mới, đừng để em phải cuộn ngược lên
  function goTo(idx: number) {
    setCur(Math.min(lastIndex, Math.max(0, idx)));
    topRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function toggleFlag(idx: number) {
    setFlags((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }

  // Chủ đề -> bài học để làm nút "Ôn ngay" ở phần "Xem lại bài làm"
  const [lessonByTopic, setLessonByTopic] = useState<Map<string, number | null>>(new Map());
  useEffect(() => {
    if (phase !== "done") return;
    const names = questionTopicNames(exam.questions);
    if (names.length === 0) return;
    fetchQuestionTopics()
      .then((topics) =>
        setLessonByTopic(new Map(topics.map((t) => [t.name, t.lessonId]))),
      )
      .catch(() => undefined);
  }, [phase, exam.questions]);

  // Lưu điểm — retry-an-toàn: kiểm tra client_token đã có chưa trước khi insert,
  // để bấm "Thử lại" sau lỗi mạng không tạo thêm một lượt làm mới.
  const save = useCallback(() => {
    if (!session) return;
    setSaveState("saving");
    const finalResponses = responsesRef.current;
    const summary = gradeExam(exam.questions, finalResponses);
    const studentId = session.user.id;
    const token = clientTokenRef.current;

    void (async () => {
      const supabase = getSupabase();
      let resultId = savedResultIdRef.current ?? (await findExistingExamResultId(token).catch(() => null));
      if (!resultId) {
        const base = {
          student_id: studentId,
          exam_id: exam.id,
          score: summary.score10,
          duration_seconds: Math.round((Date.now() - startedAt.current) / 1000),
          detail: {
            responses: finalResponses,
            correctCount: summary.correctCount,
          },
          violation_count: violationsRef.current.length,
          violations: violationsRef.current,
        };
        let res = await supabase.from("exam_results").insert({ ...base, client_token: token }).select("id").single();
        // client_token là cột mới (migration chưa chạy) — lùi về insert không có token,
        // chấp nhận mất khả năng chống trùng khi thử lại trên DB cũ.
        if (res.error) res = await supabase.from("exam_results").insert(base).select("id").single();
        if (res.error || !res.data) {
          setSaveState("failed");
          return;
        }
        resultId = res.data.id as number;
      }
      savedResultIdRef.current = resultId;
      setSaveState("saved");
      void finishExamAttempt(token, resultId);
      // Chốt đúng/sai + nhãn từng câu để phân tích chủ đề. Không chặn — lỗi ở
      // đây chỉ mất dữ liệu phân tích, điểm vẫn được lưu ở trên. Nếu lượt lưu
      // trước đã tạo các dòng này rồi thì insert lại chỉ va khóa chính, bỏ qua.
      try {
        const names = questionTopicNames(exam.questions);
        const idByName = new Map<string, number>();
        if (names.length) {
          const { data: topics } = await supabase
            .from("question_topics")
            .select("id, name")
            .in("name", names);
          for (const t of topics ?? []) idByName.set(t.name as string, t.id as number);
        }
        const rows = buildQuestionResults(exam.questions, finalResponses, idByName).map(
          (r) => ({ ...r, exam_result_id: resultId, student_id: studentId, exam_id: exam.id }),
        );
        await supabase.from("exam_question_results").insert(rows);
      } catch {
        /* bảng phân tích chưa có / lỗi mạng / đã có từ lượt lưu trước — bỏ qua */
      }
    })();
  }, [exam, session]);

  // submit được gọi từ nút bấm và từ interval hết giờ — chuyển màn hình 1 lần rồi lưu
  const submit = useCallback(() => {
    if (submittedRef.current) return;
    submittedRef.current = true;
    setUsedSeconds(Math.round((Date.now() - startedAt.current) / 1000));
    setPhase("done");
    if (document.fullscreenElement) document.exitFullscreen().catch(() => undefined);
    save();
  }, [save]);

  const confirmSubmit = () => {
    if (answeredCount === exam.questions.length) submit();
    else setConfirmOpen(true);
  };

  useEffect(() => {
    if (phase !== "running") return;
    const timer = setInterval(() => {
      setSecondsLeft((s) => {
        const next = s <= 1 ? 0 : s - 1;
        secondsLeftRef.current = next;
        if (s <= 1) submit();
        return next;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [phase, submit]);

  // Tự lưu tiến độ (đáp án + thời gian còn lại) vào exam_attempts mỗi 15s, để
  // lỡ thoát ra/mất mạng/sập máy thì vào lại vẫn khôi phục được, không phải làm lại.
  useEffect(() => {
    if (phase !== "running") return;
    const timer = setInterval(() => {
      void saveExamAttemptProgress(clientTokenRef.current, responsesRef.current, secondsLeftRef.current);
    }, 15000);
    return () => clearInterval(timer);
  }, [phase]);

  // Ghi nhận rời tab / thoát fullscreen lúc đang làm bài — chỉ log + cảnh báo,
  // không tự nộp bài, không chặn thao tác gì khác.
  useEffect(() => {
    if (phase !== "running") return;

    function pushViolation(type: ViolationType, away_ms: number, text: string) {
      violationsRef.current = [
        ...violationsRef.current,
        { type, at: new Date().toISOString(), away_ms },
      ];
      setViolationBanner({ type, text });
    }

    function onVisibilityChange() {
      if (document.hidden) {
        hiddenAtRef.current = Date.now();
        void saveExamAttemptProgress(clientTokenRef.current, responsesRef.current, secondsLeftRef.current);
        return;
      }
      if (hiddenAtRef.current == null) return;
      const away = Date.now() - hiddenAtRef.current;
      hiddenAtRef.current = null;
      const secs = Math.round(away / 1000);
      pushViolation(
        "tab_switch",
        away,
        `Đã ghi nhận em rời khỏi bài thi lúc ${new Date().toLocaleTimeString("vi-VN")} (rời ${secs}s)`,
      );
    }

    function onFullscreenChange() {
      if (document.fullscreenElement) {
        everFullscreenRef.current = true;
        return;
      }
      if (!everFullscreenRef.current) return;
      everFullscreenRef.current = false;
      pushViolation(
        "fullscreen_exit",
        0,
        `Đã ghi nhận em thoát toàn màn hình lúc ${new Date().toLocaleTimeString("vi-VN")}`,
      );
    }

    document.addEventListener("visibilitychange", onVisibilityChange);
    document.addEventListener("fullscreenchange", onFullscreenChange);
    return () => {
      document.removeEventListener("visibilitychange", onVisibilityChange);
      document.removeEventListener("fullscreenchange", onFullscreenChange);
    };
  }, [phase]);

  useEffect(() => {
    if (!violationBanner) return;
    const timer = setTimeout(() => setViolationBanner(null), 8000);
    return () => clearTimeout(timer);
  }, [violationBanner]);

  if (phase === "intro") {
    const fullSeconds = exam.duration_minutes * 60;
    // responses lưu lại có thể lệch số câu nếu đề đã bị sửa từ lúc bắt đầu — bỏ qua cho an toàn.
    const savedResponses =
      resumable?.responses && resumable.responses.length === exam.questions.length ? resumable.responses : null;
    const savedSecondsLeft = resumable ? Math.min(fullSeconds, resumable.secondsLeft ?? fullSeconds) : null;

    function beginExam() {
      if (resumable) {
        clientTokenRef.current = resumable.clientToken;
        if (savedResponses) {
          responsesRef.current = savedResponses;
          setResponses(savedResponses);
        }
      } else if (session) {
        void startExamAttempt(session.user.id, clientTokenRef.current, exam.id, itemId);
      }
      const startSecondsLeft = savedSecondsLeft ?? fullSeconds;
      secondsLeftRef.current = startSecondsLeft;
      setSecondsLeft(startSecondsLeft);
      // Giữ nguyên mốc thời gian đã dùng trước đó — coi như tạm dừng lúc thoát ra.
      startedAt.current = Date.now() - (fullSeconds - startSecondsLeft) * 1000;
      setPhase("running");
      document.documentElement.requestFullscreen().catch(() => undefined);
    }

    return (
      <div className="mx-auto max-w-xl rounded-2xl border border-white/10 bg-panel p-8">
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
        {resumable && (
          <p className="mt-3 rounded-xl border border-amber-400/30 bg-amber-400/10 px-4 py-2.5 text-sm text-amber-200">
            Em có một lượt làm dở còn {formatClock(savedSecondsLeft ?? fullSeconds)} — bấm bên dưới để làm tiếp, không mất bài.
          </p>
        )}
        <Button
          onClick={beginExam}
          className="mt-6 w-full py-3 transition-transform hover:-translate-y-0.5"
        >
          {resumable ? "Làm tiếp bài đang dở" : "Bắt đầu làm bài"}
        </Button>
        <p className="mt-3 text-center text-xs text-slate-500">
          Bài thi chạy toàn màn hình; rời khỏi tab hoặc thoát toàn màn hình sẽ được ghi nhận.
        </p>
      </div>
    );
  }

  if (phase === "running") {
    const q = exam.questions[cur];
    return (
      <div ref={topRef} className="mx-auto max-w-3xl scroll-mt-24">
        <ConfirmDialog
          open={confirmOpen}
          title="Nộp bài luôn?"
          description={`Còn ${exam.questions.length - answeredCount} câu chưa làm.`}
          confirmLabel="Nộp bài"
          cancelLabel="Làm tiếp"
          onConfirm={() => {
            setConfirmOpen(false);
            submit();
          }}
          onCancel={() => setConfirmOpen(false)}
        />
        {violationBanner && (
          <div className="mb-3 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-amber-400/40 bg-amber-400/10 px-4 py-2.5 text-sm text-amber-200">
            <span>{violationBanner.text}</span>
            <div className="flex items-center gap-3">
              {violationBanner.type === "fullscreen_exit" && (
                <button
                  type="button"
                  onClick={() =>
                    document.documentElement.requestFullscreen().catch(() => undefined)
                  }
                  className="rounded-full border border-amber-400/50 px-3 py-1 text-xs font-semibold hover:bg-amber-400/10"
                >
                  Quay lại toàn màn hình
                </button>
              )}
              <button
                type="button"
                onClick={() => setViolationBanner(null)}
                className="text-xs text-amber-300/80 hover:text-amber-200"
              >
                Đóng
              </button>
            </div>
          </div>
        )}
        <div className="sticky top-16 z-40 mb-6 rounded-2xl border border-white/10 bg-panel/95 px-5 py-3 backdrop-blur-md">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <span className="text-sm text-slate-400">
              Câu <span className="font-semibold text-white">{cur + 1}</span>/
              {exam.questions.length} · đã làm{" "}
              <span className="font-semibold text-white">
                {answeredCount}/{exam.questions.length}
              </span>
            </span>
            <span
              className={`font-mono text-lg font-semibold ${
                secondsLeft <= 60 ? "text-red-400" : "text-cyan"
              }`}
            >
              {formatClock(secondsLeft)}
            </span>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => setPaletteOpen((v) => !v)}>
                {paletteOpen ? "Ẩn bảng câu" : "Bảng câu hỏi"}
              </Button>
              <Button size="sm" onClick={confirmSubmit}>
                Nộp bài
              </Button>
            </div>
          </div>

          {paletteOpen && (
            <>
              <div className="mt-3 flex max-h-[30vh] flex-wrap gap-1.5 overflow-y-auto border-t border-white/10 pt-3">
                {exam.questions.map((item, i) => {
                  const state = answerState(item, responses[i]);
                  const flagged = flags.has(i);
                  const cls =
                    state === "done"
                      ? "border-primary bg-primary/25 text-white"
                      : state === "partial"
                        ? "border-primary/50 bg-primary/10 text-slate-200"
                        : "border-white/15 text-slate-400 hover:border-white/30";
                  return (
                    <button
                      key={i}
                      type="button"
                      onClick={() => goTo(i)}
                      title={`Câu ${i + 1}${
                        state === "done"
                          ? " · đã làm"
                          : state === "partial"
                            ? " · làm dở"
                            : " · chưa làm"
                      }${flagged ? " · đánh dấu xem lại" : ""}`}
                      className={`relative h-8 w-8 rounded-lg border text-xs font-bold transition-colors sm:h-9 sm:w-9 ${cls} ${
                        i === cur ? "ring-2 ring-white/70" : ""
                      }`}
                    >
                      {i + 1}
                      {flagged && (
                        <span className="absolute -right-0.5 -top-0.5 h-2 w-2 rounded-full bg-amber-400" />
                      )}
                    </button>
                  );
                })}
              </div>

              <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-slate-500">
                <span className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded border border-primary bg-primary/25" />
                  Đã làm
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded border border-primary/60 bg-[linear-gradient(to_top,rgba(37,99,235,0.55)_50%,transparent_50%)]" />
                  Làm dở
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded border border-white/15" />
                  Chưa làm
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="h-2 w-2 rounded-full bg-amber-400" />
                  Đánh dấu xem lại
                </span>
              </div>
            </>
          )}
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={cur}
            initial={{ opacity: 0, x: reduceMotion ? 0 : 12 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: reduceMotion ? 0 : -12 }}
            transition={{ duration: reduceMotion ? 0 : 0.18, ease: "easeOut" }}
          >
            <QuestionCard
              index={cur + 1}
              question={q}
              response={responses[cur]}
              onChange={(r) => {
                const next = [...responsesRef.current];
                next[cur] = r;
                responsesRef.current = next;
                setResponses(next);
              }}
            />
          </motion.div>
        </AnimatePresence>

        <div className="mt-6 flex flex-wrap items-center gap-2">
          <Button variant="outline" disabled={cur === 0} onClick={() => goTo(cur - 1)}>
            ← Câu trước
          </Button>
          <Button
            variant="outline"
            onClick={() => toggleFlag(cur)}
            className={
              flags.has(cur) ? "border-amber-400/60 bg-amber-400/10 text-amber-300" : ""
            }
          >
            <Flag size={14} />
            {flags.has(cur) ? "Bỏ đánh dấu" : "Đánh dấu xem lại"}
          </Button>
          {cur < lastIndex ? (
            <Button className="ml-auto" onClick={() => goTo(cur + 1)}>
              Câu sau →
            </Button>
          ) : (
            <Button className="ml-auto" onClick={confirmSubmit}>
              Nộp bài
            </Button>
          )}
        </div>
      </div>
    );
  }

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
            <Button variant="outline" size="sm" onClick={save}>
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
      <ExamReviewPager
        questions={exam.questions}
        responses={responses}
        renderAbove={(qi) => {
          const q = exam.questions[qi];
          const g = q.type !== "essay" ? gradeQuestion(q, responses[qi]) : null;
          const wrong = g ? g.earned < g.max : false;
          const topicName = (q.topic ?? "").trim();
          const lessonId = topicName ? lessonByTopic.get(topicName) : undefined;
          const formLabel =
            q.form === "ly_thuyet" || q.form === "bai_tap"
              ? QUESTION_FORM_LABELS[q.form]
              : "";
          const stage = q.form === "ly_thuyet" ? "ly_thuyet" : "bai_tap_mau";
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
              {lessonId && (
                <Link
                  href={`/lop-hoc/bai/?id=${lessonId}#secondary-stage-${stage}`}
                  className="font-semibold text-primary hover:underline"
                >
                  Ôn ngay →
                </Link>
              )}
            </div>
          );
        }}
      />
    </div>
  );
}
