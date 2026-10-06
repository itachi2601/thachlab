"use client";

import Link from "next/link";

/**
 * Trang dự phòng của service worker (public/sw.js): mở một trang chưa từng xem khi mất mạng
 * thì hiện trang này thay vì màn lỗi của trình duyệt. Được cache sẵn ở bước cài SW.
 */
export default function OfflinePage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 px-6 text-center">
      <p className="font-mono text-xs uppercase tracking-widest text-cyan-500">Đang offline</p>
      <h1 className="text-2xl font-bold text-ink">Chưa có mạng</h1>
      <p className="max-w-sm text-sm text-muted">
        Trang này em chưa mở lần nào nên chưa lưu trên máy. Bài em đã xem vẫn đọc lại được. Kết quả luyện tập em làm lúc
        này được giữ trên máy và tự gửi khi có mạng.
      </p>
      <div className="mt-2 flex flex-wrap items-center justify-center gap-3">
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="min-h-11 rounded-full bg-cyan-500 px-6 py-2.5 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
        >
          Thử lại
        </button>
        <Link
          href="/"
          className="inline-flex min-h-11 items-center rounded-full border border-line px-6 text-sm font-semibold text-ink"
        >
          Về trang chủ
        </Link>
      </div>
    </div>
  );
}
