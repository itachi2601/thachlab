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
  buildStartMap,
  CONFIDENCE_LABEL,
  DIAGNOSTIC_MAX_PROBES,
  DIAGNOSTIC_PROBE_QUESTIONS,
  DIAGNOSTIC_QUESTIONS_PER_TOPIC,
  DIAGNOSTIC_STOP_AFTER_WRONG,
  LEVEL_LABEL,
  levelOf,
  submitDiagnostic,
  type DiagnosticConfidence,
  type DiagnosticSubmitResult,
  type DiagnosticTopicResult,
} from "@/services/diagnostic";

type Phase = "loading" | "empty" | "intro" | "running" | "done";

interface Item {
  topicId: number;
  question: ExamQuestion;
  /** Bài lùi về dò tiền đề (2 câu dễ). */
  probe?: boolean;
}

interface Tally {
  correct: number;
  total: number;
  answers: { ok: boolean; conf: DiagnosticConfidence }[];
}

const CONFIDENCE_ORDER: DiagnosticConfidence[] = ["chac", "hoi", "doan"];

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

/** Bài dò tiền đề: chỉ câu dễ (thiếu thì bù câu trung bình), không câu khó. */
function pickForProbe(pool: BankQuestion[]): BankQuestion[] {
  const ok = pool.filter((q) => q.qtype !== "essay" && q.difficulty !== "kho");
  const easy = pickRandom(ok.filter((q) => q.difficulty === "de"), DIAGNOSTIC_PROBE_QUESTIONS);
  if (easy.length >= DIAGNOSTIC_PROBE_QUESTIONS) return easy;
  const taken = new Set(easy.map((q) => q.id));
  return [...easy, ...pickRandom(ok.filter((q) => !taken.has(q.id)), DIAGNOSTIC_PROBE_QUESTIONS - easy.length)];
}

/**
 * Kiểm tra đầu vào cho em vào lớp trễ: không tính điểm, không xếp hạng, không hiện đúng/sai từng câu.
 * Bài nào sai 2 câu thì dừng bài đó (không bắt làm hết, N2/C-tải nhận thức). Mỗi câu em chọn thêm độ chắc (3 mức)
 * để DB phân nhóm vững / cần ôn / hiểu chưa đúng / chưa biết. Bài chính hổng thì lùi về bài cũ kế tiếp dò tiền đề
 * (2 câu dễ, tối đa DIAGNOSTIC_MAX_PROBES bài). Kết quả gửi lên diagnostic_submit, DB tự mở mục phụ đạo.
 */
export default function EntryDiagnosticQuiz({
  studentId,
  topicIds,
  reserveIds = [],
  topicNames,
  onClose,
  onSubmitted,
}: {
  studentId: string;
  topicIds: number[];
  /** Bài cũ hơn nằm sau topicIds, dùng để dò tiền đề (theo thứ tự gần → xa). */
  reserveIds?: number[];
  topicNames: Map<number, string>;
  onClose: () => void;
  onSubmitted: () => void;
}) {
  const toast = useToast();
  const [phase, setPhase] = useState<Phase>("loading");
  const [items, setItems] = useState<Item[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [cur, setCur] = useState(0);
  const [confs, setConfs] = useState<(DiagnosticConfidence | null)[]>([]);
  const [tally, setTally] = useState<Map<number, Tally>>(new Map());
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<DiagnosticSubmitResult | null>(null);
  const [probesUsed, setProbesUsed] = useState(0);
  const order = useMemo(() => [...topicIds, ...reserveIds], [topicIds, reserveIds]);

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
        setConfs(all.map(() => null));
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

  async function finish(finalTally: Map<number, Tally>) {
    setSubmitting(true);
    try {
      const results: DiagnosticTopicResult[] = [...finalTally.entries()]
        .filter(([, v]) => v.total > 0)
        .map(([topicId, v]) => ({
          topicId,
          correct: v.correct,
          total: v.total,
          seq: order.indexOf(topicId),
          probe: !topicIds.includes(topicId),
          answers: v.answers,
        }));
      setResult(await submitDiagnostic(studentId, results));
      setPhase("done");
      onSubmitted();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa nộp được, thử lại nhé.");
    } finally {
      setSubmitting(false);
    }
  }

  /** Bài hổng (sai 2 câu, hoặc sai mà chắc) thì dò bài cũ kế tiếp bằng 2 câu dễ; trả các câu mới hoặc rỗng. */
  async function probeFor(topicId: number, t: Map<number, Tally>, list: Item[], used: number): Promise<Item[]> {
    const s = t.get(topicId);
    if (!s || used >= DIAGNOSTIC_MAX_PROBES || !topicIds.includes(topicId)) return [];
    const weak = s.total - s.correct >= DIAGNOSTIC_STOP_AFTER_WRONG || s.answers.some((a) => !a.ok && a.conf === "chac");
    if (!weak) return [];
    const olderId = order[order.indexOf(topicId) + 1];
    if (olderId == null || t.has(olderId) || list.some((i) => i.topicId === olderId)) return [];
    try {
      const pool = await fetchBankQuestions({ topicIds: await fetchTopicFamilyIds(olderId), includeArchived: false });
      return pickForProbe(pool).map((b) => ({ topicId: olderId, question: toExamQuestion(b), probe: true }));
    } catch {
      return [];
    }
  }

  /** Chấm câu hiện tại, dò tiền đề nếu bài vừa xong là bài hổng, bỏ qua câu còn lại của bài đã sai đủ, sang câu kế hoặc nộp. */
  async function next() {
    const conf = confs[cur];
    if (!conf) return;
    const item = items[cur];
    const g = gradeQuestion(item.question, responses[cur]);
    const ok = g.max > 0 && g.earned === g.max;
    const t = new Map(tally);
    const prev = t.get(item.topicId) ?? { correct: 0, total: 0, answers: [] };
    t.set(item.topicId, {
      correct: prev.correct + (ok ? 1 : 0),
      total: prev.total + 1,
      answers: [...prev.answers, { ok, conf }],
    });
    setTally(t);

    let list = items;
    const done = (id: number) => {
      const s = t.get(id);
      return !!s && s.total - s.correct >= DIAGNOSTIC_STOP_AFTER_WRONG;
    };
    const lastOfTopic = !items.slice(cur + 1).some((i) => i.topicId === item.topicId);
    if (!item.probe && (lastOfTopic || done(item.topicId))) {
      setSubmitting(true);
      const extra = await probeFor(item.topicId, t, items, probesUsed);
      setSubmitting(false);
      if (extra.length > 0) {
        list = [...items, ...extra];
        setItems(list);
        setResponses((r) => [...r, ...emptyResponses(extra.map((i) => i.question))]);
        setConfs((c) => [...c, ...extra.map(() => null)]);
        setProbesUsed((n) => n + 1);
      }
    }

    let n = cur + 1;
    while (n < list.length && done(list[n].topicId)) n += 1;
    if (n >= list.length) void finish(t);
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
              Không tính điểm, không xếp hạng. Bài này để thầy cô biết em đã vững gì (khỏi học lại) và nên kèm phần nào.
              Sau mỗi câu em chọn mức chắc chắn: chọn thật nhé, “đoán” cũng được. Sai nhiều ở một bài thì hệ thống tự chuyển bài.
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
            {isAnswered(items[cur].question, responses[cur]) && (
              <fieldset className="space-y-2">
                <legend className="text-sm font-semibold text-ink">Em chắc đến đâu về câu này?</legend>
                <div className="grid grid-cols-3 gap-2">
                  {CONFIDENCE_ORDER.map((c) => (
                    <button
                      key={c}
                      type="button"
                      aria-pressed={confs[cur] === c}
                      onClick={() => setConfs((prev) => prev.map((v, i) => (i === cur ? c : v)))}
                      className={`min-h-11 rounded-xl border px-2 text-sm font-semibold ${
                        confs[cur] === c ? "border-primary bg-primary/10 text-primary" : "border-line text-ink hover:bg-primary/5"
                      }`}
                    >
                      {CONFIDENCE_LABEL[c]}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-muted">Chọn “Em đoán” cũng không sao, thầy cô cần biết thật để kèm đúng chỗ.</p>
              </fieldset>
            )}
            <Button
              onClick={() => void next()}
              disabled={submitting || !isAnswered(items[cur].question, responses[cur]) || !confs[cur]}
              className="w-full"
            >
              {submitting ? "Đang xử lý…" : isLast ? "Nộp bài" : "Câu tiếp"}
            </Button>
          </div>
        )}

        {phase === "done" && result && <DoneSummary result={result} topicNames={topicNames} onClose={onClose} />}
      </div>
    </div>
  );
}

/** Màn kết quả cho em: nói cái em đã vững trước, rồi mới nói bắt đầu từ đâu (N1/C2: không mở đầu bằng chỗ hổng). */
function DoneSummary({
  result,
  topicNames,
  onClose,
}: {
  result: DiagnosticSubmitResult;
  topicNames: Map<number, string>;
  onClose: () => void;
}) {
  const { skip, order } = buildStartMap(result.perTopic);
  const name = (id: number) => topicNames.get(id) ?? "Bài đã học";
  const first = order[0];
  return (
    <div className="space-y-4">
      {skip.length > 0 ? (
        <div className="space-y-1.5">
          <p className="text-sm font-semibold text-ink">Em đã vững {skip.length} bài, phần này không phải học lại:</p>
          <ul className="space-y-1">
            {skip.map((r) => (
              <li key={r.topicId} className="text-sm text-ink">
                ✅ {name(r.topicId)}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p className="text-sm text-ink">Cảm ơn em đã làm bài thật. Nhờ vậy thầy cô biết bắt đầu kèm em từ đâu.</p>
      )}
      {first ? (
        <div className="space-y-1.5 rounded-xl border border-line bg-primary/5 p-3">
          <p className="text-sm text-ink">
            Mình bắt đầu từ: <span className="font-semibold">{name(first.topicId)}</span>
          </p>
          {order.length > 1 && (
            <p className="text-xs text-muted">
              Sau đó: {order.slice(1, 4).map((r) => `${name(r.topicId)} (${LEVEL_LABEL[levelOf(r)]})`).join(" · ")}
            </p>
          )}
          <p className="text-xs text-muted">Em xem khối “Phụ đạo” trên trang chủ để đăng ký buổi hoặc tự kiểm tra nhé.</p>
        </div>
      ) : (
        <p className="text-sm text-ink">Nền tảng của em ổn, chưa có phần nào cần phụ đạo gấp.</p>
      )}
      <p className="text-xs text-muted">Kết quả đã được gửi cho phụ huynh và trợ giảng.</p>
      <Button onClick={onClose} className="w-full">
        Đóng
      </Button>
    </div>
  );
}
