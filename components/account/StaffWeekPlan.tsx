"use client";
import { useEffect, useState } from "react";
import { CalendarDays } from "lucide-react";
import { getSupabase } from "@/services/supabase";

type PlanEvent = { weekday: number; start: string; end: string; title: string; where?: string; src: string; note?: string; clash?: boolean };
type Plan = { week_start: string; events: PlanEvent[]; warnings: string[]; updated_at: string };

const DAY = ["", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"];
const SRC_STYLE: Record<string, string> = {
  thachlab: "border-l-blue-500",
  "TKB Cao Thắng": "border-l-orange-500",
  "lịch công tác": "border-l-rose-500",
  "xếp tự động": "border-l-emerald-500",
  "cố định": "border-l-slate-400",
};

const pad = (n: number) => String(n).padStart(2, "0");
const iso = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
function mondayIso(offsetWeeks: number) {
  const d = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Ho_Chi_Minh" }));
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7) + offsetWeeks * 7);
  return iso(d);
}
function dayLabel(weekStart: string, weekday: number) {
  const d = new Date(`${weekStart}T00:00:00`);
  d.setDate(d.getDate() + weekday - 1);
  return `${DAY[weekday]} ${pad(d.getDate())}/${pad(d.getMonth() + 1)}`;
}

export default function StaffWeekPlan() {
  const [plans, setPlans] = useState<Plan[] | null>(null);
  const [error, setError] = useState("");
  const [week, setWeek] = useState(mondayIso(0));
  const today = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Ho_Chi_Minh" }));
  const todayIso = iso(today);

  useEffect(() => {
    getSupabase().from("staff_week_plans").select("week_start, events, warnings, updated_at").gte("week_start", mondayIso(-1)).order("week_start")
      .then(({ data, error: e }) => {
        if (e) { setError("Không tải được lịch tuần."); setPlans([]); return; }
        const list = (data ?? []) as Plan[];
        setPlans(list);
        if (list.length && !list.some((p) => p.week_start === mondayIso(0))) setWeek(list[list.length - 1].week_start);
      });
  }, []);

  const plan = plans?.find((p) => p.week_start === week);
  const weeks = plans?.map((p) => p.week_start) ?? [];

  return (
    <section className="mt-6 rounded-3xl border border-line bg-panel p-5 sm:p-8" aria-labelledby="lich-tuan-title">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 id="lich-tuan-title" className="flex items-center gap-2 font-display text-xl font-bold text-ink"><CalendarDays size={20} className="text-primary" />Lịch tuần</h2>
        {weeks.length > 1 && (
          <div className="flex gap-2" role="tablist" aria-label="Chọn tuần">
            {weeks.map((w) => (
              <button key={w} type="button" role="tab" aria-selected={w === week} onClick={() => setWeek(w)}
                className={`min-h-11 rounded-xl border px-4 py-2 text-sm font-semibold ${w === week ? "border-primary bg-primary-soft text-ink" : "border-line text-ink hover:border-line-strong"}`}>
                {dayLabel(w, 1).slice(-5)}–{dayLabel(w, 7).slice(-5)}
              </button>
            ))}
          </div>
        )}
      </div>

      {plans === null && <p className="mt-4 text-sm text-muted">Đang tải lịch tuần…</p>}
      {error && <p className="mt-4 text-sm text-amber-200">{error}</p>}
      {plans && !plan && !error && <p className="mt-4 text-sm text-muted">Chưa có lịch cho tuần này. Nhờ Claude chạy <code>/lich-tuan</code> để cập nhật.</p>}

      {plan && (
        <>
          <div className="mt-4 space-y-4">
            {[1, 2, 3, 4, 5, 6, 7].map((wd) => {
              const evs = plan.events.filter((e) => e.weekday === wd).sort((a, b) => a.start.localeCompare(b.start));
              const isToday = plan.week_start && (() => { const d = new Date(`${plan.week_start}T00:00:00`); d.setDate(d.getDate() + wd - 1); return iso(d) === todayIso; })();
              return (
                <div key={wd} className={`rounded-2xl border p-4 ${isToday ? "border-primary bg-primary-soft" : "border-line"}`}>
                  <h3 className="text-sm font-bold text-ink">{dayLabel(plan.week_start, wd)}{isToday && <span className="ml-2 text-xs text-primary">Hôm nay</span>}</h3>
                  {evs.length === 0 ? <p className="mt-2 text-sm text-muted">Trống</p> : (
                    <ul className="mt-2 space-y-2">
                      {evs.map((e, i) => (
                        <li key={i} className={`rounded-lg border-l-4 bg-surface-2 px-3 py-2 ${SRC_STYLE[e.src] ?? "border-l-slate-400"}`}>
                          <p className="text-sm font-semibold text-ink"><span className="tabular-nums">{e.start}–{e.end}</span> · {e.title}</p>
                          {e.where && <p className="text-sm text-muted">{e.where}</p>}
                          {e.clash && <p className="text-sm font-semibold text-amber-300">Trùng giờ với mục khác</p>}
                          {e.note && <p className="text-xs text-muted">{e.note}</p>}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              );
            })}
          </div>
          {plan.warnings.length > 0 && (
            <ul className="mt-4 space-y-1 text-sm text-amber-200">{plan.warnings.map((w, i) => <li key={i}>{w}</li>)}</ul>
          )}
          <p className="mt-4 text-xs text-muted">Cập nhật {new Date(plan.updated_at).toLocaleString("vi-VN")}</p>
        </>
      )}
    </section>
  );
}
