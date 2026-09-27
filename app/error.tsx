"use client";

/**
 * app/error.tsx
 *
 * Lưới an toàn cuối cùng — bắt các lỗi KHÔNG bị chặn bởi
 * components/ui/LazyErrorBoundary.tsx ở những chỗ đã biết (Reveal, QuestionSlide,
 * FormulaPanel…), ví dụ một next/dynamic()/lazy() khác thêm sau này quên bọc
 * error boundary. Không có file này thì Next dùng trang lỗi mặc định (tiếng Anh,
 * thay hẳn cả layout gốc — mất luôn header/nav) — file này giữ layout gốc, hiện
 * thông báo tiếng Việt và cho học sinh tự tải lại.
 *
 * Không dùng unstable_retry() làm nút chính: với lỗi tải chunk (ChunkLoadError),
 * React.lazy() cache trạng thái "rejected" ở cấp module — retry chỉ render lại,
 * không fetch lại chunk, nên sẽ ném lại đúng lỗi cũ ngay lập tức. Tải lại trang
 * (reload) mới thực sự lấy lại danh sách chunk mới nhất từ server.
 */

import { useEffect } from "react";

export default function Error({
  error,
}: {
  error: Error & { digest?: string };
  unstable_retry: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 px-6 text-center">
      <p className="font-mono text-xs uppercase tracking-widest text-cyan-500">Có lỗi xảy ra</p>
      <h1 className="text-2xl font-bold text-ink">Trang tải chưa xong</h1>
      <p className="max-w-sm text-sm text-muted">
        Có thể do mạng chập chờn. Thử tải lại trang — nếu vẫn lỗi, báo cho thầy Thạch giúp em.
      </p>
      <button
        type="button"
        onClick={() => window.location.reload()}
        className="mt-2 rounded-full bg-cyan-500 px-6 py-2.5 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
      >
        Tải lại trang
      </button>
    </div>
  );
}
