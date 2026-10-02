"use client";

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

// Màn "đang làm" + "sau khi nộp" của 1 phiên luyện tập (PracticeRunningView.tsx,
// PracticeDoneView.tsx) — học sinh KHÔNG thấy 2 màn này lúc mới mở bài học (chỉ hiện sau khi bấm
// "Bắt đầu luyện N câu" ở màn chọn số câu), tách chunk riêng để không nằm trong JS ban đầu của
// /lop-hoc/bai (đợt tối ưu tốc độ lần 4, perf4/RESULT.md). Cả 2 đều kéo theo QuestionCard.
const PracticeRunningViewLazy = dynamic(() => import("@/components/lessons/PracticeRunningView"), {
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

type Phase = "setup" | "running" | "done";

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
  lessonId,
  itemId,
  passScore = null,
  color = "#F59E0B",
}: {
  examIds: number[];
  lessonId: number | null;
  itemId: number | null;
  /** Điểm đạt thang 10 do giáo viên cấu hình cho mục luyện tập này — null = không đánh giá đạt. */
  passScore?: number | null;
  color?: string;
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
  const [saveState, setSaveState] = useState<"idle" | "saving" | "saved" | "failed">("idle");
  // Thang độ khó: level = mức hiện tại của em ở mục này; free = tắt thang, bốc ngẫu nhiên như cũ.
  const [level, setLevel] = useState<LadderLevel>("de");
  const [free, setFree] = useState(false);
  const [ladderNote, setLadderNote] = useState<string | null>(null);

  const startedAt = useRef(0);
  const sessionLevelRef = useRef<LadderLevel | null>(null);
  const submittedRef = useRef(false);
  const responsesRef = useRef<QuestionResponse[]>([]);
  const picksRef = useRef<PracticePick[]>([]);
  const clientTokenRef = useRef<string>("");
  const timedOutRef = useRef(false);

  useEffect(() => {
    if (!session || examIds.length === 0) return;
    let alive = true;
    void (async () => {
      setBankState("loading");
      try {
        const metas = await fetchExamsFull(examIds);
        if (!alive) return;
        const flat: PracticePick[] = [];
        for (const id of examIds) {
          const exam = metas.get(id) as Exam | undefined;
          if (!exam) continue;
          exam.questions.forEach((question, qi) => {
            // Câu tự luận không chấm tự động được — để dành cho mục Kiểm tra.
            if (question.type === "essay") return;
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
  }, [examIds, session]);

  const ladderScope = itemId ?? lessonId;
  const studentId = session?.user.id;
  useEffect(() => {
    if (studentId) setLevel(readLadderLevel(studentId, ladderScope));
  }, [studentId, ladderScope]);
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
        setSaveState(ok ? "saved" : "failed");
        const played = sessionLevelRef.current;
        if (!ok || !played) return;
        const ratio = summary.max > 0 ? summary.earned / summary.max : 0;
        const next = nextLadderLevel(played, ratio, finalPicks.length);
        if (next.moved) {
          writeLadderLevel(session.user.id, ladderScope, next.level);
          setLevel(next.level);
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
    const chosen = ladderOn ? pickForLevel(bank, level, count) : pickRandom(bank, count);
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
    setPhase("running");
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
    if (examIds.length === 0)
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
    const estimate = Math.round(count * averageSeconds(bank.map((p) => p.question)));

    return (
      <div className="space-y-4 rounded-2xl border border-white/10 bg-panel p-5">
        <p className="text-sm text-slate-300">
          Ngân hàng của bài này có{" "}
          <span className="font-bold text-white">{bank.length} câu</span>. Chọn số câu
          muốn luyện — hệ thống bốc ngẫu nhiên mỗi lần một khác.
        </p>
        {hasLabelledQuestions(bank) && (
          <div className="rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-slate-300">
            {ladderOn ? (
              <p>
                Mức hiện tại của em:{" "}
                <span className="font-bold" style={{ color }}>
                  {DIFFICULTY_LABELS[level]}
                </span>{" "}
                (Dễ → Trung bình → Khó). Đạt {Math.round(LADDER_PASS_RATIO * 100)}% trở lên thì lên mức tiếp.
              </p>
            ) : (
              <p>Đang luyện tự do — câu bốc ngẫu nhiên mọi mức, không tính lên mức.</p>
            )}
            <button
              type="button"
              onClick={() => setFree((f) => !f)}
              className="mt-1 text-xs font-semibold text-slate-400 underline underline-offset-2 hover:text-slate-200"
            >
              {ladderOn ? "Luyện tự do (bỏ thang mức)" : "Quay lại luyện theo mức"}
            </button>
          </div>
        )}
        <div className="flex flex-wrap gap-2">
          {choices.map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => setCount(c)}
              className="rounded-xl border px-4 py-2 text-sm font-semibold transition-colors"
              style={
                count === c
                  ? { borderColor: color, backgroundColor: `${color}26`, color }
                  : { borderColor: "rgba(255,255,255,0.1)", color: "#94A3B8" }
              }
            >
              {c === bank.length ? `Tất cả ${c} câu` : `${c} câu`}
            </button>
          ))}
        </div>
        <p className="text-sm text-slate-400">
          Thời lượng ước tính{" "}
          <span className="font-mono font-semibold text-white">{formatClock(estimate)}</span>{" "}
          — mỗi câu lý thuyết 30 giây, mỗi câu bài tập 1 phút 30 giây.
        </p>
        <button
          type="button"
          onClick={start}
          className="rounded-full px-6 py-2.5 text-sm font-bold text-white"
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
