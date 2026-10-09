"use client";

import { dependsOnOtherQuestion, questionKey } from "@/services/question-context";
import { useCallback, useEffect, useMemo, useRef, useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import {
  averageSeconds,
  emptyResponses,
  formatClock,
  gradeExam,
  isAnswered,
  pickRandom,
  totalSeconds,
  type Exam,
  type QuestionResponse,
} from "@/features/exams/types";
import { pendingCount } from "@/lib/offline-queue";
import { markFirstPracticeDone } from "@/lib/pwa-install";
import { fetchExamsFull, savePracticeSession, type PracticePick } from "@/services/lessons";
import {
  hasLabelledQuestions,
  LADDER_MIN_QUESTIONS,
  LADDER_PASS_RATIO,
  nextLadderLevel,
  pickForLevel,
  readLadderLevel,
  writeLadderLevel,
  type LadderLevel,
} from "@/features/lessons/practice-ladder";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import {
  dueQuestionHashes,
  pickKey,
  questionHash,
  readPracticeMode,
  recordSpacing,
  STEP_SECONDS_PER_QUESTION,
  writePracticeMode,
  type PracticeMode,
} from "@/features/lessons/practice-step";
import type { StepItem } from "@/components/lessons/PracticeStepView";
import TaskRpLine from "@/components/rank/TaskRpLine";

// Màn "đang làm" + "sau khi nộp" của 1 phiên luyện tập (PracticeRunningView.tsx,
// PracticeDoneView.tsx) — học sinh KHÔNG thấy 2 màn này lúc mới mở bài học (chỉ hiện sau khi bấm
// "Bắt đầu luyện N câu" ở màn chọn số câu), tách chunk riêng để không nằm trong JS ban đầu của
// /lop-hoc/bai (đợt tối ưu tốc độ lần 4, perf4/RESULT.md). Cả 2 đều kéo theo QuestionCard.
const PracticeRunningViewLazy = dynamic(() => import("@/components/lessons/PracticeRunningView"), {
  ssr: false,
  loading: () => <p className="text-sm text-slate-400">Đang tải câu hỏi…</p>,
});
// Chế độ "Từng câu": cũng chỉ hiện sau khi bấm bắt đầu → chunk riêng + LazyErrorBoundary như 2 màn trên.
const PracticeStepViewLazy = dynamic(() => import("@/components/lessons/PracticeStepView"), {
  ssr: false,
  loading: () => <p className="text-sm text-slate-400">Đang tải câu hỏi…</p>,
});
const PracticeDoneViewLazy = dynamic(() => import("@/components/lessons/PracticeDoneView"), {
  ssr: false,
  loading: () => <p className="text-sm text-slate-400">Đang tính điểm…</p>,
});

// LazyErrorBoundary: chưa nộp bài nên chưa có gì để mất — nếu chunk lỗi (mất mạng, CDN desync
// sau deploy…), fallback chỉ cần mời tải lại trang, không cần trấn an về dữ liệu.
function PracticeRunningView(props: ComponentProps<typeof PracticeRunningViewLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <p className="rounded-2xl border border-white/10 bg-panel p-5 text-sm text-slate-400">
          Không tải được phần làm bài (có thể do mạng chập chờn). Thử tải lại trang.
        </p>
      }
    >
      <PracticeRunningViewLazy {...props} />
    </LazyErrorBoundary>
  );
}

function PracticeStepView(props: ComponentProps<typeof PracticeStepViewLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <p className="rounded-2xl border border-white/10 bg-panel p-5 text-sm text-slate-400">
          Không tải được phần làm bài (có thể do mạng chập chờn). Thử tải lại trang.
        </p>
      }
    >
      <PracticeStepViewLazy {...props} />
    </LazyErrorBoundary>
  );
}

// LazyErrorBoundary: kết quả đã được lưu (save() ở dưới gọi ĐỘC LẬP với việc chunk này tải được
// hay không — submit() gọi setPhase("done") rồi save(...) ngay trong cùng 1 callback, không chờ
// PracticeDoneView mount) — fallback có thể yên tâm báo "kết quả đã lưu".
function PracticeDoneView(props: ComponentProps<typeof PracticeDoneViewLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <p className="rounded-2xl border border-white/10 bg-panel p-5 text-sm text-slate-400">
          Kết quả luyện tập của em đã được lưu, nhưng trang không hiện được phần xem lại (có thể
          do mạng chập chờn). Thử tải lại trang.
        </p>
      }
    >
      <PracticeDoneViewLazy {...props} />
    </LazyErrorBoundary>
  );
}

// "step" = chế độ Từng câu (không đếm giờ, không dùng timer của "running").
type Phase = "setup" | "running" | "step" | "done";

const COUNT_CHOICES = [10, 20, 30, 50];
const DEFAULT_COUNT = 20;

/**
 * Phiên luyện tập: chọn số câu (mặc định 20), hệ thống bốc ngẫu nhiên từ ngân hàng
 * câu hỏi của bài, đếm ngược tổng thời lượng (15″ mỗi câu lý thuyết, 45″ mỗi câu
 * bài tập), có bảng chọn câu để lướt qua câu khó rồi quay lại, nộp bài thì chấm
 * điểm và mở lời giải chi tiết.
 */
export default function PracticeSession({
  examIds,
  poolExamIds,
  lessonId,
  itemId,
  passScore = null,
  color = "#F59E0B",
  onActiveChange,
}: {
  examIds: number[];
  /** Đề chung của bài (kiểm tra/thi/BTVN...) — câu của các đề này cũng vào ngân hàng luyện tập, khử trùng. */
  poolExamIds?: number[];
  lessonId: number | null;
  itemId: number | null;
  /** Điểm đạt thang 10 do giáo viên cấu hình cho mục luyện tập này — null = không đánh giá đạt. */
  passScore?: number | null;
  color?: string;
  /** Báo cho trang bài: phiên đang làm dở (đã bấm Bắt đầu, chưa nộp) — trang hỏi trước khi đổi tab. */
  onActiveChange?: (active: boolean) => void;
}) {
  const { session } = useAuth();
  const [bank, setBank] = useState<PracticePick[]>([]);
  const [bankState, setBankState] = useState<"loading" | "loaded" | "error">("loading");
  const [count, setCount] = useState(DEFAULT_COUNT);
  const [phase, setPhase] = useState<Phase>("setup");
  const [picks, setPicks] = useState<PracticePick[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [flags, setFlags] = useState<Set<number>>(new Set());
  const [cur, setCur] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(0);
  const [usedSeconds, setUsedSeconds] = useState(0);
  const [saveState, setSaveState] = useState<"idle" | "saving" | "saved" | "queued" | "failed">("idle");
  // Thang độ khó: level = mức hiện tại của em ở mục này; free = tắt thang, bốc ngẫu nhiên như cũ.
  const [levelOverride, setLevelOverride] = useState<LadderLevel | null>(null);
  const [free, setFree] = useState(false);
  const [ladderNote, setLadderNote] = useState<string | null>(null);
  // Từng câu (mặc định) hay Cả bài (đồng hồ như cũ) — nhớ lựa chọn theo học sinh, như thang độ khó.
  const [modeOverride, setModeOverride] = useState<PracticeMode | null>(null);

  const startedAt = useRef(0);
  const sessionLevelRef = useRef<LadderLevel | null>(null);
  const submittedRef = useRef(false);
  const responsesRef = useRef<QuestionResponse[]>([]);
  const picksRef = useRef<PracticePick[]>([]);
  const clientTokenRef = useRef<string>("");
  const timedOutRef = useRef(false);

  useEffect(() => {
    const allIds = [...new Set([...examIds, ...(poolExamIds ?? [])])];
    if (!session || allIds.length === 0) return;
    let alive = true;
    void (async () => {
      setBankState("loading");
      try {
        const metas = await fetchExamsFull(allIds);
        if (!alive) return;
        const flat: PracticePick[] = [];
        const seen = new Set<string>();
        for (const id of allIds) {
          const exam = metas.get(id) as Exam | undefined;
          if (!exam) continue;
          exam.questions.forEach((question, qi) => {
            // Câu tự luận không chấm tự động được — để dành cho mục Kiểm tra.
            if (question.type === "essay") return;
            // Câu "tiếp câu trên" mất ngữ cảnh khi bốc ngẫu nhiên — bỏ khỏi ngân hàng luyện tập.
            if (dependsOnOtherQuestion(question)) return;
            const key = questionKey(question);
            if (seen.has(key)) return;
            seen.add(key);
            flat.push({ question, examId: exam.id, sourceIndex: qi });
          });
        }
        setBank(flat);
        setBankState("loaded");
        setCount((c) => Math.min(c, flat.length) || Math.min(DEFAULT_COUNT, flat.length));
      } catch {
        if (alive) setBankState("error");
      }
    })();
    return () => {
      alive = false;
    };
  }, [examIds, poolExamIds, session]);

  const ladderScope = itemId ?? lessonId;
  const studentId = session?.user.id;

  // Đang làm dở = phase running/step. Báo lên trang (đổi tab unmount → mất bài) và chặn đóng/tải lại
  // trang bằng beforeunload. Unmount thì báo false để trang không hỏi oan.
  const practiceActive = phase === "running" || phase === "step";
  useEffect(() => {
    onActiveChange?.(practiceActive);
    if (!practiceActive) return;
    const warn = (e: BeforeUnloadEvent) => {
      e.preventDefault();
    };
    window.addEventListener("beforeunload", warn);
    return () => {
      window.removeEventListener("beforeunload", warn);
      onActiveChange?.(false);
    };
    // onActiveChange là callback inline của trang — chỉ cần chạy lại khi phase đổi.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [practiceActive]);
  // Mức đã lưu đọc ngay khi render (không qua effect); lên mức thì ghi đè trong state + lưu lại.
  const level: LadderLevel = levelOverride ?? (studentId ? readLadderLevel(studentId, ladderScope) : "de");
  // Đọc lựa chọn đã lưu ngay khi render (không qua effect); bấm đổi thì ghi đè và lưu lại.
  const mode: PracticeMode = modeOverride ?? (studentId ? readPracticeMode(studentId) : "step");
  function changeMode(next: PracticeMode) {
    setModeOverride(next);
    if (studentId) writePracticeMode(studentId, next);
  }
  const ladderOn = !free && hasLabelledQuestions(bank);

  const questions = useMemo(() => picks.map((p) => p.question), [picks]);

  const save = useCallback(
    (used: number, timedOut: boolean) => {
      if (!session) return;
      const finalPicks = picksRef.current;
      const finalResponses = responsesRef.current;
      const summary = gradeExam(
        finalPicks.map((p) => p.question),
        finalResponses,
      );
      setSaveState("saving");
      void savePracticeSession({
        studentId: session.user.id,
        lessonId,
        itemId,
        picks: finalPicks,
        responses: finalResponses,
        score10: summary.score10,
        correctCount: summary.correctCount,
        durationSeconds: used,
        timedOut,
        clientToken: clientTokenRef.current,
      }).then((ok) => {
        setSaveState(!ok ? "failed" : pendingCount(session.user.id) > 0 ? "queued" : "saved");
        if (ok) markFirstPracticeDone();
        const played = sessionLevelRef.current;
        if (!ok || !played) return;
        const ratio = summary.max > 0 ? summary.earned / summary.max : 0;
        const next = nextLadderLevel(played, ratio, finalPicks.length);
        if (next.moved) {
          writeLadderLevel(session.user.id, ladderScope, next.level);
          setLevelOverride(next.level);
          setLadderNote(`🎉 Đạt ${Math.round(ratio * 100)}% — em được lên mức ${DIFFICULTY_LABELS[next.level]}!`);
        } else if (next.atTop) {
          setLadderNote(`🏆 Đạt ${Math.round(ratio * 100)}% ở mức cao nhất (Khó) — em đã leo hết thang.`);
        } else if (finalPicks.length < LADDER_MIN_QUESTIONS) {
          setLadderNote(`Phiên dưới ${LADDER_MIN_QUESTIONS} câu chưa tính để lên mức. Mức hiện tại: ${DIFFICULTY_LABELS[played]}.`);
        } else {
          setLadderNote(`Đạt ${Math.round(LADDER_PASS_RATIO * 100)}% mới lên mức tiếp — em ở mức ${DIFFICULTY_LABELS[played]}, luyện thêm một phiên nữa nhé.`);
        }
      });
    },
    [session, lessonId, itemId, ladderScope],
  );

  const submit = useCallback(
    (timedOut = false) => {
      if (submittedRef.current) return;
      submittedRef.current = true;
      const used = Math.round((Date.now() - startedAt.current) / 1000);
      timedOutRef.current = timedOut;
      setUsedSeconds(used);
      setPhase("done");
      save(used, timedOut);
    },
    [save],
  );
  const retry = useCallback(() => save(usedSeconds, timedOutRef.current), [save, usedSeconds]);

  useEffect(() => {
    if (phase !== "running") return;
    const timer = setInterval(() => {
      setSecondsLeft((s) => {
        if (s <= 1) {
          submit(true);
          return 0;
        }
        return s - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [phase, submit]);

  function start() {
    if (bank.length === 0) return;
    let chosen: PracticePick[];
    if (mode === "step") {
      // Giãn cách: ưu tiên (tối đa ~40% phiên) các câu em từng làm sai đã tới hạn ôn (2 ngày → 1 tuần → 1 tháng).
      const due = studentId ? dueQuestionHashes(studentId, Date.now()) : new Set<string>();
      const dueBank = bank.filter((p) => due.has(questionHash(p.question)));
      const duePicked = pickRandom(dueBank, Math.min(dueBank.length, Math.max(1, Math.ceil(count * 0.4))));
      const dueKeys = new Set(duePicked.map(pickKey));
      const restBank = bank.filter((p) => !dueKeys.has(pickKey(p)));
      const need = Math.max(0, count - duePicked.length);
      const rest = ladderOn ? pickForLevel(restBank, level, need) : pickRandom(restBank, need);
      chosen = pickRandom([...duePicked, ...rest], duePicked.length + rest.length);
    } else {
      chosen = ladderOn ? pickForLevel(bank, level, count) : pickRandom(bank, count);
    }
    sessionLevelRef.current = ladderOn ? level : null;
    setLadderNote(null);
    const blanks = emptyResponses(chosen.map((p) => p.question));
    picksRef.current = chosen;
    responsesRef.current = blanks;
    submittedRef.current = false;
    clientTokenRef.current = crypto.randomUUID();
    startedAt.current = Date.now();
    setPicks(chosen);
    setResponses(blanks);
    setFlags(new Set());
    setCur(0);
    setSecondsLeft(totalSeconds(chosen.map((p) => p.question)));
    setSaveState("idle");
    setPhase(mode === "step" ? "step" : "running");
  }

  // Hết phiên Từng câu: lưu ĐÚNG/SAI LẦN ĐẦU của mọi câu đã hiện (kể cả câu tương tự) như phiên thường —
  // practice_question_results, mastery, danh hiệu, thang độ khó chạy y như cũ; câu làm lại cuối phiên không tính.
  function finishStep(items: StepItem[]) {
    if (items.length === 0 || submittedRef.current) return;
    const finalPicks = items.map((i) => i.pick);
    const finalResponses = items.map((i) => i.response);
    picksRef.current = finalPicks;
    responsesRef.current = finalResponses;
    setPicks(finalPicks);
    setResponses(finalResponses);
    if (studentId) {
      recordSpacing(
        studentId,
        items.map((i) => ({ hash: questionHash(i.pick.question), correct: i.correct })),
        Date.now(),
      );
    }
    submit(false);
  }

  function answer(r: QuestionResponse) {
    const next = [...responsesRef.current];
    next[cur] = r;
    responsesRef.current = next;
    setResponses(next);
  }

  function toggleFlag(idx: number) {
    setFlags((current) => {
      const next = new Set(current);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }

  const answeredCount = questions.filter((q, i) => isAnswered(q, responses[i])).length;

  function confirmSubmit() {
    const left = questions.length - answeredCount;
    if (left === 0 || confirm(`Còn ${left} câu chưa làm. Nộp bài luôn?`)) submit(false);
  }

  // ---------- Màn hình mở phiên ----------
  if (phase === "setup") {
    if (examIds.length === 0 && !(poolExamIds?.length))
      return <p className="text-sm text-slate-400">Mục này chưa được gắn đề.</p>;
    if (!session)
      return (
        <p className="text-sm text-slate-400">
          <Link href="/dang-nhap" className="font-semibold text-slate-200 underline underline-offset-2">
            Đăng nhập
          </Link>{" "}
          để xem ngân hàng câu hỏi và luyện tập.
        </p>
      );
    if (bankState === "loading") return <p className="text-sm text-slate-400">Đang tải ngân hàng câu hỏi…</p>;
    if (bankState === "error")
      return <p className="text-sm text-slate-400">Không tải được ngân hàng câu hỏi. Thử tải lại trang.</p>;
    if (bank.length === 0)
      return (
        <p className="text-sm text-slate-400">
          Đề đã gắn chưa có câu trắc nghiệm/đúng–sai để luyện tập tự động.
        </p>
      );

    const choices = [...new Set([...COUNT_CHOICES.filter((c) => c < bank.length), bank.length])];

    const minutesFor = (n: number) =>
      mode === "step"
        ? Math.max(1, Math.round((n * STEP_SECONDS_PER_QUESTION) / 60))
        : Math.max(1, Math.round((n * averageSeconds(bank.map((p) => p.question))) / 60));

    return (
      <div className="mx-auto max-w-xl space-y-5 rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
        {/* RP nói trước khi làm (thầy chốt 9/10/2026): một dòng, không huy hiệu (L3) — ngay đầu để em biết lượt này có "giá" gì rồi mới chọn. */}
        <div className="rounded-xl border border-white/10 bg-white/5 px-3 py-2.5">
          <p className="text-sm font-semibold text-slate-400">Điểm xếp hạng (RP)</p>
          <div className="mt-0.5">
            <TaskRpLine kind="practice_item" sourceId={itemId} />
          </div>
        </div>

        <fieldset>
          <legend className="text-base font-bold text-white">1. Em muốn luyện kiểu nào?</legend>
          <div role="radiogroup" aria-label="Cách luyện" className="mt-2 grid gap-2 sm:grid-cols-2">
            {(
              [
                { id: "step", label: "Từng câu", hint: "Biết đúng/sai ngay. Câu sai làm lại cuối phiên. Không đếm giờ." },
                { id: "whole", label: "Cả bài", hint: "Làm hết rồi nộp, có đồng hồ đếm ngược." },
              ] as const
            ).map((m) => (
              <button
                key={m.id}
                type="button"
                role="radio"
                aria-checked={mode === m.id}
                onClick={() => changeMode(m.id)}
                className={`flex min-h-14 items-start gap-3 rounded-xl border-2 px-3 py-2.5 text-left transition-colors ${
                  mode === m.id ? "" : "border-white/15 hover:border-slate-400"
                }`}
                style={mode === m.id ? { borderColor: color, backgroundColor: `${color}33` } : undefined}
              >
                <span
                  aria-hidden
                  className="mt-1 h-4 w-4 shrink-0 rounded-full border-2"
                  style={
                    mode === m.id
                      ? { borderColor: color, background: `radial-gradient(${color} 45%, transparent 50%)` }
                      : { borderColor: "#94A3B8" }
                  }
                />
                <span>
                  <span className="block text-base font-bold text-white">
                    {m.label}
                  </span>
                  <span className="mt-0.5 block text-sm leading-snug text-slate-400">{m.hint}</span>
                </span>
              </button>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="text-base font-bold text-white">2. Bao nhiêu câu?</legend>
          <p className="mt-0.5 text-sm text-slate-400">
            Ngân hàng có {bank.length} câu, mỗi lần bốc ngẫu nhiên một khác.
          </p>
          <div role="radiogroup" aria-label="Số câu" className="mt-2 grid grid-cols-3 gap-2">
            {choices.map((c) => (
              <button
                key={c}
                type="button"
                role="radio"
                aria-checked={count === c}
                onClick={() => setCount(c)}
                className={`min-h-14 rounded-xl border-2 px-2 py-2 text-center transition-colors ${
                  count === c ? "" : "border-white/15 hover:border-slate-400"
                }`}
                style={count === c ? { borderColor: color, backgroundColor: `${color}33` } : undefined}
              >
                <span className="block text-base font-bold text-white">
                  {c === bank.length ? `Tất cả ${c}` : c} câu
                </span>
                <span className="block text-sm text-slate-400">~{minutesFor(c)} phút</span>
              </button>
            ))}
          </div>
        </fieldset>

        {hasLabelledQuestions(bank) && (
          <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1 border-t border-white/10 pt-3 text-sm text-slate-300">
            {ladderOn ? (
              <p>
                Mức của em: <span className="font-bold text-white">{DIFFICULTY_LABELS[level]}</span>
                {" "}· đạt {Math.round(LADDER_PASS_RATIO * 100)}% thì lên mức.
              </p>
            ) : (
              <p>Luyện tự do: câu ngẫu nhiên mọi mức.</p>
            )}
            <button
              type="button"
              onClick={() => setFree((f) => !f)}
              className="min-h-11 text-sm font-semibold text-slate-300 underline underline-offset-2 hover:text-white"
            >
              {ladderOn ? "Luyện tự do" : "Luyện theo mức"}
            </button>
          </div>
        )}

        <button
          type="button"
          onClick={start}
          className="min-h-12 w-full rounded-full px-6 text-base font-bold text-white"
          style={{ backgroundColor: color }}
        >
          Bắt đầu luyện {count} câu
        </button>
      </div>
    );
  }

  // ---------- Đang làm ----------
  if (phase === "running") {
    return (
      <PracticeRunningView
        questions={questions}
        responses={responses}
        cur={cur}
        flags={flags}
        secondsLeft={secondsLeft}
        color={color}
        onAnswer={answer}
        onSetCur={setCur}
        onToggleFlag={toggleFlag}
        onConfirmSubmit={confirmSubmit}
      />
    );
  }

  // ---------- Đang làm: Từng câu ----------
  if (phase === "step") {
    return (
      <PracticeStepView
        initialPicks={picks}
        bank={bank}
        color={color}
        onFinish={finishStep}
        onQuit={() => setPhase("setup")}
      />
    );
  }

  // ---------- Đã nộp ----------
  return (
    <PracticeDoneView
      questions={questions}
      responses={responses}
      usedSeconds={usedSeconds}
      saveState={saveState}
      passScore={passScore}
      ladderNote={ladderNote}
      onRetry={retry}
      onNewSession={() => setPhase("setup")}
      color={color}
    />
  );
}
