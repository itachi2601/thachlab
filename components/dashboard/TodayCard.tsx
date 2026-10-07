"use client";

import Link from "next/link";
import { AlertTriangle, ChevronRight, Megaphone, Trophy } from "lucide-react";
import type { ClassAnnouncement } from "@/services/announcements";
import { formatExitWait } from "@/services/tutoring";
import type { NextStep } from "@/features/learning/next-steps";

/**
 * Thẻ "Hôm nay em làm gì" — thẻ DUY NHẤT gợi việc ở trang chủ HS (N4, B2, L5):
 * ghi chú của GV (nếu có) → MỘT nút nổi (việc đầu) → tối đa 3 việc phụ dạng dòng chữ → cảnh báo là một dòng nhỏ.
 * Thứ tự việc do trang chủ quyết: bài kiểm tra được giao → BTVN ôn tập → rankNextSteps (mở khoá phụ đạo →
 * làm lại đề điểm thấp → học bài kế → ôn lại). Không có gì để hiện → trang chủ không render thẻ này (N3).
 * Bước "unlock" không có href: bấm gọi onUnlock để mở bài tự kiểm tra; đang chờ giãn cách thì mờ.
 */
export default function TodayCard({
  note,
  primary,
  secondary,
  alertText,
  onUnlock,
}: {
  note: ClassAnnouncement | null;
  primary: NextStep | null;
  secondary: NextStep[];
  alertText: string | null;
  onUnlock: (needId: number) => void;
}) {
  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <div className="flex items-center gap-2">
        <Megaphone size={18} className="text-blue-300" />
        <h2 className="font-display font-bold text-white">Hôm nay em làm gì</h2>
      </div>
      <div className="mt-3 space-y-2.5">
        {note && <AnnouncementNote item={note} />}

        {primary && <PrimaryStep step={primary} onUnlock={onUnlock} />}

        {secondary.length > 0 && (
          <ul className="space-y-0.5">
            {secondary.map((step) => (
              <li key={step.key}>
                <SecondaryStep step={step} onUnlock={onUnlock} />
              </li>
            ))}
          </ul>
        )}

        {alertText && (
          <p className="flex items-start gap-1.5 text-[13px] text-amber-200/80">
            <AlertTriangle size={14} className="mt-0.5 shrink-0 text-amber-300" />
            {alertText}
          </p>
        )}
      </div>
    </section>
  );
}

function stepHint(step: NextStep): string {
  return step.lockedUntil ? `Làm lại được từ ${formatExitWait(step.lockedUntil)}` : step.hint;
}

function PrimaryStep({ step, onUnlock }: { step: NextStep; onUnlock: (needId: number) => void }) {
  const hint = stepHint(step);
  const body = (
    <>
      <div className="min-w-0">
        <small className="text-[13px] font-bold uppercase tracking-wider text-blue-100">{step.action}</small>
        <p className="mt-0.5 truncate text-sm font-bold">{step.title}</p>
        {hint && <p className="truncate text-[13px] text-blue-100">{hint}</p>}
      </div>
      <ChevronRight className="shrink-0" size={18} />
    </>
  );
  const cls =
    "flex min-h-12 w-full items-center justify-between gap-3 rounded-xl bg-primary p-3 text-left text-white hover:bg-primary-dark disabled:opacity-60";
  if (step.href) {
    return (
      <Link href={step.href} className={cls}>
        {body}
      </Link>
    );
  }
  return (
    <button
      type="button"
      disabled={Boolean(step.lockedUntil)}
      onClick={() => step.needId !== undefined && onUnlock(step.needId)}
      className={cls}
    >
      {body}
    </button>
  );
}

function SecondaryStep({ step, onUnlock }: { step: NextStep; onUnlock: (needId: number) => void }) {
  const hint = stepHint(step);
  const body = (
    <>
      <span className="min-w-0 truncate">
        <span className="text-[13px] text-slate-400">{step.action} · </span>
        {step.title}
        {hint && <span className="text-[13px] text-slate-400"> · {hint}</span>}
      </span>
      <ChevronRight size={16} className="shrink-0 text-slate-500" />
    </>
  );
  const cls =
    "flex min-h-11 w-full items-center justify-between gap-2 text-left text-sm text-slate-300 hover:text-white disabled:opacity-50 disabled:hover:text-slate-300";
  if (step.href) {
    return (
      <Link href={step.href} className={cls}>
        {body}
      </Link>
    );
  }
  return (
    <button
      type="button"
      disabled={Boolean(step.lockedUntil)}
      onClick={() => step.needId !== undefined && onUnlock(step.needId)}
      className={cls}
    >
      {body}
    </button>
  );
}

/** Ghi chú "việc hôm nay" / BTVN của GV: nội dung + người đăng + link làm bài nếu có gắn đề. */
export function AnnouncementNote({ item }: { item: ClassAnnouncement }) {
  return (
    <div className="rounded-xl border border-blue-400/20 bg-blue-500/5 p-3">
      <p className="whitespace-pre-wrap text-sm text-blue-100">{item.body}</p>
      <p className="mt-1.5 text-[13px] text-slate-400">
        {item.createdByName || "Giáo viên"} ·{" "}
        {new Date(item.createdAt).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })}
      </p>
      {item.examId && (
        <Link
          href={`/kiem-tra/lam?id=${item.examId}`}
          className="mt-2.5 flex min-h-11 items-center justify-between gap-2 rounded-lg bg-blue-500/15 px-3 py-2 text-sm font-bold text-blue-100 hover:bg-blue-500/25"
        >
          <span className="flex min-w-0 items-center gap-2">
            <Trophy size={14} className="shrink-0 text-amber-300" />
            <span className="truncate">{item.examTitle ?? "Làm bài"}</span>
          </span>
          <ChevronRight size={16} className="shrink-0" />
        </Link>
      )}
    </div>
  );
}
