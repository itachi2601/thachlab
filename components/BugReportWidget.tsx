"use client";

import { useEffect, useRef, useState } from "react";
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

// Nút nổi kéo lên/xuống để khỏi che nút bấm của trang. Vị trí lưu trên máy em (localStorage), không gửi đi đâu.
const POSITION_KEY = "bug-fab-bottom";
const DRAG_THRESHOLD = 6;
const STEP = 24;

function clampBottom(px: number): number {
  const min = window.matchMedia("(max-width: 1023px)").matches ? 76 : 8;
  const max = Math.max(min, window.innerHeight - 56);
  return Math.min(max, Math.max(min, Math.round(px)));
}

export default function BugReportWidget() {
  const { session } = useAuth();
  const toast = useToast();
  const [open, setOpen] = useState(false);
  // null = vị trí mặc định theo CSS (.bug-fab, né thanh đáy trên điện thoại); có số = em đã kéo.
  const [bottomPx, setBottomPx] = useState<number | null>(null);
  const fabRef = useRef<HTMLButtonElement>(null);
  const drag = useRef<{ startY: number; startBottom: number; moved: boolean } | null>(null);
  const justDragged = useRef(false);

  useEffect(() => {
    try {
      const saved = Number(window.localStorage.getItem(POSITION_KEY));
      // Đọc sau khi mount (không đọc lúc render) để HTML server và lần render đầu của client khớp nhau.
      // eslint-disable-next-line react-hooks/set-state-in-effect
      if (saved > 0) setBottomPx(clampBottom(saved));
    } catch {
      // Trình duyệt chặn localStorage thì dùng vị trí mặc định.
    }
  }, []);

  function currentBottom(): number {
    const rect = fabRef.current?.getBoundingClientRect();
    return rect ? window.innerHeight - rect.bottom : 20;
  }

  function savePosition(px: number) {
    try {
      window.localStorage.setItem(POSITION_KEY, String(px));
    } catch {
      // Không lưu được thì thôi, lần sau về vị trí mặc định.
    }
  }

  function onPointerDown(e: React.PointerEvent<HTMLButtonElement>) {
    drag.current = { startY: e.clientY, startBottom: currentBottom(), moved: false };
    justDragged.current = false;
  }

  function onPointerMove(e: React.PointerEvent<HTMLButtonElement>) {
    const d = drag.current;
    if (!d) return;
    const dy = e.clientY - d.startY;
    if (!d.moved && Math.abs(dy) < DRAG_THRESHOLD) return;
    if (!d.moved) {
      // Chỉ "bắt" con trỏ khi thật sự kéo: bắt ngay lúc chạm làm WebView cũ (Zalo/Facebook) nuốt cú bấm.
      try {
        e.currentTarget.setPointerCapture(e.pointerId);
      } catch {
        // WebView không hỗ trợ thì vẫn kéo được trong phạm vi nút.
      }
    }
    d.moved = true;
    setBottomPx(clampBottom(d.startBottom - dy));
  }

  function onPointerUp() {
    const d = drag.current;
    drag.current = null;
    if (!d?.moved) return;
    justDragged.current = true;
    savePosition(Math.round(currentBottom()));
  }

  function onClick() {
    // Thả tay sau khi kéo không được tính là bấm mở form.
    if (justDragged.current) {
      justDragged.current = false;
      return;
    }
    setOpen(true);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLButtonElement>) {
    if (e.key !== "ArrowUp" && e.key !== "ArrowDown") return;
    e.preventDefault();
    const next = clampBottom(currentBottom() + (e.key === "ArrowUp" ? STEP : -STEP));
    setBottomPx(next);
    savePosition(next);
  }


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
        // Kèm hash: trang lý thuyết dùng #theory-sec-<itemId>-<n> để nhảy đúng đoạn,
        // thiếu hash thì link trong báo lỗi chỉ mở tới đầu trang.
        pageUrl: window.location.pathname + window.location.search + window.location.hash,
        userId: session?.user.id ?? null,
        reporterName: session ? "" : reporterName,
        reporterEmail: session ? "" : reporterEmail,
        file,
      });
      toast("success", "Đã gửi, cảm ơn bạn!");
      close();
    } catch (cause) {
      // Lỗi của Supabase là object thường (không phải Error) nên đọc .message thay vì rơi về câu chung chung.
      const msg = (cause as { message?: unknown } | null)?.message;
      setError(typeof msg === "string" && msg ? `Không gửi được: ${msg}` : "Không gửi được, thử lại sau.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <button
        ref={fabRef}
        type="button"
        onClick={onClick}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        onKeyDown={onKeyDown}
        style={bottomPx === null ? undefined : { bottom: bottomPx }}
        title="Kéo lên xuống để dời nút; bấm để báo lỗi"
        aria-label="Báo lỗi / góp ý. Kéo lên xuống để dời nút, hoặc dùng phím mũi tên."
        className="bug-fab fixed bottom-5 right-5 z-40 flex min-h-11 touch-none select-none items-center gap-2 rounded-full border border-white/15 bg-panel/95 px-4 py-2.5 text-xs font-bold text-slate-200 shadow-xl backdrop-blur-md hover:border-white/30"
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
                {Object.entries(BUG_CATEGORY_LABELS)
                // "cau_hoi" chỉ dành cho nút "Báo lỗi câu này" (có gắn exam_id/question_index) —
                // chọn ở form chung sẽ ra báo lỗi câu hỏi không biết câu nào.
                .filter(([value]) => value !== "cau_hoi")
                .map(([value, label]) => (
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
                <input type="file" accept="image/png,image/jpeg,image/webp,image/heic,image/heif" className="hidden" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
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
