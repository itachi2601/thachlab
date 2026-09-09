"use client";

import { useCallback, useEffect, useState } from "react";
import { UserPlus2 } from "lucide-react";
import type { SchoolClass } from "@/features/exams/types";
import { fetchUnassignedStudents, setUserClassStatus, type UnassignedStudent } from "@/services/classes";
import { useToast } from "@/components/ui/Toast";

export default function UnassignedStudents({
  classes,
  defaultClassId,
  onAssigned,
}: {
  classes: SchoolClass[];
  defaultClassId: number | null;
  onAssigned?: () => void;
}) {
  const toast = useToast();
  const [students, setStudents] = useState<UnassignedStudent[]>([]);
  const [targetClass, setTargetClass] = useState<Record<string, number>>({});
  const [busyId, setBusyId] = useState<string | null>(null);

  const reload = useCallback(() => {
    fetchUnassignedStudents()
      .then(setStudents)
      .catch((error: unknown) => toast("error", error instanceof Error ? error.message : "Không tải được danh sách."));
  }, [toast]);
  useEffect(reload, [reload]);

  async function assign(studentId: string) {
    const classId = targetClass[studentId] ?? defaultClassId;
    if (!classId) return;
    setBusyId(studentId);
    try {
      await setUserClassStatus(studentId, classId, "active");
      toast("success", "Đã gán vào lớp.");
      setStudents((current) => current.filter((s) => s.id !== studentId));
      onAssigned?.();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không gán được vào lớp.");
    } finally {
      setBusyId(null);
    }
  }

  return (
    <div className="space-y-4">
      <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-4 text-sm text-slate-400">
        Học sinh tự đăng ký ở trang <strong className="text-white">/dang-ky</strong> nhưng chưa được gán vào lớp hoặc
        khóa học nào. Đối chiếu đúng tên rồi gán vào khối lớp phù hợp.
      </p>
      {!students.length ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-10 text-center text-sm text-slate-500">
          Không có học sinh nào chưa phân lớp.
        </p>
      ) : (
        <div className="space-y-2">
          {students.map((student) => (
            <div
              key={student.id}
              className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-4 py-3"
            >
              <span className="font-medium text-white">{student.full_name || "(chưa có tên)"}</span>
              <span className="ml-auto flex items-center gap-2">
                <select
                  aria-label="Gán vào khối lớp"
                  value={targetClass[student.id] ?? defaultClassId ?? ""}
                  onChange={(event) => setTargetClass((current) => ({ ...current, [student.id]: Number(event.target.value) }))}
                  className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-1.5 text-xs font-semibold text-white"
                >
                  <option value="" disabled>Chọn khối lớp</option>
                  {classes.map((c) => (
                    <option key={c.id} value={c.id}>{c.icon ? `${c.icon} ` : ""}{c.name}</option>
                  ))}
                </select>
                <button
                  onClick={() => assign(student.id)}
                  disabled={busyId === student.id || !(targetClass[student.id] ?? defaultClassId)}
                  className="inline-flex items-center gap-1 rounded-full bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white disabled:opacity-50"
                >
                  <UserPlus2 size={13} /> Gán vào lớp
                </button>
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
