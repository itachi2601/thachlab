"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Flame, Trophy, X } from "lucide-react";
import StreakWeek from "@/components/rank/StreakWeek";
import type { RankStatus } from "@/features/rank/types";
import type { NextStep } from "@/features/learning/next-steps";
import type { StreakDay } from "@/services/rank";

const KEY = "thachlab-welcome-day:";

function todayKey() {
  // Ngày theo giờ VN (UTC+7), cùng nhịp với "ngày" của chuỗi; đổi ngày thì pop-up hiện lại một lần.
  return new Date(Date.now() + 7 * 3600_000).toISOString().slice(0, 10);
}

function seenToday(userId: string) {
  try {
    return window.localStorage.getItem(KEY + userId) === todayKey();
  } catch {
    return false;
  }
}

/**
 * Pop-up "Chào mừng em quay lại" — thay WelcomePanel cho học sinh đã vào lớp (thầy chốt 8/10/2026).
 * Quy tắc để không thành "mù biển quảng cáo": mỗi ngày tối đa MỘT lần (lần mở đầu), chỉ khi hôm nay chưa giữ chuỗi
 * và có việc để làm; tối đa 2 số liệu (chuỗi, RP còn thiếu) + MỘT nút dẫn thẳng vào việc đầu của thẻ "Hôm nay" (N1, N2, L5).
 * Hiện lúc mới vào trang, chưa làm bài nên không vi phạm L3/L6. Giọng nói về việc tiếp theo, không doạ mất chuỗi (L4);
 * chuỗi có đóng băng thì nhắc luôn. Đóng bằng nút ✕ / nền / Esc.
 */
export default function WelcomeBackDialog({
  userId,
  name,
  rank,
  days,
  primary,
  ready,
  onUnlock,
  onQuickPractice,
}: {
  userId: string;
  name?: string | null;
  rank: RankStatus | null | undefined;
  days: StreakDay[] | null;
  primary: NextStep | null;
  /** Dữ liệu việc hôm nay đã tải đủ (tránh hiện rồi đổi nội dung). */
  ready: boolean;
  onUnlock: (needId: number) => void;
  onQuickPractice: (step: NextStep) => void;
}) {
  const [open, setOpen] = useState(false);
  const decided = useRef(false);
  const ctaRef = useRef<HTMLElement | null>(null);

  const daily = rank?.season ? rank.daily : null;

  useEffect(() => {
    if (decided.current || !ready || rank === undefined) return;
    decided.current = true;
    if (!daily || daily.today_done || !primary || seenToday(userId)) return;
    try {
      window.localStorage.setItem(KEY + userId, todayKey());
    } catch {
      /* không lưu được thì chỉ hiện ở phiên này */
    }
    // Hoãn sang tick sau: mở pop-up là phản ứng với dữ liệu tải xong, không setState đồng bộ trong effect.
    const t = window.setTimeout(() => setOpen(true), 0);
    return () => window.clearTimeout(t);
  }, [ready, rank, daily, primary, userId]);

  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && close();
    window.addEventListener("keydown", onKey);
    ctaRef.current?.focus();
    return () => window.removeEventListener("keydown", onKey);
  }, [open, close]);

  if (!open || !daily || !primary) return null;

  const first = name?.trim().split(/\s+/).pop();
  const next = rank?.next;
  const freezeLeft = Math.max(0, (daily.freeze_per_week ?? 0) - (daily.freeze_used_week ?? 0));
  const ctaClass =
    "flex min-h-12 w-full items-center justify-center rounded-xl bg-primary px-4 text-sm font-bold text-white hover:bg-primary-dark";

  return (
    <div className="fixed inset-0 z-[60] flex items-end justify-center sm:items-center" role="dialog" aria-modal="true" aria-label="Chào mừng em quay lại">
      <button type="button" className="absolute inset-0 bg-black/60" aria-label="Đóng" onClick={close} />
      <div className="relative w-full max-w-md rounded-t-3xl border border-white/10 bg-panel p-5 pb-[calc(1.25rem+env(safe-area-inset-bottom,0px))] sm:rounded-3xl">
        <button
          type="button"
          onClick={close}
          aria-label="Đóng"
          className="absolute right-2 top-2 flex h-11 w-11 items-center justify-center rounded-full text-slate-400 hover:bg-white/10 hover:text-white"
        >
          <X size={18} />
        </button>
        <h2 className="pr-10 font-display text-xl font-bold text-white">{first ? `Chào mừng ${first} quay lại` : "Chào mừng em quay lại"}</h2>

        <div className="mt-4 space-y-3">
          <p className="flex items-center gap-2 text-base text-white">
            <Flame size={20} className="shrink-0 text-amber-400" fill={daily.streak > 0 ? "currentColor" : "none"} aria-hidden />
            {daily.streak > 0 ? <>Chuỗi <b>{daily.streak} ngày</b> đang chờ em hôm nay</> : "Hôm nay là ngày bắt đầu chuỗi mới"}
          </p>
          {days && days.length > 0 && <StreakWeek days={days} />}
          {next && (
            <p className="flex items-center gap-2 text-base text-slate-200">
              <Trophy size={18} className="shrink-0 text-amber-300" aria-hidden />
              <span>
                Còn <b className="text-white">{next.rp_needed} RP</b> nữa là lên {next.name}
              </span>
            </p>
          )}
          {daily.streak > 0 && freezeLeft > 0 && (
            <p className="text-[13px] text-sky-300">Tuần này em còn {freezeLeft} lượt đóng băng: lỡ một ngày chuỗi vẫn không gãy.</p>
          )}
        </div>

        <div className="mt-5">
          <p className="mb-2 text-[13px] text-slate-400">Việc đầu tiên hôm nay</p>
          {primary.href && !primary.practice ? (
            <Link href={primary.href} ref={ctaRef as React.Ref<HTMLAnchorElement>} onClick={close} className={ctaClass}>
              {primary.action}: {primary.title}
            </Link>
          ) : (
            <button
              type="button"
              ref={ctaRef as React.Ref<HTMLButtonElement>}
              disabled={Boolean(primary.lockedUntil)}
              onClick={() => {
                close();
                if (primary.practice) onQuickPractice(primary);
                else if (primary.needId !== undefined) onUnlock(primary.needId);
              }}
              className={`${ctaClass} disabled:opacity-60`}
            >
              {primary.action}: {primary.title}
            </button>
          )}
          <button type="button" onClick={close} className="mt-1 flex min-h-11 w-full items-center justify-center text-sm text-slate-400 hover:text-white">
            Để sau
          </button>
        </div>
      </div>
    </div>
  );
}
