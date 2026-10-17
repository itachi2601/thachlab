"use client";

import Link from "next/link";
import { Check } from "lucide-react";
import type { Lesson } from "@/features/lessons/types";
import { HSG_SUBJECT_CODE } from "@/services/academic-subjects";
import { tickId, type Hsg9Session } from "@/features/hsg9/lo-trinh";

export type LessonProgressMap = Map<number, { completed: number; total: number }>;

export function hsgLessonHref(lesson: Pick<Lesson, "id" | "chapter_id">) {
  const params = new URLSearchParams({
    id: String(lesson.id),
    subject: HSG_SUBJECT_CODE,
    chapter: String(lesson.chapter_id),
    class: "khtn-9",
  });
  return `/lop-hoc/bai?${params.toString()}`;
}

/** Tiến độ các bài của một buổi: lấy từ dấu "đã học" trên web (lesson_progress), không phải dấu tick tự ghi. */
export function SessionLessons({
  session,
  lessons,
  progress,
}: {
  session: Hsg9Session;
  lessons: Lesson[] | null;
  progress: LessonProgressMap | null;
}) {
  if (session.lessons.length === 0) return null;
  return (
    <ul className="space-y-1">
      {session.lessons.map((id) => {
        const lesson = lessons?.find((l) => l.id === id);
        const p = progress?.get(id);
        const pct = p?.total ? Math.round((p.completed / p.total) * 100) : 0;
        if (!lesson) {
          return (
            <li key={id} className="flex min-h-11 items-center text-sm text-muted">
              Bài {id} đang soạn, thầy mở khi xong.
            </li>
          );
        }
        return (
          <li key={id}>
            <Link
              href={hsgLessonHref(lesson)}
              className="flex min-h-11 items-center gap-3 rounded-lg px-1 text-sm text-ink hover:bg-primary-soft"
            >
              <span className="min-w-0 flex-1 truncate">{lesson.title}</span>
              {progress && p?.total ? (
                <span className="flex shrink-0 items-center gap-2 text-xs text-muted">
                  <span className="h-1.5 w-14 overflow-hidden rounded-full bg-line" aria-hidden>
                    <span className="block h-full rounded-full bg-ok" style={{ width: `${pct}%` }} />
                  </span>
                  <span className="tabular-nums">
                    {p.completed}/{p.total} mục
                  </span>
                </span>
              ) : null}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

/** Danh sách việc tự học 5 ngày, có ô tự đánh dấu. todayIndex được nhấn nhẹ (một điểm nổi bật, N7). */
export function TaskList({
  session,
  ticks,
  onToggle,
  todayIndex = -1,
  only,
}: {
  session: Hsg9Session;
  ticks: Record<string, boolean>;
  onToggle: ((id: string) => void) | null;
  todayIndex?: number;
  /** Chỉ hiện việc ở chỉ số này (thẻ ở trang lớp chỉ hiện việc hôm nay). */
  only?: number;
}) {
  return (
    <ul className="space-y-1">
      {session.tuHoc.map(([day, task], i) => {
        if (only !== undefined && i !== only) return null;
        const id = tickId(session.buoi, i);
        const done = !!ticks[id];
        const isToday = i === todayIndex;
        return (
          <li key={id}>
            <button
              type="button"
              disabled={!onToggle}
              onClick={() => onToggle?.(id)}
              aria-pressed={done}
              className={`flex w-full items-start gap-3 rounded-lg px-2 py-2 text-left text-sm ${
                isToday ? "bg-primary-soft" : ""
              } ${onToggle ? "cursor-pointer" : "cursor-default"}`}
            >
              <span
                className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded border ${
                  done ? "border-ok bg-ok text-white" : "border-line-strong bg-panel"
                }`}
                aria-hidden
              >
                {done && <Check className="h-3.5 w-3.5" strokeWidth={3} />}
              </span>
              <span className="min-w-0">
                <span className="block font-semibold text-ink">
                  {day}
                  {isToday && <span className="ml-2 text-xs font-medium text-primary">hôm nay</span>}
                </span>
                <span className={done ? "text-muted line-through" : "text-ink"}>{task}</span>
              </span>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
