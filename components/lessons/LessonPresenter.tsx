"use client";

import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent as ReactPointerEvent,
  type TouchEvent as ReactTouchEvent,
} from "react";
import { createPortal } from "react-dom";
import {
  ChevronLeft,
  ChevronRight,
  Eraser,
  Highlighter,
  Keyboard,
  List,
  Maximize2,
  Minimize2,
  Moon,
  Pen,
  Sun,
  Trash2,
  Undo2,
  X,
  ZoomIn,
  ZoomOut,
} from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import { splitTheorySections } from "@/features/lessons/theory-sections";
import type { LessonItem } from "@/features/lessons/types";

/**
 * components/lessons/LessonPresenter.tsx
 *
 * Chế độ TRÌNH CHIẾU bài giảng cho tab Lý thuyết của trang bài học — dạy lý thuyết trên lớp,
 * chiếu lên tivi/máy chiếu.
 *
 * Vì sao là lớp phủ (overlay) chứ không phải một route riêng: trang bài học đã tải sẵn
 * `body_html` của mọi mục lý thuyết, nên chiếu tại chỗ tốn **0 request mới** và không phải
 * dựng thêm một đường tải học liệu thứ hai (xem quy tắc tối ưu tốc độ trong AGENTS.md: không
 * thêm round-trip Supabase cho trang đã đo).
 *
 * Chia trang chiếu: dùng chung `splitTheorySections` với trang đọc (features/lessons/
 * theory-sections.ts) — mỗi mốc tiêu đề I., II., III. có sẵn trong nội dung là một trang, nên
 * thầy không phải soạn slide riêng, và trang chiếu không bao giờ lệch với bài học sinh đọc.
 *
 * Bút vẽ: nét lưu theo từng trang dưới dạng toạ độ CHUẨN HOÁ (0..1) nên đổi cỡ chữ hay xoay
 * màn hình vẫn đúng vị trí; đổi trang rồi quay lại vẫn còn nét.
 */

const ZOOM_MIN = 0.7;
const ZOOM_MAX = 2.2;
const ZOOM_STEP = 0.1;
const ZOOM_STORE = "thachlab-presenter-zoom";
const BG_STORE = "thachlab-presenter-bg";
/** Thời gian thanh điều khiển tự ẩn khi thầy không đụng chuột (ms). */
const CHROME_HIDE_MS = 3200;

type PenMode = "off" | "pen" | "marker" | "eraser";
type PresenterBg = "light" | "dark";

/** Màu bút — đỏ để khoanh ý chính, xanh để bổ sung, vàng là bút dạ quang. */
const PEN_COLORS = [
  { value: "#ef4444", label: "Đỏ" },
  { value: "#2563eb", label: "Xanh" },
  { value: "#16a34a", label: "Lục" },
];
const MARKER_COLOR = "#facc15";

interface Stroke {
  mode: "pen" | "marker";
  color: string;
  /** Độ dày tính bằng px màn hình — giữ nguyên khi phóng to chữ để nét vẽ vẫn rõ. */
  width: number;
  /** Toạ độ chuẩn hoá 0..1 so với khung vẽ. */
  points: Array<[number, number]>;
}

type PageKind = "cover" | "content";

interface DeckPage {
  key: string;
  kind: PageKind;
  /** Nhóm để dựng mục lục nhanh trong lúc chiếu (mỗi mục lý thuyết là một nhóm). */
  groupKey: string;
  groupTitle: string;
  heading: string;
  bodyHtml: string;
}

/** Tiêu đề chung của cả mục, không phải nội dung: "LÝ THUYẾT", "LÍ THUYẾT". */
const GENERIC_INTRO_RE = /^l[ýí]thuy[ếe]t$/i;

/**
 * Phần "mở bài" chỉ đáng thành một trang chiếu khi có nội dung thật (chữ, hình, bảng). Nhiều
 * bài mở đầu bằng đúng một <h2>LÝ THUYẾT</h2> — chiếu riêng một trang chỉ có chữ "LÝ THUYẾT"
 * là trang thừa, mà tiêu đề mục đã hiện sẵn ở dòng kicker phía trên rồi.
 */
function hasVisibleContent(html: string): boolean {
  if (/<(img|svg|table|figure)\b/i.test(html)) return true;
  const text = html.replace(/<[^>]+>/g, " ").replace(/&nbsp;/gi, " ").trim();
  if (text.length === 0) return false;
  return !GENERIC_INTRO_RE.test(text.replace(/\s+/g, ""));
}

/**
 * Dựng "bộ trang chiếu" từ các mục lý thuyết của bài: 1 trang bìa + mỗi đoạn lý thuyết 1 trang.
 * @param lessonTitle tên bài — dùng cho trang bìa và nhãn nhóm khi mục không có tiêu đề riêng
 */
export function buildPresenterDeck(lessonTitle: string, items: LessonItem[]): DeckPage[] {
  const pages: DeckPage[] = [
    { key: "cover", kind: "cover", groupKey: "cover", groupTitle: "Mở đầu", heading: lessonTitle, bodyHtml: "" },
  ];

  items.forEach((item) => {
    const groupKey = `item-${item.id}`;
    // mode "chieu": chia theo mốc LỚN (h2 → h3 → in đậm) để mỗi trang là một mục I., II., III.
    const { introHtml, sections } = splitTheorySections(item.body_html, item.id, "chieu");

    if (sections.length === 0) {
      // Bài chưa có mốc tiêu đề nào → cả mục là một trang, không cắt vụn nội dung.
      // introHtml đã bỏ câu thời lượng tác giả (xem stripAuthoredDuration).
      if (introHtml.trim()) {
        pages.push({
          key: `${groupKey}-all`,
          kind: "content",
          groupKey,
          groupTitle: item.title,
          heading: item.title,
          bodyHtml: introHtml,
        });
      }
      return;
    }

    if (hasVisibleContent(introHtml)) {
      pages.push({
        key: `${groupKey}-intro`,
        kind: "content",
        groupKey,
        groupTitle: item.title,
        heading: item.title,
        bodyHtml: introHtml,
      });
    }

    sections.forEach((section, index) => {
      pages.push({
        key: `${groupKey}-${index}`,
        kind: "content",
        groupKey,
        groupTitle: item.title,
        heading: section.heading || item.title,
        bodyHtml: section.bodyHtml,
      });
    });
  });

  return pages;
}

/** Cỡ chữ đã lưu của lần dạy trước (phòng/tivi khác nhau cần cỡ chữ khác nhau). */
function readStoredZoom(): number {
  if (typeof window === "undefined") return 1;
  try {
    const saved = Number(window.localStorage.getItem(ZOOM_STORE));
    return saved >= ZOOM_MIN && saved <= ZOOM_MAX ? saved : 1;
  } catch {
    return 1;
  }
}

/** Nền chiếu đã lưu: "sáng" cho phòng bật đèn, "tối" cho phòng tối. */
function readStoredBg(): PresenterBg {
  if (typeof window === "undefined") return "light";
  try {
    return window.localStorage.getItem(BG_STORE) === "dark" ? "dark" : "light";
  } catch {
    return "light";
  }
}

/** Vẽ một nét lên canvas theo toạ độ chuẩn hoá. */
function paintStroke(ctx: CanvasRenderingContext2D, stroke: Stroke, w: number, h: number) {
  const { points } = stroke;
  if (points.length === 0) return;
  ctx.save();
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.strokeStyle = stroke.color;
  ctx.fillStyle = stroke.color;
  ctx.globalAlpha = stroke.mode === "marker" ? 0.35 : 1;
  ctx.lineWidth = stroke.width;

  if (points.length === 1) {
    // Chấm một điểm (bấm không kéo) — vẽ hình tròn cho khỏi mất nét.
    ctx.beginPath();
    ctx.arc(points[0][0] * w, points[0][1] * h, stroke.width / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    return;
  }

  ctx.beginPath();
  points.forEach(([x, y], i) => {
    const px = x * w;
    const py = y * h;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  });
  ctx.stroke();
  ctx.restore();
}

export default function LessonPresenter({
  lessonTitle,
  chapterLabel,
  items,
  onClose,
}: {
  lessonTitle: string;
  chapterLabel?: string;
  /** Các mục lý thuyết của bài (đã lọc bỏ mục rỗng) — trang chiếu dựng từ đây, không gọi mạng. */
  items: LessonItem[];
  onClose: () => void;
}) {
  const pages = useMemo(() => buildPresenterDeck(lessonTitle, items), [lessonTitle, items]);

  const [index, setIndex] = useState(0);
  // Cỡ chữ và nền đọc thẳng từ lần dạy trước ngay khi khởi tạo state — component này chỉ mount
  // ở client (next/dynamic ssr:false, mở sau cú bấm) nên không có vấn đề lệch khi hydrate, và
  // tránh được việc setState trong effect (gây render chồng).
  const [zoom, setZoom] = useState(readStoredZoom);
  const [bg, setBg] = useState<PresenterBg>(readStoredBg);
  const [pen, setPen] = useState<PenMode>("off");
  /** Nhắc "đang bật bút" chỉ hiện vài giây đầu — để lâu sẽ che chữ ở đáy trang chiếu. */
  const [drawHint, setDrawHint] = useState(false);
  const [color, setColor] = useState(PEN_COLORS[0].value);
  const [menuOpen, setMenuOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [chrome, setChrome] = useState(true);
  const [isFull, setIsFull] = useState(false);
  /**
   * Số nét đã vẽ theo từng trang. Nét thật nằm trong `strokesRef` (khung vẽ đọc trực tiếp trong
   * effect/handler), nhưng render cần biết trang đang mở có nét hay không để bật/tắt nút "bỏ nét
   * vừa vẽ" / "xoá hết" — nên giữ thêm bản đếm trong state, KHÔNG đọc ref lúc render.
   */
  const [strokeCounts, setStrokeCounts] = useState<Record<number, number>>({});

  const rootRef = useRef<HTMLDivElement | null>(null);
  const stageRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const strokesRef = useRef<Map<number, Stroke[]>>(new Map());
  const liveRef = useRef<Stroke | null>(null);
  const hideTimerRef = useRef<number | null>(null);
  const drawHintTimerRef = useRef<number | null>(null);
  const touchStartRef = useRef<{ x: number; y: number } | null>(null);
  const zoomRef = useRef(zoom);

  const page = pages[Math.min(index, pages.length - 1)];
  const showChrome = chrome || pen !== "off" || menuOpen || helpOpen;
  const pageHasStrokes = (strokeCounts[index] ?? 0) > 0;

  /** Cập nhật bản đếm nét của một trang — gọi trong handler (được phép đọc ref), không gọi lúc render. */
  const syncStrokeCount = useCallback((pageIndex: number) => {
    const count = strokesRef.current.get(pageIndex)?.length ?? 0;
    setStrokeCounts((prev) => (prev[pageIndex] === count ? prev : { ...prev, [pageIndex]: count }));
  }, []);

  /** Nhóm trang theo mục lý thuyết — dựng mục lục nhảy nhanh trong lúc chiếu. */
  const groups = useMemo(() => {
    const out: { key: string; title: string; pages: { index: number; label: string }[] }[] = [];
    pages.forEach((p, i) => {
      let group = out.find((g) => g.key === p.groupKey);
      if (!group) {
        group = { key: p.groupKey, title: p.groupTitle, pages: [] };
        out.push(group);
      }
      group.pages.push({ index: i, label: p.kind === "cover" ? lessonTitle : p.heading });
    });
    return out;
  }, [pages, lessonTitle]);

  // ---------- Canvas: vẽ tay + bút dạ quang ----------

  const repaint = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    if (w === 0 || h === 0) return;
    if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    for (const stroke of strokesRef.current.get(index) ?? []) paintStroke(ctx, stroke, w, h);
    if (liveRef.current) paintStroke(ctx, liveRef.current, w, h);
  }, [index]);

  // Vẽ lại khi đổi trang, khi cửa sổ đổi kích thước, và mỗi lần số nét đổi (thêm/xoá nét).
  useEffect(() => {
    repaint();
  }, [repaint, strokeCounts]);

  useEffect(() => {
    const onResize = () => repaint();
    window.addEventListener("resize", onResize);
    window.addEventListener("orientationchange", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      window.removeEventListener("orientationchange", onResize);
    };
  }, [repaint]);

  function pointFrom(e: ReactPointerEvent<HTMLCanvasElement>): [number, number] {
    const rect = e.currentTarget.getBoundingClientRect();
    return [(e.clientX - rect.left) / Math.max(1, rect.width), (e.clientY - rect.top) / Math.max(1, rect.height)];
  }

  function eraseAt([x, y]: [number, number]) {
    const canvas = canvasRef.current;
    const list = strokesRef.current.get(index);
    if (!canvas || !list?.length) return;
    const w = canvas.clientWidth || 1;
    const h = canvas.clientHeight || 1;
    const px = x * w;
    const py = y * h;
    const radius = 16;
    const kept = list.filter(
      (stroke) => !stroke.points.some(([sx, sy]) => Math.hypot(sx * w - px, sy * h - py) < radius),
    );
    if (kept.length === list.length) return;
    strokesRef.current.set(index, kept);
    syncStrokeCount(index);
  }

  function onCanvasPointerDown(e: ReactPointerEvent<HTMLCanvasElement>) {
    if (pen === "off") return;
    e.currentTarget.setPointerCapture(e.pointerId);
    const point = pointFrom(e);
    if (pen === "eraser") {
      eraseAt(point);
      return;
    }
    liveRef.current = {
      mode: pen,
      color: pen === "marker" ? MARKER_COLOR : color,
      width: pen === "marker" ? 16 : 3,
      points: [point],
    };
    repaint();
  }

  function onCanvasPointerMove(e: ReactPointerEvent<HTMLCanvasElement>) {
    if (pen === "off") return;
    const point = pointFrom(e);
    if (pen === "eraser") {
      if (e.buttons !== 0) eraseAt(point);
      return;
    }
    const live = liveRef.current;
    if (!live) return;
    const last = live.points[live.points.length - 1];
    // Bỏ điểm quá sát nhau: nét vẫn mượt nhưng không phình dữ liệu khi rê chậm.
    if (Math.abs(point[0] - last[0]) + Math.abs(point[1] - last[1]) < 0.0015) return;
    live.points.push(point);
    repaint();
  }

  function onCanvasPointerUp() {
    const live = liveRef.current;
    if (!live) return;
    liveRef.current = null;
    strokesRef.current.set(index, [...(strokesRef.current.get(index) ?? []), live]);
    syncStrokeCount(index);
  }

  const undoStroke = useCallback(() => {
    const list = strokesRef.current.get(index);
    if (!list?.length) return;
    strokesRef.current.set(index, list.slice(0, -1));
    syncStrokeCount(index);
  }, [index, syncStrokeCount]);

  const clearPage = useCallback(() => {
    if (!(strokesRef.current.get(index)?.length ?? 0)) return;
    strokesRef.current.set(index, []);
    syncStrokeCount(index);
  }, [index, syncStrokeCount]);

  /**
   * Đổi chế độ bút — dùng chung cho nút bấm và phím tắt. Nhắc nhở tự tắt sau ít giây: khi bật
   * bút, khung vẽ phủ lên cả bài nên bấm vào nội dung sẽ không ăn, cần nói rõ cho thầy biết,
   * nhưng để thường trực thì che mất chữ ở đáy trang chiếu.
   */
  const setPenMode = useCallback((next: PenMode) => {
    setPen(next);
    if (drawHintTimerRef.current) window.clearTimeout(drawHintTimerRef.current);
    if (next === "off") {
      setDrawHint(false);
      return;
    }
    setDrawHint(true);
    drawHintTimerRef.current = window.setTimeout(() => setDrawHint(false), 4500);
  }, []);

  useEffect(() => {
    return () => {
      if (drawHintTimerRef.current) window.clearTimeout(drawHintTimerRef.current);
    };
  }, []);

  // ---------- Điều hướng ----------

  const go = useCallback(
    (next: number) => {
      setIndex(Math.max(0, Math.min(pages.length - 1, next)));
      setMenuOpen(false);
    },
    [pages.length],
  );

  // Sang trang mới thì đọc từ đầu trang đó (trang trước có thể đã cuộn xuống giữa).
  useEffect(() => {
    stageRef.current?.scrollTo({ top: 0 });
  }, [index]);

  const applyZoom = useCallback((next: number) => {
    const value = Math.round(Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, next)) * 100) / 100;
    zoomRef.current = value;
    setZoom(value);
    try {
      localStorage.setItem(ZOOM_STORE, String(value));
    } catch {
      // Trình duyệt chặn localStorage — cỡ chữ vẫn đổi, chỉ không nhớ cho lần sau.
    }
  }, []);

  const zoomBy = useCallback((delta: number) => applyZoom(zoomRef.current + delta), [applyZoom]);

  const toggleBg = useCallback(() => {
    setBg((current) => {
      const next: PresenterBg = current === "light" ? "dark" : "light";
      try {
        localStorage.setItem(BG_STORE, next);
      } catch {
        // không nhớ được thì thôi
      }
      return next;
    });
  }, []);

  const toggleFullscreen = useCallback(() => {
    if (document.fullscreenElement) {
      void document.exitFullscreen().catch(() => undefined);
      return;
    }
    void rootRef.current?.requestFullscreen?.().catch(() => undefined);
  }, []);

  const close = useCallback(() => {
    if (document.fullscreenElement) void document.exitFullscreen().catch(() => undefined);
    onClose();
  }, [onClose]);

  // ---------- Hiệu ứng vòng đời ----------

  // Khoá cuộn trang nền khi đang chiếu, và thoát toàn màn hình lúc đóng (không để thầy kẹt
  // trong màn hình chiếu sau khi bấm ✕).
  useEffect(() => {
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
      if (document.fullscreenElement) void document.exitFullscreen().catch(() => undefined);
    };
  }, []);

  // Giữ tiêu điểm trong lớp phủ (bàn phím vẫn nghe ở window, nhưng focus đúng chỗ cho a11y).
  useEffect(() => {
    rootRef.current?.focus();
  }, []);

  useEffect(() => {
    const onFsChange = () => setIsFull(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", onFsChange);
    onFsChange();
    return () => document.removeEventListener("fullscreenchange", onFsChange);
  }, []);

  /** Đặt lại đồng hồ tự ẩn thanh điều khiển. */
  const armChromeTimer = useCallback(() => {
    if (hideTimerRef.current) window.clearTimeout(hideTimerRef.current);
    hideTimerRef.current = window.setTimeout(() => setChrome(false), CHROME_HIDE_MS);
  }, []);

  // Thanh điều khiển tự ẩn cho nội dung chiếu rộng tối đa; đụng chuột/chạm là hiện lại.
  const showChromeNow = useCallback(() => {
    setChrome(true);
    armChromeTimer();
  }, [armChromeTimer]);

  // Đồng hồ chạy lại từ đầu mỗi lần sang trang. Cố ý KHÔNG setChrome(true) ở đây: lật trang
  // bằng bàn phím trong lúc thanh đang ẩn thì cứ để ẩn cho nội dung rộng nhất. Trang bìa thì
  // không hẹn giờ ẩn — vừa mở chế độ chiếu mà thanh điều khiển biến mất sau 3 giây thì thầy
  // không biết mình có những nút gì.
  useEffect(() => {
    if (index === 0) return;
    armChromeTimer();
    return () => {
      if (hideTimerRef.current) window.clearTimeout(hideTimerRef.current);
    };
  }, [armChromeTimer, index]);

  // ---------- Bàn phím ----------
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const target = e.target as HTMLElement | null;
      if (target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable)) return;

      const mod = e.ctrlKey || e.metaKey;
      if (mod) {
        if (e.key === "+" || e.key === "=") {
          e.preventDefault();
          zoomBy(ZOOM_STEP);
        } else if (e.key === "-" || e.key === "_") {
          e.preventDefault();
          zoomBy(-ZOOM_STEP);
        } else if (e.key === "0") {
          e.preventDefault();
          applyZoom(1);
        }
        return;
      }

      switch (e.key) {
        case "ArrowRight":
        case "PageDown":
        case " ":
        case "Spacebar":
          e.preventDefault();
          go(index + 1);
          break;
        case "ArrowLeft":
        case "PageUp":
          e.preventDefault();
          go(index - 1);
          break;
        case "Home":
          e.preventDefault();
          go(0);
          break;
        case "End":
          e.preventDefault();
          go(pages.length - 1);
          break;
        case "Escape":
          // Đang toàn màn hình thì trình duyệt tự lo Esc (không gửi sự kiện xuống trang) —
          // ở đây chỉ xử lý Esc khi đang KHÔNG toàn màn hình.
          if (menuOpen) setMenuOpen(false);
          else if (helpOpen) setHelpOpen(false);
          else if (pen !== "off") setPenMode("off");
          else close();
          break;
        case "f":
        case "F":
          toggleFullscreen();
          break;
        case "d":
        case "D":
          setPenMode(pen === "off" ? "pen" : "off");
          break;
        case "h":
        case "H":
          setPenMode(pen === "marker" ? "off" : "marker");
          break;
        case "e":
        case "E":
          setPenMode(pen === "eraser" ? "off" : "eraser");
          break;
        case "z":
        case "Z":
          undoStroke();
          break;
        case "c":
        case "C":
          clearPage();
          break;
        case "l":
        case "L":
          setMenuOpen((open) => !open);
          break;
        case "?":
          setHelpOpen((open) => !open);
          break;
        default:
          break;
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [applyZoom, clearPage, close, go, helpOpen, index, menuOpen, pages.length, pen, setPenMode, toggleFullscreen, undoStroke, zoomBy]);

  // ---------- Vuốt ngang để lật trang (khi không bật bút) ----------
  function onTouchStart(e: ReactTouchEvent<HTMLDivElement>) {
    if (pen !== "off") return;
    const touch = e.touches[0];
    touchStartRef.current = { x: touch.clientX, y: touch.clientY };
  }

  function onTouchEnd(e: ReactTouchEvent<HTMLDivElement>) {
    const start = touchStartRef.current;
    touchStartRef.current = null;
    if (!start || pen !== "off") return;
    const touch = e.changedTouches[0];
    const dx = touch.clientX - start.x;
    const dy = touch.clientY - start.y;
    if (Math.abs(dx) > 64 && Math.abs(dx) > Math.abs(dy) * 1.6) go(dx < 0 ? index + 1 : index - 1);
  }

  if (typeof document === "undefined") return null;

  const drawing = pen !== "off";
  const penLabel = pen === "pen" ? "Bút" : pen === "marker" ? "Dạ quang" : pen === "eraser" ? "Tẩy" : "Bút vẽ";

  return createPortal(
    <div
      ref={rootRef}
      className={`lesson-presenter ${showChrome ? "is-chrome" : ""} ${drawing ? "is-drawing" : ""}`}
      data-bg={bg}
      role="dialog"
      aria-modal="true"
      aria-label={`Trình chiếu bài giảng: ${lessonTitle}`}
      tabIndex={-1}
      onMouseMove={showChromeNow}
      onTouchStart={(e) => {
        showChromeNow();
        onTouchStart(e);
      }}
      onTouchEnd={onTouchEnd}
    >
      {/* Khung vẽ nằm dưới thanh điều khiển: bật bút vẫn bấm được nút. */}
      <canvas
        ref={canvasRef}
        className={`presenter-canvas ${drawing ? "is-active" : ""}`}
        onPointerDown={onCanvasPointerDown}
        onPointerMove={onCanvasPointerMove}
        onPointerUp={onCanvasPointerUp}
        onPointerCancel={onCanvasPointerUp}
      />

      <header className="presenter-top">
        <div className="presenter-info">
          <strong>{page.kind === "cover" ? lessonTitle : page.groupTitle}</strong>
          <span>
            {chapterLabel ? `${chapterLabel} · ` : ""}
            Trang {index + 1}/{pages.length}
          </span>
        </div>
        <div className="presenter-actions">
          <button type="button" onClick={toggleBg} title="Đổi nền chiếu: sáng cho phòng đèn, tối cho phòng tối">
            {bg === "light" ? <Sun size={16} aria-hidden /> : <Moon size={16} aria-hidden />}
            <span className="presenter-btn-text">{bg === "light" ? "Nền sáng" : "Nền tối"}</span>
          </button>
          <button type="button" onClick={() => setHelpOpen((open) => !open)} title="Phím tắt (?)">
            <Keyboard size={16} aria-hidden />
            <span className="presenter-btn-text">Phím tắt</span>
          </button>
          <button type="button" onClick={toggleFullscreen} title="Toàn màn hình (F)">
            {isFull ? <Minimize2 size={16} aria-hidden /> : <Maximize2 size={16} aria-hidden />}
            <span className="presenter-btn-text">{isFull ? "Thu nhỏ" : "Toàn màn hình"}</span>
          </button>
          <button type="button" className="presenter-close" onClick={close} title="Thoát trình chiếu (Esc)">
            <X size={16} aria-hidden />
            <span className="presenter-btn-text">Thoát</span>
          </button>
        </div>
      </header>

      <div className="presenter-stage" ref={stageRef} style={{ "--presenter-zoom": zoom } as CSSProperties}>
        <article className="presenter-slide" key={page.key}>
          {page.kind === "cover" ? (
            <div className="presenter-cover">
              <p className="presenter-cover-kicker">{chapterLabel || "Bài học"}</p>
              <h1>{lessonTitle}</h1>
              <p className="presenter-cover-sub">
                {pages.length - 1} trang nội dung · lật trang bằng <kbd>←</kbd> <kbd>→</kbd> hoặc <kbd>Space</kbd>
              </p>
              <button type="button" className="presenter-cover-start" onClick={() => go(1)}>
                Bắt đầu <ChevronRight size={18} aria-hidden />
              </button>
            </div>
          ) : (
            <>
              <p className="presenter-kicker">{page.groupTitle}</p>
              {page.heading && <h2 className="presenter-heading">{page.heading}</h2>}
              <ContentHtml html={page.bodyHtml} className="presenter-prose" />
            </>
          )}
        </article>
      </div>

      {menuOpen && (
        <div className="presenter-panel presenter-panel--menu" role="dialog" aria-label="Mục lục bài giảng">
          <div className="presenter-panel-head">
            <p>
              <List size={15} aria-hidden /> Mục lục bài giảng
            </p>
            <button type="button" onClick={() => setMenuOpen(false)} aria-label="Đóng mục lục">
              <X size={15} aria-hidden />
            </button>
          </div>
          <div className="presenter-panel-body">
            {groups.map((group) => (
              <div key={group.key} className="presenter-menu-group">
                <p className="presenter-menu-title">{group.title}</p>
                <ol>
                  {group.pages.map((entry) => (
                    <li key={entry.index}>
                      <button
                        type="button"
                        className={entry.index === index ? "is-current" : ""}
                        onClick={() => go(entry.index)}
                      >
                        <span>{entry.index + 1}</span>
                        {entry.label}
                      </button>
                    </li>
                  ))}
                </ol>
              </div>
            ))}
          </div>
        </div>
      )}

      {helpOpen && (
        <div className="presenter-panel presenter-panel--help" role="dialog" aria-label="Phím tắt khi trình chiếu">
          <div className="presenter-panel-head">
            <p>
              <Keyboard size={15} aria-hidden /> Phím tắt khi trình chiếu
            </p>
            <button type="button" onClick={() => setHelpOpen(false)} aria-label="Đóng bảng phím tắt">
              <X size={15} aria-hidden />
            </button>
          </div>
          <div className="presenter-panel-body">
            <dl className="presenter-keys">
              <div>
                <dt>
                  <kbd>→</kbd> <kbd>Space</kbd>
                </dt>
                <dd>Trang sau</dd>
              </div>
              <div>
                <dt>
                  <kbd>←</kbd>
                </dt>
                <dd>Trang trước</dd>
              </div>
              <div>
                <dt>
                  <kbd>Home</kbd> / <kbd>End</kbd>
                </dt>
                <dd>Trang đầu / trang cuối</dd>
              </div>
              <div>
                <dt>
                  <kbd>D</kbd>
                </dt>
                <dd>Bật/tắt bút vẽ (khoanh ý chính)</dd>
              </div>
              <div>
                <dt>
                  <kbd>H</kbd>
                </dt>
                <dd>Bút dạ quang vàng</dd>
              </div>
              <div>
                <dt>
                  <kbd>E</kbd>
                </dt>
                <dd>Tẩy (xoá cả nét vừa chạm)</dd>
              </div>
              <div>
                <dt>
                  <kbd>Z</kbd>
                </dt>
                <dd>Bỏ nét vừa vẽ</dd>
              </div>
              <div>
                <dt>
                  <kbd>C</kbd>
                </dt>
                <dd>Xoá hết nét ở trang này</dd>
              </div>
              <div>
                <dt>
                  <kbd>Ctrl</kbd> <kbd>+</kbd> / <kbd>−</kbd> / <kbd>0</kbd>
                </dt>
                <dd>Phóng to / thu nhỏ / về cỡ gốc</dd>
              </div>
              <div>
                <dt>
                  <kbd>L</kbd>
                </dt>
                <dd>Mở mục lục nhảy nhanh</dd>
              </div>
              <div>
                <dt>
                  <kbd>F</kbd>
                </dt>
                <dd>Toàn màn hình</dd>
              </div>
              <div>
                <dt>
                  <kbd>Esc</kbd>
                </dt>
                <dd>Tắt bút → đóng bảng → thoát trình chiếu</dd>
              </div>
            </dl>
            <p className="presenter-help-note">
              Nét vẽ lưu riêng theo từng trang — lật đi lật lại vẫn còn. Đổi cỡ chữ không làm lệch nét.
            </p>
          </div>
        </div>
      )}

      <footer className="presenter-bar">
        <button
          type="button"
          onClick={() => go(index - 1)}
          disabled={index === 0}
          title="Trang trước (←)"
          aria-label="Trang trước"
        >
          <ChevronLeft size={18} aria-hidden />
        </button>

        <button type="button" className={`presenter-page ${menuOpen ? "is-on" : ""}`} onClick={() => setMenuOpen((o) => !o)} title="Mục lục bài giảng (L)">
          <List size={15} aria-hidden />
          <span>
            Trang {index + 1}/{pages.length}
          </span>
        </button>

        <button
          type="button"
          onClick={() => go(index + 1)}
          disabled={index >= pages.length - 1}
          title="Trang sau (→ hoặc Space)"
          aria-label="Trang sau"
        >
          <ChevronRight size={18} aria-hidden />
        </button>

        <span className="presenter-bar-sep" aria-hidden />

        <button
          type="button"
          className={pen === "pen" ? "is-on" : ""}
          onClick={() => setPenMode(pen === "pen" ? "off" : "pen")}
          title="Bút vẽ — khoanh ý chính trên bài (D)"
          aria-pressed={pen === "pen"}
        >
          <Pen size={15} aria-hidden />
          {/* Nhãn CỐ ĐỊNH của công cụ, không dùng penLabel: penLabel đổi theo chế độ đang bật
              nên nút bút sẽ mang tên "Dạ quang" khi thầy đang bật dạ quang. */}
          <span className="presenter-btn-text">Bút vẽ</span>
        </button>
        <button
          type="button"
          className={pen === "marker" ? "is-on" : ""}
          onClick={() => setPenMode(pen === "marker" ? "off" : "marker")}
          title="Bút dạ quang vàng (H)"
          aria-pressed={pen === "marker"}
        >
          <Highlighter size={15} aria-hidden />
          <span className="presenter-btn-text">Dạ quang</span>
        </button>
        <button
          type="button"
          className={pen === "eraser" ? "is-on" : ""}
          onClick={() => setPenMode(pen === "eraser" ? "off" : "eraser")}
          title="Tẩy nét (E)"
          aria-pressed={pen === "eraser"}
        >
          <Eraser size={15} aria-hidden />
          <span className="presenter-btn-text">Tẩy</span>
        </button>

        {pen === "pen" && (
          <span className="presenter-colors" role="group" aria-label="Màu bút">
            {PEN_COLORS.map((option) => (
              <button
                key={option.value}
                type="button"
                className={color === option.value ? "is-current" : ""}
                style={{ "--dot": option.value } as CSSProperties}
                onClick={() => setColor(option.value)}
                title={`Màu ${option.label}`}
                aria-label={`Màu ${option.label}`}
                aria-pressed={color === option.value}
              />
            ))}
          </span>
        )}

        <button type="button" onClick={undoStroke} disabled={!pageHasStrokes} title="Bỏ nét vừa vẽ (Z)">
          <Undo2 size={15} aria-hidden />
        </button>
        <button
          type="button"
          onClick={clearPage}
          disabled={!pageHasStrokes}
          title="Xoá hết nét ở trang này (C)"
          aria-label="Xoá hết nét ở trang này"
        >
          <Trash2 size={15} aria-hidden />
        </button>

        <span className="presenter-bar-sep" aria-hidden />

        <button type="button" onClick={() => zoomBy(-ZOOM_STEP)} disabled={zoom <= ZOOM_MIN} title="Thu nhỏ chữ (Ctrl −)" aria-label="Thu nhỏ chữ">
          <ZoomOut size={15} aria-hidden />
        </button>
        <span className="presenter-zoom" aria-live="polite">
          {Math.round(zoom * 100)}%
        </span>
        <button type="button" onClick={() => zoomBy(ZOOM_STEP)} disabled={zoom >= ZOOM_MAX} title="Phóng to chữ (Ctrl +)" aria-label="Phóng to chữ">
          <ZoomIn size={15} aria-hidden />
        </button>
      </footer>

      <div className="presenter-progress" aria-hidden>
        <span style={{ width: `${((index + 1) / pages.length) * 100}%` }} />
      </div>

      {drawHint && drawing && (
        <p className="presenter-draw-hint">
          Đang bật {penLabel}: vẽ trực tiếp lên bài chiếu — bấm <kbd>Esc</kbd> để tắt
        </p>
      )}
    </div>,
    document.body,
  );
}
