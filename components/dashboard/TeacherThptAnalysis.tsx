"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { BarChart3, ChevronDown, Tv } from "lucide-react";
import { AVCN_CLASS_SLUG, AVCN_SUBJECT_CODE, expandClassIdsByGrade, type ClassStudent } from "@/services/classes";
import type { SchoolClass } from "@/features/exams/types";
import type { ExamQuestion } from "@/features/exams/types";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { fetchClassExamResults } from "@/services/class-results";
import { getSupabase } from "@/services/supabase";
import {
  fetchClassAssessments,
  fetchClassTopicMatrix,
  fetchExamOverview,
  fetchExamReviewData,
  type ReviewQuestionStat,
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

async function fetchAvcnLessonExams(isAvcn: boolean): Promise<{ id: number; title: string }[]> {
  if (!isAvcn) return [];
  try {
    const sb = getSupabase();
    const { data: items } = await sb
      .from("lesson_items")
      .select("exam_ids, lessons!inner(chapters!inner(subject_code))")
      .in("kind", ["luyen_tap", "kiem_tra"])
      .eq("lessons.chapters.subject_code", AVCN_SUBJECT_CODE);
    const ids = Array.from(new Set((items ?? []).flatMap((i: { exam_ids: number[] | null }) => i.exam_ids ?? [])));
    if (ids.length === 0) return [];
    const { data } = await sb.from("exams").select("id, title").in("id", ids).order("id", { ascending: false });
    return (data ?? []) as { id: number; title: string }[];
  } catch {
    return [];
  }
}

export default function TeacherThptAnalysis({
  classId,
  students,
  classes,
}: {
  classId: number;
  students: ClassStudent[];
  classes: SchoolClass[];
}) {
  const toast = useToast();
  const { profile } = useAuth();
  // Trợ giảng không có khu vực THPT nên bị /dashboard-thpt/chua-bai chặn — có trang chữa bài riêng.
  const reviewBase = profile?.role === "tro_giang" ? "/tro-giang/chua-bai" : "/dashboard-thpt/chua-bai";
  const studentIds = useMemo(() => students.map((s) => s.id), [students]);

  const [exams, setExams] = useState<{ id: number; title: string; own: boolean; done: number }[]>([]);
  const [search, setSearch] = useState("");
  const [examId, setExamId] = useState<number | null>(null);
  const [assessments, setAssessments] = useState<ClassAssessment[]>([]);

  const [overview, setOverview] = useState<ExamOverview | null>(null);
  const [wrongest, setWrongest] = useState<WrongestQuestion[] | null>(null);
  const [matrix, setMatrix] = useState<TopicGap[] | null>(null);
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [openQ, setOpenQ] = useState<number | null>(null);
  const [reviewStats, setReviewStats] = useState<ReviewQuestionStat[]>([]);

  const loadAssessments = useCallback(() => {
    fetchClassAssessments(classId).then(setAssessments).catch(() => setAssessments([]));
  }, [classId]);

  // Đề của lớp = đề gán cho cùng khối (exam_classes) + đề KT định kỳ; đề HS tự làm ngoài khối xếp vào "khác".
  useEffect(() => {
    loadAssessments();
    let cancelled = false;
    const classIds = expandClassIdsByGrade([classId], classes) ?? [classId];
    Promise.all([
      getSupabase()
        .from("exam_classes")
        .select("exam_id, exams(title)")
        .in("class_id", classIds),
      fetchClassExamResults(studentIds).catch(() => []),
      fetchAvcnLessonExams(classes.find((c) => c.id === classId)?.slug === AVCN_CLASS_SLUG),
    ])
      .then(([assigned, rows, avcnExams]) => {
        if (cancelled) return;
        const submitted = new Map<number, Set<string>>();
        const titles = new Map<number, string>();
        rows.forEach((r) => {
          const set = submitted.get(r.exam_id) ?? new Set<string>();
          set.add(r.student_id);
          submitted.set(r.exam_id, set);
          titles.set(r.exam_id, r.exams?.title ?? `Đề #${r.exam_id}`);
        });
        const mine = new Map<number, string>();
        for (const a of (assigned.data ?? []) as { exam_id: number; exams: { title: string } | { title: string }[] | null }[]) {
          const t = Array.isArray(a.exams) ? a.exams[0]?.title : a.exams?.title;
          mine.set(a.exam_id, t ?? titles.get(a.exam_id) ?? `Đề #${a.exam_id}`);
        }
        // Đề AVCN không gán lớp (lớp vào tự do) nên lấy theo mục Luyện tập/Kiểm tra của bài, chưa ai nộp vẫn hiện.
        avcnExams.forEach((e) => mine.set(e.id, e.title));
        const toItem = (id: number, title: string, own: boolean) => ({ id, title, own, done: submitted.get(id)?.size ?? 0 });
        const list = [
          ...[...mine.entries()].map(([id, t]) => toItem(id, t, true)),
          ...[...titles.entries()].filter(([id]) => !mine.has(id)).map(([id, t]) => toItem(id, t, false)),
        ];
        setExams(list);
        setExamId((cur) => (cur !== null && list.some((e) => e.id === cur) ? cur : list.find((e) => e.own)?.id ?? list[0]?.id ?? null));
      })
      .catch(() => setExams([]));
    return () => {
      cancelled = true;
    };
  }, [studentIds, classId, classes, loadAssessments]);

  useEffect(() => {
    if (!examId) return;
    setOverview(null);
    setWrongest(null);
    setMatrix(null);
    setOpenQ(null);
    fetchExamOverview(examId, studentIds).then(setOverview).catch(() => undefined);
    fetchWrongestQuestions(examId, studentIds).then(setWrongest).catch(() => setWrongest([]));
    fetchClassTopicMatrix(studentIds, examId).then(setMatrix).catch(() => setMatrix([]));
    setReviewStats([]);
    fetchExamReviewData(examId, studentIds).then((d) => setReviewStats(d.stats)).catch(() => setReviewStats([]));
    getSupabase()
      .from("exams")
      .select("questions")
      .eq("id", examId)
      .single()
      .then(({ data }) => setQuestions((data?.questions as ExamQuestion[]) ?? []));
  }, [examId, studentIds]);

  const assessment = assessments.find((a) => a.examId === examId) ?? null;
  const assessmentIds = useMemo(() => new Set(assessments.map((a) => a.examId)), [assessments]);
  const filtered = useMemo(() => {
    const kw = search.trim().toLowerCase();
    return kw ? exams.filter((e) => e.title.toLowerCase().includes(kw) || String(e.id) === kw) : exams;
  }, [exams, search]);
  const optionLabel = (e: { id: number; title: string; done: number }) => {
    const tag = assessmentIds.has(e.id) ? "[Định kỳ] " : "";
    return `${tag}${e.title} · ${e.done}/${students.length} nộp`;
  };
  const ownList = filtered.filter((e) => e.own);
  const otherList = filtered.filter((e) => !e.own);

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
        Chưa có đề nào gán cho khối này và lớp chưa có lượt làm bài nào.
      </p>
    );
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-3">
        <BarChart3 size={18} className="text-blue-300" />
        {exams.length > 8 && (
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Tìm đề…"
            aria-label="Tìm đề"
            className="w-36 rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-primary focus:outline-none"
          />
        )}
        <select
          value={examId ?? ""}
          onChange={(e) => setExamId(Number(e.target.value))}
          className="min-w-60 max-w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white focus:border-primary focus:outline-none"
        >
          {ownList.length > 0 && (
            <optgroup label="Đề của khối này">
              {ownList.map((e) => (
                <option key={e.id} value={e.id}>{optionLabel(e)}</option>
              ))}
            </optgroup>
          )}
          {otherList.length > 0 && (
            <optgroup label="Đề khác lớp đã làm (ngoài khối)">
              {otherList.map((e) => (
                <option key={e.id} value={e.id}>{optionLabel(e)}</option>
              ))}
            </optgroup>
          )}
        </select>
        {assessment ? (
          <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
            Bài KT định kỳ · {KIND_OPTIONS.find((k) => k.value === assessment.kind)?.label}
          </span>
        ) : (
          <select
            defaultValue=""
            onChange={(e) => e.target.value && markAssessment(e.target.value)}
            className="rounded-full border border-white/15 bg-panel px-3 py-1.5 text-xs text-slate-300"
          >
            <option value="">+ Đánh dấu bài KT định kỳ…</option>
            {KIND_OPTIONS.map((k) => (
              <option key={k.value} value={k.value}>
                {k.label}
              </option>
            ))}
          </select>
        )}
        {examId && (
          <a
            href={`${reviewBase}?exam=${examId}&class=${classId}`}
            target="_blank"
            rel="noreferrer"
            className="ml-auto inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
          >
            <Tv size={16} /> Trình chiếu chữa bài
          </a>
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
        <section className="rounded-2xl border border-white/10 bg-panel p-5">
          <p className="mb-4 text-sm font-semibold text-white">Phổ điểm</p>
          <div className="flex items-end gap-2" style={{ height: 180 }}>
            {overview.distribution.map((n, i) => {
              const maxN = Math.max(...overview.distribution, 1);
              const barHeight = n ? Math.max((n / maxN) * 138, 8) : 0;
              const isPass = i >= 5;
              return (
                <div
                  key={i}
                  className="flex h-full flex-1 flex-col items-center justify-end gap-2"
                  title={`${n} bài · điểm ${i}–${i + 1}`}
                >
                  <span className="text-[12px] font-medium tabular-nums text-slate-400">{n || ""}</span>
                  <div
                    className={`w-2.5 rounded-full transition-[height] duration-300 sm:w-3 ${
                      isPass
                        ? "bg-gradient-to-t from-sky-600 via-sky-400 to-cyan-300 shadow-[0_0_10px_rgba(56,189,248,0.4)]"
                        : "bg-gradient-to-t from-rose-600 via-rose-500 to-rose-400 shadow-[0_0_10px_rgba(244,63,94,0.35)]"
                    }`}
                    style={{ height: `${barHeight}px` }}
                  />
                  <span className="text-[12px] font-medium text-slate-500">{i}</span>
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
          <p className="rounded-2xl border border-white/10 bg-panel p-5 text-sm text-slate-500">
            Chưa có dữ liệu chi tiết từng câu (cần học sinh làm bài sau khi bật tính năng).
          </p>
        ) : (
          <div className="space-y-2">
            {wrongest.slice(0, 12).map((q) => (
              <div key={q.questionIndex} className="rounded-2xl border border-white/10 bg-panel">
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
                    <a
                      href={`${reviewBase}?exam=${examId}&class=${classId}&q=${q.questionIndex}`}
                      target="_blank"
                      rel="noreferrer"
                      className="mb-3 inline-flex items-center gap-2 rounded-full bg-primary px-3 py-1.5 text-xs font-semibold text-white hover:bg-primary-dark"
                    >
                      <Tv size={14} /> Chiếu câu này
                    </a>
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
                    <AnswerSpread question={questions[q.questionIndex]} stat={reviewStats[q.questionIndex]} />
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
          <p className="rounded-2xl border border-white/10 bg-panel p-5 text-sm text-slate-500">
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
    <div className="rounded-2xl border border-white/10 bg-panel p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-2 font-display text-2xl font-bold text-white">{value}</p>
    </div>
  );
}

/**
 * Lớp chọn gì: phân bố đáp án (trắc nghiệm) hoặc tỉ lệ đúng từng ý (đúng–sai).
 * Một phương án sai được ≥30% lớp chọn = quan niệm sai chung, đáng dạy lại trực tiếp.
 */
function AnswerSpread({ question, stat }: { question: ExamQuestion; stat?: ReviewQuestionStat }) {
  if (!stat || stat.attempted < 3) return null;
  if (question.type === "multiple_choice" && stat.optionCounts) {
    const answer = (question as { answer: number }).answer;
    const counts = stat.optionCounts;
    const topWrong = counts.reduce((best, n, i) => (i !== answer && n > (counts[best] ?? -1) ? i : best), answer === 0 ? 1 : 0);
    const misconception = counts[topWrong] / stat.attempted >= 0.3 ? topWrong : -1;
    return (
      <div className="mt-4 space-y-1.5 border-t border-white/10 pt-3">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Lớp đã chọn ({stat.attempted} em)</p>
        {counts.map((n, i) => {
          const p = Math.round((n / stat.attempted) * 100);
          const right = i === answer;
          return (
            <div key={i} className="flex items-center gap-2 text-xs">
              <span className={`w-5 shrink-0 font-semibold ${right ? "text-emerald-300" : "text-slate-300"}`}>{"ABCD"[i]}</span>
              <span className="h-2.5 flex-1 overflow-hidden rounded-full bg-white/10">
                <span className={`block h-full rounded-full ${right ? "bg-emerald-400" : i === misconception ? "bg-red-400" : "bg-slate-500"}`} style={{ width: `${p}%` }} />
              </span>
              <span className="w-20 shrink-0 text-right tabular-nums text-slate-300">{p}% · {n} em</span>
            </div>
          );
        })}
        {misconception >= 0 && (
          <p className="pt-1 text-xs text-red-300">
            ⚠ {Math.round((counts[misconception] / stat.attempted) * 100)}% lớp cùng chọn {"ABCD"[misconception]} — có thể là một quan niệm sai chung, nên hỏi lại vì sao chọn.
          </p>
        )}
      </div>
    );
  }
  if (question.type === "true_false" && stat.statementCorrectN) {
    const wrongIdx = stat.statementCorrectN.map((n, i) => ({ i, p: Math.round((n / stat.attempted) * 100) }));
    return (
      <div className="mt-4 space-y-1.5 border-t border-white/10 pt-3">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Tỉ lệ đúng từng ý ({stat.attempted} em)</p>
        {wrongIdx.map(({ i, p }) => (
          <div key={i} className="flex items-center gap-2 text-xs">
            <span className="w-5 shrink-0 font-semibold text-slate-300">{"abcd"[i]})</span>
            <span className="h-2.5 flex-1 overflow-hidden rounded-full bg-white/10">
              <span className={`block h-full rounded-full ${p < 50 ? "bg-red-400" : "bg-emerald-400"}`} style={{ width: `${p}%` }} />
            </span>
            <span className="w-20 shrink-0 text-right tabular-nums text-slate-300">{p}% đúng</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
}
