"use client";

import { useEffect, useMemo, useState } from "react";
import { fetchHomeworkOverview, type HomeworkOverviewRow } from "@/services/ta-homework";

const dateText = (iso: string | null) =>
  iso ? new Date(iso).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }) : "không đặt hạn";

/** Bài đã giao riêng 3 tuần gần nhất của một lớp: ai đã làm, điểm, ai trễ hạn. Nhóm theo đề, em chưa làm đứng trước. */
export default function TaHomeworkOverview({ classId }: { classId: number }) {
  const [rows, setRows] = useState<HomeworkOverviewRow[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let alive = true;
    setRows(null);
    setError(false);
    fetchHomeworkOverview(classId)
      .then((data) => alive && setRows(data))
      .catch(() => alive && setError(true));
    return () => {
      alive = false;
    };
  }, [classId]);

  const groups = useMemo(() => {
    const map = new Map<number, { title: string; dueAt: string | null; items: HomeworkOverviewRow[] }>();
    for (const row of rows ?? []) {
      const group = map.get(row.examId) ?? { title: row.examTitle, dueAt: row.dueAt, items: [] };
      group.items.push(row);
      map.set(row.examId, group);
    }
    return Array.from(map.entries());
  }, [rows]);

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <h3 className="font-display font-bold text-white">Bài về nhà đã giao riêng (3 tuần gần nhất)</h3>
      {error ? (
        <p className="mt-3 text-xs text-slate-500">Chưa tải được danh sách.</p>
      ) : rows === null ? (
        <p className="mt-3 text-xs text-slate-500">Đang tải…</p>
      ) : groups.length === 0 ? (
        <p className="mt-3 text-xs text-slate-500">Chưa giao bài riêng nào. Giao ở bước cuối của phiếu phụ đạo.</p>
      ) : (
        <div className="mt-3 space-y-3">
          {groups.map(([examId, group]) => {
            const done = group.items.filter((i) => i.done).length;
            return (
              <div key={examId} className="rounded-xl bg-white/[.02] p-3">
                <p className="text-sm font-semibold text-slate-100">{group.title}</p>
                <p className="mt-0.5 text-[12px] text-slate-400">
                  Hạn {dateText(group.dueAt)} · đã làm {done}/{group.items.length} em
                </p>
                <ul className="mt-2 space-y-1">
                  {group.items.map((item) => (
                    <li key={item.id} className="flex items-center justify-between gap-3 text-sm">
                      <span className="min-w-0 truncate text-slate-200">{item.studentName || "Học sinh"}</span>
                      {item.done ? (
                        <span className="shrink-0 text-emerald-300">
                          Đã làm{item.bestScore !== null ? ` · ${item.bestScore.toLocaleString("vi-VN")} điểm` : ""}
                        </span>
                      ) : item.late ? (
                        <span className="shrink-0 font-semibold text-amber-300">Trễ hạn, chưa làm</span>
                      ) : (
                        <span className="shrink-0 text-slate-400">Chưa làm</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
