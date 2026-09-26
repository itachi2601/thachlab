"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Drama, LogOut, Wrench } from "lucide-react";
import { useAuth } from "@/components/auth/auth-context";
import { useTaDemoMode } from "@/lib/tro-giang/demo";
// previewCttcEnroll/previewCttcUnenroll (services/preview-cttc.ts) gọi supabase — import
// ĐỘNG trong enterCttc/exitCttc bên dưới, vì component này render ở MỌI trang kể cả
// trang công khai (qua PublicShell.tsx); import thẳng ở đây sẽ luôn kéo theo
// @supabase/supabase-js dù component return null ngay (không phải admin) trên các trang đó.

/**
 * Nút nổi cho admin, hai chế độ:
 *
 * - "Xem như học sinh": AuthProvider ghi đè profile.role thành "student" (chỉ trên trình
 *   duyệt, không đổi session). Học sinh giả lập dùng chính user_id của admin nên vào
 *   /tai-khoan sẽ thấy màn "Bạn đang học ở đâu?" (tài khoản admin không thuộc lớp nào).
 *
 * - "Xem như SV CTTC (3 môn)": gọi RPC preview_cttc_enroll ghi danh CHÍNH tài khoản admin
 *   vào khóa mới nhất của CNC · Tiện phay · SHCN (status active), rồi ghi đè role=student +
 *   track=cttc. Mọi trang sinh viên chạy đúng đường thật (RLS thật, dữ liệu thật) — điểm danh,
 *   làm bài… ghi dưới user_id của admin. Bấm Thoát thì gỡ 3 ghi danh này để admin không nằm
 *   trong danh sách lớp nữa.
 */
export default function PreviewAsStudentToggle() {
  const router = useRouter();
  const { realProfile, previewMode, setPreviewMode } = useAuth();
  const [taDemo] = useTaDemoMode();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  if (realProfile?.role !== "admin") return null;
  // Đang xem giả lập trợ giảng — banner của chế độ đó chiếm chỗ này rồi.
  if (taDemo) return null;

  async function enterCttc() {
    setBusy(true);
    setError("");
    try {
      const { previewCttcEnroll } = await import("@/services/preview-cttc");
      const courses = await previewCttcEnroll();
      const missing = courses.filter((c) => !c.course_id).map((c) => c.subject);
      if (missing.length) setError(`Chưa có khóa đang mở cho: ${missing.join(", ")}`);
      setPreviewMode("cttc");
      router.push("/tai-khoan");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Không ghi danh thử được.");
    } finally {
      setBusy(false);
    }
  }

  async function exitCttc() {
    setBusy(true);
    setError("");
    try {
      const { previewCttcUnenroll } = await import("@/services/preview-cttc");
      await previewCttcUnenroll();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Không gỡ ghi danh thử được.");
    } finally {
      setBusy(false);
      setPreviewMode(null);
    }
  }

  const pill =
    "flex items-center gap-2 rounded-full border px-4 py-2.5 text-xs font-bold shadow-xl backdrop-blur-md";

  if (!previewMode) {
    return (
      <div className="fixed bottom-5 left-5 z-50 flex flex-col items-start gap-2">
        {error && <p className="max-w-xs rounded-xl bg-rose-500/15 px-3 py-2 text-xs text-rose-200">{error}</p>}
        <button
          type="button"
          onClick={() => setPreviewMode("student")}
          className={`${pill} border-white/15 bg-panel/95 text-slate-200 hover:border-white/30`}
        >
          <Drama size={15} className="text-fuchsia-300" />
          Xem như học sinh
        </button>
        <button
          type="button"
          disabled={busy}
          onClick={() => void enterCttc()}
          className={`${pill} border-orange-400/25 bg-panel/95 text-orange-100 hover:border-orange-400/50 disabled:opacity-60`}
        >
          <Wrench size={15} className="text-orange-300" />
          {busy ? "Đang ghi danh 3 môn…" : "Xem như SV CTTC (CNC · Tiện phay · SHCN)"}
        </button>
      </div>
    );
  }

  if (previewMode === "cttc") {
    const link = "rounded-full bg-orange-500/15 px-2.5 py-1 text-orange-100 hover:bg-orange-500/25";
    return (
      <div className="fixed bottom-5 left-5 z-50 flex flex-col items-start gap-2">
        {error && <p className="max-w-xs rounded-xl bg-rose-500/15 px-3 py-2 text-xs text-rose-200">{error}</p>}
        <div className={`${pill} flex-wrap border-orange-400/30 bg-panel/95 text-orange-200`}>
          <Wrench size={15} />
          Đang xem như SV CTTC (giả lập)
          <Link href="/tai-khoan" className={link}>SHCN</Link>
          <Link href="/lop-hoc/cnc" className={link}>CNC</Link>
          <Link href="/lop-hoc/tien-phay" className={link}>Tiện phay</Link>
          <button
            type="button"
            disabled={busy}
            onClick={() => void exitCttc()}
            className="flex items-center gap-1 rounded-full border border-white/15 px-2.5 py-1 text-slate-300 hover:border-white/30 disabled:opacity-60"
          >
            <LogOut size={12} /> {busy ? "Đang gỡ…" : "Thoát"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`fixed bottom-5 left-5 z-50 ${pill} border-fuchsia-400/30 bg-panel/95 text-fuchsia-200`}>
      <Drama size={15} />
      Đang xem giao diện học sinh (giả lập)
      <Link
        href="/tai-khoan"
        className="rounded-full bg-fuchsia-500/15 px-2.5 py-1 text-fuchsia-100 hover:bg-fuchsia-500/25"
      >
        Vào /tai-khoan
      </Link>
      <button
        type="button"
        onClick={() => setPreviewMode(null)}
        className="flex items-center gap-1 rounded-full border border-white/15 px-2.5 py-1 text-slate-300 hover:border-white/30"
      >
        <LogOut size={12} /> Thoát
      </button>
    </div>
  );
}
