"use client";
import Link from "next/link";
import { Card, vn } from "@/components/tap-luyen/ui";
import type { Measurement } from "@/lib/tap-luyen/store";
import { GOAL_LABEL, type Sex } from "@/lib/suc-khoe/dinh-duong";
import { FAT_LABEL, FRAME_LABEL, SHAPE_LABEL, analyzeBuild, currentWeeklySets, exNames } from "@/lib/suc-khoe/build";

const Chip = ({ children }: { children: React.ReactNode }) => (
  <span className="rounded-full bg-primary-soft px-2.5 py-1 text-xs font-bold text-primary">{children}</span>
);

/** Thẻ "Kiểu build" trên trang Số đo: phân loại + gợi ý tập + gợi ý ăn từ số đo mới nhất. */
export default function KieuBuild({ latest, sex, onSex, onAddMeasure }: { latest: Measurement; sex: Sex; onSex: (s: Sex) => void; onAddMeasure: () => void }) {
  const b = analyzeBuild(latest, sex);
  if (!b) return null;
  const needMore = b.missing.filter((x) => x.key === "neck_cm" || x.key === "wrist_cm" || x.key === "hip_cm" || x.key === "waist_cm");

  return (
    <>
      <Card>
        <div className="flex items-start gap-2">
          <div className="min-w-0 flex-1">
            <p className="font-bold text-ink">Kiểu build của bạn</p>
            <p className="text-xs text-muted">Ước tính từ số đo mới nhất, sai số vài %.</p>
          </div>
          <div className="flex shrink-0 overflow-hidden rounded-xl border border-line" role="group" aria-label="Giới tính để tính">
            {(["nam", "nu"] as const).map((s) => (
              <button key={s} type="button" aria-pressed={sex === s} onClick={() => onSex(s)} className={`min-h-11 px-3 text-sm font-semibold ${sex === s ? "bg-primary text-white" : "text-muted"}`}>
                {s === "nam" ? "Nam" : "Nữ"}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-2 flex flex-wrap gap-1.5">
          {b.frame && <Chip>{FRAME_LABEL[b.frame.size]}</Chip>}
          {b.band && <Chip>{FAT_LABEL[b.band]}</Chip>}
          {b.shape && <Chip>{SHAPE_LABEL[b.shape]}</Chip>}
        </div>

        <dl className="mt-3 grid grid-cols-3 gap-2 text-center">
          <div className="rounded-xl bg-surface-2 py-2">
            <dt className="text-xs text-muted">BMI</dt>
            <dd className="text-lg font-bold tabular-nums text-ink">{b.bmi != null ? vn(b.bmi) : "—"}</dd>
          </div>
          <div className="rounded-xl bg-surface-2 py-2">
            <dt className="text-xs text-muted">% mỡ</dt>
            <dd className="text-lg font-bold tabular-nums text-ink">{b.bf != null ? `${vn(b.bf, 0)}%` : "—"}</dd>
          </div>
          <div className="rounded-xl bg-surface-2 py-2">
            <dt className="text-xs text-muted">Cao/cổ tay</dt>
            <dd className="text-lg font-bold tabular-nums text-ink">{b.frame ? vn(b.frame.ratio) : "—"}</dd>
          </div>
        </dl>

        <p className="mt-3 text-sm text-ink">{b.expect}</p>

        {needMore.length > 0 && (
          <div className="mt-3 rounded-xl border border-warn/50 p-3 text-sm">
            <p className="font-semibold text-ink">Đo thêm để chính xác hơn:</p>
            <ul className="mt-1 space-y-0.5 text-muted">
              {needMore.map((x) => (
                <li key={x.key}>• <b className="text-ink">{x.label}</b> — {x.why}</li>
              ))}
            </ul>
            <button type="button" onClick={onAddMeasure} className="mt-2 min-h-11 rounded-xl bg-primary px-4 text-sm font-bold text-white">Ghi số đo</button>
          </div>
        )}
      </Card>

      <Card>
        <p className="font-bold text-ink">Gợi ý tập cho kiểu này</p>
        {b.priorities.length === 0 ? (
          <p className="mt-2 text-sm text-muted">Số đo hiện cân đối — giữ nguyên chương trình A/B/C và tăng tạ dần theo từng buổi.</p>
        ) : (
          <ul className="mt-2 divide-y divide-line">
            {b.priorities.map((p) => {
              const now = currentWeeklySets(p.group);
              return (
                <li key={p.group} className="py-2.5">
                  <p className="text-sm font-semibold text-ink">
                    {p.group}
                    {p.extraSets > 0 ? (
                      <span className="ml-1 font-bold tabular-nums text-primary">
                        {now} → {now + p.extraSets} hiệp/tuần
                      </span>
                    ) : (
                      <span className="ml-1 text-muted">giữ {now} hiệp/tuần</span>
                    )}
                  </p>
                  <p className="text-xs text-muted">{p.why}</p>
                  <p className="mt-0.5 text-xs text-ink">Bài gợi ý: {exNames(p.ex).join(" · ")}</p>
                </li>
              );
            })}
          </ul>
        )}
        {b.tips.filter((t) => t.startsWith("Mỗi nhóm")).map((t) => (
          <p key={t} className="mt-2 text-xs text-muted">{t}</p>
        ))}
      </Card>

      <Card>
        <p className="font-bold text-ink">Gợi ý ăn cho kiểu này</p>
        <p className="mt-1 text-sm text-ink">
          Hướng: <b>{GOAL_LABEL[b.goal]}</b>
          <span className="block text-xs text-muted">{b.goalWhy}.</span>
        </p>
        <ul className="mt-2 space-y-1 text-sm text-ink">
          {b.tips.filter((t) => !t.startsWith("Mỗi nhóm")).map((t) => (
            <li key={t}>• {t}</li>
          ))}
        </ul>
        <Link href="/suc-khoe/dinh-duong" className="mt-3 inline-flex min-h-11 items-center rounded-xl bg-primary px-4 text-sm font-bold text-white">
          Mở Dinh dưỡng để tính kcal →
        </Link>
      </Card>
    </>
  );
}
