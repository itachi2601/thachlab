"use client";

import { useEffect, useRef, useState } from "react";
import { AlertTriangle, BarChart3, BookOpenCheck, CalendarCheck, ClipboardPen, LayoutDashboard, ListChecks, Megaphone, UserRound } from "lucide-react";
import type { SchoolClass } from "@/features/exams/types";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchClasses, fetchClassStudents, type ClassStudent } from "@/services/classes";
import { fetchAttendanceSessions } from "@/services/class-attendance";
import { fetchClassExamResults } from "@/services/class-results";
import { fetchInstructorClasses } from "@/services/class-instructors";
import dynamic from "next/dynamic";
import type { ComponentProps, ComponentType } from "react";
import SegmentedControl from "@/components/ui/SegmentedControl";
import ParentLinkRequestsPanel from "@/components/dashboard/ParentLinkRequestsPanel";
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
const TeacherThptMastery = lazyTab(() => import("@/components/dashboard/TeacherThptMastery"));
const TeacherThptEarlyWarning = lazyTab(() => import("@/components/dashboard/TeacherThptEarlyWarning"));
const TeachingProgressTree = lazyTab(() => import("@/components/dashboard/TeachingProgressTree"));
const TeacherThptTutoring = lazyTab(() => import("@/components/dashboard/TeacherThptTutoring"));
const TeacherThptStudentProfile = lazyTab(() => import("@/components/dashboard/TeacherThptStudentProfile"));
const TeacherThptProgress = lazyTab(() => import("@/components/dashboard/TeacherThptProgress"));
const TeacherThptAttendancePanel = lazyTab(() => import("@/components/attendance/TeacherThptAttendancePanel"));
const ClassAnnouncementsPanel = lazyTab(() => import("@/components/dashboard/ClassAnnouncementsPanel"));
const TeacherThptEnrollment = lazyTab(() => import("@/components/dashboard/TeacherThptEnrollment"));

type DashboardTab =
  | "overview"
  | "progress"
  | "analysis"
  | "teaching"
  | "alerts"
  | "tutoring"
  | "announcements"
  | "profile"
  | "attendance"
  | "enrollment";

const TABS: { id: DashboardTab; label: string; icon: typeof LayoutDashboard }[] = [
  { id: "overview", label: "Tổng quan", icon: LayoutDashboard },
  { id: "progress", label: "Kết quả học tập", icon: ListChecks },
  { id: "analysis", label: "Phân tích", icon: BarChart3 },
  { id: "teaching", label: "Tiến trình dạy", icon: BookOpenCheck },
  { id: "alerts", label: "Cảnh báo & phụ đạo", icon: AlertTriangle },
  { id: "announcements", label: "Thông báo", icon: Megaphone },
  { id: "profile", label: "Hồ sơ học sinh", icon: UserRound },
  { id: "attendance", label: "Điểm danh", icon: CalendarCheck },
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
  const [analysisView, setAnalysisView] = useState<"exam" | "mastery">("exam");
  const [resultsView, setResultsView] = useState<"lessons" | "scores">("lessons");
  const [alertsView, setAlertsView] = useState<"alerts" | "early" | "tutoring">("alerts");
  const preferredClassId = useRef<number | null>(null);
  const [lastSession, setLastSession] = useState<string | null>(null);
  const [idleThisWeek, setIdleThisWeek] = useState<number | null>(null);
  const [tabsMore, setTabsMore] = useState(false);
  const tabsRef = useRef<HTMLElement | null>(null);

  const classKey = profile ? `thachlab-dashboard-thpt-class:${profile.id}` : null;

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const tab = params.get("tab");
    if (tab && TABS.some((item) => item.id === tab)) setActiveTab(tab as DashboardTab);
    const lop = Number(params.get("lop"));
    if (Number.isInteger(lop) && lop > 0) preferredClassId.current = lop;
  }, []);

  useEffect(() => {
    if (!profile) return;
    let cancelled = false;
    const load = isAdmin ? fetchClasses() : fetchInstructorClasses(profile.id);
    load
      .then((rows) => {
        if (cancelled) return;
        setClasses(rows);
        setSelectedClassId((current) => {
          let preferred = preferredClassId.current;
          if (!preferred && classKey) {
            try { preferred = Number(localStorage.getItem(classKey)) || null; } catch { /* riêng tư: bỏ qua */ }
          }
          if (preferred && rows.some((item) => item.id === preferred)) return preferred;
          if (current != null && rows.some((item) => item.id === current)) return current;
          return rows[0]?.id ?? null;
        });
        setLoadError("");
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        setLoadError(error instanceof Error ? error.message : "Không tải được danh sách lớp.");
      });
    return () => { cancelled = true; };
  }, [profile, isAdmin, classKey]);

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

  useEffect(() => {
    if (!classKey || !selectedClassId) return;
    try { localStorage.setItem(classKey, String(selectedClassId)); } catch { /* riêng tư: bỏ qua */ }
  }, [classKey, selectedClassId]);

  // Dòng tóm tắt đầu trang: buổi điểm danh gần nhất + số em chưa làm bài kể từ thứ Hai tuần này.
  useEffect(() => {
    setLastSession(null);
    setIdleThisWeek(null);
    if (!selectedClassId) return;
    let cancelled = false;
    fetchAttendanceSessions(selectedClassId)
      .then((rows) => {
        if (cancelled) return;
        const latest = [...rows].sort((a, b) => b.session_date.localeCompare(a.session_date))[0];
        setLastSession(latest ? new Date(`${latest.session_date}T00:00:00`).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" }) : null);
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [selectedClassId]);

  useEffect(() => {
    if (students.length === 0) return;
    let cancelled = false;
    const monday = new Date();
    monday.setHours(0, 0, 0, 0);
    monday.setDate(monday.getDate() - ((monday.getDay() + 6) % 7));
    fetchClassExamResults(students.map((s) => s.id), monday.toISOString())
      .then((rows) => {
        if (cancelled) return;
        const done = new Set(rows.map((r) => r.student_id));
        setIdleThisWeek(students.filter((s) => !done.has(s.id)).length);
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [students]);

  useEffect(() => {
    const el = tabsRef.current;
    if (!el) return;
    const update = () => setTabsMore(el.scrollLeft + el.clientWidth < el.scrollWidth - 4);
    update();
    el.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => { el.removeEventListener("scroll", update); window.removeEventListener("resize", update); };
  }, []);

  const selectedClass = classes.find((item) => item.id === selectedClassId) ?? null;

  return (
    <div className="teacher-dashboard space-y-6">
      <section className="relative overflow-hidden rounded-3xl border border-line bg-panel p-6 sm:p-8">
        <div className="relative">
          <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">Dashboard giáo viên · THPT</p>
          <h2 className="mt-2 font-display text-xl font-bold text-ink sm:text-2xl">
            {selectedClass
              ? [
                  /^\d+$/.test(selectedClass.name.trim()) ? `Lớp ${selectedClass.name.trim()}` : selectedClass.name,
                  lastSession ? `buổi gần nhất ${lastSession}` : null,
                  idleThisWeek != null ? `${idleThisWeek} em chưa làm bài tuần này` : null,
                ].filter(Boolean).join(" · ")
              : "Chọn lớp bên dưới để bắt đầu"}
          </h2>
          {loadError && <p className="mt-2 text-xs text-red-300">{loadError}</p>}
        </div>
      </section>

      <ParentLinkRequestsPanel />

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

      <div className="sticky top-20 z-40">
      <nav ref={tabsRef} className="flex gap-2 overflow-x-auto rounded-2xl border border-line bg-panel-deep/95 p-2 shadow-xl backdrop-blur">
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
      {tabsMore && (
        <span aria-hidden className="pointer-events-none absolute inset-y-0 right-0 w-14 rounded-r-2xl bg-gradient-to-l from-[var(--color-panel-deep)] to-transparent" />
      )}
      </div>

      {!selectedClassId ? (
        <p className="rounded-2xl border border-dashed border-line p-10 text-center text-sm text-slate-500">
          Chưa có lớp nào để hiển thị.
        </p>
      ) : (
        <>
          {activeTab === "overview" && <TeacherThptOverview classId={selectedClassId} students={students} onOpenTab={(tab) => { if (tab === "gradebook") { setResultsView("scores"); setActiveTab("progress"); } else setActiveTab(tab); }} onOpenStudent={(id) => { setSelectedStudentId(id); setActiveTab("profile"); }} />}
          {activeTab === "progress" && (
            <div className="space-y-5">
              <SegmentedControl label="Kiểu xem kết quả" value={resultsView} onChange={setResultsView} options={[["lessons", "Theo bài học"], ["scores", "Điểm bài kiểm tra"]] as const} />
              {resultsView === "lessons"
                ? <TeacherThptProgress classId={selectedClassId} students={students} />
                : <TeacherThptGradebook students={students} />}
            </div>
          )}
          {activeTab === "analysis" && (
            <div className="space-y-5">
              <SegmentedControl label="Kiểu phân tích" value={analysisView} onChange={setAnalysisView} options={[["exam", "Theo đề"], ["mastery", "Bản đồ thành thạo"]] as const} />
              {analysisView === "exam"
                ? <TeacherThptAnalysis classId={selectedClassId} students={students} classes={classes} />
                : <TeacherThptMastery students={students} onOpenStudent={(id) => { setSelectedStudentId(id); setActiveTab("profile"); }} onOpenTab={setActiveTab} />}
            </div>
          )}
          {activeTab === "teaching" && <TeachingProgressTree key={selectedClassId} classId={selectedClassId} />}
          {activeTab === "alerts" && (
            <div className="space-y-5">
              <SegmentedControl label="Nhóm cảnh báo" value={alertsView} onChange={setAlertsView} options={[["alerts", "Cảnh báo"], ["early", "Cần để ý sớm"], ["tutoring", "Phụ đạo"]] as const} />
              {alertsView === "alerts" && <TeacherThptAlerts classId={selectedClassId} students={students} />}
              {alertsView === "early" && <TeacherThptEarlyWarning students={students} onOpenStudent={(id) => { setSelectedStudentId(id); setActiveTab("profile"); }} />}
              {alertsView === "tutoring" && <TeacherThptTutoring classId={selectedClassId} students={students} />}
            </div>
          )}
          {activeTab === "announcements" && <ClassAnnouncementsPanel classId={selectedClassId} />}
                    {activeTab === "profile" && <TeacherThptStudentProfile classId={selectedClassId} students={students} selectedId={selectedStudentId} onSelect={setSelectedStudentId} />}
          {activeTab === "attendance" && <TeacherThptAttendancePanel classId={selectedClassId} students={students} />}
          {activeTab === "enrollment" && (
            <TeacherThptEnrollment classId={selectedClassId} className={selectedClass?.name ?? ""} students={students} onStudentsChanged={() => setStudentsNonce((n) => n + 1)} />
          )}
        </>
      )}
    </div>
  );
}
