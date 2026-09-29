"use client";

import { useEffect, useState } from "react";

// Khớp với thời lượng transition CSS bên dưới (panel .18s là hiệu ứng dài nhất) —
// giữ node trong DOM đủ lâu để hiệu ứng đóng chạy xong trước khi gỡ hẳn.
const CLOSE_MS = 180;

/**
 * Hộp thoại giữa màn hình dùng chung — thay cho confirm()/alert() của trình duyệt.
 * Trước dùng framer-motion (AnimatePresence + motion.div) cho hiệu ứng mở/đóng;
 * nay đổi sang CSS transition thuần để không kéo framer-motion (~140 KB) vào JS
 * ban đầu của các trang có dùng Modal (qua ConfirmDialog) — hành vi hiển thị
 * giữ nguyên: mờ dần + phóng to nhẹ lúc mở, ngược lại lúc đóng.
 */
export default function Modal({
  open,
  onClose,
  children,
}: {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  const [prevOpen, setPrevOpen] = useState(open);
  const [closing, setClosing] = useState(false);
  const [entered, setEntered] = useState(false);

  // Cập nhật NGAY trong lúc render khi prop `open` đổi — theo đúng cách React khuyến
  // nghị để "điều chỉnh state theo prop" mà không cần setState đồng bộ trong effect
  // (xem "Adjusting state when a prop changes" trong tài liệu React). `entered` tắt
  // ngay để: (a) lúc mở, node vừa mount ở đúng style ẩn ban đầu rồi effect bên dưới
  // mới bật lại qua requestAnimationFrame — trình duyệt mới chạy được transition;
  // (b) lúc đóng, node đang mở chuyển ngay sang style ẩn để transition chạy ngược
  // trong CLOSE_MS trước khi bị gỡ khỏi DOM.
  if (open !== prevOpen) {
    setPrevOpen(open);
    setClosing(!open);
    setEntered(false);
  }

  const mounted = open || closing;

  useEffect(() => {
    if (!open) return;
    const raf = requestAnimationFrame(() => setEntered(true));
    return () => cancelAnimationFrame(raf);
  }, [open]);

  useEffect(() => {
    if (!closing) return;
    const timer = window.setTimeout(() => setClosing(false), CLOSE_MS);
    return () => window.clearTimeout(timer);
  }, [closing]);

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!mounted) return null;

  return (
    <div
      className={`fixed inset-0 z-100 flex items-center justify-center bg-black/60 px-4 backdrop-blur-sm transition-opacity duration-150 motion-reduce:transition-none ${
        entered ? "opacity-100" : "opacity-0"
      }`}
      onClick={onClose}
      role="presentation"
    >
      <div
        className={`w-full max-w-sm rounded-2xl border border-white/10 bg-panel p-6 shadow-2xl transition-[opacity,transform] duration-[180ms] ease-out motion-reduce:transition-none ${
          entered ? "translate-y-0 scale-100 opacity-100" : "translate-y-2 scale-[0.94] opacity-0"
        }`}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        {children}
      </div>
    </div>
  );
}
