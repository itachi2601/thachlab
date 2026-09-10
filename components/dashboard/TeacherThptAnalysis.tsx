"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { BarChart3, ChevronDown } from "lucide-react";
import type { ClassStudent } from "@/services/classes";
import type { ExamQuestion } from "@/features/exams/types";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import ContentHtml from "@/components/exams/ContentHtml";
import { useToast } from "@/components/ui/Toast";
import { fetchClassExamResults } from "@/services/class-results";
import { getSupabase } from "@/services/supabase";
import {
  fetchClassAssessments,
  fetchClassTopicMatrix,
  fetchExamOverview,
  fetchWrongestQuestions,
  publishClassAssessment,
  type ClassAssessment,
  type ExamOverview,
  type TopicGap,
  type WrongestQuestion,
} from "@/services/analytics";

const KIND_OPTIONS = [
  { value: "giua_ki", label: "Giữa kỳ" },
  { value: "cuoi_ki", label: "Cuối kỳ" },
  { value: "chuong", label: "KT chương" },
  { value: "thuong_xuyen", label: "KT thường xuyên" },
];

function formLabel(form: string) {
  return form === "ly_thuyet" || form === "bai_tap"
    ? QUESTION_FORM_LABELS[form]
    : "—";
}

function heat(pctVal: number) {
  if (pctVal >= 60) return "bg-red-500/25 text-red-300";
  if (pctVal >= 35) return "bg-amber-500/20 text-amber-300";
  if (pctVal >= 15) return "bg-white/10 text-slate-300";
  return "bg-emerald-500/15 text-emerald-300";
}

export default function TeacherThptAnalysis({
  classId,
  students,
}: {
  classId: number;
  students: ClassStudent[];
}) {
  const toast = useToast();
  const studentIds = useMemo(() => students.map((s) => s.id), [students]);

  const [exams, setExams] = useState<{ id: number; title: string }[]>([]);
  const [examId, setExamId] = useState<number | null>(null);
  const [assessments, setAssessments] = useState<ClassAssessment[]>([]);

  const [overview, setOverview] = useState<ExamOverview | null>(null);
  const [wrongest, setWrongest] = useState<WrongestQuestion[] | null>(null);
  const [matrix, setMatrix] = useState<TopicGap[] | null>(null);
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [openQ, setOpenQ] = useState<number | null>(null);

  const loadAssessments = useCallback(() => {
    fetchClassAssessments(classId).then(setAssessments).catch(() => setAssessments([]));
  }, [classId]);

  useEffect(() => {
    loadAssessments();
    fetchClassExamResults(studentIds)
      .then((rows) => {
        const map = new Map<number, string>();
        rows.forEach((r) => map.set(r.exam_id, r.exams?.title ?? `Đề #${r.exam_id}`));
        const list = [...map.entries()].map(([id, title]) => ({ id, title }));
        setExams(list);
        setExamId((cur) => cur ?? list[0]?.id ?? null);
      })
      .catch(() => setExams([]));
  }, [studentIds, loadAssessments]);

  useEffect(() => {
    if (!examId) return;
    setOverview(null);
    setWrongest(null);
    setMatrix(null);
    setOpenQ(null);
    fetchExamOverview(examId, studentIds).then(setOverview).catch(() => undefined);
    fetchWrongestQuestions(examId, studentIds).then(setWrongest).catch(() => setWrongest([]));
    fetchClassTopicMatrix(studentIds, examId).then(setMatrix).catch(() => setMatrix([]));
    getSupabase()
      .from("exams")
      .select("questions")
      .eq("id", examId)
      .single()
      .then(({ data }) => setQuestions((data?.questions as ExamQuestion[]) ?? []));
  }, [examId, studentIds]);

  const assessment = assessments.find((a) => a.examId === examId) ?? null;

  const topics = useMemo(() => {
    const set = new Map<string, { ly: TopicGap | null; bt: TopicGap | null }>();
    for (const g of matrix ?? []) {
      const e = set.get(g.topic) ?? { ly: null, bt: null };
      if (g.form === "ly_thuyet") e.ly = g;
      else if (g.form === "bai_tap") e.bt = g;
      set.set(g.topic, e);
    }
    return [...set.entries()].sort(
      (a, b) =>
        Math.max(b[1].ly?.pct ?? 0, b[1].bt?.pct ?? 0) -
        Math.max(a[1].ly?.pct ?? 0, a[1].bt?.pct ?? 0),
    );
  }, [matrix]);

  async function markAssessment(kind: string) {
    if (!examId) return;
    try {
      await publishClassAssessment({ classId, examId, kind, term: "" });
      toast("success", "Đã đánh dấu là bài kiểm tra định kỳ.");
      loadAssessments();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không lưu được.");
    }
  }

  if (exams.length === 0) {
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">
        Lớp chưa có lượt làm bài kiểm tra nào.
      </p>
    );
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-3">
        <BarChart3 size={18} className="text-blue-300" />
        <select
          value={examId ?? ""}
          onChange={(e) => setExamId(Number(e.target.value))}
          className="min-w-60 rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-sm text-white focus:border-primary focus:outline-none"
        >
          {exams.map((e) => (
            <option key={e.id} value={e.id}>
              {e.title}
            </option>
          ))}
        </select>
        {assessment ? (
          <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
            Bài KT định kỳ · {KIND_OPTIONS.find((k) => k.value === assessment.kind)?.label}
          </span>
        ) : (
          <select
            defaultValue=""
            onChange={(e) => e.target.value && markAssessment(e.target.value)}
            className="rounded-full border border-white/15 bg-[#0B1020] px-3 py-1.5 text-xs text-slate-300"
          >
            <option value="">+ Đánh dấu bài KT định kỳ…</option>
            {KIND_OPTIONS.map((k) => (
              <option key={k.value} value={k.value}>
                {k.label}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Tổng quan */}
      <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <Metric label="Lượt làm" value={overview ? String(overview.attempts) : "…"} />
        <Metric
          label="Điểm trung bình"
          value={overview ? overview.average.toLocaleString("vi-VN") : "…"}
        />
        <Metric label="Tỉ lệ đạt (≥5)" value={overview ? `${overview.passRate}%` : "…"} />
        <Metric
          label="Thời gian TB"
          value={
            overview
              ? `${Math.floor(overview.avgSeconds / 60)}′${String(overview.avgSeconds % 60).padStart(2, "0")}`
              : "…"
          }
        />
      </section>

      {overview && overview.attempts > 0 && (
        <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
          <p className="mb-3 text-sm font-semibold text-white">Phân bố điểm</p>
          <div className="flex items-end gap-1.5" style={{ height: 90 }}>
            {overview.distribution.map((n, i) => {
              const maxN = Math.max(...overview.distribution, 1);
              return (
                <div key={i} className="flex flex-1 flex-col items-center gap-1">
                  <span className="text-[10px] text-slate-500">{n || ""}</span>
                  <div
                    className={`w-full rounded-t ${i < 5 ? "bg-red-400/60" : "bg-blue-400/70"}`}
                    style={{ height: `${(n / maxN) * 64 + (n ? 4 : 0)}px` }}
                  />
                  <span className="text-[10px] text-slate-500">{i}</span>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Câu sai nhiều nhất */}
      <section>
        <h3 className="mb-3 font-display font-semibold text-white">Câu sai nhiều nhất</h3>
        {wrongest === null ? (
          <p className="text-sm text-slate-400">Đang tải…</p>
        ) : wrongest.length === 0 ? (
          <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-sm text-slate-500">
            Chưa có dữ liệu chi tiết từng câu (cần học sinh làm bài sau khi bật tính năng).
          </p>
        ) : (
          <div className="space-y-2">
            {wrongest.slice(0, 12).map((q) => (
              <div key={q.questionIndex} className="rounded-2xl border border-white/10 bg-[#0B1020]">
                <button
                  type="button"
                  onClick={() =>
                    setOpenQ((cur) => (cur === q.questionIndex ? null : q.questionIndex))
                  }
                  className="flex w-full items-center gap-3 p-4 text-left"
                >
                  <span className="min-w-0 flex-1">
                    <span className="block text-sm font-semibold text-white">
                      Câu {q.questionIndex + 1}
                      <span className="ml-2 font-normal text-slate-400">
                        {q.topic} · {formLabel(q.form)}
                      </span>
                    </span>
                  </span>
                  <span className="shrink-0 text-right">
                    <span
                      className={`font-mono text-base font-bold ${q.pct >= 60 ? "text-red-300" : q.pct >= 30 ? "text-amber-300" : "text-slate-300"}`}
                    >
                      {q.pct}%
                    </span>
                    <span className="ml-2 text-xs text-slate-500">
                      {q.wrong}/{q.total}
                    </span>
                  </span>
                  <ChevronDown
                    size={16}
                    className={`shrink-0 text-slate-500 transition-transform ${openQ === q.questionIndex ? "rotate-180" : ""}`}
                  />
                </button>
                {openQ === q.questionIndex && questions[q.questionIndex] && (
                  <div className="border-t border-white/10 p-4 text-sm text-slate-300">
                    <ContentHtml
                      html={questions[q.questionIndex].question}
                      className="exam-content block"
                    />
                    {questions[q.questionIndex].type === "multiple_choice" && (
                      <ul className="mt-2 space-y-1 text-xs">
                        {(questions[q.questionIndex] as { options: string[]; answer: number }).options.map(
                          (opt, oi) => (
                            <li
                              key={oi}
                              className={
                                oi ===
                                (questions[q.questionIndex] as { answer: number }).answer
                                  ? "text-emerald-300"
                                  : "text-slate-500"
                              }
                            >
                              {"ABCD"[oi]}. <ContentHtml html={opt} />
                            </li>
                          ),
                        )}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Ma trận chủ đề */}
      <section>
        <h3 className="mb-3 font-display font-semibold text-white">Chủ đề yếu của lớp</h3>
        {matrix === null ? (
          <p className="text-sm text-slate-400">Đang tải…</p>
        ) : topics.length === 0 ? (
          <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-sm text-slate-500">
            Chưa có dữ liệu chủ đề.
          </p>
        ) : (
          <div className="overflow-x-auto rounded-2xl border border-white/10">
            <table className="w-full min-w-[420px] text-sm">
              <thead className="bg-white/5 text-xs text-slate-400">
                <tr>
                  <th className="px-4 py-2 text-left font-medium">Chủ đề</th>
                  <th className="px-3 py-2 text-center font-medium">Lý thuyết</th>
                  <th className="px-3 py-2 text-center font-medium">Bài tập</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {topics.map(([topic, e]) => (
                  <tr key={topic}>
                    <td className="px-4 py-2 text-white">{topic}</td>
                    {[e.ly, e.bt].map((g, i) => (
                      <td key={i} className="px-3 py-2 text-center">
                        {g ? (
                          <span
                            className={`inline-block min-w-[3rem] rounded-md px-2 py-1 font-mono font-semibold ${heat(g.pct)}`}
                            title={`sai ${g.wrong}/${g.total}`}
                          >
                            {g.pct}%
                          </span>
                        ) : (
                          <span className="text-slate-600">—</span>
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-2 font-display text-2xl font-bold text-white">{value}</p>
    </div>
  );
}
