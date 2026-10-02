"use client";

import Link from "next/link";
import { Check, ChevronDown } from "lucide-react";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { chapterDisplayTitle, isSemesterExam } from "@/features/lessons/types";

export interface ChapterTreeEntry {
  chapter: Chapter;
  lessons: Lesson[];
}

interface Props {
  entries: ChapterTreeEntry[];
  /** "learn": trang bài (bài đang xem = is-current). "pick": trang chương (chương đang chọn = is-current). */
  mode: "learn" | "pick";
  currentLessonId?: number;
  currentChapterId?: number;
  openChapterIds: Set<number>;
  onToggleChapter: (chapterId: number) => void;
  /** pick: bấm tên chương thì chọn chương (cột giữa đổi), mũi tên vẫn chỉ gấp/mở. */
  onPickChapter?: (chapterId: number) => void;
  lessonHref: (lesson: Lesson) => string;
  isLessonDone: (lesson: Lesson) => boolean;
  onLessonClick?: (lesson: Lesson) => void;
  /** Kết quả ô "Tìm bài trong khoá"; null = không lọc. */
  filterLessonIds?: Set<number> | null;
}

/**
 * Cây chương dùng chung cho trang bài (cột trái ≥1024 + ngăn kéo <640) và trang chương (cột trái ≥1024).
 * Component thuần hiển thị: chương nào đang mở, chương/bài nào đang chọn đều do trang quyết và truyền xuống.
 */
export default function ChapterTree(p: Props) {
  return (
    <div className="lesson-tree">
      {p.entries.map(({ chapter, lessons }, chapterIndex) => {
        const filter = p.filterLessonIds;
        const shown = filter ? lessons.filter((l) => filter.has(l.id)) : lessons;
        if (shown.length === 0) return null;
        const open = p.openChapterIds.has(chapter.id);
        const done = lessons.filter(p.isLessonDone).length;
        const picked = p.mode === "pick" && chapter.id === p.currentChapterId;
        return (
          <div key={chapter.id}>
            <button
              type="button"
              className={`lesson-tree-chapter ${picked ? "is-current" : ""}`}
              onClick={() =>
                p.mode === "pick" && p.onPickChapter ? p.onPickChapter(chapter.id) : p.onToggleChapter(chapter.id)
              }
              aria-expanded={open}
              aria-current={picked ? "true" : undefined}
            >
              <em>{chapterIndex + 1}</em>
              <span>{chapterDisplayTitle(chapter.title)}</span>
              <small>{done}/{lessons.length} bài</small>
              <ChevronDown
                size={15}
                className={open ? "is-open" : ""}
                aria-hidden
                onClick={(e) => {
                  if (p.mode === "pick") {
                    e.stopPropagation();
                    p.onToggleChapter(chapter.id);
                  }
                }}
              />
            </button>
            {open && (
              <ol>
                {shown.map((lesson) => {
                  const current = p.mode === "learn" && lesson.id === p.currentLessonId;
                  const isDone = p.isLessonDone(lesson);
                  const exam = isSemesterExam(lesson.lesson_kind);
                  const icon = isDone ? <Check size={11} /> : exam ? "KT" : current ? "●" : "○";
                  const cls = `${isDone ? "is-done" : ""} ${exam ? "is-exam" : ""}`.trim();
                  return (
                    <li key={lesson.id}>
                      {current ? (
                        <span className={`lesson-tree-current is-current ${cls}`} aria-current="page">
                          <i aria-hidden>{icon}</i>
                          <span>{lesson.title}</span>
                        </span>
                      ) : (
                        <Link href={p.lessonHref(lesson)} className={cls} onClick={() => p.onLessonClick?.(lesson)}>
                          <i aria-hidden>{icon}</i>
                          <span>{lesson.title}</span>
                        </Link>
                      )}
                    </li>
                  );
                })}
              </ol>
            )}
          </div>
        );
      })}
      {p.filterLessonIds?.size === 0 && <p className="lesson-panel-empty">Không thấy bài nào khớp.</p>}
    </div>
  );
}
