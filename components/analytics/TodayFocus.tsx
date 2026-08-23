"use client";

import { useEffect, useState } from "react";
import { Flame, Sparkles, Target } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchWrongTopicStats, type TopicStats } from "@/services/analytics";
import { fetchStudyStreak, type DailyStreak } from "@/services/daily-progress";

/** Gợi ý "hôm nay nên học gì" + chuỗi ngày học liên tiếp, đặt đầu trang đề thi. */
export default function TodayFocus({ onReview }: { onReview: (topic: string) => void }) {
  const { session } = useAuth();
  const [streak, setStreak] = useState<DailyStreak | null>(null);
  const [weakest, setWeakest] = useState<TopicStats | null>(null);

  useEffect(() => {
    if (!session?.user.id) return;
    fetchStudyStreak(session.user.id).then(setStreak);
    fetchWrongTopicStats(session.user.id).then((stats) => setWeakest(stats[0] ?? null));
  }, [session?.user.id]);

  if (!session || !streak) return null;

  return (
    <div className="rounded-2xl border border-blue-500/20 bg-gradient-to-r from-blue-500/10 to-transparent p-5">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-orange-500/15 text-orange-300">
            <Flame size={20} />
          </span>
          <div>
            <p className="font-display text-lg font-bold text-white">
              {streak.current > 0
                ? `${streak.current} ngày học liên tiếp`
                : "Bắt đầu chuỗi ngày học của em"}
            </p>
            <p className="text-sm text-slate-400">
              {streak.activeToday
                ? "Hôm nay đã học — giữ vững phong độ nhé!"
                : "Chưa có hoạt động hôm nay. Học một chút để giữ chuỗi."}
            </p>
          </div>
        </div>

        {weakest ? (
          <button
            onClick={() => onReview(weakest.topic)}
            className="flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-500"
          >
            <Target size={16} />
            Hôm nay ôn: {weakest.topic} ({weakest.percentage}% sai)
          </button>
        ) : (
          <span className="flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2.5 text-sm text-slate-400">
            <Sparkles size={16} />
            Làm 1 đề để bắt đầu phân tích chủ đề
          </span>
        )}
      </div>
    </div>
  );
}
