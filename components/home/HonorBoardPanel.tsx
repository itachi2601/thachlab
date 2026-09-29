"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowUpCircle, Flame, TrendingUp, Trophy } from "lucide-react";
import Avatar from "@/components/ui/Avatar";
import RankAvatarFrame from "@/components/rank/RankAvatarFrame";
import WornTitle from "@/components/rank/WornTitle";
import { divisionLabel, tierMeta, type PublicHonorBoard, type PublicHonorGrade } from "@/features/rank/types";
import { fetchPublicHonor } from "@/services/rank";

/** Mục "Vinh danh tuần" trên trang chủ công khai — chỉ render khi RPC trả về ít nhất một khối có dữ liệu. */
export default function HonorBoardPanel() {
  const [board, setBoard] = useState<PublicHonorBoard | null | undefined>(undefined);
  const [grade, setGrade] = useState<string | null>(null);

  useEffect(() => {
    fetchPublicHonor().then(setBoard).catch(() => setBoard(null));
  }, []);

  const grades = useMemo(
    () => (board?.grades ?? []).filter((g) => g.top.length > 0 || g.tier_ups.length > 0 || g.streak),
    [board],
  );
  // Mặc định mở khối lớn nhất có bục (thường là khối đông và sôi nổi nhất).
  const active = grades.find((g) => g.grade === grade) ?? [...grades].reverse().find((g) => g.top.length > 0) ?? grades[0];

  if (!board || grades.length === 0 || !active) return null;

  return (
    <section id="vinh-danh" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div className="max-w-2xl">
            <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">
              Vinh danh tuần · {weekLabel(board.week_start, active.use_prev)}
            </p>
            <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Các bạn học chăm nhất tuần này
            </h2>
            <p className="mt-4 text-base leading-relaxed text-muted">
              Xếp theo RP kiếm được trong tuần, làm mới sáng Thứ Hai — ai chăm tuần này đều lên bục được.
            </p>
          </div>
          <div className="flex gap-2" role="tablist" aria-label="Chọn khối">
            {grades.map((g) => {
              const on = g.grade === active.grade;
              return (
                <button
                  key={g.grade}
                  role="tab"
                  aria-selected={on}
                  onClick={() => setGrade(g.grade)}
                  className={`rounded-full border px-4 py-1.5 text-sm font-medium transition ${
                    on ? "border-cyan-300 bg-cyan-300 text-slate-900" : "border-line text-muted hover:border-white/30 hover:text-ink"
                  }`}
                >
                  Khối {g.grade}
                </button>
              );
            })}
          </div>
        </div>

        <Podium key={active.grade} g={active} />

        <p className="mt-8 text-xs text-slate-500">
          Tên hiện rút gọn theo lựa chọn của từng bạn. Học sinh đổi cách hiện (đầy đủ, rút gọn hoặc ẩn) trong{" "}
          <Link href="/tai-khoan/" className="text-cyan-300 underline-offset-4 hover:underline">
            trang tài khoản
          </Link>
          .
        </p>
      </div>
    </section>
  );
}

function Podium({ g }: { g: PublicHonorGrade }) {
  // Desktop: hạng 1 đứng giữa (2 · 1 · 3); mobile: danh sách 1 · 2 · 3 theo thứ tự tự nhiên.
  const ORDER = ["sm:order-2", "sm:order-1", "sm:order-3"];
  const notes = [
    g.improved_acc
      ? {
          key: "improved",
          Icon: TrendingUp,
          label: "Tiến bộ nhất",
          who: g.improved_acc.name,
          detail: `Tỉ lệ đúng +${String(g.improved_acc.gain).replace(".", ",")} điểm % so với 2 tuần trước (đạt ${Math.round(g.improved_acc.acc)}%)`,
        }
      : g.improved && {
          key: "improved",
          Icon: TrendingUp,
          label: "Tiến bộ nhất",
          who: g.improved.name,
          detail: `+${g.improved.delta} RP so với tuần trước`,
        },
    g.tier_ups.length > 0 && {
      key: "tier",
      Icon: ArrowUpCircle,
      label: "Lên bậc tuần này",
      who: g.tier_ups.map((t) => t.name).join(", "),
      detail: g.tier_ups.map((t) => `${tierMeta(t.tier_code).name} ${divisionLabel(t.division)}`.trim()).filter((v, i, a) => a.indexOf(v) === i).join(" · "),
    },
    g.streak && {
      key: "streak",
      Icon: Flame,
      label: "Chuỗi ngày dài nhất",
      who: g.streak.name,
      detail: `${g.streak.days} ngày học liên tiếp`,
    },
  ].filter(Boolean) as { key: string; Icon: typeof Flame; label: string; who: string; detail: string }[];

  return (
    <>
      {g.top.length === 0 ? (
        <p className="mt-10 rounded-2xl border border-dashed border-line p-6 text-sm text-muted">
          Khối {g.grade} chưa có bạn nào nhận RP tuần này. Bài luyện tập đầu tiên sẽ đưa em lên bục.
        </p>
      ) : (
        <ul className="mt-10 grid gap-3 sm:grid-cols-3 sm:items-end">
          {g.top.map((m, i) => {
            const first = m.pos === 1;
            const meta = tierMeta(m.tier_code, m.paragon);
            return (
              <li
                key={`${m.name}-${i}`}
                className={`flex items-center gap-4 rounded-2xl border bg-panel p-4 sm:flex-col sm:text-center ${ORDER[i] ?? "sm:order-4"} ${
                  first ? "border-cyan-300/50 sm:pb-6 sm:pt-7" : "border-line"
                }`}
              >
                <div className="flex shrink-0 flex-col items-center gap-2">
                  <span className={`font-mono text-[11px] uppercase tracking-widest ${first ? "text-cyan-300" : "text-slate-500"}`}>
                    Hạng {m.pos}
                  </span>
                  <RankAvatarFrame tier={{ code: m.tier_code, division: m.division, paragon: m.paragon }} size={first ? 72 : 56}>
                    <Avatar url={m.avatar} name={m.name} size={first ? 72 : 56} />
                  </RankAvatarFrame>
                </div>
                <div className="min-w-0 flex-1 sm:mt-2">
                  <p className="truncate text-base font-semibold text-ink">{m.name}</p>
                  {m.title && <WornTitle title={m.title} className="mt-0.5 sm:justify-center" />}
                  <p className="mt-1 text-xs text-slate-400">
                    {meta.name} {m.paragon ? "" : divisionLabel(m.division)}
                  </p>
                  <p className="mt-1.5 font-mono text-sm text-cyan-300">+{m.rp_week} RP tuần</p>
                </div>
              </li>
            );
          })}
        </ul>
      )}
      {(g.top_more ?? 0) > 0 && (
        <p className="mt-3 text-xs text-slate-400">
          và {g.top_more} bạn khác cùng hạng với các bạn trên — bục chỉ hiện được 5 bạn, xếp theo tên.
        </p>
      )}

      {notes.length > 0 && (
        <div className="mt-6 rounded-2xl border border-line bg-panel/60 px-4 py-2">
          <p className="flex items-center gap-2 py-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            <Trophy size={14} className="text-amber-300" /> Ghi nhận tuần
          </p>
          <ul className="divide-y divide-line">
            {notes.map(({ key, Icon, label, who, detail }) => (
              <li key={key} className="flex flex-wrap items-center gap-x-3 gap-y-1 py-2.5 text-sm">
                <Icon size={16} className="shrink-0 text-cyan-300" />
                <span className="w-full text-slate-400 sm:w-40">{label}</span>
                <span className="font-medium text-ink">{who}</span>
                <span className="text-slate-400">{detail}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}

function weekLabel(weekStart: string, usePrev: boolean): string {
  const start = new Date(`${weekStart}T00:00:00+07:00`);
  if (usePrev) start.setDate(start.getDate() - 7);
  const end = new Date(start);
  end.setDate(end.getDate() + 6);
  const f = (d: Date) => {
    const p = new Intl.DateTimeFormat("en-GB", { day: "2-digit", month: "2-digit", timeZone: "Asia/Ho_Chi_Minh" }).formatToParts(d);
    const get = (t: string) => p.find((x) => x.type === t)?.value ?? "";
    return `${get("day")}/${get("month")}`;
  };
  return `${usePrev ? "tuần trước " : ""}${f(start)} đến ${f(end)}`;
}
