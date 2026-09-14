"use client";

import { useState } from "react";
import { CalendarCheck, NotebookPen } from "lucide-react";
import HomeroomDailyReport from "@/components/dashboard/HomeroomDailyReport";
import HomeroomWeeklyEditor from "@/components/dashboard/HomeroomWeeklyEditor";

type Student = { id: string; name: string; className: string };

/** Tab "Sinh hoạt lớp" của GVCN: theo dõi điểm danh hàng ngày + soạn nội dung sinh hoạt tuần. */
export default function HomeroomShcnPanel({ courseId, students }: { courseId: number; students: Student[] }) {
  const [view, setView] = useState<"daily" | "weekly">("daily");

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-2">
        {([["daily", "Điểm danh hàng ngày", CalendarCheck], ["weekly", "Nội dung sinh hoạt tuần", NotebookPen]] as const).map(([id, label, Icon]) => (
          <button
            key={id}
            onClick={() => setView(id)}
            className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === id ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}
          >
            <Icon size={16} />{label}
          </button>
        ))}
      </div>
      {view === "daily" ? <HomeroomDailyReport courseId={courseId} students={students} /> : <HomeroomWeeklyEditor courseId={courseId} />}
    </div>
  );
}
