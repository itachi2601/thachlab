"use client";

import { useCallback, useEffect, useRef, useState, type CSSProperties, type PointerEvent as ReactPointerEvent } from "react";
import { Eraser, Highlighter, Pen, Trash2, Undo2 } from "lucide-react";

/**
 * components/lessons/presenter-ink.tsx — BÚT VẼ DÙNG CHUNG cho các màn trình chiếu (23/11/2026).
 *
 * Tách từ LessonPresenter (bút / dạ quang / tẩy / bỏ nét / xoá trang) để trình chiếu bài tập mẫu dùng cùng một cách vẽ,
 * cùng phím (D H E Z C) và cùng lớp CSS toàn cục `.presenter-canvas`, `.presenter-colors` trong globals.css.
 * Nét lưu theo `pageKey` (mỗi trang/dạng một tập nét), toạ độ chuẩn hoá 0..1 nên đổi cỡ cửa sổ không lệch.
 * LessonPresenter vẫn giữ bản riêng của nó — chuyển sang module này khi có dịp sửa file đó (tránh giẫm phiên khác).
 */

export type PenMode = "off" | "pen" | "marker" | "eraser";

/** Màu bút — đỏ để khoanh ý chính, xanh để bổ sung, lục để đánh dấu đúng; vàng là bút dạ quang. */
export const PEN_COLORS = [
  { value: "#ef4444", label: "Đỏ" },
  { value: "#2563eb", label: "Xanh" },
  { value: "#16a34a", label: "Lục" },
];
export const MARKER_COLOR = "#facc15";

interface Stroke {
  mode: "pen" | "marker";
  color: string;
  /** Độ dày tính bằng px màn hình — giữ nguyên khi phóng to chữ để nét vẽ vẫn rõ. */
  width: number;
  /** Toạ độ chuẩn hoá 0..1 so với khung vẽ. */
  points: Array<[number, number]>;
}

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
    ctx.beginPath();
    ctx.arc(points[0][0] * w, points[0][1] * h, stroke.width / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    return;
  }
  ctx.beginPath();
  points.forEach(([x, y], i) => {
    if (i === 0) ctx.moveTo(x * w, y * h);
    else ctx.lineTo(x * w, y * h);
  });
  ctx.stroke();
  ctx.restore();
}

export function penLabelOf(pen: PenMode) {
  return pen === "pen" ? "Bút" : pen === "marker" ? "Dạ quang" : pen === "eraser" ? "Tẩy" : "Bút vẽ";
}

/** Trạng thái + thao tác bút cho một màn chiếu. `pageKey` đổi → canvas vẽ tập nét của trang mới. */
export function usePresenterInk(pageKey: string) {
  const [pen, setPen] = useState<PenMode>("off");
  const [color, setColor] = useState(PEN_COLORS[0].value);
  const [drawHint, setDrawHint] = useState(false);
  const [counts, setCounts] = useState<Record<string, number>>({});
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const strokesRef = useRef(new Map<string, Stroke[]>());
  const liveRef = useRef<Stroke | null>(null);
  const hintTimerRef = useRef<number | null>(null);

  const sync = useCallback((key: string) => {
    setCounts((c) => ({ ...c, [key]: strokesRef.current.get(key)?.length ?? 0 }));
  }, []);

  const repaint = useCallback(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return;
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
    for (const s of strokesRef.current.get(pageKey) ?? []) paintStroke(ctx, s, w, h);
    if (liveRef.current) paintStroke(ctx, liveRef.current, w, h);
  }, [pageKey]);

  useEffect(() => {
    repaint();
  }, [repaint, counts]);

  useEffect(() => {
    window.addEventListener("resize", repaint);
    window.addEventListener("orientationchange", repaint);
    return () => {
      window.removeEventListener("resize", repaint);
      window.removeEventListener("orientationchange", repaint);
    };
  }, [repaint]);

  useEffect(
    () => () => {
      if (hintTimerRef.current) window.clearTimeout(hintTimerRef.current);
    },
    [],
  );

  function pointFrom(e: ReactPointerEvent<HTMLCanvasElement>): [number, number] {
    const r = e.currentTarget.getBoundingClientRect();
    return [(e.clientX - r.left) / Math.max(1, r.width), (e.clientY - r.top) / Math.max(1, r.height)];
  }

  function eraseAt([x, y]: [number, number]) {
    const canvas = canvasRef.current;
    const list = strokesRef.current.get(pageKey);
    if (!canvas || !list?.length) return;
    const w = canvas.clientWidth || 1;
    const h = canvas.clientHeight || 1;
    const kept = list.filter((s) => !s.points.some(([sx, sy]) => Math.hypot(sx * w - x * w, sy * h - y * h) < 16));
    if (kept.length === list.length) return;
    strokesRef.current.set(pageKey, kept);
    sync(pageKey);
  }

  const canvasProps = {
    ref: canvasRef,
    className: `presenter-canvas ${pen !== "off" ? "is-active" : ""}`,
    onPointerDown(e: ReactPointerEvent<HTMLCanvasElement>) {
      if (pen === "off") return;
      e.currentTarget.setPointerCapture(e.pointerId);
      const p = pointFrom(e);
      if (pen === "eraser") return eraseAt(p);
      liveRef.current = { mode: pen, color: pen === "marker" ? MARKER_COLOR : color, width: pen === "marker" ? 16 : 3, points: [p] };
      repaint();
    },
    onPointerMove(e: ReactPointerEvent<HTMLCanvasElement>) {
      if (pen === "off") return;
      const p = pointFrom(e);
      if (pen === "eraser") {
        if (e.buttons !== 0) eraseAt(p);
        return;
      }
      const live = liveRef.current;
      if (!live) return;
      const last = live.points[live.points.length - 1];
      if (Math.abs(p[0] - last[0]) + Math.abs(p[1] - last[1]) < 0.0015) return;
      live.points.push(p);
      repaint();
    },
    onPointerUp() {
      const live = liveRef.current;
      if (!live) return;
      liveRef.current = null;
      strokesRef.current.set(pageKey, [...(strokesRef.current.get(pageKey) ?? []), live]);
      sync(pageKey);
    },
    onPointerCancel() {
      canvasProps.onPointerUp();
    },
  };

  const undo = useCallback(() => {
    const list = strokesRef.current.get(pageKey);
    if (!list?.length) return;
    strokesRef.current.set(pageKey, list.slice(0, -1));
    sync(pageKey);
  }, [pageKey, sync]);

  const clear = useCallback(() => {
    if (!strokesRef.current.get(pageKey)?.length) return;
    strokesRef.current.set(pageKey, []);
    sync(pageKey);
  }, [pageKey, sync]);

  /** Nhắc "đang bật bút" tự tắt sau 4,5 s: thường trực thì che chữ ở đáy màn chiếu. */
  const setPenMode = useCallback((next: PenMode) => {
    setPen(next);
    if (hintTimerRef.current) window.clearTimeout(hintTimerRef.current);
    setDrawHint(next !== "off");
    if (next !== "off") hintTimerRef.current = window.setTimeout(() => setDrawHint(false), 4500);
  }, []);

  /** Phím bút chung (D H E Z C). Trả về true nếu đã xử lý. */
  const handleKey = useCallback(
    (key: string) => {
      const k = key.toLowerCase();
      if (k === "d") setPenMode(pen === "pen" ? "off" : "pen");
      else if (k === "h") setPenMode(pen === "marker" ? "off" : "marker");
      else if (k === "e") setPenMode(pen === "eraser" ? "off" : "eraser");
      else if (k === "z") undo();
      else if (k === "c") clear();
      else return false;
      return true;
    },
    [pen, setPenMode, undo, clear],
  );

  return { pen, setPenMode, color, setColor, drawHint, hasStrokes: (counts[pageKey] ?? 0) > 0, undo, clear, handleKey, canvasProps };
}

export type PresenterInk = ReturnType<typeof usePresenterInk>;

/** Nhóm nút bút trên thanh dưới (đặt trong `.presenter-bar`). */
export function PresenterInkTools({ ink }: { ink: PresenterInk }) {
  const { pen, setPenMode, color, setColor, hasStrokes, undo, clear } = ink;
  return (
    <>
      <button type="button" className={pen === "pen" ? "is-on" : ""} onClick={() => setPenMode(pen === "pen" ? "off" : "pen")} title="Bút vẽ — khoanh ý chính (D)" aria-pressed={pen === "pen"}>
        <Pen size={15} aria-hidden />
        <span className="presenter-btn-text">Bút vẽ</span>
      </button>
      <button type="button" className={pen === "marker" ? "is-on" : ""} onClick={() => setPenMode(pen === "marker" ? "off" : "marker")} title="Bút dạ quang vàng (H)" aria-pressed={pen === "marker"} aria-label="Dạ quang">
        <Highlighter size={15} aria-hidden />
      </button>
      <button type="button" className={pen === "eraser" ? "is-on" : ""} onClick={() => setPenMode(pen === "eraser" ? "off" : "eraser")} title="Tẩy nét (E)" aria-pressed={pen === "eraser"} aria-label="Tẩy">
        <Eraser size={15} aria-hidden />
      </button>
      {pen === "pen" && (
        <span className="presenter-colors" role="group" aria-label="Màu bút">
          {PEN_COLORS.map((o) => (
            <button
              key={o.value}
              type="button"
              className={color === o.value ? "is-current" : ""}
              style={{ "--dot": o.value } as CSSProperties}
              onClick={() => setColor(o.value)}
              title={`Màu ${o.label}`}
              aria-label={`Màu ${o.label}`}
              aria-pressed={color === o.value}
            />
          ))}
        </span>
      )}
      {hasStrokes && (
        <>
          <button type="button" onClick={undo} title="Bỏ nét vừa vẽ (Z)" aria-label="Bỏ nét vừa vẽ">
            <Undo2 size={15} aria-hidden />
          </button>
          <button type="button" onClick={clear} title="Xoá hết nét ở dạng này (C)" aria-label="Xoá hết nét">
            <Trash2 size={15} aria-hidden />
          </button>
        </>
      )}
    </>
  );
}
