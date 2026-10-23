"use client";

import { useEffect, useState } from "react";
import { Pencil } from "lucide-react";
import { getSupabase } from "@/services/supabase";
import { fetchExamOverview, fetchWrongestQuestions, type ExamOverview, type WrongestQuestion } from "@/services/analytics";
import type { ExamQuestion } from "@/features/exams/types";

type ExamRef = { id: number; title: string };

const EMPTY_EXAMS: ExamRef[] = [];
const EMPTY_QUESTIONS: ExamQuestion[] = [];

/**
 * Phân tích đề của bài AVCN đang chọn (Luyện tập + Kiểm tra) để thầy biết câu nào sai nhiều mà sửa đề.
 * Đề AVCN không gán lớp (lớp vào tự do, gán sẽ chặn xem lại), nên lấy đề qua lesson_items.exam_ids
 * thay vì exam_classes như phân tích của lớp THPT.
 */
export default function TeacherAvcnExamAnalysis({ examIds, studentIds }: { examIds: number[]; studentIds: string[] }) {
  const [examsState, setExamsState] = useState<ExamRef[] | null>(null);
  const [selectedExamId, setSelectedExamId] = useState<number | null>(null);
  const [questionsState, setQuestionsState] = useState<{ examId: number; list: ExamQuestion[] } | null>(null);
  const [overviewState, setOverviewState] = useState<{ examId: number; data: ExamOverview } | null>(null);
  const [wrongestState, setWrongestState] = useState<{ examId: number; list: WrongestQuestion[] } | null>(null);

  const idsKey = examIds.join(",");
  // Khoá rỗng (không còn đề) hoặc đổi đề: giá trị được suy ra ngay lúc render thay vì reset bằng setState trong effect.
  const exams = idsKey === "" ? EMPTY_EXAMS : (examsState ?? EMPTY_EXAMS);
  const examId = idsKey === "" ? null : selectedExamId;
  const questions = questionsState && questionsState.examId === examId ? questionsState.list : EMPTY_QUESTIONS;
  const overview = overviewState && overviewState.examId === examId ? overviewState.data : null;
  const wrongest = wrongestState && wrongestState.examId === examId ? wrongestState.list : null;

  useEffect(() => {
    if (examIds.length === 0) return;
    void getSupabase()
      .from("exams")
      .select("id, title")
      .in("id", examIds)
      .then(({ data }) => {
        const list = (data ?? []) as ExamRef[];
        setExamsState(list);
        // Ưu tiên đề Kiểm tra (id lớn hơn, đăng sau Luyện tập).
        setSelectedExamId((cur) => (cur !== null && list.some((e) => e.id === cur) ? cur : (list.at(-1)?.id ?? null)));
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [idsKey]);

  useEffect(() => {
    if (examId === null) return;
    let cancelled = false;
    void getSupabase()
      .from("exams_staff")
      .select("questions")
      .eq("id", examId)
      .single()
      .then(({ data }) => {
        if (cancelled) return;
        setQuestionsState({ examId, list: (data?.questions as ExamQuestion[]) ?? [] });
      });
    fetchExamOverview(examId, studentIds)
      .then((data) => {
        if (cancelled) return;
        setOverviewState({ examId, data });
      })
      .catch(() => undefined);
    fetchWrongestQuestions(examId, studentIds)
      .then((list) => {
        if (cancelled) return;
        setWrongestState({ examId, list });
      })
      .catch(() => {
        if (cancelled) return;
        setWrongestState({ examId, list: [] });
      });
    return () => {
      cancelled = true;
    };
  }, [examId, studentIds]);

  if (exams.length === 0) return null;

  return (
    <section className="space-y-3">
      <div className="flex flex-wrap items-center gap-3">
        <h3 className="font-semibold text-ink">Phân tích đề để sửa</h3>
        <select
          aria-label="Đề"
          value={examId ?? ""}
          onChange={(e) => setSelectedExamId(Number(e.target.value))}
          className="rounded-xl border border-line-strong bg-panel-deep px-3 py-2 text-sm text-ink"
        >
          {exams.map((e) => (
            <option key={e.id} value={e.id}>
              {e.title}
            </option>
          ))}
        </select>
        {examId !== null && (
          <a
            href={`/quan-tri/sua-de?exam=${examId}`}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 rounded-xl border border-line-strong px-3 py-2 text-sm font-bold text-ink hover:bg-surface-2"
          >
            <Pencil size={14} /> Sửa đề
          </a>
        )}
      </div>

      {overview && overview.attempts > 0 ? (
        <p className="text-sm text-muted">
          {overview.attempts} sinh viên đã làm · điểm trung bình {overview.average.toFixed(1)} · đạt (≥5) {Math.round(overview.passRate)}%
        </p>
      ) : (
        <p className="text-sm text-muted">Chưa có sinh viên nào trong lớp nộp đề này.</p>
      )}

      {wrongest && wrongest.length > 0 && (
        <div className="overflow-x-auto rounded-2xl border border-line">
          <table className="w-full min-w-120 text-left text-sm">
            <thead className="bg-surface-2 text-muted">
              <tr>
                <th className="px-4 py-3 font-medium">Câu</th>
                <th className="px-4 py-3 font-medium">Nội dung</th>
                <th className="px-4 py-3 font-medium">Sai</th>
                <th className="px-4 py-3 font-medium" />
              </tr>
            </thead>
            <tbody className="divide-y divide-line text-ink">
              {wrongest.slice(0, 12).map((q) => {
                const raw = (questions[q.questionIndex]?.question ?? "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
                // Câu Article có đoạn văn đứng đầu: lấy phần sau đoạn cho dễ nhận.
                const stem = raw.length > 110 ? `…${raw.slice(-110)}` : raw;
                return (
                  <tr key={q.questionIndex}>
                    <td className="px-4 py-3 font-semibold">{q.questionIndex + 1}</td>
                    <td className="px-4 py-3 text-muted">{stem || "—"}</td>
                    <td className={`px-4 py-3 font-mono font-bold ${q.pct >= 60 ? "text-red-500" : q.pct >= 30 ? "text-amber-600" : "text-ink"}`}>
                      {q.pct}% <span className="font-normal text-muted">({q.wrong}/{q.total})</span>
                    </td>
                    <td className="px-4 py-3">
                      <a
                        href={`/quan-tri/sua-de?exam=${examId}&q=${q.questionIndex}`}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs font-bold text-cyan-600 hover:underline"
                      >
                        Sửa câu
                      </a>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
