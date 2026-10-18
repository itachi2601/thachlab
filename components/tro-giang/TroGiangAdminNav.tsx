"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { CheckSquare, Clock, Drama, Video, Wallet, type LucideIcon } from "lucide-react";
import { setTaDemoMode } from "@/lib/tro-giang/demo";
import { getSupabase } from "@/services/supabase";

/** Phát sau khi duyệt/từ chối/trả phiếu để thanh điều hướng đếm lại số phiếu chờ. */
export const TA_PENDING_CHANGED = "ta-pending-changed";

const SECTIONS: { href: string; label: string; hint: string; icon: LucideIcon; badge?: boolean }[] = [
  { href: "/quan-tri/tro-giang", label: "Duyệt buổi", hint: "Việc cần xử lý hằng ngày", icon: CheckSquare, badge: true },
  { href: "/quan-tri/tro-giang/luong-thang", label: "Chấm điểm & lương", hint: "Chốt tháng cho từng trợ giảng", icon: Wallet },
  { href: "/quan-tri/tro-giang/video", label: "Video TikTok", hint: "Chi phí, thưởng, học sinh đăng ký", icon: Video },
  { href: "/quan-tri/tro-giang/gio-doi", label: "Giờ cả đội", hint: "Tổng giờ và ngưỡng của khoá", icon: Clock },
];

export default function TroGiangAdminNav() {
  const pathname = usePathname().replace(/\/$/, "");
  const [pending, setPending] = useState<number | null>(null);

  const loadPending = useCallback(() => {
    getSupabase()
      .from("ta_sessions")
      .select("id", { count: "exact", head: true })
      .eq("status", "submitted")
      .then(({ count }) => setPending(count ?? 0));
  }, []);

  useEffect(() => {
    loadPending();
    window.addEventListener(TA_PENDING_CHANGED, loadPending);
    return () => window.removeEventListener(TA_PENDING_CHANGED, loadPending);
  }, [loadPending]);

  const current = SECTIONS.find((s) => s.href === pathname) ?? SECTIONS[0];

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <nav aria-label="Các mục quản trị trợ giảng" className="flex flex-wrap gap-2">
          {SECTIONS.map((s) => {
            const active = s.href === current.href;
            const Icon = s.icon;
            return (
              <Link
                key={s.href}
                href={s.href}
                aria-current={active ? "page" : undefined}
                className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-bold transition ${
                  active ? "bg-primary text-white" : "bg-white/5 text-slate-300 hover:bg-white/10"
                }`}
              >
                <Icon size={15} />
                {s.label}
                {s.badge && pending ? (
                  <span className="rounded-full bg-amber-400 px-2 py-0.5 text-[12px] font-bold text-slate-900">{pending}</span>
                ) : null}
              </Link>
            );
          })}
        </nav>

        {/* Mở giao diện trợ giảng với một hồ sơ giả lập — không đọc/ghi dữ liệu thật. */}
        <Link
          href="/tro-giang?gialap=1"
          onClick={() => setTaDemoMode(true)}
          className="ml-auto flex items-center gap-2 rounded-xl border border-fuchsia-400/30 bg-fuchsia-500/10 px-4 py-2 text-sm font-bold text-fuchsia-200 transition hover:border-fuchsia-400/60"
        >
          <Drama size={15} />
          Xem trước giao diện trợ giảng
        </Link>
      </div>
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="font-display text-xl font-bold text-white">{current.label}</h1>
        <p className="text-sm text-slate-400">{current.hint}</p>
      </div>
      <Link
        href="/tro-giang/quy-che"
        className="block rounded-xl border border-blue-400/25 bg-blue-500/5 p-3 text-sm text-blue-200"
      >
        Quy chế mới từ 01/10/2026 · tháng 10 chưa giảm lương · xem chi tiết
      </Link>
    </div>
  );
}
