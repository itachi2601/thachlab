"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { Flag } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import QuestionCard from "@/components/exams/QuestionCard";
import {
  averageSeconds,
  emptyResponses,
  formatClock,
  gradeExam,
  gradeQuestion,
  isAnswered,
  pickRandom,
  questionSeconds,
  totalSeconds,
  type Exam,
  type QuestionResponse,
} from "@/features/exams/types";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import { derivePracticeStatus } from "@/features/progress/types";
import { fetchExamsFull, savePracticeSession, type PracticePick } from "@/services/lessons";

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

  const startedAt = useRef(0);
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
      }).then((ok) => setSaveState(ok ? "saved" : "failed"));
    },
    [session, lessonId, itemId],
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
    const chosen = pickRandom(bank, count);
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
          — mỗi câu lý thuyết 15 giây, mỗi câu bài tập 45 giây.
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
    const q = questions[cur];
    return (
      <div className="space-y-4 rounded-2xl border border-white/10 bg-panel p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="text-sm text-slate-400">
            Câu <span className="font-semibold text-white">{cur + 1}</span>/{questions.length} ·
            đã làm{" "}
            <span className="font-semibold text-white">
              {answeredCount}/{questions.length}
            </span>
          </span>
          <span
            className={`font-mono text-lg font-semibold ${
              secondsLeft <= 30 ? "text-red-400" : "text-cyan"
            }`}
          >
            {formatClock(secondsLeft)}
          </span>
          <button
            type="button"
            onClick={confirmSubmit}
            className="rounded-full px-4 py-1.5 text-sm font-bold text-white"
            style={{ backgroundColor: color }}
          >
            Nộp bài
          </button>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {questions.map((item, i) => {
            const done = isAnswered(item, responses[i]);
            const flagged = flags.has(i);
            return (
              <button
                key={i}
                type="button"
                onClick={() => setCur(i)}
                title={`Câu ${i + 1}${flagged ? " · đã đánh dấu" : ""}`}
                className={`h-9 w-9 rounded-lg border text-xs font-bold transition-colors ${
                  i === cur ? "ring-2 ring-white/70" : ""
                }`}
                style={{
                  borderColor: flagged ? "#FBBF24" : done ? color : "rgba(255,255,255,0.12)",
                  backgroundColor: done ? `${color}33` : "transparent",
                  color: done ? "#FFFFFF" : flagged ? "#FBBF24" : "#94A3B8",
                }}
              >
                {i + 1}
              </button>
            );
          })}
        </div>

        <QuestionCard
          index={cur + 1}
          question={q}
          response={responses[cur]}
          onChange={answer}
        />

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            disabled={cur === 0}
            onClick={() => setCur((i) => Math.max(0, i - 1))}
            className="rounded-xl border border-white/15 px-4 py-2 text-sm text-slate-300 hover:border-white/30 disabled:opacity-40"
          >
            ← Câu trước
          </button>
          <button
            type="button"
            onClick={() => toggleFlag(cur)}
            className={`inline-flex items-center gap-1.5 rounded-xl border px-4 py-2 text-sm font-semibold ${
              flags.has(cur)
                ? "border-amber-400/60 bg-amber-400/10 text-amber-300"
                : "border-white/15 text-slate-300 hover:border-white/30"
            }`}
          >
            <Flag size={14} />
            {flags.has(cur) ? "Bỏ đánh dấu" : "Đánh dấu xem lại"}
          </button>
          {cur < questions.length - 1 ? (
            <button
              type="button"
              onClick={() => setCur((i) => Math.min(questions.length - 1, i + 1))}
              className="rounded-xl px-4 py-2 text-sm font-bold text-white"
              style={{ backgroundColor: color }}
            >
              Câu sau →
            </button>
          ) : (
            <button
              type="button"
              onClick={confirmSubmit}
              className="rounded-xl px-4 py-2 text-sm font-bold text-white"
              style={{ backgroundColor: color }}
            >
              Nộp bài
            </button>
          )}
          <span className="text-xs text-slate-500">
            Câu này {questionSeconds(q)} giây trong tổng thời lượng
          </span>
        </div>
      </div>
    );
  }

  // ---------- Đã nộp ----------
  const summary = gradeExam(questions, responses);
  const practiceStatus =
    saveState === "saved"
      ? derivePracticeStatus({ sessionCount: 1, bestScore10: summary.score10, passScore })
      : null;
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-white/10 bg-panel p-6 text-center">
        <p className="font-display text-4xl font-bold text-gradient">
          {summary.score10.toLocaleString("vi-VN")}
        </p>
        <p className="mt-2 text-sm text-slate-300">
          Đúng trọn vẹn {summary.correctCount}/{questions.length} câu · {formatClock(usedSeconds)}
        </p>
        {practiceStatus && passScore !== null && (
          <p
            className={`mt-2 inline-block rounded-full border px-3 py-1 text-xs font-bold ${
              practiceStatus.status === "passed"
                ? "border-emerald-500/40 bg-emerald-500/15 text-emerald-300"
                : "border-red-500/40 bg-red-500/15 text-red-300"
            }`}
          >
            {practiceStatus.label}
          </p>
        )}
        <p className="mt-2 text-xs text-slate-500">
          {saveState === "saving" && "Đang lưu…"}
          {saveState === "saved" && "✓ Đã ghi lại để thầy biết em cần ôn phần nào"}
          {saveState === "idle" && "Điểm luyện tập không tính vào bảng điểm"}
        </p>
        {saveState === "failed" && (
          <p className="mt-2 flex flex-col items-center gap-2 text-xs text-red-300">
            <span>Chưa lưu được kết quả luyện tập — kiểm tra mạng rồi thử lại.</span>
            <button
              type="button"
              onClick={retry}
              className="rounded-full border border-white/15 px-4 py-1.5 text-xs font-semibold text-white hover:border-white/30"
            >
              Thử lại
            </button>
          </p>
        )}
        <button
          type="button"
          onClick={() => setPhase("setup")}
          className="mt-4 rounded-full px-5 py-2 text-sm font-bold text-white"
          style={{ backgroundColor: color }}
        >
          Luyện phiên mới
        </button>
      </div>

      <ol className="space-y-4">
        {questions.map((q, i) => {
          const g = gradeQuestion(q, responses[i]);
          const wrong = g.earned < g.max;
          const topicName = (q.topic ?? "").trim();
          const formLabel =
            q.form === "ly_thuyet" || q.form === "bai_tap" ? QUESTION_FORM_LABELS[q.form] : "";
          return (
            <li key={i}>
              {wrong && (topicName || formLabel) && (
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
                </div>
              )}
              <QuestionCard index={i + 1} question={q} response={responses[i]} review />
            </li>
          );
        })}
      </ol>
    </div>
  );
}
