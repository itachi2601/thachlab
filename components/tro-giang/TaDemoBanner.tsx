"use client";

import Link from "next/link";
import { Drama, LogOut } from "lucide-react";
import { setTaDemoMode } from "@/lib/tro-giang/demo";

/**
 * raised: trang /tro-giang/ghi đã có thanh "Lưu buổi" dán đáy màn hình — đẩy banner lên trên nó.
 *
 * Thanh nổi báo cho giáo viên biết đang xem bản giả lập — mọi số trên màn hình là số mẫu,
 * form ghi buổi cũng không ghi gì vào database. Bấm "Thoát" để về khu quản trị.
 */
export default function TaDemoBanner({ raised = false }: { raised?: boolean }) {
  return (
    <div
      className={`fixed inset-x-0 z-50 flex flex-wrap items-center justify-center gap-2 border-t border-fuchsia-400/30 bg-[#0B1020]/95 px-4 py-2.5 text-xs font-bold text-fuchsia-200 backdrop-blur-md ${
        raised ? "bottom-[88px]" : "bottom-0"
      }`}
    >
      <Drama size={15} />
      Đang xem giao diện trợ giảng (giả lập) — số liệu là mẫu, không lưu gì cả
      <Link
        href="/quan-tri/tro-giang"
        onClick={() => setTaDemoMode(false)}
        className="flex items-center gap-1 rounded-full border border-white/15 px-2.5 py-1 text-slate-300 hover:border-white/30"
      >
        <LogOut size={12} /> Thoát
      </Link>
    </div>
  );
}
