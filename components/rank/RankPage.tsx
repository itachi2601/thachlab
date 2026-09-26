"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { CalendarCheck, ChevronRight, Flag, History, Medal, Route, Target, Trophy } from "lucide-react";
import EmptyState from "@/components/ui/EmptyState";
import { useToast } from "@/components/ui/Toast";
import RankBadge from "@/components/rank/RankBadge";
import TierName from "@/components/rank/TierName";
import TitleCollection from "@/components/rank/TitleCollection";
import TierLadder from "@/components/rank/TierLadder";
import {
  LEDGER_KIND_LABELS,
  LEVEL_LABELS,
  formatRp,
  tierLabel,
  tierMeta,
  titleDisplay,
  type RankLedgerEntry,
  type RankSeasonSummary,
  type RankStatus,
  type RankTitle,
  type TitleLevel,
} from "@/features/rank/types";
import {
  fetchLedgerOf,
  fetchMyRankStatus,
  fetchMyTitles,
  fetchSeasonsOf,
  setDisplayTitle,
} from "@/services/rank";

const TIER_SORT_KEY = "thachlab-rank-tier-sort";

function Section({ icon: Icon, title, children, aside }: { icon: typeof Trophy; title: string; children: React.ReactNode; aside?: React.ReactNode }) {
  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-6">
      <div className="mb-4 flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/5 text-slate-300">
          <Icon size={16} />
        </span>
        <h2 className="font-display text-lg font-semibold text-white">{title}</h2>
        {aside && <span className="ml-auto text-xs text-slate-500">{aside}</span>}
      </div>
      {children}
    </section>
  );
}

function Condition({ done, children }: { done: boolean; children: React.ReactNode }) {
  return (
    <li className="flex items-start gap-2 text-sm">
      <span
        className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[11px] font-bold ${
          done ? "bg-emerald-500/20 text-emerald-300" : "bg-white/5 text-slate-500"
        }`}
      >
        {done ? "✓" : "•"}
      </span>
      <span className={done ? "text-slate-400 line-through decoration-slate-600" : "text-slate-200"}>{children}</span>
    </li>
  );
}

export default function RankPage({ studentId, studentName }: { studentId: string; studentName: string }) {
  const toast = useToast();
  const reduceMotion = useReducedMotion();
  const [status, setStatus] = useState<RankStatus | null | undefined>(undefined);
  const [titles, setTitles] = useState<RankTitle[]>([]);
  const [ledger, setLedger] = useState<RankLedgerEntry[]>([]);
  const [seasons, setSeasons] = useState<RankSeasonSummary[]>([]);
  const [celebrate, setCelebrate] = useState<string | null>(null);

  const load = useCallback(() => {
    fetchMyRankStatus()
      .then((s) => {
        setStatus(s);
        // Hiệu ứng lên hạng nhẹ: so với bậc lần trước xem trang này (lưu trên máy em).
        try {
          const key = `${TIER_SORT_KEY}:${s?.season?.id ?? 0}`;
          const prev = Number(window.localStorage.getItem(key) ?? "0");
          const cur = s?.tier?.sort ?? 0;
          if (prev > 0 && cur > prev) setCelebrate(tierLabel(s?.tier?.code, s?.tier?.division, s?.tier?.paragon));
          if (cur > 0) window.localStorage.setItem(key, String(cur));
        } catch {
          /* localStorage không sẵn — bỏ qua */
        }
      })
      .catch(() => setStatus(null));
    fetchMyTitles().then(setTitles).catch(() => setTitles([]));
    fetchLedgerOf(studentId, null, 60).then(setLedger).catch(() => setLedger([]));
    fetchSeasonsOf(studentId).then(setSeasons).catch(() => setSeasons([]));
  }, [studentId]);

  useEffect(load, [load]);

  async function wear(code: string | null, level: TitleLevel | null) {
    try {
      await setDisplayTitle(code, level);
      toast("success", code ? "Đã đeo danh hiệu" : "Đã bỏ danh hiệu");
      fetchMyRankStatus().then(setStatus).catch(() => undefined);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa đổi được danh hiệu");
    }
  }

  const paragon = !!status?.tier?.paragon;
  const meta = tierMeta(status?.tier?.code, paragon);
  const bar = useMemo(() => {
    const t = status?.tier;
    if (!t || !status) return 0;
    if (t.div_max === null) return 100;
    const span = t.div_max - t.div_min + 1;
    return Math.max(4, Math.min(100, Math.round(((status.rp - t.div_min) / Math.max(1, span)) * 100)));
  }, [status]);

  if (status === undefined) {
    return <p className="text-sm text-slate-400">Đang tải xếp hạng…</p>;
  }

  const ledgerBySeason = status?.season ? ledger.filter((l) => l.season_id === status.season!.id) : ledger;

  return (
    <div className="space-y-6">
      <AnimatePresence>
        {celebrate && (
          <motion.div
            className="fixed inset-x-0 top-20 z-50 mx-auto w-fit rounded-2xl border px-5 py-3 text-center shadow-2xl"
            style={{ borderColor: `${meta.color}88`, background: "rgba(11,16,32,0.96)" }}
            initial={{ opacity: 0, y: reduceMotion ? 0 : -12, scale: reduceMotion ? 1 : 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reduceMotion ? 0 : 0.35, ease: "easeOut" }}
            onClick={() => setCelebrate(null)}
            role="status"
          >
            <p className="text-xs font-bold uppercase tracking-widest" style={{ color: meta.light }}>
              Lên hạng!
            </p>
            <p className="font-display text-lg font-bold text-white">{celebrate}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Huy hiệu + RP + tiến trình */}
      <section
        className="relative overflow-hidden rounded-3xl border p-5 sm:p-7"
        style={{ borderColor: `${meta.color}55`, background: `radial-gradient(120% 120% at 0% 0%, ${meta.color}33 0%, rgba(11,16,32,0.6) 55%)` }}
      >
        <div className="flex flex-col gap-5 sm:flex-row sm:items-center">
          <RankBadge code={status?.tier?.code} division={status?.tier?.division} paragon={paragon} size={96} className="mx-auto sm:mx-0" />
          <div className="min-w-0 flex-1 text-center sm:text-left">
            <p className="text-xs font-bold uppercase tracking-widest text-slate-400">{studentName}</p>
            {status?.season ? (
              <>
                <h1 className="mt-1">
                  <TierName code={status.tier?.code} division={status.tier?.division} paragon={paragon} size="lg" className="sm:[&>span]:text-left [&>span]:text-center" />
                </h1>
                <p className="mt-1 text-sm text-slate-300">
                  {status.display_title ? titleDisplay(status.display_title.name, status.display_title.level) : "Chưa đeo danh hiệu — chọn ở bộ sưu tập bên dưới"}
                </p>
                <p className="mt-3 font-display text-2xl font-bold text-white">
                  {formatRp(status.rp)} <span className="text-base font-semibold text-slate-400">RP</span>
                </p>
                <div className="mt-2 h-2 overflow-hidden rounded-full bg-white/10">
                  <div className="h-full rounded-full transition-[width] motion-reduce:transition-none" style={{ width: `${bar}%`, background: `linear-gradient(90deg, ${meta.color}, ${meta.light})` }} />
                </div>
                <p className="mt-1 text-xs text-slate-500">
                  {paragon
                    ? "Danh vị Vô Song — trên cả Chí Tôn, chỉ dành cho người đã sưu tập trọn bộ danh hiệu"
                    : status.tier?.div_max !== null && status.tier
                      ? `Phân bậc hiện tại: ${formatRp(status.tier.div_min)}–${formatRp(status.tier.div_max)} RP`
                      : "Bậc cao nhất — không còn phân bậc"}
                  {" · "}Mùa {status.season.name} ({new Date(status.season.starts_on).toLocaleDateString("vi-VN")} – {new Date(status.season.ends_on).toLocaleDateString("vi-VN")})
                </p>
              </>
            ) : (
              <>
                <h1 className="font-display text-2xl font-bold text-white">Chưa mở mùa xếp hạng</h1>
                <p className="mt-1 text-sm text-slate-400">
                  RP sẽ bắt đầu tính khi giáo viên mở mùa cho lớp em. Danh hiệu đã sưu tập vẫn giữ nguyên.
                </p>
              </>
            )}
          </div>
        </div>
      </section>

      <Section icon={Route} title="Lộ trình các bậc" aside={<span className="hidden sm:inline">Chạm huy hiệu để xem điều kiện</span>}>
        <TierLadder status={status} />
      </Section>

      {status?.season && (
        <div className="grid gap-4 sm:grid-cols-2">
          <Section icon={Flag} title="Điều kiện lên hạng">
            {status.next ? (
              <ul className="space-y-2">
                <Condition done={status.next.rp_needed === 0}>
                  Đạt {formatRp(status.next.min_rp)} RP để chạm <b>{status.next.name}</b>
                  {status.next.rp_needed > 0 && ` (còn ${formatRp(status.next.rp_needed)} RP)`}
                </Condition>
                {status.next.gate && status.next.gate.required_title_count > 0 && (
                  <Condition done={status.next.gate.titles_have >= status.next.gate.required_title_count}>
                    {status.next.gate.required_title_count} danh hiệu chuyên môn mức{" "}
                    {LEVEL_LABELS[status.next.gate.required_title_level ?? "thuc_tinh"]} (đang có {status.next.gate.titles_have})
                  </Condition>
                )}
                {status.next.gate?.challenge_required && (
                  <Condition done={status.next.gate.challenge_best_pct !== null && status.next.gate.challenge_best_pct >= status.next.gate.challenge_pass_pct}>
                    {status.next.gate.challenge_exam_id ? (
                      <>
                        Thử thách: <b>{status.next.gate.challenge_title}</b> — đạt từ {status.next.gate.challenge_pass_pct}%
                        {status.next.gate.challenge_best_pct !== null ? ` (tốt nhất: ${status.next.gate.challenge_best_pct}%)` : " (chưa làm)"}
                        {" · "}
                        <Link href={`/kiem-tra/lam/?id=${status.next.gate.challenge_exam_id}`} className="text-cyan-300 hover:underline">
                          Làm thử thách
                        </Link>
                      </>
                    ) : (
                      <>Thử thách lên hạng — chờ giáo viên giao đề</>
                    )}
                  </Condition>
                )}
                {status.next.gate?.passed && <Condition done>Đã vượt điều kiện lên {status.next.name}</Condition>}
              </ul>
            ) : (
              <p className="text-sm text-slate-300">
                {paragon
                  ? "Em đã đạt danh vị Vô Song — không còn điều kiện nào phía trước. Giữ trọn bộ danh hiệu tới hết mùa để danh vị được ghi vào thành tích mùa."
                  : "Em đang ở bậc cao nhất của mùa này. Giữ vững phong độ!"}
              </p>
            )}
          </Section>

          <Section icon={CalendarCheck} title="Mục tiêu tuần" aside={status.weekly ? `+${status.weekly.rp} RP` : undefined}>
            {status.weekly && (
              <>
                <p className="text-sm text-slate-300">
                  Hoàn thành <b className="text-white">{status.weekly.target}</b> bài tính RP đạt từ{" "}
                  <b className="text-white">{String(status.weekly.min_score).replace(".", ",")}</b> điểm trong tuần (Thứ Hai – Chủ Nhật).
                </p>
                <div className="mt-3 flex items-center gap-2">
                  {Array.from({ length: status.weekly.target }).map((_, i) => (
                    <span
                      key={i}
                      className={`h-3 flex-1 rounded-full ${i < status.weekly!.done ? "bg-emerald-400" : "bg-white/10"}`}
                    />
                  ))}
                </div>
                <p className="mt-2 text-xs text-slate-500">
                  {status.weekly.achieved
                    ? "Tuần này đã đạt — RP đã cộng."
                    : `${status.weekly.done}/${status.weekly.target} bài · tuần từ ${new Date(status.weekly.week_start).toLocaleDateString("vi-VN")}`}
                </p>
              </>
            )}
          </Section>
        </div>
      )}

      <Section icon={Medal} title="Bộ sưu tập danh hiệu" aside={`${status?.titles_count ?? 0} đã mở`}>
        {titles.length === 0 ? (
          <EmptyState title="Chưa có dữ liệu danh hiệu" description="Danh hiệu tính từ các bài kiểm tra em đã làm." />
        ) : (
          <TitleCollection
            titles={titles}
            displayCode={status?.display_title?.code ?? null}
            displayLevel={status?.display_title?.level ?? null}
            canWear
            onWear={wear}
          />
        )}
      </Section>

      <div className="grid gap-4 sm:grid-cols-2">
        <Section icon={History} title="Lịch sử nhận RP">
          {ledgerBySeason.length === 0 ? (
            <p className="text-sm text-slate-500">Chưa có RP nào — làm một bài luyện tập được tính RP để bắt đầu.</p>
          ) : (
            <ul className="divide-y divide-white/5">
              {ledgerBySeason.slice(0, 30).map((l) => (
                <li key={l.id} className="flex items-start gap-3 py-2 text-sm">
                  <span className={`w-14 shrink-0 text-right font-semibold ${l.amount >= 0 ? "text-emerald-300" : "text-red-300"}`}>
                    {l.amount >= 0 ? "+" : ""}
                    {l.amount}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-slate-200">{l.reason || LEDGER_KIND_LABELS[l.source_kind]}</span>
                    <span className="text-xs text-slate-500">
                      {LEDGER_KIND_LABELS[l.source_kind]}
                      {l.actor_name && ` · ${l.actor_name}`} · {new Date(l.created_at).toLocaleDateString("vi-VN")}
                    </span>
                  </span>
                </li>
              ))}
            </ul>
          )}
        </Section>

        <Section icon={Target} title="Thành tích theo mùa">
          {seasons.length === 0 ? (
            <p className="text-sm text-slate-500">Chưa tham gia mùa nào.</p>
          ) : (
            <ul className="space-y-2">
              {seasons.map((s) => (
                <li key={s.season_id} className="flex items-center gap-3 rounded-xl border border-white/10 p-3">
                  <RankBadge code={s.tier_code} division={s.division} paragon={s.paragon} size={36} />
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-semibold text-white">
                      {s.name} {s.status === "active" && <span className="text-xs font-normal text-emerald-300">· đang diễn ra</span>}
                    </span>
                    <span className="text-xs text-slate-500">
                      {tierLabel(s.tier_code, s.division, s.paragon)} · {formatRp(s.rp)} RP
                      {s.status === "closed" && ` · ${s.titles_count} danh hiệu`}
                    </span>
                  </span>
                  <ChevronRight size={16} className="text-slate-600" />
                </li>
              ))}
            </ul>
          )}
        </Section>
      </div>
    </div>
  );
}
