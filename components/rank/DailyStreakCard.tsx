"use client";

import { Flame, Snowflake } from "lucide-react";
import { type RankStatus } from "@/features/rank/types";
import type { StreakDay } from "@/services/rank";
import StreakWeek from "@/components/rank/StreakWeek";

/**
 * Chuỗi ngày kiểu Duolingo/Snapchat: ngọn lửa sáng khi hôm nay đã giữ chuỗi
 * (làm >= 1 bài tính RP đạt điểm tối thiểu), kèm một dòng gợi ý việc nên làm —
 * không phải nhiệm vụ bắt buộc, chỉ là gợi ý để giữ chuỗi hoặc tiến gần mục tiêu tuần.
 * status = undefined → đang tải; chưa mở mùa / chưa có khối daily → ẩn thẻ.
 */
export default function DailyStreakCard({
  status,
  suggestion,
  days,
  className = "",
}: {
  status: RankStatus | null | undefined;
  /** Gợi ý việc nên làm hôm nay, hiện khi chưa giữ chuỗi. */
  suggestion?: string | null;
  /** 7 ngày gần nhất; null/undefined (RPC chưa chạy) → không vẽ dải. */
  days?: StreakDay[] | null;
  className?: string;
}) {
  if (status === undefined) {
    return <div className={`h-[72px] animate-pulse rounded-2xl bg-surface-2 ${className}`} />;
  }
  if (!status?.season || !status.daily) return null;

  const { streak, today_done, min_score, rp, reset_hour, freeze_per_week = 0, freeze_used_week = 0, freeze_saved_recent } = status.daily;
  const freezeLeft = Math.max(0, freeze_per_week - freeze_used_week);

  return (
    <div className={`min-w-0 rounded-2xl border border-line bg-panel p-4 sm:p-5 ${className}`}>
      <div className="flex min-w-0 items-center gap-3">
      <span
        className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full ${
          today_done ? "bg-amber-500/20" : "bg-surface-2"
        }`}
      >
        <Flame size={22} className={today_done ? "text-warn" : "text-muted"} fill={today_done ? "currentColor" : "none"} />
      </span>
      <div className="min-w-0 flex-1">
        <p className="font-display text-base font-bold text-ink">
          {streak > 0 ? `Chuỗi ${streak} ngày` : "Bắt đầu chuỗi ngày"}
          {today_done && <span className="ml-2 text-xs font-normal text-ok">đã giữ hôm nay ✓</span>}
        </p>
        <p className="mt-0.5 truncate text-sm text-muted">
          {today_done
            ? `+${rp} RP hôm nay — quay lại ngày mai để chuỗi không gãy.`
            : suggestion || `Làm 1 bài đạt từ ${String(min_score).replace(".", ",")} điểm hôm nay để giữ chuỗi (+${rp} RP).`}
        </p>
        {freeze_per_week > 0 && streak > 0 && (
          <p className="mt-1 flex items-center gap-1 text-xs text-muted">
            <Snowflake size={12} />
            {freeze_saved_recent
              ? "Chuỗi vừa được đóng băng cứu một ngày trống — tuần này hết lượt."
              : freezeLeft > 0
                ? `Có ${freezeLeft} lượt đóng băng tuần này: lỡ 1 ngày chuỗi vẫn không gãy.`
                : "Tuần này đã dùng lượt đóng băng, đừng bỏ ngày nữa nhé."}
            {typeof reset_hour === "number" && reset_hour > 0 && (
              <span className="text-slate-500"> · Ngày mới tính từ {reset_hour}h sáng.</span>
            )}
          </p>
        )}
      </div>
      </div>
      {days && days.length > 0 && <StreakWeek days={days} className="mt-3" />}
    </div>
  );
}
