"use client";

import Link from "next/link";
import { AlertTriangle, ChevronRight } from "lucide-react";
import type { RankStatus } from "@/features/rank/types";
import { formatExitWait } from "@/services/tutoring";
import type { NextStep } from "@/features/learning/next-steps";

/**
 * Thẻ "Hôm nay em làm gì" — thẻ DUY NHẤT gợi việc ở trang chủ HS (N4, B2, L5). Từ 8/10/2026 (thầy chốt) chỉ có việc THÍCH ỨNG
 * theo hồ sơ của em, không còn việc/bài giao chung cho cả lớp (bài kiểm tra mới báo qua chuông thông báo):
 * MỘT nút nổi (việc đầu: chủ đề phụ đạo → kỹ năng yếu; không có chỗ hổng thì "Học tiếp" kèm lời động viên)
 * → tối đa 3 lựa chọn khác dạng hàng có gợi ý → chân thẻ: RP hôm nay/tuần + "Cách tăng RP" → cảnh báo là một dòng nhỏ.
 * Bước "unlock" không có href: bấm gọi onUnlock. Bước "weak": bấm mở luyện nhanh 10 câu (onQuickPractice).
 * Mọi con số RP lấy từ rank_my_status (cấu hình mùa thật), không chép cứng. Chuỗi ngày và RP còn thiếu nằm ở khung chào.
 */
export default function TodayCard({
  primary,
  secondary,
  alertText,
  rank,
  onUnlock,
  onQuickPractice,
}: {
  primary: NextStep | null;
  secondary: NextStep[];
  alertText: string | null;
  rank?: RankStatus | null;
  onUnlock: (needId: number) => void;
  onQuickPractice: (step: NextStep) => void;
}) {
  const act = { onUnlock, onQuickPractice };
  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <h2 className="font-display font-bold text-white">Hôm nay em làm gì</h2>
      <div className="mt-3 space-y-2.5">
        {primary && <PrimaryStep step={primary} {...act} />}

        {secondary.length > 0 && (
          <>
            <p className="pt-1 text-[13px] font-bold uppercase tracking-wide text-slate-400">Hoặc em chọn một việc khác</p>
            <ul className="space-y-2">
              {secondary.map((step) => (
                <li key={step.key}>
                  <OptionStep step={step} {...act} />
                </li>
              ))}
            </ul>
          </>
        )}

        <RpFoot rank={rank} />

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

/** Chân thẻ: một dòng cho việc giữ chuỗi hôm nay, một dòng mục tiêu tuần, và mục thu gọn "Cách tăng RP". */
function RpFoot({ rank }: { rank?: RankStatus | null }) {
  if (!rank?.season) return null;
  const { daily, weekly } = rank;
  const lines: string[] = [];
  if (daily && !daily.today_done && daily.rp > 0) {
    lines.push(`Hôm nay chưa giữ chuỗi: làm một bài đạt từ ${fmt(daily.min_score)} điểm để nhận +${daily.rp} RP.`);
  }
  if (weekly && !weekly.achieved) {
    lines.push(`Tuần này ${weekly.done}/${weekly.target} bài (từ ${fmt(weekly.min_score)} điểm). Đủ bài nhận +${weekly.rp} RP.`);
  }
  return (
    <div className="border-t border-white/10 pt-2.5 text-[13px] text-slate-300">
      {lines.length > 0 && (
        <ul className="space-y-1.5">
          {lines.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      )}
      <details>
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

type Act = { onUnlock: (needId: number) => void; onQuickPractice: (step: NextStep) => void };

/** Bước có href → liên kết; weak → luyện nhanh; unlock → mở bài tự kiểm tra. */
function StepControl({ step, className, children, onUnlock, onQuickPractice }: { step: NextStep; className: string; children: React.ReactNode } & Act) {
  if (step.practice) {
    return (
      <button type="button" onClick={() => onQuickPractice(step)} className={className}>
        {children}
      </button>
    );
  }
  if (step.href) {
    return (
      <Link href={step.href} className={className}>
        {children}
      </Link>
    );
  }
  return (
    <button
      type="button"
      disabled={Boolean(step.lockedUntil)}
      onClick={() => step.needId !== undefined && onUnlock(step.needId)}
      className={className}
    >
      {children}
    </button>
  );
}

function PrimaryStep({ step, ...act }: { step: NextStep } & Act) {
  const hint = stepHint(step);
  return (
    <StepControl
      step={step}
      {...act}
      className="flex min-h-14 w-full items-center justify-between gap-3 rounded-xl bg-primary p-3 text-left text-white hover:bg-primary-dark disabled:opacity-60"
    >
      <span className="min-w-0">
        <small className="block text-[13px] font-bold uppercase tracking-wider text-blue-100">{step.action}</small>
        <span className="mt-0.5 block text-sm font-bold">{step.title}</span>
        {hint && <span className="mt-0.5 block text-[13px] leading-snug text-blue-100">{hint}</span>}
      </span>
      <ChevronRight className="shrink-0" size={18} />
    </StepControl>
  );
}

function OptionStep({ step, ...act }: { step: NextStep } & Act) {
  const hint = stepHint(step);
  return (
    <StepControl
      step={step}
      {...act}
      className="flex min-h-14 w-full items-center justify-between gap-3 rounded-xl border border-white/10 bg-white/5 p-3 text-left hover:bg-white/10 disabled:opacity-50"
    >
      <span className="min-w-0">
        <span className="block text-sm font-bold text-white">
          {step.action}: {step.title}
        </span>
        {hint && <span className="mt-0.5 block text-[13px] leading-snug text-slate-400">{hint}</span>}
      </span>
      <ChevronRight size={16} className="shrink-0 text-slate-500" />
    </StepControl>
  );
}
