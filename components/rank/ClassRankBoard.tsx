"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowUp, Flame, Sparkles, Trophy, Users } from "lucide-react";
import Avatar from "@/components/ui/Avatar";
import RankBadge from "@/components/rank/RankBadge";
import TierName from "@/components/rank/TierName";
import WornTitle from "@/components/rank/WornTitle";
import type { ClassGoal, ClassRankBoard as Board } from "@/features/rank/types";
import { fetchClassRankBoard } from "@/services/rank";

const MEDAL = [
  { label: "1", color: "#fbbf24", bg: "rgba(251,191,36,.12)", border: "rgba(251,191,36,.45)" },
  { label: "2", color: "#cbd5e1", bg: "rgba(203,213,225,.10)", border: "rgba(203,213,225,.35)" },
  { label: "3", color: "#f59e0b", bg: "rgba(217,119,6,.10)", border: "rgba(217,119,6,.35)" },
];

function daysLeft(endsOn: string): number {
  const end = new Date(`${endsOn}T23:59:59+07:00`).getTime();
  return Math.max(0, Math.ceil((end - Date.now()) / 86_400_000));
}

/**
 * Trang Rank (/lop-hoc/xep-hang, chuyển từ trang chủ HS 7/10/2026): bảng tuần của lớp — top 3 theo RP KIẾM ĐƯỢC TRONG TUẦN (reset Thứ Hai),
 * vị trí của em + 1 bạn ngay trên/dưới, và ghi nhận tuần này. Vị trí của em chỉ so với bạn CÙNG BẬC, không hiện thứ tự tuyệt đối.
 */
export default function ClassRankBoard({ classId }: { classId: number }) {
  const [data, setData] = useState<Board | null | undefined>(undefined);

  useEffect(() => {
    fetchClassRankBoard(classId).then(setData).catch(() => setData(null));
  }, [classId]);

  if (data === undefined || data === null || !data.season) return null;

  const me = data.me;
  const left = daysLeft(data.season.ends_on);
  const weekStart = new Date(data.week_start).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" });

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Trophy size={18} className="text-amber-300" />
          <h2 className="font-display font-bold text-white">Bảng tuần của lớp</h2>
        </div>
        <Link href="/lop-hoc/" className="text-xs text-cyan-300 hover:underline">
          Bậc cả lớp →
        </Link>
      </div>
      <p className="mt-1 text-xs text-slate-500">
        Tính RP kiếm được từ Thứ Hai {weekStart} · chốt Chủ Nhật 23:59 rồi làm lại từ đầu. Ai chăm tuần này đều lên được top.
      </p>

      {/* Mục tiêu chung của lớp — hợp tác: huy hiệu của bất kỳ bạn nào cũng tính */}
      {data.class_goal && data.class_goal.target > 0 && <ClassGoalBar goal={data.class_goal} />}

      {/* Khối 1 — Top tuần */}
      <div className="mt-4">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">Top tuần</p>
        {data.top_week.length === 0 ? (
          <p className="rounded-xl border border-dashed border-white/10 p-3 text-sm text-slate-400">
            Chưa ai nhận RP tuần này. Bài luyện tập đầu tiên em làm sẽ đưa em lên top 1.
          </p>
        ) : (
          <ul className="grid gap-2 sm:grid-cols-3">
            {data.top_week.map((m, i) => {
              const medal = MEDAL[Math.min(m.pos, 3) - 1] ?? MEDAL[2];
              return (
                <li
                  key={`${m.name}-${i}`}
                  className="flex items-center gap-2.5 rounded-xl border p-2.5"
                  style={{ borderColor: m.is_me ? "rgba(34,211,238,.6)" : medal.border, background: medal.bg }}
                >
                  <span
                    className="font-display grid h-7 w-7 shrink-0 place-items-center rounded-full text-sm font-black text-slate-900"
                    style={{ background: medal.color }}
                  >
                    {m.pos}
                  </span>
                  <Avatar url={m.avatar} name={m.name} size={30} />
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-sm font-semibold text-white">
                      {m.name}
                      {m.is_me && <span className="ml-1 text-xs font-normal text-cyan-300">(em)</span>}
                    </span>
                    {m.title && <WornTitle title={m.title} className="block" />}
                    <span className="flex items-center gap-1 text-xs text-slate-400">
                      <RankBadge code={m.tier_code ?? undefined} division={m.division} paragon={m.paragon} size={14} />
                      <b className="text-emerald-300">+{m.rp_week} RP</b> tuần này
                    </span>
                  </span>
                </li>
              );
            })}
          </ul>
        )}
      </div>

      {/* Khối 2 — Vị trí của em */}
      {me && (
        <div className="mt-4 rounded-xl border border-cyan-400/20 bg-cyan-500/5 p-3">
          <p className="text-sm text-white">
            {me.rp_week === 0 ? (
              <>
                Em <b>chưa có RP tuần này</b>. Làm 1 bài luyện tập đạt từ 7,0 là có RP ngay.
              </>
            ) : (
              <>
                Trong nhóm {me.tier_code ? <TierName code={me.tier_code} size="sm" /> : "chưa xếp bậc"}
                {me.tier_size > 1 ? <> ({me.tier_size} bạn)</> : null}, tuần này em có <b className="text-emerald-300">+{me.rp_week} RP</b>
                {me.tied > 0 && <span className="text-slate-400"> · ngang với {me.tied} bạn cùng bậc</span>}
                {me.in_top && <span className="ml-1 text-amber-300">· Em đang trong top 3 lớp!</span>}
                {!me.above && !me.in_top && <span className="ml-1 text-amber-300">· Em đang dẫn đầu bậc!</span>}
              </>
            )}
          </p>
          <div className="mt-2 space-y-1 text-xs text-slate-300">
            {me.above && (
              <p className="flex items-center gap-1.5">
                <ArrowUp size={12} className="text-cyan-300" />
                <Avatar url={me.above.avatar} name={me.above.name} size={16} />
                Còn <b className="text-white">{me.above.rp_week - me.rp_week + 1} RP</b> nữa để vượt {me.above.name} (cùng bậc)
              </p>
            )}
            {me.below && (
              <p className="flex items-center gap-1.5 text-slate-400">
                <Flame size={12} className="text-orange-300" />
                <Avatar url={me.below.avatar} name={me.below.name} size={16} />
                {me.below.name} đang bám sau em {me.rp_week - me.below.rp_week} RP
              </p>
            )}
          </div>
        </div>
      )}

      {/* Khối 4 — Ghi nhận tuần này */}
      <div className="mt-4">
        <p className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-400">
          <Sparkles size={14} /> Ghi nhận tuần này
        </p>
        {data.improved === null && data.weekly.length === 0 ? (
          <p className="text-xs text-slate-500">Chưa có ghi nhận nào trong tuần — là người đầu tiên nhé!</p>
        ) : (
          <ul className="space-y-1 text-sm">
            {data.improved && (
              <li className="flex items-center gap-1.5 text-slate-300">
                <Avatar url={data.improved.avatar} name={data.improved.name} size={18} />
                <span>
                  <b className="text-white">{data.improved.name}</b> tiến bộ nhất tuần
                  <span className="ml-1 text-xs text-emerald-300">+{data.improved.delta} RP so với tuần trước</span>
                </span>
              </li>
            )}
            {data.weekly.slice(0, 6).map((e, i) => (
              <li key={i} className="text-slate-300">
                <b className="text-white">{e.name}</b> {e.label}
                <span className="ml-1 text-xs text-slate-600">{new Date(e.at).toLocaleDateString("vi-VN", { weekday: "short" })}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <p className="mt-3 text-[12px] text-slate-500">
        {data.season.name} còn <b className="text-slate-300">{left} ngày</b>.
      </p>
    </section>
  );
}

function ClassGoalBar({ goal }: { goal: ClassGoal }) {
  const pct = Math.min(100, Math.round((goal.done / Math.max(1, goal.target)) * 100));
  return (
    <div
      className="mt-3 rounded-xl border p-3"
      style={{ borderColor: goal.reached ? "rgba(52,211,153,.45)" : "rgba(255,255,255,.1)", background: goal.reached ? "rgba(52,211,153,.08)" : undefined }}
    >
      <p className="flex items-center gap-1.5 text-sm font-semibold text-white">
        <Users size={15} className={goal.reached ? "text-emerald-300" : "text-cyan-300"} />
        Mục tiêu chung: cả lớp đạt {goal.target} huy hiệu tuần này
        <span className="ml-auto text-xs font-normal text-slate-400">
          {Math.min(goal.done, goal.target)}/{goal.target}
        </span>
      </p>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-white/10">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, background: goal.reached ? "#34d399" : "#22d3ee" }} />
      </div>
      <p className="mt-1.5 text-xs text-slate-400">
        {goal.reached ? (
          <>Cả lớp đã đạt mục tiêu{goal.rp > 0 ? <> — mỗi bạn được <b className="text-emerald-300">+{goal.rp} RP</b></> : null}. Cảm ơn mọi người!</>
        ) : (
          <>
            Huy hiệu của <b className="text-slate-200">bất kỳ bạn nào</b> trong lớp đều tính
            {goal.rp > 0 ? <>; đạt mục tiêu, mỗi bạn nhận <b className="text-emerald-300">+{goal.rp} RP</b></> : null}. Rủ nhau cùng học nhé.
          </>
        )}
        {goal.my_contrib > 0 && <span className="ml-1 text-cyan-300">Em đã góp {goal.my_contrib} huy hiệu.</span>}
      </p>
    </div>
  );
}
