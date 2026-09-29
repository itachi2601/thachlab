"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useToast } from "@/components/ui/Toast";
import type { ExamQuestion } from "@/features/exams/types";
import { QUESTION_FORM_LABELS } from "@/features/exams/types";
import ContentHtml from "@/components/exams/ContentHtmlLazy";
import {
  createQuestionTopic,
  deleteQuestionTopic,
  fetchQuestionTopics,
  lessonTopics,
  outcomesOf,
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
  const parents = lessonTopics(gradeTopics).sort(
    (a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi"),
  );
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

  async function addOutcome(parent: QuestionTopic, name: string) {
    const siblings = outcomesOf(topics, parent.id);
    try {
      await createQuestionTopic({
        grade,
        name,
        chapterId: parent.chapterId,
        lessonId: parent.lessonId,
        parentId: parent.id,
        sortOrder: parent.sortOrder + siblings.length + 1,
      });
      reload();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không thêm được yêu cầu cần đạt.");
    }
  }

  async function remove(t: QuestionTopic) {
    if (!confirm(`Xoá "${t.name}"? Các mục phụ đạo gắn với nó cũng mất.`)) return;
    try {
      await deleteQuestionTopic(t.id);
      reload();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không xoá được.");
    }
  }

  return (
    <div className="space-y-8">
      <header>
        <p className="admin-lead" style={{ marginTop: 0 }}>
          Hai tầng: <strong className="text-slate-200">bài học</strong> → các{" "}
          <strong className="text-slate-200">yêu cầu cần đạt</strong> trong bài. Câu hỏi nên gắn
          vào yêu cầu cần đạt cho mịn; mục phụ đạo vẫn gom lên tầng bài để đủ số câu mà kết luận.
          Bài học chọn ở tầng cha quyết định nút &ldquo;Ôn lại&rdquo; của học sinh.
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

      <section className="admin-card">
        <div className="flex flex-wrap gap-3">
          <input
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addTopic()}
            placeholder="Tên chủ đề tầng bài, vd Nội năng. Định luật 1 nhiệt động lực học"
            className={`${input} min-w-64 flex-1`}
          />
          <button
            onClick={addTopic}
            className="admin-btn admin-btn--primary"
          >
            + Thêm chủ đề bài học
          </button>
        </div>

        <div className="mt-4 space-y-3">
          {parents.length === 0 && (
            <p className="text-sm text-slate-500">Lớp này chưa có chủ đề nào.</p>
          )}
          {parents.map((t) => (
            <TopicNode
              key={t.id}
              topic={t}
              outcomes={outcomesOf(gradeTopics, t.id)}
              chapters={chapters}
              lessons={lessons}
              lessonsByChapter={lessonsByChapter}
              onPatch={patch}
              onAddOutcome={addOutcome}
              onRemove={remove}
            />
          ))}
        </div>
      </section>

      <ExamTagger grade={grade} topics={gradeTopics} onNeedTopic={reload} />
    </div>
  );
}

// ---------- Một bài học + các yêu cầu cần đạt của nó ----------
function TopicNode({
  topic,
  outcomes,
  chapters,
  lessons,
  lessonsByChapter,
  onPatch,
  onAddOutcome,
  onRemove,
}: {
  topic: QuestionTopic;
  outcomes: QuestionTopic[];
  chapters: Chapter[];
  lessons: Lesson[];
  lessonsByChapter: Map<number, Lesson[]>;
  onPatch: (id: number, p: Parameters<typeof updateQuestionTopic>[1]) => void;
  onAddOutcome: (parent: QuestionTopic, name: string) => void;
  onRemove: (t: QuestionTopic) => void;
}) {
  const [draft, setDraft] = useState("");

  function submit() {
    if (!draft.trim()) return;
    onAddOutcome(topic, draft);
    setDraft("");
  }

  return (
    <div className="admin-card">
      <div className="flex flex-wrap items-center gap-3">
        <input
          defaultValue={topic.name}
          onBlur={(e) =>
            e.target.value.trim() !== topic.name && onPatch(topic.id, { name: e.target.value })
          }
          className={`${input} min-w-48 flex-1 font-semibold`}
        />
        <select
          value={topic.chapterId ?? ""}
          onChange={(e) =>
            onPatch(topic.id, {
              chapterId: e.target.value ? Number(e.target.value) : null,
              lessonId: null,
            })
          }
          className={`${input} bg-panel`}
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
          value={topic.lessonId ?? ""}
          onChange={(e) =>
            onPatch(topic.id, { lessonId: e.target.value ? Number(e.target.value) : null })
          }
          className={`${input} bg-panel`}
        >
          <option value="">— Bài học (cho nút Ôn lại) —</option>
          {(topic.chapterId ? lessonsByChapter.get(topic.chapterId) ?? [] : lessons).map((l) => (
            <option key={l.id} value={l.id}>
              {l.title}
            </option>
          ))}
        </select>
      </div>

      <div className="mt-3 space-y-1.5 border-l border-white/10 pl-4">
        {outcomes.length === 0 && (
          <p className="text-xs text-slate-500">
            Chưa tách yêu cầu cần đạt — câu hỏi của bài này chỉ gắn được nhãn ở mức cả bài.
          </p>
        )}
        {outcomes.map((o) => (
          <div key={o.id} className="flex items-center gap-2">
            <span className="text-xs text-slate-600">└</span>
            <input
              defaultValue={o.name}
              onBlur={(e) =>
                e.target.value.trim() !== o.name && onPatch(o.id, { name: e.target.value })
              }
              className={`${input} flex-1 text-[13px]`}
            />
            <button
              onClick={() => onRemove(o)}
              title="Xoá yêu cầu cần đạt"
              className="rounded-lg border border-white/10 px-2 py-1 text-xs text-slate-400 hover:border-rose-400/40 hover:text-rose-300"
            >
              Xoá
            </button>
          </div>
        ))}
        <div className="flex items-center gap-2 pt-1">
          <span className="text-xs text-slate-600">+</span>
          <input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && submit()}
            placeholder="Thêm yêu cầu cần đạt, vd Viết phương trình dao động điều hoà"
            className={`${input} flex-1 text-[13px]`}
          />
          <button
            onClick={submit}
            className="admin-chip"
          >
            Thêm
          </button>
        </div>
      </div>
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
  // Nhóm theo bài để chọn nhanh: mở một bài ra là thấy các yêu cầu cần đạt của bài đó.
  const grouped = useMemo(
    () =>
      lessonTopics(topics)
        .sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi"))
        .map((parent) => ({ parent, outcomes: outcomesOf(topics, parent.id) })),
    [topics],
  );
  // Câu còn gắn ở mức cả bài trong khi bài đó đã tách yêu cầu cần đạt.
  const coarseNames = new Set(
    grouped.filter((g) => g.outcomes.length > 0).map((g) => g.parent.name),
  );
  const coarseCount = questions.filter((q) => coarseNames.has((q.topic ?? "").trim())).length;

  return (
    <section className="admin-card">
      <h2 className="admin-h2">Gắn nhãn cho một đề</h2>
      <p className="mt-1 text-sm text-slate-400">
        Sửa chủ đề / loại cho từng câu (đề nhập bằng skill up-đề thường đã có sẵn nhãn).
        Chọn đúng <strong className="text-slate-300">yêu cầu cần đạt</strong> trong bài thay vì
        để ở mức cả bài — thầy mới biết em hổng phần nào.
      </p>

      <select
        value={examId ?? ""}
        onChange={(e) => setExamId(Number(e.target.value))}
        className={`${input} mt-4 min-w-72 bg-panel`}
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
              {coarseCount > 0 && (
                <span className="text-amber-300">
                  {" "}
                  · {coarseCount} câu mới ở mức cả bài
                </span>
              )}
            </span>
            <button
              onClick={save}
              disabled={!dirty || busy}
              className="rounded-full bg-primary px-5 py-1.5 text-sm font-semibold text-white disabled:opacity-40"
            >
              {busy ? "Đang lưu…" : "Lưu nhãn"}
            </button>
          </div>

          <div className="mt-4 space-y-2">
            {questions.map((q, i) => (
              <div
                key={i}
                className="grid gap-2 admin-card sm:grid-cols-[1fr_200px_150px]"
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
                  className={`${input} bg-panel`}
                >
                  <option value="">— Chủ đề —</option>
                  {grouped.map((g) => (
                    <optgroup key={g.parent.id} label={g.parent.name}>
                      {g.outcomes.length === 0 ? (
                        <option value={g.parent.name}>{g.parent.name} (cả bài)</option>
                      ) : (
                        <>
                          {g.outcomes.map((o) => (
                            <option key={o.id} value={o.name}>
                              {o.name}
                            </option>
                          ))}
                          <option value={g.parent.name}>— cả bài —</option>
                        </>
                      )}
                    </optgroup>
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
                  className={`${input} bg-panel`}
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
