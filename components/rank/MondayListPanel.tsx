"use client";

import { useEffect, useState } from "react";
import { Copy, Sparkles, TrendingUp } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import type { MondayList } from "@/features/rank/types";
import { fetchMondayList } from "@/services/rank";

const fmtDay = (iso: string) => new Date(`${iso}T00:00:00`).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" });
const pct = (n: number) => `${String(n).replace(".", ",")}%`;

/**
 * Danh sách thứ Hai cho thầy: 5 em lên mức (huy hiệu/bậc) + 5 em tiến bộ nhất của TUẦN VỪA QUA,
 * để nhắc tên trước lớp — ghi nhận qua thầy quan trọng hơn qua web với nhóm dưới (GĐ 1b #9).
 * Chưa chạy migration 20260930150000 hoặc chưa có dữ liệu → ẩn hẳn, không báo lỗi.
 */
export default function MondayListPanel({ classId }: { classId: number }) {
  const toast = useToast();
  const [data, setData] = useState<MondayList | null | undefined>(undefined);

  useEffect(() => {
    let cancelled = false;
    fetchMondayList(classId)
      .then((d) => { if (!cancelled) setData(d); })
      .catch(() => { if (!cancelled) setData(null); });
    return () => { cancelled = true; };
  }, [classId]);

  if (!data) return null;
  const empty = data.level_ups.length === 0 && data.improved.length === 0;

  function copyText() {
    if (!data) return;
    const lines = [`Ghi nhận tuần ${fmtDay(data.week_start)}–${fmtDay(data.week_end)}`];
    if (data.level_ups.length) {
      lines.push("Lên mức:");
      for (const m of data.level_ups) lines.push(`- ${m.name}: ${m.items.join(", ")}`);
    }
    if (data.improved.length) {
      lines.push("Tiến bộ nhất:");
      for (const m of data.improved) lines.push(`- ${m.name}: tỉ lệ đúng ${pct(m.acc_base)} → ${pct(m.acc_now)} (+${String(m.gain).replace(".", ",")} điểm %)`);
    }
    navigator.clipboard.writeText(lines.join("\n")).then(
      () => toast("success", "Đã chép danh sách"),
      () => toast("error", "Không chép được"),
    );
  }

  return (
    <section className="rounded-2xl border border-amber-300/20 bg-amber-500/[.05] p-5">
      <div className="mb-3 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2 text-amber-300">
          <Sparkles size={18} />
          <h3 className="font-display text-lg font-bold text-white">Danh sách thứ Hai</h3>
          <span className="text-xs text-slate-400">tuần {fmtDay(data.week_start)}–{fmtDay(data.week_end)}</span>
        </div>
        {!empty && (
          <button type="button" onClick={copyText} className="admin-chip flex items-center gap-1.5">
            <Copy size={13} /> Chép
          </button>
        )}
      </div>
      {empty ? (
        <p className="text-sm text-slate-400">Tuần vừa rồi chưa có em nào lên mức hay đủ dữ liệu để xét tiến bộ.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <p className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-400">
              <Sparkles size={13} /> Lên mức
            </p>
            <ul className="space-y-1.5 text-sm">
              {data.level_ups.map((m) => (
                <li key={m.student_id} className="text-slate-300">
                  <b className="text-white">{m.name}</b>
                  <span className="block text-xs text-slate-400">{m.items.join(" · ")}</span>
                </li>
              ))}
              {data.level_ups.length === 0 && <li className="text-xs text-slate-500">Chưa có.</li>}
            </ul>
          </div>
          <div>
            <p className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-400">
              <TrendingUp size={13} /> Tiến bộ nhất
            </p>
            <ul className="space-y-1.5 text-sm">
              {data.improved.map((m) => (
                <li key={m.student_id} className="text-slate-300">
                  <b className="text-white">{m.name}</b>
                  <span className="block text-xs text-slate-400">
                    tỉ lệ đúng {pct(m.acc_base)} → {pct(m.acc_now)}{" "}
                    <b className="text-emerald-300">+{String(m.gain).replace(".", ",")} điểm %</b>
                  </span>
                </li>
              ))}
              {data.improved.length === 0 && <li className="text-xs text-slate-500">Chưa có (cần ≥ 15 câu ở mỗi mốc so sánh).</li>}
            </ul>
          </div>
        </div>
      )}
    </section>
  );
}
