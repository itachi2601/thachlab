"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { Check, Lock } from "lucide-react";
import RankBadge from "@/components/rank/RankBadge";
import TierName from "@/components/rank/TierName";
import {
  LEVEL_LABELS,
  TIER_ORDER,
  divisionLabel,
  formatRp,
  tierMeta,
  type RankStatus,
  type TierCode,
} from "@/features/rank/types";
import { fetchTierLadder, type TierLadderStep } from "@/services/rank";

/**
 * Lộ trình các bậc: em xem trước toàn bộ huy hiệu (kể cả phân bậc III/II/I) và điều kiện lên từng bậc.
 * Ngưỡng RP + điều kiện lấy từ rank_tiers của mùa đang mở (giáo viên chỉnh được), không hardcode.
 * Bấm một huy hiệu trên dải để xem chi tiết bậc đó; mặc định mở bậc hiện tại của em.
 */

interface Division {
  division: 1 | 2 | 3;
  min: number;
  max: number;
}

/** Cùng công thức với SQL rank_tier_info: chia đều [min_rp, next_min-1] thành 3 đoạn III → I. */
function divisionsOf(step: TierLadderStep): Division[] | null {
  if (!step.has_divisions || step.next_min === null) return null;
  const w = Math.floor((step.next_min - step.min_rp) / 3);
  if (w <= 0) return null;
  return [
    { division: 3, min: step.min_rp, max: step.min_rp + w - 1 },
    { division: 2, min: step.min_rp + w, max: step.min_rp + 2 * w - 1 },
    { division: 1, min: step.min_rp + 2 * w, max: step.next_min - 1 },
  ];
}

function challengeRequired(step: TierLadderStep): boolean {
  return step.challenge_exam_id !== null || step.code === "cao_thu" || step.code === "thach_dau";
}

type CondState = "done" | "todo" | "neutral";

function Cond({ state, children }: { state: CondState; children: React.ReactNode }) {
  return (
    <li className="flex items-start gap-2 text-sm">
      <span
        className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[11px] font-bold ${
          state === "done" ? "bg-emerald-500/20 text-emerald-300" : "bg-white/5 text-slate-500"
        }`}
      >
        {state === "done" ? <Check size={12} /> : "•"}
      </span>
      <span className={state === "done" ? "text-slate-400" : "text-slate-200"}>{children}</span>
    </li>
  );
}

export default function TierLadder({ status }: { status: RankStatus | null }) {
  const reduceMotion = useReducedMotion();
  const seasonId = status?.season?.id ?? null;
  const currentSort = status?.tier?.sort ?? 0;
  const [steps, setSteps] = useState<TierLadderStep[] | null | undefined>(seasonId ? undefined : null);
  const [selected, setSelected] = useState<TierCode>((status?.tier?.code as TierCode | undefined) ?? "tan_binh");

  useEffect(() => {
    if (!seasonId) return;
    let alive = true;
    fetchTierLadder(seasonId)
      .then((s) => alive && setSteps(s))
      .catch(() => alive && setSteps(null));
    return () => {
      alive = false;
    };
  }, [seasonId]);

  // Không có mùa / chưa tải được ngưỡng → vẫn cho xem đủ 7 huy hiệu, chỉ thiếu số RP.
  const list: TierLadderStep[] = useMemo(() => {
    if (steps && steps.length > 0) return steps;
    return TIER_ORDER.map((code, i) => ({
      season_id: 0,
      code,
      sort: i + 1,
      name: tierMeta(code).name,
      min_rp: 0,
      has_divisions: code !== "cao_thu" && code !== "thach_dau",
      required_title_count: 0,
      required_title_level: null,
      challenge_exam_id: null,
      challenge_pass_score: null,
      next_min: null,
      challenge_title: null,
    }));
  }, [steps]);
  const hasNumbers = !!steps && steps.length > 0;

  const step = list.find((s) => s.code === selected) ?? list[0];
  const meta = tierMeta(step.code);
  const divisions = hasNumbers ? divisionsOf(step) : null;
  const isCurrent = status?.season ? step.sort === currentSort : false;
  const reached = status?.season ? step.sort < currentSort : false;
  const isNext = !!status?.next && status.next.code === step.code;
  const gate = isNext ? status?.next?.gate ?? null : null;
  const rp = status?.rp ?? 0;
  const fillPct = list.length > 1 ? ((Math.max(1, currentSort) - 1) / (list.length - 1)) * 100 : 0;

  const rpState: CondState = reached || isCurrent ? "done" : isNext ? (status!.next!.rp_needed === 0 ? "done" : "todo") : "neutral";
  const titleState: CondState = reached || isCurrent ? "done" : gate ? (gate.titles_have >= gate.required_title_count ? "done" : "todo") : "neutral";
  const chalState: CondState =
    reached || isCurrent
      ? "done"
      : gate
        ? gate.passed || (gate.challenge_best_pct !== null && gate.challenge_best_pct >= gate.challenge_pass_pct)
          ? "done"
          : "todo"
        : "neutral";
  const passPct = Math.round((step.challenge_pass_score ?? 8) * 10);

  return (
    <div>
      {/* Dải 7 huy hiệu — cuộn ngang trên máy nhỏ */}
      <div className="relative -mx-1 overflow-x-auto px-1 pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        <div className="relative flex items-start justify-between gap-0.5 sm:gap-2">
          <div className="pointer-events-none absolute left-5 right-5 top-5 h-0.5 rounded-full bg-white/10 sm:top-7" aria-hidden>
            {status?.season && (
              <div
                className="h-full rounded-full"
                style={{ width: `${fillPct}%`, background: `linear-gradient(90deg, ${tierMeta("tan_binh").color}, ${tierMeta(status.tier?.code).light})` }}
              />
            )}
          </div>
          {list.map((s) => {
            const m = tierMeta(s.code);
            const cur = status?.season ? s.sort === currentSort : false;
            const done = status?.season ? s.sort < currentSort : false;
            const locked = status?.season ? s.sort > currentSort : false;
            const active = s.code === step.code;
            return (
              <button
                key={s.code}
                type="button"
                onClick={() => setSelected(s.code)}
                aria-pressed={active}
                aria-label={`${m.en} · ${m.name}${cur ? " (bậc hiện tại)" : ""}`}
                className="group relative flex w-10 flex-col items-center gap-1 outline-none sm:w-20"
              >
                <span
                  className={`relative flex h-10 w-10 items-center justify-center rounded-full transition sm:h-14 sm:w-14 ${
                    active ? "ring-2 ring-offset-2 ring-offset-[#0b1020]" : "group-hover:scale-105 group-focus-visible:ring-2"
                  } ${locked && !active ? "opacity-55 saturate-50" : ""}`}
                  style={{ background: active ? `${m.color}33` : "rgba(11,16,32,0.9)", ["--tw-ring-color" as string]: m.light }}
                >
                  <RankBadge code={s.code} division={s.has_divisions ? (cur ? status?.tier?.division : done ? 1 : 3) : null} size={40} className="hidden sm:block" />
                  <RankBadge code={s.code} division={s.has_divisions ? (cur ? status?.tier?.division : done ? 1 : 3) : null} size={30} className="sm:hidden" />
                  {done && (
                    <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500 text-white ring-2 ring-[#0b1020]">
                      <Check size={10} strokeWidth={3} />
                    </span>
                  )}
                  {locked && (
                    <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-slate-700 text-slate-300 ring-2 ring-[#0b1020]">
                      <Lock size={9} />
                    </span>
                  )}
                </span>
                <span
                  className={`hidden w-full truncate text-center text-[10px] font-bold uppercase tracking-wide sm:block ${active ? "" : "text-slate-500"}`}
                  style={{ fontFamily: "var(--font-cinzel), Cinzel, serif", color: active ? m.light : undefined }}
                >
                  {m.en}
                </span>
                {cur && <span className="h-1 w-1 rounded-full sm:-mt-0.5" style={{ background: m.light }} aria-hidden />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Chi tiết bậc đang chọn */}
      <AnimatePresence mode="wait" initial={false}>
        <motion.div
          key={step.code}
          initial={{ opacity: 0, y: reduceMotion ? 0 : 6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          transition={{ duration: reduceMotion ? 0 : 0.2 }}
          className="mt-4 rounded-2xl border p-4 sm:p-5"
          style={{ borderColor: `${meta.color}55`, background: `linear-gradient(135deg, ${meta.color}22 0%, rgba(11,16,32,0) 65%)` }}
        >
          <div className="flex items-center gap-3 sm:gap-4">
            <RankBadge code={step.code} division={step.has_divisions ? (isCurrent ? status?.tier?.division : 1) : null} size={72} className="shrink-0" />
            <div className="min-w-0 flex-1">
              <TierName code={step.code} division={isCurrent ? status?.tier?.division : null} size="md" />
              <p className="mt-1.5 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs">
                {isCurrent && (
                  <span className="rounded-full px-2 py-0.5 font-bold uppercase tracking-wider" style={{ background: `${meta.color}44`, color: meta.light }}>
                    Bậc hiện tại của em
                  </span>
                )}
                {reached && <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 font-bold uppercase tracking-wider text-emerald-300">Đã đạt</span>}
                {isNext && status?.next && status.next.rp_needed > 0 && (
                  <span className="rounded-full bg-white/10 px-2 py-0.5 font-semibold text-slate-200">Còn {formatRp(status.next.rp_needed)} RP</span>
                )}
                {hasNumbers && (
                  <span className="text-slate-400">
                    {step.next_min !== null ? `${formatRp(step.min_rp)} – ${formatRp(step.next_min - 1)} RP` : `Từ ${formatRp(step.min_rp)} RP`}
                  </span>
                )}
              </p>
            </div>
          </div>

          {divisions && (
            <div className="mt-4">
              <p className="text-[11px] font-bold uppercase tracking-widest text-slate-500">Phân bậc · III đồng → II bạc → I vàng</p>
              <div className="mt-2 grid grid-cols-3 gap-2">
                {divisions.map((d) => {
                  const here = isCurrent && status?.tier?.division === d.division;
                  const passed = reached || (isCurrent && rp > d.max);
                  return (
                    <div
                      key={d.division}
                      className={`flex items-center gap-2 rounded-xl border p-2 ${here ? "border-white/30 bg-white/10" : "border-white/10 bg-white/[0.03]"}`}
                    >
                      <RankBadge code={step.code} division={d.division} size={34} className="shrink-0" />
                      <span className="min-w-0">
                        <span className="block text-xs font-bold text-white" style={{ fontFamily: "var(--font-cinzel), Cinzel, serif" }}>
                          {meta.en} {divisionLabel(d.division)}
                        </span>
                        <span className={`block truncate text-[11px] ${passed ? "text-emerald-300" : "text-slate-400"}`}>
                          {formatRp(d.min)}–{formatRp(d.max)} RP
                        </span>
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
          {step.has_divisions && !divisions && (
            <p className="mt-3 text-xs text-slate-500">Có 3 phân bậc III · II · I theo RP trong bậc.</p>
          )}
          {!step.has_divisions && <p className="mt-3 text-xs text-slate-500">Bậc này không chia phân bậc — huy hiệu luôn bằng vàng.</p>}

          <div className="mt-4">
            <p className="text-[11px] font-bold uppercase tracking-widest text-slate-500">Điều kiện đạt bậc</p>
            {step.sort === 1 ? (
              <p className="mt-2 text-sm text-slate-300">Bậc khởi đầu — mọi học sinh tham gia mùa đều bắt đầu từ đây.</p>
            ) : !hasNumbers ? (
              <p className="mt-2 text-sm text-slate-400">Ngưỡng RP và điều kiện cụ thể sẽ hiện khi giáo viên mở mùa xếp hạng.</p>
            ) : (
              <ul className="mt-2 space-y-2">
                <Cond state={rpState}>
                  Đạt <b className="text-white">{formatRp(step.min_rp)} RP</b> trong mùa
                </Cond>
                {step.required_title_count > 0 && (
                  <Cond state={titleState}>
                    Có <b className="text-white">{step.required_title_count}</b> danh hiệu chuyên môn mức{" "}
                    <b className="text-white">{LEVEL_LABELS[step.required_title_level ?? "thuc_tinh"]}</b> trở lên
                    {gate ? ` (đang có ${gate.titles_have})` : ""}
                  </Cond>
                )}
                {challengeRequired(step) && (
                  <Cond state={chalState}>
                    {step.challenge_exam_id ? (
                      <>
                        Vượt thử thách <b className="text-white">{step.challenge_title ?? "lên hạng"}</b> — đạt từ {passPct}%
                        {gate && gate.challenge_best_pct !== null ? ` (tốt nhất: ${gate.challenge_best_pct}%)` : ""}
                        {isNext && (
                          <>
                            {" · "}
                            <Link href={`/kiem-tra/lam/?id=${step.challenge_exam_id}`} className="text-cyan-300 hover:underline">
                              Làm thử thách
                            </Link>
                          </>
                        )}
                      </>
                    ) : (
                      <>Vượt thử thách lên hạng — giáo viên sẽ giao đề riêng cho bậc này</>
                    )}
                  </Cond>
                )}
              </ul>
            )}
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
