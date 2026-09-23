"use client";

import { useCallback, useEffect, useState } from "react";
import { Download, Flag } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { formatHours, formatVnd } from "@/lib/tro-giang/format";
import {
  createFlag,
  fetchAssistants,
  getMonthlyScore,
  type TaAssistant,
  type TaMonthlyScore,
} from "@/lib/tro-giang/queries";

import PolicyMonthlyReview from "./PolicyMonthlyReview";

interface Row {
  assistant: TaAssistant;
  score: TaMonthlyScore;
}

function currentMonthInput() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
}

function todayStr() {
  return new Date().toLocaleDateString("sv-SE");
}

export default function AdminMonthlyTable({ reloadKey = 0 }: { reloadKey?: number }) {
  const toast = useToast();
  const [month, setMonth] = useState(currentMonthInput());
  const [rows, setRows] = useState<Row[] | null>(null);
  const [flagFor, setFlagFor] = useState<TaAssistant | null>(null);
  const [flagNote, setFlagNote] = useState("");
  const [flagDate, setFlagDate] = useState(todayStr());
  const [busy, setBusy] = useState(false);

  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (month >= "2026-10") return;
    let cancelled = false;
    fetchAssistants()
      .then(async (assistants) => {
        const scores = await Promise.all(
          assistants.map((a) => getMonthlyScore(a.id, `${month}-01`)),
        );
        if (!cancelled) setRows(assistants.map((assistant, i) => ({ assistant, score: scores[i] })));
      })
      .catch(() => {
        if (!cancelled) setRows([]);
      });
    return () => {
      cancelled = true;
    };
  }, [month, reloadKey, refreshKey]);

  const load = useCallback(() => setRefreshKey((k) => k + 1), []);

  function exportCsv() {
    if (!rows) return;
    const header =
      "Trợ giảng,Bậc,Giờ quy đổi,Chạm HS (40),Phiếu lỗi (20),Phụ đạo (20),Tập trung (20),Tổng điểm,Thưởng/giờ,Tiền nền,Thưởng,Tiền chấm bài,Thực nhận";
    const lines = rows.map(({ assistant, score }) =>
      [
        assistant.short_name,
        assistant.tier,
        score.converted_hours,
        score.touches_score,
        score.error_note_score,
        score.phudao_score,
        score.focus_score,
        score.total_score,
        score.bonus_per_hour,
        score.base_pay,
        score.bonus_pay,
        score.grading_pay,
        score.total_pay,
      ].join(","),
    );
    const blob = new Blob(["﻿" + [header, ...lines].join("\n")], {
      type: "text/csv;charset=utf-8",
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `tro-giang-${month}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  async function submitFlag() {
    if (!flagFor) return;
    setBusy(true);
    try {
      await createFlag(flagFor.id, flagNote.trim(), flagDate);
      toast("success", `Đã ghi nhắc nhở cho ${flagFor.short_name}.`);
      setFlagFor(null);
      setFlagNote("");
      load();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không ghi được nhắc nhở.");
    } finally {
      setBusy(false);
    }
  }

  if (month >= "2026-10") return <div className="space-y-4"><div className="flex flex-wrap items-center gap-3"><label className="text-sm text-slate-300">Tháng <input aria-label="Tháng tổng hợp" type="month" value={month} onChange={e=>setMonth(e.target.value)} className="rounded-xl border border-white/10 bg-panel px-3 py-2 text-white"/></label><span className="text-sm text-blue-200">Quy chế Phần A · từ 01/10/2026</span></div><PolicyMonthlyReview key={month} month={`${month}-01`} reloadKey={reloadKey}/></div>;

  return (
    <div className="space-y-4">
      <button onClick={()=>setMonth("2026-10")} className="rounded-xl border border-blue-400/30 px-4 py-2 text-sm text-blue-200">Xem quy chế mới từ tháng 10/2026</button>
      <div className="flex flex-wrap items-center gap-3">
        <input
          type="month"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white"
        />
        <button
          type="button"
          onClick={exportCsv}
          disabled={!rows || rows.length === 0}
          className="inline-flex items-center gap-2 rounded-xl border border-white/15 px-4 py-2 text-sm font-semibold text-slate-200 disabled:opacity-40"
        >
          <Download size={15} />
          Xuất CSV
        </button>
      </div>

      {rows === null ? (
        <p className="text-slate-400">Đang tính điểm từng trợ giảng…</p>
      ) : rows.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">
          Chưa có trợ giảng nào. Chạy scripts/seed-tro-giang.mjs để tạo danh sách.
        </p>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-white/10">
          <table className="w-full min-w-[900px] text-sm">
            <thead className="bg-white/5 text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th className="px-4 py-3 text-left">Trợ giảng</th>
                <th className="px-3 py-3 text-right">Giờ QĐ</th>
                <th className="px-3 py-3 text-right">Chạm /40</th>
                <th className="px-3 py-3 text-right">Phiếu lỗi /20</th>
                <th className="px-3 py-3 text-right">Phụ đạo /20</th>
                <th className="px-3 py-3 text-right">Tập trung /20</th>
                <th className="px-3 py-3 text-right">Tổng</th>
                <th className="px-3 py-3 text-right">Tiền nền</th>
                <th className="px-3 py-3 text-right">Thưởng</th>
                <th className="px-3 py-3 text-right">Thực nhận</th>
                <th className="px-3 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {rows.map(({ assistant, score }) => (
                <tr key={assistant.id}>
                  <td className="px-4 py-3">
                    <span className="font-semibold text-white">{assistant.short_name}</span>
                    <span className="ml-2 rounded-full bg-white/10 px-2 py-0.5 text-[10px] font-bold text-slate-300">
                      {assistant.tier}
                      {assistant.retained_rate ? " · bảo lưu" : ""}
                    </span>
                  </td>
                  <td className="px-3 py-3 text-right font-mono tabular-nums text-slate-200">{formatHours(score.converted_hours)}</td>
                  <td className="px-3 py-3 text-right font-mono tabular-nums text-slate-300">{score.touches_score}</td>
                  <td className="px-3 py-3 text-right font-mono tabular-nums text-slate-300">{score.error_note_score}</td>
                  <td className="px-3 py-3 text-right font-mono tabular-nums text-slate-300">{score.phudao_score}</td>
                  <td className="px-3 py-3 text-right font-mono tabular-nums text-slate-300">{score.focus_score}</td>
                  <td
                    className={`px-3 py-3 text-right font-mono font-bold tabular-nums ${
                      score.total_score >= 85 ? "text-emerald-300" : score.total_score >= 70 ? "text-blue-300" : "text-amber-300"
                    }`}
                  >
                    {score.total_score}
                  </td>
                  <td className="px-3 py-3 text-right font-mono tabular-nums text-slate-200">{formatVnd(score.base_pay)}</td>
                  <td className="px-3 py-3 text-right font-mono tabular-nums text-slate-200">{formatVnd(score.bonus_pay)}</td>
                  <td className="px-3 py-3 text-right font-mono font-bold tabular-nums text-white">{formatVnd(score.total_pay)}</td>
                  <td className="px-3 py-3 text-right">
                    <button
                      type="button"
                      onClick={() => {
                        setFlagFor(assistant);
                        setFlagNote("");
                        setFlagDate(todayStr());
                      }}
                      title="Ghi nhắc nhở làm việc riêng"
                      className="rounded-lg border border-white/15 p-2 text-slate-400 hover:border-amber-400/40 hover:text-amber-300"
                    >
                      <Flag size={14} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {flagFor && (
        <div className="rounded-2xl border border-amber-400/30 bg-amber-500/10 p-4">
          <p className="font-semibold text-amber-100">Ghi nhắc nhở làm việc riêng — {flagFor.short_name}</p>
          <p className="mt-1 text-xs text-amber-200/80">Mỗi lượt trừ 10 điểm tiêu chí &quot;tập trung trong giờ&quot; của tháng.</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <input
              type="date"
              value={flagDate}
              onChange={(e) => setFlagDate(e.target.value)}
              className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white"
            />
            <input
              value={flagNote}
              onChange={(e) => setFlagNote(e.target.value)}
              placeholder="Ghi chú (ví dụ: dùng điện thoại riêng trong giờ dạy)"
              className="min-w-0 flex-1 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500"
            />
            <button
              type="button"
              disabled={busy}
              onClick={submitFlag}
              className="rounded-xl bg-amber-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
            >
              Ghi nhận
            </button>
            <button
              type="button"
              onClick={() => setFlagFor(null)}
              className="rounded-xl border border-white/15 px-4 py-2 text-sm font-semibold text-slate-300"
            >
              Huỷ
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
