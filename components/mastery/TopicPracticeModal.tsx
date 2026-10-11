"use client";

import { useEffect, useRef, useState } from "react";
import { BookOpen, CheckCircle2, CircleAlert, X } from "lucide-react";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import type { PracticePick } from "@/services/lessons";
import { markFirstPracticeDone } from "@/lib/pwa-install";
import { fetchExamsFull, savePracticeSession } from "@/services/lessons";
import type { Difficulty, Exam, ExamQuestion, QuestionResponse } from "@/features/exams/types";
import {
  DIFFICULTY_LABELS,
  buildQuestionResults,
  emptyResponses,
  gradeExam,
  isAnswered,
  pickRandom,
} from "@/features/exams/types";

import { questionKey } from "@/services/question-context";
import { isFullyCorrect } from "@/features/lessons/practice-step";

type Phase = "loading" | "empty" | "intro" | "running" | "done";

const COUNT = 10;

/** Chia `count` câu cho các bài (mỗi bài ≥1 nếu còn chỗ); bài thiếu câu thì phần dư dồn sang bài còn câu. */
function allocate(sizes: number[], count: number): number[] {
  const take = sizes.map(() => 0);
  let left = Math.min(count, sizes.reduce((a, b) => a + b, 0));
  const order = pickRandom(
    sizes.map((_, i) => i),
    sizes.length,
  );
  while (left > 0) {
    let moved = false;
    for (const i of order) {
      if (left === 0) break;
      if (take[i] < sizes[i]) {
        take[i] += 1;
        left -= 1;
        moved = true;
      }
    }
    if (!moved) break;
  }
  return take;
}

/** Thứ tự dễ → khó để mở đầu bằng câu em làm được, rồi tăng dần (câu "" xếp như trung bình). */
const DIFF_RANK: Record<string, number> = { de: 0, "": 1, "trung-binh": 1, kho: 2 };
/** Phần phụ đạo: tối đa 70% số câu thuộc đúng phần em hổng, còn lại là câu khác của bài. */
const FOCUS_SHARE = 0.7;
/** Sai từng này câu của phần hổng trong cùng lượt → mời xem lại lý thuyết tương tác. */
const THEORY_AFTER_WRONG = 2;

interface LessonResult {
  lessonId: number;
  correct: number;
  total: number;
}

function masteryTone(correct: number, total: number): { tone: "success" | "warning" | "error"; text: string } {
  const pct = total === 0 ? 0 : (correct / total) * 100;
  if (pct >= 80) return { tone: "success", text: "Nắm vững" };
  if (pct >= 50) return { tone: "warning", text: "Cần luyện" };
  return { tone: "error", text: "Chưa đạt" };
}

/**
 * "Luyện 10 câu phần này" từ thẻ mastery (components/mastery/LessonMasteryCard.tsx) — bốc tối đa
 * 10 câu cùng YCCĐ (khớp theo tên `topicName`, đúng cách `exams.questions[].topic` được gắn khi
 * đăng đề) từ CHÍNH các đề đã gắn vào bài học đang xem (`examIds`, học sinh đã có quyền đọc qua
 * cách trang bài học vẫn dùng — không cần RLS/RPC mới cho `question_bank`).
 *
 * Cố tình TÁI DÙNG plumbing "luyện tập" hiện có thay vì viết luồng mới:
 * - `fetchExamsFull` (services/lessons.ts) — đúng hàm PracticeSession.tsx đang dùng để tải câu hỏi.
 * - `gradeExam`/`emptyResponses`/`isAnswered`/`pickRandom` (features/exams/types.ts).
 * - `savePracticeSession` (services/lessons.ts) — ghi practice_sessions + practice_question_results,
 *   NHỜ VẬY lượt luyện này cũng tự động tính vào 10 lượt gần nhất của lần tính mastery kế tiếp.
 * - `QuestionCard` — cùng UI trả lời câu hỏi với ExamRunner/PracticeSession/FixQuizModal.
 *
 * Trang /luyen-tap dùng lại modal này: `topicName` rỗng = mọi YCCĐ của bài, `difficulty` (tuỳ chọn)
 * lọc thêm theo mức Dễ/TB/Khó — cùng nguồn câu, cùng đường ghi phiên luyện.
 *
 * KHÔNG dùng `rank_fix_quiz_start`/`FixQuizModal` (components/rank/FixQuizModal.tsx): hàm đó cần
 * một `exam_result_id` có thật + mùa rank đang mở + đề là nguồn RP, và bốc theo topic TẦNG BÀI
 * (coalesce parent_id) chứ không theo đúng YCCĐ — không khớp ngữ cảnh "cuối bài học"/"sau khi nộp
 * luyện tập" (không phải lúc nào cũng có exam_result). Không dùng select thẳng `question_bank` lọc
 * `topic_id` vì RLS bảng đó chỉ mở cho học sinh qua đúng 1 policy hẹp gắn với `tutoring_needs`
 * đang mở — nới thêm sẽ phạm luật "không nới RLS".
 */
export default function TopicPracticeModal({
  lessonId,
  examIds,
  topicName,
  difficulty,
  count = COUNT,
  examIdsByLesson,
  lessonTitles,
  onPickLesson,
  onClose,
  onFinished,
}: {
  lessonId: number | null;
  examIds: number[];
  topicName: string;
  difficulty?: Difficulty;
  /** Số câu bốc tối đa (mặc định 10). */
  count?: number;
  /** "Ôn tổng hợp" nhiều bài: bài → các đề của bài. Có prop này thì bốc đều giữa các bài, khử câu
   *  trùng giữa các đề và lưu phiên với lesson_id null (`lessonId`/`examIds` bị bỏ qua). */
  examIdsByLesson?: Record<number, number[]>;
  lessonTitles?: Record<number, string>;
  /** Màn kết quả nhiều bài: nút "Luyện riêng bài này". */
  onPickLesson?: (lessonId: number) => void;
  onClose: () => void;
  onFinished?: () => void;
}) {
  const { session } = useAuth();
  const toast = useToast();
  const [phase, setPhase] = useState<Phase>("loading");
  const [picks, setPicks] = useState<PracticePick[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [cur, setCur] = useState(0);
  // Chế độ phụ đạo một phần (có topicName): báo đúng/sai ngay từng câu. checked[i] = câu i đã kiểm tra, ok[i] = đúng trọn vẹn.
  const [checked, setChecked] = useState<boolean[]>([]);
  const [ok, setOk] = useState<boolean[]>([]);
  const [saving, setSaving] = useState(false);
  const [result, setResult] = useState<{ score10: number; correctCount: number; total: number } | null>(null);
  // Bài của từng câu đã bốc (chỉ dùng ở chế độ nhiều bài) và kết quả theo bài sau khi nộp.
  const [pickLessons, setPickLessons] = useState<number[]>([]);
  const [byLesson, setByLesson] = useState<LessonResult[]>([]);
  // Token giữ nguyên suốt phiên: bấm "Nộp bài" hai lần nhanh (hoặc thử lại sau lỗi mạng) không lưu trùng.
  const clientToken = useRef<string | null>(null);
  const submitting = useRef(false);
  const multi = examIdsByLesson !== undefined;
  const guided = !multi && topicName.trim() !== "";

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const allIds = examIdsByLesson
          ? [...new Set(Object.values(examIdsByLesson).flat())]
          : examIds;
        const metas = await fetchExamsFull(allIds);
        if (cancelled) return;
        const collect = (ids: number[], seen?: Set<string>, anyTopic = false) => {
          const out: PracticePick[] = [];
          for (const id of ids) {
            const exam = metas.get(id) as Exam | undefined;
            if (!exam) continue;
            exam.questions.forEach((question, qi) => {
              if (question.type === "essay") return;
              if (!anyTopic && topicName.trim() !== "" && (question.topic ?? "").trim() !== topicName.trim()) return;
              if (difficulty && question.difficulty !== difficulty) return;
              if (seen) {
                const key = questionKey(question);
                if (seen.has(key)) return;
                seen.add(key);
              }
              out.push({ question, examId: exam.id, sourceIndex: qi });
            });
          }
          return out;
        };

        let chosen: PracticePick[];
        let lessonOfPick: number[] = [];
        if (examIdsByLesson) {
          const seen = new Set<string>();
          const lessonIdList = Object.keys(examIdsByLesson).map(Number);
          const pools = lessonIdList.map((lid) => collect([...new Set(examIdsByLesson[lid])], seen));
          const take = allocate(pools.map((p) => p.length), count);
          const tagged = pools.flatMap((pool, i) =>
            pickRandom(pool, take[i]).map((pick) => ({ pick, lessonId: lessonIdList[i] })),
          );
          const mixed = pickRandom(tagged, tagged.length);
          chosen = mixed.map((t) => t.pick);
          lessonOfPick = mixed.map((t) => t.lessonId);
        } else if (topicName.trim() !== "") {
          // Lượt phụ đạo một phần: ~70% câu đúng phần em hổng (ưu tiên Dễ/TB, xếp dễ → khó), câu đầu và câu cuối
          // là câu khác của bài (em làm được) để mở đầu và kết thúc không bằng chuỗi câu sai.
          const focusAll = collect(examIds);
          const focusKeys = new Set(focusAll.map((p) => `${p.examId}:${p.sourceIndex}`));
          const others = collect(examIds, undefined, true).filter((p) => !focusKeys.has(`${p.examId}:${p.sourceIndex}`));
          const wantOthers = Math.min(others.length, Math.max(0, count - Math.ceil(count * FOCUS_SHARE)));
          const focusN = Math.min(focusAll.length, count - wantOthers);
          const otherN = Math.min(others.length, count - focusN);
          const notHard = focusAll.filter((p) => p.question.difficulty !== "kho");
          const hard = focusAll.filter((p) => p.question.difficulty === "kho");
          const focus = [...pickRandom(notHard, Math.min(notHard.length, focusN)), ...pickRandom(hard, Math.max(0, focusN - notHard.length))].sort(
            (a, b) => (DIFF_RANK[a.question.difficulty ?? ""] ?? 1) - (DIFF_RANK[b.question.difficulty ?? ""] ?? 1),
          );
          const warm = pickRandom(others, otherN);
          chosen = otherN >= 2 ? [warm[0], ...focus, ...warm.slice(1)] : [...warm, ...focus];
        } else {
          chosen = pickRandom(collect(examIds), count);
        }
        setPicks(chosen);
        setChecked(chosen.map(() => false));
        setOk(chosen.map(() => false));
        setPickLessons(lessonOfPick);
        setResponses(emptyResponses(chosen.map((p) => p.question)));
        setPhase(chosen.length === 0 ? "empty" : "intro");
      } catch {
        if (!cancelled) setPhase("empty");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [examIds, examIdsByLesson, topicName, difficulty, count]);

  const label = multi
    ? `${Object.keys(examIdsByLesson).length} bài`
    : [topicName.trim() || "Cả bài", difficulty ? DIFFICULTY_LABELS[difficulty] : ""].filter(Boolean).join(" · ");
  const questions = picks.map((p) => p.question);
  const lastIndex = questions.length - 1;
  const answeredCount = questions.filter((q, i) => isAnswered(q, responses[i])).length;

  const focusWrong = picks.filter((p, i) => checked[i] && !ok[i] && (p.question.topic ?? "").trim() === topicName.trim()).length;
  const needTheory = guided && lessonId !== null && focusWrong >= THEORY_AFTER_WRONG;

  function checkCurrent() {
    if (!isAnswered(questions[cur], responses[cur])) return;
    setChecked((p) => p.map((v, i) => (i === cur ? true : v)));
    setOk((p) => p.map((v, i) => (i === cur ? isFullyCorrect(questions[cur], responses[cur]) : v)));
  }

  function setResponse(i: number, r: QuestionResponse) {
    setResponses((prev) => {
      const next = [...prev];
      next[i] = r;
      return next;
    });
  }

  async function submit() {
    if (!session || picks.length === 0 || submitting.current) return;
    submitting.current = true;
    setSaving(true);
    try {
      const summary = gradeExam(questions, responses);
      clientToken.current ??= crypto.randomUUID();
      await savePracticeSession({
        studentId: session.user.id,
        lessonId: multi ? null : lessonId,
        itemId: null,
        picks,
        responses,
        score10: summary.score10,
        correctCount: summary.correctCount,
        durationSeconds: 0,
        timedOut: false,
        clientToken: clientToken.current,
      });
      markFirstPracticeDone();
      if (multi) {
        const rows = buildQuestionResults(questions, responses);
        const acc = new Map<number, LessonResult>();
        rows.forEach((r, i) => {
          const lid = pickLessons[i];
          const cur = acc.get(lid) ?? { lessonId: lid, correct: 0, total: 0 };
          cur.total += 1;
          if (r.is_correct) cur.correct += 1;
          acc.set(lid, cur);
        });
        setByLesson([...acc.values()]);
      }
      setResult({ score10: summary.score10, correctCount: summary.correctCount, total: questions.length });
      setPhase("done");
      onFinished?.();
    } catch {
      toast("error", "Chưa lưu được kết quả, thử lại nhé.");
    } finally {
      submitting.current = false;
      setSaving(false);
    }
  }

  const wide = phase === "running" || (phase === "done" && byLesson.length > 1);

  return (
    <div
      className="fixed inset-0 z-100 flex items-center justify-center bg-black/60 px-4 py-6 backdrop-blur-sm animate-modal-backdrop-in"
      onClick={onClose}
      role="presentation"
    >
      <div
        className={`max-h-[90vh] w-full overflow-y-auto rounded-2xl border border-white/10 bg-panel p-5 shadow-2xl sm:p-6 animate-modal-panel-in ${
          wide ? "max-w-2xl" : "max-w-sm"
        }`}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
          <div className="mb-3 flex items-start justify-between gap-3">
            <h2 className="font-display text-lg font-semibold text-white">{multi ? "Ôn tổng hợp" : "Luyện thêm"}: {label}</h2>
            <button
              type="button"
              onClick={onClose}
              aria-label="Đóng"
              className="-mr-2 -mt-2 flex h-11 w-11 shrink-0 items-center justify-center text-slate-400 hover:text-white"
            >
              <X size={18} />
            </button>
          </div>

          {phase === "loading" && <p className="text-sm text-slate-400">Đang soạn câu hỏi…</p>}

          {phase === "empty" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                {multi
                  ? "Các bài em chọn chưa có câu trắc nghiệm để ôn. Hãy chọn thêm bài khác nhé."
                  : "Chưa có đủ câu hỏi cho yêu cầu này trong các đề của bài học. Hãy hỏi thầy/cô nhé."}
              </p>
              <Button variant="outline" onClick={onClose} className="w-full">
                Đóng
              </Button>
            </div>
          )}

          {phase === "intro" && (
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                <strong className="text-white">{label}</strong> · {questions.length} câu bốc ngẫu nhiên từ
                {multi ? " các bài em chọn." : " các đề của bài học."}
              </p>
              {multi && questions.length < count && (
                <p className="text-sm text-amber-300">
                  Chỉ có {questions.length} câu phù hợp (em chọn {count} câu).
                </p>
              )}
              <p className="text-xs text-slate-500">Làm xong sẽ tính vào mức độ thành thạo của em ở phần này.</p>
              <Button onClick={() => setPhase("running")} className="w-full">
                Bắt đầu
              </Button>
            </div>
          )}

          {phase === "running" && (
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold text-white">
                  Câu {cur + 1}/{questions.length}
                </p>
                <p className="text-xs text-slate-500">
                  Đã trả lời {answeredCount}/{questions.length}
                </p>
              </div>
              <QuestionCard
                key={`${cur}-${guided && checked[cur] ? "r" : "a"}`}
                index={cur + 1}
                question={questions[cur]}
                response={responses[cur]}
                onChange={guided && checked[cur] ? undefined : (r) => setResponse(cur, r)}
                review={guided && checked[cur]}
              />
              {guided && checked[cur] && (
                <p
                  role="status"
                  aria-live="polite"
                  className={`flex items-start gap-2 rounded-xl border px-3 py-2 text-sm ${
                    ok[cur] ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-100" : "border-amber-500/40 bg-amber-500/10 text-amber-100"
                  }`}
                >
                  {ok[cur] ? <CheckCircle2 size={18} className="mt-0.5 shrink-0" aria-hidden /> : <CircleAlert size={18} className="mt-0.5 shrink-0" aria-hidden />}
                  <span>{ok[cur] ? "Đúng rồi." : "Chưa đúng. Đáp án và lời giải ở phía trên."}</span>
                </p>
              )}
              {needTheory && checked[cur] && !ok[cur] && (
                <TheoryNudge lessonId={lessonId} topicName={topicName} wrong={focusWrong} newTab />
              )}
              <div className="flex items-center justify-between gap-2">
                <Button variant="outline" onClick={() => setCur((i) => Math.max(0, i - 1))} disabled={cur === 0}>
                  Câu trước
                </Button>
                {guided && !checked[cur] ? (
                  <Button onClick={checkCurrent} disabled={!isAnswered(questions[cur], responses[cur])}>
                    Kiểm tra
                  </Button>
                ) : cur < lastIndex ? (
                  <Button onClick={() => setCur((i) => Math.min(lastIndex, i + 1))}>Câu tiếp</Button>
                ) : (
                  <Button onClick={submit} disabled={saving}>
                    {saving ? "Đang nộp…" : "Nộp bài"}
                  </Button>
                )}
              </div>
            </div>
          )}

          {phase === "done" && result && (
            <div className="space-y-4">
              <div
                className={`rounded-xl border p-4 text-center ${
                  result.correctCount === result.total
                    ? "border-emerald-500/40 bg-emerald-500/10"
                    : "border-amber-500/40 bg-amber-500/10"
                }`}
              >
                <p className="text-3xl font-bold text-white">{result.score10.toFixed(2)}</p>
                <p className="mt-1 text-sm text-slate-300">
                  Đúng {result.correctCount}/{result.total} câu
                </p>
              </div>
              {guided && lessonId !== null && (focusWrong >= THEORY_AFTER_WRONG || result.correctCount * 2 < result.total) && (
                <TheoryNudge lessonId={lessonId} topicName={topicName} wrong={focusWrong} />
              )}
              {multi && byLesson.length > 0 && (
                <ul className="divide-y divide-white/10 rounded-xl border border-white/10">
                  {byLesson.map((r) => {
                    const m = masteryTone(r.correct, r.total);
                    return (
                      <li key={r.lessonId} className="space-y-2 px-3 py-3">
                        <div className="flex items-start justify-between gap-2">
                          <p className="min-w-0 flex-1 text-sm font-semibold text-white">
                            {lessonTitles?.[r.lessonId] ?? `Bài ${r.lessonId}`}
                          </p>
                          <Badge tone={m.tone} className="shrink-0 whitespace-nowrap">
                            {m.text}
                          </Badge>
                        </div>
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <p className="text-[13px] text-slate-400">
                            Đúng {r.correct}/{r.total} câu
                          </p>
                          {onPickLesson && (
                            <button
                              type="button"
                              onClick={() => onPickLesson(r.lessonId)}
                              className="min-h-11 rounded-full border border-white/15 px-4 text-[13px] font-semibold text-white hover:border-white/30"
                            >
                              Luyện riêng bài này
                            </button>
                          )}
                        </div>
                      </li>
                    );
                  })}
                </ul>
              )}
              <Button variant="outline" onClick={onClose} className="w-full">
                Đóng
              </Button>
            </div>
          )}
      </div>
    </div>
  );
}

/** Mời xem lại lý thuyết tương tác của bài. Đang làm dở thì mở tab mới để không mất lượt (newTab). */
function TheoryNudge({ lessonId, topicName, wrong, newTab = false }: { lessonId: number | null; topicName: string; wrong: number; newTab?: boolean }) {
  if (lessonId === null) return null;
  return (
    <div className="flex items-start gap-3 rounded-xl border border-sky-500/40 bg-sky-500/10 px-3 py-3 text-sm text-slate-100">
      <BookOpen size={18} className="mt-0.5 shrink-0" aria-hidden />
      <div className="space-y-2">
        <p>
          Phần <b>{topicName}</b> em còn sai {wrong > 0 ? `${wrong} câu` : "nhiều"}. Xem lại lý thuyết tương tác của bài rồi quay lại luyện nhé
          {newTab ? " — bài đang làm vẫn giữ nguyên." : "."}
        </p>
        <a
          href={`/lop-hoc/bai?id=${lessonId}#muc=ly-thuyet`}
          {...(newTab ? { target: "_blank", rel: "noopener" } : {})}
          className="inline-flex min-h-11 items-center rounded-full border border-white/20 px-4 text-sm font-semibold text-white hover:border-white/40"
        >
          Mở lý thuyết{newTab ? " (tab mới)" : ""}
        </a>
      </div>
    </div>
  );
}
