"use client";

import { useEffect, useState, type ComponentType } from "react";
import Link from "next/link";
import { useAuth, useAuthSnapshot } from "@/components/auth/auth-context";

/**
 * Chỉ admin thấy khối này trên trang chủ. Khách và học sinh không tải phần bảng (chunk riêng).
 * Trạng thái đăng nhập hiện ngay từ hồ sơ; bảng việc nạp sau.
 */
export default function AdminHomeToday() {
  const live = useAuth();
  const snap = useAuthSnapshot();
  const profile = live.profile ?? snap.profile;
  const [Board, setBoard] = useState<ComponentType | null>(null);

  useEffect(() => {
    if (profile?.role !== "admin") return;
    let cancelled = false;
    import("./AdminTodayBoard").then((mod) => {
      if (!cancelled) setBoard(() => mod.default);
    });
    return () => {
      cancelled = true;
    };
  }, [profile?.role]);

  useEffect(() => {
    if (profile?.role !== "admin") return;
    document.documentElement.setAttribute("data-admin-board", "");
    return () => document.documentElement.removeAttribute("data-admin-board");
  }, [profile?.role]);

  if (profile?.role !== "admin") return null;

  const name = profile.full_name?.trim() || "Quản trị viên";

  return (
    <section aria-label="Việc của quản trị" className="relative z-10 bg-bg px-6 pt-24 lg:px-12">
      <style>{`html[data-admin-board] #thpt{padding-top:1rem}@media (min-width:640px){html[data-admin-board] #thpt{padding-top:1.5rem}}`}</style>
      <div className="mx-auto max-w-6xl rounded-2xl border border-line bg-panel p-4 sm:p-5">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
          <p className="inline-flex items-center gap-2 text-sm font-semibold text-ink">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" aria-hidden />
            Đã đăng nhập
          </p>
          <p className="text-sm text-muted">
            {name} · Quản trị viên
          </p>
          <Link href="/quan-tri" className="text-sm font-semibold text-primary hover:underline">
            Vào quản trị
          </Link>
        </div>
        {Board ? <Board /> : <p className="mt-3 text-sm text-muted">Đang lấy việc hôm nay…</p>}
      </div>
    </section>
  );
}
