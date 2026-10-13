"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import {
  fetchMyChapterMasteryPct,
  MASTERY_ICON,
  MASTERY_LABEL,
  type ChapterLessonMastery,
} from "@/services/mastery";

interface ChapterMasteryRadarProps {
  studentId: string;
  onLoaded?: (hasData: boolean) => void;
  /** Giáo viên xem hồ sơ em: dữ liệu đã tính sẵn (RPC chỉ đọc theo người đang đăng nhập). Có thì không gọi RPC. */
  preloaded?: { current: ChapterLessonMastery[]; prev: ChapterLessonMastery[] | null };
}

function truncateTitle(title: string, maxLen = 14): string {
  if (title.length <= maxLen) return title;
  return title.slice(0, maxLen - 1) + "…";
}

export default function ChapterMasteryRadar({
  studentId,
  onLoaded,
  preloaded,
}: ChapterMasteryRadarProps) {
  const [loading, setLoading] = useState(true);
  const [currentData, setCurrentData] = useState<ChapterLessonMastery[] | null>(null);
  const [prevData, setPrevData] = useState<ChapterLessonMastery[] | null>(null);
  // Giữ callback mới nhất trong ref để effect không nạp lại RPC mỗi lần cha render.
  const onLoadedRef = useRef(onLoaded);
  useEffect(() => {
    onLoadedRef.current = onLoaded;
  });

  useEffect(() => {
    let active = true;

    if (preloaded) {
      void Promise.resolve().then(() => {
        if (!active) return;
        const hasData = preloaded.current.some((item) => item.pct !== null);
        setCurrentData(hasData ? preloaded.current : null);
        setPrevData(hasData ? preloaded.prev : null);
        setLoading(false);
        onLoadedRef.current?.(hasData);
      });
      return () => {
        active = false;
      };
    }

    const prevMonthDate = new Date(Date.now() - 30 * 86400e3);
    Promise.all([
      fetchMyChapterMasteryPct().catch(() => null),
      fetchMyChapterMasteryPct(prevMonthDate).catch(() => null),
    ])
      .then(([cur, prev]) => {
        if (!active) return;
        if (!cur || cur.length === 0) {
          setCurrentData(null);
          setPrevData(null);
          setLoading(false);
          onLoadedRef.current?.(false);
          return;
        }

        const withData = cur.filter((item) => item.pct !== null);
        if (withData.length === 0) {
          setCurrentData(null);
          setPrevData(null);
          setLoading(false);
          onLoadedRef.current?.(false);
          return;
        }

        setCurrentData(cur);
        setPrevData(prev ?? null);
        setLoading(false);
        onLoadedRef.current?.(true);
      })
      .catch(() => {
        if (!active) return;
        setCurrentData(null);
        setPrevData(null);
        setLoading(false);
        onLoadedRef.current?.(false);
      });

    return () => {
      active = false;
    };
  }, [studentId, preloaded]);

  const prevMap = useMemo(() => {
    const map = new Map<number, ChapterLessonMastery>();
    if (prevData) {
      for (const item of prevData) {
        map.set(item.lessonId, item);
      }
    }
    return map;
  }, [prevData]);

  if (loading) {
    return (
      <div
        className="h-[280px] rounded-2xl border border-line bg-panel p-5"
        aria-busy="true"
        aria-label="Đang tải năng lực chương…"
      />
    );
  }

  if (!currentData) return null;

  const lessonsWithData = currentData.filter((item) => item.pct !== null);
  if (lessonsWithData.length === 0) return null;

  const chapterTitle = currentData[0]?.chapterTitle || "Chương đang học";
  const useRadar = lessonsWithData.length >= 3;

  // Radar: Tối đa 8 trục, nếu >8 bài có dữ liệu thì lấy 8 bài gần nhất theo sortOrder.
  const radarLessons = useRadar
    ? lessonsWithData.length > 8
      ? lessonsWithData.slice(-8)
      : lessonsWithData
    : [];

  const prevLessonsWithDataCount = prevData
    ? prevData.filter((i) => i.pct !== null).length
    : 0;
  const hasPrevRadar = useRadar && prevLessonsWithDataCount >= 3;

  // Nút Ôn bài yếu nhất: bài có pct thấp nhất trong các bài weak/practicing.
  const weakLessons = currentData.filter(
    (item) => item.pct !== null && (item.level === "weak" || item.level === "practicing")
  );
  const weakestLesson =
    weakLessons.length > 0
      ? [...weakLessons].sort((a, b) => {
          const pctA = a.pct ?? 0;
          const pctB = b.pct ?? 0;
          if (pctA !== pctB) return pctA - pctB;
          return a.sortOrder - b.sortOrder;
        })[0]
      : null;

  // Radar geometry
  const cx = 160;
  const cy = 160;
  const R = 80;
  const R_label = 98;
  const N = radarLessons.length;

  const curCoords = radarLessons.map((lesson, i) => {
    const angle = (i * 2 * Math.PI) / N - Math.PI / 2;
    const pct = Math.max(0, Math.min(100, lesson.pct ?? 0));
    const r = (pct / 100) * R;
    return {
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    };
  });
  const curPointsString = curCoords.map((pt) => `${pt.x},${pt.y}`).join(" ");

  const prevCoords = hasPrevRadar
    ? radarLessons.map((lesson, i) => {
        const angle = (i * 2 * Math.PI) / N - Math.PI / 2;
        const prevItem = prevMap.get(lesson.lessonId);
        const prevPct =
          prevItem && prevItem.pct !== null
            ? Math.max(0, Math.min(100, prevItem.pct))
            : 0;
        const r = (prevPct / 100) * R;
        return {
          x: cx + r * Math.cos(angle),
          y: cy + r * Math.sin(angle),
        };
      })
    : [];
  const prevPointsString = prevCoords.map((pt) => `${pt.x},${pt.y}`).join(" ");

  return (
    <section className="rounded-2xl border border-line bg-panel p-5">
      <h2 className="font-display font-semibold text-ink">
        Năng lực chương: {chapterTitle}
      </h2>
      <p className="mt-0.5 text-[13px] text-muted">
        So với chính em 30 ngày trước và mục tiêu 80%
      </p>

      {useRadar ? (
        <div className="mt-4">
          <svg
            viewBox="0 0 320 320"
            className="mx-auto block w-full max-w-[360px]"
            role="img"
            aria-label={`Sơ đồ năng lực chương ${chapterTitle}`}
          >
            {/* Lớp 1: Lưới 4 vòng 25/50/75/100 */}
            {[0.25, 0.5, 0.75, 1.0].map((ringPct) => (
              <circle
                key={ringPct}
                cx={cx}
                cy={cy}
                r={R * ringPct}
                fill="none"
                stroke="var(--color-line-strong)"
                strokeWidth="1"
                strokeOpacity="0.4"
              />
            ))}

            {/* Trục toả từ tâm */}
            {radarLessons.map((_, i) => {
              const angle = (i * 2 * Math.PI) / N - Math.PI / 2;
              const x2 = cx + R * Math.cos(angle);
              const y2 = cy + R * Math.sin(angle);
              return (
                <line
                  key={i}
                  x1={cx}
                  y1={cy}
                  x2={x2}
                  y2={y2}
                  stroke="var(--color-line-strong)"
                  strokeWidth="1"
                  strokeOpacity="0.4"
                />
              );
            })}

            {/* Nhãn trục (tên bài rút gọn <= 14 ký tự) */}
            {radarLessons.map((lesson, i) => {
              const angle = (i * 2 * Math.PI) / N - Math.PI / 2;
              const lx = cx + R_label * Math.cos(angle);
              const ly = cy + R_label * Math.sin(angle);

              const cos = Math.cos(angle);
              const sin = Math.sin(angle);
              const textAnchor =
                cos > 0.25 ? "start" : cos < -0.25 ? "end" : "middle";
              const dominantBaseline =
                sin < -0.6 ? "auto" : sin > 0.6 ? "hanging" : "central";

              return (
                <text
                  key={lesson.lessonId}
                  x={lx}
                  y={ly}
                  textAnchor={textAnchor}
                  dominantBaseline={dominantBaseline}
                  fontSize="11"
                  fill="var(--color-muted)"
                >
                  <title>{lesson.lessonTitle}</title>
                  {truncateTitle(lesson.lessonTitle, 14)}
                </text>
              );
            })}

            {/* Lớp 2: Vòng mục tiêu 80% */}
            <circle
              cx={cx}
              cy={cy}
              r={R * 0.8}
              fill="none"
              stroke="var(--color-ok)"
              strokeDasharray="4 4"
              strokeWidth="1.5"
              strokeOpacity="0.6"
            />

            {/* Lớp 3: Chính em tháng trước (nếu >= 3 bài có dữ liệu) */}
            {hasPrevRadar && (
              <polygon
                points={prevPointsString}
                fill="none"
                stroke="var(--color-muted)"
                strokeWidth="1.5"
                strokeDasharray="3 3"
              />
            )}

            {/* Lớp 4: Hiện tại */}
            <polygon
              points={curPointsString}
              fill="var(--color-primary)"
              fillOpacity="0.18"
              stroke="var(--color-primary)"
              strokeWidth="2"
            />
            {curCoords.map((pt, i) => {
              const item = radarLessons[i];
              const dotColor =
                item.level === "weak"
                  ? "var(--color-danger)"
                  : item.level === "practicing"
                    ? "var(--color-warn)"
                    : "var(--color-primary)";
              return (
                <circle
                  key={item.lessonId}
                  cx={pt.x}
                  cy={pt.y}
                  r={3}
                  fill={dotColor}
                >
                  <title>{`${item.lessonTitle}: ${item.pct}%`}</title>
                </circle>
              );
            })}
          </svg>

          {/* Chú thích (legend) */}
          <div className="mt-3 flex flex-col gap-1.5 text-xs text-muted">
            <div className="flex items-center gap-2">
              <svg width="24" height="10" className="shrink-0" aria-hidden="true">
                <line
                  x1="0"
                  y1="5"
                  x2="24"
                  y2="5"
                  stroke="var(--color-primary)"
                  strokeWidth="2"
                />
                <circle cx="12" cy="5" r="3" fill="var(--color-primary)" />
              </svg>
              <span>Hiện tại</span>
            </div>
            <div className="flex items-center gap-2">
              <svg width="24" height="10" className="shrink-0" aria-hidden="true">
                <line
                  x1="0"
                  y1="5"
                  x2="24"
                  y2="5"
                  stroke="var(--color-ok)"
                  strokeWidth="1.5"
                  strokeDasharray="3 3"
                />
              </svg>
              <span>Mục tiêu: Nắm vững (80%)</span>
            </div>
            {hasPrevRadar && (
              <div className="flex items-center gap-2">
                <svg width="24" height="10" className="shrink-0" aria-hidden="true">
                  <line
                    x1="0"
                    y1="5"
                    x2="24"
                    y2="5"
                    stroke="var(--color-muted)"
                    strokeWidth="1.5"
                    strokeDasharray="3 3"
                  />
                </svg>
                <span>Chính em 30 ngày trước</span>
              </div>
            )}
          </div>
        </div>
      ) : (
        /* 1–2 bài có dữ liệu: thanh ngang */
        <div className="mt-4 space-y-3">
          {lessonsWithData.map((item) => {
            const barColor =
              item.level === "weak"
                ? "var(--color-danger)"
                : item.level === "practicing"
                  ? "var(--color-warn)"
                  : "var(--color-primary)";
            const pct = Math.max(0, Math.min(100, item.pct ?? 0));
            return (
              <div key={item.lessonId} className="space-y-1">
                <div className="flex items-baseline justify-between gap-2 text-sm">
                  <span className="truncate font-medium text-ink">
                    {item.lessonTitle}
                  </span>
                  <span className="shrink-0 text-muted">
                    <span className="font-semibold text-ink">{pct}%</span> ·{" "}
                    {MASTERY_LABEL[item.level]}
                  </span>
                </div>
                <div className="relative h-2.5 w-full overflow-hidden rounded-full bg-surface-2">
                  <div
                    className="h-full rounded-full"
                    style={{ width: `${pct}%`, backgroundColor: barColor }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Bảng số */}
      <div className="mt-5 border-t border-line pt-3">
        <ul className="space-y-2">
          {currentData.map((item) => {
            const icon = MASTERY_ICON[item.level];
            const prevItem = prevMap.get(item.lessonId);
            let deltaStr = "";
            if (item.pct !== null && prevItem && prevItem.pct !== null) {
              const diff = item.pct - prevItem.pct;
              if (diff > 0) deltaStr = `tăng ${diff} điểm %`;
              else if (diff < 0) deltaStr = `giảm ${Math.abs(diff)} điểm %`;
              else deltaStr = "giữ nguyên";
            }

            return (
              <li key={item.lessonId} className="text-sm leading-relaxed text-ink">
                <span className="mr-1.5" aria-hidden="true">
                  {icon}
                </span>
                <span className="font-medium">{item.lessonTitle}</span>
                <span className="text-muted"> — </span>
                {item.pct !== null ? (
                  <>
                    <span className="font-semibold text-ink">{item.pct}%</span>
                    <span className="text-muted">
                      {" "}
                      · {MASTERY_LABEL[item.level]}
                    </span>
                    {deltaStr && (
                      <span className="text-muted"> · {deltaStr}</span>
                    )}
                  </>
                ) : (
                  <span className="text-muted">chưa làm</span>
                )}
              </li>
            );
          })}
        </ul>
      </div>

      {/* Nút chính duy nhất hoặc dòng chúc mừng */}
      <div className="mt-5">
        {weakestLesson ? (
          <Link
            href={`/lop-hoc/bai/?id=${weakestLesson.lessonId}#secondary-stage-ly_thuyet`}
            className="inline-flex min-h-11 w-full items-center justify-center rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-primary-dark sm:w-auto"
          >
            Ôn bài yếu nhất
          </Link>
        ) : (
          <p className="text-sm font-medium text-ok">
            Chương này em đã nắm vững, học tiếp bài mới.
          </p>
        )}
      </div>
    </section>
  );
}
