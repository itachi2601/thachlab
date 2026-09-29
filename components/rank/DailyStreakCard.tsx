"use client";

import { Flame } from "lucide-react";
import { type RankStatus } from "@/features/rank/types";

/**
 * Chuỗi ngày kiểu Duolingo/Snapchat: ngọn lửa sáng khi hôm nay đã giữ chuỗi
 * (làm >= 1 bài tính RP đạt điểm tối thiểu), kèm một dòng gợi ý việc nên làm —
 * không phải nhiệm vụ bắt buộc, chỉ là gợi ý để giữ chuỗi hoặc tiến gần mục tiêu tuần.
 * status = undefined → đang tải; chưa mở mùa / chưa có khối daily → ẩn thẻ.
 */
export default function DailyStreakCard({
  status,
  suggestion,
  className = "",
}: {
  status: RankStatus | null | undefined;
  /** Gợi ý việc nên làm hôm nay, hiện khi chưa giữ chuỗi. */
  suggestion?: string | null;
  className?: string;
}) {
  if (status === undefined) {
    return <div className={`h-[72px] animate-pulse rounded-2xl bg-white/5 ${className}`} />;
  }
  if (!status?.season || !status.daily) return null;

  const { streak, today_done, min_score, rp } = status.daily;

  return (
    <div
      className={`flex items-center gap-3 rounded-2xl border p-4 sm:p-5 ${className}`}
      style={{
        borderColor: today_done ? "#f59e0b55" : "rgba(255,255,255,.1)",
        background: today_done ? "linear-gradient(135deg, #f59e0b26 0%, rgba(11,16,32,0) 60%)" : undefined,
      }}
    >
      <span
        className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full ${
          today_done ? "bg-amber-500/20" : "bg-white/5"
        }`}
      >
        <Flame size={22} className={today_done ? "text-amber-400" : "text-slate-600"} fill={today_done ? "currentColor" : "none"} />
      </span>
      <div className="min-w-0 flex-1">
        <p className="font-display text-base font-bold text-white">
          {streak > 0 ? `Chuỗi ${streak} ngày` : "Bắt đầu chuỗi ngày"}
          {today_done && <span className="ml-2 text-xs font-normal text-emerald-300">đã giữ hôm nay ✓</span>}
        </p>
        <p className="mt-0.5 truncate text-sm text-slate-400">
          {today_done
            ? `+${rp} RP hôm nay — quay lại ngày mai để chuỗi không gãy.`
            : suggestion || `Làm 1 bài đạt từ ${String(min_score).replace(".", ",")} điểm hôm nay để giữ chuỗi (+${rp} RP).`}
        </p>
      </div>
    </div>
  );
}
