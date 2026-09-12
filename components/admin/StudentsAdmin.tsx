"use client";

import { useEffect, useState } from "react";
import { Clock3, FileSpreadsheet, UserRound, UserX } from "lucide-react";
import type { SchoolClass } from "@/features/exams/types";
import { fetchClasses, fetchClassStudents, type ClassStudent } from "@/services/classes";
import { useAuth } from "@/components/auth/AuthProvider";
import TeacherThptStudentProfile from "@/components/dashboard/TeacherThptStudentProfile";
import ClassRosterImportPanel from "@/components/dashboard/ClassRosterImportPanel";
import ClassPendingRequests from "@/components/admin/ClassPendingRequests";
import UnassignedStudents from "@/components/admin/UnassignedStudents";

type Tab = "profile" | "pending" | "roster" | "unassigned";

const TABS: { id: Tab; label: string; icon: typeof UserRound }[] = [
  { id: "profile", label: "Hồ sơ học sinh", icon: UserRound },
  { id: "pending", label: "Chờ duyệt", icon: Clock3 },
  { id: "roster", label: "Nhập danh sách", icon: FileSpreadsheet },
];

export default function StudentsAdmin() {
  const { profile } = useAuth();
  const isAdmin = profile?.role === "admin";
  const tabs = isAdmin ? [...TABS, { id: "unassigned" as const, label: "Chưa phân lớp", icon: UserX }] : TABS;
  const [tab, setTab] = useState<Tab>("profile");
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [selectedClassId, setSelectedClassId] = useState<number | null>(null);
  const [students, setStudents] = useState<ClassStudent[]>([]);
  const [selectedStudentId, setSelectedStudentId] = useState<string | null>(null);
  const [studentsNonce, setStudentsNonce] = useState(0);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    fetchClasses().then((rows) => {
      setClasses(rows);
      setSelectedClassId((current) => (rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null));
    });
  }, []);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      if (!selectedClassId) { if (!cancelled) setStudents([]); return; }
      try {
        const rows = await fetchClassStudents(selectedClassId);
        if (cancelled) return;
        setStudents(rows);
        setSelectedStudentId((current) => (rows.some((item) => item.id === current) ? current : rows[0]?.id ?? null));
        setLoadError("");
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
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <h2 className="font-display text-lg font-semibold text-white">Học sinh</h2>
        <p className="mt-2 text-sm text-slate-400">
          Xem hồ sơ, lịch sử làm bài, điểm danh của học sinh theo khối lớp — hoặc nhập danh sách
          học sinh từ file Excel để tự tạo tài khoản và thêm vào lớp.
        </p>
        <label className="mt-4 block max-w-sm">
          <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">
            Khối lớp{classes.length > 0 && ` · ${classes.length} lớp`}
          </span>
          <select
            aria-label="Khối lớp"
            value={selectedClassId ?? ""}
            onChange={(event) => setSelectedClassId(Number(event.target.value))}
            className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm font-semibold text-white"
          >
            <option value="" disabled>{classes.length ? "Chọn khối lớp" : "Chưa có lớp nào"}</option>
            {classes.map((item) => (
              <option key={item.id} value={item.id}>{item.icon ? `${item.icon} ` : ""}{item.name}</option>
            ))}
          </select>
        </label>
        {loadError && <p className="mt-2 text-xs text-red-300">{loadError}</p>}
      </section>

      {!selectedClassId ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-10 text-center text-sm text-slate-500">
          Chưa có lớp nào để hiển thị — thêm ở mục Lớp học.
        </p>
      ) : (
        <>
          <nav className="flex gap-2 overflow-x-auto rounded-2xl border border-white/10 bg-[#080d1d]/95 p-2">
            {tabs.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setTab(item.id)}
                  className={`inline-flex shrink-0 items-center gap-2 rounded-xl px-4 py-3 text-sm font-bold ${
                    tab === item.id ? "bg-blue-600 text-white" : "text-slate-400 hover:bg-white/5 hover:text-white"
                  }`}
                >
                  <Icon size={17} />{item.label}
                </button>
              );
            })}
          </nav>

          {tab === "profile" && (
            <TeacherThptStudentProfile
              classId={selectedClassId}
              students={students}
              selectedId={selectedStudentId}
              onSelect={setSelectedStudentId}
            />
          )}
          {tab === "pending" && (
            <ClassPendingRequests
              classId={selectedClassId}
              className={selectedClass?.name ?? ""}
              onReviewed={() => setStudentsNonce((n) => n + 1)}
            />
          )}
          {tab === "roster" && (
            <ClassRosterImportPanel
              classId={selectedClassId}
              className={selectedClass?.name ?? ""}
              onImported={() => setStudentsNonce((n) => n + 1)}
            />
          )}
          {tab === "unassigned" && isAdmin && (
            <UnassignedStudents
              classes={classes}
              defaultClassId={selectedClassId}
              onAssigned={() => setStudentsNonce((n) => n + 1)}
            />
          )}
        </>
      )}
    </div>
  );
}
