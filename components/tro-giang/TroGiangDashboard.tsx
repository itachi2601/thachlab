"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { PenLine, Sparkles } from "lucide-react";
import ScoreRing from "./ScoreRing";
import { SESSION_TYPE_META, STATUS_META } from "@/lib/tro-giang/constants";
import { formatHours, formatVnd, buildNextTierMessage } from "@/lib/tro-giang/format";
import {
  fetchRecentSessions,
  getAccruedHours,
  getMonthlyScore,
  type TaAssistant,
  type TaMonthlyScore,
  type TaSessionListItem,
} from "@/lib/tro-giang/queries";

function currentMonthStr() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-01`;
}

function ScoreBar({ label, value, max }: { label: string; value: number; max: number }) {
  const pct = max > 0 ? Math.min(100, (value / max) * 100) : 0;
  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between text-xs">
        <span className="font-medium text-slate-300">{label}</span>
        <span className="font-mono font-bold tabular-nums text-white">
          {value.toFixed(1)}<span className="text-slate-500">/{max}</span>
        </span>
      </div>
      <div className="h-2 rounded-full bg-white/10">
        <div className="h-2 rounded-full bg-blue-500 transition-all" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function StatTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-1.5 font-mono text-lg font-bold tabular-nums text-white">{value}</p>
    </div>
  );
}

export default function TroGiangDashboard({ assistant }: { assistant: TaAssistant }) {
  const [score, setScore] = useState<TaMonthlyScore | null>(null);
  const [accruedHours, setAccruedHours] = useState<number | null>(null);
  const [sessions, setSessions] = useState<TaSessionListItem[] | null>(null);

  useEffect(() => {
    const month = currentMonthStr();
    getMonthlyScore(assistant.id, month).then(setScore).catch(() => setScore(null));
    getAccruedHours(assistant.id).then(setAccruedHours).catch(() => setAccruedHours(null));
    fetchRecentSessions(assistant.id, 10).then(setSessions).catch(() => setSessions([]));
  }, [assistant.id]);

  const hasActivity = !!score && (score.lop_sessions > 0 || score.phudao_sessions > 0 || score.converted_hours > 0 || score.papers_graded > 0);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-bold text-white">Chào {assistant.short_name}</h1>
        <p className="mt-1 text-sm text-slate-400">Bậc {assistant.tier} · Hiệu suất tháng này</p>
      </div>

      <section className="rounded-3xl border border-white/10 bg-[#0B1020] p-6">
        {!score ? (
          <p className="text-slate-500">Đang tải điểm hiệu suất…</p>
        ) : !hasActivity ? (
          <div className="flex flex-col items-center gap-3 py-4 text-center">
            <Sparkles className="text-blue-300" size={30} />
            <p className="font-display text-lg font-bold text-white">Chưa có buổi nào trong tháng này</p>
            <p className="text-sm text-slate-400">Ghi buổi đầu tiên để bắt đầu tính điểm hiệu suất.</p>
          </div>
        ) : (
          <>
            <div className="flex flex-wrap items-center gap-6">
              <ScoreRing score={score.total_score} />
              <div className="flex min-w-[220px] flex-1 flex-col gap-3">
                <ScoreBar label="Chạm học sinh" value={score.touches_score} max={40} />
                <ScoreBar label="Nộp phiếu lỗi đúng hạn" value={score.error_note_score} max={20} />
                <ScoreBar label="Hồ sơ phụ đạo" value={score.phudao_score} max={20} />
                <ScoreBar label="Tập trung trong giờ" value={score.focus_score} max={20} />
              </div>
            </div>
            <p className="mt-5 rounded-xl bg-blue-500/10 px-4 py-3 text-sm text-blue-100">
              {buildNextTierMessage(score)}
            </p>
          </>
        )}
      </section>

      {score && (
        <section className="grid grid-cols-2 gap-3">
          <StatTile label="Giờ quy đổi tháng này" value={`${formatHours(score.converted_hours)} giờ`} />
          <StatTile label="Tiền nền" value={formatVnd(score.base_pay)} />
          <StatTile label="Thưởng dự kiến" value={formatVnd(score.bonus_pay)} />
          <StatTile label="Thực nhận dự kiến" value={formatVnd(score.total_pay)} />
        </section>
      )}

      {accruedHours !== null && (
        <p className="text-center text-xs text-slate-500">
          Giờ tích lũy xét lên bậc (trọn đời): <span className="font-mono font-semibold text-slate-300">{formatHours(accruedHours)} giờ</span>
        </p>
      )}

      <Link
        href="/tro-giang/ghi"
        className="flex items-center justify-center gap-2 rounded-2xl bg-blue-600 py-4 text-base font-bold text-white shadow-lg shadow-blue-600/20"
      >
        <PenLine size={18} />
        Ghi buổi hôm nay
      </Link>

      <section>
        <h2 className="mb-3 font-display text-lg font-bold text-white">Buổi gần đây</h2>
        {sessions === null ? (
          <p className="text-slate-500">Đang tải…</p>
        ) : sessions.length === 0 ? (
          <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">
            Chưa ghi buổi nào. Bấm &quot;Ghi buổi hôm nay&quot; ở trên để bắt đầu.
          </p>
        ) : (
          <div className="flex flex-col gap-2.5">
            {sessions.map((s) => {
              const typeMeta = SESSION_TYPE_META[s.session_type];
              const statusMeta = STATUS_META[s.status];
              const TypeIcon = typeMeta.icon;
              const StatusIcon = statusMeta.icon;
              return (
                <div key={s.id} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 p-4">
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/10 text-slate-300">
                    <TypeIcon size={18} />
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="font-medium text-white">
                      {typeMeta.label}
                      {s.class_label ? ` · ${s.class_label}` : ""}
                    </p>
                    <p className="text-xs text-slate-400">
                      {new Date(s.work_date).toLocaleDateString("vi-VN")}
                      {s.hours ? ` · ${formatHours(s.hours)} giờ` : ""}
                      {s.papers_graded ? ` · ${s.papers_graded} bài` : ""}
                    </p>
                    {s.status === "rejected" && s.reject_reason && (
                      <p className="mt-1 text-xs text-red-300">Lý do: {s.reject_reason}</p>
                    )}
                  </div>
                  <span className={`flex shrink-0 items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold ${statusMeta.className}`}>
                    <StatusIcon size={13} />
                    {statusMeta.label}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
