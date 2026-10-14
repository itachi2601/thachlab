"use client";

import { useCallback, useEffect, useState } from "react";
import { NotebookPen } from "lucide-react";
import PresenterNoteBox from "@/components/lessons/PresenterNoteBox";

export interface LessonNoteContext {
  itemId: number | null;
  pageKey: string;
  pageHeading: string;
}

/**
 * Nút + phím N ghi chú nhanh ngay trên trang bài học (lý thuyết, bài tập mẫu, luyện tập…) khi thầy
 * dạy không bật chế độ trình chiếu. Dùng chung hộp ghi chú với trình chiếu (PresenterNoteBox).
 * `getContext` được gọi LÚC MỞ hộp để chụp đúng mục/dạng đang nằm trong tầm mắt.
 * Chỉ render cho giáo viên/trợ giảng (trang quyết định), học sinh không thấy.
 */
export default function LessonNoteFab({
  lessonId,
  getContext,
}: {
  lessonId: number;
  getContext: () => LessonNoteContext;
}) {
  const [ctx, setCtx] = useState<LessonNoteContext | null>(null);
  const [saved, setSaved] = useState(false);

  const open = useCallback(() => setCtx(getContext()), [getContext]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key !== "n" && e.key !== "N") return;
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.tagName === "SELECT" || t.isContentEditable)) return;
      // Đang bật chế độ trình chiếu thì trình chiếu tự lo phím N (lớp phủ có hộp ghi chú riêng).
      if (document.querySelector(".lesson-presenter")) return;
      e.preventDefault();
      open();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <div className="lesson-note-float">
      {!ctx && (
        <button type="button" className="lesson-note-fab" onClick={open} title="Ghi chú nhanh cho mục đang xem (N)">
          <NotebookPen size={16} aria-hidden />
          <span>Ghi chú</span>
        </button>
      )}
      {ctx && (
        <PresenterNoteBox
          lessonId={lessonId}
          itemId={ctx.itemId}
          pageKey={ctx.pageKey}
          pageHeading={ctx.pageHeading}
          onClose={(didSave) => {
            setCtx(null);
            if (didSave) {
              setSaved(true);
              window.setTimeout(() => setSaved(false), 1800);
            }
          }}
        />
      )}
      {saved && <p className="presenter-note-saved" role="status">Đã ghi chú</p>}
    </div>
  );
}
