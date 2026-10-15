"use client";

import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import Link from "next/link";
import {
  fetchMyChapterMasteryPct,
  fetchMyCourseMasteryPct,
  MASTERY_ICON,
  MASTERY_LABEL,
  fetchLessonMastery,
  type ChapterLessonMastery,
  type TopicMastery,
} from "@/services/mastery";
import QuickPractice, { type QuickPracticeRequest } from "@/components/mastery/QuickPractice";

/** Tối đa 3 YCCĐ yếu nhất của một bài (chỉ Chưa đạt / Cần luyện thêm, đủ ≥4 lượt), thấp nhất lên trước. */
function weakestTopics(topics: TopicMastery[]): TopicMastery[] {
  return topics
    .filter((t) => t.pct !== null && (t.level === "weak" || t.level === "practicing"))
    .sort((a, b) => (a.pct ?? 0) - (b.pct ?? 0) || a.sortOrder - b.sortOrder)
    .slice(0, 3);
}

interface ChapterMasteryRadarProps {
  studentId: string;
  onLoaded?: (hasData: boolean) => void;
  /** Giáo viên xem hồ sơ em: dữ liệu đã tính sẵn (RPC chỉ đọc theo người đang đăng nhập). Có thì không gọi RPC. */
  preloaded?: { current: ChapterLessonMastery[]; prev: ChapterLessonMastery[] | null };
  /** Bản gọn cho trang chủ HS: chỉ sơ đồ + bài yếu nhất + lối vào kết quả chi tiết (bỏ chú thích dài và bảng số). */
  compact?: boolean;
  /** Giáo viên xem hồ sơ em: dữ liệu cả khoá đã tính sẵn (buildCourseRadar) → có bộ chuyển phạm vi, không gọi RPC. */
  courseData?: { current: ChapterLessonMastery[]; prev: ChapterLessonMastery[] | null };
  /** "parent": phụ huynh xem (xưng "con", bỏ nút luyện/ôn — phụ huynh không vào được bài của lớp). */
  viewer?: "student" | "parent";
}

interface RadarViewProps extends ChapterMasteryRadarProps {
  /** "lesson": đỉnh = bài của một chương (mặc định). "chapter": đỉnh = chương (cả khoá; khoá HSG = mảng). */
  unit?: "lesson" | "chapter";
  /** Cho phép mở YCCĐ yếu của bài dù dữ liệu truyền sẵn (chỉ chính em xem, không phải giáo viên). */
  allowDrill?: boolean;
  /** Tiêu đề/ghi chú thay mặc định; ReactNode đặt dưới tiêu đề (bộ chuyển phạm vi). */
  title?: string;
  subtitle?: string;
  headerSlot?: ReactNode;
  /** Chế độ "chapter": chạm một đỉnh/hàng thì chuyển sang xem các bài của chương đó. */
  onPickChapter?: (chapterId: number) => void;
}

function RadarView({
  studentId,
  onLoaded,
  preloaded,
  compact = false,
  unit = "lesson",
  allowDrill = false,
  title,
  subtitle,
  headerSlot,
  onPickChapter,
  viewer = "student",
}: RadarViewProps) {
  const isChapterUnit = unit === "chapter";
  const isParent = viewer === "parent";
  const who = isParent ? "con" : "em";
  const unitWord = isChapterUnit ? "mảng" : "bài";
  const [loading, setLoading] = useState(!preloaded);
  const [currentData, setCurrentData] = useState<ChapterLessonMastery[] | null>(
    preloaded && preloaded.current.some((item) => item.pct !== null) ? preloaded.current : null
  );
  const [prevData, setPrevData] = useState<ChapterLessonMastery[] | null>(
    preloaded && preloaded.current.some((item) => item.pct !== null) ? preloaded.prev : null
  );
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

  // Nút chính + bài mở sẵn: bài có pct thấp nhất trong các bài weak/practicing.
  const weakestLesson = useMemo(() => {
    const weak = (currentData ?? []).filter(
      (item) => item.pct !== null && (item.level === "weak" || item.level === "practicing")
    );
    if (weak.length === 0) return null;
    return [...weak].sort((a, b) => (a.pct ?? 0) - (b.pct ?? 0) || a.sortOrder - b.sortOrder)[0];
  }, [currentData]);

  // Tầng 2 (YCCĐ của một bài) chỉ ở bản đầy đủ của chính em: RPC đọc theo người đang đăng nhập,
  // và trang chủ (compact) không được thêm round-trip.
  const drillDown = !compact && !isChapterUnit && (!preloaded || allowDrill);
  const [userOpen, setUserOpen] = useState<number | null | undefined>(undefined);
  // Bài đang được nhấn mạnh trên sơ đồ (chạm đỉnh hoặc chạm hàng); mặc định là bài yếu nhất.
  const [focusId, setFocusId] = useState<number | null>(null);
  const openId = userOpen !== undefined ? userOpen : drillDown ? (weakestLesson?.lessonId ?? null) : null;
  const [topicsByLesson, setTopicsByLesson] = useState<Record<number, TopicMastery[] | "error">>({});
  const [practice, setPractice] = useState<QuickPracticeRequest | null>(null);
  // Luôn nạp bài yếu nhất (cho nút chính) và bài đang mở; mỗi bài một lần, kết quả giữ trong cache.
  const wantIds = drillDown
    ? [weakestLesson?.lessonId, openId].filter((id): id is number => typeof id === "number" && topicsByLesson[id] === undefined)
    : [];
  const wantKey = wantIds.join(",");
  useEffect(() => {
    if (!wantKey) return;
    for (const id of wantKey.split(",").map(Number)) {
      fetchLessonMastery(id)
        .then((m) => setTopicsByLesson((prev) => ({ ...prev, [id]: m.topics })))
        .catch(() => setTopicsByLesson((prev) => ({ ...prev, [id]: "error" })));
    }
  }, [wantKey]);

  const weakestTopicsList = weakestLesson ? topicsByLesson[weakestLesson.lessonId] : undefined;
  const weakestTopic = drillDown && Array.isArray(weakestTopicsList) ? (weakestTopics(weakestTopicsList)[0] ?? null) : null;

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

  const chapterTitle = title ?? (currentData[0]?.chapterTitle || "Chương đang học");
  // Đỉnh theo chương: giữ cả mảng chưa làm (vẽ ở tâm) để em thấy chỗ trống; đỉnh theo bài chỉ lấy bài đã có dữ liệu.
  const axisItems = isChapterUnit ? currentData : lessonsWithData;
  const useRadar = axisItems.length >= 3;

  // Radar: Tối đa 8 trục, nếu >8 thì lấy 8 mục cuối theo sortOrder.
  const radarLessons = useRadar ? (axisItems.length > 8 ? axisItems.slice(-8) : axisItems) : [];

  const prevLessonsWithDataCount = prevData
    ? prevData.filter((i) => i.pct !== null).length
    : 0;
  const hasPrevRadar = useRadar && prevLessonsWithDataCount >= 3;

  // Radar geometry
  const cx = 180;
  const cy = 170;
  const R = 100;
  const R_label = 126;
  const N = radarLessons.length;
  const activeFocusId = focusId ?? weakestLesson?.lessonId ?? null;
  // Mã bài ngắn B1…Bn (theo "Bài N" trong tên, không có thì theo thứ tự) — tên đầy đủ nằm ở bảng bên dưới.
  const codeOf = (lessonId: number): string => {
    const idx = currentData.findIndex((l) => l.lessonId === lessonId);
    if (isChapterUnit) return `C${idx + 1}`;
    const title = idx >= 0 ? currentData[idx].lessonTitle : "";
    const m = title.match(/^Bài\s*(\d+)/i);
    return m ? `B${m[1]}` : `B${idx + 1}`;
  };
  const levelColor = (level: ChapterLessonMastery["level"]) =>
    level === "mastered"
      ? "var(--color-ok)"
      : level === "practicing"
        ? "var(--color-warn)"
        : level === "weak"
          ? "var(--color-danger)"
          : "var(--color-line-strong)";
  const ringPoints = (k: number) =>
    radarLessons
      .map((_, i) => {
        const angle = (i * 2 * Math.PI) / N - Math.PI / 2;
        return `${cx + R * k * Math.cos(angle)},${cy + R * k * Math.sin(angle)}`;
      })
      .join(" ");

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

  if (compact && useRadar) {
    const lowest = [...radarLessons].sort((a, b) => (a.pct ?? 0) - (b.pct ?? 0))[0];
    const cx2 = 70;
    const cy2 = 70;
    const R2 = 46;
    const at = (i: number, k: number) => {
      const angle = (i * 2 * Math.PI) / N - Math.PI / 2;
      return [cx2 + R2 * k * Math.cos(angle), cy2 + R2 * k * Math.sin(angle)] as const;
    };
    const poly = (k: (i: number) => number) => radarLessons.map((_, i) => at(i, k(i)).join(",")).join(" ");
    return (
      <section className="rounded-2xl border border-line bg-panel p-4">
        <div className="flex items-baseline justify-between gap-3">
          <h2 className="font-display font-bold text-ink">Bản đồ năng lực</h2>
          <Link href="/lop-hoc/ket-qua" className="-my-3 inline-flex min-h-11 shrink-0 items-center text-[13px] text-primary hover:underline">
            Xem kết quả ›
          </Link>
        </div>
        <p className="text-[13px] text-muted">{chapterTitle}</p>
        <div className="mt-2 flex items-center gap-3">
          <svg viewBox="-18 -4 176 148" className="h-36 w-[176px] shrink-0" role="img" aria-label={isChapterUnit ? `Sơ đồ năng lực theo ${unitWord}: ${chapterTitle}` : `Sơ đồ năng lực chương ${chapterTitle}`}>
            {[0.33, 0.66, 1].map((k) => (
              <polygon key={k} points={poly(() => k)} fill="none" stroke="var(--color-line-strong)" strokeWidth="1" strokeOpacity="0.5" />
            ))}
            <polygon points={poly((i) => Math.max(0.03, (radarLessons[i].pct ?? 0) / 100))} fill="var(--color-primary)" fillOpacity="0.2" stroke="var(--color-primary)" strokeWidth="2" />
            {radarLessons.map((l, i) => {
              const [x, y] = at(i, Math.max(0.03, (l.pct ?? 0) / 100));
              const isLow = l.lessonId === lowest.lessonId;
              if (!isLow) return <circle key={l.lessonId} cx={x} cy={y} r={3} fill="var(--color-primary)" />;
              return (
                <g key={l.lessonId}>
                  <circle cx={x} cy={y} r={11} fill="var(--color-panel)" stroke="var(--color-danger)" strokeWidth="2" />
                  <text x={x} y={y} textAnchor="middle" dominantBaseline="central" fontSize="11" fontWeight="700" fill="var(--color-ink)">
                    {l.pct ?? "–"}
                  </text>
                </g>
              );
            })}
            {radarLessons.map((l, i) => {
              const [x, y] = at(i, 1.3);
              return (
                <text key={l.lessonId} x={x} y={y} textAnchor="middle" dominantBaseline="central" fontSize="11" fill="var(--color-muted)">
                  {codeOf(l.lessonId)}
                </text>
              );
            })}
          </svg>
          <div className="min-w-0 text-sm">
            {weakestLesson ? (
              <>
                <p className="text-[13px] font-semibold text-danger">Yếu nhất</p>
                <p className="font-bold text-ink">{weakestLesson.lessonTitle}</p>
                <p className="text-[13px] text-muted">{weakestLesson.pct}% thành thạo</p>
                <Link
                  href={isChapterUnit ? "/lop-hoc/ket-qua" : `/lop-hoc/bai/?id=${weakestLesson.lessonId}#secondary-stage-ly_thuyet`}
                  className="mt-1 inline-flex min-h-11 items-center font-bold text-primary hover:underline"
                >
                  {isChapterUnit ? "Xem các bài ›" : "Ôn 5 phút ›"}
                </Link>
              </>
            ) : (
              <p className="font-medium text-ok">
                {isChapterUnit ? `Các mảng ${who} đã làm đều vững, học tiếp mảng còn trống.` : `Chương này ${who} đã nắm vững, học tiếp bài mới.`}
              </p>
            )}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="rounded-2xl border border-line bg-panel p-5">
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="font-display font-semibold text-ink">
          {compact ? "Bản đồ năng lực" : isChapterUnit ? `Năng lực ${chapterTitle}` : `Năng lực chương: ${chapterTitle}`}
        </h2>
        {compact && (
          <Link href="/lop-hoc/ket-qua" className="-my-3 inline-flex min-h-11 shrink-0 items-center text-[13px] text-primary hover:underline">
            Xem kết quả ›
          </Link>
        )}
      </div>
      <p className="mt-0.5 text-[13px] text-muted">
        {compact ? chapterTitle : (subtitle ?? `So với chính ${who} 30 ngày trước và mục tiêu 80%`)}
      </p>
      {!compact && headerSlot}

      {useRadar ? (
        <div className="mt-4">
          <svg
            viewBox="0 0 360 340"
            className="mx-auto block w-full max-w-[360px]"
            role="img"
            aria-label={isChapterUnit ? `Sơ đồ năng lực theo ${unitWord}: ${chapterTitle}` : `Sơ đồ năng lực chương ${chapterTitle}`}
          >
            {/* Lớp 1: Lưới 4 vòng 25/50/75/100, số chia thang nằm giữa trục 1 và trục 2 */}
            {[0.25, 0.5, 0.75, 1.0].map((ringPct) => {
              const a = Math.PI / N - Math.PI / 2;
              return (
                <g key={ringPct}>
                  <polygon
                    points={ringPoints(ringPct)}
                    fill="none"
                    stroke="var(--color-line-strong)"
                    strokeWidth="1"
                    strokeOpacity="0.45"
                  />
                  <text
                    x={cx + R * ringPct * Math.cos(a) + 3}
                    y={cy + R * ringPct * Math.sin(a)}
                    fontSize="11"
                    fill="var(--color-muted)"
                    stroke="var(--color-panel)"
                    strokeWidth="3"
                    paintOrder="stroke"
                  >
                    {Math.round(ringPct * 100)}
                  </text>
                </g>
              );
            })}

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
                  fontSize="13"
                  fontWeight="600"
                  fill="var(--color-ink)"
                >
                  <title>{lesson.lessonTitle}</title>
                  {codeOf(lesson.lessonId)}
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
              const isFocus = item.lessonId === activeFocusId;
              return (
                <g
                  key={item.lessonId}
                  role="button"
                  tabIndex={0}
                  aria-label={item.pct === null ? `${item.lessonTitle}: chưa làm` : `${item.lessonTitle}: ${item.pct}%, ${MASTERY_LABEL[item.level]}`}
                  onClick={() => setFocusId(item.lessonId)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      setFocusId(item.lessonId);
                    }
                  }}
                  className="cursor-pointer outline-none"
                >
                  <title>{item.pct === null ? `${item.lessonTitle}: chưa làm` : `${item.lessonTitle}: ${item.pct}%`}</title>
                  {/* Vùng chạm rộng ~44px, không vẽ */}
                  <circle cx={pt.x} cy={pt.y} r={22} fill="transparent" />
                  <circle
                    cx={pt.x}
                    cy={pt.y}
                    r={isFocus ? 18 : 15}
                    fill="var(--color-panel)"
                    stroke={levelColor(item.level)}
                    strokeWidth={isFocus ? 3 : 2}
                  />
                  <text
                    x={pt.x}
                    y={pt.y}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fontSize="12"
                    fontWeight="700"
                    fill="var(--color-ink)"
                  >
                    {item.pct ?? "–"}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Chú thích (legend) */}
          {!compact && <div className="mt-3 flex flex-col gap-1.5 text-xs text-muted">
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
            <p>
                {isChapterUnit
                  ? "Số trong vòng tròn là % thành thạo của cả mảng (dấu – là chưa làm). Chạm một vòng để xem mảng đó trong bảng."
                  : "Số trong vòng tròn là % thành thạo của bài. Chạm một vòng để xem bài đó trong bảng."}
              </p>
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
                <span>Chính {who} 30 ngày trước</span>
              </div>
            )}
          </div>}
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

      {/* Bảng số; bản đầy đủ của chính em: bấm một bài để xem YCCĐ yếu nhất của bài đó */}
      {!compact && <div className="mt-5 border-t border-line pt-3">
        <ul className="space-y-2">
          {currentData.map((item) => {
            const icon = MASTERY_ICON[item.level];
            const prevItem = prevMap.get(item.lessonId);
            let deltaStr = "";
            if (item.pct !== null && prevItem && prevItem.pct !== null) {
              const diff = item.pct - prevItem.pct;
              if (diff > 0) deltaStr = `▲ tăng ${diff} điểm %`;
              else if (diff < 0) deltaStr = `▼ giảm ${Math.abs(diff)} điểm %`;
              else deltaStr = "= giữ nguyên";
            }
            const canOpen = drillDown && item.pct !== null;
            const canPick = isChapterUnit && !!onPickChapter && item.pct !== null;
            const isOpen = canOpen && openId === item.lessonId;
            const topics = isOpen ? topicsByLesson[item.lessonId] : undefined;

            const label = (
              <>
                <span className="mr-1.5" aria-hidden="true">
                  {icon}
                </span>
                <span className="mr-1.5 font-bold text-muted">{codeOf(item.lessonId)}</span>
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
              </>
            );

            return (
              <li
                key={item.lessonId}
                className={`rounded-lg text-sm leading-relaxed text-ink ${item.lessonId === activeFocusId && useRadar ? "bg-primary-soft" : ""}`}
              >
                {canPick ? (
                  <button
                    type="button"
                    onClick={() => {
                      setFocusId(item.lessonId);
                      onPickChapter?.(item.lessonId);
                    }}
                    className="flex min-h-11 w-full items-center justify-between gap-2 rounded-lg px-1 text-left hover:bg-surface-2"
                  >
                    <span className="min-w-0">{label}</span>
                    <span className="shrink-0 text-[13px] font-semibold text-primary">Xem các bài ›</span>
                  </button>
                ) : canOpen ? (
                  <button
                    type="button"
                    aria-expanded={isOpen}
                    onClick={() => {
                      setUserOpen(isOpen ? null : item.lessonId);
                      setFocusId(item.lessonId);
                    }}
                    className="flex min-h-11 w-full items-center justify-between gap-2 rounded-lg px-1 text-left hover:bg-surface-2"
                  >
                    <span className="min-w-0">{label}</span>
                    <span className="shrink-0 text-muted" aria-hidden="true">
                      {isOpen ? "▴" : "▾"}
                    </span>
                  </button>
                ) : (
                  label
                )}
                {isOpen && (
                  <div className="mt-1 rounded-xl bg-surface-2 p-3">
                    {topics === undefined && <p className="text-[13px] text-muted">Đang tải kỹ năng…</p>}
                    {topics === "error" && (
                      <p className="text-[13px] text-muted">Chưa tải được chi tiết kỹ năng. Em thử lại sau nhé.</p>
                    )}
                    {Array.isArray(topics) &&
                      (() => {
                        const weak = weakestTopics(topics);
                        if (weak.length === 0) {
                          return (
                            <p className="text-[13px] text-muted">
                              Chưa có kỹ năng nào của bài này bị sai nhiều. Làm thêm câu để có thêm dữ liệu.
                            </p>
                          );
                        }
                        return (
                          <ul className="space-y-2">
                            {weak.map((t) => (
                              <li key={t.topicId}>
                                <button
                                  type="button"
                                  onClick={() => setPractice({ lessonId: item.lessonId, topicName: t.topicName })}
                                  className="flex min-h-11 w-full items-center justify-between gap-3 rounded-lg border border-line bg-panel px-3 py-2 text-left hover:border-primary"
                                >
                                  <span className="min-w-0">
                                    <span className="block text-sm font-medium text-ink">{t.topicName}</span>
                                    <span className="block text-[13px] text-muted">
                                      {MASTERY_ICON[t.level]} đúng {t.pct}% · {MASTERY_LABEL[t.level]}
                                    </span>
                                  </span>
                                  <span className="shrink-0 text-[13px] font-semibold text-primary">Luyện 10 câu ›</span>
                                </button>
                              </li>
                            ))}
                          </ul>
                        );
                      })()}
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </div>}

      {/* Nút chính duy nhất hoặc dòng chúc mừng */}
      <div className="mt-5">
        {isParent && weakestLesson ? (
          <p className="text-sm text-ink">
            Cần thêm nhất: <b>{weakestLesson.lessonTitle}</b> — {weakestLesson.pct}% thành thạo.
          </p>
        ) : weakestLesson && isChapterUnit ? (
          onPickChapter ? (
            <button
              type="button"
              onClick={() => onPickChapter(weakestLesson.lessonId)}
              className="inline-flex min-h-11 w-full items-center justify-center rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-primary-dark sm:w-auto"
            >
              Xem các bài của mảng yếu nhất
            </button>
          ) : null
        ) : weakestLesson ? (
          weakestTopic ? (
            <>
              <button
                type="button"
                onClick={() => setPractice({ lessonId: weakestLesson.lessonId, topicName: weakestTopic.topicName })}
                className="inline-flex min-h-11 w-full items-center justify-center rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-primary-dark sm:w-auto"
              >
                Luyện đúng chỗ yếu
              </button>
              <p className="mt-1.5 text-[13px] text-muted">
                {weakestTopic.topicName} · {weakestLesson.lessonTitle}
              </p>
            </>
          ) : (
            <Link
              href={`/lop-hoc/bai/?id=${weakestLesson.lessonId}#secondary-stage-ly_thuyet`}
              className="inline-flex min-h-11 w-full items-center justify-center rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-primary-dark sm:w-auto"
            >
              Ôn bài yếu nhất
            </Link>
          )
        ) : (
          <p className="text-sm font-medium text-ok">
            {isChapterUnit ? `Các mảng ${who} đã làm đều vững, học tiếp mảng còn trống.` : `Chương này ${who} đã nắm vững, học tiếp bài mới.`}
          </p>
        )}
      </div>

      {drillDown && (
        <QuickPractice
          request={practice}
          onClose={() => setPractice(null)}
          onFinished={() => {
            // Luyện xong: bỏ cache để mở lại bài thấy % mới (làm mới bài đang mở).
            setTopicsByLesson({});
          }}
          onUnavailable={(req) => {
            setPractice(null);
            window.location.assign(`/lop-hoc/bai?id=${req.lessonId}`);
          }}
        />
      )}
    </section>
  );
}

type RadarScope = "chapter" | "course";

/** Gộp các bài của một chương thành một đỉnh: % = Σđiểm đạt / Σđiểm tối đa (đúng công thức mastery-rules, không lấy trung bình % bài). */
function rollUpByChapter(rows: ChapterLessonMastery[]): ChapterLessonMastery[] {
  const byChapter = new Map<number, ChapterLessonMastery[]>();
  for (const r of rows) {
    const list = byChapter.get(r.chapterId);
    if (list) list.push(r);
    else byChapter.set(r.chapterId, [r]);
  }
  const out: ChapterLessonMastery[] = [];
  for (const [chapterId, list] of byChapter) {
    const se = list.reduce((acc, r) => acc + (r.earned ?? 0), 0);
    const sm = list.reduce((acc, r) => acc + (r.max ?? 0), 0);
    const pct = sm > 0 ? Math.round((se / sm) * 100) : null;
    out.push({
      chapterId,
      chapterTitle: list[0].chapterTitle,
      lessonId: chapterId,
      lessonTitle: list[0].chapterTitle,
      sortOrder: list[0].chapterSort ?? 0,
      answeredCount: list.reduce((acc, r) => acc + r.answeredCount, 0),
      pct,
      level: pct === null ? "insufficient" : pct >= 80 ? "mastered" : pct >= 50 ? "practicing" : "weak",
      chapterSort: list[0].chapterSort,
      subjectCode: list[0].subjectCode,
      isLatest: list.some((r) => r.isLatest),
    });
  }
  return out.sort((a, b) => a.sortOrder - b.sortOrder || a.chapterId - b.chapterId);
}

/**
 * Sơ đồ năng lực: theo chương (đỉnh = bài) hoặc cả khoá (đỉnh = chương; khoá HSG KHTN 9 mỗi chương là một
 * mảng Cơ / Nhiệt – Âm / Điện / Quang / Điện từ). Giáo viên xem hồ sơ em (preloaded) giữ nguyên bản theo chương.
 */
export default function ChapterMasteryRadar(props: ChapterMasteryRadarProps) {
  if (props.preloaded && !props.courseData) return <RadarView {...props} />;
  return <CourseRadar {...props} />;
}

function CourseRadar({ studentId, onLoaded, compact = false, courseData, viewer = "student" }: ChapterMasteryRadarProps) {
  const [fetchLoading, setLoading] = useState(!courseData);
  const [fetchedCur, setCur] = useState<ChapterLessonMastery[] | null>(null);
  const [fetchedPrev, setPrev] = useState<ChapterLessonMastery[] | null>(null);
  const hasPreloaded = !!courseData && courseData.current.some((r) => r.pct !== null);
  const loading = courseData ? false : fetchLoading;
  const cur = courseData ? (hasPreloaded ? courseData.current : null) : fetchedCur;
  const prev = courseData ? (hasPreloaded ? courseData.prev : null) : fetchedPrev;
  const [scope, setScope] = useState<RadarScope | null>(null);
  const [pickedChapter, setPickedChapter] = useState<number | null>(null);
  const onLoadedRef = useRef(onLoaded);
  useEffect(() => {
    onLoadedRef.current = onLoaded;
  });

  useEffect(() => {
    if (courseData) return;
    let active = true;
    const prevDate = new Date(Date.now() - 30 * 86400e3);
    const finish = (c: ChapterLessonMastery[] | null, p: ChapterLessonMastery[] | null) => {
      if (!active) return;
      const hasData = !!c && c.some((r) => r.pct !== null);
      setCur(hasData ? c : null);
      setPrev(hasData ? p : null);
      setLoading(false);
      onLoadedRef.current?.(hasData);
    };
    // Ưu tiên RPC cả khoá; chưa chạy migration thì lùi về RPC theo chương (không có bộ chuyển).
    Promise.all([fetchMyCourseMasteryPct(), fetchMyCourseMasteryPct(prevDate).catch(() => null)])
      .then(([c, p]) => finish(c, p))
      .catch(() =>
        Promise.all([fetchMyChapterMasteryPct(), fetchMyChapterMasteryPct(prevDate).catch(() => null)])
          .then(([c, p]) => finish(c, p))
          .catch(() => finish(null, null))
      );
    return () => {
      active = false;
    };
  }, [studentId, courseData]);

  const chapters = useMemo(() => {
    const seen = new Map<number, { id: number; title: string; sort: number }>();
    for (const r of cur ?? []) {
      if (!seen.has(r.chapterId)) seen.set(r.chapterId, { id: r.chapterId, title: r.chapterTitle, sort: r.chapterSort ?? 0 });
    }
    return [...seen.values()].sort((a, b) => a.sort - b.sort || a.id - b.id);
  }, [cur]);

  if (loading) {
    return (
      <div
        className="h-[280px] rounded-2xl border border-line bg-panel p-5"
        aria-busy="true"
        aria-label="Đang tải năng lực…"
      />
    );
  }
  if (!cur) return null;

  const hasCourse = cur.some((r) => r.chapterSort !== undefined) && chapters.length >= 2;
  const latestChapterId = cur.find((r) => r.isLatest)?.chapterId ?? chapters[0]?.id ?? cur[0].chapterId;
  const isHsg = (cur[0].subjectCode ?? "").startsWith("hsg");
  const courseLabel = isHsg ? "Theo mảng" : "Cả khoá";
  const effScope: RadarScope = !hasCourse ? "chapter" : (scope ?? (isHsg ? "course" : "chapter"));
  const selChapter = chapters.some((c) => c.id === pickedChapter) ? (pickedChapter as number) : latestChapterId;

  const pickChapter = (id: number) => {
    setPickedChapter(id);
    setScope("chapter");
  };

  let curView: ChapterLessonMastery[];
  let prevView: ChapterLessonMastery[] | null;
  if (effScope === "course") {
    curView = rollUpByChapter(cur);
    prevView = prev ? rollUpByChapter(prev) : null;
  } else {
    curView = hasCourse ? cur.filter((r) => r.chapterId === selChapter) : cur;
    prevView = prev ? (hasCourse ? prev.filter((r) => r.chapterId === selChapter) : prev) : null;
  }

  const switcher = hasCourse ? (
    <div className="mt-3 flex flex-wrap items-center gap-2">
      <div role="group" aria-label="Phạm vi xem" className="inline-flex overflow-hidden rounded-xl border border-line">
        {(
          [
            ["chapter", "Theo chương"],
            ["course", courseLabel],
          ] as const
        ).map(([val, label]) => (
          <button
            key={val}
            type="button"
            aria-pressed={effScope === val}
            onClick={() => setScope(val)}
            className={`min-h-11 px-4 text-sm font-semibold ${
              effScope === val ? "bg-primary text-white" : "bg-panel text-ink hover:bg-surface-2"
            }`}
          >
            {label}
          </button>
        ))}
      </div>
      {effScope === "chapter" && (
        <label className="flex min-w-0 items-center gap-2 text-sm text-muted">
          <span className="shrink-0">Chương</span>
          <select
            value={selChapter}
            onChange={(e) => pickChapter(Number(e.target.value))}
            className="min-h-11 min-w-0 max-w-[14rem] rounded-xl border border-line bg-panel px-3 text-sm text-ink"
          >
            {chapters.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
        </label>
      )}
    </div>
  ) : null;

  if (!curView.some((r) => r.pct !== null)) {
    return (
      <section className="rounded-2xl border border-line bg-panel p-5">
        <h2 className="font-display font-semibold text-ink">Năng lực chương</h2>
        {switcher}
        <p className="mt-3 text-sm text-muted">
          {viewer === "parent" ? "Con" : "Em"} chưa làm bài nào của chương này nên chưa có sơ đồ.
        </p>
      </section>
    );
  }

  return (
    <RadarView
      key={`${effScope}-${effScope === "chapter" ? selChapter : "all"}`}
      studentId={studentId}
      compact={compact}
      onLoaded={onLoaded}
      preloaded={{ current: curView, prev: prevView }}
      allowDrill={effScope === "chapter" && !courseData}
      unit={effScope === "course" ? "chapter" : "lesson"}
      title={effScope === "course" ? (isHsg ? "theo mảng kiến thức" : "cả khoá") : undefined}
      subtitle={
        effScope === "course"
          ? `Mỗi đỉnh là một chương; so với chính ${viewer === "parent" ? "con" : "em"} 30 ngày trước và mục tiêu 80%`
          : undefined
      }
      viewer={viewer}
      headerSlot={switcher}
      onPickChapter={effScope === "course" ? pickChapter : undefined}
    />
  );
}
