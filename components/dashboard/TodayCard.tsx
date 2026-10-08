"use client";

import Link from "next/link";
import { AlertTriangle, ChevronRight, Flame, Megaphone, Target, Trophy } from "lucide-react";
import type { ClassAnnouncement } from "@/services/announcements";
import type { RankStatus } from "@/features/rank/types";
import { formatExitWait } from "@/services/tutoring";
import type { NextStep } from "@/features/learning/next-steps";

/**
 * Thẻ "Hôm nay em làm gì" — thẻ DUY NHẤT gợi việc ở trang chủ HS (N4, B2, L5):
 * MỘT nút nổi (việc đầu) kèm dòng "làm xong được gì" → tối đa 3 việc phụ dạng dòng chữ → dải RP (còn bao nhiêu RP lên bậc,
 * chuỗi ngày, mục tiêu tuần, "Cách tăng RP") → cảnh báo là một dòng nhỏ. Việc là việc CÁ NHÂN theo dữ liệu của em;
 * ghi chú chung của GV không nằm ở đây (thầy chốt 8/10/2026) mà ở khối "Thầy nhắn" riêng, thấp hơn.
 * Mọi con số RP lấy từ rank_my_status (cấu hình mùa thật), không chép cứng từ tài liệu.
 * Thứ tự việc do trang chủ quyết: bài kiểm tra được giao → BTVN ôn tập → rankNextSteps (mở khoá phụ đạo →
 * làm lại đề điểm thấp → học bài kế → ôn lại). Không có gì để hiện → trang chủ không render thẻ này (N3).
 * Bước "unlock" không có href: bấm gọi onUnlock để mở bài tự kiểm tra; đang chờ giãn cách thì mờ.
 */
export default function TodayCard({
  primary,
  secondary,
  alertText,
  rank,
  onUnlock,
}: {
  primary: NextStep | null;
  secondary: NextStep[];
  alertText: string | null;
  rank?: RankStatus | null;
  onUnlock: (needId: number) => void;
}) {
  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <div className="flex items-center gap-2">
        <Megaphone size={18} className="text-blue-300" />
        <h2 className="font-display font-bold text-white">Hôm nay em làm gì</h2>
      </div>
      <div className="mt-3 space-y-2.5">
        {primary && <PrimaryStep step={primary} onUnlock={onUnlock} />}
        {primary && <PrimaryReward step={primary} rank={rank} />}

        {secondary.length > 0 && (
          <ul className="space-y-0.5">
            {secondary.map((step) => (
              <li key={step.key}>
                <SecondaryStep step={step} onUnlock={onUnlock} />
              </li>
            ))}
          </ul>
        )}

        <RpStrip rank={rank} />

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

function fmt(n: number) {
  return String(n).replace(".", ",");
}

/**
 * Dòng "làm xong được gì" dưới nút nổi. Chỉ nói điều đúng với luật RP hiện hành:
 * RP của một bài chỉ tính lần làm ĐẦU TIÊN (làm lại không cộng thêm) nhưng làm lại vẫn giữ chuỗi/góp mục tiêu tuần.
 */
function PrimaryReward({ step, rank }: { step: NextStep; rank?: RankStatus | null }) {
  const daily = rank?.season ? rank.daily : null;
  const lines: string[] = [];
  if (step.kind === "assigned") lines.push("RP của bài tính theo điểm lần làm đầu tiên, nên em cứ làm cẩn thận.");
  if (step.kind === "retry") lines.push("Làm lại không cộng thêm RP bài này, nhưng giúp em nắm chắc hơn.");
  if (daily && !daily.today_done && daily.rp > 0 && (step.kind === "assigned" || step.kind === "retry")) {
    lines.push(`Đạt từ ${fmt(daily.min_score)} điểm → giữ chuỗi ngày, +${daily.rp} RP.`);
  }
  if (lines.length === 0) return null;
  return (
    <ul className="space-y-0.5 px-1 text-[13px] text-slate-300">
      {lines.map((line) => (
        <li key={line}>{line}</li>
      ))}
    </ul>
  );
}

/** Dải RP: còn bao nhiêu RP lên bậc, chuỗi, mục tiêu tuần + "Cách tăng RP" (trả lời câu "em không biết làm gì để tăng RP"). */
function RpStrip({ rank }: { rank?: RankStatus | null }) {
  if (!rank?.season) return null;
  const { next, daily, weekly } = rank;
  const items: React.ReactNode[] = [];
  if (next) {
    items.push(
      <li key="next" className="flex items-center gap-1.5">
        <Trophy size={14} className="shrink-0 text-amber-300" />
        <span>
          Còn <b className="text-white">{next.rp_needed} RP</b> lên {next.name}
          {next.gate && !next.gate.passed && <span className="text-slate-400"> (có thêm điều kiện lên bậc)</span>}
        </span>
      </li>,
    );
  }
  if (daily) {
    items.push(
      <li key="streak" className="flex items-center gap-1.5">
        <Flame size={14} className={`shrink-0 ${daily.today_done ? "text-amber-400" : "text-slate-500"}`} />
        <span>
          {daily.today_done
            ? `Hôm nay đã giữ chuỗi ${daily.streak} ngày ✓`
            : `Chuỗi ${daily.streak} ngày · giữ hôm nay +${daily.rp} RP`}
        </span>
      </li>,
    );
  }
  if (weekly) {
    items.push(
      <li key="week" className="flex items-center gap-1.5">
        <Target size={14} className={`shrink-0 ${weekly.achieved ? "text-emerald-300" : "text-slate-500"}`} />
        <span>
          {weekly.achieved
            ? `Đã đủ mục tiêu tuần ✓`
            : `Tuần này ${weekly.done}/${weekly.target} bài (từ ${fmt(weekly.min_score)} điểm) → +${weekly.rp} RP`}
        </span>
      </li>,
    );
  }
  return (
    <div className="border-t border-white/10 pt-2.5">
      {items.length > 0 && <ul className="space-y-1.5 text-[13px] text-slate-300">{items}</ul>}
      <details className="mt-1 text-[13px] text-slate-300">
        <summary className="flex min-h-11 cursor-pointer items-center text-blue-200 hover:text-white">Cách tăng RP</summary>
        <ul className="space-y-1.5 pb-1 pl-4 text-slate-300">
          <li className="list-disc">Làm bài lần đầu: RP tính theo điểm. Làm lại không cộng thêm RP bài đó.</li>
          <li className="list-disc">Đọc lý thuyết rồi làm đúng phần lớn câu kiểm tra nhanh cuối bài.</li>
          <li className="list-disc">Mỗi ngày làm ít nhất một bài đạt điểm tối thiểu để giữ chuỗi.</li>
          <li className="list-disc">Đủ số bài trong tuần để nhận RP mục tiêu tuần.</li>
          <li className="list-disc">Sửa lại chủ đề đã sai và làm tốt hơn hai tuần trước để nhận RP sửa sai, tiến bộ.</li>
        </ul>
      </details>
    </div>
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
