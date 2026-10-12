"use client";

import { useEffect, useMemo, useState } from "react";
import { X } from "lucide-react";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeQuestion, isAnswered, pickRandom } from "@/features/exams/types";
import { fetchBankQuestions, toExamQuestion, type BankQuestion } from "@/services/question-bank";
import { fetchTopicFamilyIds } from "@/services/tutoring";
import {
  DIAGNOSTIC_QUESTIONS_PER_TOPIC,
  DIAGNOSTIC_STOP_AFTER_WRONG,
  submitDiagnostic,
  type DiagnosticTopicResult,
} from "@/services/diagnostic";

type Phase = "loading" | "empty" | "intro" | "running" | "done";

interface Item {
  topicId: number;
  question: ExamQuestion;
}

/** 3 câu mỗi bài: ưu tiên 2 dễ + 1 trung bình (câu khó không dùng để chẩn đoán), thiếu mức nào bù từ mức còn lại. */
function pickForTopic(pool: BankQuestion[]): BankQuestion[] {
  const ok = pool.filter((q) => q.qtype !== "essay" && q.difficulty !== "kho");
  const easy = pickRandom(ok.filter((q) => q.difficulty === "de"), 2);
  const mid = pickRandom(ok.filter((q) => q.difficulty !== "de"), DIAGNOSTIC_QUESTIONS_PER_TOPIC - easy.length);
  const picked = [...easy, ...mid];
  if (picked.length < DIAGNOSTIC_QUESTIONS_PER_TOPIC) {
    const taken = new Set(picked.map((q) => q.id));
    picked.push(...pickRandom(ok.filter((q) => !taken.has(q.id)), DIAGNOSTIC_QUESTIONS_PER_TOPIC - picked.length));
  }
  return picked;
}

/**
 * Kiểm tra đầu vào cho em vào lớp trễ: không tính điểm, không xếp hạng, không hiện đúng/sai từng câu.
 * Bài nào sai 2 câu thì dừng bài đó (không bắt làm hết, N2/C-tải nhận thức). Kết quả gửi lên diagnostic_submit,
 * DB tự mở mục phụ đạo và báo phụ huynh.
 */
export default function EntryDiagnosticQuiz({
  studentId,
  topicIds,
  topicNames,
  onClose,
  onSubmitted,
}: {
  studentId: string;
  topicIds: number[];
  topicNames: Map<number, string>;
  onClose: () => void;
  onSubmitted: () => void;
}) {
  const toast = useToast();
  const [phase, setPhase] = useState<Phase>("loading");
  const [items, setItems] = useState<Item[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [cur, setCur] = useState(0);
  const [tally, setTally] = useState<Map<number, { correct: number; total: number }>>(new Map());
  const [submitting, setSubmitting] = useState(false);
  const [needCount, setNeedCount] = useState(0);

  useEffect(() => {
    let cancelled = false;
    Promise.all(
      topicIds.map(async (topicId) => {
        const family = await fetchTopicFamilyIds(topicId);
        const pool = await fetchBankQuestions({ topicIds: family, includeArchived: false });
        return pickForTopic(pool).map((b) => ({ topicId, question: toExamQuestion(b) }));
      }),
    )
      .then((groups) => {
        if (cancelled) return;
        const all = groups.flat();
        setItems(all);
        setResponses(emptyResponses(all.map((i) => i.question)));
        setPhase(all.length === 0 ? "empty" : "intro");
      })
      .catch(() => {
        if (!cancelled) setPhase("empty");
      });
    return () => {
      cancelled = true;
    };
  }, [topicIds]);

  const topicCount = useMemo(() => new Set(items.map((i) => i.topicId)).size, [items]);

  async function finish(finalTally: Map<number, { correct: number; total: number }>) {
    setSubmitting(true);
    try {
      const results: DiagnosticTopicResult[] = [...finalTally.entries()]
        .filter(([, v]) => v.total > 0)
        .map(([topicId, v]) => ({ topicId, correct: v.correct, total: v.total }));
      setNeedCount(await submitDiagnostic(studentId, results));
      setPhase("done");
      onSubmitted();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa nộp được, thử lại nhé.");
    } finally {
      setSubmitting(false);
    }
  }

  /** Chấm câu hiện tại, bỏ qua các câu còn lại của bài đã sai đủ, sang câu kế hoặc nộp. */
  function next() {
    const item = items[cur];
    const g = gradeQuestion(item.question, responses[cur]);
    const ok = g.max > 0 && g.earned === g.max;
    const t = new Map(tally);
    const prev = t.get(item.topicId) ?? { correct: 0, total: 0 };
    t.set(item.topicId, { correct: prev.correct + (ok ? 1 : 0), total: prev.total + 1 });
    setTally(t);
    let n = cur + 1;
    while (n < items.length) {
      const s = t.get(items[n].topicId);
      if (s && s.total - s.correct >= DIAGNOSTIC_STOP_AFTER_WRONG) n += 1;
      else break;
    }
    if (n >= items.length) void finish(t);
    else setCur(n);
  }

  function setResponse(r: QuestionResponse) {
    setResponses((prev) => {
      const nextR = [...prev];
      nextR[cur] = r;
      return nextR;
    });
  }

  const wide = phase === "running";
  const isLast = cur === items.length - 1;

  return (
    <div
      className="fixed inset-0 z-100 flex items-center justify-center bg-black/60 px-4 py-6 backdrop-blur-sm"
      onClick={phase === "running" ? undefined : onClose}
      role="presentation"
    >
      <div
        className={`max-h-[90vh] w-full overflow-y-auto rounded-2xl border border-line bg-panel p-5 shadow-2xl sm:p-6 ${
          wide ? "max-w-2xl" : "max-w-sm"
        }`}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="mb-3 flex items-start justify-between gap-3">
          <h2 className="font-display text-lg font-semibold text-ink">Kiểm tra đầu vào</h2>
          <button type="button" onClick={onClose} aria-label="Đóng" className="min-h-11 min-w-11 text-muted hover:text-primary">
            <X size={18} />
          </button>
        </div>

        {phase === "loading" && <p className="text-sm text-muted">Đang soạn câu hỏi…</p>}

        {phase === "empty" && (
          <div className="space-y-4">
            <p className="text-sm text-ink">Ngân hàng câu hỏi chưa có câu nào cho các bài này. Em nhờ trợ giảng giúp nhé.</p>
            <Button variant="outline" onClick={onClose} className="w-full">
              Đóng
            </Button>
          </div>
        )}

        {phase === "intro" && (
          <div className="space-y-4">
            <p className="text-sm text-ink">
              {topicCount} bài lớp đã học trước khi em vào · khoảng {Math.max(5, Math.round(items.length * 0.7))} phút.
            </p>
            <p className="text-sm text-ink">
              Không tính điểm, không xếp hạng. Bài này để thầy cô biết nên kèm em phần nào. Câu nào chưa biết em cứ chọn
              theo cảm nhận, sai nhiều ở một bài thì hệ thống tự chuyển sang bài khác.
            </p>
            <Button onClick={() => setPhase("running")} className="w-full">
              Bắt đầu
            </Button>
          </div>
        )}

        {phase === "running" && items[cur] && (
          <div className="space-y-4">
            <p className="text-sm font-semibold text-ink">{topicNames.get(items[cur].topicId) ?? "Bài đã học"}</p>
            <QuestionCard
              key={cur}
              index={cur + 1}
              question={items[cur].question}
              response={responses[cur]}
              onChange={setResponse}
            />
            <Button
              onClick={next}
              disabled={submitting || !isAnswered(items[cur].question, responses[cur])}
              className="w-full"
            >
              {submitting ? "Đang nộp…" : isLast ? "Nộp bài" : "Câu tiếp"}
            </Button>
          </div>
        )}

        {phase === "done" && (
          <div className="space-y-4">
            <p className="text-sm text-ink">
              {needCount === 0
                ? "Xong rồi! Nền tảng của em ổn, chưa có phần nào cần phụ đạo gấp."
                : `Xong rồi! Có ${needCount} bài cần củng cố — em xem ở khối "Phụ đạo" ngay trên trang chủ, đăng ký buổi hoặc tự kiểm tra nhé.`}
            </p>
            <p className="text-xs text-slate-500">Kết quả đã được gửi cho phụ huynh và trợ giảng.</p>
            <Button onClick={onClose} className="w-full">
              Đóng
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
