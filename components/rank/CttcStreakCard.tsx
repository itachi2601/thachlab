"use client";

import { useEffect, useState } from "react";
import DailyStreakCard from "@/components/rank/DailyStreakCard";
import { fetchMyRankStatus, fetchMyStreakDays, type StreakDay } from "@/services/rank";
import type { RankStatus } from "@/features/rank/types";

/** Chuỗi ngày cho sinh viên CTTC: giữ chuỗi, không hiện RP/hạng. */
export default function CttcStreakCard({ className = "" }: { className?: string }) {
  const [rank, setRank] = useState<RankStatus | null | undefined>(undefined);
  const [days, setDays] = useState<StreakDay[] | null>(null);
  useEffect(() => {
    let cancelled = false;
    fetchMyRankStatus().then((s) => !cancelled && setRank(s)).catch(() => !cancelled && setRank(null));
    fetchMyStreakDays().then((d) => !cancelled && setDays(d));
    return () => { cancelled = true; };
  }, []);
  return <DailyStreakCard status={rank} days={days} hideRp className={className} />;
}
