"use client";

import { useEffect, useRef, useState } from "react";
import { CheckCircle2, Clock3, Flag, Sparkles } from "lucide-react";

export default function StudySessionSummary({
  completedItems,
  currentLesson,
}: {
  completedItems: number;
  currentLesson?: string;
}) {
  const [summary, setSummary] = useState<{ minutes: number; completed: number } | null>(null);
  const startedAt = useRef(0);
  useEffect(() => { startedAt.current = Date.now(); }, []);
  function finish() {
    const minutes = Math.max(1, Math.round((Date.now() - startedAt.current) / 60_000));
    setSummary({ minutes, completed: completedItems });
  }

  if (summary) {
    return (
      <section className="rounded-2xl border border-emerald-400/20 bg-gradient-to-r from-emerald-500/10 to-cyan-500/5 p-5">
        <div className="flex items-center gap-2 text-emerald-300"><Sparkles size={18} /><strong className="font-display">Tổng kết buổi học</strong></div>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <SummaryItem icon={<Clock3 size={16} />} value={`${summary.minutes} phút`} label="Thời gian học" />
          <SummaryItem icon={<CheckCircle2 size={16} />} value={String(summary.completed)} label="Mục vừa hoàn thành" />
          <SummaryItem icon={<Flag size={16} />} value={currentLesson ?? "Chưa mở bài"} label="Điểm dừng" compact />
        </div>
        <p className="mt-4 text-sm text-slate-300">Tiến độ đã được lưu. Lần sau em có thể tiếp tục từ đúng bài này.</p>
        <button type="button" onClick={() => setSummary(null)} className="mt-3 text-xs font-semibold text-emerald-300 hover:underline">Tiếp tục học</button>
      </section>
    );
  }

  return (
    <div className="flex justify-end">
      <button type="button" onClick={finish} className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2.5 text-sm font-semibold text-slate-300 hover:border-emerald-400/30 hover:text-emerald-300">
        <Flag size={16} /> Kết thúc và xem tổng kết
      </button>
    </div>
  );
}

function SummaryItem({ icon, value, label, compact = false }: { icon: React.ReactNode; value: string; label: string; compact?: boolean }) {
  return (
    <div className="rounded-xl border border-white/10 bg-black/10 p-4">
      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-slate-400">{icon}{label}</div>
      <strong className={`mt-2 block text-white ${compact ? "truncate text-sm" : "text-xl"}`}>{value}</strong>
    </div>
  );
}
