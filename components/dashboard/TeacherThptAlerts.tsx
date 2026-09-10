"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import type { ClassStudent } from "@/services/classes";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import {
  ALERT_STATUS_LABEL,
  fetchClassAlerts,
  sweepMissedAssessments,
  updateAlert,
  type StudentAlert,
} from "@/services/analytics";

const STATUS_FLOW: StudentAlert["status"][] = [
  "open",
  "contacted",
  "tutoring",
  "resolved",
  "dismissed",
];

const STATUS_TONE: Record<StudentAlert["status"], string> = {
  open: "border-red-500/40 text-red-300 bg-red-500/10",
  contacted: "border-amber-500/40 text-amber-300 bg-amber-500/10",
  tutoring: "border-blue-500/40 text-blue-300 bg-blue-500/10",
  resolved: "border-emerald-500/40 text-emerald-300 bg-emerald-500/10",
  dismissed: "border-white/15 text-slate-400 bg-white/5",
};

export default function TeacherThptAlerts({
  classId,
  students,
}: {
  classId: number;
  students: ClassStudent[];
}) {
  const { profile } = useAuth();
  const toast = useToast();
  const [alerts, setAlerts] = useState<StudentAlert[] | null>(null);
  const [filter, setFilter] = useState<"active" | "all">("active");
  const [sweeping, setSweeping] = useState(false);

  const studentIds = useMemo(() => students.map((s) => s.id), [students]);
  const nameById = useMemo(() => new Map(students.map((s) => [s.id, s.full_name])), [students]);

  const load = useCallback(() => {
    fetchClassAlerts(studentIds).then(setAlerts).catch(() => setAlerts([]));
  }, [studentIds]);
  useEffect(load, [load]);

  // Rà "bỏ bài kiểm tra" mỗi khi mở tab.
  useEffect(() => {
    if (studentIds.length === 0) return;
    sweepMissedAssessments(classId).then((n) => {
      if (n > 0) load();
    });
  }, [classId, studentIds.length, load]);

  async function setStatus(alert: StudentAlert, status: StudentAlert["status"]) {
    try {
      await updateAlert(alert.id, { status, handledBy: profile?.id });
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không cập nhật được.");
    }
  }
  async function assignMe(alert: StudentAlert) {
    if (!profile) return;
    try {
      await updateAlert(alert.id, { assignedTo: profile.id });
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Không gán được.");
    }
  }
  async function runSweep() {
    setSweeping(true);
    const n = await sweepMissedAssessments(classId, 3);
    setSweeping(false);
    toast("success", n > 0 ? `Đã rà, cập nhật ${n} cảnh báo.` : "Không có cảnh báo mới.");
    load();
  }

  if (!alerts) return <p className="text-sm text-slate-400">Đang tải…</p>;

  const shown = alerts.filter((a) =>
    filter === "all" ? true : a.status !== "resolved" && a.status !== "dismissed",
  );
  const openCount = alerts.filter((a) => a.status === "open").length;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-2 text-amber-300">
          <AlertTriangle size={18} />
          <h3 className="font-display text-lg font-bold text-white">Cảnh báo phụ đạo</h3>
          {openCount > 0 && (
            <span className="rounded-full bg-red-500/15 px-2 py-0.5 text-xs font-bold text-red-300">
              {openCount} mới
            </span>
          )}
        </div>
        <div className="ml-auto flex items-center gap-2">
          <div className="inline-flex rounded-full border border-white/10 bg-white/5 p-0.5 text-xs">
            {(["active", "all"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`rounded-full px-3 py-1 font-semibold ${
                  filter === f ? "bg-blue-600 text-white" : "text-slate-400"
                }`}
              >
                {f === "active" ? "Đang mở" : "Tất cả"}
              </button>
            ))}
          </div>
          <button
            onClick={runSweep}
            disabled={sweeping}
            className="inline-flex items-center gap-1.5 rounded-full border border-white/15 px-3 py-1.5 text-xs font-semibold text-slate-300 hover:border-white/30 disabled:opacity-50"
          >
            <RefreshCw size={13} className={sweeping ? "animate-spin" : ""} /> Rà bỏ bài
          </button>
        </div>
      </div>

      {shown.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">
          Không có cảnh báo nào {filter === "active" ? "đang mở" : ""}.
        </p>
      ) : (
        <div className="space-y-2">
          {shown.map((a) => (
            <div
              key={a.id}
              className="rounded-2xl border border-white/10 bg-[#0B1020] p-4"
            >
              <div className="flex flex-wrap items-start gap-3">
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <strong className="text-white">
                      {nameById.get(a.studentId) ?? "(đã rời lớp)"}
                    </strong>
                    {a.severity === "urgent" && (
                      <span className="rounded-full bg-red-500/15 px-2 py-0.5 text-[10px] font-bold text-red-300">
                        KHẨN
                      </span>
                    )}
                    <span
                      className={`rounded-full border px-2 py-0.5 text-[11px] font-semibold ${STATUS_TONE[a.status]}`}
                    >
                      {ALERT_STATUS_LABEL[a.status]}
                    </span>
                    <span className="text-[11px] text-slate-500">
                      {a.kind === "missed_assessment" ? "Bỏ bài KT" : "Điểm thấp liên tiếp"}
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-slate-300">{a.reason}</p>
                  {a.assignedTo && (
                    <p className="mt-1 text-xs text-slate-500">
                      Phụ trách: {nameById.get(a.assignedTo) ?? "trợ giảng"}
                    </p>
                  )}
                </div>
                <div className="flex flex-col items-end gap-1.5">
                  {!a.assignedTo && (
                    <button
                      onClick={() => assignMe(a)}
                      className="rounded-lg border border-white/15 px-3 py-1 text-xs text-slate-300 hover:border-white/30"
                    >
                      Nhận xử lý
                    </button>
                  )}
                  <div className="flex flex-wrap justify-end gap-1">
                    {STATUS_FLOW.filter((s) => s !== a.status && s !== "open").map((s) => (
                      <button
                        key={s}
                        onClick={() => setStatus(a, s)}
                        className={`rounded-lg border px-2.5 py-1 text-xs font-semibold ${STATUS_TONE[s]}`}
                      >
                        {ALERT_STATUS_LABEL[s]}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
