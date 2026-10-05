"use client";

import Link from "next/link";
import { BookOpen, ChevronRight, RotateCcw, Sparkles, Users } from "lucide-react";
import { formatExitWait } from "@/services/tutoring";
import type { NextStep, NextStepKind } from "@/features/learning/next-steps";

const ICON: Record<NextStepKind, typeof BookOpen> = { unlock: Users, retry: RotateCcw, lesson: BookOpen, review: BookOpen };
const ICON_COLOR: Record<NextStepKind, string> = {
  unlock: "text-sky-300",
  retry: "text-rose-300",
  lesson: "text-blue-300",
  review: "text-blue-300",
};
const ROW =
  "flex min-h-11 w-full items-center justify-between gap-3 rounded-xl border border-emerald-400/20 bg-black/15 p-3 text-left hover:bg-black/25 disabled:opacity-50 disabled:hover:bg-black/15";

export default function NextStepsCard({ steps, onUnlock }: { steps: NextStep[]; onUnlock: (needId: number) => void }) {
  return (
    <section className="rounded-2xl border border-emerald-400/25 bg-gradient-to-r from-emerald-500/10 to-transparent p-4 sm:p-5">
      <div className="flex items-center gap-2 text-emerald-300">
        <Sparkles size={18} />
        <h2 className="font-display font-bold text-white">Em đã làm xong bài được giao — việc nên làm tiếp</h2>
      </div>
      <div className="mt-3 space-y-2">
        {steps.map((step) => {
          const Icon = ICON[step.kind];
          const hint = step.lockedUntil ? `Làm lại được từ ${formatExitWait(step.lockedUntil)}` : step.hint;
          const body = (
            <>
              <span className="flex min-w-0 items-center gap-2">
                <Icon size={16} className={`shrink-0 ${ICON_COLOR[step.kind]}`} />
                <span className="min-w-0">
                  <strong className="block truncate text-sm text-white">{step.title}</strong>
                  {hint && <small className="block truncate text-[13px] text-slate-400">{hint}</small>}
                </span>
              </span>
              <ChevronRight size={16} className="shrink-0 text-emerald-300" />
            </>
          );
          return step.href ? (
            <Link key={step.key} href={step.href} className={ROW}>{body}</Link>
          ) : (
            <button
              key={step.key}
              type="button"
              disabled={Boolean(step.lockedUntil)}
              onClick={() => step.needId !== undefined && onUnlock(step.needId)}
              className={ROW}
            >
              {body}
            </button>
          );
        })}
      </div>
    </section>
  );
}
