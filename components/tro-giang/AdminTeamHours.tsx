"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, Check } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { formatHours } from "@/lib/tro-giang/format";
import {
  fetchCourseTotalHours,
  fetchHoursCap,
  fetchTeamMonthlyHours,
  updateHoursCap,
  type TaTeamMonthlyHours,
} from "@/lib/tro-giang/queries";

function monthLabel(iso: string) {
  const d = new Date(iso);
  return `${d.getMonth() + 1}/${String(d.getFullYear()).slice(2)}`;
}

export default function AdminTeamHours({ reloadKey = 0 }: { reloadKey?: number }) {
  const toast = useToast();
  const [months, setMonths] = useState<TaTeamMonthlyHours[] | null>(null);
  const [total, setTotal] = useState<number | null>(null);
  const [cap, setCap] = useState<number | null>(null);
  const [capDraft, setCapDraft] = useState("");
  const [busy, setBusy] = useState(false);

  const load = useCallback(() => {
    fetchTeamMonthlyHours(12).then(setMonths).catch(() => setMonths([]));
    fetchCourseTotalHours().then(setTotal).catch(() => setTotal(null));
    fetchHoursCap()
      .then((c) => {
        setCap(c);
        setCapDraft(String(c));
      })
      .catch(() => setCap(null));
  }, []);

  useEffect(load, [load, reloadKey]);

  async function saveCap() {
    const n = Number(capDraft);
    if (!Number.isFinite(n) || n <= 0) {
      toast("error", "Ngưỡng giờ phải là số dương.");
      return;
    }
    setBusy(true);
    try {
      await updateHoursCap(Math.round(n));
      setCap(Math.round(n));
      toast("success", "Đã lưu ngưỡng giờ của khoá.");
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không lưu được.");
    } finally {
      setBusy(false);
    }
  }

  const over = total != null && cap != null && total > cap;
  const peak = months && months.length > 0 ? Math.max(...months.map((m) => m.converted_hours)) : 0;

  return (
    <div className="space-y-4">
      <div
        className={`rounded-2xl border p-4 ${over ? "border-red-500/40 bg-red-500/10" : "border-white/10 bg-white/5"}`}
      >
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Tổng giờ quy đổi cả khoá</p>
            <p className="mt-1 font-mono text-2xl font-bold tabular-nums text-white">
              {total === null ? "—" : formatHours(total)}
              {cap !== null && <span className="text-base text-slate-500"> / {cap.toLocaleString("vi-VN")} giờ</span>}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-xs font-semibold text-slate-400">Ngưỡng</label>
            <input
              value={capDraft}
              onChange={(e) => setCapDraft(e.target.value)}
              inputMode="numeric"
              className="w-28 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-right font-mono text-sm tabular-nums text-white"
            />
            <button
              type="button"
              disabled={busy || capDraft === String(cap)}
              onClick={saveCap}
              className="inline-flex items-center gap-1.5 rounded-xl border border-white/15 px-3 py-2 text-sm font-semibold text-slate-200 disabled:opacity-40"
            >
              <Check size={14} />
              Lưu
            </button>
          </div>
        </div>
        {over && (
          <p className="mt-3 inline-flex items-center gap-2 rounded-xl bg-red-500/15 px-3 py-2 text-sm font-semibold text-red-200">
            <AlertTriangle size={15} />
            Đã vượt ngưỡng giờ đặt cho khoá — vượt {formatHours(total! - cap!)} giờ.
          </p>
        )}
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Giờ quy đổi theo tháng — cả đội</p>
        {months === null ? (
          <p className="mt-3 text-slate-500">Đang tải…</p>
        ) : months.length === 0 ? (
          <p className="mt-3 text-sm text-slate-500">
            Chưa có buổi nào được duyệt nên chưa vẽ được biểu đồ mùa vụ.
          </p>
        ) : (
          <div className="mt-4 flex h-44 items-end gap-2">
            {months.map((m) => (
              <div key={m.month} className="flex min-w-0 flex-1 flex-col items-center gap-1.5">
                <span className="font-mono text-[10px] tabular-nums text-slate-400">{formatHours(m.converted_hours)}</span>
                <div
                  className="w-full rounded-t bg-blue-500/80"
                  style={{ height: `${peak > 0 ? Math.max(4, (m.converted_hours / peak) * 100) : 4}%` }}
                  title={`${m.session_count} buổi`}
                />
                <span className="text-[10px] text-slate-500">{monthLabel(m.month)}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
