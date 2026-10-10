"use client";

import { ArrowRight, BookOpen } from "lucide-react";
import type { InlineLessonProgress } from "@/components/lessons/InlineLessonAccordion";

export default function ContinueLearningCard({
  chapterTitle,
  lessonTitle,
  progress,
  onContinue,
}: {
  chapterTitle: string;
  lessonTitle: string;
  progress?: InlineLessonProgress;
  onContinue: () => void;
}) {
  const percent = progress?.total ? Math.round((progress.completed / progress.total) * 100) : null;
  return (
    <aside className="rounded-2xl border border-line bg-panel p-5">
      <div className="flex flex-wrap items-center gap-4">
        <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary-soft text-primary"><BookOpen size={21} /></span>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-bold uppercase tracking-wider text-primary">Tiếp tục từ nơi em đã dừng</p>
          <h3 className="mt-1 truncate font-display font-bold text-ink">{lessonTitle}</h3>
          <p className="mt-1 truncate text-xs text-muted">{chapterTitle}{percent !== null ? ` · ${percent}% hoàn thành` : ""}</p>
        </div>
        <button type="button" onClick={onContinue} className="inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-bold text-white hover:bg-primary-dark">
          Tiếp tục học <ArrowRight size={16} />
        </button>
      </div>
    </aside>
  );
}
