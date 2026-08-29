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
    <aside className="rounded-2xl border border-blue-400/20 bg-gradient-to-r from-blue-500/10 to-cyan-500/5 p-5">
      <div className="flex flex-wrap items-center gap-4">
        <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/15 text-blue-300"><BookOpen size={21} /></span>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-bold uppercase tracking-wider text-blue-300">Tiếp tục từ nơi em đã dừng</p>
          <h3 className="mt-1 truncate font-display font-bold text-white">{lessonTitle}</h3>
          <p className="mt-1 truncate text-xs text-slate-400">{chapterTitle}{percent !== null ? ` · ${percent}% hoàn thành` : ""}</p>
        </div>
        <button type="button" onClick={onContinue} className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-bold text-white hover:bg-blue-500">
          Tiếp tục học <ArrowRight size={16} />
        </button>
      </div>
    </aside>
  );
}
