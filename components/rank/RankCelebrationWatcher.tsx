"use client";

/**
 * Theo dõi học sinh vừa LÊN RANK hoặc VỪA ĐẠT DANH HIỆU / lên mức danh hiệu → bật pop-up chúc mừng.
 * Không cần migration: so ảnh chụp lần trước (localStorage, theo từng tài khoản) với rank_my_status + rank_my_titles.
 *  - Lần đầu trên máy: chỉ ghi mốc, không chúc mừng (tránh ăn mừng cả bộ sưu tập cũ).
 *  - Đổi mùa / rank tụt: ghi lại mốc im lặng.
 *  - Không bật trong lúc làm bài (/kiem-tra/lam) hay khu quản trị (QUY-TAC L3, L6) — kiểm lại khi đổi trang / quay lại tab.
 *  - Mốc chỉ cập nhật khi em đóng pop-up, nên tải lại trang giữa chừng không mất lời chúc.
 */

import dynamic from "next/dynamic";
import { usePathname } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import { useAuth } from "@/components/auth/auth-context";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import { isStudentPreview } from "@/features/rank/preview";
import { TIER_ORDER, levelRank, tierMeta, titleDisplay, type RankStatus, type RankTitle, type TierCode, type TitleLevel } from "@/features/rank/types";
import type { CelebrationEvent } from "@/components/rank/RankCelebrationModal";
import { fetchMyRankStatus, fetchMyTitles } from "@/services/rank";

const RankCelebrationModal = dynamic(() => import("@/components/rank/RankCelebrationModal"), { ssr: false });

const QUIET_PREFIXES = ["/quan-tri", "/kiem-tra/lam", "/phu-huynh", "/tro-giang/ghi"];

interface Snapshot {
  season: number | null;
  tier: number; // điểm thứ hạng gộp (bậc + phân bậc + Thách Đấu)
  titles: Record<string, number>; // code → levelRank
}

const key = (uid: string) => `thachlab-rank-seen:${uid}`;

function readSnap(uid: string): Snapshot | null {
  try {
    const raw = localStorage.getItem(key(uid));
    return raw ? (JSON.parse(raw) as Snapshot) : null;
  } catch {
    return null;
  }
}

function writeSnap(uid: string, s: Snapshot) {
  try {
    localStorage.setItem(key(uid), JSON.stringify(s));
  } catch {
    /* không lưu được thì thôi — tệ nhất là chúc mừng lại một lần */
  }
}

function tierScore(status: RankStatus | null): number {
  const t = status?.tier;
  if (!t) return -1;
  if (t.paragon) return 1000;
  const idx = TIER_ORDER.indexOf(t.code);
  return idx * 10 + (t.division ? 4 - t.division : 0);
}

function snapOf(status: RankStatus | null, titles: RankTitle[]): Snapshot {
  const map: Record<string, number> = {};
  for (const t of titles) if (levelRank(t.level) > 0) map[t.code] = levelRank(t.level);
  return { season: status?.season?.id ?? null, tier: tierScore(status), titles: map };
}

export default function RankCelebrationWatcher() {
  const { session, profile } = useAuth();
  const pathname = usePathname();
  const [queue, setQueue] = useState<CelebrationEvent[]>([]);
  const pending = useRef<Snapshot | null>(null);
  const busy = useRef(false);
  const uid = session?.user.id ?? null;
  const isStudent = profile?.role === "student";
  const quiet = QUIET_PREFIXES.some((p) => pathname.startsWith(p));

  const check = useCallback(async () => {
    if (!uid || busy.current || pending.current || document.visibilityState === "hidden") return;
    busy.current = true;
    try {
      const [status, titles] = await Promise.all([fetchMyRankStatus(), fetchMyTitles()]);
      const now = snapOf(status, titles);
      const before = readSnap(uid);
      if (!before || before.season !== now.season) {
        writeSnap(uid, now);
        return;
      }
      const events: CelebrationEvent[] = [];
      const t = status?.tier;
      if (t && now.tier > before.tier) {
        const meta = tierMeta(t.code, t.paragon);
        events.push({ kind: "rank", code: t.code as TierCode, division: t.division, paragon: !!t.paragon, name: meta.name, en: meta.en });
      }
      for (const ti of titles) {
        const lv = levelRank(ti.level);
        if (lv > (before.titles[ti.code] ?? 0)) {
          events.push({
            kind: "title",
            code: ti.code,
            level: (ti.level ?? "don") as TitleLevel,
            name: titleDisplay(ti.name, ti.level),
            description: ti.description,
            first: !before.titles[ti.code],
          });
        }
      }
      if (events.length === 0) {
        if (JSON.stringify(now) !== JSON.stringify(before)) writeSnap(uid, now);
        return;
      }
      pending.current = now;
      setQueue(events);
    } catch {
      /* mạng/RPC lỗi → bỏ qua, lần sau kiểm lại */
    } finally {
      busy.current = false;
    }
  }, [uid]);

  useEffect(() => {
    if (!uid || !isStudent || quiet || isStudentPreview()) return;
    void check();
    const onVis = () => void check();
    document.addEventListener("visibilitychange", onVis);
    window.addEventListener("thachlab:rank-check", onVis);
    return () => {
      document.removeEventListener("visibilitychange", onVis);
      window.removeEventListener("thachlab:rank-check", onVis);
    };
  }, [uid, isStudent, quiet, pathname, check]);

  const next = useCallback(() => {
    setQueue((q) => {
      const rest = q.slice(1);
      if (rest.length === 0 && uid && pending.current) {
        writeSnap(uid, pending.current);
        pending.current = null;
      }
      return rest;
    });
  }, [uid]);

  if (quiet || queue.length === 0) return null;
  return (
    <LazyErrorBoundary>
      <RankCelebrationModal key={queue.length} event={queue[0]} remaining={queue.length - 1} onNext={next} />
    </LazyErrorBoundary>
  );
}
