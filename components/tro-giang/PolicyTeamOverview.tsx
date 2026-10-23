"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, ChevronRight } from "lucide-react";
import { flagSession } from "@/lib/tro-giang/co-bat-thuong";
import { formatHours, formatVnd } from "@/lib/tro-giang/format";
import { getPolicyMonth, getPolicySessions, POLICY_SCORES, type MonthPolicy } from "@/lib/tro-giang/policy";
import { fetchAssistants, fetchFlagContext, type TaAssistant, type TaSessionRow } from "@/lib/tro-giang/queries";

interface Row {
  assistant: TaAssistant;
  month?: MonthPolicy;
  error?: string;
  red: number;
  amber: number;
  sessionCount: number;
}

const SEGMENT_COLOR: Record<string, string> = {
  touches: "bg-violet-500",
  phudao: "bg-emerald-500",
  homework: "bg-blue-500",
  attendance: "bg-amber-500",
  observation: "bg-slate-400",
};

const budgetKey = (month: string) => `ta-budget-${month.slice(0, 7)}`;

function readBudget(month: string): string {
  try {
    return localStorage.getItem(budgetKey(month)) ?? "";
  } catch {
    return "";
  }
}

export default function PolicyTeamOverview({ month, onOpen }: { month: string; onOpen: (assistantId: string) => void }) {
  const [rows, setRows] = useState<Row[] | null>(null);
  const [error, setError] = useState("");
  const [budget, setBudget] = useState(() => readBudget(month));

  useEffect(() => {
    let active = true;
    (async () => {
      const assistants = (await fetchAssistants()).filter((a) => a.active);
      const loaded = await Promise.all(
        assistants.map(async (assistant) => {
          try {
            const [score, sessions] = await Promise.all([getPolicyMonth(assistant.id, month), getPolicySessions(assistant.id, month)]);
            return { assistant, month: score, sessions };
          } catch (e) {
            return { assistant, error: e instanceof Error ? e.message : "Không tải được", sessions: [] as TaSessionRow[] };
          }
        }),
      );
      const live = loaded.flatMap((l) => l.sessions.filter((s) => s.status !== "rejected"));
      const ctx = await fetchFlagContext(live).catch(() => ({ history: live, passRatios: new Map<string, number | null>() }));
      const result: Row[] = loaded.map((l) => {
        let red = 0;
        let amber = 0;
        const mine = l.sessions.filter((s) => s.status !== "rejected");
        for (const s of mine) {
          const flags = flagSession(s, ctx.history, ctx.passRatios.get(s.id));
          if (flags.some((f) => f.level === "red")) red += 1;
          else if (flags.length) amber += 1;
        }
        return { assistant: l.assistant, month: l.month, error: l.error, red, amber, sessionCount: mine.length };
      });
      if (active) setRows(result);
    })().catch((e) => {
      if (active) setError(e instanceof Error ? e.message : "Không tải được bảng cả đội.");
    });
    return () => {
      active = false;
    };
  }, [month]);

  const summary = useMemo(() => {
    const ok = (rows ?? []).filter((r) => r.month);
    const pay = ok.reduce((sum, r) => sum + (r.month?.total_pay ?? 0), 0);
    const waiting = ok.filter((r) => (r.month?.missing.length ?? 0) > 0).length;
    const attention = (rows ?? []).filter((r) => r.red > 0 || r.amber > 0 || (r.month?.total_score ?? 100) < 70).length;
    const reds = (rows ?? []).reduce((sum, r) => sum + r.red, 0);
    return { pay, waiting, attention, reds };
  }, [rows]);

  const budgetNumber = Number(budget.replace(/\D/g, "")) * 1_000_000;
  const budgetPct = budgetNumber > 0 ? Math.round((summary.pay / budgetNumber) * 100) : null;

  function saveBudget(value: string) {
    setBudget(value);
    try {
      localStorage.setItem(budgetKey(month), value);
    } catch {
      /* chỉ là tiện lợi cho riêng thầy, không có thì thôi */
    }
  }

  if (error) return <p role="alert" className="rounded-xl bg-red-500/10 p-4 text-red-200">{error}</p>;
  if (rows === null) return <p className="text-slate-400">Đang tải bảng cả đội…</p>;
  if (rows.length === 0)
    return <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Chưa có trợ giảng nào đang hoạt động.</p>;

  const sorted = [...rows].sort((a, b) => b.red - a.red || b.amber - a.amber || (a.month?.total_score ?? 101) - (b.month?.total_score ?? 101));

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-3">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Tiền tạm tính cả đội</p>
          <p className="mt-1 font-mono text-2xl font-bold tabular-nums text-white">{formatVnd(summary.pay)}</p>
          <label className="mt-2 flex items-center gap-2 text-xs text-slate-400">
            Ngân sách (triệu đồng)
            <input
              inputMode="numeric"
              value={budget}
              onChange={(e) => saveBudget(e.target.value.replace(/\D/g, ""))}
              placeholder="15"
              className="w-16 rounded-lg border border-white/10 bg-white/5 px-2 py-1 text-right font-mono text-white"
            />
          </label>
          {budgetPct !== null && (
            <div className="mt-2">
              <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
                <div className={`h-full ${budgetPct > 100 ? "bg-red-500" : budgetPct > 85 ? "bg-amber-500" : "bg-emerald-500"}`} style={{ width: `${Math.min(100, budgetPct)}%` }} />
              </div>
              <p className="mt-1 text-xs text-slate-400">Đã dùng {budgetPct}% ngân sách</p>
            </div>
          )}
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Cần thầy xem</p>
          <p className="mt-1 text-2xl font-bold text-white">{summary.attention} / {rows.length} người</p>
          <p className={`mt-2 text-xs ${summary.reds ? "text-red-300" : "text-slate-400"}`}>{summary.reds ? `${summary.reds} buổi có cờ đỏ` : "Không có cờ đỏ"}</p>
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Chưa đủ để chốt</p>
          <p className="mt-1 text-2xl font-bold text-white">{summary.waiting} người</p>
          <p className="mt-2 text-xs text-slate-400">Còn buổi chờ duyệt hoặc thiếu đơn giá</p>
        </div>
      </div>

      <ul className="space-y-2">
        {sorted.map((r) => {
          const m = r.month;
          return (
            <li key={r.assistant.id}>
              <button
                type="button"
                onClick={() => onOpen(r.assistant.id)}
                className="flex w-full flex-wrap items-center gap-x-4 gap-y-2 rounded-2xl border border-white/10 bg-white/5 p-4 text-left hover:border-white/25"
              >
                <span className="min-w-[8rem] flex-1">
                  <span className="block font-semibold text-white">{r.assistant.short_name}</span>
                  <span className="text-xs text-slate-400">
                    {m ? `${formatHours(m.class_hours + m.teaching_hours)} giờ lớp · ${m.tutoring_count} buổi phụ đạo` : r.error}
                    {m?.closed_at ? " · đã chốt" : ""}
                  </span>
                </span>
                {m && (
                  <span className="order-last w-full sm:order-none sm:w-56" aria-hidden>
                    <span className="flex h-2 overflow-hidden rounded-full bg-white/10">
                      {POLICY_SCORES.map(([key, , max]) => (
                        <span key={key} className={SEGMENT_COLOR[key]} style={{ width: `${((m[key] ?? 0) / 100) * 100}%` }} title={`${key} ${m[key] ?? 0}/${max}`} />
                      ))}
                    </span>
                  </span>
                )}
                {m && (
                  <span className={`font-mono text-lg font-bold tabular-nums ${m.total_score === null ? "text-slate-500" : m.total_score >= 85 ? "text-emerald-300" : m.total_score >= 70 ? "text-blue-300" : "text-amber-300"}`}>
                    {m.total_score ?? "—"}
                  </span>
                )}
                {r.red > 0 && (
                  <span className="inline-flex items-center gap-1 rounded-full bg-red-500/20 px-2.5 py-1 text-xs font-semibold text-red-300">
                    <AlertTriangle size={12} /> {r.red} cờ đỏ
                  </span>
                )}
                {r.amber > 0 && (
                  <span className="inline-flex items-center gap-1 rounded-full bg-amber-500/15 px-2.5 py-1 text-xs font-semibold text-amber-300">
                    <AlertTriangle size={12} /> {r.amber} cờ vàng
                  </span>
                )}
                {r.red === 0 && r.amber === 0 && r.sessionCount > 0 && (
                  <span className="rounded-full bg-emerald-500/15 px-2.5 py-1 text-xs font-semibold text-emerald-300">Sạch</span>
                )}
                {m && (
                  <span className="font-mono text-sm font-semibold tabular-nums text-white">
                    {m.total_pay === null ? "Chờ đủ dữ liệu" : formatVnd(m.total_pay)}
                  </span>
                )}
                <ChevronRight size={16} className="text-slate-500" />
              </button>
            </li>
          );
        })}
      </ul>

      <p className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-400">
        {POLICY_SCORES.map(([key, label]) => (
          <span key={key} className="inline-flex items-center gap-1.5">
            <span className={`inline-block h-2.5 w-2.5 rounded-sm ${SEGMENT_COLOR[key]}`} />
            {label}
          </span>
        ))}
      </p>
    </div>
  );
}
