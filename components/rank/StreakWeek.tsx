"use client";

import { Flame, Snowflake } from "lucide-react";
import type { StreakDay } from "@/services/rank";

const WEEKDAY = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];

function weekdayOf(iso: string) {
  // iso là ngày lịch YYYY-MM-DD (giờ VN); dựng ở giữa trưa UTC để không lệch ngày theo múi giờ máy.
  return WEEKDAY[new Date(`${iso}T12:00:00Z`).getUTCDay()];
}

/**
 * Dải 7 ngày của chuỗi (kiểu Duolingo): lửa = đã giữ chuỗi, bông tuyết = ngày trống được đóng băng, vòng rỗng = chưa làm.
 * Ngày cuối là hôm nay (viền sáng). Không dùng đỏ/cảnh báo cho ngày trống (L4: nói về việc tiếp theo, không phạt);
 * nghĩa không chỉ nằm ở màu — có icon và aria-label từng ô (M5).
 */
export default function StreakWeek({ days, className = "" }: { days: StreakDay[]; className?: string }) {
  return (
    <ol className={`grid grid-cols-7 gap-1 ${className}`} aria-label="Chuỗi 7 ngày gần nhất">
      {days.map((day, index) => {
        const today = index === days.length - 1;
        const label = `${weekdayOf(day.d)}: ${day.state === "done" ? "đã giữ chuỗi" : day.state === "frozen" ? "được đóng băng" : today ? "hôm nay, chưa làm" : "chưa làm"}`;
        return (
          <li key={day.d} className="flex flex-col items-center gap-1" aria-label={label}>
            <span className={`text-[13px] ${today ? "font-bold text-ink" : "text-muted"}`}>{weekdayOf(day.d)}</span>
            <span
              className={`flex h-9 w-9 items-center justify-center rounded-full ${
                day.state === "done" ? "bg-amber-500/20" : day.state === "frozen" ? "bg-primary-soft" : "bg-surface-2"
              } ${today ? "ring-2 ring-primary" : ""}`}
            >
              {day.state === "done" && <Flame size={18} className="text-amber-400" fill="currentColor" aria-hidden />}
              {day.state === "frozen" && <Snowflake size={16} className="text-primary" aria-hidden />}
            </span>
          </li>
        );
      })}
    </ol>
  );
}
