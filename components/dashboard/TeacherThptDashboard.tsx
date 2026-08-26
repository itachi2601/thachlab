"use client";

import { useEffect, useState } from "react";
import { CalendarCheck, GraduationCap, LayoutDashboard, UserRound } from "lucide-react";
import type { SchoolClass } from "@/features/exams/types";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchClasses, fetchClassStudents, type ClassStudent } from "@/services/classes";
import { fetchInstructorClasses } from "@/services/class-instructors";
import TeacherThptOverview from "@/components/dashboard/TeacherThptOverview";
import TeacherThptGradebook from "@/components/dashboard/TeacherThptGradebook";
import TeacherThptStudentProfile from "@/components/dashboard/TeacherThptStudentProfile";
import TeacherThptAttendancePanel from "@/components/attendance/TeacherThptAttendancePanel";

type DashboardTab = "overview" | "gradebook" | "profile" | "attendance";

const TABS: { id: DashboardTab; label: string; icon: typeof LayoutDashboard }[] = [
  { id: "overview", label: "Tổng quan", icon: LayoutDashboard },
  { id: "gradebook", label: "Bảng điểm", icon: GraduationCap },
  { id: "profile", label: "Hồ sơ học sinh", icon: UserRound },
  { id: "attendance", label: "Điểm danh", icon: CalendarCheck },
];

export default function TeacherThptDashboard() {
  const { profile } = useAuth();
  const isAdmin = profile?.role === "admin";
  const [activeTab, setActiveTab] = useState<DashboardTab>("overview");
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [selectedClassId, setSelectedClassId] = useState<number | null>(null);
  const [students, setStudents] = useState<ClassStudent[]>([]);
  const [selectedStudentId, setSelectedStudentId] = useState<string | null>(null);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    if (!profile) return;
    let cancelled = false;
    const load = isAdmin ? fetchClasses() : fetchInstructorClasses(profile.id);
    load
      .then((rows) => {
        if (cancelled) return;
        setClasses(rows);
        setSelectedClassId((current) => (rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null));
        setLoadError("");
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        setLoadError(error instanceof Error ? error.message : "Không tải được danh sách lớp.");
      });
    return () => { cancelled = true; };
  }, [profile, isAdmin]);

  useEffect(() => {
    if (!selectedClassId) { setStudents([]); return; }
    let cancelled = false;
    fetchClassStudents(selectedClassId)
      .then((rows) => {
        if (cancelled) return;
        setStudents(rows);
        setSelectedStudentId((current) => (rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null));
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        setStudents([]);
        setLoadError(error instanceof Error ? error.message : "Không tải được danh sách học sinh.");
      });
    return () => { cancelled = true; };
  }, [selectedClassId]);

  const selectedClass = classes.find((item) => item.id === selectedClassId) ?? null;

  return (
    <div className="teacher-dashboard space-y-6">
      <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] via-[#0e1c32] to-[#071426] p-6 sm:p-8">
        <div className="absolute -right-20 -top-24 h-64 w-64 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="relative">
          <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">Dashboard giáo viên · THPT</p>
          <h2 className="mt-2 font-display text-2xl font-bold text-white">Chào {profile?.full_name || "thầy/cô"} 👋</h2>
          <p className="mt-2 text-sm text-slate-400">
            {selectedClass ? `Đang xem lớp ${selectedClass.name} · ${students.length} học sinh` : "Chọn khối lớp bên dưới để bắt đầu theo dõi học sinh."}
          </p>
          {loadError && <p className="mt-2 text-xs text-red-300">{loadError}</p>}
        </div>
      </section>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-4 sm:p-5">
        <label className="block">
          <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">
            Lớp đang dạy{classes.length > 0 && ` · ${classes.length} lớp`}
          </span>
          <select
            aria-label="Lớp đang dạy"
            value={selectedClassId ?? ""}
            onChange={(event) => setSelectedClassId(Number(event.target.value))}
            className="w-full max-w-sm rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm font-semibold text-white"
          >
            <option value="" disabled>{classes.length ? "Chọn khối lớp" : "Chưa được phân công lớp nào"}</option>
            {classes.map((item) => (
              <option key={item.id} value={item.id}>{item.icon ? `${item.icon} ` : ""}{item.name}</option>
            ))}
          </select>
        </label>
      </section>

      <nav className="sticky top-20 z-40 flex gap-2 overflow-x-auto rounded-2xl border border-white/10 bg-[#080d1d]/95 p-2 shadow-xl backdrop-blur">
        {TABS.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`inline-flex shrink-0 items-center gap-2 rounded-xl px-4 py-3 text-sm font-bold ${
                activeTab === tab.id ? "bg-blue-600 text-white" : "text-slate-400 hover:bg-white/5 hover:text-white"
              }`}
            >
              <Icon size={17} />{tab.label}
            </button>
          );
        })}
      </nav>

      {!selectedClassId ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-10 text-center text-sm text-slate-500">
          Chưa có lớp nào để hiển thị.
        </p>
      ) : (
        <>
          {activeTab === "overview" && <TeacherThptOverview classId={selectedClassId} students={students} onOpenTab={setActiveTab} onOpenStudent={(id) => { setSelectedStudentId(id); setActiveTab("profile"); }} />}
          {activeTab === "gradebook" && <TeacherThptGradebook students={students} />}
          {activeTab === "profile" && <TeacherThptStudentProfile classId={selectedClassId} students={students} selectedId={selectedStudentId} onSelect={setSelectedStudentId} />}
          {activeTab === "attendance" && <TeacherThptAttendancePanel classId={selectedClassId} students={students} />}
        </>
      )}
    </div>
  );
}
