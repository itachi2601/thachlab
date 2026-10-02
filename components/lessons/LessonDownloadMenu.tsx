"use client";

import { useEffect, useRef, useState } from "react";
import { ChevronDown, Download, FileText, Printer } from "lucide-react";
import type { LessonItem } from "@/features/lessons/types";
import { exportLessonAsDocx, exportLessonAsLatex, lessonHasDownloadableContent } from "@/services/lesson-export";

/**
 * Tải ngược Lý thuyết + Bài tập mẫu của bài học về Word/LaTeX/PDF — chiều ngược
 * của skill dang-bai-hoc-thachlab. Không hiện nút nếu bài chưa có nội dung để tải
 * (chỉ có video/đề thì không có gì để xuất).
 */
export default function LessonDownloadMenu({
  lessonTitle,
  chapterTitle,
  items,
  onPrint,
}: {
  lessonTitle: string;
  chapterTitle: string;
  items: LessonItem[];
  onPrint: () => void;
}) {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState<"" | "docx" | "tex">("");
  const [err, setErr] = useState("");
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open]);

  if (!lessonHasDownloadableContent(items)) return null;

  async function handle(kind: "docx" | "tex" | "pdf") {
    setErr("");
    setOpen(false);
    if (kind === "pdf") {
      onPrint();
      return;
    }
    setBusy(kind);
    try {
      if (kind === "docx") await exportLessonAsDocx(lessonTitle, chapterTitle, items);
      else exportLessonAsLatex(lessonTitle, chapterTitle, items);
    } catch {
      setErr("Không tải được file — thử lại hoặc dùng trình duyệt khác (Chrome/Edge/Safari bản mới).");
    } finally {
      setBusy("");
    }
  }

  return (
    <div className="lesson-download" ref={rootRef}>
      <button
        type="button"
        className="lesson-btn-ghost lesson-download-toggle"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
      >
        <Download size={15} /> Tải bài học <ChevronDown size={14} className={open ? "rotate-180" : ""} />
      </button>
      {open && (
        <div className="lesson-download-menu">
          <button type="button" onClick={() => handle("docx")} disabled={busy !== ""}>
            <FileText size={14} /> {busy === "docx" ? "Đang dựng file…" : "Word (.docx)"}
          </button>
          <button type="button" onClick={() => handle("tex")} disabled={busy !== ""}>
            <FileText size={14} /> LaTeX (.tex)
          </button>
          <button type="button" onClick={() => handle("pdf")} disabled={busy !== ""}>
            <Printer size={14} /> In / Lưu PDF
          </button>
        </div>
      )}
      {err && <p className="lesson-download-error">{err}</p>}
    </div>
  );
}
