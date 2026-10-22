"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import { QrCode } from "lucide-react";

/**
 * components/exams/ExamQrButton.tsx — nút "Mã QR" cạnh nút Làm bài của mỗi đề kiểm tra
 * trong trang bài học. Bấm là mở màn chiếu QR cỡ lớn (`ExamQrOverlay`), để thầy chiếu lên
 * tivi cho cả lớp quét — học sinh không phải gõ link.
 *
 * Vì sao đặt ngay trong trang bài: lúc kiểm tra chương, thầy đang chiếu đúng trang bài này.
 * Mở thêm trang quản trị chỉ để lấy mã QR là thêm một việc, dễ quên.
 *
 * Phần vẽ QR nằm ở file riêng, nạp bằng `next/dynamic` khi bấm — gói QR không vào JS đầu
 * trang bài (quy tắc tốc độ tải ở AGENTS.md). Nút cao 44px (D2).
 */
const ExamQrOverlay = dynamic(() => import("@/components/exams/ExamQrOverlay"), { ssr: false });

export default function ExamQrButton({ examId, title }: { examId: number; title?: string }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="inline-flex min-h-11 items-center justify-center gap-1.5 rounded-lg border border-line px-3 text-[13px] font-semibold text-ink hover:border-line-strong"
        aria-label={`Mã QR của đề ${examId} — chiếu lên bảng cho cả lớp quét`}
        title="Chiếu mã QR của đề này lên bảng"
      >
        <QrCode size={16} aria-hidden />
        Mã QR
      </button>
      {open && <ExamQrOverlay examId={examId} title={title} onClose={() => setOpen(false)} />}
    </>
  );
}
