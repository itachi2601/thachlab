"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Sparkles, TrendingUp } from "lucide-react";
import RankBadge from "@/components/rank/RankBadge";
import TierName from "@/components/rank/TierName";
import Avatar from "@/components/ui/Avatar";
import { divisionLabel, tierMeta, titleDisplay, type ClassRankGroups as Groups } from "@/features/rank/types";
import { fetchClassRankGroups } from "@/services/rank";

/**
 * Trang lớp: nhóm bạn theo bậc (tên xếp ABC — không thứ tự, không RP) + ghi nhận tuần này.
 * RPC rank_class_groups chỉ trả cho thành viên lớp / giáo viên lớp.
 */
export default function ClassRankGroups({ classId }: { classId: number }) {
  const [data, setData] = useState<Groups | null | undefined>(undefined);

  useEffect(() => {
    fetchClassRankGroups(classId).then(setData).catch(() => setData(null));
  }, [classId]);

  if (data === undefined || data === null || !data.season) return null;
  const tiers = data.tiers.filter((t) => t.members.length > 0);

  return (
    <section className="lesson-section">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2>Bậc trong lớp</h2>
        <Link href="/lop-hoc/xep-hang/" className="text-xs text-cyan-300 hover:underline">
          Xếp hạng của em →
        </Link>
      </div>
      <p className="lesson-muted mb-3 text-xs">Mùa {data.season.name} · cùng bậc là ngang nhau, không xếp thứ tự.</p>

      {tiers.length === 0 && data.unranked.length === 0 ? (
        <p className="text-sm text-slate-500">Lớp chưa có ai nhận RP trong mùa này.</p>
      ) : (
        <div className="space-y-3">
          {tiers.map((t) => {
            const meta = tierMeta(t.code);
            return (
              <div key={t.code} className="rounded-2xl border p-3 sm:p-4" style={{ borderColor: `${meta.color}44`, background: `${meta.color}0f` }}>
                <div className="mb-2 flex items-center gap-2">
                  <RankBadge code={t.code} size={28} />
                  <TierName code={t.code} size="sm" />
                  <span className="text-xs text-slate-500">· {t.members.length} bạn</span>
                </div>
                <ul className="flex flex-wrap gap-2">
                  {t.members.map((m, i) => (
                    <li key={`${m.name}-${i}`} className="flex items-center gap-1.5 rounded-full border border-white/10 bg-panel py-1 pl-1 pr-3 text-xs text-slate-200">
                      <Avatar url={m.avatar} name={m.name} size={18} />
                      {m.name}
                      {m.division && <span className="ml-1 text-slate-500">{divisionLabel(m.division)}</span>}
                      {m.title && (
                        <span className="ml-1 text-amber-200/80">
                          <Sparkles size={10} className="mr-0.5 inline" />
                          {titleDisplay(m.title.name, m.title.level)}
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
          {data.unranked.length > 0 && (
            <div className="rounded-2xl border border-dashed border-white/10 p-3 sm:p-4">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Chưa nhận RP · {data.unranked.length} bạn</p>
              <ul className="flex flex-wrap gap-2">
                {data.unranked.map((m, i) => (
                  <li key={`${m.name}-${i}`} className="flex items-center gap-1.5 rounded-full border border-white/5 py-1 pl-1 pr-3 text-xs text-slate-500">
                    <Avatar url={m.avatar} name={m.name} size={18} />
                    {m.name}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="mt-4">
        <p className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-400">
          <TrendingUp size={14} /> Tuần này
        </p>
        {data.weekly.length === 0 ? (
          <p className="text-xs text-slate-500">Chưa có ghi nhận nào trong tuần — là người đầu tiên nhé!</p>
        ) : (
          <ul className="space-y-1 text-sm">
            {data.weekly.slice(0, 12).map((e, i) => (
              <li key={i} className="text-slate-300">
                <b className="text-white">{e.name}</b> {e.label}
                <span className="ml-1 text-xs text-slate-600">{new Date(e.at).toLocaleDateString("vi-VN", { weekday: "short" })}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
