"use client";

import { useEffect, useState } from "react";
import { Pencil } from "lucide-react";
import { getSupabase } from "@/services/supabase";
import { fetchExamOverview, fetchWrongestQuestions, type ExamOverview, type WrongestQuestion } from "@/services/analytics";
import type { ExamQuestion } from "@/features/exams/types";

type ExamRef = { id: number; title: string };

/**
 * Phân tích đề của bài AVCN đang chọn (Luyện tập + Kiểm tra) để thầy biết câu nào sai nhiều mà sửa đề.
 * Đề AVCN không gán lớp (lớp vào tự do, gán sẽ chặn xem lại), nên lấy đề qua lesson_items.exam_ids
 * thay vì exam_classes như phân tích của lớp THPT.
 */
export default function TeacherAvcnExamAnalysis({ examIds, studentIds }: { examIds: number[]; studentIds: string[] }) {
  const [exams, setExams] = useState<ExamRef[]>([]);
  const [examId, setExamId] = useState<number | null>(null);
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [overview, setOverview] = useState<ExamOverview | null>(null);
  const [wrongest, setWrongest] = useState<WrongestQuestion[] | null>(null);

  const idsKey = examIds.join(",");
  useEffect(() => {
    if (examIds.length === 0) {
      setExams([]);
      setExamId(null);
      return;
    }
    void getSupabase()
      .from("exams")
      .select("id, title")
      .in("id", examIds)
      .then(({ data }) => {
        const list = (data ?? []) as ExamRef[];
        setExams(list);
        // Ưu tiên đề Kiểm tra (id lớn hơn, đăng sau Luyện tập).
        setExamId((cur) => (cur !== null && list.some((e) => e.id === cur) ? cur : (list.at(-1)?.id ?? null)));
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [idsKey]);

  useEffect(() => {
    if (examId === null) return;
    setOverview(null);
    setWrongest(null);
    setQuestions([]);
    void getSupabase()
      .from("exams")
      .select("questions")
      .eq("id", examId)
      .single()
      .then(({ data }) => setQuestions((data?.questions as ExamQuestion[]) ?? []));
    fetchExamOverview(examId, studentIds).then(setOverview).catch(() => undefined);
    fetchWrongestQuestions(examId, studentIds).then(setWrongest).catch(() => setWrongest([]));
  }, [examId, studentIds]);

  if (exams.length === 0) return null;

  return (
    <section className="space-y-3">
      <div className="flex flex-wrap items-center gap-3">
        <h3 className="font-semibold text-ink">Phân tích đề để sửa</h3>
        <select
          aria-label="Đề"
          value={examId ?? ""}
          onChange={(e) => setExamId(Number(e.target.value))}
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
