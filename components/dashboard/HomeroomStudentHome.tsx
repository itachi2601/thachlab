"use client";

import { useEffect, useState } from "react";
import { CalendarCheck, ClipboardList, UserCheck } from "lucide-react";
import StudentAttendancePanel from "@/components/attendance/StudentAttendancePanel";
import MonitorDailyAttendancePanel from "@/components/attendance/MonitorDailyAttendancePanel";
import ShcnWeekList from "@/components/dashboard/ShcnWeekList";
import { MONITOR_ROLE_LABEL, fetchMyMonitorRoles, type MonitorRole } from "@/services/homeroom-shcn";

type Tab = "weeks" | "attendance" | "monitor";

/**
 * Không gian lớp chủ nhiệm của sinh viên: xem lại nội dung sinh hoạt tuần, điểm danh tiết SHCN
 * của mình, và — nếu là lớp trưởng/lớp phó — nhập điểm danh hàng ngày cho cả lớp.
 */
export default function HomeroomStudentHome({ courseId, courseName, schoolYear, studentId }: {
  courseId: number;
  courseName: string;
  schoolYear: string;
  studentId: string;
}) {
  const [monitorRole, setMonitorRole] = useState<MonitorRole | null>(null);
  const [tab, setTab] = useState<Tab>("weeks");

  useEffect(() => {
    let cancelled = false;
    fetchMyMonitorRoles(studentId)
      .then((rows) => {
        if (cancelled) return;
        const role = rows.find((row) => row.course_id === courseId)?.role ?? null;
        setMonitorRole(role);
        // Lớp trưởng vào là thấy ngay việc phải làm mỗi ngày.
        if (role) setTab("monitor");
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [courseId, studentId]);

  const tabs: { id: Tab; label: string; icon: typeof ClipboardList }[] = [
    { id: "weeks", label: "Sinh hoạt lớp", icon: ClipboardList },
    { id: "attendance", label: "Điểm danh của tôi", icon: CalendarCheck },
    ...(monitorRole ? [{ id: "monitor" as const, label: `Điểm danh lớp (${MONITOR_ROLE_LABEL[monitorRole]})`, icon: UserCheck }] : []),
  ];

  return (
    <>
      <div className="mb-5 flex flex-wrap items-center gap-2 rounded-2xl border border-emerald-400/25 bg-emerald-500/10 px-5 py-3 text-sm text-emerald-200">
        <strong>{courseName}</strong><span>· {schoolYear}</span>
      </div>

      <nav className="mb-5 flex gap-2 overflow-x-auto rounded-2xl border border-white/10 bg-[#080d1d] p-2">
        {tabs.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setTab(item.id)}
              className={`inline-flex shrink-0 items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-bold ${tab === item.id ? "bg-blue-600 text-white" : "text-slate-400 hover:bg-white/5 hover:text-white"}`}
            >
              <Icon size={16} />{item.label}
            </button>
          );
        })}
      </nav>

      {tab === "weeks" && <ShcnWeekList courseId={courseId} />}
      {tab === "attendance" && <StudentAttendancePanel courseId={courseId} studentId={studentId} />}
      {tab === "monitor" && monitorRole && <MonitorDailyAttendancePanel courseId={courseId} role={monitorRole} />}
    </>
  );
}
