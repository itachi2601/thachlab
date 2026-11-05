"use client";

import { useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import QuestionCard from "@/components/exams/QuestionCard";
import Button from "@/components/ui/Button";
import { getSupabase } from "@/services/supabase";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeExam, isAnswered } from "@/features/exams/types";
import { arrangeForMotivation } from "@/features/lessons/practice-arrange";

const COUNT = 3;

type Phase = "idle" | "loading" | "empty" | "running" | "done";

interface SimilarRow {
  id: number;
  question: ExamQuestion;
  same_form: boolean;
}

/** Nguồn câu đang hiện: đúng dạng (question_dang) hay cùng chủ đề (dự phòng, chưa phân dạng). */
type Source = "dang" | "chu_de";

/**
 * "Làm bài tương tự" ở cuối một dạng bài tập mẫu, bốc COUNT câu từ ngân hàng (HS không đọc thẳng bảng — RLS):
 * 1. `get_similar_dang_questions(lesson, số dạng)` — chỉ câu đã gán ĐÚNG dạng (question_dang, unsure=false).
 * 2. Dạng chưa có câu gán (hoặc RPC chưa có trên DB) → `get_similar_bank_questions(chủ đề)` nhưng ghi rõ nhãn
 *    "Câu cùng chủ đề (chưa phân dạng)" để em không tưởng đó là cùng dạng.
 * 3. Cả hai rỗng → báo "Dạng này chưa có bài tương tự", không đưa câu lệch.
 * Chấm ngay phía em để đối chiếu; chưa ghi vào phiên luyện tập/mastery (RPC không trả mã đề nguồn).
 * Đặt sau lời giải để "ví dụ mẫu đi trước, retrieval đi sau" (docs/AI-TUTOR.md 9.3).
 */
export default function SimilarBankPractice({
  lessonId,
  dangNo,
  topicId,
  form,
  color = "#8B5CF6",
  stepTitles,
  defaultStep,
  onGoRoi,
}: {
  lessonId?: number;
  /** Số N trong nhãn "Dạng N · …" của dạng mẫu. */
  dangNo?: number;
  topicId?: number;
  form?: string;
  color?: string;
  /** Gỡ rối (9/10/2026): làm sai → hỏi "em tính đến bước nào?" theo các bước của dạng mẫu rồi gọi onGoRoi(idx). */
  stepTitles?: string[];
  defaultStep?: number;
  onGoRoi?: (stepIdx: number) => void;
}) {
  const [goRoi, setGoRoi] = useState(false);
  const [phase, setPhase] = useState<Phase>("idle");
  const [rows, setRows] = useState<SimilarRow[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [seen, setSeen] = useState<number[]>([]);
  const [error, setError] = useState(false);
  // null = chưa chọn nguồn. Đã có câu đúng dạng thì "làm câu khác" chỉ lấy tiếp đúng dạng (hết thì báo hết).
  const [source, setSource] = useState<Source | null>(null);

  async function fetchDang(exclude: number[]): Promise<SimilarRow[] | null> {
    if (!lessonId || dangNo == null) return null;
    const { data, error: err } = await getSupabase().rpc("get_similar_dang_questions", {
      p_lesson_id: lessonId,
      p_dang_no: dangNo,
      p_exclude_ids: exclude,
      p_limit: COUNT,
    });
    return err ? null : ((data ?? []) as SimilarRow[]); // lỗi (kể cả RPC chưa chạy migration) → coi như chưa có
  }

  async function fetchChuDe(exclude: number[]): Promise<SimilarRow[] | null> {
    if (!topicId) return [];
    const { data, error: err } = await getSupabase().rpc("get_similar_bank_questions", {
      p_topic_id: topicId,
      p_form: form ?? "",
      p_exclude_ids: exclude,
      p_limit: COUNT,
    });
    return err ? null : ((data ?? []) as SimilarRow[]);
  }

  const usable = (list: SimilarRow[]) => list.filter((r) => r.question && r.question.type !== "essay");

  async function load(exclude: number[]) {
    setPhase("loading");
    setError(false);
    let next: SimilarRow[] = [];
    let src: Source | null = source;
    let failed = false;
    if (src !== "chu_de") {
      const dang = await fetchDang(exclude);
      next = usable(dang ?? []);
      if (next.length > 0) src = "dang";
      else if (src === "dang") failed = dang === null; // đang lấy tiếp đúng dạng mà lỗi mạng → "chưa tải được", không phải "đã hết"
    }
    if (next.length === 0 && src !== "dang") {
      const chuDe = await fetchChuDe(exclude);
      failed = chuDe === null;
      next = usable(chuDe ?? []);
      if (next.length > 0) src = "chu_de";
    }
    setSource(src);
    if (next.length === 0) {
      setError(failed);
      setPhase("empty");
      return;
    }
    next = arrangeForMotivation(next);
    setRows(next);
    setResponses(emptyResponses(next.map((r) => r.question)));
    setSeen([...exclude, ...next.map((r) => r.id)]);
    setPhase("running");
  }

  const questions = rows.map((r) => r.question);
  const answered = questions.filter((q, i) => isAnswered(q, responses[i])).length;
  const summary = phase === "done" ? gradeExam(questions, responses) : null;

  if (phase === "idle") {
    return (
      <div className="mt-4 rounded-xl border border-line p-4">
        <p className="text-sm text-ink">
          Đọc xong lời giải thì <strong className="text-ink">gấp lại, tự trình bày từ đầu trên giấy</strong>, rồi thử
          {" "}{COUNT} bài cùng dạng.
        </p>
        <Button onClick={() => void load(seen)} className="mt-3" style={{ background: color }}>
          Làm bài tương tự
        </Button>
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-3 rounded-xl border border-line p-4" role="region" aria-label="Bài tương tự">
      {phase === "loading" && <p className="text-sm text-muted">Đang tìm bài tương tự…</p>}
      {phase === "empty" && (
        <p className="text-sm text-ink" role="status">
          {error
            ? "Chưa tải được bài tương tự, thử lại sau nhé."
            : seen.length > 0
              ? source === "chu_de"
                ? "Đã hết câu cùng chủ đề trong ngân hàng."
                : "Đã hết bài tương tự cho dạng này trong ngân hàng."
              : "Dạng này chưa có bài tương tự."}
        </p>
      )}
      {(phase === "running" || phase === "done") && (
        <>
          {source === "chu_de" && (
            <p className="text-sm text-muted" role="note">
              Câu cùng chủ đề (chưa phân dạng) — có thể khác cách giải dạng mẫu.
            </p>
          )}
          {rows.map((r, i) => (
            <QuestionCard
              key={r.id}
              index={i + 1}
              question={r.question}
              response={responses[i]}
              review={phase === "done"}
              onChange={(v) =>
                phase === "running" && setResponses((prev) => prev.map((x, j) => (j === i ? v : x)))
              }
            />
          ))}
          {phase === "running" ? (
            <Button onClick={() => setPhase("done")} disabled={answered === 0}>
              Chấm {answered}/{questions.length} câu
            </Button>
          ) : (
            <div className="space-y-3">
              <div className="flex flex-wrap items-center gap-3">
                <p className="text-sm font-semibold text-ink">
                  Đúng {summary?.correctCount ?? 0}/{questions.length} câu
                </p>
                <Button variant="outline" onClick={() => { setGoRoi(false); void load(seen); }}>
                  Làm {COUNT} câu khác
                </Button>
                {stepTitles && onGoRoi && (summary?.correctCount ?? 0) < questions.length && !goRoi && (
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
                        style={i === defaultStep ? { borderColor: color } : undefined}
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
        </>
      )}
    </div>
  );
}
