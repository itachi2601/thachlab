"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { CheckCircle2 } from "lucide-react";
import ClassPicker from "@/components/admin/ClassPicker";
import ExamSection, { type ExamSectionSeed, type TopicGroup } from "@/components/admin/ExamSection";
import { MissingFigureNotice } from "@/components/admin/MissingFigureNotice";
import { useToast } from "@/components/ui/Toast";
import { canonicalizeQuestionTopics, type Difficulty, type ExamQuestion, type SchoolClass } from "@/features/exams/types";
import { fetchQuestionTopics, lessonTopics, outcomesOf, type QuestionTopic } from "@/services/analytics";
import { classGrade, fetchClasses, setItemClasses } from "@/services/classes";
import { BUNDLE_SCHEMA, validateBundle, type LessonBundle } from "@/services/lesson-import";
import { questionsMissingFigure } from "@/services/question-figures";
import { getSupabase } from "@/services/supabase";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const selectCls = `${inputCls} bg-panel`;
const pageSize = 12;

interface ExamListRow {
  id: number;
  title: string;
  published: boolean;
  duration_minutes: number;
  question_count: number;
  created_at: string;
  classIds: number[];
}

interface FullExam {
  id: number;
  title: string;
  published: boolean;
  duration_minutes: number;
  topic: string;
  difficulty: Difficulty;
  subject_code: string;
  questions: ExamQuestion[];
  pass_score: number | null;
  cnc_key: string | null;
  created_at: string;
  classIds: number[];
}

function fmtDate(iso: string): string {
  return new Date(iso).toLocaleDateString("vi-VN");
}

/** Trang "Sửa đề đã đăng" — tìm một đề có sẵn trong `exams`, sửa trực tiếp nội dung/đáp án/nhãn
 * rồi lưu đè lên đúng id đó, nên mọi bài học / mục đã gắn đề này không cần đổi gì. */
export default function ExamLibraryAdmin() {
  const toast = useToast();

  const [classes, setClasses] = useState<SchoolClass[]>([]);
  useEffect(() => {
    fetchClasses().then(setClasses);
  }, []);
  const classById = useMemo(() => new Map(classes.map((c) => [c.id, c])), [classes]);
  const grades = useMemo(
    () =>
      Array.from(new Set(classes.map((c) => classGrade(c.name)).filter((g): g is string => !!g))).sort((a, b) =>
        a.localeCompare(b, "vi", { numeric: true }),
      ),
    [classes],
  );
  function classNames(ids: number[]): string {
    return ids
      .map((id) => classById.get(id)?.name)
      .filter((n): n is string => !!n)
      .join(", ");
  }

  // ----- Tìm đề -----
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("all");
  const [page, setPage] = useState(0);
  const [listRetry, setListRetry] = useState(0);
  const [result, setResult] = useState<{ rows: ExamListRow[]; count: number; key: string } | null>(null);
  const [failure, setFailure] = useState<{ key: string; message: string } | null>(null);
  const requestKey = JSON.stringify([search, status, page, listRetry]);

  useEffect(() => {
    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        let q = getSupabase()
          .from("exams")
          .select("id, title, published, duration_minutes, question_count, created_at, exam_classes(class_id)", { count: "exact" });
        const term = search.trim();
        if (/^#?\d+$/.test(term)) q = q.eq("id", Number(term.replace("#", "")));
        else if (term) q = q.ilike("title", `%${term.replace(/[\\%_]/g, "\\$&")}%`);
        if (status !== "all") q = q.eq("published", status === "published");
        const { data, count: total, error } = await q
          .order("created_at", { ascending: false })
          .range(page * pageSize, (page + 1) * pageSize - 1);
        if (error) throw error;
        if (cancelled) return;
        const rows = (data ?? []).map((r) => ({
          id: r.id,
          title: r.title,
          published: r.published,
          duration_minutes: r.duration_minutes,
          question_count: r.question_count,
          created_at: r.created_at,
          classIds: ((r.exam_classes as { class_id: number }[] | null) ?? []).map((c) => c.class_id),
        }));
        setResult({ rows, count: total ?? 0, key: requestKey });
        setFailure(null);
      } catch (e) {
        if (!cancelled)
          setFailure({ key: requestKey, message: e instanceof Error ? e.message : "Không tải được danh sách đề." });
      }
    }, 250);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [search, status, page, listRetry, requestKey]);

  const listError = failure?.key === requestKey ? failure.message : null;
  const listBusy = result?.key !== requestKey && !listError;
  const rows = result?.key === requestKey ? result.rows : [];
  const count = result?.key === requestKey ? result.count : 0;
  const pages = Math.max(1, Math.ceil(count / pageSize));

  // ----- Đề đang chọn để sửa -----
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [full, setFull] = useState<FullExam | null>(null);
  const [loadingFull, setLoadingFull] = useState(false);
  const [seed, setSeed] = useState<ExamSectionSeed | null>(null);
  const [gradeOverride, setGradeOverride] = useState<string | null>(null);
  const [publishedInput, setPublishedInput] = useState(false);
  const [passScoreInput, setPassScoreInput] = useState("");
  const [classIdsInput, setClassIdsInput] = useState<number[]>([]);
  const [examBundle, setExamBundle] = useState<LessonBundle | null>(null);
  const [saving, setSaving] = useState(false);
  const [figureAckFor, setFigureAckFor] = useState<LessonBundle | null>(null);

  const seedCounter = useRef(0);
  async function selectExam(id: number) {
    if (loadingFull) return;
    setSelectedId(id);
    setLoadingFull(true);
    setFull(null);
    setExamBundle(null);
    setFigureAckFor(null);
    try {
      const [{ data, error }, { data: classRows }] = await Promise.all([
        getSupabase().from("exams").select("*").eq("id", id).single(),
        getSupabase().from("exam_classes").select("class_id").eq("exam_id", id),
      ]);
      if (error || !data) throw new Error(error?.message ?? "Không tải được đề.");
      const row: FullExam = {
        id: data.id,
        title: data.title,
        published: data.published,
        duration_minutes: data.duration_minutes,
        topic: data.topic ?? "",
        difficulty: (data.difficulty ?? "") as Difficulty,
        subject_code: data.subject_code ?? "vat-ly",
        questions: (data.questions ?? []) as ExamQuestion[],
        pass_score: data.pass_score ?? null,
        cnc_key: data.cnc_key ?? null,
        created_at: data.created_at,
        classIds: (classRows ?? []).map((r) => r.class_id as number),
      };
      setFull(row);
      setPublishedInput(row.published);
      setPassScoreInput(row.pass_score != null ? String(row.pass_score) : "");
      setClassIdsInput(row.classIds);
      setGradeOverride(null);
      const bundle: LessonBundle = {
        schema: BUNDLE_SCHEMA,
        theory_html: "",
        worked_examples: [],
        exam: {
          title: row.title,
          topic: row.topic || undefined,
          difficulty: row.difficulty || "",
          duration_minutes: row.duration_minutes,
          subject_code: row.subject_code,
          questions: row.questions,
        },
      };
      setExamBundle(bundle);
      seedCounter.current += 1;
      setSeed({ token: seedCounter.current, bundle });
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không tải được đề.");
      setSelectedId(null);
    } finally {
      setLoadingFull(false);
    }
  }

  const grade = gradeOverride ?? (full ? classGrade(classById.get(full.classIds[0] ?? -1)?.name ?? "") : null);

  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  useEffect(() => {
    if (!grade) return;
    fetchQuestionTopics(grade)
      .then(setTopics)
      .catch(() => setTopics([]));
  }, [grade]);
  // `topics` có thể còn giữ dữ liệu khối cũ trong lúc chờ tải khối mới — lọc theo `grade`
  // ngay dưới đây nên không cần tự xoá state khi `grade` tạm thời rỗng.
  const catalogNames = useMemo(() => topics.filter((t) => t.grade === grade).map((t) => t.name), [topics, grade]);
  const topicGroups = useMemo<TopicGroup[]>(() => {
    const parents = lessonTopics(topics.filter((t) => t.grade === grade));
    return parents
      .sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi"))
      .map((p) => ({ parent: p, names: outcomesOf(topics, p.id).map((o) => o.name) }))
      .filter((g) => g.names.length > 0);
  }, [topics, grade]);

  const questions = examBundle?.exam.questions ?? [];
  const check = examBundle ? validateBundle(examBundle) : null;
  const missingFigure = questionsMissingFigure(questions);
  const figureAck = figureAckFor !== null && figureAckFor === examBundle;
  const setFigureAck = (v: boolean) => setFigureAckFor(v ? examBundle : null);
  const canSave =
    !!examBundle &&
    !!full &&
    !!check?.ok &&
    questions.length > 0 &&
    !saving &&
    !!examBundle.exam.title.trim() &&
    (missingFigure.length === 0 || figureAck);

  async function save() {
    if (!examBundle || !full) return;
    setSaving(true);
    try {
      const supabase = getSupabase();
      const passScoreValue = passScoreInput.trim() !== "" ? Number(passScoreInput) : null;
      const payload = {
        title: examBundle.exam.title.trim(),
        duration_minutes: examBundle.exam.duration_minutes ?? full.duration_minutes,
        subject_code: examBundle.exam.subject_code || full.subject_code,
        topic: examBundle.exam.topic?.trim() || "",
        difficulty: examBundle.exam.difficulty ?? "",
        questions: canonicalizeQuestionTopics(examBundle.exam.questions, catalogNames),
        published: publishedInput,
        pass_score: passScoreValue,
      };
      let res = await supabase.from("exams").update(payload).eq("id", full.id);
      // pass_score có thể là cột mới chưa chạy migration ở một số môi trường — lùi về không có ngưỡng.
      if (res.error) {
        const { pass_score, ...rest } = payload;
        void pass_score;
        res = await supabase.from("exams").update(rest).eq("id", full.id);
      }
      if (res.error) throw new Error(res.error.message);
      await setItemClasses("exam_classes", "exam_id", full.id, classIdsInput);
      toast("success", "Đã lưu thay đổi.");
      setFull({ ...full, ...payload, pass_score: passScoreValue, classIds: classIdsInput });
      setResult((old) =>
        old
          ? {
              ...old,
              rows: old.rows.map((r) =>
                r.id === full.id
                  ? {
                      ...r,
                      title: payload.title,
                      duration_minutes: payload.duration_minutes,
                      published: payload.published,
                      question_count: payload.questions.length,
                      classIds: classIdsInput,
                    }
                  : r,
              ),
            }
          : old,
      );
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không lưu được.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <p className="admin-lead" style={{ marginTop: 0 }}>
          Tìm một đề đã đăng, sửa trực tiếp nội dung, đáp án, lời giải hoặc nhãn Chủ đề/Dạng của từng câu, rồi bấm Lưu.
          Đề vẫn giữ nguyên mã số nên mọi bài học đã gắn đề này không cần đổi gì.
        </p>
      </header>

      <section className="space-y-3 rounded-2xl border border-white/10 bg-white/5 p-4">
        <div className="flex flex-wrap gap-2">
          <input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(0);
            }}
            placeholder="Tìm tên đề hoặc mã, ví dụ #123…"
            className={`${inputCls} min-w-0 flex-1 basis-64`}
          />
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(0);
            }}
            className={`${selectCls} w-auto`}
          >
            <option value="all">Tất cả trạng thái</option>
            <option value="published">Đã xuất bản</option>
            <option value="draft">Bản nháp</option>
          </select>
        </div>

        <div aria-live="polite" className="text-xs text-slate-400">
          {listBusy ? "Đang tìm…" : listError ? "Không tải được danh sách" : `${count} đề · Mới nhất trước`}
        </div>
        {listError && (
          <p role="alert" className="text-sm text-red-300">
            {listError}{" "}
            <button type="button" onClick={() => setListRetry((n) => n + 1)} className="underline">
              Thử lại
            </button>
          </p>
        )}
        {!listBusy && !listError && rows.length === 0 && <p className="py-6 text-center text-sm text-slate-400">Không có đề phù hợp.</p>}

        <div className="divide-y divide-white/10 overflow-hidden rounded-xl border border-white/10">
          {rows.map((r) => (
            <button
              key={r.id}
              type="button"
              onClick={() => selectExam(r.id)}
              className={`flex w-full flex-wrap items-center gap-3 px-3 py-2.5 text-left text-sm hover:bg-white/5 ${
                selectedId === r.id ? "bg-primary/10" : ""
              }`}
            >
              <span className="min-w-0 flex-1">
                <span className="block truncate text-slate-100">{r.title}</span>
                <span className="block text-xs text-slate-400">
                  #{r.id} · {r.question_count} câu · {r.duration_minutes} phút
                  {r.classIds.length > 0 && ` · ${classNames(r.classIds)}`} · {fmtDate(r.created_at)}
                </span>
              </span>
              <span
                className={`shrink-0 rounded-full px-2 py-0.5 text-[11px] font-semibold ${
                  r.published ? "bg-emerald-500/15 text-emerald-300" : "bg-white/10 text-slate-400"
                }`}
              >
                {r.published ? "Đã xuất bản" : "Bản nháp"}
              </span>
            </button>
          ))}
        </div>

        <div className="flex items-center justify-between gap-2">
          <button type="button" disabled={page === 0} onClick={() => setPage((p) => p - 1)} className="admin-chip">
            ← Trước
          </button>
          <span className="text-xs text-slate-400">
            Trang {page + 1} / {pages}
          </span>
          <button type="button" disabled={listBusy || !!listError || page + 1 >= pages} onClick={() => setPage((p) => p + 1)} className="admin-chip">
            Sau →
          </button>
        </div>
      </section>

      {selectedId !== null && (
        <section className="space-y-4 rounded-2xl border border-white/10 bg-white/5 p-4">
          {loadingFull && <p className="text-sm text-slate-400">Đang tải đề #{selectedId}…</p>}
          {full && (
            <>
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 pb-4">
                <div>
                  <h2 className="admin-h2">Đề #{full.id}</h2>
                  <p className="mt-1 text-xs text-slate-400">
                    Tạo lúc {fmtDate(full.created_at)}
                    {full.cnc_key && " · Ngân hàng CNC"}
                  </p>
                </div>
                <label className="inline-flex items-center gap-2 text-sm text-slate-300">
                  <input type="checkbox" checked={publishedInput} onChange={(e) => setPublishedInput(e.target.checked)} />
                  Xuất bản (học sinh thấy được)
                </label>
              </div>

              <div className="grid gap-3 sm:grid-cols-2">
                <label className="text-xs font-semibold text-slate-400">
                  Điểm đạt, thang 10 (để trống = không đánh giá đạt)
                  <input
                    type="number"
                    min={0}
                    max={10}
                    step={0.25}
                    value={passScoreInput}
                    onChange={(e) => setPassScoreInput(e.target.value)}
                    className={`${inputCls} mt-1`}
                  />
                </label>
                <label className="text-xs font-semibold text-slate-400">
                  Khối lớp (để tra yêu cầu cần đạt khi gắn nhãn Chủ đề)
                  <select value={grade ?? ""} onChange={(e) => setGradeOverride(e.target.value || null)} className={`${selectCls} mt-1`}>
                    <option value="">— chọn khối —</option>
                    {grades.map((g) => (
                      <option key={g} value={g}>
                        Khối {g}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <ClassPicker selected={classIdsInput} onChange={setClassIdsInput} />

              <ExamSection
                subjectCode={full.subject_code}
                topicGroups={topicGroups}
                catalogNames={catalogNames}
                lessonPicked={false}
                onChange={setExamBundle}
                externalSeed={seed}
                hideRawText
              />

              {check && !check.ok && (
                <ul className="space-y-1 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-200">
                  {check.errors.map((e, i) => (
                    <li key={i}>• {e}</li>
                  ))}
                </ul>
              )}
              {missingFigure.length > 0 && <MissingFigureNotice nums={missingFigure} ack={figureAck} onAck={setFigureAck} />}

              <div className="sticky bottom-4 flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#080D1A]/95 p-4 shadow-2xl backdrop-blur">
                <button
                  type="button"
                  onClick={save}
                  disabled={!canSave}
                  className="rounded-full bg-primary px-6 py-2.5 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {saving ? "Đang lưu…" : "Lưu thay đổi"}
                </button>
                {canSave && (
                  <span className="inline-flex items-center gap-1 text-xs text-emerald-300">
                    <CheckCircle2 size={14} /> Sẵn sàng lưu
                  </span>
                )}
              </div>
            </>
          )}
        </section>
      )}
    </div>
  );
}
