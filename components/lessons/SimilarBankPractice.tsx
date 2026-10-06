"use client";

import { useState } from "react";
import QuestionCard from "@/components/exams/QuestionCard";
import Button from "@/components/ui/Button";
import { getSupabase } from "@/services/supabase";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";
import { emptyResponses, gradeExam, isAnswered } from "@/features/exams/types";

const COUNT = 3;

type Phase = "idle" | "loading" | "empty" | "running" | "done";

interface SimilarRow {
  id: number;
  question: ExamQuestion;
  same_form: boolean;
}

/**
 * "Làm bài tương tự" ở cuối một dạng bài tập mẫu: bốc COUNT câu cùng chủ đề (ưu tiên cùng Dạng) từ
 * ngân hàng câu hỏi qua RPC `get_similar_bank_questions` (học sinh không đọc được bảng trực tiếp — RLS).
 * Chấm ngay phía em để đối chiếu; chưa ghi vào phiên luyện tập/mastery (RPC không trả mã đề nguồn).
 * Đặt sau lời giải để "ví dụ mẫu đi trước, retrieval đi sau" (docs/AI-TUTOR.md 9.3).
 */
export default function SimilarBankPractice({
  topicId,
  form,
  color = "#8B5CF6",
}: {
  topicId: number;
  form?: string;
  color?: string;
}) {
  const [phase, setPhase] = useState<Phase>("idle");
  const [rows, setRows] = useState<SimilarRow[]>([]);
  const [responses, setResponses] = useState<QuestionResponse[]>([]);
  const [seen, setSeen] = useState<number[]>([]);
  const [error, setError] = useState(false);

  async function load(exclude: number[]) {
    setPhase("loading");
    setError(false);
    const { data, error: err } = await getSupabase().rpc("get_similar_bank_questions", {
      p_topic_id: topicId,
      p_form: form ?? "",
      p_exclude_ids: exclude,
      p_limit: COUNT,
    });
    if (err) {
      setError(true);
      setPhase("empty");
      return;
    }
    const next = ((data ?? []) as SimilarRow[]).filter((r) => r.question && r.question.type !== "essay");
    if (next.length === 0) {
      setPhase("empty");
      return;
    }
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
      <div className="mt-4 rounded-xl border border-white/10 p-4">
        <p className="text-sm text-slate-300">
          Đọc xong lời giải thì <strong className="text-white">gấp lại, tự trình bày từ đầu trên giấy</strong>, rồi thử
          {" "}{COUNT} bài cùng dạng.
        </p>
        <Button onClick={() => void load(seen)} className="mt-3" style={{ background: color }}>
          Làm bài tương tự
        </Button>
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-3 rounded-xl border border-white/10 p-4" role="region" aria-label="Bài tương tự">
      {phase === "loading" && <p className="text-sm text-slate-400">Đang tìm bài tương tự…</p>}
      {phase === "empty" && (
        <p className="text-sm text-slate-300" role="status">
          {error
            ? "Chưa tải được bài tương tự, thử lại sau nhé."
            : seen.length > 0
              ? "Đã hết bài tương tự cho dạng này trong ngân hàng."
              : "Ngân hàng chưa có bài tương tự cho dạng này."}
        </p>
      )}
      {(phase === "running" || phase === "done") && (
        <>
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
            <div className="flex flex-wrap items-center gap-3">
              <p className="text-sm font-semibold text-white">
                Đúng {summary?.correctCount ?? 0}/{questions.length} câu
              </p>
              <Button variant="outline" onClick={() => void load(seen)}>
                Làm {COUNT} câu khác
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
