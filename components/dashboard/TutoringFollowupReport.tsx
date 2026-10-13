"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle } from "lucide-react";
import {
  FOLLOWUP_LABEL,
  fetchFollowupReport,
  followupState,
  type FollowupRow,
  type FollowupState,
} from "@/services/tutoring";

const TONE: Record<FollowupState, string> = {
  upcoming: "border-line bg-surface-2 text-muted",
  no_roll: "border-warn/40 bg-surface-2 text-warn",
  absent: "border-line bg-surface-2 text-muted",
  no_quiz: "border-warn/40 bg-surface-2 text-warn",
  failed: "border-warn/40 bg-surface-2 text-warn",
  passed: "border-ok/40 bg-surface-2 text-ok",
  cleared: "border-ok/40 bg-surface-2 text-ok",
};

/**
 * Thầy nhìn một chỗ biết: em nào đăng ký buổi nào, học chủ đề gì, có mặt không, làm bài kiểm tra đạt chưa,
 * mục phụ đạo đã được khắc phục chưa. Số liệu từ RPC tutoring_followup_report (14/10/2026).
 */
export default function TutoringFollowupReport({ classId }: { classId: number }) {
  const [rows, setRows] = useState<FollowupRow[] | null>(null);
  const [failed, setFailed] = useState(false);
  const [nowMs] = useState(() => Date.now());

  useEffect(() => {
    let alive = true;
    fetchFollowupReport(classId, 30)
      .then((r) => alive && setRows(r))
      .catch(() => alive && setFailed(true));
    return () => {
      alive = false;
    };
  }, [classId]);

  const bySlot = useMemo(() => {
    const map = new Map<number, FollowupRow[]>();
    for (const r of rows ?? []) map.set(r.slotId, [...(map.get(r.slotId) ?? []), r]);
    return [...map.values()];
  }, [rows]);

  const warnings = useMemo(() => {
    let noRoll = 0;
    let noSession = 0;
    for (const group of bySlot) {
      const past = followupState(group[0], nowMs) !== "upcoming";
      if (!past) continue;
      if (group.some((r) => r.attended === null)) noRoll += 1;
      else if (group.some((r) => r.attended === true) && !group[0].hasSession) noSession += 1;
    }
    return { noRoll, noSession };
  }, [bySlot, nowMs]);

  if (failed) return null; // chưa chạy migration 20261014110000 thì ẩn, không làm hỏng tab
  if (!rows || rows.length === 0) return null;

  return (
    <section className="rounded-3xl border border-white/10 bg-panel p-4 sm:p-6">
      <h2 className="font-display text-xl font-bold text-white">Em đã đăng ký phụ đạo — 30 ngày qua</h2>
      <p className="mt-1 text-sm text-slate-400">
        Mỗi dòng: em, chủ đề đã chọn, có mặt hay vắng, kết quả bài kiểm tra cuối buổi.
      </p>
      {(warnings.noRoll > 0 || warnings.noSession > 0) && (
        <div className="mt-3 space-y-1 rounded-xl border border-warn/40 bg-surface-2 p-3 text-sm text-warn">
          {warnings.noRoll > 0 && (
            <p className="flex items-center gap-2">
              <AlertTriangle size={14} /> {warnings.noRoll} buổi đã qua mà trợ giảng chưa điểm danh.
            </p>
          )}
          {warnings.noSession > 0 && (
            <p className="flex items-center gap-2">
              <AlertTriangle size={14} /> {warnings.noSession} buổi có em có mặt nhưng chưa có phiếu ghi buổi.
            </p>
          )}
        </div>
      )}
      <div className="mt-4 space-y-3">
        {bySlot.map((group) => {
          const head = group[0];
          const date = new Date(`${head.workDate}T00:00:00`).toLocaleDateString("vi-VN", {
            weekday: "short",
            day: "2-digit",
            month: "2-digit",
          });
          return (
            <div key={head.slotId} className="rounded-2xl border border-white/10 p-3">
              <p className="text-sm font-bold text-white">
                {date} · {head.startTime.slice(0, 5)} · {head.assistantName}
              </p>
              <ul className="mt-2 space-y-2">
                {group.map((r) => {
                  const state = followupState(r, nowMs);
                  return (
                    <li key={`${r.registrationId}-${r.topicId}`} className="text-sm text-slate-300">
                      <strong className="text-white">{r.studentName}</strong>
                      <span className="block text-[13px] text-slate-400">{r.topicName}</span>
                      <span className={`mt-1 inline-block rounded-full border px-3 py-1 text-[13px] font-semibold ${TONE[state]}`}>
                        {FOLLOWUP_LABEL[state]}
                        {(state === "failed" || state === "passed") && ` · ${r.bestPct}%`}
                      </span>
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </div>
    </section>
  );
}
