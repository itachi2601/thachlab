"use client";

import Image from "next/image";
import { Lock, Sparkles } from "lucide-react";
import {
  GRADE_LABELS,
  ROADMAP_GRADES,
  SPECIALIST_TITLE_GRADES,
} from "@/features/rank/title-grades";
import { LEVEL_LABELS, LEVEL_ORDER, levelRank, type RankTitle, type TitleLevel } from "@/features/rank/types";
import { titleBadgeLockedSrc, titleBadgeSrc } from "@/features/rank/badge-assets";

/** Lộ trình gợi ý: nhóm các danh hiệu chuyên môn đã có sẵn theo lớp, để học sinh biết nên nhắm huy hiệu nào khi học lớp nào. */
export default function TitleGradeRoadmap({ titles }: { titles: RankTitle[] }) {
  const byCode = new Map(titles.map((t) => [t.code, t]));

  return (
    <div className="space-y-6">
      <p className="text-xs text-slate-500">
        Gợi ý huy hiệu chuyên môn nên nhắm tới theo từng lớp — dựa trên chương trình học, không phải danh hiệu mới.
      </p>
      {ROADMAP_GRADES.map((grade) => {
        const codes = Object.entries(SPECIALIST_TITLE_GRADES)
          .filter(([, grades]) => grades.includes(grade))
          .map(([code]) => code);
        const list = codes.map((c) => byCode.get(c)).filter((t): t is RankTitle => !!t);
        if (list.length === 0) return null;
        const owned = list.filter((t) => t.level).length;
        return (
          <section key={grade}>
            <div className="mb-3 flex items-baseline justify-between gap-3">
              <h3 className="font-display text-base font-semibold text-white">{GRADE_LABELS[grade]}</h3>
              <span className="text-xs text-slate-500">
                {owned}/{list.length} đã mở
              </span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {list.map((t) => {
                const unlocked = !!t.level;
                const wearLevel = (t.level ?? null) as TitleLevel | null;
                const badgeSrc = unlocked ? titleBadgeSrc(t.code, wearLevel) : titleBadgeLockedSrc(t.code);
                return (
                  <article
                    key={t.code}
                    className={`flex items-center gap-3 rounded-2xl border p-3 ${
                      unlocked ? "border-amber-400/30 bg-amber-400/5" : "border-white/10 bg-white/[0.02]"
                    }`}
                  >
                    {badgeSrc ? (
                      <Image
                        src={badgeSrc}
                        alt=""
                        width={40}
                        height={40}
                        className={`h-10 w-10 shrink-0 ${unlocked ? "" : "opacity-40 grayscale"}`}
                      />
                    ) : (
                      <span
                        className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${
                          unlocked ? "bg-amber-400/20 text-amber-200" : "bg-white/5 text-slate-500"
                        }`}
                      >
                        {unlocked ? <Sparkles size={16} /> : <Lock size={14} />}
                      </span>
                    )}
                    <div className="min-w-0 flex-1">
                      <p className={`truncate text-sm font-semibold ${unlocked ? "text-white" : "text-slate-300"}`}>{t.name}</p>
                      <p className="text-[12px] text-slate-500">
                        {unlocked ? LEVEL_LABELS[LEVEL_ORDER[Math.max(0, levelRank(t.level) - 1)]] : "Chưa mở"}
                      </p>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        );
      })}
    </div>
  );
}
