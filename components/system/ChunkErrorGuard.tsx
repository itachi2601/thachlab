"use client";

/**
 * components/system/ChunkErrorGuard.tsx
 *
 * Lưới an toàn CAO HƠN cả React Error Boundary (LazyErrorBoundary, app/error.tsx).
 *
 * Bối cảnh: khi 1 chunk JS runtime của Turbopack tải lỗi (mạng chập chờn, hoặc
 * hosting vừa deploy bản mới nên chunk cũ theo hash đã bị xoá), lỗi `ChunkLoadError`
 * đôi khi xảy ra NGAY TRONG cơ chế nạp chunk của Turbopack runtime (`Promise.all`
 * bên trong `turbopack-*.js`) — xem `perf4/RESULT.md` §6 và ghi chú "GIỚI HẠN" trong
 * `components/ui/LazyErrorBoundary.tsx`. Trong trường hợp đó lỗi KHÔNG đi qua đường
 * `getDerivedStateFromError` của bất kỳ React Error Boundary nào (kể cả boundary bọc
 * đúng vị trí) mà nổi thẳng lên thành `window.onerror`/`unhandledrejection` — nằm
 * ngoài tầm với của `LazyErrorBoundary` và `app/error.tsx` (cả hai đều là React Error
 * Boundary, chỉ bắt được lỗi ném ra TRONG lúc React render/commit).
 *
 * Thực nghiệm khi vá lại đợt này (27/9/2026, build từ `dd9bd74e`): xoá thử chunk
 * RevealMotion (3 cách: chunk component nhỏ, 1 trong 2 bản chunk framer-motion trùng,
 * và cả 3 cùng lúc) không còn tái hiện được màn trắng — `LazyErrorBoundary` cục bộ
 * trong `Reveal.tsx` đã bắt đúng ở build hiện tại (khớp phần "ĐỢT SAU" của
 * `perf4/RESULT.md`, viết cùng ngày, ghi nhận kết quả ngược với ghi chú "GIỚI HẠN" cũ
 * hơn). Vì hành vi này được chính `perf4/RESULT.md` ghi nhận là KHÔNG ổn định giữa các
 * lần build/tuỳ thời điểm lỗi xảy ra trong tiến trình hydrate, lớp này vẫn được thêm
 * làm lưới dự phòng cho các trường hợp: (a) một `next/dynamic()`/`lazy()` mới thêm
 * sau này quên bọc `LazyErrorBoundary`, (b) đúng kịch bản lỗi nổi ra ngoài React như
 * `perf4/RESULT.md` §6 đã quan sát được trên build khác.
 *
 * Cách nhận diện: message lỗi thực tế quan sát được khi giả lập (xoá chunk trong
 * `out/_next/static/chunks/`, xem console) đều có dạng:
 *   "ChunkLoadError: Failed to load chunk /_next/static/chunks/<hash>.js from module <id>"
 * → khớp cả 2 chuỗi con "ChunkLoadError" và "Failed to load chunk". Giữ thêm
 * "Loading chunk" (cách webpack cũ dùng, phòng khi runtime đổi) và "Failed to fetch
 * dynamically imported module" (thông điệp gốc của trình duyệt cho `import()` lỗi ở
 * Firefox/Safari khi lỗi không đi qua wrapper ChunkLoadError của bundler) — không đoán
 * thêm pattern nào khác ngoài những gì đã thấy thực tế hoặc là biến thể đã biết rõ của
 * đúng loại lỗi này.
 *
 * Xử lý: reload trang ĐÚNG MỘT LẦN (đánh dấu bằng `sessionStorage`, tự hết khi đóng tab
 * — mỗi phiên duyệt mới lại được thử reload 1 lần). Nếu đã reload rồi mà lỗi vẫn xảy ra
 * (mạng vẫn đứt, hosting vẫn thiếu file) → để nó rơi xuống `app/error.tsx` bình thường,
 * KHÔNG tự xử lý tiếp, không bao giờ im lặng/trắng trang.
 */

import { useEffect } from "react";

const RELOAD_FLAG = "thachlab-chunk-reload";

const CHUNK_ERROR_PATTERNS = [
  "ChunkLoadError",
  "Failed to load chunk",
  "Loading chunk",
  "Failed to fetch dynamically imported module",
];

function isChunkLoadError(message: unknown): boolean {
  if (typeof message !== "string" || message.length === 0) return false;
  return CHUNK_ERROR_PATTERNS.some((pattern) => message.includes(pattern));
}

function reloadOnce() {
  try {
    if (sessionStorage.getItem(RELOAD_FLAG)) {
      // Đã reload 1 lần trong phiên tab này rồi mà lỗi vẫn còn — không lặp lại,
      // để app/error.tsx (nếu lỗi lọt vào React) hoặc chính trang lỗi hiện tại xử lý.
      return;
    }
    sessionStorage.setItem(RELOAD_FLAG, "1");
  } catch {
    // sessionStorage có thể bị chặn (chế độ ẩn danh nghiêm ngặt, cookie bị tắt…) —
    // không có cách nào đánh dấu "đã reload" thì thà không tự reload còn hơn lặp vô hạn.
    return;
  }
  window.location.reload();
}

export default function ChunkErrorGuard() {
  useEffect(() => {
    function onError(event: ErrorEvent) {
      const message = event.error instanceof Error ? event.error.message : event.message;
      if (isChunkLoadError(message)) {
        reloadOnce();
      }
    }

    function onRejection(event: PromiseRejectionEvent) {
      const reason = event.reason;
      const message =
        reason instanceof Error ? reason.message : typeof reason === "string" ? reason : "";
      if (isChunkLoadError(message)) {
        reloadOnce();
      }
    }

    window.addEventListener("error", onError);
    window.addEventListener("unhandledrejection", onRejection);
    return () => {
      window.removeEventListener("error", onError);
      window.removeEventListener("unhandledrejection", onRejection);
    };
  }, []);

  return null;
}
