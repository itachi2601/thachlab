"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion } from "@/features/exams/types";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import ContentHtml from "@/components/exams/ContentHtml";
import {
  createQuestionTopic,
  fetchQuestionTopics,
  updateQuestionTopic,
  type QuestionTopic,
} from "@/services/analytics";
import { fetchChapters, fetchLessons } from "@/services/lessons";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { getSupabase } from "@/services/supabase";

const GRADES = ["10", "11", "12", "9"];
const input =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

export default function QuestionTopicsAdmin() {
  const toast = useToast();
  const [grade, setGrade] = useState("12");
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [newName, setNewName] = useState("");

  const reload = useCallback(() => {
    fetchQuestionTopics().then(setTopics).catch(() => setTopics([]));
  }, []);
  useEffect(reload, [reload]);
  useEffect(() => {
    fetchChapters().then(setChapters).catch(() => undefined);
    fetchLessons(true).then(setLessons).catch(() => undefined);
  }, []);

  const gradeTopics = topics.filter((t) => t.grade === grade);
  const lessonsByChapter = useMemo(() => {
    const m = new Map<number, Lesson[]>();
    for (const l of lessons) {
      const arr = m.get(l.chapter_id) ?? [];
      arr.push(l);
      m.set(l.chapter_id, arr);
    }
    return m;
  }, [lessons]);

  async function addTopic() {
    if (!newName.trim()) return;
    try {
      await createQuestionTopic({ grade, name: newName });
      setNewName("");
      reload();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không tạo được chủ đề.");
    }
  }

  async function patch(id: number, p: Parameters<typeof updateQuestionTopic>[1]) {
    try {
      await updateQuestionTopic(id, p);
      reload();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không lưu được.");
    }
  }

  return (
    <div className="space-y-8">
      <header>
        <h1 className="font-display text-2xl font-bold text-white">Chủ đề câu hỏi</h1>
        <p className="mt-1 text-sm text-slate-400">
          Danh mục chủ đề chuẩn hoá cho phần phân tích kết quả. Gắn mỗi chủ đề vào một bài học
          để nút &ldquo;Ôn lại&rdquo; của học sinh nhảy đúng chỗ.
        </p>
      </header>

      <div className="flex flex-wrap gap-2">
        {GRADES.map((g) => (
          <button
            key={g}
            onClick={() => setGrade(g)}
            className={`rounded-full border px-4 py-1.5 text-sm font-semibold ${
              grade === g
                ? "border-blue-400 bg-blue-500/15 text-blue-200"
                : "border-white/10 text-slate-400 hover:border-white/30"
            }`}
          >
            {g === "9" ? "KHTN 9" : `Lớp ${g}`}
          </button>
        ))}
      </div>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex flex-wrap gap-3">
          <input
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addTopic()}
            placeholder="Tên chủ đề mới, vd Nội năng"
            className={`${input} min-w-64 flex-1`}
          />
          <button
            onClick={addTopic}
            className="rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark"
          >
            + Thêm chủ đề
          </button>
        </div>

        <div className="mt-4 space-y-2">
          {gradeTopics.length === 0 && (
            <p className="text-sm text-slate-500">Lớp này chưa có chủ đề nào.</p>
          )}
          {gradeTopics.map((t) => (
            <div
              key={t.id}
              className="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 bg-white/[.02] px-4 py-3"
            >
              <input
                defaultValue={t.name}
                onBlur={(e) =>
                  e.target.value.trim() !== t.name && patch(t.id, { name: e.target.value })
                }
                className={`${input} min-w-48 flex-1`}
              />
              <select
                value={t.chapterId ?? ""}
                onChange={(e) =>
                  patch(t.id, {
                    chapterId: e.target.value ? Number(e.target.value) : null,
                    lessonId: null,
                  })
                }
                className={`${input} bg-[#0B1020]`}
              >
                <option value="">— Chương —</option>
                {chapters
                  .filter((c) => c.subjectCode === "vat-ly")
                  .map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.title}
                    </option>
                  ))}
              </select>
              <select
                value={t.lessonId ?? ""}
                onChange={(e) =>
                  patch(t.id, { lessonId: e.target.value ? Number(e.target.value) : null })
                }
                className={`${input} bg-[#0B1020]`}
              >
                <option value="">— Bài học (cho nút Ôn lại) —</option>
                {(t.chapterId ? lessonsByChapter.get(t.chapterId) ?? [] : lessons).map((l) => (
                  <option key={l.id} value={l.id}>
                    {l.title}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      </section>

      <ExamTagger grade={grade} topics={gradeTopics} onNeedTopic={reload} />
    </div>
  );
}

// ---------- Gắn nhãn chủ đề + loại cho từng câu của một đề ----------
function ExamTagger({
  grade,
  topics,
  onNeedTopic,
}: {
  grade: string;
  topics: QuestionTopic[];
  onNeedTopic: () => void;
}) {
  const toast = useToast();
  const [exams, setExams] = useState<{ id: number; title: string }[]>([]);
  const [examId, setExamId] = useState<number | null>(null);
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    getSupabase()
      .from("exams")
      .select("id, title")
      .eq("subject_code", "vat-ly")
      .order("created_at", { ascending: false })
      .then(({ data }) => setExams((data as { id: number; title: string }[]) ?? []));
  }, []);

  useEffect(() => {
    if (!examId) return;
    setDirty(false);
    getSupabase()
      .from("exams")
      .select("questions")
      .eq("id", examId)
      .single()
      .then(({ data }) => setQuestions((data?.questions as ExamQuestion[]) ?? []));
  }, [examId]);

  function setQ(i: number, patch: Partial<ExamQuestion>) {
    setQuestions((cur) => cur.map((q, qi) => (qi === i ? ({ ...q, ...patch } as ExamQuestion) : q)));
    setDirty(true);
  }

  async function save() {
    if (!examId) return;
    setBusy(true);
    const { error } = await getSupabase()
      .from("exams")
      .update({ questions })
      .eq("id", examId);
    setBusy(false);
    if (error) {
      toast("error", error.message);
      return;
    }
    toast("success", "Đã lưu nhãn chủ đề.");
    setDirty(false);
  }

  const tagged = questions.filter((q) => (q.topic ?? "").trim() && q.form).length;

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <h2 className="font-display font-semibold text-white">Gắn nhãn cho một đề</h2>
      <p className="mt-1 text-sm text-slate-400">
        Sửa chủ đề / loại cho từng câu (đề nhập bằng skill up-đề thường đã có sẵn nhãn).
      </p>

      <select
        value={examId ?? ""}
        onChange={(e) => setExamId(Number(e.target.value))}
        className={`${input} mt-4 min-w-72 bg-[#0B1020]`}
      >
        <option value="">— Chọn đề —</option>
        {exams.map((e) => (
          <option key={e.id} value={e.id}>
            {e.title}
          </option>
        ))}
      </select>

      {examId && (
        <>
          <div className="mt-4 flex items-center gap-3 text-sm">
            <span className="text-slate-400">
              Đã gắn {tagged}/{questions.length} câu
            </span>
            <button
              onClick={save}
              disabled={!dirty || busy}
              className="rounded-full bg-[#2563EB] px-5 py-1.5 text-sm font-semibold text-white disabled:opacity-40"
            >
              {busy ? "Đang lưu…" : "Lưu nhãn"}
            </button>
          </div>

          <div className="mt-4 space-y-2">
            {questions.map((q, i) => (
              <div
                key={i}
                className="grid gap-2 rounded-xl border border-white/10 bg-white/[.02] p-3 sm:grid-cols-[1fr_200px_150px]"
              >
                <div className="min-w-0 text-sm text-slate-300">
                  <span className="mr-1 font-semibold text-primary">Câu {i + 1}.</span>
                  <ContentHtml
                    html={(q.question || "").slice(0, 220)}
                    className="exam-content"
                  />
                </div>
                <select
                  value={q.topic ?? ""}
                  onChange={(e) => setQ(i, { topic: e.target.value } as Partial<ExamQuestion>)}
                  className={`${input} bg-[#0B1020]`}
                >
                  <option value="">— Chủ đề —</option>
                  {topics.map((t) => (
                    <option key={t.id} value={t.name}>
                      {t.name}
                    </option>
                  ))}
                  {(q.topic ?? "").trim() &&
                    !topics.some((t) => t.name === q.topic) && (
                      <option value={q.topic}>{q.topic} (chưa có trong danh mục)</option>
                    )}
                </select>
                <select
                  value={q.form ?? ""}
                  onChange={(e) =>
                    setQ(i, { form: e.target.value } as Partial<ExamQuestion>)
                  }
                  className={`${input} bg-[#0B1020]`}
                >
                  <option value="">— Loại —</option>
                  <option value="ly_thuyet">{QUESTION_FORM_LABELS.ly_thuyet}</option>
                  <option value="bai_tap">{QUESTION_FORM_LABELS.bai_tap}</option>
                </select>
              </div>
            ))}
          </div>
          <p className="mt-3 text-xs text-slate-500">
            Chủ đề chưa có trong danh mục lớp {grade === "9" ? "KHTN 9" : grade}? Thêm ở khung
            trên rồi{" "}
            <button onClick={onNeedTopic} className="text-primary hover:underline">
              tải lại
            </button>
            .
          </p>
        </>
      )}
    </section>
  );
}
