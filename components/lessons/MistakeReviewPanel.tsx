"use client";

import { useEffect, useState } from "react";
import { ChevronDown } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import QuestionCard from "@/components/exams/QuestionCard";
import { fetchMyLatestMistakes, type MistakeReviewItem } from "@/services/lessons";

export default function MistakeReviewPanel() {
  const { session } = useAuth();
  const [mistakes, setMistakes] = useState<MistakeReviewItem[] | null>(null);
  const [open, setOpen] = useState(false);
  const [visibleCount, setVisibleCount] = useState(5);

  useEffect(() => {
    if (!session) return;
    fetchMyLatestMistakes(session.user.id).then(setMistakes).catch(() => setMistakes([]));
  }, [session]);

  if (!session || !mistakes?.length) return null;
  const preview = Math.min(5, mistakes.length);
  return (
    <section className="class-mistake">
      <button type="button" onClick={() => setOpen((current) => !current)} aria-expanded={open} aria-controls="mistake-review-list" className="class-mistake-toggle">
        <span>Ôn {preview} câu vừa sai</span>
        <ChevronDown size={18} className={open ? "is-open" : ""} aria-hidden />
      </button>
      {open && (
        <div id="mistake-review-list" className="space-y-5 pb-2">
          {mistakes.slice(0, visibleCount).map((item) => (
            <div key={`${item.examId}-${item.questionIndex}`}>
              <p className="mb-2 text-sm font-semibold text-slate-300">{item.examTitle}</p>
              <QuestionCard index={item.questionIndex + 1} question={item.question} response={item.response} review />
            </div>
          ))}
          {visibleCount < mistakes.length && (
            <button type="button" onClick={() => setVisibleCount((count) => count + 5)} className="w-full rounded-xl border border-white/10 px-4 py-3 text-sm font-semibold text-slate-300 hover:border-white/25">
              Xem thêm {Math.min(5, mistakes.length - visibleCount)} câu
            </button>
          )}
        </div>
      )}
    </section>
  );
}
