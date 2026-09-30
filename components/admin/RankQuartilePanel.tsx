"use client";

import { useEffect, useState } from "react";
import type { QuartileGroup, QuartileMetrics } from "@/features/rank/types";
import { fetchQuartileMetrics, type RankSeason } from "@/services/rank";

const pct = (a: number | null | undefined, n: number) => (a === null || a === undefined || n === 0 ? "—" : `${Math.round((100 * a) / n)}%`);

/**
 * Đo nhóm 25% thấp nhất (GĐ 1b #10): nhóm chọn theo tỉ lệ đúng 28 ngày TRƯỚC khi mở mùa.
 * Ba số cần theo dõi — còn làm bài ở tuần 4–5, nhận ≥ 1 huy hiệu, thoát ≥ 1 chủ đề phụ đạo.
 * Nếu ba số của nhóm thấp không nhúc nhích so với nhóm còn lại = hệ đang nới khoảng cách.
 */
export default function RankQuartilePanel({ season }: { season: RankSeason }) {
  const [data, setData] = useState<QuartileMetrics | null | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchQuartileMetrics(season.id)
      .then((d) => { if (!cancelled) setData(d); })
      .catch((e) => { if (!cancelled) { setData(null); setError(e instanceof Error ? e.message : "Không tải được (đã chạy migration 20260930150000 chưa?)"); } });
    return () => { cancelled = true; };
  }, [season.id]);

  if (data === undefined) return <p className="admin-empty">Đang tính…</p>;
  if (!data) return <p className="admin-empty">{error ?? "Không có dữ liệu."}</p>;

  const bottom = data.groups.bottom;
  const rest = data.groups.rest;
  const rows: { label: string; hint: string; get: (g: QuartileGroup) => number | null }[] = [
    { label: "Còn làm bài trong mùa", hint: "≥ 1 lượt làm bài từ ngày mở mùa", get: (g) => g.active_season },
    { label: "Còn làm bài ở tuần 4–5", hint: data.w45_ready ? "≥ 1 lượt trong ngày 22–35 của mùa" : "chưa tới tuần 4 của mùa", get: (g) => g.active_w45 },
    { label: "Nhận ≥ 1 huy hiệu", hint: "danh hiệu/mức danh hiệu mới trong mùa", get: (g) => g.with_badge },
    { label: "Thoát ≥ 1 chủ đề phụ đạo", hint: "trạng thái “đã thoát” trong mùa", get: (g) => g.cleared },
  ];

  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-400">
        Nhóm 25% thấp nhất theo <b className="text-slate-200">{data.baseline}</b>. Nhóm “Còn lại” để so sánh; em chưa đủ dữ liệu trước mùa
        ({data.groups.no_baseline?.n ?? 0} em) không xếp nhóm.
      </p>
      {!bottom ? (
        <p className="admin-empty">Chưa đủ dữ liệu trước mùa để chọn nhóm 25% thấp nhất.</p>
      ) : (
        <div className="admin-table-wrap">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-slate-400">
                <th className="p-2">Chỉ số</th>
                <th className="p-2">Nhóm 25% thấp ({bottom.n} em)</th>
                <th className="p-2">Còn lại ({rest?.n ?? 0} em)</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const b = r.get(bottom);
                const o = rest ? r.get(rest) : null;
                return (
                  <tr key={r.label} className="border-t border-white/5">
                    <td className="p-2">
                      <span className="block text-slate-200">{r.label}</span>
                      <span className="block text-xs text-slate-500">{r.hint}</span>
                    </td>
                    <td className="p-2 font-semibold text-amber-300">
                      {pct(b, bottom.n)} <span className="text-xs font-normal text-slate-500">{b === null ? "" : `(${b})`}</span>
                    </td>
                    <td className="p-2 text-slate-300">
                      {rest ? pct(o, rest.n) : "—"} <span className="text-xs text-slate-500">{o === null || !rest ? "" : `(${o})`}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
