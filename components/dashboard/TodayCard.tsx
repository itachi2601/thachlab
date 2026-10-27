"use client";

import Link from "next/link";
import { AlertTriangle, ChevronRight } from "lucide-react";
import type { RankStatus } from "@/features/rank/types";
import { formatExitWait } from "@/services/tutoring";
import StreakWeek from "@/components/rank/StreakWeek";
import type { StreakDay } from "@/services/rank";
import type { NextStep } from "@/features/learning/next-steps";

/**
 * Thẻ "Hôm nay em làm gì" — thẻ DUY NHẤT gợi việc ở trang chủ HS (N4, B2, L5). Việc THÍCH ỨNG theo hồ sơ của em, cộng
 * (từ 17/10/2026) đề kiểm tra lớp đã giao mà em chưa làm — chung 2 suất đầu với BTVN, xem features/learning/next-steps.ts:
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
  days,
  doneToday = 0,
  onUnlock,
  onQuickPractice,
}: {
  /** Số bài em đã nộp hôm nay — dòng "Hôm nay đã xong n bài" để em thấy mình tiến tới đâu (không cộng RP riêng, L3). */
  doneToday?: number;
  primary: NextStep | null;
  secondary: NextStep[];
  alertText: string | null;
  rank?: RankStatus | null;
  /** Dải 7 ngày giữ chuỗi: chỉ hiện ở thẻ này (chuỗi ngày không lặp ở nơi khác trên trang chủ). */
  days?: StreakDay[] | null;
  onUnlock: (needId: number) => void;
  onQuickPractice: (step: NextStep) => void;
}) {
  const act = { onUnlock, onQuickPractice };
  const steps = [primary, ...secondary].filter((s): s is NextStep => s !== null);
  return (
    <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="font-display font-bold text-ink">Việc hôm nay</h2>
        {steps.length > 0 && <span className="text-[13px] text-muted">còn {steps.length} việc</span>}
      </div>
      {doneToday > 0 && (
        <p className="mt-1 text-[13px] font-semibold text-ok">✓ Hôm nay em đã xong {doneToday} bài</p>
      )}
      {steps.length > 0 && (
        <ul className="mt-1">
          {steps.map((step, i) => (
            <li key={step.key} className={i > 0 ? "border-t border-line" : ""}>
              <StepRow step={step} {...act} />
            </li>
          ))}
        </ul>
      )}
      {primary && <StartButton step={primary} {...act} />}

      {days && days.length > 0 && <StreakWeek days={days} className="mt-4" />}

      <div className="mt-3 space-y-2.5">
        <RpFoot rank={rank} />

        {alertText && (
          <p className="flex items-start gap-1.5 text-[13px] text-warn">
            <AlertTriangle size={14} className="mt-0.5 shrink-0 text-warn" />
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
    <div className="border-t border-line pt-2.5 text-[13px] text-ink">
      {lines.length > 0 && (
        <ul className="space-y-1.5">
          {lines.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      )}
      <details>
        <summary className="flex min-h-11 cursor-pointer items-center text-primary hover:underline">Cách tăng RP</summary>
        <ul className="space-y-1.5 pb-1 pl-4 text-ink">
          <li className="list-disc">Bài tính RP: RP theo điểm em đạt. Làm lại điểm cao hơn thì được cộng phần chênh.</li>
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

const KIND_TAG: Record<NextStep["kind"], { label: string; cls: string }> = {
  session: { label: "Ôn tập", cls: "bg-primary-soft text-primary" },
  homework: { label: "Bài về nhà", cls: "bg-primary-soft text-primary" },
  assigned: { label: "Kiểm tra lớp", cls: "bg-warn/10 text-warn" },
  unlock: { label: "Phụ đạo", cls: "bg-warn/10 text-warn" },
  weak: { label: "Kỹ năng yếu", cls: "bg-primary-soft text-primary" },
  retry: { label: "Làm lại", cls: "bg-primary-soft text-primary" },
  lesson: { label: "Học tiếp", cls: "bg-ok/10 text-ok" },
  review: { label: "Ôn lại", cls: "bg-ok/10 text-ok" },
};

/** Một việc = một hàng: nhãn loại · tên việc · gợi ý nhỏ. Cả hàng là vùng bấm (đích chạm ≥56px). */
function StepRow({ step, ...act }: { step: NextStep } & Act) {
  const hint = stepHint(step);
  const tag = KIND_TAG[step.kind];
  return (
    <StepControl step={step} {...act} className="flex min-h-14 w-full items-center gap-3 py-2.5 text-left disabled:opacity-50">
      <span className={`shrink-0 rounded-md px-2 py-0.5 text-[12px] font-bold ${tag.cls}`}>{tag.label}</span>
      <span className="min-w-0 flex-1">
        <span className="block text-sm font-semibold text-ink">{step.title}</span>
        {hint && <span className="mt-0.5 block text-[13px] leading-snug text-muted">{hint}</span>}
      </span>
      <ChevronRight size={16} className="shrink-0 text-muted" />
    </StepControl>
  );
}

/** Nút nổi duy nhất của trang (B2): bắt đầu việc đầu tiên. */
function StartButton({ step, ...act }: { step: NextStep } & Act) {
  return (
    <StepControl
      step={step}
      {...act}
      className="mt-3 flex min-h-12 w-full items-center justify-center rounded-xl bg-primary px-4 text-sm font-bold text-white hover:bg-primary-dark disabled:opacity-60"
    >
      Bắt đầu việc đầu tiên
    </StepControl>
  );
}
