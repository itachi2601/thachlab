"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Maximize2, Minimize2, X } from "lucide-react";
import { makeQrCode, QR_QUIET_ZONE as QUIET } from "@/lib/qr";
import { examQrUrl } from "@/lib/exam-link";

/**
 * components/exams/ExamQrOverlay.tsx — màn chiếu mã QR của MỘT đề, mở từ nút "Mã QR"
 * ngay trong trang bài học (`components/exams/ExamQrButton.tsx`).
 *
 * Vì sao có: thầy đang chiếu trang bài lên tivi/máy chiếu lúc kiểm tra chương. Bấm nút
 * này là cả màn hình thành mã QR cỡ lớn + số đề, học sinh ở cuối lớp quét được — không
 * phải mở trang quản trị, không phải gõ link.
 *
 * Quy tắc thiết kế (docs/QUY-TAC-THIET-KE.md):
 *  - M1: màn chiếu nền sáng chữ tối (positive polarity) — máy chiếu rõ hơn, camera chỉ
 *    đọc được QR trên nền sáng.
 *  - M5: QR nằm trong khung trắng có đệm đều; vùng trắng quanh mã 4 ô (QUIET) để máy ảnh
 *    bắt được góc.
 *  - B2: trên màn chiếu chỉ có MỘT điểm nổi bật là mã QR; số đề và tiêu đề hạ cấp thành chữ.
 *  - D2: nút đóng/toàn màn hình ≥ 44px.
 *  - B4: không hoạt hình lặp, không hiệu ứng tự chạy.
 *
 * Kỹ thuật: sinh QR ngay trên máy bằng `lib/qr.ts` (cùng hàm mà trang soạn đề dùng) — không
 * gọi dịch vụ ngoài, không thêm request, chạy được với web xuất tĩnh. Cả file này được
 * `next/dynamic` nạp lúc bấm nút nên gói QR không nằm trong JS đầu trang bài.
 */

/** Mã QR vẽ bằng SVG: một <path> đen trên nền trắng, co giãn theo khung cha. */
function QrSvg({ text, label }: { text: string; label: string }) {
  const { d, count } = useMemo(() => makeQrCode(text), [text]);
  const box = count + QUIET * 2;
  return (
    <svg
      viewBox={`${-QUIET} ${-QUIET} ${box} ${box}`}
      style={{ display: "block", width: "100%", height: "100%" }}
      shapeRendering="crispEdges"
      role="img"
      aria-label={label}
    >
      <rect x={-QUIET} y={-QUIET} width={box} height={box} fill="#ffffff" />
      <path d={d} fill="#000000" />
    </svg>
  );
}

export default function ExamQrOverlay({
  examId,
  title,
  onClose,
}: {
  examId: number;
  /** Tiêu đề đề — hiện dưới số đề trên màn chiếu. */
  title?: string;
  onClose: () => void;
}) {
  const url = useMemo(() => examQrUrl(examId), [examId]);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const [full, setFull] = useState(false);

  const toggleFull = useCallback(() => {
    if (document.fullscreenElement) void document.exitFullscreen?.().catch(() => undefined);
    else void rootRef.current?.requestFullscreen?.().catch(() => undefined);
  }, []);

  useEffect(() => {
    // Vào là chiếu luôn cho cả lớp; trình duyệt chặn (không có https, thiếu quyền) thì thôi,
    // nút "Toàn màn hình" vẫn dùng được.
    void rootRef.current?.requestFullscreen?.().catch(() => undefined);

    const onFs = () => setFull(!!document.fullscreenElement);
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
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
        ThachLab · Mã đề
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

      <p className="text-center text-[clamp(13px,1.4vw,20px)] text-slate-500">
        Quét mã bằng camera điện thoại để mở đúng đề này. Không quét được thì vào ThachLab → Quét mã → gõ {examId}.
      </p>
    </div>,
    document.body,
  );
}
