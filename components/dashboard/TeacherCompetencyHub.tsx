"use client";

import { useState } from "react";
import { ClipboardCheck, FileCheck2, Grid3x3 } from "lucide-react";
import type { CncLearningRecord } from "@/services/cnc-learning-records";
import ClassCompetencyMatrix from "@/components/competencies/ClassCompetencyMatrix";
import TeacherChecklistPanel from "@/components/dashboard/TeacherChecklistPanel";
import TeacherDrawingApprovals from "@/components/dashboard/TeacherDrawingApprovals";

type Student = { id: string; name: string; className: string; records: CncLearningRecord[] };

export default function TeacherCompetencyHub({ courseId, students }: { courseId: number; students: Student[] }) {
  const [view, setView] = useState<"approvals" | "checklist" | "matrix">("approvals");
  const [pendingCount, setPendingCount] = useState(0);

  return <div className="space-y-5">
    <div className="flex flex-wrap gap-2">
      <button onClick={() => setView("approvals")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === "approvals" ? "border-emerald-400/40 bg-emerald-500/10 text-emerald-200" : "border-white/10 text-slate-400"}`}><FileCheck2 size={16} />Duyệt hồ sơ{pendingCount > 0 ? ` · ${pendingCount}` : ""}</button>
      <button onClick={() => setView("checklist")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === "checklist" ? "border-violet-400/40 bg-violet-500/10 text-violet-200" : "border-white/10 text-slate-400"}`}><ClipboardCheck size={16} />Chấm chéo checklist</button>
      <button onClick={() => setView("matrix")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view === "matrix" ? "border-blue-400/40 bg-blue-500/10 text-blue-200" : "border-white/10 text-slate-400"}`}><Grid3x3 size={16} />Ma trận năng lực</button>
    </div>

    {view === "approvals" && <TeacherDrawingApprovals courseId={courseId} onPendingCountChange={setPendingCount} />}
    {view === "checklist" && <TeacherChecklistPanel courseId={courseId} students={students.map(item => ({ id: item.id, name: item.name, className: item.className }))} />}
    {view === "matrix" && <ClassCompetencyMatrix courseId={courseId} students={students} />}
  </div>;
}
