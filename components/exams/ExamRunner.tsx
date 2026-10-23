"use client";

import { useCallback, useEffect, useRef, useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import { CheckCircle2, CircleAlert, Flag } from "lucide-react";
import Html from "@/components/exams/ContentHtml";
import { allDistractorHints, distractorHints } from "@/features/lessons/practice-step";
import LateNightNudge from "@/components/rank/LateNightNudge";
import { useAuth } from "@/components/auth/AuthProvider";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import QuestionSlide from "@/components/exams/QuestionSlide";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type {
  ExamForTaking,
  ExamQuestionPublic,
  ExamSubmitResult,
  PracticeAnswerCheck,
  QuestionResponse,
} from "@/features/exams/types";
import {
  emptyResponses,
  gradeQuestion,
  groupQuestionIndexesByType,
  isAnswered,
  isFullExam,
  QUESTION_TYPE_LABELS,
} from "@/features/exams/types";
import {
  findOpenExamAttempt,
  saveExamAttemptProgress,
  startExamAttempt,
  type OpenExamAttempt,
} from "@/services/progress";
import { checkPracticeAnswer, submitExamAttempt, toFullExam } from "@/services/exam-server";
import { fetchStartRpNotice, invalidateMyRankCache, type StartRpNotice } from "@/services/rank";

// Màn hình sau khi nộp bài (điểm + xem lại từng câu, components/exams/ExamDoneView.tsx) kéo theo
// ExamResultSummary + ExamReviewPager — học sinh KHÔNG thấy màn này lúc mới vào trang (chỉ hiện
// sau khi bấm "Nộp bài"), tách chunk riêng để không nằm trong JS ban đầu của /kiem-tra/lam (đợt
// tối ưu tốc độ lần 4, perf4/RESULT.md). loading hiện dòng chữ ngắn thay vì null — tránh cảm giác
// "bấm nộp bài không có phản hồi gì" trong lúc chờ chunk tải (thường < 1 lần, cache 1 năm sau đó).
const ExamDoneViewLazy = dynamic(() => import("@/components/exams/ExamDoneView"), {
  ssr: false,
  loading: () => <p className="text-center text-muted">Đang tính điểm…</p>,
});

// LazyErrorBoundary: điểm đã được server lưu (màn này chỉ mount SAU khi submit_exam_attempt trả kết quả)
// — nên nếu chunk lỗi (mất mạng, hoặc site vừa deploy bản mới xoá chunk cũ),
// fallback có thể yên tâm báo "điểm đã lưu" thay vì làm học sinh tưởng mất bài. app/error.tsx là
// lưới cuối nếu vì lý do gì đó boundary này không bắt được (xem components/ui/LazyErrorBoundary.tsx).
function ExamDoneView(props: ComponentProps<typeof ExamDoneViewLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div className="mx-auto max-w-xl rounded-2xl border border-line bg-panel p-6 text-center">
          <p className="text-sm text-ink">
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

function answerState(q: ExamQuestionPublic, r: QuestionResponse): AnswerState {
  if (q.type === "true_false") {
    const picks = Array.isArray(r) ? r : [];
    const statements = q.statements ?? [];
    const filled = statements.filter((_, i) => picks[i] != null).length;
    if (filled === 0) return "empty";
    return filled === statements.length ? "done" : "partial";
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
  teacherView = false,
}: {
  /** Đề đã lược đáp án (get_exam_for_taking). Staff nhận đề đầy đủ (exam.full) để xem đáp án / làm thử. */
  exam: ExamForTaking;
  /** Mục bài học đang gắn đề này (nếu có) — dùng để ghi nhận exam_attempts. */
  itemId?: number | null;
  /** Chỉ có khi đây là quiz kiểm tra nhanh cuối lý thuyết: số câu đúng tối thiểu để đạt. */
  minCorrect?: number | null;
  /** Chỉ có khi đây là quiz kiểm tra nhanh cuối lý thuyết: bài học SỞ HỮU mục lý thuyết đó —
   *  dùng để "Ôn ngay" nhảy đúng đoạn (q.theorySection) thay vì tra theo topic chung chung. */
  theoryLessonId?: number | null;
  /** Giáo viên xem đáp án. "Làm thử" vẫn ở trong bộ nhớ: không tạo lượt, không lưu nháp, không ghi điểm. */
  teacherView?: boolean;
}) {
  const { session, profile } = useAuth();
  const [phase, setPhase] = useState<Phase>("intro");
  const [tryMode, setTryMode] = useState(false);
  // Rời chế độ giáo viên giữa chừng (bật "Xem như học sinh") thì bỏ phiên làm thử,
  // kẻo đồng hồ/nộp bài của phiên đó bắt đầu ghi xuống DB.
  if (!teacherView && tryMode) {
    setTryMode(false);
    if (phase !== "intro") setPhase("intro");
  }
  const memoryOnly = teacherView || tryMode;
  const [rpNotice, setRpNotice] = useState<StartRpNotice | null>(null);
  useEffect(() => {
    if (!session || memoryOnly) return;
    let alive = true;
    fetchStartRpNotice(exam.id, itemId).then((n) => alive && setRpNotice(n)).catch(() => {});
    return () => { alive = false; };
  }, [session, exam.id, itemId, memoryOnly]);
  const [responses, setResponses] = useState<QuestionResponse[]>(() =>
    emptyResponses(exam.questions),
  );
  const [secondsLeft, setSecondsLeft] = useState(exam.duration_minutes * 60);
  const [saveState, setSaveState] = useState<
    "idle" | "saving" | "saved" | "failed"
  >("idle");
  const [usedSeconds, setUsedSeconds] = useState(0);
  // Kết quả server chấm (điểm + đề đủ đáp án/lời giải). Chưa có thì màn "done" chỉ hiện trạng thái chờ —
  // KHÔNG chấm tạm ở máy học sinh (thầy chốt 24/10/2026: đáp án không bao giờ nằm ở trình duyệt khi chưa nộp).
  const [result, setResult] = useState<ExamSubmitResult | null>(null);
  const durationRef = useRef(0);
  const submittingRef = useRef(false);
  const [cur, setCur] = useState(0);
  const [flags, setFlags] = useState<Set<number>>(new Set());
  // Kiểm tra nhanh cuối lý thuyết: bấm "Kiểm tra" là biết đúng/sai câu đó ngay (L1), câu đã kiểm thì khoá đáp án
  // nên điểm vẫn là lần chọn đầu. Đề thường (Luyện tập/Kiểm tra) không đổi: có điểm sau khi nộp.
  const instant = theoryLessonId != null;
  const [checked, setChecked] = useState<Map<number, PracticeAnswerCheck>>(new Map());
  const [checkBusy, setCheckBusy] = useState(false);
  const [checkError, setCheckError] = useState("");
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
  const secondsLeftRef = useRef(secondsLeft);

  // Bài đang làm dở của học sinh này cho đúng đề này (nếu có) — dò 1 lần khi vào
  // màn hình giới thiệu, undefined = đang dò, null = không có.
  const [resumable, setResumable] = useState<OpenExamAttempt | null | undefined>(undefined);
  useEffect(() => {
    if (!session || phase !== "intro" || memoryOnly) return;
    let cancelled = false;
    findOpenExamAttempt(session.user.id, exam.id).then((a) => {
      if (!cancelled) setResumable(a);
    });
    return () => {
      cancelled = true;
    };
  }, [session, exam.id, phase, memoryOnly]);

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

  // Tự lưu tiến độ (đáp án + thời gian còn lại) vào exam_attempts, để lỡ thoát ra/mất
  // mạng/sập máy thì vào lại vẫn khôi phục được, không phải làm lại.
  // Tiết kiệm log Supabase (28/9/2026): kiểm mỗi 30s nhưng chỉ ghi khi đáp án có đổi so với
  // lần ghi trước; ngoài ra cứ tối đa 2 phút ghi một lần dù không đổi để đồng hồ còn lại
  // (seconds_left) không lệch quá 2 phút khi khôi phục. Trước đây ghi vô điều kiện mỗi 15s.
  const flushProgress = useCallback((force: boolean) => {
    if (memoryOnly) return;
    const dirty = responsesRef.current !== lastSavedResponsesRef.current;
    const stale = Date.now() - lastSavedAtRef.current >= 120_000;
    if (!force && !dirty && !stale) return;
    lastSavedResponsesRef.current = responsesRef.current;
    lastSavedAtRef.current = Date.now();
    void saveExamAttemptProgress(clientTokenRef.current, responsesRef.current, secondsLeftRef.current);
  }, [memoryOnly]);

  // Nộp bài: server chấm + ghi (RPC submit_exam_attempt). Idempotent theo client_token nên "Thử lại" sau lỗi
  // mạng không tạo thêm lượt làm. Mất mạng thì CHỜ: giữ bài ở màn này (responses vẫn trong bộ nhớ + exam_attempts
  // tự lưu nháp), chưa có điểm/đáp án tới khi server trả lời.
  const save = useCallback(() => {
    if (!session || memoryOnly || submittingRef.current) return;
    submittingRef.current = true;
    setSaveState("saving");
    submitExamAttempt({
      examId: exam.id,
      clientToken: clientTokenRef.current,
      responses: responsesRef.current,
      durationSeconds: durationRef.current,
      violations: violationsRef.current,
    })
      .then((r) => {
        invalidateMyRankCache();
        setResult(r);
        setSaveState("saved");
      })
      .catch(() => setSaveState("failed"))
      .finally(() => {
        submittingRef.current = false;
      });
  }, [exam.id, session, memoryOnly]);

  // submit được gọi từ nút bấm và từ interval hết giờ — chuyển màn hình 1 lần rồi lưu
  const submit = useCallback(() => {
    if (submittedRef.current) return;
    submittedRef.current = true;
    durationRef.current = Math.round((Date.now() - startedAt.current) / 1000);
    setUsedSeconds(durationRef.current);
    setPhase("done");
    // Lưu nháp lần cuối để lỡ mất mạng/đóng trang thì vào lại vẫn khôi phục được bài.
    flushProgress(true);
    if (document.fullscreenElement) document.exitFullscreen().catch(() => undefined);
    save();
  }, [save, flushProgress]);

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

  // Bấm "Kiểm tra" (quiz cuối lý thuyết): hỏi server chấm 1 câu. Làm thử của giáo viên (đề đầy đủ, không
  // ghi gì) chấm ngay ở máy vì giáo viên vốn đã xem được đáp án.
  async function runCheck(idx: number) {
    if (checkBusy) return;
    const resp = responsesRef.current[idx];
    setCheckError("");
    setCheckBusy(true);
    try {
      let res: PracticeAnswerCheck;
      if (memoryOnly && isFullExam(exam)) {
        const full = exam.questions[idx];
        const g = gradeQuestion(full, resp);
        res = {
          exam_id: exam.id,
          question_index: idx,
          earned: g.earned,
          max: g.max,
          is_correct: g.max > 0 && g.earned === g.max,
          question: full,
        };
      } else {
        res = await checkPracticeAnswer(exam.id, idx, resp);
      }
      setChecked((prev) => new Map(prev).set(idx, res));
    } catch {
      setCheckError("Chưa kiểm tra được câu này — kiểm tra mạng rồi bấm Kiểm tra lại. Đáp án của em vẫn được giữ.");
    } finally {
      setCheckBusy(false);
    }
  }

  if (teacherView && !isFullExam(exam)) {
    return (
      <p className="text-center text-muted">
        Em chưa có quyền xem đáp án của đề này (chỉ đề của lớp mình trợ giảng hoặc đề đã gửi xem trước).
      </p>
    );
  }

  if (teacherView && !tryMode && isFullExam(exam)) {
    const blanks = emptyResponses(exam.questions);
    return (
      <div className="mx-auto max-w-3xl">
        <h1 className="font-display text-2xl font-bold text-ink">{exam.title}</h1>
        <p className="mt-2 text-sm text-muted">
          {exam.questions.length} câu · đáp án và lời giải
        </p>
        <Button variant="outline" className="mt-4 min-h-11" onClick={() => setTryMode(true)}>
          Làm thử
        </Button>
        <div className="mt-6 space-y-6">
          {groupQuestionIndexesByType(exam.questions).map((section) => (
            <section key={section.type}>
              <h2 className="mb-3 text-sm font-semibold text-muted">
                {QUESTION_TYPE_LABELS[section.type]}
              </h2>
              <div className="space-y-4">
                {section.indices.map((i) => (
                  <QuestionCard
                    key={i}
                    index={i + 1}
                    question={exam.questions[i]}
                    response={blanks[i]}
                    review
                    selfCheck
                  />
                ))}
              </div>
            </section>
          ))}
        </div>
      </div>
    );
  }

  if (phase === "intro") {
    const fullSeconds = exam.duration_minutes * 60;
    // responses lưu lại có thể lệch số câu nếu đề đã bị sửa từ lúc bắt đầu — bỏ qua cho an toàn.
    const savedResponses =
      resumable?.responses && resumable.responses.length === exam.questions.length ? resumable.responses : null;
    const savedSecondsLeft = resumable ? Math.min(fullSeconds, resumable.secondsLeft ?? fullSeconds) : null;

    function beginExam() {
      if (resumable && !memoryOnly) {
        clientTokenRef.current = resumable.clientToken;
        if (savedResponses) {
          responsesRef.current = savedResponses;
          setResponses(savedResponses);
        }
      } else if (session && !memoryOnly) {
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
      <div className="mx-auto max-w-xl rounded-2xl border border-line bg-panel p-8">
        <h1 className="font-display text-2xl font-bold text-ink">
          {exam.title}
        </h1>
        <p className="mt-3 text-sm text-muted">
          {exam.questions.length} câu · {exam.duration_minutes} phút ·{" "}
          {instant ? "bấm Kiểm tra là biết đúng/sai từng câu, kèm lời giải" : "nộp bài là có điểm ngay kèm lời giải"}
        </p>
        {memoryOnly && (
          <p className="mt-2 text-sm text-muted">
            Làm thử trên máy này — không tạo lượt làm, không ghi điểm.
          </p>
        )}
        <p className="mt-2 text-sm text-muted">
          Học sinh:{" "}
          <span className="font-semibold text-ink">
            {profile?.full_name}
          </span>
          {profile?.class_name && ` · Lớp ${profile.class_name}`}
        </p>
        <LateNightNudge className="mt-4 text-left" />
        {rpNotice && (
          <p
            className={`mt-3 rounded-xl border px-4 py-2.5 text-sm ${
              rpNotice.counts ? "border-line bg-bg text-ink" : "border-line bg-bg text-muted"
            }`}
          >
            {!rpNotice.counts
              ? "Bài này không tính RP — làm để luyện tập."
              : rpNotice.earned >= rpNotice.maxRp
                ? `Em đã nhận đủ ${rpNotice.maxRp} RP từ bài này. Làm lại vẫn để ôn tập, nhưng không cộng thêm RP.`
                : rpNotice.earned > 0
                  ? `Bài này tính RP (tối đa ${rpNotice.maxRp}). Em đã nhận ${rpNotice.earned} RP — làm lại đạt điểm cao hơn sẽ được cộng phần chênh lệch.`
                  : `Bài này tính RP (tối đa ${rpNotice.maxRp}, theo điểm em đạt). Làm lại đạt điểm cao hơn sẽ được cộng phần chênh lệch.`}
          </p>
        )}
        {resumable && (
          <p className="mt-3 rounded-xl border border-amber-400/30 bg-amber-400/10 px-4 py-2.5 text-sm text-amber-200">
            Em có một lượt làm dở còn {formatClock(savedSecondsLeft ?? fullSeconds)} — bấm bên dưới để làm tiếp, không mất bài.
          </p>
        )}
        <Button
          onClick={beginExam}
          className="mt-6 w-full py-3 transition-transform hover:-translate-y-0.5"
        >
          {resumable && !memoryOnly ? "Làm tiếp bài đang dở" : "Bắt đầu làm bài"}
        </Button>
        {memoryOnly && (
          <button
            type="button"
            onClick={() => setTryMode(false)}
            className="mt-2 min-h-11 w-full text-sm font-semibold text-primary"
          >
            Xem đáp án
          </button>
        )}
        <p className="mt-3 text-center text-[13px] text-muted">
          Bài thi chạy toàn màn hình; rời khỏi tab hoặc thoát toàn màn hình sẽ được ghi nhận.
        </p>
      </div>
    );
  }

  if (phase === "running") {
    const q = exam.questions[cur];
    // Câu đã Kiểm tra: server (check_practice_answer) trả đúng/sai + câu ĐỦ đáp án/lời giải của riêng câu đó.
    const check = instant ? checked.get(cur) : undefined;
    const isChecked = check !== undefined;
    const curCorrect = check?.is_correct === true;
    // Giáo viên/trợ giảng làm thử: thấy lý do của MỌI phương án sai, không chỉ phương án mình chọn.
    const curHints = check ? (teacherView ? allDistractorHints(check.question) : distractorHints(check.question, responses[cur])) : [];
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
          <div role="alert" className="fixed inset-x-3 top-20 z-50 mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-3 rounded-xl border border-amber-400/40 bg-surface-2 px-4 py-2.5 text-sm text-amber-200 shadow-lg">
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
        <div className="sticky top-16 z-40 mb-6 rounded-2xl border border-line bg-panel/95 px-4 py-2 backdrop-blur-md">
          <div className="flex items-center justify-between gap-3">
            <span className="text-sm text-muted">
              Câu <span className="font-semibold text-ink">{cur + 1}</span>/{exam.questions.length}
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
              <div className="mt-3 max-h-[30vh] space-y-2 overflow-y-auto border-t border-line pt-3">
                {groupQuestionIndexesByType(exam.questions).map((section) => (
                  <div key={section.type}>
                    <div className="mb-1 text-[13px] font-semibold uppercase tracking-wide text-muted">
                      {QUESTION_TYPE_LABELS[section.type]} · {section.indices.length} câu
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {section.indices.map((i) => {
                        const item = exam.questions[i];
                        const state = answerState(item, responses[i]);
                        const flagged = flags.has(i);
                        const cls =
                          state === "done"
                            ? "border-primary bg-primary/25 text-ink"
                            : state === "partial"
                              ? "border-primary/50 bg-primary/10 text-ink"
                              : "border-line text-muted hover:border-line-strong";
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
                              i === cur ? "ring-2 ring-primary" : ""
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

              <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-[13px] text-muted">
                <span className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded border border-primary bg-primary/25" />
                  Đã làm
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded border border-primary/60 bg-primary/10" />
                  Làm dở
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded border border-line-strong" />
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

        <div className="exam-paper">
        <QuestionSlide slideKey={cur}>
          <QuestionCard
            index={cur + 1}
            question={check ? check.question : q}
            response={responses[cur]}
            review={isChecked}
            onChange={
              isChecked
                ? undefined
                : (r) => {
                    const next = [...responsesRef.current];
                    next[cur] = r;
                    responsesRef.current = next;
                    setResponses(next);
                  }
            }
          />
        </QuestionSlide>
        </div>

        {checkError && !isChecked && (
          <p role="alert" className="mt-4 rounded-xl border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-base text-amber-100">
            {checkError}
          </p>
        )}

        {isChecked && (
          <div className="mt-4 space-y-3" role="status" aria-live="polite">
            {curCorrect ? (
              <p className="flex items-start gap-2 rounded-xl border border-emerald-500/40 bg-emerald-500/10 px-3 py-2 text-base text-emerald-100">
                <CheckCircle2 size={20} className="mt-0.5 shrink-0 text-emerald-300" aria-hidden />
                <span>Đúng rồi.</span>
              </p>
            ) : (
              <p className="flex items-start gap-2 rounded-xl border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-base text-amber-100">
                <CircleAlert size={20} className="mt-0.5 shrink-0 text-amber-300" aria-hidden />
                <span>Chưa đúng. Đáp án và lời giải ở phía trên.</span>
              </p>
            )}
            {curHints.length > 0 && (
              <ul className="space-y-2 border-l-2 border-amber-400/60 pl-3 text-base leading-relaxed text-ink">
                {curHints.map((h) => (
                  <li key={h.label}>
                    <b>Vì sao em chọn {h.label} chưa đúng:</b> <Html html={h.note} />
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {/* mb-28: chừa chỗ để cuộn thanh nút lên khỏi nút Báo lỗi nổi + banner giả lập (D2/D3) */}
        <div className="exam-nav-row mb-28 mt-6 flex items-center gap-2">
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
          {instant && !isChecked ? (
            <Button
              className="ml-auto min-h-11"
              disabled={checkBusy || !isAnswered(q, responses[cur])}
              onClick={() => void runCheck(cur)}
            >
              {checkBusy ? "Đang kiểm tra…" : "Kiểm tra"}
            </Button>
          ) : cur < lastIndex ? (
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

  // Làm thử của giáo viên: đề đã đầy đủ đáp án, chấm tại máy (không ghi gì).
  if (memoryOnly && isFullExam(exam)) {
    return (
      <ExamDoneView
        exam={toFullExam(exam, exam.questions)}
        responses={responses}
        itemId={itemId}
        minCorrect={minCorrect}
        theoryLessonId={theoryLessonId}
        usedSeconds={usedSeconds}
        saveState="idle"
        onRetry={save}
        memoryOnly
        onBackToAnswers={() => { setTryMode(false); setPhase("intro"); }}
      />
    );
  }

  // Chưa có kết quả từ server: giữ bài, báo rõ, cho thử lại. Không hiện điểm/đáp án tự tính.
  if (!result) {
    return (
      <div className="mx-auto max-w-xl rounded-2xl border border-line bg-panel p-6 text-center" role="status" aria-live="polite">
        {saveState === "failed" ? (
          <>
            <p className="text-base font-semibold text-ink">Chưa nộp được bài lên hệ thống.</p>
            <p className="mt-2 text-sm text-muted">
              Bài làm của em vẫn được giữ trên trang này. Kiểm tra mạng rồi bấm Thử lại — đừng tắt hay tải lại trang. Điểm và
              đáp án sẽ hiện ngay khi hệ thống chấm xong.
            </p>
            <Button className="mt-4 min-h-11" onClick={save}>
              Thử lại
            </Button>
          </>
        ) : (
          <p className="text-base text-ink">Đang nộp bài và chấm điểm…</p>
        )}
      </div>
    );
  }

  return (
    <ExamDoneView
      exam={toFullExam(exam, result.questions)}
      responses={responses}
      itemId={itemId}
      minCorrect={minCorrect}
      theoryLessonId={theoryLessonId}
      usedSeconds={usedSeconds}
      saveState="saved"
      onRetry={save}
      serverSummary={{ score10: result.score10, correctCount: result.correct_count }}
    />
  );
}
