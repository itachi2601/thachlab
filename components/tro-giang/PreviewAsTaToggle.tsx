"use client";

import Link from "next/link";
import { Drama } from "lucide-react";
import { useAuth } from "@/components/auth/auth-context";
import { setTaDemoMode, useTaDemoMode } from "@/lib/tro-giang/demo";

/**
 * Nút nổi cho admin: lối vào nhanh "Xem như trợ giảng" từ bất kỳ trang nào — giống hệt
 * nút "Xem như học sinh" (xem components/auth/PreviewAsStudentToggle.tsx) nhưng bật cờ
 * giả lập trợ giảng (lib/tro-giang/demo.ts) rồi mở /tro-giang?gialap=1. Trạng thái
 * "đang xem" + nút thoát đã có sẵn ở TaDemoBanner.tsx ngay trên trang /tro-giang nên
 * nút này tự ẩn khi chế độ giả lập đang bật.
 */
export default function PreviewAsTaToggle() {
  const { realProfile, previewAsStudent } = useAuth();
  const [taDemo] = useTaDemoMode();

  if (realProfile?.role !== "admin") return null;
  // Đang xem giả lập học sinh hoặc trợ giảng rồi — tránh chồng nút/banner.
  if (previewAsStudent || taDemo) return null;

  return (
    <Link
      href="/tro-giang?gialap=1"
      onClick={() => setTaDemoMode(true)}
      className="fixed bottom-5 right-5 z-50 flex items-center gap-2 rounded-full border border-white/15 bg-panel/95 px-4 py-2.5 text-xs font-bold text-slate-200 shadow-xl backdrop-blur-md hover:border-white/30"
    >
      <Drama size={15} className="text-fuchsia-300" />
      Xem như trợ giảng
    </Link>
  );
}
