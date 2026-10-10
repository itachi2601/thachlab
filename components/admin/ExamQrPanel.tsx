"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Check, Copy, Download, Maximize2, Minimize2, X } from "lucide-react";
import { makeQrCode, QR_QUIET_ZONE as QUIET } from "@/lib/qr";
import { examQrUrl } from "@/lib/exam-link";

/**
 * components/admin/ExamQrPanel.tsx
 *
 * Khối "Mã QR của đề" + chế độ CHIẾU LÊN BẢNG, dùng ở trang soạn đề
 * (`/quan-tri/sua-de` và `/quan-tri/dang-de`).
 *
 * Vì sao có: thầy soạn đề trên máy tính rồi chiếu mã QR lên tivi/máy chiếu; học sinh quét
 * bằng điện thoại là vào ĐÚNG đề đó trên thachlab — không phải gõ link, không phải chép
 * mã đề lên bảng.
 *
 * Quy tắc thiết kế (docs/QUY-TAC-THIET-KE.md) — trang quản trị nền tối, nhưng mã QR và
 * màn chiếu là thứ HỌC SINH nhìn:
 *  - M5: QR nền trắng nằm giữa giao diện tối → luôn bọc trong khung sáng có đệm, không dán
 *    ô trắng trần lên nền đen (loá cục bộ).
 *  - M1: màn chiếu nền sáng chữ tối (positive polarity) — máy chiếu rõ hơn, và máy ảnh chỉ
 *    đọc được QR trên nền sáng.
 *  - B2: trên màn chiếu chỉ có MỘT điểm nổi bật là mã QR; mã đề và tiêu đề hạ cấp thành chữ.
 *  - D2: nút trong trang quản trị ≥ 44px, nhãn một dòng.
 *  - B4: không hoạt hình lặp, không hiệu ứng tự chạy.
 *
 * Kỹ thuật: sinh QR ngay trên máy bằng `qrcode-generator` (cùng gói mà bản in sách dùng ở
 * `book/`) — không gọi dịch vụ ngoài, không thêm request, không cần server (web xuất tĩnh).
 */

/** Mã QR vẽ bằng SVG: một <path> đen trên nền trắng, co giãn theo khung cha. */
function QrSvg({ text, label, style }: { text: string; label: string; style?: React.CSSProperties }) {
  const { d, count } = useMemo(() => makeQrCode(text), [text]);
  const box = count + QUIET * 2;
  return (
    <svg
      viewBox={`${-QUIET} ${-QUIET} ${box} ${box}`}
      style={{ display: "block", width: "100%", height: "100%", ...style }}
      shapeRendering="crispEdges"
      role="img"
      aria-label={label}
    >
      <rect x={-QUIET} y={-QUIET} width={box} height={box} fill="#ffffff" />
      <path d={d} fill="#000000" />
    </svg>
  );
}

/** Lưu QR thành ảnh PNG để dán vào slide/đề in — không cần mạng, vẽ bằng canvas. */
function downloadPng(text: string, filename: string) {
  const { count, isDark } = makeQrCode(text);
  const scale = Math.max(4, Math.floor(1200 / (count + QUIET * 2)));
  const side = (count + QUIET * 2) * scale;
  const canvas = document.createElement("canvas");
  canvas.width = side;
  canvas.height = side;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, side, side);
  ctx.fillStyle = "#000000";
  for (let r = 0; r < count; r += 1) {
    for (let c = 0; c < count; c += 1) {
      if (isDark(r, c)) ctx.fillRect((c + QUIET) * scale, (r + QUIET) * scale, scale, scale);
    }
  }
  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }, "image/png");
}

/** Màn chiếu toàn màn hình: nền trắng, QR lớn, mã đề lớn — để cả lớp quét từ xa. */
function ProjectionBoard({
  examId,
  title,
  meta,
  url,
  onClose,
}: {
  examId: number;
  title?: string;
  meta?: string;
  url: string;
  onClose: () => void;
}) {
  const rootRef = useRef<HTMLDivElement | null>(null);
  const [full, setFull] = useState(false);

  const toggleFull = useCallback(() => {
    if (document.fullscreenElement) void document.exitFullscreen?.().catch(() => undefined);
    else void rootRef.current?.requestFullscreen?.().catch(() => undefined);
  }, []);

  useEffect(() => {
    void rootRef.current?.requestFullscreen?.().catch(() => undefined);
    const onFs = () => setFull(!!document.fullscreenElement);
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("fullscreenchange", onFs);
    window.addEventListener("keydown", onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("fullscreenchange", onFs);
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = prevOverflow;
      if (document.fullscreenElement) void document.exitFullscreen?.().catch(() => undefined);
    };
  }, [onClose]);

  return createPortal(
    <div
      ref={rootRef}
      className="fixed inset-0 z-[200] flex flex-col items-center justify-center gap-[2.5vh] bg-white px-6 py-8 text-[#0b1220]"
      role="dialog"
      aria-modal="true"
      aria-label={`Mã QR của đề ${examId}`}
    >
      <div className="absolute right-4 top-4 flex items-center gap-2">
        <button
          type="button"
          onClick={toggleFull}
          className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-slate-300 text-slate-600 hover:border-slate-500"
          aria-label={full ? "Thoát toàn màn hình" : "Toàn màn hình"}
          title={full ? "Thoát toàn màn hình" : "Toàn màn hình"}
        >
          {full ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
        </button>
        <button
          type="button"
          onClick={onClose}
          className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-slate-300 text-slate-600 hover:border-slate-500"
          aria-label="Đóng màn chiếu"
          title="Đóng (Esc)"
        >
          <X size={20} />
        </button>
      </div>

      <p className="text-[clamp(12px,1.4vw,20px)] font-semibold uppercase tracking-[0.3em] text-slate-400">
        ThachLab · Vật lí
      </p>

      {/* B2: một điểm nổi bật duy nhất là mã QR. */}
      <div
        className="shrink-0 rounded-3xl border-[6px] border-slate-900 bg-white p-[1.5vh]"
        style={{ width: "min(52vh, 46vw)", height: "min(52vh, 46vw)" }}
      >
        <QrSvg text={url} label={`Mã QR mở đề ${examId} trên ThachLab`} />
      </div>

      <h2 className="font-display text-[clamp(34px,7vw,120px)] font-extrabold leading-none">Đề #{examId}</h2>
      {title && (
        <p className="max-w-[92vw] text-center text-[clamp(16px,2.2vw,38px)] font-semibold text-slate-700">{title}</p>
      )}
      {meta && <p className="text-[clamp(13px,1.5vw,22px)] text-slate-500">{meta}</p>}

      <p className="text-center text-[clamp(13px,1.4vw,20px)] text-slate-500">
        Quét mã bằng camera điện thoại để mở đúng đề này trên thachlab
      </p>
    </div>,
    document.body,
  );
}

export default function ExamQrPanel({
  examId,
  title,
  meta,
  hint,
}: {
  examId: number;
  /** Tiêu đề đề — hiện dưới mã đề trên màn chiếu. */
  title?: string;
  /** Dòng phụ trên màn chiếu, ví dụ "12 câu · 45 phút · Lớp 12A1". */
  meta?: string;
  /** Dòng nhắc riêng của trang gọi (ví dụ nhắc đăng đề xong mới chiếu được). */
  hint?: string;
}) {
  const url = useMemo(() => examQrUrl(examId), [examId]);
  const [copied, setCopied] = useState(false);
  const [projecting, setProjecting] = useState(false);

  useEffect(() => {
    if (!copied) return;
    const timer = setTimeout(() => setCopied(false), 2000);
    return () => clearTimeout(timer);
  }, [copied]);

  const copy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
    } catch {
      // Trình duyệt chặn clipboard (không phải HTTPS, hoặc thiếu quyền): chọn sẵn link để thầy chép tay.
      window.prompt("Chép link này:", url);
    }
  }, [url]);

  return (
    <section className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="flex flex-wrap items-start gap-4">
        {/* M5: khung sáng có đệm đều quanh mã — không dán ô trắng trần lên nền tối. */}
        <div className="shrink-0 rounded-xl bg-white p-3" style={{ width: 148, height: 148 }}>
          <QrSvg text={url} label={`Mã QR mở đề ${examId}`} />
        </div>

        <div className="min-w-0 flex-1 basis-64 space-y-3">
          <div>
            <h3 className="admin-h2">Mã QR của đề #{examId}</h3>
            <p className="mt-1 text-xs text-slate-400">
              Học sinh quét mã này là vào đúng đề, không phải gõ link. Mở “Chiếu lên bảng” rồi kéo sang máy
              chiếu/tivi cho cả lớp quét.
            </p>
            {hint && <p className="mt-1 text-xs text-amber-300/90">{hint}</p>}
          </div>

          <p className="break-all rounded-lg border border-white/10 bg-black/30 px-2 py-1.5 font-mono text-[11px] text-slate-400">
            {url}
          </p>

          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={() => setProjecting(true)}
              className="inline-flex min-h-11 items-center gap-2 rounded-full bg-primary px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark"
            >
              <Maximize2 size={16} /> Chiếu lên bảng
            </button>
            <button type="button" onClick={copy} className="admin-chip inline-flex min-h-11 items-center gap-2 px-4">
              {copied ? <Check size={15} /> : <Copy size={15} />} {copied ? "Đã chép" : "Sao chép link"}
            </button>
            <button
              type="button"
              onClick={() => downloadPng(url, `qr-de-${examId}.png`)}
              className="admin-chip inline-flex min-h-11 items-center gap-2 px-4"
            >
              <Download size={15} /> Tải ảnh QR
            </button>
          </div>
        </div>
      </div>

      {projecting && (
        <ProjectionBoard
          examId={examId}
          title={title}
          meta={meta}
          url={url}
          onClose={() => setProjecting(false)}
        />
      )}
    </section>
  );
}
