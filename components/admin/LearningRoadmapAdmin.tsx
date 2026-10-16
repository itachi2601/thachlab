"use client";

import { useEffect, useMemo, useState } from "react";
import type { SchoolClass } from "@/features/exams/types";
import { SECTION_META, SECTION_ORDER, type LessonItemKind } from "@/features/lessons/types";
import { fetchClasses } from "@/services/classes";
import { getSupabase } from "@/services/supabase";

interface ChapterRow { id: number; title: string; sort_order: number }
interface LessonRow { id: number; chapter_id: number; title: string; sort_order: number; published: boolean }
interface ItemRow { lesson_id: number; kind: string; published_at: string | null }

/** Trạng thái một mục của bài: đã mở cho HS / có nhưng đang ẩn / chưa có. */
type Cell = "live" | "hidden" | "none";

const CELL_STYLE: Record<Cell, string> = {
  live: "bg-emerald-500/20 text-emerald-300",
  hidden: "bg-amber-500/20 text-amber-300",
  none: "bg-slate-500/10 text-slate-500",
};
const CELL_LABEL: Record<Cell, string> = { live: "Đã mở", hidden: "Đang ẩn", none: "Chưa có" };

/** Lộ trình thầy xem: Lớp → Chương → Bài, mỗi bài đã có/ẩn/thiếu những mục nào. Chỉ đọc. */
export default function LearningRoadmapAdmin() {
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [classId, setClassId] = useState<number | null>(null);
  const [chapterClasses, setChapterClasses] = useState<{ chapter_id: number; class_id: number }[]>([]);
  const [chapters, setChapters] = useState<ChapterRow[]>([]);
  const [lessons, setLessons] = useState<LessonRow[]>([]);
  const [items, setItems] = useState<ItemRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [onlyGaps, setOnlyGaps] = useState(false);

  useEffect(() => {
    const supabase = getSupabase();
    (async () => {
      try {
        const [cls, cc, ch, ls, it] = await Promise.all([
          fetchClasses(true),
          supabase.from("chapter_classes").select("chapter_id, class_id"),
          supabase.from("chapters").select("id, title, sort_order").order("sort_order"),
          supabase.from("lessons").select("id, chapter_id, title, sort_order, published").order("sort_order"),
          supabase.from("lesson_items").select("lesson_id, kind, published_at"),
        ]);
        for (const r of [cc, ch, ls, it]) if (r.error) throw r.error;
        setClasses(cls);
        setClassId(cls[0]?.id ?? null);
        setChapterClasses((cc.data ?? []) as { chapter_id: number; class_id: number }[]);
        setChapters((ch.data ?? []) as ChapterRow[]);
        setLessons((ls.data ?? []) as LessonRow[]);
        setItems((it.data ?? []) as ItemRow[]);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Không tải được dữ liệu");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const itemMap = useMemo(() => {
    const m = new Map<string, Cell>();
    for (const i of items) {
      const key = `${i.lesson_id}:${i.kind}`;
      const cell: Cell = i.published_at && new Date(i.published_at) <= new Date() ? "live" : "hidden";
      if (m.get(key) !== "live") m.set(key, cell);
    }
    return m;
  }, [items]);

  const rows = useMemo(() => {
    if (classId == null) return [];
    const ids = new Set(chapterClasses.filter((c) => c.class_id === classId).map((c) => c.chapter_id));
    return chapters
      .filter((c) => ids.has(c.id))
      .map((c) => ({
        chapter: c,
        lessons: lessons
          .filter((l) => l.chapter_id === c.id)
          .map((l) => {
            const cells = SECTION_ORDER.map((k) => itemMap.get(`${l.id}:${k}`) ?? ("none" as Cell));
            return { lesson: l, cells, gap: !l.published || cells.slice(0, 1).some((x) => x !== "live") };
          }),
      }));
  }, [classId, chapterClasses, chapters, lessons, itemMap]);

  const total = rows.reduce((n, r) => n + r.lessons.length, 0);
  const open = rows.reduce((n, r) => n + r.lessons.filter((l) => l.lesson.published).length, 0);

  if (loading) return <p className="p-6 text-slate-400">Đang tải lộ trình…</p>;
  if (error) return <p className="p-6 text-rose-400">{error}</p>;

  return (
    <div className="mx-auto max-w-5xl p-4 sm:p-6">
      <h1 className="text-xl font-bold text-slate-100">Lộ trình học sinh</h1>
      <p className="mt-1 text-sm text-slate-400">
        Chuỗi chương → bài mỗi lớp, mục nào đã mở, đang ẩn hoặc chưa soạn. Chỉ xem, sửa ở trang Bài học.
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        {classes.map((c) => (
          <button
            key={c.id}
            type="button"
            onClick={() => setClassId(c.id)}
            className={`min-h-11 rounded-full px-4 text-sm font-medium ${
              classId === c.id ? "bg-sky-600 text-white" : "bg-slate-500/15 text-slate-300"
            }`}
          >
            {c.icon} {c.name}
          </button>
        ))}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-4 text-sm text-slate-300">
        <span>{rows.length} chương · {open}/{total} bài đã mở</span>
        <label className="flex min-h-11 items-center gap-2">
          <input type="checkbox" checked={onlyGaps} onChange={(e) => setOnlyGaps(e.target.checked)} />
          Chỉ hiện bài còn thiếu/ẩn
        </label>
      </div>

      <div className="mt-2 flex flex-wrap gap-2 text-xs">
        {(Object.keys(CELL_LABEL) as Cell[]).map((c) => (
          <span key={c} className={`rounded px-2 py-1 ${CELL_STYLE[c]}`}>{CELL_LABEL[c]}</span>
        ))}
      </div>

      {rows.length === 0 && <p className="mt-6 text-slate-400">Lớp này chưa có chương nào.</p>}

      {rows.map(({ chapter, lessons: ls }) => {
        const shown = onlyGaps ? ls.filter((l) => l.gap || l.cells.includes("hidden")) : ls;
        if (shown.length === 0) return null;
        return (
          <section key={chapter.id} className="mt-6">
            <h2 className="text-base font-semibold text-slate-100">{chapter.title}</h2>
            <ol className="mt-2 space-y-2">
              {shown.map(({ lesson, cells }, idx) => (
                <li key={lesson.id} className="rounded-lg border border-slate-500/20 p-3">
                  <p className="text-sm font-medium text-slate-200">
                    {idx + 1}. {lesson.title}
                    {!lesson.published && <span className="ml-2 rounded bg-amber-500/20 px-2 py-0.5 text-xs text-amber-300">Bài đang ẩn</span>}
                  </p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {SECTION_ORDER.map((k: LessonItemKind, i) => (
                      <span key={k} className={`rounded px-2 py-1 text-xs ${CELL_STYLE[cells[i]]}`} title={CELL_LABEL[cells[i]]}>
                        {SECTION_META[k].icon} {SECTION_META[k].label}
                      </span>
                    ))}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        );
      })}
    </div>
  );
}
