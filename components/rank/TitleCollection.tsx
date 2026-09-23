"use client";

import { useState } from "react";
import { Check, Lock, Sparkles } from "lucide-react";
import Button from "@/components/ui/Button";
import {
  GROUP_LABELS,
  GROUP_ORDER,
  LEVEL_LABELS,
  LEVEL_ORDER,
  isSpecialistProgress,
  levelRank,
  type CollectionProgress,
  type RankTitle,
  type SpecialistProgress,
  type TitleLevel,
} from "@/features/rank/types";

function nextRequirement(t: RankTitle): string {
  if (t.kind === "achievement") return t.description;
  if (t.kind === "collection") {
    const p = t.progress as CollectionProgress | null;
    if (!p) return "Mở khi đã có đủ mọi danh hiệu bộ sưu tập đang khả dụng";
    return `${p.met}/${p.required} danh hiệu đạt ${LEVEL_LABELS[p.level]}`;
  }
  const p = t.progress;
  if (!isSpecialistProgress(p)) return t.description;
  if (!t.active) return "Chưa gắn chủ đề — chờ giáo viên";
  const r = levelRank(t.level);
  if (r === 0) {
    return `Thức Tỉnh: ≥ ${p.min_questions} câu (đã ${p.n}), chạm ≥ ½ chủ đề (${p.covered}/${p.total_topics}), đúng ≥ ${p.awaken_accuracy}% (đang ${p.acc}%)`;
  }
  if (r === 1) {
    return `Làm Chủ: ≥ ${p.min_questions * 2} câu (đã ${p.n}), đủ ${p.total_topics} chủ đề (${p.covered}), đúng ≥ ${p.master_accuracy}% (đang ${p.acc}%)`;
  }
  if (r === 2) {
    return p.legend_exam_id
      ? `Huyền Thoại: đề thử thách ≥ ${p.legend_accuracy}% (tốt nhất: ${p.legend_best === null ? "chưa làm" : `${p.legend_best}%`})`
      : "Huyền Thoại: chờ giáo viên giao đề thử thách";
  }
  return "Đã đạt mức cao nhất";
}

function progressPct(t: RankTitle): number {
  if (t.kind === "collection") {
    const p = t.progress as CollectionProgress | null;
    return p && p.required > 0 ? Math.round((p.met / p.required) * 100) : 0;
  }
  const p = t.progress as SpecialistProgress | null;
  if (!p || !t.active) return 0;
  const r = levelRank(t.level);
  if (r >= 3) return 100;
  const need = r === 0 ? p.min_questions : p.min_questions * 2;
  const acc = r === 0 ? p.awaken_accuracy : p.master_accuracy;
  const qPart = Math.min(1, p.n / Math.max(1, need));
  const aPart = Math.min(1, p.acc / Math.max(1, acc));
  const cPart = p.total_topics > 0 ? Math.min(1, p.covered / (r === 0 ? Math.max(1, Math.ceil(p.total_topics / 2)) : p.total_topics)) : 0;
  return Math.round(((qPart + aPart + cPart) / 3) * 100);
}

export default function TitleCollection({
  titles,
  displayCode,
  displayLevel,
  canWear,
  onWear,
}: {
  titles: RankTitle[];
  displayCode: string | null;
  displayLevel: string | null;
  canWear: boolean;
  onWear?: (code: string | null, level: TitleLevel | null) => void;
}) {
  const [showHidden, setShowHidden] = useState(false);
  const hiddenCount = titles.filter((t) => !t.visible).length;
  const shown = titles.filter((t) => t.visible || showHidden);

  return (
    <div className="space-y-8">
      {GROUP_ORDER.map((g) => {
        const list = shown.filter((t) => t.group === g);
        if (list.length === 0) return null;
        const owned = list.filter((t) => t.level).length;
        return (
          <section key={g}>
            <div className="mb-3 flex items-baseline justify-between gap-3">
              <h3 className="font-display text-base font-semibold text-white">{GROUP_LABELS[g]}</h3>
              <span className="text-xs text-slate-500">
                {owned}/{list.length} đã mở
              </span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {list.map((t) => {
                const unlocked = !!t.level;
                const wearing = displayCode === t.code;
                const pct = progressPct(t);
                const wearLevel = (t.level ?? null) as TitleLevel | null;
                return (
                  <article
                    key={t.code}
                    className={`rounded-2xl border p-4 ${
                      unlocked ? "border-amber-400/30 bg-amber-400/5" : "border-white/10 bg-white/[0.02]"
                    } ${!t.active && t.kind === "specialist" ? "opacity-60" : ""}`}
                  >
                    <div className="flex items-start gap-3">
                      <span
                        className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
                          unlocked ? "bg-amber-400/20 text-amber-200" : "bg-white/5 text-slate-500"
                        }`}
                      >
                        {unlocked ? <Sparkles size={18} /> : <Lock size={16} />}
                      </span>
                      <div className="min-w-0 flex-1">
                        <p className={`font-display font-semibold ${unlocked ? "text-white" : "text-slate-300"}`}>{t.name}</p>
                        <p className="text-xs text-slate-500">{t.description}</p>
                        {t.kind === "specialist" && (
                          <div className="mt-2 flex gap-1.5">
                            {LEVEL_ORDER.map((lv) => {
                              const has = !!t.levels[lv];
                              return (
                                <span
                                  key={lv}
                                  className={`rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                                    has ? "bg-amber-400/25 text-amber-100" : "bg-white/5 text-slate-500"
                                  }`}
                                  title={has ? `Nhận ${new Date(t.levels[lv]!).toLocaleDateString("vi-VN")}` : undefined}
                                >
                                  {has && <Check size={10} className="mr-0.5 inline" />}
                                  {LEVEL_LABELS[lv]}
                                </span>
                              );
                            })}
                          </div>
                        )}
                        <p className="mt-2 text-xs text-slate-400">{nextRequirement(t)}</p>
                        {levelRank(t.level) < 3 && (t.kind !== "achievement") && (
                          <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-white/10">
                            <div className="h-full rounded-full bg-gradient-to-r from-cyan-400 to-blue-500" style={{ width: `${pct}%` }} />
                          </div>
                        )}
                        {canWear && unlocked && (
                          <div className="mt-3">
                            {wearing ? (
                              <Button size="sm" variant="outline" onClick={() => onWear?.(null, null)}>
                                Đang đeo · Bỏ
                              </Button>
                            ) : (
                              <Button size="sm" onClick={() => onWear?.(t.code, wearLevel)}>
                                Đeo danh hiệu
                              </Button>
                            )}
                            {wearing && displayLevel && t.kind === "specialist" && (
                              <span className="ml-2 text-xs text-slate-500">{LEVEL_LABELS[displayLevel as TitleLevel]}</span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        );
      })}
      {hiddenCount > 0 && (
        <button type="button" onClick={() => setShowHidden((v) => !v)} className="text-xs text-slate-500 underline-offset-2 hover:text-slate-300 hover:underline">
          {showHidden ? "Ẩn" : "Hiện"} {hiddenCount} danh hiệu ngoài chương trình lớp em
        </button>
      )}
    </div>
  );
}
