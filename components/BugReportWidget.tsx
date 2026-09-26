"use client";

import { useState } from "react";
import Link from "next/link";
import { Bug, Paperclip, X } from "lucide-react";
import { useAuth } from "@/components/auth/auth-context";
import { useToast } from "@/components/ui/Toast";
import { BUG_CATEGORY_LABELS, type BugCategory } from "@/lib/bug-report-labels";
// submitBugReport (services/bug-reports.ts, gọi supabase + services/image-compress) import
// ĐỘNG trong submit() bên dưới — widget này render ở MỌI trang kể cả trang công khai (qua
// PublicShell.tsx); import thẳng ở đây sẽ luôn kéo theo @supabase/supabase-js dù đa số
// người xem chỉ thấy nút nổi, không bao giờ mở form/gửi báo lỗi.

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

export default function BugReportWidget() {
  const { session } = useAuth();
  const toast = useToast();
  const [open, setOpen] = useState(false);
  const [category, setCategory] = useState<BugCategory>("khac");
  const [description, setDescription] = useState("");
  const [reporterName, setReporterName] = useState("");
  const [reporterEmail, setReporterEmail] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  function close() {
    if (busy) return;
    setOpen(false);
    setCategory("khac");
    setDescription("");
    setReporterName("");
    setReporterEmail("");
    setFile(null);
    setError("");
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!description.trim()) return;
    setBusy(true);
    setError("");
    try {
      const { submitBugReport } = await import("@/services/bug-reports");
      await submitBugReport({
        description,
        category,
        pageUrl: window.location.pathname + window.location.search,
        userId: session?.user.id ?? null,
        reporterName: session ? "" : reporterName,
        reporterEmail: session ? "" : reporterEmail,
        file,
      });
      toast("success", "Đã gửi, cảm ơn bạn!");
      close();
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
        className="fixed bottom-5 right-5 z-40 flex items-center gap-2 rounded-full border border-white/15 bg-panel/95 px-4 py-2.5 text-xs font-bold text-slate-200 shadow-xl backdrop-blur-md hover:border-white/30"
      >
        <Bug size={16} className="text-amber-300" />
        Báo lỗi / Góp ý
      </button>

      {open && (
        <div className="fixed inset-0 z-50 grid place-items-center bg-black/60 p-4" onClick={close}>
          <section
            role="dialog"
            aria-modal="true"
            aria-label="Báo lỗi và góp ý"
            className="w-full max-w-md rounded-2xl border border-white/10 bg-panel p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between">
              <h2 className="flex items-center gap-2 text-lg font-bold text-white">
                <Bug size={18} className="text-amber-300" />
                Báo lỗi &amp; góp ý
              </h2>
              <button type="button" onClick={close} className="text-slate-400 hover:text-white">
                <X size={20} />
              </button>
            </div>
            {session && (
              <Link href="/bao-loi-cua-toi" className="mt-2 inline-block text-xs font-semibold text-cyan-300 hover:text-cyan-200">
                Xem các báo lỗi &amp; đề xuất đã gửi của tôi →
              </Link>
            )}

            <form onSubmit={submit} className="mt-4 space-y-3">
              <select value={category} onChange={(e) => setCategory(e.target.value as BugCategory)} className={inputCls}>
                {Object.entries(BUG_CATEGORY_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
              <textarea
                required
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Mô tả lỗi bạn gặp phải, hoặc tính năng bạn muốn đề xuất…"
                rows={4}
                className={inputCls}
              />
              {!session && (
                <div className="grid gap-3 sm:grid-cols-2">
                  <input value={reporterName} onChange={(e) => setReporterName(e.target.value)} placeholder="Họ tên (không bắt buộc)" className={inputCls} />
                  <input value={reporterEmail} onChange={(e) => setReporterEmail(e.target.value)} placeholder="Email để liên hệ lại (không bắt buộc)" className={inputCls} />
                </div>
              )}
              <label className="flex cursor-pointer items-center gap-2 rounded-xl border border-dashed border-white/15 px-4 py-2.5 text-sm text-slate-400 hover:border-white/30">
                <Paperclip size={15} />
                {file ? file.name : "Đính kèm ảnh chụp màn hình (không bắt buộc)"}
                <input type="file" accept="image/*" className="hidden" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
              </label>
              {error && <p className="text-sm text-red-400">{error}</p>}
              <button type="submit" disabled={busy || !description.trim()} className="w-full rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-50">
                {busy ? "Đang gửi…" : "Gửi"}
              </button>
            </form>
          </section>
        </div>
      )}
    </>
  );
}
