"use client";

import { useEffect, useState } from "react";
import { useToast } from "@/components/ui/Toast";
import { fetchClassStudents, type ClassStudent } from "@/services/classes";
import { fetchHomeworkChecks, setHomeworkCheck, type HomeworkCheck } from "@/services/homework-checks";
import { fetchSeasons } from "@/services/rank";

const PERCENT_STEPS = [0, 25, 50, 75, 100];

function rpFor(percent: number): number {
  return Math.round((10 * percent) / 100);
}

/**
 * Chấm nhanh % học sinh đã làm một bài tập về nhà, ngay trên lớp. RP cộng theo tỉ lệ
 * (xem homework_check_set trong docs/supabase-migration-homework-check.sql) — chỉ khi
 * lớp đang có mùa rank mở, nếu không vẫn ghi % để lưu vết, chỉ là chưa cộng RP.
 */
export default function HomeworkCheckPanel({ announcementId, classId }: { announcementId: number; classId: number }) {
  const toast = useToast();
  const [students, setStudents] = useState<ClassStudent[] | null>(null);
  const [checks, setChecks] = useState<Record<string, HomeworkCheck>>({});
  const [seasonId, setSeasonId] = useState<number | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchClassStudents(classId), fetchHomeworkChecks(announcementId), fetchSeasons()])
      .then(([studentRows, checkRows, seasons]) => {
        if (cancelled) return;
        setStudents(studentRows);
        setChecks(checkRows);
        const active = seasons.find(
          (s) => s.status === "active" && (s.class_ids.length === 0 || s.class_ids.includes(classId)),
        );
        setSeasonId(active?.id ?? null);
      })
      .catch(() => {
        if (!cancelled) setStudents([]);
      });
    return () => {
      cancelled = true;
    };
  }, [classId, announcementId]);

  async function pick(studentId: string, percent: number) {
    setBusyId(studentId);
    try {
      await setHomeworkCheck({ announcementId, studentId, percent, seasonId });
      setChecks((prev) => ({ ...prev, [studentId]: { studentId, percent, checkedAt: new Date().toISOString() } }));
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa chấm được.");
    } finally {
      setBusyId(null);
    }
  }

  if (students === null) return <p className="p-3 text-xs text-slate-500">Đang tải danh sách lớp…</p>;
  if (students.length === 0) return <p className="p-3 text-xs text-slate-500">Lớp chưa có học sinh nào.</p>;

  return (
    <div className="space-y-2 rounded-xl border border-white/10 bg-panel-deep p-3">
      {!seasonId && (
        <p className="text-[12px] text-amber-300/80">Lớp chưa có mùa rank đang mở — vẫn chấm được, chỉ chưa cộng RP.</p>
      )}
      {students.map((s) => {
        const current = checks[s.id]?.percent;
        return (
          <div key={s.id} className="flex flex-wrap items-center gap-2 py-1">
            <span className="min-w-0 flex-1 truncate text-sm text-slate-200">{s.full_name}</span>
            <div className="flex flex-wrap gap-1">
              {PERCENT_STEPS.map((p) => (
                <button
                  key={p}
                  type="button"
                  disabled={busyId === s.id}
                  onClick={() => pick(s.id, p)}
                  className={`rounded-lg px-2 py-1 text-[12px] font-bold ${
                    current === p
                      ? "bg-cyan-500/25 text-cyan-200"
                      : "bg-white/[.04] text-slate-400 hover:bg-white/[.08]"
                  } disabled:opacity-40`}
                >
                  {p}%
                </button>
              ))}
            </div>
            {current !== undefined && (
              <span className="text-[12px] text-slate-500">+{rpFor(current)} RP</span>
            )}
          </div>
        );
      })}
    </div>
  );
}
