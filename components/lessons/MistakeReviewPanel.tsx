"use client";

import { useEffect, useState } from "react";
import { AlertCircle, ChevronDown } from "lucide-react";
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
  return (
    <section className="rounded-2xl border border-amber-400/20 bg-amber-500/5">
      <button type="button" onClick={() => setOpen((current) => !current)} aria-expanded={open} aria-controls="mistake-review-list" className="flex w-full items-center gap-4 p-5 text-left">
        <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10 text-amber-300"><AlertCircle size={20} /></span>
        <span className="min-w-0 flex-1">
          <strong className="block font-display text-white">Ôn lại lỗi sai</strong>
          <small className="mt-1 block text-slate-400">{mistakes.length} câu cần xem lại từ lần làm gần nhất</small>
        </span>
        <span className="text-sm font-semibold text-amber-300">{open ? "Thu gọn" : "Bắt đầu ôn"}</span>
        <ChevronDown size={18} className={`text-amber-300 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div id="mistake-review-list" className="space-y-5 border-t border-amber-400/10 p-5">
          {mistakes.slice(0, visibleCount).map((item) => (
            <div key={`${item.examId}-${item.questionIndex}`}>
              <p className="mb-2 text-xs font-bold uppercase tracking-wide text-amber-300">{item.examTitle}</p>
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
