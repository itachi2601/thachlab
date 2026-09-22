"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

/** Các "dạng bài" (bài tập mẫu): hàng thu/mở, tên dạng hiện rõ, lời giải mở ngay dưới hàng đó. */
export default function WorkedQuestionsGrid({
  questions,
  color = "#8B5CF6",
}: {
  questions: LessonWorkedQuestion[];
  color?: string;
}) {
  const [openIdx, setOpenIdx] = useState<Set<number>>(() => new Set(questions.length ? [0] : []));

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
    <div className="lesson-worked">
      {questions.map((q, idx) => {
        const open = openIdx.has(idx);
        return (
          <div key={idx} className="lesson-worked-row">
            <button
              type="button"
              onClick={() => toggle(idx)}
              aria-expanded={open}
              className="lesson-worked-head"
            >
              <span
                className="lesson-worked-num"
                style={open ? { borderColor: color, color } : undefined}
              >
                {idx + 1}
              </span>
              <span className="lesson-worked-label">{q.label || `Ví dụ ${idx + 1}`}</span>
              <ChevronDown size={16} className={open ? "rotate-180" : ""} />
            </button>
            {open && (
              <div className="lesson-worked-body">
                <ContentHtml html={q.body_html} className="block leading-relaxed" />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
