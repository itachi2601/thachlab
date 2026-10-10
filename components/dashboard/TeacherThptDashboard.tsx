"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, BarChart3, CalendarCheck, ClipboardPen, FileSpreadsheet, GraduationCap, LayoutDashboard, LifeBuoy, ListChecks, Megaphone, UserRound } from "lucide-react";
import type { SchoolClass } from "@/features/exams/types";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchClasses, fetchClassStudents, type ClassStudent } from "@/services/classes";
import { fetchInstructorClasses } from "@/services/class-instructors";
import dynamic from "next/dynamic";
import type { ComponentProps, ComponentType } from "react";
import { LazyErrorBoundary, LazyPanelFallback } from "@/components/ui/LazyErrorBoundary";

// Mỗi tab là một chunk riêng, chỉ tải khi thầy bấm vào — JS ban đầu của trang
// chỉ còn khung + tab Tổng quan. Khung chờ giữ chiều cao tương đương một tab.
const TabSkeleton = () => <div className="min-h-[24rem] animate-pulse rounded-2xl bg-surface-2" aria-hidden />;
const TabError = () => <LazyPanelFallback />;

// Mỗi tab bọc LazyErrorBoundary: lỗi render bên trong 1 tab chỉ hỏng đúng tab
// đó, không kéo sập cả dashboard đang mở dở của giáo viên. Tên export giữ
// nguyên như cũ để không phải sửa chỗ dùng bên dưới.
function lazyTab<P extends object>(loader: () => Promise<{ default: ComponentType<P> }>) {
  const Inner = dynamic(loader, { loading: TabSkeleton });
  return function LazyTab(props: ComponentProps<typeof Inner>) {
    return (
      <LazyErrorBoundary fallback={<TabError />}>
        <Inner {...(props as P)} />
      </LazyErrorBoundary>
    );
  };
}

const TeacherThptOverview = lazyTab(() => import("@/components/dashboard/TeacherThptOverview"));
const TeacherThptGradebook = lazyTab(() => import("@/components/dashboard/TeacherThptGradebook"));
const TeacherThptAnalysis = lazyTab(() => import("@/components/dashboard/TeacherThptAnalysis"));
const TeacherThptAlerts = lazyTab(() => import("@/components/dashboard/TeacherThptAlerts"));
const TeacherThptTutoring = lazyTab(() => import("@/components/dashboard/TeacherThptTutoring"));
const TeacherThptStudentProfile = lazyTab(() => import("@/components/dashboard/TeacherThptStudentProfile"));
const TeacherThptProgress = lazyTab(() => import("@/components/dashboard/TeacherThptProgress"));
const TeacherThptAttendancePanel = lazyTab(() => import("@/components/attendance/TeacherThptAttendancePanel"));
const ClassRosterImportPanel = lazyTab(() => import("@/components/dashboard/ClassRosterImportPanel"));
const ClassAnnouncementsPanel = lazyTab(() => import("@/components/dashboard/ClassAnnouncementsPanel"));
const TeacherThptEnrollment = lazyTab(() => import("@/components/dashboard/TeacherThptEnrollment"));

type DashboardTab =
  | "overview"
  | "progress"
  | "analysis"
  | "alerts"
  | "tutoring"
  | "announcements"
  | "gradebook"
  | "profile"
  | "attendance"
  | "roster"
  | "enrollment";

const TABS: { id: DashboardTab; label: string; icon: typeof LayoutDashboard }[] = [
  { id: "overview", label: "Tổng quan", icon: LayoutDashboard },
  { id: "progress", label: "Quá trình học tập", icon: ListChecks },
  { id: "analysis", label: "Phân tích", icon: BarChart3 },
  { id: "alerts", label: "Cảnh báo phụ đạo", icon: AlertTriangle },
  { id: "tutoring", label: "Phụ đạo", icon: LifeBuoy },
  { id: "announcements", label: "Thông báo", icon: Megaphone },
  { id: "gradebook", label: "Bảng điểm", icon: GraduationCap },
  { id: "profile", label: "Hồ sơ học sinh", icon: UserRound },
  { id: "attendance", label: "Điểm danh", icon: CalendarCheck },
  { id: "roster", label: "Nhập danh sách", icon: FileSpreadsheet },
  { id: "enrollment", label: "Ghi danh", icon: ClipboardPen },
];

export default function TeacherThptDashboard() {
  const { profile } = useAuth();
  // Trợ giảng thấy đủ các khối lớp như admin.
  const isAdmin = profile?.role === "admin" || profile?.role === "tro_giang";
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

  const [studentsNonce, setStudentsNonce] = useState(0);
  useEffect(() => {
    let cancelled = false;
    void (async () => {
      if (!selectedClassId) { if (!cancelled) setStudents([]); return; }
      try {
        const rows = await fetchClassStudents(selectedClassId);
        if (cancelled) return;
        setStudents(rows);
        setSelectedStudentId((current) => (rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null));
      } catch (error) {
        if (cancelled) return;
        setStudents([]);
        setLoadError(error instanceof Error ? error.message : "Không tải được danh sách học sinh.");
      }
    })();
    return () => { cancelled = true; };
  }, [selectedClassId, studentsNonce]);

  const selectedClass = classes.find((item) => item.id === selectedClassId) ?? null;

  return (
    <div className="teacher-dashboard space-y-6">
      <section className="relative overflow-hidden rounded-3xl border border-line bg-panel p-6 sm:p-8">
        <div className="relative">
          <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">Dashboard giáo viên · THPT</p>
          <h2 className="mt-2 font-display text-2xl font-bold text-ink">Chào {profile?.full_name || "thầy/cô"} 👋</h2>
          <p className="mt-2 text-sm text-muted">
            {selectedClass ? `Đang xem lớp ${selectedClass.name} · ${students.length} học sinh` : "Chọn khối lớp bên dưới để bắt đầu theo dõi học sinh."}
          </p>
          {loadError && <p className="mt-2 text-xs text-red-300">{loadError}</p>}
        </div>
      </section>

      <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
        <label className="block">
          <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-muted">
            Lớp đang dạy{classes.length > 0 && ` · ${classes.length} lớp`}
          </span>
          <select
            aria-label="Lớp đang dạy"
            value={selectedClassId ?? ""}
            onChange={(event) => setSelectedClassId(Number(event.target.value))}
            className="w-full max-w-sm rounded-xl border border-line-strong bg-panel-deep px-4 py-3 text-sm font-semibold text-ink"
          >
            <option value="" disabled>{classes.length ? "Chọn khối lớp" : "Chưa được phân công lớp nào"}</option>
            {classes.map((item) => (
              <option key={item.id} value={item.id}>{item.icon ? `${item.icon} ` : ""}{item.name}</option>
            ))}
          </select>
        </label>
      </section>

      <nav className="sticky top-20 z-40 flex gap-2 overflow-x-auto rounded-2xl border border-line bg-panel-deep/95 p-2 shadow-xl backdrop-blur">
        {TABS.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`inline-flex shrink-0 items-center gap-2 rounded-xl px-4 py-3 text-sm font-bold ${
                activeTab === tab.id ? "bg-blue-600 text-white" : "text-muted hover:bg-surface-2 hover:text-primary"
              }`}
            >
              <Icon size={17} />{tab.label}
            </button>
          );
        })}
      </nav>

      {!selectedClassId ? (
        <p className="rounded-2xl border border-dashed border-line p-10 text-center text-sm text-slate-500">
          Chưa có lớp nào để hiển thị.
        </p>
      ) : (
        <>
          {activeTab === "overview" && <TeacherThptOverview classId={selectedClassId} students={students} onOpenTab={setActiveTab} onOpenStudent={(id) => { setSelectedStudentId(id); setActiveTab("profile"); }} />}
          {activeTab === "progress" && <TeacherThptProgress classId={selectedClassId} students={students} />}
          {activeTab === "analysis" && <TeacherThptAnalysis classId={selectedClassId} students={students} />}
          {activeTab === "alerts" && <TeacherThptAlerts classId={selectedClassId} students={students} />}
          {activeTab === "tutoring" && <TeacherThptTutoring classId={selectedClassId} students={students} />}
          {activeTab === "announcements" && <ClassAnnouncementsPanel classId={selectedClassId} />}
          {activeTab === "gradebook" && <TeacherThptGradebook students={students} />}
          {activeTab === "profile" && <TeacherThptStudentProfile classId={selectedClassId} students={students} selectedId={selectedStudentId} onSelect={setSelectedStudentId} />}
          {activeTab === "attendance" && <TeacherThptAttendancePanel classId={selectedClassId} students={students} />}
          {activeTab === "enrollment" && <TeacherThptEnrollment classId={selectedClassId} className={selectedClass?.name ?? ""} students={students} onStudentsChanged={() => setStudentsNonce((n) => n + 1)} />}
          {activeTab === "roster" && <ClassRosterImportPanel classId={selectedClassId} className={selectedClass?.name ?? ""} onImported={() => setStudentsNonce((n) => n + 1)} />}
        </>
      )}
    </div>
  );
}
