"use client";

import { useState } from "react";
import { Flag, X } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import Button from "@/components/ui/Button";
import { useToast } from "@/components/ui/Toast";

/**
 * Nút nhỏ "Báo lỗi câu này" — chỉ hiện lúc xem lại bài làm (đã có đáp án đúng để
 * so sánh). Khác BugReportWidget (nút nổi báo lỗi chung toàn trang): gắn kèm
 * exam_id + question_index để admin nhảy thẳng vào đúng câu ở /quan-tri/sua-de,
 * không phải tự dò trong đề.
 */
export default function ReportQuestionButton({ examId, questionIndex }: { examId: number; questionIndex: number }) {
  const { session } = useAuth();
  const toast = useToast();
  const [open, setOpen] = useState(false);
  const [description, setDescription] = useState("");
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!description.trim()) return;
    setBusy(true);
    setError("");
    try {
      const { submitBugReport } = await import("@/services/bug-reports");
      await submitBugReport({
        description,
        category: "cau_hoi",
        pageUrl: window.location.pathname + window.location.search + window.location.hash,
        userId: session?.user.id ?? null,
        examId,
        questionIndex,
      });
      toast("success", "Đã gửi, thầy sẽ xem lại câu này!");
      setSent(true);
      setOpen(false);
      setDescription("");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không gửi được, thử lại sau.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        disabled={sent}
        className="inline-flex items-center gap-1.5 rounded-full border border-line px-3 py-1.5 text-xs font-semibold text-muted hover:border-amber-400/50 hover:text-amber-300 disabled:cursor-default disabled:opacity-60"
      >
        <Flag size={13} />
        {sent ? "Đã báo lỗi câu này" : "Báo lỗi câu này"}
      </button>

      {open && (
        <div className="fixed inset-0 z-50 grid place-items-center bg-black/60 p-4" onClick={() => !busy && setOpen(false)}>
          <section
            role="dialog"
            aria-modal="true"
            aria-label="Báo lỗi câu hỏi"
            className="w-full max-w-md rounded-2xl border border-line bg-panel p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between">
              <h2 className="flex items-center gap-2 text-lg font-bold text-ink">
                <Flag size={18} className="text-amber-300" />
                Báo lỗi câu {questionIndex + 1}
              </h2>
              <button type="button" onClick={() => setOpen(false)} className="text-muted hover:text-primary">
                <X size={20} />
              </button>
            </div>
            <form onSubmit={submit} className="mt-4 space-y-3">
              <textarea
                required
                autoFocus
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Em nghĩ đáp án/lời giải câu này sai ở đâu, hoặc câu bị lỗi gì?"
                rows={4}
                className="w-full rounded-xl border border-line-strong bg-surface-2 px-4 py-2.5 text-sm text-ink placeholder:text-slate-500 focus:border-primary focus:outline-none"
              />
              {error && <p className="text-sm text-red-400">{error}</p>}
              <Button type="submit" disabled={busy || !description.trim()} className="w-full">
                {busy ? "Đang gửi…" : "Gửi"}
              </Button>
            </form>
          </section>
        </div>
      )}
    </>
  );
}
