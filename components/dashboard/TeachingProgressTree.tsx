"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { CalendarDays, ChevronDown, MessageSquarePlus, Trash2 } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchQuestionTopics, lessonTopics, type QuestionTopic } from "@/services/analytics";
import { fetchCurriculumMeta, type ChapterMeta } from "@/services/class-insights";
import { WEEKDAY_LABEL } from "@/services/thpt-courses-public";
import {
  addTeachingNote,
  deleteTeachingNote,
  fetchTeachingCourses,
  fetchTeachingState,
  localIso,
  setTaught,
  weekStartOf,
  type TeachingCourse,
  type TeachingState,
} from "@/services/teaching-progress";

const fmt = (iso: string) => new Date(`${iso}T00:00:00`).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" });

/**
 * Cây tiến trình bài dạy của một khoá: tick "đã dạy" (kèm ngày → tuần) + ghi chú cải tiến cho năm sau.
 * Thầy (dashboard THPT) và trợ giảng (/tro-giang/tien-trinh) dùng chung đúng một dữ liệu.
 * Lịch tuần lấy từ lịch khoá đã đăng; tick bài làm mốc "lớp đang dạy tới" của khoá dịch theo (phục vụ bù bài).
 */
export default function TeachingProgressTree({ classId }: { classId?: number | null }) {
  const toast = useToast();
  const [courses, setCourses] = useState<TeachingCourse[] | null>(null);
  const [courseId, setCourseId] = useState<number | null>(null);
  const [state, setState] = useState<TeachingState | null>(null);
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [chapters, setChapters] = useState<Map<number, ChapterMeta>>(new Map());
  const [open, setOpen] = useState<number | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState<number | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetchTeachingCourses(classId)
      .then((rows) => {
        if (cancelled) return;
        setCourses(rows);
        setCourseId((cur) => (rows.some((c) => c.id === cur) ? cur : rows[0]?.id ?? null));
      })
      .catch((e: unknown) => { if (!cancelled) { setCourses([]); setError(e instanceof Error ? e.message : "Không tải được."); } });
    fetchCurriculumMeta().then((m) => { if (!cancelled) setChapters(m.chapters); }).catch(() => undefined);
    return () => { cancelled = true; };
  }, [classId]);

  const course = courses?.find((c) => c.id === courseId) ?? null;
  const grade = course ? course.className.match(/\d+/)?.[0] : undefined;

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      if (!grade) { if (!cancelled) setTopics([]); return; }
      const rows = await fetchQuestionTopics(grade).catch(() => [] as QuestionTopic[]);
      if (!cancelled) setTopics(lessonTopics(rows));
    })();
    return () => { cancelled = true; };
  }, [grade]);

  const reload = useCallback(async (id: number) => {
    try {
      setState(await fetchTeachingState(id));
      setError("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Không tải được tiến trình.");
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      if (courseId == null) { if (!cancelled) setState(null); return; }
      try {
        const s = await fetchTeachingState(courseId);
        if (!cancelled) { setState(s); setError(""); }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Không tải được tiến trình.");
      }
    })();
    return () => { cancelled = true; };
  }, [courseId]);

  const markByTopic = useMemo(() => new Map((state?.progress ?? []).map((p) => [p.topicId, p])), [state]);
  const notesByTopic = useMemo(() => {
    const m = new Map<number, NonNullable<typeof state>["notes"]>();
    for (const n of state?.notes ?? []) m.set(n.topicId, [...(m.get(n.topicId) ?? []), n]);
    return m;
  }, [state]);

  const groups = useMemo(() => {
    const by = new Map<number | null, QuestionTopic[]>();
    for (const t of topics) by.set(t.chapterId, [...(by.get(t.chapterId) ?? []), t]);
    return [...by.entries()]
      .map(([ch, list]) => ({
        chapterId: ch,
        title: ch != null ? chapters.get(ch)?.title ?? "Chương khác" : "Chưa xếp chương",
        order: ch != null ? chapters.get(ch)?.sortOrder ?? 999 : 1000,
        list: list.sort((a, b) => a.sortOrder - b.sortOrder || a.name.localeCompare(b.name, "vi")),
      }))
      .sort((a, b) => a.order - b.order);
  }, [topics, chapters]);

  const weeks = useMemo(() => {
    const m = new Map<string, string[]>();
    for (const p of state?.progress ?? []) {
      const name = topics.find((t) => t.id === p.topicId)?.name ?? `Bài #${p.topicId}`;
      m.set(p.weekStart, [...(m.get(p.weekStart) ?? []), name]);
    }
    return [...m.entries()].sort((a, b) => (a[0] < b[0] ? 1 : -1));
  }, [state, topics]);

  function weekNo(weekStart: string): string {
    if (!course?.startsAt) return `Tuần ${fmt(weekStart)}`;
    const n = Math.floor((new Date(`${weekStart}T00:00:00`).getTime() - new Date(`${weekStartOf(course.startsAt)}T00:00:00`).getTime()) / (7 * 86400000)) + 1;
    return n >= 1 ? `Tuần ${n}` : `Tuần ${fmt(weekStart)}`;
  }

  async function toggle(topicId: number, taught: boolean) {
    if (courseId == null) return;
    setBusy(topicId);
    try {
      await setTaught(courseId, topicId, taught, taught ? localIso(new Date()) : undefined);
      await reload(courseId);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa lưu được.");
    } finally {
      setBusy(null);
    }
  }
  async function changeDate(topicId: number, iso: string) {
    if (courseId == null || !iso) return;
    try {
      await setTaught(courseId, topicId, true, iso);
      await reload(courseId);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa lưu được.");
    }
  }
  async function saveNote(topicId: number) {
    if (courseId == null || !draft.trim()) return;
    try {
      await addTeachingNote(courseId, topicId, draft);
      setDraft("");
      await reload(courseId);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa lưu được ghi chú.");
    }
  }
  async function removeNote(id: number) {
    if (courseId == null) return;
    try {
      await deleteTeachingNote(id);
      await reload(courseId);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa xoá được.");
    }
  }

  if (courses === null) return <p className="text-sm text-slate-400">Đang tải…</p>;
  if (courses.length === 0) {
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">
        {error || "Chưa có khoá học nào của khối này để ghi tiến trình. Tạo khoá ở tab Danh sách lớp trước."}
      </p>
    );
  }

  const total = topics.length;
  const done = topics.filter((t) => markByTopic.has(t.id)).length;
  const today = localIso(new Date());
  const thisWeek = weekStartOf(today);
  const taughtThisWeek = (state?.progress ?? []).filter((p) => p.weekStart === thisWeek).length;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-3">
        <select
          aria-label="Chọn khoá"
          value={courseId ?? ""}
          onChange={(e) => { setCourseId(Number(e.target.value)); setOpen(null); }}
          className="min-w-60 max-w-full rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white"
        >
          {courses.map((c) => (
            <option key={c.id} value={c.id}>{c.className} · {c.name}{c.schoolYear ? ` · ${c.schoolYear}` : ""}</option>
          ))}
        </select>
        {course && course.schedules.length > 0 && (
          <p className="flex items-start gap-1.5 text-xs text-slate-400">
            <CalendarDays size={14} className="mt-0.5 shrink-0" />
            <span>
              {course.schedules.map((s) => `${WEEKDAY_LABEL[s.weekday] ?? ""} ${s.start.slice(0, 5)}–${s.end.slice(0, 5)}${s.location ? ` · ${s.location}` : ""}`).join(" · ")}
            </span>
          </p>
        )}
      </div>

      {error && <p className="rounded-xl border border-red-500/30 p-3 text-sm text-red-300">{error}</p>}

      <section className="rounded-2xl border border-white/10 bg-panel p-4">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <p className="text-sm font-semibold text-white">Đã dạy {done}/{total} bài</p>
          <p className="text-xs text-slate-400">Tuần này ({fmt(thisWeek)}): {taughtThisWeek} bài</p>
        </div>
        <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-white/10">
          <div className="h-full rounded-full bg-blue-500" style={{ width: `${total ? Math.round((done / total) * 100) : 0}%` }} />
        </div>
      </section>

      {weeks.length > 0 && (
        <section className="rounded-2xl border border-white/10 bg-panel p-4">
          <h3 className="mb-2 font-display text-base font-bold text-white">Theo tuần</h3>
          <ul className="space-y-1.5 text-sm">
            {weeks.slice(0, 6).map(([ws, names]) => (
              <li key={ws} className="flex gap-3">
                <span className="w-28 shrink-0 text-slate-400">{weekNo(ws)} · {fmt(ws)}</span>
                <span className="min-w-0 text-slate-200">{names.join("; ")}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {topics.length === 0 ? (
        <p className="text-sm text-slate-500">Chưa có danh mục bài của khối này.</p>
      ) : (
        groups.map((g) => (
          <section key={g.chapterId ?? "none"} className="rounded-2xl border border-white/10 bg-panel">
            <h3 className="border-b border-white/10 px-4 py-3 font-display text-base font-bold text-white">{g.title}</h3>
            <ul className="divide-y divide-white/5">
              {g.list.map((t) => {
                const mark = markByTopic.get(t.id);
                const notes = notesByTopic.get(t.id) ?? [];
                const isOpen = open === t.id;
                return (
                  <li key={t.id}>
                    <div className="flex items-center gap-3 px-4 py-2">
                      <input
                        type="checkbox"
                        aria-label={`Đã dạy: ${t.name}`}
                        checked={Boolean(mark)}
                        disabled={busy === t.id}
                        onChange={(e) => void toggle(t.id, e.target.checked)}
                        className="size-6 shrink-0 accent-blue-600"
                      />
                      <span className="min-w-0 flex-1 text-sm text-slate-100">
                        {t.name}
                        {mark && (
                          <span className="block text-xs text-slate-400">
                            {weekNo(mark.weekStart)} · dạy {fmt(mark.taughtOn)}{mark.by ? ` · ${mark.by}` : ""}
                          </span>
                        )}
                      </span>
                      {mark && (
                        <input
                          type="date"
                          aria-label={`Ngày dạy ${t.name}`}
                          value={mark.taughtOn}
                          onChange={(e) => void changeDate(t.id, e.target.value)}
                          className="hidden rounded-lg border border-white/10 bg-panel-deep px-2 py-1 text-xs text-slate-200 sm:block"
                        />
                      )}
                      <button
                        type="button"
                        onClick={() => { setOpen(isOpen ? null : t.id); setDraft(""); }}
                        aria-expanded={isOpen}
                        className="inline-flex h-11 shrink-0 items-center gap-1 rounded-lg px-2 text-xs text-slate-300 hover:bg-white/10"
                      >
                        <MessageSquarePlus size={16} />
                        {notes.length > 0 ? notes.length : ""}
                        <ChevronDown size={14} className={isOpen ? "rotate-180" : ""} />
                      </button>
                    </div>
                    {isOpen && (
                      <div className="space-y-3 bg-white/[.03] px-4 py-3">
                        {mark && (
                          <label className="flex items-center gap-2 text-xs text-slate-400 sm:hidden">
                            Ngày dạy
                            <input
                              type="date"
                              value={mark.taughtOn}
                              onChange={(e) => void changeDate(t.id, e.target.value)}
                              className="rounded-lg border border-white/10 bg-panel-deep px-2 py-1.5 text-sm text-slate-200"
                            />
                          </label>
                        )}
                        {notes.length === 0 ? (
                          <p className="text-xs text-slate-500">Chưa có ghi chú. Ghi điều cần cải tiến khi dạy bài này ở năm học sau.</p>
                        ) : (
                          <ul className="space-y-2">
                            {notes.map((n) => (
                              <li key={n.id} className="rounded-xl bg-white/[.05] p-3 text-sm text-slate-100">
                                <p className="whitespace-pre-wrap">{n.body}</p>
                                <p className="mt-1 flex items-center gap-2 text-xs text-slate-400">
                                  <span>{n.schoolYear || new Date(n.createdAt).getFullYear()} · {n.author ?? "—"} · {new Date(n.createdAt).toLocaleDateString("vi-VN")}</span>
                                  {n.mine && (
                                    <button type="button" onClick={() => void removeNote(n.id)} aria-label="Xoá ghi chú" className="ml-auto inline-flex h-8 items-center text-slate-400 hover:text-red-300">
                                      <Trash2 size={14} />
                                    </button>
                                  )}
                                </p>
                              </li>
                            ))}
                          </ul>
                        )}
                        <div className="flex gap-2">
                          <textarea
                            value={draft}
                            onChange={(e) => setDraft(e.target.value)}
                            rows={2}
                            maxLength={1000}
                            placeholder="Ví dụ: ví dụ lực ma sát nghỉ nên làm thí nghiệm kéo hộp trước; HS hay nhầm chiều lực…"
                            className="min-w-0 flex-1 rounded-xl border border-white/10 bg-panel px-3 py-2 text-sm text-white"
                          />
                          <button
                            type="button"
                            disabled={!draft.trim()}
                            onClick={() => void saveNote(t.id)}
                            className="self-end rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
                          >
                            Lưu
                          </button>
                        </div>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </section>
        ))
      )}
    </div>
  );
}
