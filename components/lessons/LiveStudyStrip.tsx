"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { fetchLiveStudySummary, type LiveStudySummary } from "@/services/learning-presence";

// Khuya 23:00–04:30 (giờ VN) ẩn thẻ — khớp lời nhắc nghỉ khuya, không rủ em thức học.
function isLateNight(): boolean {
  const parts = new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Ho_Chi_Minh", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date());
  const h = Number(parts.find((p) => p.type === "hour")?.value);
  const m = Number(parts.find((p) => p.type === "minute")?.value);
  const minutes = h * 60 + m;
  return minutes >= 23 * 60 || minutes < 4 * 60 + 30;
}

/**
 * Báo live toàn trường: bao nhiêu bạn đang học, bài nào đang đông (N1, M2).
 * Ẩn danh; server đã che số khi dưới 3 em. Không có ai / lỗi / khuya → không hiện gì.
 */
export default function LiveStudyStrip({ className = "" }: { className?: string }) {
  const [data, setData] = useState<LiveStudySummary | null>(null);

  useEffect(() => {
    if (isLateNight()) return;
    let alive = true;
    const load = () => fetchLiveStudySummary().then((v) => alive && setData(v)).catch(() => undefined);
    void load();
    const timer = window.setInterval(() => { if (document.visibilityState === "visible") void load(); }, 60_000);
    return () => { alive = false; window.clearInterval(timer); };
  }, []);

  if (!data || (!data.few && data.total === 0)) return null;

  return (
    <div className={`min-w-0 rounded-2xl border border-line bg-panel p-4 ${className}`}>
      <p className="flex items-center gap-2 text-sm font-semibold text-ink">
        <span className="relative flex h-2.5 w-2.5 shrink-0">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-ok opacity-60" />
          <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-ok" />
        </span>
        {data.few ? "Vài bạn đang học cùng bạn" : `${data.total} bạn đang học cùng bạn`}
      </p>
      {data.topics.length > 0 && (
        <ul className="mt-2 space-y-1">
          {data.topics.map((t) => (
            <li key={t.lessonId}>
              <Link href={`/lop-hoc/bai?id=${t.lessonId}`} className="flex min-h-11 items-center justify-between gap-3 rounded-lg px-1 text-sm text-muted hover:text-ink">
                <span className="min-w-0 truncate">{t.title}</span>
                <span className="shrink-0 text-xs">{t.n} bạn</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
