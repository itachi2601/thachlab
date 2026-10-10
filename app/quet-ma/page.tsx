"use client";

import dynamic from "next/dynamic";
import { useCallback, useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { Keyboard } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import { examIdFromScan, examTakePath } from "@/lib/exam-link";

/**
 * app/quet-ma/page.tsx — mục QUÉT MÃ QR của học sinh.
 *
 * Thầy soạn đề rồi chiếu mã QR lên bảng (`components/admin/ExamQrPanel.tsx`); học sinh vào đây
 * quét là mở đúng đề, không phải gõ link dài.
 *
 * Hai đường vào đề, cố ý để cả hai (N3 — đừng để học sinh bí):
 *  1. quét mã bằng camera;
 *  2. gõ số đề — máy không có camera, camera hỏng, hoặc mã trên bảng bị lấp.
 *
 * Phần camera tải chậm (`next/dynamic ssr:false`) và bọc `LazyErrorBoundary`: bộ giải mã QR không
 * nằm trong JS ban đầu, và lỗi tải chunk chỉ hỏng đúng khung camera, ô gõ mã vẫn dùng được.
 *
 * Quy tắc thiết kế (docs/QUY-TAC-THIET-KE.md): N1 một màn một việc, B2 một điểm nổi bật (mã QR là
 * chính, ô gõ mã hạ cấp), D2 nút ≥ 44px, D4 chữ ngắn, M2 tương phản đủ.
 */

const QrScannerCard = dynamic(() => import("@/components/scan/QrScannerCard"), {
  ssr: false,
  loading: () => (
    <p className="mx-auto max-w-sm rounded-2xl border border-white/10 bg-panel p-6 text-center text-sm text-slate-400">
      Đang tải phần quét mã…
    </p>
  ),
});

export default function ScanExamPage() {
  const router = useRouter();
  const [manual, setManual] = useState("");
  const [error, setError] = useState("");

  const open = useCallback(
    (raw: string) => {
      const id = examIdFromScan(raw);
      if (!id) {
        setError("Mã này không phải mã đề của ThachLab. Em thử lại, hoặc gõ số đề thầy ghi trên bảng.");
        return;
      }
      setError("");
      router.push(examTakePath(id));
    },
    [router],
  );

  function submitManual(e: FormEvent) {
    e.preventDefault();
    open(manual);
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-2xl px-6 pt-28 pb-24 lg:px-8">
        <h1 className="font-display text-2xl font-bold text-white sm:text-3xl">Quét mã QR của đề</h1>
        <p className="mt-2 text-sm text-slate-400">
          Thầy chiếu mã QR lên bảng, em quét là vào đúng đề đó. Không quét được thì gõ số đề ở ô dưới.
        </p>

        <div className="mt-6">
          <LazyErrorBoundary
            fallback={
              <p role="alert" className="mx-auto max-w-sm rounded-2xl border border-white/10 bg-panel p-6 text-center text-sm text-slate-300">
                Không tải được phần quét mã (có thể do mạng chập chờn). Em gõ số đề ở ô bên dưới nhé.
              </p>
            }
          >
            <QrScannerCard onResult={open} />
          </LazyErrorBoundary>
        </div>

        <form onSubmit={submitManual} className="mt-8 rounded-2xl border border-white/10 bg-panel p-4">
          <label htmlFor="ma-de" className="flex items-center gap-2 text-sm font-semibold text-slate-300">
            <Keyboard size={16} /> Gõ số đề
          </label>
          <p className="mt-1 text-xs text-slate-500">Số đề là số thầy ghi trên bảng, ví dụ 770.</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <input
              id="ma-de"
              value={manual}
              onChange={(e) => setManual(e.target.value)}
              inputMode="numeric"
              autoComplete="off"
              placeholder="Ví dụ: 770"
              className="min-h-12 min-w-0 flex-1 basis-40 rounded-xl border border-white/10 bg-white/5 px-3 text-base text-white placeholder:text-slate-500 focus:border-primary focus:outline-none"
            />
            <button
              type="submit"
              className="min-h-12 rounded-xl border border-white/15 px-5 text-sm font-semibold text-white hover:border-white/30"
            >
              Mở đề
            </button>
          </div>
        </form>

        {error && (
          <p role="alert" className="mt-4 text-center text-sm text-amber-300">
            {error}
          </p>
        )}
      </main>
      <Footer variant="app" />
    </>
  );
}
