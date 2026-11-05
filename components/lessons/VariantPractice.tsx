"use client";

import { useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import QuestionCard from "@/components/exams/QuestionCard";
import Button from "@/components/ui/Button";
import type { QuestionResponse } from "@/features/exams/types";
import type { WorkedVariant } from "@/features/lessons/types";
import { generate, gradeNumeric, type VariantQuestion } from "@/lib/bien-the";

type Phase = "idle" | "running" | "done" | "broken";

const newSeed = () => (Math.random() * 2 ** 32) >>> 0;

/**
 * "Luyện đổi số" ở cuối một dạng bài tập mẫu (chặng 3A, 5/11/2026): máy tự sinh câu cùng dạng từ khuôn `bien_the`
 * (lib/bien-the.ts) — không gọi mạng, vô hạn câu. Một câu mỗi lượt (N1: tải nhận thức thấp), nhãn A. B. C. D. /
 * ô đáp số do QuestionCard sinh (E1–E3). Sai → hỏi "em tính đến bước nào" như SimilarBankPractice (gỡ rối);
 * chọn phương án nhiễu thì gợi ý sẵn bước ứng với lỗi đó.
 */
export default function VariantPractice({
  bt,
  color = "#8B5CF6",
  stepTitles,
  defaultStep,
  onGoRoi,
}: {
  bt: WorkedVariant;
  color?: string;
  stepTitles?: string[];
  defaultStep?: number;
  onGoRoi?: (stepIdx: number) => void;
}) {
  const [phase, setPhase] = useState<Phase>("idle");
  const [q, setQ] = useState<VariantQuestion | null>(null);
  const [resp, setResp] = useState<QuestionResponse>(null);
  const [done, setDone] = useState({ n: 0, right: 0 });
  const [goRoi, setGoRoi] = useState(false);

  function next() {
    const g = generate(bt, newSeed());
    if (!g) return setPhase("broken");
    setQ(g);
    setResp(g.question.type === "short_answer" ? "" : null);
    setGoRoi(false);
    setPhase("running");
  }

  if (phase === "idle") {
    return (
      <div className="mt-4 rounded-xl border border-line p-4">
        <p className="text-sm text-ink">
          <strong className="text-ink">Luyện đổi số:</strong> cùng dạng này, số liệu mới mỗi lần — làm bao nhiêu câu tuỳ em.
        </p>
        <Button onClick={next} className="mt-3" style={{ background: color }}>
          Làm câu đổi số
        </Button>
      </div>
    );
  }
  if (phase === "broken" || !q) {
    return (
      <p className="mt-4 rounded-xl border border-line p-4 text-sm text-ink" role="status">
        Chưa sinh được câu đổi số cho dạng này.
      </p>
    );
  }

  const qq = q.question;
  const numeric = qq.type === "short_answer" ? gradeNumeric(typeof resp === "string" ? resp : "", q, bt) : null;
  const correct = numeric ? numeric.dung : resp === (qq.type === "multiple_choice" ? qq.answer : -1);
  // Ô đáp số trong sai số cho phép nhưng khác chuỗi đáp án: đưa QuestionCard chuỗi chuẩn để thẻ tô "Đúng".
  const reviewResp = numeric?.dung && !numeric.khopChuoi && qq.type === "short_answer" ? qq.answer : resp;
  const answered = qq.type === "short_answer" ? typeof resp === "string" && resp.trim() !== "" : resp !== null;
  const pickedStep = typeof resp === "number" ? q.stepByOption?.[resp] : undefined;
  const hintStep = pickedStep ?? defaultStep;

  function check() {
    setPhase("done");
    setDone((d) => ({ n: d.n + 1, right: d.right + (correct ? 1 : 0) }));
  }

  return (
    <div className="mt-4 space-y-3 rounded-xl border border-line p-4" role="region" aria-label="Luyện đổi số">
      <p className="text-xs text-muted">
        Luyện đổi số · số liệu do máy sinh{done.n > 0 ? ` · đã làm ${done.n} câu, đúng ${done.right}` : ""}
      </p>
      <QuestionCard
        key={q.seed}
        index={done.n + (phase === "done" ? 0 : 1)}
        question={qq}
        response={phase === "done" ? reviewResp : resp}
        review={phase === "done"}
        onChange={phase === "running" ? setResp : undefined}
      />
      {phase === "done" && numeric?.dung && !numeric.khopChuoi && (
        <p className="text-xs text-muted">
          Em ghi {String(resp)}, đáp án làm tròn là {qq.type === "short_answer" ? qq.answer : ""} — lệch trong sai số cho phép
          {bt.sai_so ? ` (±${(bt.sai_so * 100).toLocaleString("vi-VN")} %)` : ""} nên tính đúng.
        </p>
      )}
      {phase === "running" ? (
        <Button onClick={check} disabled={!answered}>
          Chấm
        </Button>
      ) : (
        <div className="space-y-3">
          <div className="flex flex-wrap items-center gap-3">
            <Button variant="outline" onClick={next}>
              Câu khác
            </Button>
            {!correct && stepTitles && onGoRoi && !goRoi && (
              <Button variant="outline" onClick={() => setGoRoi(true)}>
                Xem lại chỗ kẹt
              </Button>
            )}
          </div>
          {goRoi && stepTitles && onGoRoi && (
            <div className="rounded-lg border border-line p-3" role="region" aria-label="Gỡ rối">
              <p className="mb-2 text-sm text-ink">Em tính đến bước nào thì kẹt? Chọn để mở lại đúng bước đó trong bài mẫu.</p>
              <div className="grid gap-2">
                {stepTitles.map((t, i) => (
                  <button
                    key={i}
                    type="button"
                    className="lesson-btn-ghost bt-goroi-btn"
                    style={i === hintStep ? { borderColor: color } : undefined}
                    onClick={() => onGoRoi(i)}
                  >
                    <span className="mr-2 text-muted">{i + 1}.</span>
                    <ContentHtml html={t} className="inline" />
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
