"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { CalendarDays } from "lucide-react";
import { getSupabase } from "@/services/supabase";

type PlanEvent = { weekday: number; start: string; end: string; title: string; where?: string; src: string; note?: string; clash?: boolean };
type Plan = { week_start: string; events: PlanEvent[]; warnings: string[]; updated_at: string };

const DAY = ["", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"];
const DAY_SHORT = ["", "T2", "T3", "T4", "T5", "T6", "T7", "CN"];
// Màu viền trái theo nguồn + chú giải (điểm 6)
const SRC: { key: string; label: string; border: string; dot: string }[] = [
  { key: "thachlab", label: "Thachlab", border: "border-l-blue-500", dot: "bg-blue-500" },
  { key: "TKB Cao Thắng", label: "Cao Thắng", border: "border-l-orange-500", dot: "bg-orange-500" },
  { key: "lịch công tác", label: "Lịch công tác", border: "border-l-rose-500", dot: "bg-rose-500" },
  { key: "cố định", label: "Cố định", border: "border-l-slate-400", dot: "bg-slate-400" },
  { key: "xếp tự động", label: "Tập luyện", border: "border-l-emerald-500", dot: "bg-emerald-500" },
];
const srcOf = (s: string) => SRC.find((x) => x.key === s) ?? SRC[3];

const pad = (n: number) => String(n).padStart(2, "0");
const iso = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const nowVN = () => new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Ho_Chi_Minh" }));
function mondayIso(offsetWeeks: number) {
  const d = nowVN();
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7) + offsetWeeks * 7);
  return iso(d);
}
function dateOf(weekStart: string, weekday: number) {
  const d = new Date(`${weekStart}T00:00:00`);
  d.setDate(d.getDate() + weekday - 1);
  return d;
}
const dm = (d: Date) => `${pad(d.getDate())}/${pad(d.getMonth() + 1)}`;
const toMin = (hhmm: string) => { const [h, m] = hhmm.split(":").map(Number); return h * 60 + m; };
function fmtDur(min: number) {
  const h = Math.floor(min / 60), m = min % 60;
  return h ? `${h} giờ${m ? ` ${m} phút` : ""}` : `${m} phút`;
}
// Bỏ chuỗi gỡ lỗi của script còn sót trong dữ liệu cũ (điểm 5)
const cleanNote = (n?: string) => n?.replace(/\s*·?\s*khớp "[^"]*"/g, "").trim() || "";

type Kind = "day" | "truot" | "gym" | "truong";
function kindOf(e: PlanEvent): Kind {
  const t = e.title.toLowerCase();
  if (t.includes("trượt băng")) return "truot";
  if (t.includes("gym")) return "gym";
  if (e.src === "thachlab" || e.src === "TKB Cao Thắng" || t.startsWith("dạy")) return "day";
  return "truong";
}

function EventItem({ e, compact }: { e: PlanEvent; compact?: boolean }) {
  const note = cleanNote(e.note);
  const s = srcOf(e.src);
  return (
    <li className={`rounded-lg border-l-4 bg-surface-2 ${compact ? "px-2 py-1.5" : "px-3 py-2"} ${s.border}`}>
      {compact ? (
        <>
          <p className="whitespace-nowrap text-xs font-semibold tabular-nums text-ink">{e.start}–{e.end}</p>
          <p className="line-clamp-3 text-xs font-semibold leading-snug text-ink" title={e.title}>
            {e.title}{e.where && <span className="font-normal text-muted"> · {e.where}</span>}
          </p>
        </>
      ) : (
        <p className="line-clamp-2 text-sm font-semibold leading-snug text-ink" title={e.title}>
          <span className="tabular-nums">{e.start}–{e.end}</span> · {e.title}
          {e.where && <span className="font-normal text-muted"> · {e.where}</span>}
        </p>
      )}
      {e.clash && <p className="text-xs font-semibold text-warn">⚠ Trùng giờ với mục khác</p>}
      {(note || e.title.length > 60) && (
        <details className="mt-0.5">
          <summary className="cursor-pointer select-none text-xs text-muted">Chi tiết</summary>
          {e.title.length > 60 && <p className="mt-1 text-xs text-ink">{e.title}</p>}
          {note && <p className="mt-1 text-xs text-muted">{note}</p>}
        </details>
      )}
    </li>
  );
}

export default function StaffWeekPlan() {
  const [plans, setPlans] = useState<Plan[] | null>(null);
  const [error, setError] = useState("");
  const [week, setWeek] = useState(mondayIso(0));
  const [day, setDay] = useState(() => ((nowVN().getDay() + 6) % 7) + 1);
  const [tick, setTick] = useState(0);
  const touchX = useRef<number | null>(null);
  const now = nowVN();
  const todayIso = iso(now);
  const nowMin = now.getHours() * 60 + now.getMinutes();

  useEffect(() => {
    getSupabase().from("staff_week_plans").select("week_start, events, warnings, updated_at").gte("week_start", mondayIso(-1)).order("week_start")
      .then(({ data, error: e }) => {
        if (e) { setError("Không tải được lịch tuần."); setPlans([]); return; }
        const list = (data ?? []) as Plan[];
        setPlans(list);
        if (list.length && !list.some((p) => p.week_start === mondayIso(0))) { setWeek(list[list.length - 1].week_start); setDay(1); }
      });
    const t = setInterval(() => setTick((x) => x + 1), 60_000); // cập nhật dòng "Tiếp theo" mỗi phút
    return () => clearInterval(t);
  }, []);

  const plan = plans?.find((p) => p.week_start === week);
  const weeks = plans?.map((p) => p.week_start) ?? [];
  const isCurrentWeek = week === mondayIso(0);
  const todayWd = ((now.getDay() + 6) % 7) + 1;

  const byDay = useMemo(() => {
    const m: PlanEvent[][] = [[], [], [], [], [], [], [], []];
    plan?.events.forEach((e) => m[e.weekday]?.push(e));
    m.forEach((l) => l.sort((a, b) => a.start.localeCompare(b.start)));
    return m;
  }, [plan]);

  // Điểm 4: tổng kết tuần
  const summary = useMemo(() => {
    const c = { day: 0, truot: 0, gym: 0, truong: 0 };
    plan?.events.forEach((e) => { c[kindOf(e)]++; });
    return c;
  }, [plan]);

  // Điểm 3: mục đang diễn ra / kế tiếp (chỉ tuần hiện tại)
  const next = useMemo(() => {
    void tick;
    if (!plan) return null;
    if (week > mondayIso(0)) { // tuần tới: mục đầu tiên của tuần
      for (let wd = 1; wd <= 7; wd++) if (byDay[wd].length) return { e: byDay[wd][0], label: `Mở đầu tuần · ${DAY[wd]}`, rest: "" };
      return null;
    }
    if (!isCurrentWeek) return null;
    const today = byDay[todayWd];
    const cur = today.find((e) => toMin(e.start) <= nowMin && nowMin < toMin(e.end));
    if (cur) return { e: cur, label: "Đang diễn ra", rest: `còn ${fmtDur(toMin(cur.end) - nowMin)}` };
    const later = today.find((e) => toMin(e.start) > nowMin);
    if (later) return { e: later, label: "Tiếp theo", rest: `còn ${fmtDur(toMin(later.start) - nowMin)}` };
    for (let wd = todayWd + 1; wd <= 7; wd++) if (byDay[wd].length) return { e: byDay[wd][0], label: `Tiếp theo · ${DAY[wd]}`, rest: "" };
    return { e: null, label: "Tuần này đã xong", rest: "" };
  }, [plan, week, isCurrentWeek, byDay, todayWd, nowMin, tick]);

  const weekRange = plan ? `${dm(dateOf(plan.week_start, 1))}–${dm(dateOf(plan.week_start, 7))}` : "";
  const dayIso = (wd: number) => (plan ? iso(dateOf(plan.week_start, wd)) : "");

  const onTouchStart = (x: number) => { touchX.current = x; };
  const onTouchEnd = (x: number) => {
    if (touchX.current === null) return;
    const dx = x - touchX.current; touchX.current = null;
    if (Math.abs(dx) < 50) return;
    setDay((d) => Math.min(7, Math.max(1, d + (dx < 0 ? 1 : -1))));
  };

  return (
    <section className="mt-6 rounded-3xl border border-line bg-panel p-5 sm:p-8" aria-labelledby="lich-tuan-title">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 id="lich-tuan-title" className="flex items-center gap-2 font-display text-xl font-bold text-ink">
          <CalendarDays size={20} className="text-primary" />Lịch tuần{weekRange && <span className="ml-2 font-semibold text-muted">{weekRange}</span>}
        </h2>
        {weeks.length > 1 && (
          <div className="flex gap-2" role="tablist" aria-label="Chọn tuần">
            {weeks.map((w) => (
              <button key={w} type="button" role="tab" aria-selected={w === week} onClick={() => { setWeek(w); setDay(w === mondayIso(0) ? todayWd : 1); }}
                className={`min-h-11 rounded-xl border px-4 py-2 text-sm font-semibold ${w === week ? "border-primary bg-primary-soft text-ink" : "border-line text-ink hover:border-line-strong"}`}>
                {dm(dateOf(w, 1))}–{dm(dateOf(w, 7))}
              </button>
            ))}
          </div>
        )}
      </div>

      {plans === null && <p className="mt-4 text-sm text-muted">Đang tải lịch tuần…</p>}
      {error && <p className="mt-4 text-sm text-warn">{error}</p>}
      {plans && !plan && !error && <p className="mt-4 text-sm text-muted">Chưa có lịch cho tuần này. Nhờ Claude chạy <code>/lich-tuan</code> để cập nhật.</p>}

      {plan && (
        <>
          {next && (
            <p className="mt-4 rounded-xl border border-primary bg-primary-soft px-4 py-3 text-sm text-ink">
              <span className="font-bold">{next.label}</span>
              {next.e && <>: <span className="tabular-nums font-semibold">{next.e.start}</span> {next.e.title}{next.e.where && <span className="text-muted"> · {next.e.where}</span>}</>}
              {next.rest && <span className="text-muted"> · {next.rest}</span>}
            </p>
          )}

          <p className="mt-3 text-sm text-muted">
            {summary.day} buổi dạy · {summary.truot} trượt băng{summary.truot < 3 && <span className="font-semibold text-warn"> (thiếu)</span>} · {summary.gym} gym{summary.gym < 2 && <span className="font-semibold text-warn"> (thiếu)</span>} · {summary.truong} việc trường
          </p>

          <ul className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted" aria-label="Chú giải màu">
            {SRC.map((s) => <li key={s.key} className="flex items-center gap-1.5"><span className={`inline-block h-2.5 w-2.5 rounded-full ${s.dot}`} />{s.label}</li>)}
          </ul>

          {/* Điểm 1: mobile — dải 7 ngày, xem một ngày, vuốt để sang ngày */}
          <div className="md:hidden">
            <div className="mt-4 grid grid-cols-7 gap-1" role="tablist" aria-label="Chọn ngày">
              {[1, 2, 3, 4, 5, 6, 7].map((wd) => {
                const isToday = dayIso(wd) === todayIso;
                const sel = wd === day;
                return (
                  <button key={wd} type="button" role="tab" aria-selected={sel} onClick={() => setDay(wd)}
                    className={`flex min-h-14 flex-col items-center justify-center rounded-xl border text-sm ${sel ? "border-primary bg-primary-soft font-bold text-ink" : "border-line text-ink"}`}>
                    <span className={isToday ? "text-primary" : ""}>{DAY_SHORT[wd]}</span>
                    <span className="tabular-nums text-xs text-muted">{pad(dateOf(plan.week_start, wd).getDate())}</span>
                    <span className="mt-0.5 flex gap-0.5">{byDay[wd].slice(0, 5).map((e, i) => <span key={i} className={`h-1 w-1 rounded-full ${srcOf(e.src).dot}`} />)}</span>
                  </button>
                );
              })}
            </div>
            <div className="mt-3 rounded-2xl border border-line p-3" onTouchStart={(ev) => onTouchStart(ev.touches[0].clientX)} onTouchEnd={(ev) => onTouchEnd(ev.changedTouches[0].clientX)}>
              <h3 className="text-sm font-bold text-ink">{DAY[day]} {dm(dateOf(plan.week_start, day))}{dayIso(day) === todayIso && <span className="ml-2 text-xs text-primary">Hôm nay</span>}</h3>
              {byDay[day].length === 0 ? <p className="mt-2 text-sm text-muted">Trống</p> : (
                <ul className="mt-2 space-y-2">{byDay[day].map((e, i) => <EventItem key={i} e={e} />)}</ul>
              )}
            </div>
          </div>

          {/* Điểm 2: desktop — lưới 7 cột */}
          <div className="mt-4 hidden grid-cols-7 gap-2 md:grid">
            {[1, 2, 3, 4, 5, 6, 7].map((wd) => {
              const isToday = dayIso(wd) === todayIso;
              return (
                <div key={wd} className={`min-w-0 rounded-2xl border p-2 ${isToday ? "border-primary bg-primary-soft" : "border-line"}`}>
                  <h3 className="text-sm font-bold text-ink">{DAY_SHORT[wd]} <span className="tabular-nums font-semibold text-muted">{dm(dateOf(plan.week_start, wd))}</span>{isToday && <span className="ml-1 text-xs text-primary">Hôm nay</span>}</h3>
                  {byDay[wd].length === 0 ? <p className="mt-2 text-xs text-muted">Trống</p> : (
                    <ul className="mt-2 space-y-1.5">{byDay[wd].map((e, i) => <EventItem key={i} e={e} compact />)}</ul>
                  )}
                </div>
              );
            })}
          </div>

          {plan.warnings.length > 0 && (
            <ul className="mt-4 space-y-1 text-sm text-warn">{plan.warnings.map((w, i) => <li key={i}>{w}</li>)}</ul>
          )}
          <p className="mt-4 text-xs text-muted">Cập nhật {new Date(plan.updated_at).toLocaleString("vi-VN")}</p>
        </>
      )}
    </section>
  );
}
