"use client";

import { useEffect, useState } from "react";
import { CalendarClock, CheckCircle2 } from "lucide-react";
import { fetchRecentAnnouncements, type ClassAnnouncement } from "@/services/announcements";
import { fetchHomeworkChecks, type HomeworkCheck } from "@/services/homework-checks";

/** Bài tập về nhà gần đây của lớp con — đúng nội dung con thấy ở trang chủ của mình, kèm
 * tình trạng trợ giảng đã chấm bao nhiêu % (nếu đã kiểm tra trên lớp). */
export default function ParentHomeworkNotes({ classId, studentId }: { classId: number; studentId: string }) {
  const [items, setItems] = useState<ClassAnnouncement[] | null>(null);
  const [percents, setPercents] = useState<Record<number, number>>({});

  useEffect(() => {
    let cancelled = false;
    fetchRecentAnnouncements(classId, "homework", 5)
      .then(async (rows) => {
        if (cancelled) return;
        setItems(rows);
        const entries = await Promise.all(
          rows.map(async (item) => {
            const checks = await fetchHomeworkChecks(item.id).catch(() => ({}) as Record<string, HomeworkCheck>);
            return [item.id, checks[studentId]?.percent] as const;
          }),
        );
        if (cancelled) return;
        const next: Record<number, number> = {};
        for (const [id, percent] of entries) if (percent !== undefined) next[id] = percent;
        setPercents(next);
      })
      .catch(() => {
        if (!cancelled) setItems([]);
      });
    return () => {
      cancelled = true;
    };
  }, [classId, studentId]);

  if (items === null || items.length === 0) return null;

  return (
    <section className="mb-6 rounded-2xl border border-line bg-panel p-5">
      <h2 className="flex items-center gap-2 font-display font-semibold text-ink">
        <CalendarClock size={16} className="text-primary" /> Bài tập về nhà
      </h2>
      <div className="mt-3 space-y-2">
        {items.map((item) => {
          const percent = percents[item.id];
          return (
            <div key={item.id} className="rounded-xl border border-blue-400/20 bg-blue-500/5 p-3">
              <p className="whitespace-pre-wrap text-sm text-ink">{item.body}</p>
              <p className="mt-1.5 text-[12px] text-muted">
                {item.createdByName || "Giáo viên"} ·{" "}
                {new Date(item.createdAt).toLocaleString("vi-VN", {
                  day: "2-digit",
                  month: "2-digit",
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </p>
              {percent !== undefined ? (
                <p className="mt-1.5 flex items-center gap-1.5 text-[12px] font-semibold text-ok">
                  <CheckCircle2 size={12} /> Trợ giảng đã chấm trên lớp: {percent}% đã làm
                </p>
              ) : (
                // P2: chữ phụ trong khối phụ huynh phải ≥4,5:1 (nhắm 7:1) — dùng token muted
                // (đã được .parent-page nâng lên #3d4653) thay cho slate-500/#64748b.
                <p className="mt-1.5 text-[12px] text-muted">Chưa được chấm trên lớp.</p>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
