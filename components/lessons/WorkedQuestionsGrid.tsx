"use client";

import { useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

/** Lưới các "dạng bài" (bài tập mẫu): mỗi ô là 1 dạng, bấm để mở/đóng lời giải mẫu. */
export default function WorkedQuestionsGrid({
  questions,
  color = "#8B5CF6",
}: {
  questions: LessonWorkedQuestion[];
  color?: string;
}) {
  const [openIdx, setOpenIdx] = useState<Set<number>>(new Set());

  function toggle(idx: number) {
    setOpenIdx((current) => {
      const next = new Set(current);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }

  if (questions.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {questions.map((q, idx) => {
          const active = openIdx.has(idx);
          return (
            <button
              key={idx}
              type="button"
              onClick={() => toggle(idx)}
              className="flex min-w-16 flex-col items-center gap-0.5 rounded-xl border px-3 py-2 text-xs font-semibold transition-colors"
              style={
                active
                  ? { borderColor: color, backgroundColor: `${color}26`, color }
                  : { borderColor: "rgba(255,255,255,0.1)", color: "#94A3B8" }
              }
            >
              <span>BÀI {idx + 1}</span>
              <span className="text-[10px] font-bold uppercase opacity-80">
                {q.label || "TL"}
              </span>
            </button>
          );
        })}
      </div>
      <div className="space-y-3">
        {questions.map(
          (q, idx) =>
            openIdx.has(idx) && (
              <div
                key={idx}
                className="rounded-2xl border p-5 text-slate-200"
                style={{ borderColor: `${color}4D`, backgroundColor: "#0B1020" }}
              >
                <p className="mb-2 text-xs font-bold uppercase tracking-wide" style={{ color }}>
                  Bài {idx + 1}{q.label ? ` · ${q.label}` : ""}
                </p>
                <ContentHtml html={q.body_html} className="block leading-relaxed" />
              </div>
            ),
        )}
      </div>
    </div>
  );
}
