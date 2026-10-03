"use client";

import { useCallback, useEffect, useRef, useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import { Flag } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import QuestionSlide from "@/components/exams/QuestionSlide";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type { Exam, ExamQuestion, QuestionResponse } from "@/features/exams/types";
import {
  buildQuestionResults,
  emptyResponses,
  gradeExam,
  groupQuestionIndexesByType,
  isAnswered,
  QUESTION_TYPE_LABELS,
  questionTopicNames,
} from "@/features/exams/types";
import {
  finishExamAttempt,
  findExistingExamResultId,
  findOpenExamAttempt,
  saveExamAttemptProgress,
  startExamAttempt,
  type OpenExamAttempt,
} from "@/services/progress";
import { getSupabase } from "@/services/supabase";

// Màn hình sau khi nộp bài (điểm + xem lại từng câu, components/exams/ExamDoneView.tsx) kéo theo
// ExamResultSummary + ExamReviewPager — học sinh KHÔNG thấy màn này lúc mới vào trang (chỉ hiện
// sau khi bấm "Nộp bài"), tách chunk riêng để không nằm trong JS ban đầu của /kiem-tra/lam (đợt
// tối ưu tốc độ lần 4, perf4/RESULT.md). loading hiện dòng chữ ngắn thay vì null — tránh cảm giác
// "bấm nộp bài không có phản hồi gì" trong lúc chờ chunk tải (thường < 1 lần, cache 1 năm sau đó).
const ExamDoneViewLazy = dynamic(() => import("@/components/exams/ExamDoneView"), {
  ssr: false,
  loading: () => <p className="text-center text-slate-400">Đang tính điểm…</p>,
});

// LazyErrorBoundary: điểm đã được lưu (save() ở dưới gọi ĐỘC LẬP với việc chunk này tải được hay
// không — submit() gọi setPhase("done") rồi save() ngay trong cùng 1 callback, không chờ
// ExamDoneView mount) — nên nếu chunk lỗi (mất mạng, hoặc site vừa deploy bản mới xoá chunk cũ),
// fallback có thể yên tâm báo "điểm đã lưu" thay vì làm học sinh tưởng mất bài. app/error.tsx là
// lưới cuối nếu vì lý do gì đó boundary này không bắt được (xem components/ui/LazyErrorBoundary.tsx).
function ExamDoneView(props: ComponentProps<typeof ExamDoneViewLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div className="mx-auto max-w-xl rounded-2xl border border-white/10 bg-panel p-6 text-center">
          <p className="text-sm text-slate-300">
            Điểm của em đã được lưu, nhưng trang không hiện được phần xem lại bài làm (có thể do
            mạng chập chờn). Thử tải lại trang.
          </p>
          <Button variant="outline" size="sm" className="mt-3" onClick={() => window.location.reload()}>
            Tải lại trang
          </Button>
        </div>
      }
    >
      <ExamDoneViewLazy {...props} />
    </LazyErrorBoundary>
  );
}

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
  theoryLessonId = null,
}: {
  exam: Exam;
  /** Mục bài học đang gắn đề này (nếu có) — dùng để ghi nhận exam_attempts. */
  itemId?: number | null;
  /** Chỉ có khi đây là quiz kiểm tra nhanh cuối lý thuyết: số câu đúng tối thiểu để đạt. */
  minCorrect?: number | null;
  /** Chỉ có khi đây là quiz kiểm tra nhanh cuối lý thuyết: bài học SỞ HỮU mục lý thuyết đó —
   *  dùng để "Ôn ngay" nhảy đúng đoạn (q.theorySection) thay vì tra theo topic chung chung. */
  theoryLessonId?: number | null;
}) {
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
  const [cur, setCur] = useState(0);
  const [flags, setFlags] = useState<Set<number>>(new Set());
  const [paletteOpen, setPaletteOpen] = useState(false);
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
  const lastSavedResponsesRef = useRef<QuestionResponse[] | null>(null);
  const lastSavedAtRef = useRef(0);
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

  // Tự lưu tiến độ (đáp án + thời gian còn lại) vào exam_attempts, để lỡ thoát ra/mất
  // mạng/sập máy thì vào lại vẫn khôi phục được, không phải làm lại.
  // Tiết kiệm log Supabase (28/9/2026): kiểm mỗi 30s nhưng chỉ ghi khi đáp án có đổi so với
  // lần ghi trước; ngoài ra cứ tối đa 2 phút ghi một lần dù không đổi để đồng hồ còn lại
  // (seconds_left) không lệch quá 2 phút khi khôi phục. Trước đây ghi vô điều kiện mỗi 15s.
  const flushProgress = useCallback((force: boolean) => {
    const dirty = responsesRef.current !== lastSavedResponsesRef.current;
    const stale = Date.now() - lastSavedAtRef.current >= 120_000;
    if (!force && !dirty && !stale) return;
    lastSavedResponsesRef.current = responsesRef.current;
    lastSavedAtRef.current = Date.now();
    void saveExamAttemptProgress(clientTokenRef.current, responsesRef.current, secondsLeftRef.current);
  }, []);

  useEffect(() => {
    if (phase !== "running") return;
    lastSavedResponsesRef.current = responsesRef.current;
    lastSavedAtRef.current = Date.now();
    const timer = setInterval(() => flushProgress(false), 30_000);
    return () => clearInterval(timer);
  }, [phase, flushProgress]);

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
        flushProgress(true);
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
  }, [phase, flushProgress]);

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
        <p className="mt-3 text-center text-[13px] text-slate-400">
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
          <div role="alert" className="fixed inset-x-3 top-20 z-50 mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-3 rounded-xl border border-amber-400/40 bg-[#2a2210] px-4 py-2.5 text-sm text-amber-200 shadow-lg">
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
        <div className="sticky top-16 z-40 mb-6 rounded-2xl border border-white/10 bg-panel/95 px-4 py-2 backdrop-blur-md">
          <div className="flex items-center justify-between gap-3">
            <span className="text-sm text-slate-400">
              Câu <span className="font-semibold text-white">{cur + 1}</span>/{exam.questions.length}
              <span className="ml-2 hidden sm:inline">· đã làm {answeredCount}</span>
            </span>
            <span
              className={`font-mono text-lg font-semibold ${
                secondsLeft <= 60 ? "text-red-400" : "text-cyan"
              }`}
            >
              {formatClock(secondsLeft)}
            </span>
            <Button
              variant="outline"
              size="sm"
              className="min-h-11"
              aria-expanded={paletteOpen}
              onClick={() => setPaletteOpen((v) => !v)}
            >
              {paletteOpen ? "Đóng" : `Bảng câu · ${answeredCount}/${exam.questions.length}`}
            </Button>
          </div>

          {paletteOpen && (
            <>
              <div className="mt-3 max-h-[30vh] space-y-2 overflow-y-auto border-t border-white/10 pt-3">
                {groupQuestionIndexesByType(exam.questions).map((section) => (
                  <div key={section.type}>
                    <div className="mb-1 text-[13px] font-semibold uppercase tracking-wide text-slate-400">
                      {QUESTION_TYPE_LABELS[section.type]} · {section.indices.length} câu
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {section.indices.map((i) => {
                        const item = exam.questions[i];
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
                            className={`relative h-11 w-11 rounded-lg border text-sm font-bold transition-colors ${cls} ${
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
                  </div>
                ))}
              </div>

              <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-[13px] text-slate-400">
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
              <Button variant="outline" size="sm" className="mt-3 min-h-11 w-full" onClick={confirmSubmit}>
                Nộp bài
              </Button>
            </>
          )}
        </div>

        <QuestionSlide slideKey={cur}>
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
        </QuestionSlide>

        <div className="mt-6 flex items-center gap-2">
          <Button variant="outline" className="min-h-11" disabled={cur === 0} onClick={() => goTo(cur - 1)}>
            ← Trước
          </Button>
          <Button
            variant="outline"
            onClick={() => toggleFlag(cur)}
            className={`min-h-11 ${
              flags.has(cur) ? "border-amber-400/60 bg-amber-400/10 text-amber-300" : ""
            }`}
          >
            <Flag size={14} />
            {flags.has(cur) ? "Bỏ dấu" : "Đánh dấu"}
          </Button>
          {cur < lastIndex ? (
            <Button className="ml-auto min-h-11" onClick={() => goTo(cur + 1)}>
              Sau →
            </Button>
          ) : (
            <Button className="ml-auto min-h-11" onClick={confirmSubmit}>
              Nộp bài
            </Button>
          )}
        </div>
      </div>
    );
  }

  return (
    <ExamDoneView
      exam={exam}
      responses={responses}
      itemId={itemId}
      minCorrect={minCorrect}
      theoryLessonId={theoryLessonId}
      usedSeconds={usedSeconds}
      saveState={saveState}
      onRetry={save}
    />
  );
}
